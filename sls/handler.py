import json
import urllib.request

import os

import boto3

def run(event, context):
    r = urllib.request.urlopen("http://www.forshaw.tech")

    # Get the expected 'good' length from the environment. Default to 10k
    goodlength = int(os.environ.get('EXPECTED_WEBSITE_SIZE_KB', 10)) * 1024
    goodlength = r.length > goodlength

    # Overall health
    healthy = r.code == 200 and r.msg == "OK" and goodlength
    response = {
        "statusCode": r.code,
        "length": r.length,
        "status": r.msg,
        "health": healthy
    }

    if not healthy:
        # This will throw if it does not exist, so hopefully raise a cloudwatch error
        topic_arn = os.environ['HEALTH_ALERT_SNS_ARN']

        message = "Error with forshaw.tech website. " + str(response)
        sns = boto3.client('sns')
        sns.publish(TopicArn=topic_arn, Message=message)

    return response
