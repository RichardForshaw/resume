import json
import urllib.request

import os

import boto3


def get_pushbullet_token():
    # Get pushbullet token from environment
    return os.environ.get('PB_TOKEN')


def s3_renaming_example(event, context):
    # Handler to correlate all S3 logs into a single blog statistic
    #Handle an update from an s3 bucket
    print("Reading options from event: {}\n".format(event))

    # Ensure this is for the correct bucket
    try:
        expected_logs_bucket = os.environ['LOGS_BUCKET_NAME']
    except KeyError:
        print("IMPROPERLY CONFIGURED: Could not access expected environment variables BUCKET_NAME and PATH_PREFIX")
        return False

    # Read in bucket files
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(expected_logs_bucket)
    page_names = [obj.key for obj in bucket.objects.filter(Prefix="logs/").limit(3)]
    print(f"Scan complete: {len(page_names)} files loaded")

    # Log like this so it is one line per record
    for pd in page_names:
        print(pd)

    # Safety guardrail
    if len(page_names) == 0 or page_names[0].startswith('logs/2022-11-1'):
        print("Reached the top! Stopping...")
        return

    # Rename object: Need to copy and delete
    s3c = boto3.client('s3')
    try:
        new_name = ('/R-').join(page_names[0].split("/"))
        print(f"Rename {page_names[0]} to {new_name}")
        s3c.copy_object(
            CopySource={ 'Bucket': expected_logs_bucket, 'Key': page_names[0]},
            Bucket=expected_logs_bucket,
            Key=new_name)
        s3c.delete_object(Bucket=expected_logs_bucket, Key=page_names[0])
    except Exception as e:
        print("Failed to copy or rename:")
        print(e)


def run_health(event, context):
    ''' Handler to check website health by ensuring it meets a certain size '''
    # Extract the sites from the environment
    sites = None
    try:
        sites = {url: size for url, size in (v.split(',') for k, v in os.environ.items() if k.startswith("EXPECTED_") and k.endswith("_SIZE_KB"))}
    except Exception as e:
        print("Failed to get site data from environment")
        print(e)

    if not sites:
        print("No sites were defined in the environment.")
        return False

    results = []
    for site, size in sites.items():
        print(f"Testing site: {site}")
        response = webpage_size_test(site, int(size))
        results.append(response)
        if not response["health"]:
            # This will throw if it does not exist, so hopefully raise a cloudwatch error
            topic_arn = os.environ['HEALTH_ALERT_SNS_ARN']

            message = f"Unexpected error checking {site} website. " + str(response)
            sns = boto3.client('sns')
            sns.publish(TopicArn=topic_arn, Message=message)

    return results


def webpage_size_test(url, expected_size_kb):
    ''' Retrieve a website and make sure it is no less than the given expected size.
        Return a dict indicating the health and http status
    '''
    r = urllib.request.urlopen("http://" + url)

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

