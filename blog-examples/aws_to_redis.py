# Script to generate redis commands from AWS log content
import sys
import os
import re
from datetime import datetime

# For file loading
from glob import glob

from handler import parse_s3_logs_to_dynamo

# Configuration
S3_LOG_TS_FORMAT = '[%d/%b/%Y:%H:%M:%S %z]'
BUCKET_NAME = 'www.developdeploydeliver.com'

# The tuple defining what to get from the aws s3 log string
DYNAMO_FIELDS_TUPLE = (
    (7, 'UserPages', 'S'),      # PartitionKey: User and Page
    (2, 'SortKey', 'S'),        # Sort Key: Timestamp
    (16, 'AgentString', 'S'),   # Agent Access String
    (13, 'ServiceTime', 'S'),   # Page Access Time
    (3, 'RemoteAddress', 'S'),
    (15, 'Referrer', 'S')        # The page that referred this request
)

def parse_file(filename, parse_config):

    parse_config['translations'] = {
        # Convert timestamp to epoch
        'SortKey': lambda x: str(int(datetime.strptime(x, S3_LOG_TS_FORMAT).timestamp())),
        # Strip index.html from page name
        'UserPages': lambda x: re.sub(r'index\.html', '', x)
    }

    # Open the file for reading
    with open(filename, 'r') as file:
        # Read the file line by line, generate tuple
        table_data = parse_s3_logs_to_dynamo(file.read(), DYNAMO_FIELDS_TUPLE, **parse_config)

    # Return the list of parsed lines, without empty results
    return table_data

def dynamo_to_redis(ddict):
    ''' Convert a dynamo entry to redis entry commands '''
    # Redis entries are:
    #   HSET <KEY>#<SORTKEY> ...other decomposed values...
    #   RPUSH <KEY> <SORTKEY>
    #   SADD USER#INDEX PAGE
    #   HINCRBY USER#PAGES <PAGE> 1
    user_key, page_key = ddict['UserPages']['S'].split('#')
    if page_key == "":
        page_key = "/"
    item_key = '#'.join([user_key, page_key, ddict['SortKey']['S']])
    ts = ddict['SortKey']['S']
    h_string = ''
    for k, v in ddict.items():
        if k not in ['UserPages', 'SortKey']:
            h_string += k + ' "' + v['S'] + '" '

    return [
        'HSET ' + item_key + ' ' + h_string,
        f'RPUSH {page_key} {ts}',
        f'SADD {user_key}#INDEX "{page_key}"',
        f'HINCRBY {user_key}#PAGES {page_key} 1'
    ]

# Read filename argument
if __name__ == "__main__":

    # Check the number of arguments
    if len(sys.argv) == 1:
        print("Error: No file(s) specified")
        sys.exit()

    # Get the file name from the first argument
    filename = sys.argv[1]

    # Assume that the user is using file globbing
    files = glob(filename)

    # Check if the file exists
    if not len(files) or not os.path.exists(files[0]):
        print("Error: The provided file '{}' does not exist".format(filename))
        sys.exit()

    # Set up config
    parse_config = {
        'bucket_name': BUCKET_NAME,
        'folder_prefix': '',
        'file_filter': 'index.html',
        'pk_format': 'Richard#{}'
    }

    # Open the file and call the parse function
    print(f'Processing {len(files)} files...')
    if len(files) < 10:
        print(files)
    for f in files:
        for i in parse_file(f, parse_config):
            print('\n'.join(dynamo_to_redis(i)))

    # End with a "QUIT"
    print("QUIT\n")
