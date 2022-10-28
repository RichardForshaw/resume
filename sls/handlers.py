from itertools import chain
import json
from typing import Counter
import urllib.request

import os
import re

import boto3


def get_pushbullet_token():
    # Get pushbullet token from environment
    return os.environ.get('PB_TOKEN')


def run_pageviews(event, context):
    # Handler to correlate all S3 logs into a single blog statistic
    #Handle an update from an s3 bucket
    print("Reading options from event: {}\n".format(event))

    # Ensure this is for the correct bucket
    try:
        expected_logs_bucket = os.environ['LOGS_BUCKET_NAME']
        expected_www_bucket = os.environ['WWW_BUCKET_NAME']
        expected_path = os.environ['PATH_PREFIX']
    except KeyError:
        print("IMPROPERLY CONFIGURED: Could not access expected environment variables BUCKET_NAME and PATH_PREFIX")
        return False

    # Read all files from bucket
    print(f"Scan objects in bucket {expected_logs_bucket}")
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(expected_logs_bucket)
    page_data = [obj.get()['Body'].read().splitlines() for obj in bucket.objects.filter(Prefix='logs/')]
    print(f"Scan complete: {len(page_data)} files loaded")
    print(page_data[:5])

    # Now perform processing to tally up page views
    # Ensure our data is in string format for parsing
    collate_config = {
        'bucket_name': expected_www_bucket,
        'folder_prefix': expected_path,
        'only_folders': True
    }
    print(f"Collate page views. Config: {collate_config}")
    stats_dict = collate_page_views(flatten_byte_strings(page_data), **collate_config)

    # Write to file in root
    print(str(stats_dict))
    bucket.put_object(Key='access_stats', Body=str(stats_dict))

    return stats_dict

def flatten_byte_strings(lists):
    # Flatten a list of lists of byte strings into a list of strings
    return map(lambda x: str(x, 'utf-8', 'ignore'), chain(*lists))

def collate_page_views(log_data, bucket_name='.*', folder_prefix='', only_folders=False):
    ''' Allow a list of log strings to be filtered by bucket name, folder prefix and other things.
        By default, this will only list 'GET' operations (views).
        Options:
         - bucket_name: the name of the bucket being accessed
         - folder_prefix: the prefix folder to the GET operations. This filters anything starting
                with GET /folder_prefix/something...
         - only_folders: only count access requests to folders. The way this blog is set up, clicking a
                link makes requests that are at the folder level.
                (Note this omits the trailing slash in the results keys)
    '''
    # Ensure folder name has trailing slash
    if len(folder_prefix) and folder_prefix[-1] != '/':
        folder_prefix += '/'

    # Filter OBJECT.GET and retain object paths
    re_match = rf'^[0-9a-f]+ {bucket_name} .*GET\.OBJECT.*GET /({folder_prefix}.*){"/" if only_folders else ""} HTTP.*'
    return dict(Counter(re.sub(re_match, r'\1', l) for l in filter(lambda x: re.match(re_match, x), log_data)))

def run_health(event, context):
    ''' Handler to check website health by ensuring it meets a certain size '''
    response = webpage_size_test("http://www.forshaw.tech", int(os.environ.get('EXPECTED_WEBSITE_SIZE_KB', 10)))
    if not response["health"]:
        # This will throw if it does not exist, so hopefully raise a cloudwatch error
        topic_arn = os.environ['HEALTH_ALERT_SNS_ARN']

        message = "Unexpected error with forshaw.tech website. " + str(response)
        sns = boto3.client('sns')
        sns.publish(TopicArn=topic_arn, Message=message)

    # Next: Test blog site

    return response

def webpage_size_test(url, expected_size_kb):
    ''' Retrieve a website and make sure it is no less than the given expected size.
        Return a dict indicating the health and http status
    '''
    r = urllib.request.urlopen(url)

    # Get the expected 'good' length from the environment. Default to 10k
    good_length = expected_size_kb * 1024
    good_length = r.length > good_length

    # Overall health dict
    return {
        "statusCode": r.code,
        "length": r.length,
        "status": r.msg,
        "health": r.code == 200 and r.msg == "OK" and good_length
    }

def contact_form_email(event, context):
    ''' Handler for web contact form email '''
    # Receiver is defined in environment (or the admin account)
    receiver = os.environ.get('CONTACT_FORM_TARGET_EMAIL', 'aws@forshaw.tech')

    # Receiver is an email that is from the verified domain
    sender = os.environ.get('CONTACT_FORM_SOURCE_EMAIL', None)

    if not sender:
        print("Incorrectly configured: Missing email sender address")

    # Get body from context
    print(f"Processing event: {event}")
    if 'rawPath' in event and 'body' in event:
        # HTTP response. Get everything from the event body JSON
        data = json.loads(event['body'])
    else:
        # (Otherwise assume this is a test event from the lambda console)
        data = event

    msgBody = f"Name: {data.get('name', 'No name supplied')}\nEmail: {data['email']}\nMessage: {data.get('message', 'No message provided')}\n"
    message = {
        'Body': {
            'Text': {
                'Data': msgBody,
                'Charset': 'UTF-8'
            }
        },
        'Subject': {
            'Data': 'Forshaw.tech contact enquiry from: ' + data['email'],
            'Charset': 'UTF-8'
        }
    }

    # Email parameters
    email_dest = { 'ToAddresses': (receiver, ) }

    # Log
    print(f"Preparing to send contact request received from {data['email']}")
    print(data.get('message', 'No message provided'))

    # Get email client
    ses = boto3.client('ses')
    response = ses.send_email(Destination=email_dest, Source=sender, Message=message)
    print(response)

    # For the time-being, send a notification to pushbullet
    http_response = response['ResponseMetadata']['HTTPStatusCode']
    notify_pushbullet("Tech Website Form Submission", f"Message from {data['email']} (SES Response: {http_response})")

    return { 'action': f'email sent to {receiver}', 'status': http_response}

# Pushbullet notifications - load conditionally
if get_pushbullet_token():
    from pushbullet import Pushbullet

def notify_pushbullet(subject, message):
    pb_token = get_pushbullet_token()

    if not pb_token:
        print('Cannot sent PushBullet message... could not find PB_TOKEN')
        return

    pb=Pushbullet(pb_token)
    pb.push_note(subject, message)

