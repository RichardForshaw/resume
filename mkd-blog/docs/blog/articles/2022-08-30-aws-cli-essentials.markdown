---
layout: post
title:  "AWS CLI and Docker Essentials"
description: "Over a few years I have built up a small library of home projects deployed on AWS. When I need to revisit them it is easy to forget many of the key CLI commands and configuration items that I need most often to get back up and running."
revision_date: "2023-01-31"
tags:
    - Cloud Development
    - AWS
    - Docker
    - Serverless
    - DynamoDB
author: Richard Forshaw
---

A few years ago I had built up a small library of home projects deployed on AWS as I built upon my knowledge of cloud-native apps and infrastructure. Those projects are still active but have been neglected, and in the world of tech, to neglect knowledge is to destroy it. Amongst that neglected knowledge is the use of the Command-Line Interface (CLI).

I am very much an old-school keyboard lover, and I prefer being able to type commands to execute them rather than using dashboards, buttons and deployment consoles. Typing commands also lends itself to scripting and to maintaining executable definitions, which in turn is the foundation of infrastructure-as code, which in my book is also a good thing.

As with a lot of AWS documentation, there is a focus on _what things do_ rather than _how to do something_, and I often want to combine the _what_ and the _how_ to re-construct my own version of the manual in my brain. So when it was time to jump back into my old projects (and perhaps do a few new ones), I had to re-familiarise myself with using the AWS CLI in order to re-familiarise myself with my project structures. In the spirit of documentation and spreading of knowledge, this article is a collection of the commands and configuration that came up, and tend to come up often, so I don't have to google them repeatedly, and now hopefully neither do you.

![Docker Lambda and Serverless](images/docker-lambda-serverless.png)


## Tools

