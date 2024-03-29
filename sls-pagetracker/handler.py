import json
import os
import re
import base64
from urllib import parse
from datetime import datetime
from collections import Counter
from functools import reduce

from botocore.exceptions import ClientError
import boto3

from dynamo_helpers import (
    query_page_index_params,
    count_page_visits_params,
    query_page_visits_params,
    query_page_counters_params,
    update_page_totals_counter_params,
    update_page_visits_counter_params
)

from helpers import parse_date_string_or_timestamp, sparse_dict_to_array

S3_LOG_TS_FORMAT = '[%d/%b/%Y:%H:%M:%S %z]'

# SortKey values and prefixes for indicating a specific metrics
# IMPORTANT: This must come AFTER the digits in the ascii table
SK_CLASS_PREFIX = ":"
SK_SHARE_PREFIX = SK_CLASS_PREFIX + "SHARE#"


# The tuple defining what to get from the aws s3 log string
DYNAMO_FIELDS_TUPLE = (
    (7, 'UserPages', 'S'),      # PartitionKey: User and Page
    (2, 'SortKey', 'S'),        # Sort Key: Timestamp
    (16, 'AgentString', 'S'),   # Agent Access String
    (13, 'ServiceTime', 'N'),   # Page Access Time
    (3, 'RemoteAddress', 'S'),
    (15, 'Referrer', 'S')        # The page that referred this request
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
        dynamo_table_name = os.environ['TARGET_DYNAMO_TABLE']
    except KeyError:
        print("IMPROPERLY CONFIGURED: Could not access expected environment variables BUCKET_NAME and TARGET_DYNAMO_TABLE")
        return False

    # PATH_PREFIX is optional
    expected_path = os.environ.get('PATH_PREFIX','')
    if expected_path == '':
        print("No PATH_PREFIX variable found. Not using path prefix.")

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
    print(f"Processing object: {object_key}")

    # Add translations here because it can't be printed
    parse_config['translations'] = {
        # Convert timestamp to epoch
        'SortKey': lambda x: str(int(datetime.strptime(x, S3_LOG_TS_FORMAT).timestamp())),
        # Strip index.html from page name
        'UserPages': lambda x: re.sub(r'index\.html', '', x)
    }
    table_data = parse_s3_logs_to_dynamo(log_data, DYNAMO_FIELDS_TUPLE, **parse_config)

    # Add custom field
    for item in table_data:
        # Add in an attribute for the key source
        item['SourceObject'] = {'S': object_key}

    matched_pages = []
    if len(table_data):
        matched_pages = [item['UserPages']['S'] for item in table_data]
        print(f"Matched data in {object_key} for pages:\n" + ('\n').join(matched_pages))
        print(table_data[0])
    else:
        print(f'No items from {object_key} were matched')
        return

    # Write to dynamo. Currently one call per item.
    if len(table_data) < 4:
        dynamo_write_simple_items(dynamo_table_name, table_data)
    else:
        dynamo_write_batched_items(dynamo_table_name, table_data)

    # Perform all increment operations
    # This could be done as a batch transaction item, but it is all-or-nothing
    dynamo_client = boto3.client('dynamodb')
    for user_page in set(matched_pages):
        page = user_page.split('#')[1].lower()

        if len(page):
            # Increment the total page count
            ts_list = [ int(item['SortKey']['S']) for item in table_data if item['UserPages']['S'] == user_page ]
            print(f"Processing page stats for {user_page}: {ts_list}")
            try:
                result = dynamo_client.update_item(
                    **update_page_totals_counter_params(dynamo_table_name, "Richard", page, ts_list),
                    ReturnValues="UPDATED_NEW")

                # Logging
                new_val = result['Attributes']
                print(f"Updated total count for (value: {new_val})")

            except Exception as e:
                print(f"Failed to increment total page counter for {page} in Dynamo")
                print(e)

            # Increment the daily page count
            try:
                result = dynamo_client.update_item(
                    **update_page_visits_counter_params(dynamo_table_name, "Richard", page, ts_list),
                    ReturnValues="UPDATED_NEW"
                )

                # Logging
                new_val = result['Attributes']
                print(f"Updated {page} access count (new value: {new_val})")

            except Exception as e:
                print(f"Failed to update daily counter for {page} in Dynamo")
                print(e)

    # Write page index to Dynamo - is this legacy now? Should use a set?
    # TODO: No need to do this. Can get the PAGES list instead and use the key names. That is if we need
    # to do this at all?
    for user_page in set(matched_pages):
        item = { 'UserPages': {'S': 'Richard#INDEX'}, 'SortKey': {'S': user_page} }
        try:
            dynamo_client.put_item(
                TableName=dynamo_table_name,
                Item=item,
                ConditionExpression="attribute_not_exists(SortKey)")
            print(f"Wrote new INDEX record: {user_page}")
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

def dynamo_write_simple_items(table_name, item_list):
    dynamo_client = boto3.client('dynamodb')
    for item in item_list:
        try:
            dynamo_client.put_item(TableName=table_name, Item=item)
        except Exception as e:
            print(f"Failed to write {item['UserPages']} record to Dynamo")
            print(e)

def dynamo_write_batched_items(table_name, item_list):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    with table.batch_writer(overwrite_by_pkeys=['UserPages', 'SortKey']) as batch:
        print(f"Batch-writing {len(item_list)} items...")
        for item in item_list:
            # So, using this method, there is no need to us the {'Type': Value } notation...
            # so we can undo it here
            raw_item = { k: list(v.values())[0] for k, v in item.items() }
            batch.put_item(Item=raw_item)

    print("Done...")

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

def return_400(reason):
    return {
        "isBase64Encoded": False,
        "statusCode": 400,
        "body": reason
    }

def return_404(reason):
    return {
        "isBase64Encoded": False,
        "statusCode": 404,
        "body": reason
    }

def handle_blog_page_count_totals(event, context):
    # Handler which parses the content of the new object and writes to Dynamo
    # Important fields (Note there could be multiple records):

    # Parameters from environment
    try:
        dynamo_table_name = os.environ['TARGET_DYNAMO_TABLE']
    except KeyError:
        print("IMPROPERLY CONFIGURED: Could not access expected environment variables BUCKET_NAME and PATH_PREFIX")
        return False

    # Get root query filter from environment
    path_filter = os.environ.get('DEFAULT_INDEX_PATH_QUERY', None)

    # This function has two optional parameters
    full_scan = False
    params = event.get('queryStringParameters')
    print(params)
    if params:
        # Assume that the first parameter is a user-requested path query for the count
        for param in iter(params.keys()):
            if param == "FULLSCAN":
                full_scan = True
            else:
                path_filter = param
    elif not path_filter:
        return return_400("No path filter parameter given and no default path filter configured")

    # Query the indexes from Dynamo
    client = boto3.client('dynamodb')
    if not full_scan:
        # Query the pages counters
        result = client.query(
            **query_page_counters_params(dynamo_table_name, "Richard"),
            ReturnConsumedCapacity="TOTAL"
        )

        # Construct results according to the path filter
        # User reduce with a counter to add up all the page totals
        def acc_totals(acc, item):
            acc.update({k: int(v['N']) for k, v in item.items() if k.startswith(path_filter)})
            return acc
        result_dict = dict(reduce(acc_totals, result['Items'], Counter()))

        total_consumed = result['ConsumedCapacity']['CapacityUnits']

        result_dict['TotalPageViews'] = sum(result_dict.values())

    else:
        # Perform a full scan and count for views
        result = client.query(**query_page_index_params(dynamo_table_name, "Richard", path_filter),
                            ReturnConsumedCapacity="TOTAL")

        # Now we must query for the items
        result_dict = {}
        total_consumed = result['ConsumedCapacity']['CapacityUnits']
        total_page_views = 0
        for item in result['Items']:
            # Remove the user prefix
            page_name = item['SortKey']['S'].split("#")[1]
            page_result = client.query(**count_page_visits_params(dynamo_table_name, "Richard", page_name),
                                    ReturnConsumedCapacity="TOTAL")

            print(page_result)
            if page_result['Count']:
                print(f"{page_name}: {page_result['Count']}")
                result_dict[page_name] = page_result['Count']
                total_page_views += page_result['Count']

            total_consumed += page_result['ConsumedCapacity']['CapacityUnits']

        # Show the total
        result_dict['TotalPageViews'] = total_page_views

    # Final results: also get the earliest blog access time
    page_result = client.query(TableName=dynamo_table_name,
                Limit=1,
                KeyConditionExpression="UserPages = :pk",
                ExpressionAttributeValues={ ":pk": {"S": "Richard#blog/"} },
                ReturnConsumedCapacity='TOTAL')

    total_consumed += page_result['ConsumedCapacity']['CapacityUnits']

    result_dict['DynamoConsumedCapacity'] = total_consumed
    result_dict['ResultsStartTime'] = page_result['Items'][0]['SortKey']['S']
    time_string = datetime.utcfromtimestamp(int(page_result['Items'][0]['SortKey']['S'])).strftime(S3_LOG_TS_FORMAT)
    result_dict['ResultsStartTimeString'] = time_string

    return result_dict

def between_fn(bottom_limit, top_limit):
    ''' Returns a function which detects if input x is between bottom_limit and top_limit, or ignores the
        limit if it is None
    '''
    def fn(x):
        if x > bottom_limit:
            if top_limit and x < top_limit:
                return True

        return False
    return fn

def handle_blog_page_visit_history(event, context):
    ''' Handler which returns a list of daily visit frequencies for a given page name request.
        Can take the following parameters:
          - page (required): url-identifier of the page. If there is an unnamed parameter, it is assumed to be this.
          - from_date: a YYYY-MM-DD date taken to be midnight GMT before which timestamps are culled
          - to_date: a YYYY-MM-DD date taken to be midnight GMT after which timestamps are culled
          - from_time: a timestamp value before which timestamps are culled. The timestamp is rounded down to a day.
          - to_time: a timestamp value after which timestamps are culled. The timestamp is rounded down to a day.

        Returned in the format:
        {
            PageName: the page name
            AccessFreq: [{
                YYYYMM: yyyymm
                DailyAccess: [list of daily access frequency in contiguous days]
            },
            ]
        }

        Note: Returning timestamps is not supported here, because timestamps are irregular and the intent
        is to present a regular frequency.
    '''
    print(event)

    # Parameters from environment
    try:
        dynamo_table_name = os.environ['TARGET_DYNAMO_TABLE']
    except KeyError:
        print("IMPROPERLY CONFIGURED: Could not access expected environment variables BUCKET_NAME and PATH_PREFIX")
        return False

    # This function expects at least one parameter
    params = event.get('queryStringParameters')
    print(params)
    if not params:
        return return_400("Request missing required parameter(s)")

    # Construct parameters
    page_param = None
    from_param = None
    to_param = None
    if params:
        # Look for start and end times
        from_param = parse_date_string_or_timestamp(params.pop('from_date', None), params.pop('from_time', None))
        to_param   = parse_date_string_or_timestamp(params.pop('to_date', None), params.pop('to_time', None))

        # page parameter
        page_param = next(iter(params.keys()))

    if not page_param:
        return return_400("Request missing required parameter(s)")

    # Construct query limits
    query_params = {}
    if from_param or to_param:
        print(f"Filtering timestamps between {from_param or 'earliest'} and {to_param or 'latest'}")
        query_params = { 'FromLimit': from_param, 'ToLimit': to_param}

    # Query dynamo page visits to return list of daily frequencies
    client = boto3.client('dynamodb')
    from_month = from_param[0] if from_param else None
    to_month = to_param[0] if to_param else None
    result = client.query(
                    **query_page_visits_params(dynamo_table_name, "Richard", page_param, from_month=from_month, to_month=to_month),
                    ReturnConsumedCapacity="TOTAL")

    if not result['Items']:
        return return_404(f"Page not found: {page_param}")

    # Convert the results into contiguous lists
    items = result['Items']
    print(f"Result for {page_param} begins: {items[0]}")
    access_list = [
        {
            "YYYYMM": i['SortKey']['S'].split("#")[1],
            "DailyAccess": sparse_dict_to_array({k[1:]: v['N'] for k, v in i.items() if k.startswith("D")}, offset=1)
        } for i in items
    ]

    return {
        'PageName': page_param,
        'AccessFreq': access_list,
        'QueryParameters': query_params,
        'DynamoConsumedCapacity': result['ConsumedCapacity']['CapacityUnits'] }

def handle_page_share(event, context):
    ''' Handler which reports a sharing event to Dynamo '''
    print(event)

    try:
        dynamo_table_name = os.environ['TARGET_DYNAMO_TABLE']
    except KeyError:
        print("IMPROPERLY CONFIGURED: Could not access expected environment variables BUCKET_NAME and PATH_PREFIX")
        return False

    # This function expects at least one parameter
    params = event.get('queryStringParameters')
    print(params)
    if not params:
        # Check for encoded form parameters
        form_body = event.get('body')
        if form_body:
            print("Extracting parameters from POST body")
            if event.get('isBase64Encoded', False):
                form_body = base64.b64decode(form_body)

            # Need to unquote (results in a string) then parse
            params = dict(parse.parse_qsl(parse.unquote(form_body)))
            print(params)
        else:
            return return_400("Request missing required parameter(s)")

    share_service = params.get('share_service')
    share_page = params.get('share_url')

    if not share_service or not share_page:
        return return_400("Request missing required parameter(s)")

    # Prefix the page with the user. Strip any leading '/', to conform with the storage structure.
    share_key = "Richard#" + share_page.lstrip('/')

    # Check that page exists, to prevent spam or mistakes
    client = boto3.client('dynamodb')
    result = client.query(**query_page_index_params(dynamo_table_name, "Richard", "blog/articles/20"))
    result2 = client.query(**query_page_index_params(dynamo_table_name, "Richard", "blog/books"))

    valid_page_names = [page['SortKey']['S'] for page in result['Items'] + result2['Items']]
    if share_key not in valid_page_names:
        return return_400(f"Provided page name {share_page} is not a recognised page")

    # Report to Dynamo
    share_entry = {
        'UserPages': { 'S': share_key },
        'SortKey': { 'S': SK_SHARE_PREFIX + str(int(datetime.utcnow().timestamp())) },
        'Service': { 'S': share_service }
    }
    dynamo_write_simple_items(dynamo_table_name, [share_entry,])

    return True
