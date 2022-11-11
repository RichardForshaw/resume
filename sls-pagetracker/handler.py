import json
import os
import re
from datetime import datetime
from itertools import chain

from botocore.exceptions import ClientError
import boto3

S3_LOG_TS_FORMAT = '[%d/%b/%Y:%H:%M:%S %z]'

# The tuple defining what to get from the aws s3 log string
DYNAMO_FIELDS_TUPLE = (
    (7, 'UserPages', 'S'),      # PartitionKey: User and Page
    (2, 'SortKey', 'S'),        # Sort Key: Timestamp
    (16, 'AgentString', 'S'),   # Agent Access String
    (13, 'ServiceTime', 'N'),   # Page Access Time
    (3, 'RemoteAddress', 'S')
)

def handle_s3_view_log(event, context):
    # Handler which parses the content of the new object and writes to Dynamo
    # Important fields (Note there could be multiple records):
    # event['Records'][0]['s3']: The s3 information
    # event['Records'][0]['s3']['bucket']['name']
    # event['Records'][0]['s3']['object']['key']
    print(f"S3 event has {len(event['Records'])} record(s)")
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    # Parameters from environment
    try:
        expected_www_bucket = os.environ['WWW_BUCKET_NAME']
        expected_path = os.environ['PATH_PREFIX']
        dynamo_table_name = os.environ['TARGET_DYNAMO_TABLE']
    except KeyError:
        print("IMPROPERLY CONFIGURED: Could not access expected environment variables BUCKET_NAME and PATH_PREFIX")
        return False

    # open and parse
    # TODO: Multiple files
    log_data = read_strings_from_s3_object(bucket_name, object_key)
    print(f"Scan complete: {len(log_data)} entries loaded.")

    if not log_data:
        print(f"No page data could be loaded for {object_key}. Exiting.")
        return

    # Run extraction
    parse_config = {
        'bucket_name': expected_www_bucket,
        'folder_prefix': expected_path,
        'file_filter': 'index.html',
        'pk_format': 'Richard#{}'
    }
    print(f"Parsing config: {parse_config}")

    # Add translations here because it can't be printed
    parse_config['translations'] = {
        # Convert timestamp to epoch
        'SortKey': lambda x: str(int(datetime.strptime(x, S3_LOG_TS_FORMAT).timestamp())),
        # Strip index.html from page name
        'UserPages': lambda x: re.sub(r'index\.html', '', x)
    }
    table_data = parse_s3_logs_to_dynamo(log_data, DYNAMO_FIELDS_TUPLE, **parse_config)

    matched_pages = []
    if len(table_data):
        matched_pages = [item['UserPages']['S'] for item in table_data]
        print(f"Matched data for pages:\n" + ('\n').join(matched_pages))
        print(table_data[0])
    else:
        print(f'No items from {object_key} were matched')

    # Write to dynamo. Currently one call per item.
    dynamo_client = boto3.client('dynamodb')
    for item in table_data:
        # Add in an attribute for the key source
        item['SourceObject'] = {'S': object_key}
        try:
            dynamo_client.put_item(TableName=dynamo_table_name, Item=item)
        except Exception as e:
            print(f"Failed to write {item['UserPages']} record to Dynamo")
            print(e)

    # Write page index to Dynamo
    for page in set(matched_pages):
        item = { 'UserPages': {'S': 'Richard#INDEX'}, 'SortKey': {'S': page} }
        try:
            dynamo_client.put_item(
                TableName=dynamo_table_name,
                Item=item,
                ConditionExpression="attribute_not_exists(SortKey)")
            print(f"Wrote new INDEX record: {page}")
        except ClientError as ce:
            # Probably means that the record already exists
            if ce.response['Error']['Code'] =='ConditionalCheckFailedException':
                # Do Nothing
                pass
            else:
                print(f'Got unexpected ClientError:')
                print(ce)
        except Exception as e:
            print(f"Failed to write {item} record to Dynamo")
            print(e)


