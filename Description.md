# Overview of hosting a static website with continuous delivery on S3

This file provides an overview of the steps taken to host a website on AWS S3.

## Purpose

The purpose of this project was to demonstrate how a static website could be hosted simply on AWS and use AWS pipeline technology to perform DevOps-style continuous deployment.

## S3 Hosting

The website is hosted on AWS S3. This is straightforward to do in CloudFormation, however you need to remember to assign a Bucket Policy in order to allow the public to access it (but not modify it).
The bucket also needs to be put into 'WebSite' configuration mode so that it can serve the index.html file.

## IAM/Role Setup

The first thing to do is create a role that is designed to access (and only access) this project. Using your root account (or preferably a power-user account that you have already created), make a new group with the appropriate permissions for managing the S3 bucket and the deployment pipeline (from the set of standard AWS managed policies). You can then add a user to this group, and use that user to access that project.

The purpose of doing this is to limit the 'blast radius' of the user/group, so that the user cannot do anything they are not supposed to do.

Potentially a better way of doing this is to create a new account, linked to your main account, with a role inside it which has the appropriate permissions. You can then enable members of a group to take on that role in order to do things in the new account. The additional benefit of this is that you can use that role in your AWS CLI config in order to administer the project, which will mirror the benefits of enforcing users to adopt that role in the project account.

_[This can be the subject of another IAM talk: product accounts (for better traceability), roles, automated setup with CF...]_

You will also need a role with which to execute the pipeline, but that is covered in a following section.

## Pipeline Creation

The Pipeline is the most complicated part, even though its parts are simple. You need to define two stages in the pipeline, one to get the source from gitHub, and one to deploy it.

Pipelines are defined in 'Stages'. Our pipeline has 2 simple stages: a 'source' stage (to checkout the repository) and a 'Deploy' stage to deploy it. The source stage needs to be configured with the correct GitHub owner and repository, and the deploy stage needs to know where the outputs from that stage are together with information on the target (in this case S3). Because the code obtained from GitHub is a zip file, the Deploy stage also needs to specify `extract: true`.

This also requires us to grant AWS CodePipeline permission to access our GitHub repo for the Source stage. This is done by providing a GitHub OAuth token. This is generated manually from GitHub, and is passed to the Pipeline stage in CloudFormation. Note it is best to do this as a parameter, *not* to hard-code the token into the CloudFormation file. (Coincidentally, if you check a file into GitHub that has a string that matches an OAuth token that it has generated, it will delete the OAuth token. This is a good demonstration of DevSecOps).

One of the odd things is that the pipeline needs a place to store the checked-out artifacts. This is typically an S3 bucket. At the moment this means that we need to create a second bucket to do this, and also means that in the future we will need to come up with a method of cleaning this bucket up. (TODO)

## Webhook Creation

This is all great, but currently we need to manually kick off the deployment. In order to automate this, a Webhook is used to kick off the pipeline when GitHub notifies the URL endpoint that something has happened. In the CloudFormation, you must specify what it is that you want the webhook to do, in our case it is to kick off the 'source' part of the pipeline.

This requires a 2-step process of creating a URL endpoint and also telling GitHub what that endpoint is. This is a little bit cumbersome because after creating the stack, you will need to run a `aws list-webhooks` command to get this and feed it back to GitHub.

On the GitHub side, once you know the URL, you create the webhook call in your project settings. The Gotcha is that you need to specify the URL payload as *JSON*.

## Routing

This was a tricky bit, mainly because I had a custom domain. I could have simply created a record in my domain provider to point at the S3 bucket, but then if anything about the bucket had changed I would have had to update manually, as well as update it manually in the first place... where is the automation in that?

Instead, I set up a hosted zone in Route53 with Nameservers that I pointed my domain provider to, and created a record to point to my S3-hosted website.

