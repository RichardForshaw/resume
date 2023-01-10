---
layout: post
title:  "Web Analytics 3-Ways"
description: "I recently used AWS DynamoDB to demonstrate how to build a simple web analytics tool. In this post I consider using Redis and AWS Athena as alternatives. I look at which may the most suitable and how they differ."
revision_date: "2023-01-10"
tags:
    - Cloud Development
    - AWS
    - DynamoDB
    - Databases
author: Richard Forshaw
---

I recently published a series on [getting started with Dynamo DB](./2022-11-DynamoDB-Page-View-Tracker-Pt1.markdown), which used a project for tracking visits to a website hosted on AWS S3 as an example of using lambda events and DynamoDB. The Dynamo database was then queried via API Gateway to get the page visit statistics.

Because I am keen to explore other technologies, this got me thinking about what other solutions might be available to do the same thing and evaluating what would be the best tool for the job. I had previously used Redis as a caching solution but I knew that it was capable of doing much more than that. I had also briefly used AWS Athena, which had the benefit of being able to query S3 data directly.

This post looks into Redis and Athena as alternatives to DynamoDB for this specific task and answers a few questions about suitability.

_This was also presented as a Tech Talk at [Tech Meetup Vietnam](https://www.meetup.com/tech-meetup/)._

## Traps Ahead

I initially used DynamoDB to store the page visit events for the web-tracking solution. You can see the detail of this in the [previous series](./2022-11-DynamoDB-Page-View-Tracker-Pt1.markdown). I tried to design the Dynamo data model based on my expected access patterns, but I still managed to get a few things wrong. This is a common pitfall in data modelling for NoSQL databases, and despite trying to avoid it, I fell for it. Migrating your way of thinking from relational to NoSQL is difficult, because it also means you need to move away from thinking about data storage optimisation, and towards thinking about access time.

![Tightrope and Crocodiles](images/tightrope_and_crocodiles.png)

Before treading in the realm of the NoSQL database it is worth doing some reading and research into NoSQL data modelling. There is an excellent [talk by Rick Houlihan](https://www.youtube.com/watch?v=HaEPXoXVf2k) which goes through various modelling techniques for NoSQL databases, mainly aimed at DynamoDB. It starts off at an intermediate level, but the final third is quite advanced and he moves at a fast pace so make use of that pause button!

DynamoDB's pricing model, along with many other serverless offerings, comes down to reads and writes. I think this is a good thing because your read-behaviour also directly impacts your performance and responsiveness, so optimising your read-performance benefits you in two ways. Because of this, the biggest advice I can give is that you should aim for **all your user access patterns to access only one record**. This can be a bit anti-intuitive when coming from a relational background because that was of thinking promotes optimal data storage and shows how many user requests can be derived from data, but this change in thinking is worth it. So: analyse your access patterns, then analyse them again.

With that said, let's look at the databases.

![DynamoDB](images/amazon-dynamodb-logo.png){: style="max-height:150px;"}

## DynamoDB

Dynamo is a very powerful document-based NoSQL database which is fully cloud-native. It scales automatically and it is renowned for powering the [Amazon Prime Day](https://aws.amazon.com/blogs/aws/prime-day-2021-two-chart-topping-days/) sales, peaking at over 80 million requests per second and offering reliability of up to 5-nines. DynamoDB is serverless, which means it is easy to get up and running - you just need to provision a table and start using it with your AWS access keys. There is also a [docker image](https://hub.docker.com/r/amazon/dynamodb-local) that is available for download, so you can play with it locally.

While DynamoDB is a type of key-value store, it configures its key in a specific way: you must provide a Partition Key (or Hash Key) which must be matched exactly in any query. You can then provide an optional SortKey (or Range Key) which is automatically sorted in the database (hence the name) and can be matched partially or even not at all. This provides a lot of flexibility for storing data, but it does mean that you should consider carefully how this fits in to your access patterns.

In the case of a web tracker, I had to consider matching single records in the case of retrieving statistics or metadata, and multiple records in the case of getting page visit or sharing details. If your app is dealing with users and their details, you will also need to store and access this data as part of your access patterns.

In addition to this you can configure your SortKey to be able to represent hierarchical data, so you can 'drill down'. Once again, this is driven by your access patterns. For example in Rick Houlihan's video you can store staff information hierarchically in terms of Country -> State -> Office -> Department.

### Indexes

Dynamo is powerful in that it also give you control over how your data is indexed. The indexes it provides are the Local Secondary Index (LSI), and the Global Secondary Index (GSI).

A Local Secondary Index allows you to index data using a different Sort Key, but must use the same Partition Key. An example for web-tracking may be indexing by browser type or source IP address. Note that for a LSI, there is no need for your overall key (Partition + Sort) to be unique - this is only a requirement for the primary key definition.

The Global Secondary Index allows you to define a completely different index for your data. An example for web-tracking may be to index on access time so that you can quickly access all of today's traffic. You can define a different key structure if you want - i.e. if your initial index was a composite key of Partition Key and Sort Key, your GSI could only have a Partition Key.

One key difference to remember is that LSIs must be created when you create the table, whereas GSIs can be created at any time. Which brings us back to access pattern modelling. If you decide you need an LSI after you have deployed your table then it is going to be tough to do.

![Redis](images/Redis-Logo-Thin.png){: style="max-height:150px;"}

## Redis

Redis (REmote DIctionary Server) is an in-memory advanced-key-value database which outgrew its original key-value behaviour long ago and now provides many types of data storage options. And it is lightning fast. It is definitely worth getting to know. Perhaps two of its most famous users are Twitter and Instagram, which have used it to serve millions of users at lightning speed. It also serves companies like StackOverflow and GitHub.

### Setup

Redis comes as a [dockerised image](https://hub.docker.com/_/redis) and so is easy to set up and [run locally](https://redis.io/docs/stack/get-started/install/docker/) which is a massive benefit. To do this, fetch the image (in this case `redis/redis-stack` ), then run:

`docker run -d --name my_redis -p 6379:6379 -p 8001:8001 redis/redis-stack`

One great thing about Redis is that importing data is simple: the Redis CLI can ingest a text file of Redis commands, which are very easy to generate from source data. A Redis script looks like this:

```
HSET my_key#1669849589 AgentString "Mozilla/5.0" ServiceTime "67" RemoteAddress "183.192.226.145"
RPUSH list_key 1669849589
SADD INDEX "/"
HSET my_key#1669863752 AgentString "Twitterbot/1.0" ServiceTime "10" RemoteAddress "199.59.150.182"
RPUSH list_key 1669863752
...
QUIT
```

You can execute the script using the running docker container as follows:

`docker exec my_redis sh -c "redis-cli < /path/to/file/in/container.redis"`

One thing to remember is to put `QUIT` at the end of the script file so that the CLI exits, otherwise you will be stuck in an invisible shell.

### Storing Data

For comparison purposes, I tried to set the Redis data up in a similar way to DynamoDB, which is when I realised that I was wasting Redis's abilities. The Redis team has taken taken a different approach to handling a variety of access patterns by providing [more data types](https://redis.io/docs/data-types/), which is one reason why Redis is so versatile and so loved. You will see below that things turned out a little different to the Dynamo implementation.

The key difference (pardon the pun) is that Redis used a simple single key to access a value, whereas DynamoDB's key is more complicated and perhaps allows some flexibility in accessing hierarchical data. Redis however offers so many different data types for so many purposes that you quickly find yourself not worrying about this very much.

I populated the Redis table by taking the interim Dynamo operation-level data (i.e. generated from the AWS access log files but before sent to Dynamo) and converting them into Redis commands. Redis provides the HASH data type which is just like a Dynamo record. For example:

`HSET /blog/articles/2022-11-On-Greed/#1669866904 AgentString "Twitterbot/1.0" ServiceTime "23" RemoteAddress "199.59.150.183" Referrer "-"`

As a reference, this is how you would perform the same operation in Dynamodb using the AWS CLI:

```
aws dynamodb put-item --table-name MyTable --item '{"UserPages": {"S": "/blog/articles/2022-11-On-Greed/"}, "SortKey": {"S": "1669866904"}, "Referrer": {"S": "-"}, "AgentString": {"S": "Twitterbot/1.0"}, "ServiceTime": {"N": "23"}, "RemoteAddress": {"S": "199.59.150.183"}}'
```

Yuk. However, I was able to match the storage format using Redis with what I used in Dynamo.

## Leveling Up

It was at this point that I realised I had made a mistake with my DynamoDB model. I will cover this in a later post, but in essence the method I was using to count page accesses was tied to the size of my table, which was a very bad thing for performance as well as cost as the table size went up. It's also important to note that these type of scanning operations are typically blocking operations, which have other performance knock-ons. Unfortunately there are still a lot of questions in Stack Overflow about how to count the number of keys matching a pattern in Redis, which exhibits exactly this problem.

![Level Up](images/4x1up.jpg)

The variety of data types available in Redis opened my eyes over how to improve the data structure. This came down to two things:

 - Use the hash incrementing command (HINCRBY) to keep track of visits
 - Use a list for page access times as well as storing each access record individually

Redis makes this very easy because of its rich command set. I decided I would also do the same thing in Dynamo. Below is a table comparing the commands:

| Purpose                     | Redis                     | Dynamo                         |
------------------------------|---------------------------|---------------------------------
| Push to a list              | `RPUSH <key> <item>`        | `SET #key = list_append(if_not_exists(#key, :empty_list), :val)`
| Increment a field/attribute | `HINCRBY <key> <item> <val>`| `ADD #attr :val`

It is true that you can put a Lambda between the client and your Dynamo table to do about anything you want, but it is much nicer to have these types of data handled natively. Because DynamoDB tries to be more flexible with lower-level commands, you need to handle data initialisation (like the empty list above), which feels a little clunky. Redis however knows that `RPUSH` is a command for lists, so if there is no value present for the given key it automatically creates a list.

### Performance

So how do things compare now that we have our new data structures? It means that we can access a single entry instead of having to process multiple. The results not only in faster access times but also in lower cost in the case of DynamoDB. In the interest of revealing what a bad table implementation looks like, I also ran the tests on the old data model.

| Query                      |  Dynamo Query | Dynamo Get-Item | Redis Key Scan | Redis Get Key |
-----------------------------|----------|---------------|----------------|--------------------------
| Page visit totals          |  1000ms   |  200ms  |  250ms  |  180ms  |
| Page history list          |  270ms    |  220ms  |  170ms  |  160ms  |

The key thing to remember is that the difference in performance is present for only 1,500 total records; as the table size increases, the 'Query' and 'Key Scan' operation times will increase proportionally whereas the 'Get-Item' and 'Get Key' operation times will stay the same, which is exactly what you want: consistent and predictable read-times regardless of scale.

_Note that this test is not very stringent and compares the time in the libraries (boto3 and redis-py), so take the timings with a pinch of salt._

### Different goals

As mentioned above, Redis still requires you to think about design if you are going to get the most out of it. I solved my own design problem in two different ways: using a counter and using a set. As we have discussed, both are much faster and more scalable. So you still need to perform some up-front design thinking and architectural spiking to ensure that you catch as many access patterns as you can and design your database appropriately.

Server vs Serverless is also a big thing: it forces you to think about costs in different ways. DynamoDB charges users on data access (both writing and reading), and also on data storage volume (however you do get 25GB free, which is pretty big). Redis on the other hand needs to be run on a server and as such comes with a fixed monthly cost, depending on your provisioned memory size. Surveying a few Redis providers shows that this cost varies between about US$5 (introductory rate) to US$50. Using the AWS DynamoDB calculator showed that you would need to be operating at nearly 100 million accesses per month to be charged $50 on-demand pricing (for reference, there are 2.6 million seconds in a month).

The cost benefits for a small project are certainly on the side of Dynamo, but the larger variety of data types and server-side processing does make Redis very attractive. It is probably worth starting with Redis locally with Docker, because it is quick to set up and test your data model. If you then decide to use something else then you will have lost the least amount of time, and if you switch to Dynamo then you will have a good handle on what your data model should look like.

### Right Tools? Right Job?

It is important to take the discussion a level higher and look at the type of application. In general there are two types of data applications: OLAP (On-Line Analytics Processing) and OLTP (On-Line Transaction Processing). OLAP is traditionally in the realm of relational databases and their ability to query data in many different ways based on the schema. OLTP deals with active usage by millions of live users, typically performing the same operations and workflows over and over again.

The example of a web-tracking tool seems to fall somewhere in the middle - when dealing with a website with high-frequency access, you want to get some of the features of OLAP, but the information that is returned from the queries is perhaps more in the OLAP camp.

The interesting thing about this example is that the source data is provided by the AWS web-access-logs feature when you use S3 for web hosting. This is a form of structured data that is automatically written to an S3 location, which opens up an opportunity with another tool.

![Amazon Athena](images/amazon-athena-cover.png){: style="max-height:150px;"}

## Athena

AWS Athena is a very interesting beast. It allows you to query data in-place in long-term storage (such as S3) using SQL, and it is serverless. This means that there is:

 * No server to configure
 * No database to configure
 * No data ingestion process

Athena is so suited to analysing web access logs that there is a [page dedicated to it](https://aws.amazon.com/premiumsupport/knowledge-center/analyze-logs-athena/).

### Querying data

The amazing thing is that it is so easy to get going, compared to the other options. Here is a sample sequence:

```
# Store a query
aws athena create-named-query --name totalvisits
    --database my_s3_database
    --query-string "SELECT COUNT(*) FROM mybucket_logs WHERE LOWER(key) LIKE 'my/articles/%index.html' AND operation='WEBSITE.GET.OBJECT' AND httpstatus='200'"

# Show stored queries
aws athena list-named-queries

# Retrieve the query details
aws athena get-named-query --named-query-id 09f659cd-2a59-49be-977e-cee283e3e --output json --query NamedQuery.QueryString

# Start a query
aws athena start-query-execution --work-group primary --query-string <string>

# Get query results
aws athena get-query-results --query-execution-id 337aba4d-de0a-41d3-9e90-61ff5ac3
```

This may seem a little long-winded but some of the commands are provided only for managing your queries. You should also note that you need to set up your data model first, which is much easier to do in the console.

### Performance

Performance is nowhere near that of DynamoDB or Redis, but the question is: does it have to be? Since the queries are more OLAP than OLTP, there probably does not need to be a hard time limit on serving the results, especially when this is weighed up against flexibility on designing your queries.

The hard numbers are that a query on 4 months of web logs to get a table of pages and corresponding visits takes about 2 seconds with Athena, and this will be a function of the size of the log data. It also means that you need to keep all of your data if you want to query it, and there is likely to be a lot of wastage in the data format.

But the flip-side is the cost: it is $5 to query 1TB of data. My website is 4 months old and only has 30MB of weblog data. Performing some simple calcs means that if I am lucky enough to grow exponentially, after 2 years I will have 1GB of logs and I will be paying $15/month. But this is where we must think outside the box.

### Opportunities

The key is to look for opportunities. Combining DynamoDB and Athena could look something like this:

 * Web access logs written to S3
 * Trigger lambda to strip superfluous data and write to another location
 * Trigger second lambda to write common statistics to Dynamo, which can be delivered quickly
 * Use Athena to perform custom querying

This way, you would get the cost benefits of both systems, as well as the performance and querying flexibility of each separately. It is very possible to run advanced analytics on a popular website like this for a dollar a month. As usual it is often better to be competent in multiple systems, and proficient in only a few.
