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

`dynamodb update-item --table-name PageTrackTable --key '{ "UserPages": {"S": "Richard"}, "SortKey": {"S": "PAGES"} }' --update-expression "ADD #page :incr" --expression-attribute-names '{ "#page": "blog/articles/2021-11-16-understanding-scrum/"}' --expression-attribute-values '{":incr": {"N": "1" }}' --return-values UPDATED_NEW`

Add to a list and create new list if not present:

`dynamodb update-item --table-name PageTrackTable --update-expression "SET #key = list_append(if_not_exists(#key, :empty), :val)" --expression-attribute-names '{"#key": "blog/books/2022-12-book-review-2022/"}' --expression-attribute-values '{ ":val": { "L": [...] }, ":empty": { "L": [] } }' --key '{"UserPages": {"S": "Richard"}, "SortKey": {"S": "VISITS"}}'`

Remove an attribute:

`dynamodb update-item --table-name PageTrackTable --key '{ "UserPages": {"S": "Richard"}, "SortKey": {"S": "PAGES"} }' --update-expression "REMOVE #attr" --expression-attribute-names '{ "#attr": "<attrname>"}'`

Retrieve an attribute:

`dynamodb get-item --table-name PageTrackTable --key '{ "UserPages": { "S": "Richard"}, "SortKey": {"S": "VISITS"}}' --projection-expression "#page" --expression-attribute-names '{ "#page": "blog/articles/2023-02-aws-cli-advanced-filtering/" }'`

## Queries

Get all records partially matching a key

`dynamodb query --table-name PageTrackTable --key-condition-expression "UserPages = :pk AND begins_with(SortKey, :sk)" --expression-attribute-values '{ ":pk": { "S": "Richard#INDEX" }, ":sk": { "S": "Richard#blog/articles" } }' --return-consumed-capacity TOTAL`

Get count of records matching a key

`dynamodb query --table-name PageTrackTable --key-condition-expression "UserPages = :pk" --expression-attribute-values '{ ":pk": { "S": "Richard#blog/articles/2022-10-On-Technical-Debt/" } }' --select COUNT --return-consumed-capacity TOTAL`

Get a single item match

`dynamodb get-item --table-name PageTrackTable --key '{ "UserPages": { "S": "Richard#blog/articles/2022-10-On-Technical-Debt/" }, "SortKey": {"S": "VISITS#..."} }'`

## Athena

Get all the stored query names from athena

```
aws athena list-named-queries --query "NamedQueryIds | join(' ', @)" | tr -d '"' | xargs aws athena batch-get-named-query --query "NamedQueries[].[Name,Description || 'None'] | [*].join(':', @)" --named-query-ids | sed 's/:/:\t/'
```

Note the `sed` command is used to insert tabs for readability. I'm not sure how to do this in JMES.

## jq parsing

 * List all sort key results from dynamo response: `jq '.Items[].SortKey.S'`
 * Convert DynamoDB list into regular array: `jq '[.Item.L[] | .N]'`
 * Convert DynamoDB map of lists into arrays: `jq '.Item | with_entries(.value |= [.L[]?.N])`
 * Replace a list with its length: `jq '.Item.List.L |= length'`
 * Replace all lists with lengths in an array: `jq '.Items |= [.[] | .List.L |= length]`

## Using JQ ETL scripts

In order to use the JQ scripts, use the command of the form:

`jq -r -f <script-file>`

`-r` will use 'raw' format which is compatible with piping the command to aws.

The form for launching a query from athena is:

```
aws athena list-named-queries --query "NamedQueryIds | join(' ', @)" | tr -d '"' \
| xargs aws athena batch-get-named-query --query "NamedQueries[?Name=='<name_of_query>'].QueryString | [0]" --named-query-ids \
| sed 's/\\n/ /g' \
| xargs aws athena start-query-execution --work-group primary --query-execution-context Catalog=AwsDataCatalog,Database=ddd_s3_access_logs_db --query-string
```

This can probably be put into a script. The `sed` command replaces the newlines with spaces.

Retrieving and processing results:

```
aws athena get-query-results --query-execution-id 123-ABC | jq -r -f <script-file> \
| xargs -n 1 -I data aws dynamodb batch-write-item --request-items 'data'
```

The `-n 1` is only needed if there is a lot of data grouped into lines, for example the daily page visits which groups each page into a new batch request line. Queries which don't do this can be passed in as a single request (that is, up to 25 requests in the batch request)

