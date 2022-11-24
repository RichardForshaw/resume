---
revision_date: "2022/11/24"
---

I have over 20 years of experience with developing and delivering software. I still love doing that, but I also love helping and mentoring the next generation of coders to become better. Software is everywhere and is developed everywhere; I believe it is important to build the talents of the new programming generations on the experience of the last.

This blog seeks to provide tips on developing, deploying and delivering software well, whether that be writing robust and efficient code, automating your deployment pipelines or embracing agile delivery methods the right way.

# About this site

In the interest of keeping things simple, and to eat a bit of my own dogfood, this site is hosted on an AWS serverless bucket and generated using CodePipeline and a static site generator [MKDocs](https://www.mkdocs.org). Page visits are tracked using DynamoDB and stats are provided using lambda.

An overview is presented here.

## Basic Overview

A basic overview is shown below

![Basic design overview](StaticWebSiteDevOps_Basic.png "Overview")

The website is hosted on an S3 bucket, which has a Policy attached which allows it to be viewed by the outside world.

A pipeline is defined which is kicked off by a Webhook. The Pipeline checks out the code and then runs CodeBuild (not shown on diagram), and then deploys it to the S3 bucket. The Pipeline is granted a role to be able to do this. It also has an intermediate 'deployment' bucket to operate with.

If there is a problem with the pipeline, CloudWatch has a rule to publish the failure to a SNS topic, which then pushes it out through a subscription.

## Other things

There is also a lambda which periodically checks the website health and pushes a notification to the same subscription if it detects a problem.

