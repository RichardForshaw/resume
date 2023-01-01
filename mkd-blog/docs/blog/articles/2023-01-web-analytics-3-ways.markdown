---
layout: post
title:  "Web Analytics 3 Ways"
description: "I recently used AWS DynamoDB to demonstrate how to build a simple web analytics tool. In this post I compare that solution with two others: Redis and AWS Athena. I look at which one is the most suitable and how they differ."
tags:
    - Cloud Development
    - AWS
    - DynamoDB
    - Databases
author: Richard Forshaw
---

Recently I published a series on getting started with Dynamo DB [...], which used tracking visits to a website hosted on AWS as an example of using lambda events and DynamoDB. The Dynamo database was then queried to get the page visit statistics.

This got me thinking about what other solutions might be available to do the same thing and evaluating what would be the best tool for the job. I had previously used Redis as a caching solution but I knew that it was capable of doing much more than that. I had also briefly used AWS Athena, which had the benefit of being able to query S3 data directly.

This post looks into Redis and Athena as alternatives to DynamoDB for this specific task and answers a few questions about suitability.

## Dynamo recap

I initially used DynamoDB to store the page visits. I tried to carefully design the Dynamo data model based on my expected access patterns, but I still think I managed to get s few things wrong:

 1. Using Dynamo makes you focus on minimising the spread of data over your table, because this is what costs money (and it also influences your access performance). Because of this I probably still made a couple of mistakes (below)
 2. Using a query when a list was better. When returning time sequences, a list would be better because it only hits one key. However this presents two problems:
   - Information is duplicated, which I don't like; to maintain a list of access times as well as the access data puts the same information in two places which means that you have to start considering atomicity.
   - Dynamo lists only support get and set operations, so if you want to do a count you still have to run a Query.
 3. On top of this if you want to support simple counts then you also run into duplication issues...

To improve the current solution I would do the following:

 1. Implement the index as a single item of page_name: views attributes. Use the `ADD` update method to update these on each page view. Then all totals can be retrieved in one go
 2. If that is not desirable, implement the page index as a set, not a separate entry each. Then there is no need for the conditional `attribute_not_exists` function.


## Redis

Redis (REmote DIctionary Server) is an in-memory advanced-key-value database which outgrew its original key-value behaviour long ago and now provides many types of data storage options. And it is lightning fast. It is definitely worth getting to know. Perhaps two of its most famous users are Twitter and Instagram, which have used it to serve millions of users at lightning speed.

### Setup

