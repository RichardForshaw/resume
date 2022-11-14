---
layout: post
title:  "AWS: A DynamoDB Page View Tracker"
description: "After exploring DynamoDB a few times, I finally found a project which was broad enough to touch most aspects of DynamoDB but simple enough to be turned into a tutorial. So here it is. (Part 1 of 3)"
tags:
    - Cloud Development
    - Serverless
    - AWS
    - DynamoDB
author: Richard Forshaw
---

I've kicked off a few projects using DynamoDB, and I've wondered if they would be suitable to create a tutorial which can appeal to anyone wanting to get started on DynamoDB. Until now I haven't had a project which I think would resonate with many people, but in developing this blog to keep my cloud-skills alive I happened across a good topic: writing your own Google Analytics.

That seems to be quite a large undertaking, and you are right, so this is a very cut-down MVP-type version which only involves tracking visitors to pages and being able to view the results. But even that small scope covers a lot of ground, which is good.

In the following series we will look into DynamoDB and lambda and tying them together with serverless.

!['S3-lambda-dynamo'](images/s3-lambda-dynamodb.png)

## Intro: Choosing Dynamo

DynamoDB - what is it good for? Why use it here? Well it is true that you could build this project in a number of ways, but this problem is simple enough to be a good intro to Dynamo yet non-trivial enough to demonstrate how you must think when embarking down the DynamoDB path. Because it will keep growing over time, it is also scalable enough to have to think a little about scalable data issues.

