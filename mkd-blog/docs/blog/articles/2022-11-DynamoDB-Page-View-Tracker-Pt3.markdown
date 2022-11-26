---
layout: post
title:  "AWS: A DynamoDB Page View Tracker (Part 3)"
description: "This series on getting started with DynamoDB and Serverless continues with providing API endpoints to query our page view statistics."
tags:
    - Cloud Development
    - Serverless
    - AWS
    - DynamoDB
    - Databases
author: Richard Forshaw
---

So here we are; we have [bootstrapped](../articles/2022-11-DynamoDB-Page-View-Tracker-Pt1.markdown) our DynamoDB instance and table structure using Serverless, and then [created and deployed](../articles/2022-11-DynamoDB-Page-View-Tracker-Pt2.markdown) a lambda to parse AWS logs and add access records to Dynamo. Now we will look at querying the data that is in Dynamo.

!['S3-lambda-dynamo'](images/s3-lambda-dynamodb.png)

## Basic Querying

First let's look at building up basic queries from the command line. This is a simple case of using the aws command line. We have used the page names as the partition keys in our database. One key feature of DynamoDB is that partition keys must be matched exactly, and range keys can be queried partially with various operators. This is because Dynamo will typically split the data across physical nodes according to the partition keys, which is why you can't partially query a partition key.

Let's look back at our use cases from Part 1. First we wanted to access the total per-page views, which is basically the count of entries of each page. In this case the most useful pages are the blog articles. So this is simple - we can just request a count of each partition key corresponding to an article.

But... how do we know what keys to query? As discussed, we can't query a partial partition key, we have to know each key exactly. How do we know that?

### Gotcha!

I left this to part 3 because this highlights the importance of analysing your access patterns. An access pattern is not just the data that you want to see, you need to *include the recipe* of how to get that data. Every DynamoDb guide you will see vehemently discourages the use of 'scan' because this gets very expensive as your data grows; in our case, we expect that our awesome blog will be getting hundreds of hits a day, so that will be in the order of hundreds of thousands of records after one year. So this is not the answer we want.

The key here is to maintain an index, which is where Dynamo's [Single-Table-Design](https://www.alexdebrie.com/posts/dynamodb-single-table/) thinking comes into its own. We need to maintain entries of all the pages that are available in our table. This is accomplished by maintaining an "INDEX" partition key with the page names as the Sort Key. The page names match exactly with the partition key values of the pages that we already track. Something like this:

|  UserPage       |   SortKey     |
|-----------------|---------------|
| INDEX           |  blog/articles/2018-11-28-backlog-priorities/
| INDEX           |  blog/articles/2021-11-16-understanding-scrum/
| blog/articles/2021-11-16-understanding-scrum/ | 1662606144
| blog/articles/2021-11-16-understanding-scrum/ | 1662607990
| blog/articles/2021-11-16-understanding-scrum/ | 1662610949
| blog/articles/2018-11-28-backlog-priorities/  | 1662609497
| blog/articles/2018-11-28-backlog-priorities/  | 1662615564
|   ...           |  ...


### Updated lambda

So lets update our lambda to account for this. We can use a nifty parameter to only write an entry if it doesn't already exist to cut down on writes:

```
from botocore.exceptions import ClientError

# ...

    # Write page index to Dynamo
    for page in set(matched_pages):
        item = { 'UserPages': {'S': 'INDEX'}, 'SortKey': {'S': page} }
        try:
            dynamo_client.put_item(
                TableName=dynamo_table_name,
                Item=item,
                ConditionExpression="attribute_not_exists(SortKey)")
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
```

This code appears after we have written our page record. It uses the `set` collection as a convenience to eliminate any duplicate page names. Then we use the client to write a record with `INDEX` as the partition key and the page name as the sort key.

The interesting parameter is `ConditionExpression="attribute_not_exists(SortKey)"`. This uses a built-in function to only perform the write if the `attribute_not_exists` function succeeds. Note that there is a little bit of extra error handling because of this condition; we know that the key will already exist many many times, so we check for the failure message of `ConditionalCheckFailedException` and ignore it. Otherwise we may see many misleading errors in our CloudWatch logs.

