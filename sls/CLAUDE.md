# sls/ - site health check + contact form

Serverless Framework service `wwwstatuscheck`. Deploys independently via `sls deploy` from this folder.

 * `handlers.py`:
   - `run_health` - scheduled every 30 min, checks both sites return `200 OK` and are above an expected minimum size, alerts via SNS on failure
   - `contact_form_email` - `POST /contact_form` behind API Gateway, used by the resume site's contact form; sends via SES, optionally notifies Pushbullet if `PB_TOKEN` is set
 * `serverless.yml` - reads stack outputs (SNS topic ARN, SES target/source addresses) from `raf-tech-website-stack` via `${cf:...}` - see `aws-cf/CLAUDE.md` if those outputs change.

## Conventions

 * Keep the two functions in this service (`statuschecker`, `contactformemail`) - it's separate from `sls-pagetracker/`, which is a different service with its own DynamoDB table and API.
