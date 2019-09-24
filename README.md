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

# Run Local

## With Docker

Yes you can just load `index.html` into your browser, but it is better to try and mimix it being served from a webserver instead. Do this with the following command:

`docker run --name raf-resume -v ${PWD}:/usr/share/nginx/html:ro -p 8000:80 nginx:1.17-alpine`

# Setup website on S3

## CloudFormation

Cloudformation is in the `aws-cf` folder. To create it:

```
aws --profile <your cred profile> --region <target region> cloudformation create-stack --stack-name raf-tech-website-stack --template-body file://aws-cf/raf-tech-website.yaml
```