This is where things became a bit unstuck... Firstly the documentation is a bit wacky around how to set up the alias record. It turns out you have to use some hardcoded hosted zone IDs and region-specific endpoint names in your CloudFormation, which was not straightforward to understand. Secondly, an important part of the puzzle to get this DNS routing to work is that _your S3 bucket name has to have the same name as the *URL you wish to access it* with_. I found this snippet buried away in a support forum - (It's actually hidden away in this bit of doco: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/RoutingToS3Bucket.html).

Fortunately, because everything is code, I just added a parameter and referenced it through the CloudFormation, and then ran update-stack. After some messing about with deleting a non-empty bucket (gotcha) then everything was fine.

### Routing both sites

This is a simple method of having one bucket that routes to another. The root domain appears to try to route to an S3 bucket that is called the same as the domain (but I'm not sure why this happens). Since there isn't one, we just have to create one which redirects everything to the `www` bucket, which does have the website content.

## Contact Form Implementation

The contact form server-side setup was fairly straightforward. You can add an `SES:EmailIdentity` to your cloudformation and AWS will identify the new resource and verify the email address by sending a verification email to it. Once the user verifies it, you can use this email address in a boto3 `ses.send_email` call.

A serverless lambda is then deployed which is triggered from an APIGateway. The lambda simply takes POST data and executes the email action. The contact form can execute the POST data.

### Service idea:

Can infrastructure be set up to *create* email addresses, and assign a lambda to it so that contact forms can be dynamically created by a user?

  - User requests a contact form endpoint
  - A lambda creates cloudformation template for that user
  - lambda uses cloudformation call to create the SES email identity and hook up a lambda to it
  - (potentially one lambda is better for versioning purposes, but one lambda per user better for billing?)
  - User can then unsubscribe or update their email
  - How to make money? First mailbox is free? Second costs X/month? X/100 emails?

## How long did this take?

Because I experienced a bit of pain with the IAM roles and the routing, setting up the basic hosting and delivery pipeline probably took about a day. Which in the scheme of things is not a long time. If I had to set it up again it would probably take half as long.

# Advanced

## Good practices

### Parameterising the CloudFormation

In the initial CloudFormation, there is a bunch of project-specific information. It is fairly easy to see that if we remove this, we have a fairly generic CloudFormation template which could be used to roll out many S3-website-pipeline-webhook patterns which can be configured for different projects.

In order to parameterise the CloudFormation, simply add a 'Parameters' section to the top which defines them. This allows us to do thinks like define a root name for the project which we can prepend to all the infrastructure.

We can put these parameters into a file, but it is unsafe to store things like OAuth tokens in a file like this.

### CloudFormation Linting

This can be done with a simple program like `cfn-lint` for python. This will go through your template and let you know if you have any errors.

A neat way to do this is to download a docker image that has a slim version of Python installed and run the command from there, if you don't want python packages to pollute your local environment.

## Monitoring

### CloudWatch and Error Notification

A Cloudwatch event rule can be set up to listen for failures of all or part of your code pipeline. This is fairly straightforward, but there are a few gotchas...
 - CloudWatch event groups have to be prefixed by `/aws/events/` it seems
 - In order to publish to an SNS topic, CloudWatch Events have to be granted the appropriate permissions

Once these are solved, the cloudwatch rule can be created to match specific events based on some of its published details, and then both log the event and also publish the event (or part of it) to SNS where it can be distributed to subscriber endpoints. Again, this can all be defined in cloudformation.

(More advanced: this can form a different cloudformation template which uses outputs of the web stack template)

### Website health monitoring

This can be achieved very simply by adding a lambda which simply retrieves the site and checks for a `200:OK` status. Because it is a static website there is not much else you can do, except perhaps check that the size of the page is not really small (e.g. it's accidentally been deleted...). This can then raise an SNS notification (which can send you a text).

This was done with the serverless framework, which is a very simple deployment (in fact using SLS might be overkill, but it's simpler for a developer!). The main requirements are:
 - Need to set up a timer
 - Lambda needs permission to write to the SNS queue
 - Lambda needs access to the SNS queue ARN to use
 - Use a few environment variables

### Sub: Re-creating the site if it is accidentally deleted!

I did test this because I had to rename the bucket. Deleting the bucket, re-running the cloud formation and then running the pipeline all works fine and the site is re-deployed in a few minutes.

Following on from the above health monitor, if the site returns a code which indicates the site is not there (404 maybe?) then the lambda could also kick off the pipeline deployment again.

## Upgrading

### Dependencies

The current dependency list is:

 - Docker:
   - amaysim/serverless 2.72
   - Python 3.9.7
   - mkdocs 1.3.1


### Upgrading the docker image

The docker image is referenced in the Dockerfile. You can refer to a new version here and then run

`docker build -t <your tag name> .`

**NOTE: This will always get the latest MKDocs, because there is no `requirements.txt` file to lock the version.

You should then test the following:

 - Build the mkdocs image
 - Anything else??

### Upgrading Python

Note that the python version in the docker image (tested above) affects the following:
 - The MKDocs build
 - The lambda to test the website health

 The MKDocs build is affected by the python version in the CodeBuild image. This is defined in the `buildspec.yml`, and is deployed when the website is pushed to github (the codebuild image will look for `buildspec.xml` in the root folder which is being deployed). This can therefore be tested when the latest blog version is pushed to github.

 The health-test lambda is deployed with the serverless functions, and so can only really be tested when the lambda is executed. The health-check lambda is currently run every 30 minutes, or can be run manually from the console or invoked using `sls`. In the future it might be better to test this on deployment somehow, or have an SNS which notifies someone of a failed execution.

## Meta
### How long did this take?

Cloudwatch was a bit tricky, and had a few manual steps, but once that was solved, it took maybe 2 hours total. The lambda probably took less than 2 hours.

## A better DevOps example: adding a build step

In order to demonstrate DevOps practices more advanced than just copying a repo to an S3 bucket, I decided to use a static website generator to convert my blog articles into a website and host them in the same location. And of course use it to deploy website updates.

### CodePipeline and CodeBuild

First up was creating a codebuild to perform the simple task of generating the static site. I did this by using MKDocs, a python-based static site generator, and then used CodeBuild to perform it in my DevOps CD pipeline.

Codebuild is fairly simple with CloudFormation, however as with most services you need to define a ServiceRole, and it takes a bit of time to make sure that you grant the role the appropriate permissions. In our case we just need access to creating logs and the S3 buckets where the source and output artifacts are hosted.

Gotcha: You need separate permissions for the Bucket and the Bucket Contents, since these are different actions.

Setting up a buildspec is also fairly straightforward; the main thing is to specify the build envronment (python), install libraries that you need for the build (MKDocs), and then list the build steps.

Gotcha: If you want to use the `**/*` glob to copy the whole directory as the output artifact it needs to be quoted: `"**/*"`.

Gotcha: Because we are deploying to a public Web-site S3 bucket, you need to turn off encryption, otherwise no-one will be able to read it!

Downside: When debugging CodeBuild and the `buildspec.yml` file, it can be a bit painful as you will need to keep uploading your source ZIP file and invoking CodeBuild to check the output. However there is the ability to run the build locally.

### Integrating with CodePipeline

Integration with CodePipeline is simple; you just have to change the `Source` and `Artifact` types to be `CODEPIPELINE` and it just works. CodePipeline takes care of passing the artefacts between stages. Note that you still need a deployment stage because CodeBuild will not longer write to your chosen artifact deployment bucket - instead it passes it on to CodePipeline.

The service role becomes slightly simpler in this case as CodeBuild no longer needs to access anything other than the artifact bucket.

## Future:

### Trigger pipeline run on bucket creation, in case you have to recreate the bucket.

### Split into 2 repos

Because submitting changes to the Stack shouldn't really cause the pipeline to re-run (unless you are doing some inception stuff). So they are dependent on each other but only one way.

### Put sensitive keys into secure storage

Because even though the parameters are only local, some of them should probably be checked in with the pipeline (or maybe the website code), and some (like API keys) end up being visible on the stack information page.

## Best Practices???