Redis comes as a [dockerised image](https://hub.docker.com/_/redis) and so is easy to set up and [run locally](https://redis.io/docs/stack/get-started/install/docker/) which is a massive benefit. To do this, fetch the image (in this case `redis/redis-stack` ), then run:

`docker run -d --name my_redis -p 6379:6379 -p 8001:8001 redis/redis-stack`

If you want to load data in using a script then you should also consider mounting a volume, however you can also just copy your script into the running container.

To import data into redis, you can send a redis script to the CLI. The script contains a list of redis commands like:

```
HSET my_key#1669849589 AgentString "Mozilla/5.0" ServiceTime "67" RemoteAddress "183.192.226.145"
LPUSH list_key 1669849589
SADD INDEX "/"
HSET my_key#1669863752 AgentString "Twitterbot/1.0" ServiceTime "10" RemoteAddress "199.59.150.182"
LPUSH list_key 1669863752

```

You can execute this using the running docker container as follows:

`docker exec my_redis sh -c "redis-cli < /path/to/file/in/container.redis"`

One thing to remember is to put `QUIT` at the end of the script file so that the CLI exits, otherwise you will be stuck in an invisible shell.

### Storing Data

For comparison purposes, I tried to set the Redis data up in a similar way to DynamoDB, but I ran into some trouble. However I quickly realised that the Redis team had taken taken a different approach to handling different access patterns by providing more data types, rather than extending the ways to access existing types (I guess you could say horizontally instead of vertically), which is one reason why Redis is so versatile. You will see below that things turned out a little different to the Dynamo implementation.

I created the data by taking the interim dynamo operation-level data (i.e. generated from the AWS access log files but before sent to Dynamo) and converted them into Redis commands. Redis provides the HASH data type which is just like a Dynamo record. For example:

`HSET /blog/articles/2022-11-On-Greed/#1669866904 AgentString "Twitterbot/1.0" ServiceTime "23" RemoteAddress "199.59.150.183" Referrer "-"`

You can see that there is one major different between a Redis record and a DynamoDB record: in Dynamo you can strategically design your key to have a partition key and sort key which you can query separately. Redis only has one key, however you can query keys using wildcards (In Dynamo you can only use the `begins_with` on the sort key)

In this way I was able to match the storage format using Redis with what I used in Dynamo.

### Performance

When preparing to compare performance, I immediately was stuck by how to count records. Redis does not have an obvious way of doing this server-side which means that you have to send all data to the client and count them on the client side, which is not really efficient for network traffic. For the sake of comparison I stuck with this method to see what would happen. The most expensive DynamoDB query I had was to generate all of the page totals, which used a method of getting a list of all the pages (stored under an 'INDEX' key) and querying the number of access records for each page.

I was impressed by what I saw. Performing the Total Page counts in Dynamo tended to come out at about 1.8s. Being generous and subtracting the init time put it at 1.5s. When I did the same test in Redis, I got 0.3s. I realised that these times are influenced by the speed at which the lambda calculation operates, which is limited by then lambda configuration. So instead I queried the database directly, trying to execute it as a single query. This gave me a result of about 1 second.

The next test was to retrieve all the access times for a page. This is done by querying for a set of matching keys. This is probably a better test because it involves less post-processing, and it held a similar result: Dynamo 0.2s, Redis 0.05s.

I do realise that this test is very basic and is probably not completely like-for-like, but I believe I am comparing the server-side times appropriately, and even if the test is not perfect the comparison is still significant enough to say that Redis is faster (about 3x at face value). This probably comes with the fact that it is a memory-database and memory is fast.

## Leveling Up

Enough with sticking to the original data design. I had learnt a few lessons while using Redis; what improvements could I make by using its advanced storage types? I decided to do two things:

 - Use the hash incrementing command to keep track of visits
 - Use a list for page access times as well as storing each access record individually

Note that I can use the field names of the page counter hash to get a list of pages if I needed to, so no need to store that separately. Redis supports this with "HKEYS", but in Dynamo I have to get the whole item.

The aim of this would be to reduce the access pattern to a single record. Redis makes this very easy because of its rich command set. I would also do the same thing in Dynamo. Below is a table comparing the commands:

| Purpose                     | Redis                     | Dynamo                         |
--------------------------------------------------------------------------------------------
| Push to a list              | RPUSH <key> <item>        | SET #key = list_append(if_not_exists(#key, :empty_list), :val)
| Increment a field/attribute | HINCRBY <key> <item> <val>| ADD #attr :val

It is true that you can put Lambda between the client and your Dynamo table to do about anything you want, but it is much nicer to have these types of data handled natively. The big difference between the two is that Dynamo shares commands between data types, so you need to handle data initialisation, which feels a little clunky. Redis however knows that `RPUSH` is a command for lists, so if there is no value present for the given key it automatically creates a list. Dynamo does however assume that a missing field should be initialised to zero for incrementing.

So how do things compare now that we have our new data structures?



### Thinking about design still important

... I see a lot of questions in Stack Overflow about how to count the number of keys matching a pattern in Redis. I need to do the same here but I do it in two different ways: using a counter and using a set. Both are much faster and only need to access one record rather than scan through the whole database (which is what KEYS will do, and KEYS is a blocking function.) So you still need to perform some up-front design thinking and architectural spiking to ensure that you catch as many access patterns as you can and design your database appropriately.

### Different goals

As mentioned above, Redis still requires you to think about design if you are going to get the most out of it. But you also have to think about costs, and you have to think about it in a different way.

DynamoDB charges users on data access (both writing and reading), and also on (???). However it doesn't charge you for data size (except maybe if you count using multiple tables). Redis on the other hand needs to be run on a server and as such comes with a fixed monthly cost, depending on your provisioned size. Surveying a few Redis providers shows that this cost varies between... TODO

You can argue that because you are not charged for row-based access, you don't need to worry about it like in Dynamo and you don't have to optimise so much, but you do still want to give your users fast performance. But you probably don't need to take it as far as with Dynamo, and in this case Redis is probably better cost-wise once you hit a certain user-level because your costs won't increase.

## Takeaways

It is probably worth starting with Redis, mainly because you can quickly set it up locally with Docker and test your data model. If you then decide to use something else then you will have lost the least amount of time, and if you switch to Dynamo then you will have a good handle on what your data model should look like.
