# aws-cf/ - infrastructure as code

CloudFormation for both static sites: S3 hosting buckets, Route53, ACM certs, CodePipeline/CodeBuild, IAM roles, SES (contact form), SNS.

 * `raf-tech-website.yaml` - main stack, name `raf-tech-website-stack`: buckets, DNS, pipeline, cert/CNAME params
 * `raf-tech-website-build.yaml` - CodeBuild service role/config
 * `raf-tech-groups-roles.yaml` - IAM groups/roles for account access

Create the main stack with:

```
aws --profile <cred profile> --region <region> cloudformation create-stack \
  --stack-name raf-tech-website-stack \
  --template-body file://raf-tech-website.yaml \
  --parameters file://<params>.json
```

Requires at minimum a `WebsiteName` parameter.

## Conventions

 * Infra changes go through these templates and `update-stack`, not manual console edits - the console drifts and the next `update-stack` will fight it.
 * `sls/` and `sls-pagetracker/` (Serverless Framework services elsewhere in the repo) read outputs from `raf-tech-website-stack` via `${cf:...}` variables in their `serverless.yml` - if you rename/remove a stack output, check both of those.
 * See `Description.md` (repo root) for the history/gotchas behind specific design choices here (routing, certs, double-deploy setup) before changing them.
