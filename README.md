# My Resume

GitHub storage for online resume. Also to demonstrate some simple CD from here to webpage.

# First principles: updating this repo

## On Windows with SSH

 * Ensure you have an SSH key in GitHub
 * Clone the repo
 * Make sure that you have set the repo up as SSH:
    * git config --local remote.origin.url git@github.com:<RepoName>
    * (Anything else to do? ssh config?)
 * Make changes
 * git push
 * Site will be automatically deployed

# Test Locally

## With Docker

Yes you can just load `index.html` into your browser, but it is better to try and mimic it being served from a webserver instead. Do this with the following command:

`docker run --name raf-resume -v ${PWD}:/usr/share/nginx/html:ro -p 8000:80 nginx:1.23-alpine`

_Note that the docker container does not seem to respond to Ctrl-C inputs. So you can run it with a `-d` flag (detached) and then just stop it with `docker container stop...`_
### Testing the blog

There is a dockerfile which creates a simple docker image with mkdocs installed. Once this is created (say with the name: mkdimage), the blog can be built in docker as follows. First change to the mkdocs folder (with the YML file in it). Then run:

`docker run --rm -v ${PWD}:/opt/project --entrypoint mkdocs mkdimage build`

This will output the resulting build into a directory called 'site', which you can then use to run the previously mentioned `nginx` docker image.

# Components

Template: https://html5up.net/
Content: Mine
Hosting: AWS S3

## Infrastructure

The website is designed to be hosted on S3, as designed and deployed by myself. This is in order to serve a) as a living exercise for others and b) as a demonstration of my AWS knowledge.

### CloudFormation

The infrastructure stack is expressed as Cloudformation in the `aws-cf` folder. The current stack name is: `raf-tech-website-stack`. To create it:

```
aws --profile <your cred profile> --region <target region> cloudformation create-stack --stack-name raf-tech-website-stack --template-body file://aws-cf/raf-tech-website.yaml --parameters file://filename.json
```

Note that you need to provide:
 * WebsiteName


### Services:

 * IAM Roles and Policies
 * S3
 * CodePipeline, CodeBuild
 * Lambda
 * Dynamo

# The Blog

# Dynamo:

## Updates

Set many attributes - best to do in a file with:

dynamodb put-item --table-name PageTrackTable --item file://totals.json

Increment an attribute:

dynamodb update-item --table-name PageTrackTable --key '{ "UserPages": {"S": "Richard"}, "SortKey": {"S": "PAGES"} }' --update-expression "ADD #page :incr" --expression-attribute-names '{ "#page": "blog/articles/2021-11-16-understanding-scrum/"}' --expression-attribute-values '{":incr": {"N": "1" }}' --return-values UPDATED_NEW

Remove an attribute:

dynamodb update-item --table-name PageTrackTable --key '{ "UserPages": {"S": "Richard"}, "SortKey": {"S": "PAGES"} }' --update-expression "REMOVE #attr" --expression-attribute-names '{ "#attr": "<attrname>"}'

## Queries

dynamodb query --table-name PageTrackTable --key-condition-expression "UserPages = :pk AND begins_with(SortKey, :sk)" --expression-attribute-values '{ ":pk": { "S": "Richard#INDEX" }, ":sk": { "S": "Richard#blog/articles" } }' --return-consumed-capacity TOTAL

dynamodb query --table-name PageTrackTable --key-condition-expression "UserPages = :pk" --expression-attribute-values '{ ":pk": { "S": "Richard#blog/articles/2022-10-On-Technical-Debt/" } }' --select COUNT --return-consumed-capacity TOTAL

## jq parsing

List all sort key results from dynamo response: `jq ".Items[].SortKey.S"`

curl -v <url>
