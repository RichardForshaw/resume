import json
import urllib.request

import os

import boto3

def run(event, context):

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