DynamoDB is super-powerful but only in the right hands. It provides amazing scalability with lightning-fast lookups and retrieval even if you have millions of records. I have been in a workshop with the amazing [Rick Houlihan](https://twitter.com/houlihan_rick), and he demonstrated some of the amazing things it can do. But you must be aware what NoSQL databases are best used for.

NoSQL databases are best for [OLTP (Online Transaction Processing)](https://www.ibm.com/cloud/blog/olap-vs-oltp). They allow you to deal with amazing volumes of single transactions. However they are not good at OLAP (Online Analytics Processing). OLAP is what Relational Databases are good for; you define the relations first and then worry about how you are going to use them.

Functionally speaking, this particular problem is probably on the border of OLTP and OLAP, being an analytics-type problem. You may think that about many applications, but in this case we can identify early that we essentially want to do the same small set of well-known operations over and over, which puts us in the realm of OLTP. The key thing is knowing this up front.

### Designing the Dynamo table

The most important thing to do after identifying this is to identify what those operations are. In this case, to build a simple page tracker, I wanted to know the following:

 - The total per-page views within a given time range
 - The per-page views variation over time (by day/week/month)

So what access patterns are needed to do this? I needed to analyse the queries I expected to make and I came up with the following simple requests:

 - Counting all access records for a given page
 - Counting access records for a given page within a time range

This now gives me my Dynamo table design: To access data per-page and to filter it on a time range. My basic table design would therefore be:

 - Partition key: Page identifying (in this case I just used the URL path)
 - Sort key: Access timestamp

This exercise is very important because in NoSQL it is very hard to change these decisions. In a relational database once you define your relations you can design dozens of ways to query that data, so it is very flexible. With NoSQL you need to do things differently, and this is so important to remember. I have read **so many questions on Stack Overflow** asking about how to query a DynamoDB table in a different way now that it is populated with data, and the answer is the same: either try to use a secondary index (if possible), or build your table in a different way.

The awesome Alex DeBrie also has a [great page](https://www.alexdebrie.com/posts/dynamodb-single-table/) on single-table DynamoDB design.

!['Serverless-key'](images/serverless-key.png)

## Serverless bootstrap

So we know our goal: to be able to query something (most likely an endpoint) so we can render our page view stats in some way in a web page. We will use the Serverless framework to do this, so let's get started.

First off: everyone should know by now how to kick off a new serverless project right? No? Well here it is:

```
serverless create --template aws-python3 --name dynamopagetracker
```

Now that your serverless project is bootstrapped, we can start working in our new `serverless.yml` file.

### Things to remember

It is typically best practice to deploy your stack using a role, and that role must be create (or updated if you have an existing role) with the appropriate permissions.

It is really worth understanding IAM and the permission models before diving too far into an exercise like this. Spend some time reading the information or looking at a tutorial to get started. Make sure you look carefully at any cloudformation error messages that you get that say there is a permission error and find out what is being requested. Make sure you understand how to write policies to allow those things, and not just liberally allow everything. It will be worth it in the long run.

I will assume that this knowledge exists for the purpose of this exercise as it is not really the focus, except if there is a particular gotcha.

!['IAM Policy Gotcha'](images/IAMPolicyBrain.jpg)

### Dynamo

The great thing is that the Dynamo definition can go right in to the serverless.yml file. Here we define our keys that we decided on from the design step: The page name for the partition key and a timestamp for the Sort Key:

```
resources:
  Description: Serverless Stack for page-tracking with DynamoDB
  Resources:
    PageTrackTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: PageTrackTable
        AttributeDefinitions:
         -
           AttributeName: UserPages
           AttributeType: S
         -
           AttributeName: SortKey
           AttributeType: S

        KeySchema:
          -
            AttributeName: UserPages
            KeyType: HASH
          -
            AttributeName: SortKey
            KeyType: RANGE
```

Note here that even though the SortKey will be a timestamp, I am storing it as a string. I've done this for a reason that will be revealed later.

### The First Lambda

I usually start small with lambda; something which just prints out the event that is being received so that you know what to do with it. AWS events can be complex and I think that just while we are getting the stack up and running it is worth keeping it simple:

```
def handle_s3_view_log(event, context):
    #Handle an update from an s3 bucket
    print("Reading options from event: {}\n".format(event))
```

The serverless lambda definition is also straightforward:

```
functions:
  pagetracker:
    handler: handler.handle_s3_view_log
    logRetentionInDays: 30
    timeout: 10
    events:
      - s3:
          bucket: ${cf:existing-stack-export-of-bucket}
          existing: true
          event: s3:ObjectCreated:*
          rules:
            - prefix: logs/
```

Here we use some common parameters to say that we only want logs kept for 30 days and our function timeout is 10s (should be plenty). We then define the event that we want to trigger the lambda. In this case I have an existing bucket that I have set up for receiving the logs from the built-in AWS s3 access log feature, and I want to run a lambda whenever there is a new log.

Note that the Serverless framework will try to create everything for you, so it initially tried to create my logs bucket which already existed. Because of this I needed to use the `existing: true` flag. But that raised another problem.

### IAM = Infuriating Access Machinations

For simplicity, I set up the AWS S3 logging feature which allows me to track requests for the various pages in an S3 bucket configured as a web site. Because I want to use events from an existing bucket, Serverless needs to do this by running a custom resource lambda (this is one example of something that is not set up with simple configuration). This then means that there is an additional layer of permissions that is required:

 - First the deployment service needs to pass the deployment role to the custom resource lambda
 - Then the lambda must be allowed to perform bucket configuration operations

If you wish to have Serverless set up the bucket for you, then this won't be an issue, but this is one case where there are other decisions that have been made that need to be accommodated, e.g. that there should be a logs bucket aligned with the lifecycle of the web page, not with the lifecycle of this lambda function. These types of decisions are important to the architecture of the whole system, so you are likely to come across them occasionally.

The solution in my case was to allow `iam:PassRole` to be performed by my deployment role, and to also allow the necessary s3 actions to be performed on my logs bucket by that role.

### Hey Presto: No Servers!

So you have a database table and a lambda that is triggered by an S3 event but doesn't really do anything, but if you watch logs come in to the logging bucket (or write a file there yourself), you will be able to verify that the lambda does indeed get triggered.

So what next? We will look at fleshing out the Lambda function in the next post.

