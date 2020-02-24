---
disable_toc: true
revision_date: ##sed_date_here##
title: Forshaw.Tech Blog
---

A collection of articles written by me.

## About this site

In the interest of keeping things simple, and to eat a bit of my own dogfood, this site is hosted on an AWS serverless bucket and generated using CodePipeline and a static site generator [MKDocs](www.mkdocs.org).

An overview is presented here.

### Basic Overview

A basic overview is shown below

![Basic design overview](StaticWebSiteDevOps_Basic.png "Overview")

The website is hosted on an S3 bucket, which has a Policy attached which allows it to be viewed by the outside world.

A pipeline is defined which is kicked off by a Webhook. The Pipeline checks out the code and then runs CodeBuild (not shown on diagram), and then deploys it to the S3 bucket. The Pipeline is granted a role to be able to do this. It also has an intermediate 'deployment' bucket to operate with.

If there is a problem with the pipeline, CloudWatch has a rule to publish the failure to a SNS topic, which then pushes it out through a subscription.

### Other things

There is also a lambda which periodically checks the website health and pushes a notification to the same subscription if it detects a problem.


