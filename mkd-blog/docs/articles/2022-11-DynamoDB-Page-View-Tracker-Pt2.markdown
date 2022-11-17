---
layout: post
title:  "AWS: A DynamoDB Page View Tracker (Part 2)"
description: "This post continues with building a small analytics-like page tracker on AWS. This time we set up the S3-to-Dynamo processing lambda."
tags:
    - Cloud Development
    - Serverless
    - AWS
    - DynamoDB
    - Databases
author: Richard Forshaw
---

In [Part 1](../articles/2022-11-DynamoDB-Page-View-Tracker-Pt1.markdown) we bootstrapped a DynamoDB table and basic Lambda function using the [Serverless Framework](https://www.serverless.com/framework) with the aim of being able to query for page-view stats on a set of web pages. Now we will look at developing and deploying the Lambda to write the records that we need into Dynamo.

!['S3-lambda-dynamo'](images/s3-lambda-dynamodb.png)

## Developing your Lambda

As noted in Part 1, the easiest way of getting the access statistics was from the AWS S3 access log feature. This very conveniently provides a log of access requests to all of the objects stored in your S3 bucket, so when the bucket is configured as a website, you can use this to track access to your pages.

This task is therefore simply a means of parsing the log files. Fortunately the log file format is documented [on this page](https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html). In short, you will need to find a way to parse this and extract what you want. In my case I wanted to go from this:

```
d6ad5...6af62 www.forshaw.tech [20/Oct/2022:08:49:42 +0000] 14.161.28.234 - K6E...7N1 WEBSITE.GET.OBJECT blog/articles/2021-11-21-understanding-scrum-part-2/index.html "GET /blog/articles/2021-11-21-understanding-scrum-part-2/ HTTP/1.1" 200 - 21653 21653 100 99 "http://www.forshaw.tech/blog/tags/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0" - LA99A...EegEE= - - - www.forshaw.tech - -
```

To something like this:

```
{
    'PageName': {
        'S': 'blog/articles/2021-11-21-understanding-scrum-part-2'
    },
    'SortKey': {
        'S': '1666255782'
    },
    'AgentString': {
        'S': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
    },
    'RemoteAddress': {
        'S': '14.161.28.234'
    }
}
```

This strange format is how you need to submit a typical record to DynamoDB, providing the field name, data type and data itself. The example here demonstrates that the lambda function needs to:

 - identify each field in the string
 - filter entries and fields that are not needed
 - perform transformations (e.g. converting the timestamp into epoch time)
 - specify custom names for the target dictionary fields
 - construct a dictionary matching the [boto3 DynamoDB spec](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item)

Parsing the log files looks straightforward but is a little complicated. It requires some slightly advanced knowledge of regular expressions which is probably beyond the scope of this article, mainly because the fields are not consistently delimited. That is, the time field is delimited by []s and there are other fields delimited by quotes. This is a great exercise in functional development. As mentioned, the code specifics are out of scope of this article, but maybe I'll post my solution one day!

!["Modular Shape"](images/modular.jpg)

### Tip: Be modular

Having said the above, it is very useful to ensure that you write your parsing function as a separate function, away from the handling of the Lambda and DynamoDB functionality. Why? Well firstly it is difficult to test lambdas, especially ones triggered by AWS events. Therefore it is an incredible time-saver to separate your core processing logic so that it can be properly unit-tested. Then when you finally deploy the function you really only have to sort out the AWS-side of things.

Local unit tests are a huge benefit: With just a few examples of your log format, you can modify them in many ways and test various features of your processing lambda. In my case I tested:

 * parsing fields into different data types
 * Performing field translations (e.g. a textual date format into an epoch-style timestamp)
 * Decorating field results (e.g. trimming 'index.html' off URL paths or adding prefixes to sort keys)
 * Pre-filtering log records

All this could be done in the safety and efficiency of my local environment without going through deployment cycles and having to manually browse cloud logs.

Another reason for being modular is that in my case (and possibly yours as well), in the future you may want to be able to import old S3 access logs that were perhaps collected before developing this project. Any S3 log that is lying around and not being properly processed by your lambda yet is just being wasted. If your processing functions are in a sharable function or module, then you can write a very simple wrapper to parse them locally and push them into Dynamo yourself.

## Reading from S3

The things that I will talk about here are parsing the event received by the lambda and sending it to Dynamo.

In the lambda function, is it straightforward to see that there are particular bits of the AWS S3 event that you need:

```
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
```

_Note: this assumes that there is only one record per lambda invocation. It may be possible that in high-volume contexts, your lambda receives multiple file records._

Then you need to use an S3 client to open the file which has been passed to us:

```
    # Open and read S3 object
    s3 = boto3.client('s3')
    try:
        file_data = s3.get_object(Bucket=bucket_name, Key=object_key).read()
    except Exception as e:
        print(f"Unable to read {object_key} from {bucket_name}")
        print(e)
```

There are 2 tricky things here - one is making sure your IAM statements are correct and making sure you can read the data from S3 correctly.

### More IAM Fun

In the first case, you will need to ensure your lambda has permission to read from the logs bucket. This is easily done in the `serverless.yml` file:

```
  iam:
    role:
      statements:
        # IAM role to access S3 objects
        - Effect: "Allow"
          Action:
            - "s3:ListBucket"
            - "s3:GetObject"
          Resource:
            - ...YourBucketArn      # (See below)
```

_Note that this is a simplified version allowing access to the whole bucket. In practice you may only want to grant access to a specified folder._

This is where things can get tricky. Previously I have managed infrastructure stacks separately to the `serverless.yml` file, and I have used the serverless variable notation: `${cf:my-other-stack.MyOutputName}` to obtain values that are output from that stack.

This time, the DynamoDB table is defined internally in the 'resources' section. So how do you access it? Well, it turns out it is easy, but for the fact that it doesn't appear to be documented well on the Serverless website. There are two ways of accessing stack information:

To access a resource name (or another property which is explicitly defined), just use dot-notation to refer to it:

```
    environment:
      TARGET_DYNAMO_TABLE: ${self:resources.Resources.MyTable.Properties.TableName}
```

if you need to access a derived property (one that is not explicit in  your resource definition), you can use the `GetAtt` function directly on your resource name like so:

```
    Resource:
      - Fn::GetAtt: [PageTrackTable, Arn]
```

!['Binary text'](images/binary_fade.jpg)
### Reading S3 Data

In the second case, because S3 is an object store (not, as many people would like to think, a text-file store), despite the fact that you are storing logs, objects in S3 are stored as bytes and as such when you read them from the S3 bucket they are returned as _bytes_ and not _strings_. You therefore need to convert them in order to perform string-processing operations on them. The way I do this in python is:

```
data = str(file_data, 'utf-8', 'ignore')
```

## Writing to Dynamo

Writing to Dynamo is pretty easy, compared to the above. You just need to use the standard Boto3 library, and as long as you have formatted your dynamo item as shown previously, and your IAM is configured to allow your lambda to write to Dynamo, you can push it to dynamo with one function call:

```
    dynamo_client = boto3.client('dynamodb')
    for item in table_data:
        dynamo_client.put_item(TableName=dynamo_table_name, Item=item)
```

Of course it is good to wrap this in exception handling. Exception handling with the python Boto3 library is a little tricky. In essence, there are no exceptions for failures that happen on the server side; if you simply catch an 'Exception' type then you won't get much info. Instead you need to catch a `ClientError` exception and check the contents:

```
from botocore.exceptions import ClientError

# ...

    try:
        dynamo_client.do_something(...)
    except ClientError as ce:
        if ce.response['Error']['Code'] =='SomeDocumentedErrorName':
            print(f'Got unexpected ClientError:')
            print(ce)
```

Note also that here I am pushing each item separately. This is because I rarely expect a flurry of traffic. However if I do get some peak traffic and there are a large number ot page view records in one lambda event, then I would consider switching to one of the [batch-writing methods](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#batch-writing).

## Set it free...

So there we have it...:

 - A lambda which reads from S3, processes and writes to DynamoDB
 - The correct permissions for the lambda to be able to do this
 - All the `serverless.yml` setup from the first part

We can now deploy our service with a simple `sls deploy`.

Once deployed, it will happily chug away and push data into your DynamoDB table. What do we do with it then? Check out Part 3, coming soon...

