---
disable_toc: true
revision_date: ##sed_date_here##
title: Forshaw.Tech Blog
---

A collection of articles written by me.

## Latest

### Multiple Layers of Software Quality

"I had a discussion recently where I was asked: 'How do you go about ensuring quality in your software?' I used to think this was a simple question, but that was when I was young and I only looked at the world in a certain way. After several years of experience I am uncovering and understanding more aspects of quality." [...More](articles/2022-10-08-Layers-Of-Software-Quality.markdown)

### Getting To Know Modern Javascript

"Last year I undertook a large project in Javascript, and I was able to dig a bit deeper into the language, instead of just using it to manipulate web pages. I noticed the same thing happening, and I have been since reminded about how many cool things you can do in JavaScript these days to write clean, compact and concise code." [...More](articles/2022-10-06-getting-to-know-javascript.markdown)


## About this site

In the interest of keeping things simple, and to eat a bit of my own dogfood, this site is hosted on an AWS serverless bucket and generated using CodePipeline and a static site generator [MKDocs](https://www.mkdocs.org).

An overview is presented here.

### Basic Overview

A basic overview is shown below

![Basic design overview](StaticWebSiteDevOps_Basic.png "Overview")

The website is hosted on an S3 bucket, which has a Policy attached which allows it to be viewed by the outside world.

A pipeline is defined which is kicked off by a Webhook. The Pipeline checks out the code and then runs CodeBuild (not shown on diagram), and then deploys it to the S3 bucket. The Pipeline is granted a role to be able to do this. It also has an intermediate 'deployment' bucket to operate with.

If there is a problem with the pipeline, CloudWatch has a rule to publish the failure to a SNS topic, which then pushes it out through a subscription.

### Other things

There is also a lambda which periodically checks the website health and pushes a notification to the same subscription if it detects a problem.