def read_strings_from_s3_object(bucket_name, object_key):
    ''' Given a S3 bucket name and object key, read the contents and return an array of strings.'''
    s3 = boto3.client('s3')
    try:
        data = s3.get_object(Bucket=bucket_name, Key=object_key)['Body'].read()
    except Exception as e:
        print(f"Unable to read {object_key} from {bucket_name}")
        print(e)
        data = ''

    # Parse the data: Convert from bytes to string and split
    if isinstance(data, bytes):
        data = str(data, 'utf-8', 'ignore')
    return data.splitlines()


def parse_log_string_to_dynamo(log_string, fields_tuples, pk_format=None, translations={}):
    ''' Parse an AWS log string to a dynamo dictionary.
        The log string follows the format defined here: https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html

        The fields_tuples is a tuple of 3-tuples which define the index, target field name and type
        of the field to be extracted, such as:
        (1, 'BucketName', 'S') or (9, 'HTTPResult', 'N')

        Structured field names can be provided in pk_format and sk_format. If provided:
         - pk_format will provide the string format to write the partition key value, assumed to be
           the first item in fields_tuples
         - sk_format will provide the string format to write the sort key value, assumed to be the
           second item in fields_tuples
         - translations is a dict of translations to apply to field names. These will run on the
           field, before any formatting takes place

    '''
    def not_blank(s):
        return s != ' ' and s != ''

    # Parse the string into a tuple of entries
    fields = list(filter(not_blank, re.split(r'( |["\[].*?["\]])', log_string)))

    # Extract the fields as per the spec
    def extract_field(idx, name, type):
        field = fields[idx].strip('"')
        t = translations.get(name)
        if t:
            field = t(field)

        # Note that numbers must be sent as strings, so force the conversion here
        return (name, {type: str(field) if type in ['S', 'N'] else field})

    data = dict(extract_field(*field_spec) for field_spec in fields_tuples)

    # Format the PK if requested
    if pk_format:
        pk_data = fields_tuples[0]
        data[pk_data[1]][pk_data[2]] = pk_format.format(data[pk_data[1]][pk_data[2]])

    return data


def parse_s3_logs_to_dynamo(log_data, field_tuples, bucket_name='', folder_prefix='', file_filter='', **kwargs):
    ''' Parse a list of log strings and return a list of equivalent dynamo records to write
        Options:
         - bucket_name: the expected name of the bucket being accessed
         - folder_prefix: the prefix folder to the GET operations. This filters anything starting
                with GET /folder_prefix/something...
         - file_filter: only match access to certain files. Often in blogs, the blog entries are served
                as an access to a directory, thus this allows the log to be filtered on requests
                for 'index.html' or similar
         - kwargs: All other arguments are sent to the log string parser

        Notes:
         - The log strings are either a list of strings or a single string separated by newlines
         - This function will ONLY parse 'GET.OBJECT' operations
         - The function is reliant on the current AWS access log format (see parse_log_string_to_dynamo)

    '''
    # Ensure folder name has trailing slash
    if len(folder_prefix) and folder_prefix[-1] != '/':
        folder_prefix += '/'

    # Work internally with a list of strings
    if isinstance(log_data, str):
        log_data = log_data.splitlines()

    # Filter anything not matching GET.OBJECT. Include a folder prefix if present
    # NOTE this currently relies on the log format maintaining the current field ordering
    # REGEX explanation:
    #  - Match bucket name if given
    #  - Match anything then ".GET.OBJECT " literal (note space)
    #  - Match the folder prefix if given
    #  - Match any non-whitespace
    #  - Match the file filter before the next whitespace
    filter_match = bucket_name + r".*\.GET\.OBJECT " + folder_prefix + r"\S*" + file_filter
    print(f"Filtering logs with expression: {filter_match}")
    r = re.compile(filter_match)
    valid_strings = filter(r.search, log_data)

    # Call parsing function
    return [parse_log_string_to_dynamo(entry, field_tuples, **kwargs) for entry in valid_strings]