### Continuing the query

Now that our new code is running (and perhaps after a bit of a wait), we can query the new index records to find out what pages we have available to analyse:

```
aws dynamodb query --table-name PageTrackTable
                --key-condition-expression "UserPages = :pk AND begins_with(SortKey, :sk)"
                --expression-attribute-values '{ ":pk": { "S": "INDEX" }, ":sk": { "S": "blog/articles" } }'
```

This query uses an extra item in the query to do a bit of filtering for us, since we are only interested in blog pages. This basically resolves to:

```
UserPages = "INDEX" AND begins_with(SortKey, "blog/articles")
```

This query will return results in a fairly unreadable JSON format. This is where it is handy to know some basic parsing provided by the [jq tool](https://stedolan.github.io/jq/tutorial/). With a simple expression, we can extract the SortKey values from the dynamo results:

```
aws dynamodb query [...] | jq ".Items[].SortKey.S"

"blog/articles/2018-11-28-backlog-priorities/"
"blog/articles/2019-10-16-serverless-adventures-in-a-new-dimension/"
"blog/articles/2020-12-13-philosophy-for-developers/"
"blog/articles/2021-11-16-understanding-scrum/"
...
```

We can now perform a query to count the entries for one of these keys. Note the use of `--select COUNT` here:

```
aws dynamodb query --table-name PageTrackTable
                --key-condition-expression "UserPages = :pk"
                --expression-attribute-values '{ ":pk": { "S": "blog/articles/2021-11-16-understanding-scrum/" } }'
                --select COUNT

{
    "Count": 72,
    "ScannedCount": 72,
}
```

## Building the Query Endpoints

We can now deploy some functions to do this querying for us, with a little bit of prettying. The Serverless Framework once again makes this a simple task, at least to set up the infrastructure, in our `serverless.yml` file.

```
provider:
  # ...

  # Enable cors so we can post contact info from the web page
  httpApi:
    cors: true

functions:
  pagecounttotals:
    handler: handler.handle_blog_page_count_totals
    logRetentionInDays: 30
    timeout: 10
    events:
      - httpApi:
          path: /pagetotals
          method: get
    environment:
      TARGET_DYNAMO_TABLE: ${self:resources.Resources.PageTrackTable.Properties.TableName}
```

The new function uses the `httpApi` event type, allowing us to specify an endpoint path, in this case `/pagetotals`. Note that we need to enable CORS, because the source of our request is not going to be the same domain as that in which our HTTP endpoints are.

Now for the handler, which is added to the existing handler file:

```
def handle_blog_page_count_totals(event, context):
    # [1] Parameters from environment
    try:
        dynamo_table_name = os.environ['TARGET_DYNAMO_TABLE']
    except KeyError:
        print("IMPROPERLY CONFIGURED: Missing environment variable TARGET_DYNAMO_TABLE")
        return False

    # [2] Query the indexes from Dynamo
    client = boto3.client('dynamodb')
    result = client.query(
                TableName=dynamo_table_name,
                ProjectionExpression="UserPages,SortKey",
                KeyConditionExpression="UserPages = :pk AND begins_with(SortKey, :sk)",
                ExpressionAttributeValues={ ":pk": {"S": "INDEX"}, ":sk": {"S": "blog/articles/" }})

    # [3] Now we must query for the items
    result_dict = {}
    for item in result['Items']:
        page_name = item['SortKey']['S']
        page_result = client.query(
                    TableName=dynamo_table_name,
                    Select='COUNT',
                    KeyConditionExpression="UserPages = :pk",
                    ExpressionAttributeValues={ ":pk": {"S": page_name}})

        if page_result['Count']:
            result_dict[page_name] = page_result['Count']

    return result_dict
```

This is a basic version of the actual production version - I additionally keep track of the total visits, the earliest timestamp and the capacity used by the queries, but you can add what you want.

There are essentially 3 parts to this function:

 1. Get configuration parameters from the environment. This is handy in case a key bit of infrastructure changes - it is good practice to not hard-code too many things which may change. It also allows the function to be split more easily between dev and prod environments and potentially reused elsewhere.
 2. Perform the query on the INDEX key, which was shown above
 3. Perform queries on each of the results from (2) and format them nicely to be returned to the client. This provides a dictionary with the pages as the keys and the counts as the values.

### IAM strikes again

Because we are now fiddling about with new services, we need to ensure that we are allowed to do so. Our Serverless deployment role will need to be updated with a new permission. If you are using CloudFormation it will look a bit like this:

```
    - PolicyName: APIGatewayDeploymentPolicies
        PolicyDocument:
        Version: 2012-10-17
        Statement:
            - Effect: Allow
            Action:
                - 'apigateway:*'     # <-- Remember to restrict this!
            Resource:
                - 'arn:aws:apigateway:ap-southeast-1::/apis'
```

Our new lambda will also need permission to query our Dynamo table in the `serverless.yml` file:

```
  iam:
    role:
      statements:
        # ...
        - Effect: "Allow"
          Action:
            - "dynamodb:PutItem"
            - "dynamodb:UpdateItem"
            - "dynamodb:BatchWriteItem"
            - "dynamodb:Query"          # <-- New permission
          Resource:
            - Fn::GetAtt: [PageTrackTable, Arn]
```

### Let's Query

The Serverless Framework has a handy feature whereby it spits out the endpoint URL after deploying your service. if you miss it you can also run `sls info` to get the same information. It will look something like this:

```
service: my-sls-page-tracker
region: ap-southeast-2
stack: my-sls-page-tracker-dev
endpoints:
  GET - https://rf7???0f9.execute-api.ap-southeast-2.amazonaws.com/pagetotals
```

This means that you can plug the endpoint into something like `curl` to check that everything is working. Once again we can use `jq` to do some prettying for us (this basically just prints the JSON nicely so we can read it...):

```
curl https://rf7???0f9.execute-api.ap-southeast-2.amazonaws.com/pagetotals

{
  "blog/articles/2022-07-14-data-reporting-tips-for-developers/": 38,
  "blog/articles/2022-07-20-software-pipelines/": 53,
  "blog/articles/2022-08-24-first-vietnam-experiences/": 50,
  "blog/articles/2022-08-30-aws-cli-essentials/": 145,
  "blog/articles/2022-09-08-productivity-and-agile/": 91,
  ...
}
```

## Over to you

You thought I was going to give you everything? It's best to learn by doing, so I'll throw the query for the second goal (page views over time) over to you. Just to get you started, here is the Dynamo CLI query:

```
aws dynamodb query --table-name PageTrackTable
                --key-condition-expression "UserPages = :pk"
                --expression-attribute-values '{ ":pk": { "S": "<page_name>" } }'
                --projection SortKey | jq '.Items[].SortKey.S'
```

Note this uses a new parameter: `--projection SortKey`. This tells Dynamo that we only want the SortKey value back again, otherwise it will send us back the full records for each match.

## What's Unfinished

This series is meant to be a simple practical example of using Dynamo, and there are some improvements to be made, both functionally and in using Dynamo in a better way:

 * The queries we have made almost amount to a simple 'scan' operation, which is generally frowned upon. However these typically fall under intermediate and advanced techniques, potentially involving secondary indexes, dynamodb streams, caching and other such things.
 * We expect to perform some additional filtering on our queries, such as viewing history for the current week or month, or simply when a page was last accessed. These not only involve changing the way Dynamo is queried but also handles passing parameters to our endpoints.
 * As our number of published pages increases, we may want to perform some parallel querying to speed things up. Perhaps we want to query on what browsers are viewing our site or where they are being referred from.

All these are beyond the scope of this series, but I expect that some of them will be turned into useful articles, so thank you for reading and stay tuned!