The tools used in this article are as follows:

 - Docker
 - [amaysim/serverless](https://hub.docker.com/r/amaysim/serverless) docker image (v2.72)
 - AWS CLI
 - [Serverless Framework](https://www.serverless.com/)

This combination may mean that some of the examples below may not map exactly to your particular use case or configuration, so please bear that in mind.

## Container Configuration

I tend to do my development in Docker. Because of this, in order to use the AWS CLI in docker, it has to be configured with your AWS credentials etc. You can do this by running `aws config` every time you run your container, but you can see how that would get annoying quickly. If you have other AWS accounts and projects, it is also likely that you have one `credentials` file (and maybe a `config` file) which you share between these projects.

The best way to do this is to make your AWS `config` and `credentials` files available in the docker container. According to the [AWS Documentation](https://docs.aws.amazon.com/sdkref/latest/guide/file-location.html), the files should be stored in your home folder (i.e. in `~/.aws/`, assuming you are using a Linux-type container). The best way I have seen to do this is to mount this directory as part of your container creation process, i.e.:

`docker container -v <dir of your files>:/your/home/.aws ...`

**Windows users NB**: If you use an absolute path or one that has a space in it, use **single quotes surrounding the entire mount argument**, i.e. `-v 'C:\Users\My Name\my aws files:/your/home/.aws:ro'` ('ro' is to specify a read-only mount if you want that).

Once this is done, there are two ways of accessing the correct profile:

 1. start your Docker container with the extra argument `-e AWS_PROFILE=<your profile>`. This will set the AWS profile name in the environment that is always used.
 2. add the argument `--profile <your profile>` to each AWS command that you run in the container. Note that this overrides the value set in (1)

If you are going to be using the same profile for many commands (e.g. you are firmly in the development stage), then (1) is the better option. If for example you are setting up your AWS environment and will be executing commands with different profiles, then (2) is probably better, however you can still do (1), and then override it with (2) when needed.

![Beware](images/watch-your-step.png)

### Gotchas

The AWS config & credentials files are tricky beasts, and they are still not very well documented. If like me you keep multiple profiles for multiple project (as you should as a best practice!), you need to remember some key things about these files. You can check out the AWS documentation [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html), but here are some distilled key points.

_(Note this list assumes you are familiar with setting up CLI credentials for your project, or already have them set up, as in my case where I am returning to an old project)_

 1. The profile name in `config` must match the config section name in `credentials`. Don't get mixed up using `source_profile` parameters - this is used for IAM assume role, not as a link between profiles and credentials.
 2. The config section in the `credentials` supports some of the fields used in the `config` file, and takes precedence over them. So if you are using `config` profiles in a simple way (e.g. just setting a region), there may not be much point in using them at all since the same configuration can be stored in the `credentials` file.
 3. The `config` file can be used for simple separation of sensitive data (e.g. you can probably get away with checking your `config` file into source control or putting less security around it, but DON'T put less security around your `credentials` file!), but it is probably best used for configuring IAM assume-role operations, since the previous 2 points basically make trivial profile configuration a bit clumsy. The corollary to this is that if a framework or tool you use in turn uses the AWS CLI and thus requires one or both of these to be present (check your tool's documentation!)

### Networking Tips

By default, if you run multiple containers, they should be able to talk to each other. Generally any container you start will connect to the default 'bridge' network. If you inspect this network with:

`docker network inspect bridge`

You will see what containers are connected to it and what their IP addresses are, for example:

```
[
    {
        // ...
        "Containers": {
            "3978ee54a4517e...0a7cdd3c4c649e": {
                "Name": "my_redis",
                "EndpointID": "36e06b4...d258d5598068c012",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            },
            "dc746d52534793...66ff756dcce146c": {
                "Name": "my_service",
                "EndpointID": "a5bb314e...33dc486d9381093e",
                "MacAddress": "02:42:ac:11:00:03",
                "IPv4Address": "172.17.0.3/16",
                "IPv6Address": ""
            }
        },
    }
]
```

In this example I was playing around with Redis, and I could connect to it from my service container at `172.17.0.2`.

If you are doing more deliberate networking things then you should create and connect to a defined network. This is most easily done in a docker-compose file as follows (again using Redis as an example):

```
version: '3.6'

services:
  redis:
    image: redis:6.0

  myservice:
    build: .
    image: myservice

    environment:
      - REDIS_URL=redis://redis:6379  # <- The container can by accessed by its name

```

## Maintaining Dependencies

I've created my fair share of containers in Python and Javascript, each with their own quirks, and maintaining the dependencies of your project is always something that comes up. This is a small detour from the primary subject of the article (and probably warrants a more complete article), but it is a worthy one, since regardless of your language of choice, you will probably:

  a. be doing some local testing, thus will need to have local dependencies
  b. be packaging up these dependencies somehow to deploy them somewhere
  c. want to manage your dependency versions and not have them upgraded silently (e.g. when you build or start your container)
  d. want to keep things clean in your Docker container

For Python, dependency management is usually straightforward because the standard way is to install them globally. In the old days (i.e. 'pre-Docker' days), to manage multiple Python projects you typically had to use [virtualenv](https://virtualenv.pypa.io/en/latest/) (and _virtualenvwrapper_... whistfull sigh), and you then proceeded to create multiple environments and switch between them. But then Docker came along and (in my opinion) solved this problem by giving you a full virtual machine in which you could isolate you entire environment (not just your Python one).

I tend to maintain a number of requirements files: `requirements.txt` (the standard one), `requirements-dev.txt` (for development tools) and `requirements-test.txt` (for test tools). The reason for splitting them is that when you deploy your service, you only want to deploy the dependencies required to run the service; in the same vein, if I have a CI/CD solution, I generally want to only deploy the service requirements and the test requirements.

This is done simply enough with the following lines in `Dockerfile`:

```
# Setup a temp location to use to install libraries
RUN mkdir /code
WORKDIR /code

# Upgrade pip
RUN pip3 install --upgrade pip

# Install python packages
ADD requirements.txt /code/requirements.txt
ADD requirements-test.txt /code/requirements-test.txt
RUN pip3 install --no-cache -r /code/requirements.txt
RUN pip3 install --no-cache -r /code/requirements-test.txt
```

Javascript is a trickier beast. Because NPM installs into the `node_modules` folder, and that folder is typically present in your working path, we run into a 'layer masking' issue.

There are 2 ways you can deal with Javascript's `node_modules`, and it is up to you which one you choose as they both have pros and cons:

 1. You can simply choose to build and run your Docker container, and run `npm install` in the running container with your local code volume mounted. This works fine, but has the side-effect of adding your node_modules folder to the host computer (because it is run in the mounted volume). This does not present any functional hurdles, but I don't like it because:
    - it means that code 'spills over' out of your nice contained dev container
    - you then have to exclude the `node_modules` folder in your `.gitignore` file
    - it means you have to remember to run `npm install` when you create your container (or alternatively run a script at container start-up which just adds overhead to your startup)
 2. The other way is to build the NPM install into the Dockerfile, so that it runs when you create the container. This keeps the `node_modules` folder in the container and keeps your code tree on the host machine cleaner. This does mean that you need to build the docker container whenever the `package.json` file changes, but I argue that this represents a new version of the development environment and should in fact warrant a new container build and version.

You can implement (2) with the following simple Dockerfile code:

```
WORKDIR /opt/myproj/
COPY package.json package-lock.json ./
RUN npm install
```

However this is where we hit the snag; when you run the container, you will do so with a `-v ${PWD}:/opt/myproj/` option (or your particular variation). When you then try to run your javascript code, \*poof\* the `node_modules` folder has disappeared. This is because the volume you mounted into the container, having been done after `docker build` built the filesystem, has now masked the files that npm installed there (since they share a common parent directory).

You can solve this by some Docker volume magic. If you create a volume for your node modules:

`docker volume create node-modules`

You can then add an extra `-v` argument to your docker command to mount the volume at the location of your _container's node_modules folder_, and despite it being initially hidden by you mounting your code folder, the new mount instruction supersedes that instruction and reveals the once-hidden folder:

`docker run ... -v node-modules:/opt/myproj/node_modules ...`

This is a bit of a mind-bender, but it works. It is described a bit more elegantly using docker-compose in [this excellent post](https://jdlm.info/articles/2019/09/06/lessons-building-node-app-docker.html).

## Stacks and Deploys

_[From this point on, this article assumes that you have `AWS_PROFILE` set to your profile and you are querying your default region, so `--profile` and `--region` arguments will be omitted.]_

![Toppling dominoes](images/domino-push.jpg)

### Some Philosophy

There is more than one way to deploy your stuff - historically I have mixed manual Cloudformation and serverless config. (Yes there is also SAM, but I have not migrated my existing projects to that yet!) I have done this because while serverless is great for running serverless things (things that execute), some AWS infrastructure is best kept out of the serverless config files, in my opinion. This opinion is based on the following:

  1. Some AWS infrastructure is simply not supported by Serverless; this is because Serverless is for _creating apps_ on AWS (and other providers). Apps usually have business logic (i.e. functions) bundled with them, and so the Serverless framework is really designed around deploying this logic (i.e. Lambdas) with its associated infrastructure (e.g. REST endpoints, queues, databases).
  2. It is good practice to separate concerns of your app. If you have everything in your serverless project, then when you tear it down you tear it **all** down. Sometimes you want to deploy and test infrastructure separately, or maybe some of your infrastructure is used by multiple functions or projects, or has a different life-cycle to other infrastructure. One example is the routing for your website or email infrastructure. Another example may be your database or backup database. If you run a `sls remove`, do you want those things to disappear as well?

This also warrants a more detailed post!

### Useful Commands

You probably tend to run the same commands over and over. Here is a refresher for the ones you will probably run the most.

|                                 |  AWS CLI                         | Serverless         |
|---------------------------------|----------------------------------|--------------------|
|  List your stacks / projects    | `aws cloudformation list-stacks` | `sls info [--verbose]`  |
|  List stack content / functions | `aws cloudformation list-stack-resources --stack-name <the stack name>` | `sls deploy list [functions]` |
|  Deploy a stack / function      | `aws cloudformation create-stack --stack-name <the stack name> --template-body file://my-file.json`  | `sls deploy [-f function]`  |
|  Deploy with a parameters file  | `aws cloudformation create-stack <see above params> --parameters file://my-params-file.json `        | Parameters are handled differently  |
|  Update a stack / function      | `aws cloudformation update-stack <see above params>`         | `sls deploy [function -f function]`      |

_Extra notes: If your cloudformation file contains IAM specifications, you must append `--capabilities CAPABILITY_NAMED_IAM` on the end of the aws command._

## Formatting and Filtering Output

Simple output formatting can be controlled with the CLI command line or the `config` file. Output is by default returned as JSON output, which can be difficult to read. A simple flag can convert this into a table format which is easier to read than the JSON format:

  - as parameter: `--output table`
  - as `config` file option: `output = table`

If you do want to list as JSON (perhaps you wish to pipeline the output to something else), then you can do some filtering of the output. This has proven to be useful to me for example with commands that return a large amount of data. This is of particular note when faced with data returned from Dynamo, when faced with a large query result but you only want to see a few fields.

There are two types of filtering: client-side and server-side. The critical thing to note is:

  - client-side filtering is done by the CLI tool and occurs **after the information has been received** from the server. This if you are concerned with internet traffic, this filtering does not affect what is sent from the server, only what is rendered to you
  - server-side filtering is done (as the name suggests) on the server, and reduces the traffic that is sent to you. Because it is server-side, it is only supported by some services, typically those which are likely to return large data sets (such as DynamoDB)

### CLI examples

Filter only stack ID, name and update time:

`aws cloudformation describe-stacks --query 'Stacks[*].[StackId, StackName, LastUpdatedTime]'`

Show stack name and ID for stacks whose name contains 'database':

``aws cloudformation describe-stacks --query 'Stacks[?StackId.contains(@, `database`)].[StackId, StackName]'``

### Dynamo examples

Dynamo is a more complicated beast, but when your database gets big then server-side filtering will be helpful in saving bandwidth and increasing responsiveness. You should be very careful to note the difference between _querying_ and _filtering_, as there is a subtle distinction. I shall not attempt to explain it in full here, instead jump into [Alex Debrie's excellent article](https://www.alexdebrie.com/posts/dynamodb-filter-expressions/).

**First, a warning.** What I will say here is that _some server-side filters don't look like filters_, and will incur costs on your Dynamo read capacity without you knowing it. I'm looking at you: `ProjectionExpression`.

Any well-read DynamoDB enthusiast will know that using a filter-expression still means that many more items are read from the table than what is dictated by your filter expression, but you might not know that _this also happens at the item level_ with a projection expression. So, and this is worth highlighting:

 > if you have structured your data as an item with many attributes and one of your access patterns is to retrieve a single attribute (this is quite common if using Redis), _Dynamo will read the entire item before applying the projection_.

 This means that if your item takes up many Read Capacity Units (the unit of cost), then you will be charged the full amount to read the item even though you are only accessing one attribute.

Be warned. Now, back to some Dynamo examples.

Query database based on a partition key and sort key:

`aws dynamodb query --table-name mytable --key-condition-expression "PKey = :pkey AND SKey > :skey" --expression-attribute-values "{ \":pkey\": {\"S\": \"PARTITION#key\" }, \":skey\": { \"S\": \"SORT#key\" } }"`

Query and then filter the fields to view:

`aws dynamodb query --table-name mytable <query params> --projection-expression Attr1,Attr2,OtherAttributeNames`

_Warning! The above query still reads whole items that match the query (see above)_

### More Filtering

I'm glad you want to know more about filtering - for more advanced filtering techniques, head over to [this post](./2023-01-31-aws-cli-advanced-tips.markdown)

## Other Useful Things

![Toolkit](images/toolkit.jpg)
### S3 Globbing

S3 is a wonderful storage system, especially because it can serve web content directly. I use it for storing web access logs (which I write about in [another project](./2022-11-DynamoDB-Page-View-Tracker-Pt1.markdown)). But some things it doesn't do well, like handling wildcard access for syncing files. So if you want to sync some files according to a simple pattern, do this:

`aws s3 sync s3://<bucket-name>/<path> . --exclude * --include <pattern>`

This processes the parameters in order, excluding everything and then including files based on your pattern. This is essentially doing the same as a typical `cp <pattern> .` command but written in a less obvious way.

_Gotcha: It is best to wrap the patterns in quotes. This is because if it is not in quotes, the command shell will try to interpret it instead, and will try to replace the pattern with a list of local files._

### CURL

You can't write AWS-based web-services without knowing a bit of CURL. You just can't. It is likely that most serverless-oriented people will be deploying some kind of API which returns results as JSON, and the easiest way to test them is by calling the endpoint, and CURL is the easiest way to do that. Here are some basic CURL commands which you may use often, together with how to decode the AWS event in Python.

<table>
<thead><tr><th>Example<th>CURL Command<th style="width: 45%">Python decoding of Lambda event</tr></thead>
<tbody>
<tr>
<td>Call an endpoint
<td>

<code>"curl http[s]://your.endpoint"</code>

<td>
[None]
</tr>
<tr>
<td>Call an endpoint with parameters
<td>

<code>"curl http[s]://your.endpoint?your_param..."</code>

<td>

```
event.get('queryStringParameters').get('your_param')
```

</tr>
<tr>
<td>POST with parameters
<td>

<code>"curl -X POST http[s]://your.endpoint?your_param=..."</code>

<td>
[Same as above]
</tr>
<tr>
<td>POST with form data
<td>

<code>"curl -d "your_param=..." http[s]://your.endpoint"</code>

<td>

```
from urllib import parse

parse_qs(parse.unquote(event.get('body'))).get('your_param')
```

Note that this method interprets each parameter value as a list. If each value is a single item, you can instead do:

```
from urllib import parse

dict(parse_qsl(parse.unquote(event.get('body'))).get('your_param'))
```

</tr>
<tr>
<td>POST with form data (base64 encoded)
<td>

<code>"curl -d "your_param=..." http[s]://your.endpoint"</code>

<td>

```
import base64
from urllib import parse

body = base64.b64decode(event.get('body))
parse_qs(parse.unquote(body)).get('your_param')
```

(The same caveat applies as above)

</tr>

</table>


