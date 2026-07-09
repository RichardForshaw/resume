# Repo Map

Personal repo with three responsibilities: hosting config for two static sites, the blog content for one of them, and a serverless page-tracking service. See `README.md` for build/deploy commands and `Description.md` for the AWS build narrative.

Each major folder below has its own `CLAUDE.md` with the detail for that aspect - only read it when you're actually working in that folder or on that deployment. Nothing here should be treated as applying repo-wide beyond this file.

## Working from the repo root

If a request is made while working from this root folder (rather than already inside `aws-cf/`, `mkd-blog/`, `sls/`, or `sls-pagetracker/`), and it isn't obvious from the request that the user means to manage the repo as a whole (e.g. "update the README", "what's the overall structure", cross-cutting changes to `buildspec.yml`), stop and ask which of the three functions they want to work on:

 * AWS/CloudFormation hosting (`aws-cf/`)
 * The blog (`mkd-blog/`)
 * The page-tracking / contact-form serverless services (`sls/`, `sls-pagetracker/`)

Then direct the work to happen from that folder rather than operating on it from root, so the relevant scoped `CLAUDE.md` is the one actually in effect. Don't ask this if the user has already named the folder, the file, or the aspect (e.g. "fix the pagetracker date filter", "add an S3 bucket policy") - only ask when the target is genuinely ambiguous.

 * `aws-cf/` - CloudFormation infra for both sites -> see `aws-cf/CLAUDE.md`
 * `mkd-blog/` - blog content and MKDocs build -> see `mkd-blog/CLAUDE.md`
 * `sls/` - site health check + contact form (Serverless Framework) -> see `sls/CLAUDE.md`
 * `sls-pagetracker/` - page-tracking API (Serverless Framework) -> see `sls-pagetracker/CLAUDE.md`

## Two static websites (the one cross-cutting fact)

One CodePipeline/CodeBuild pipeline (`buildspec.yml`, root) builds and deploys both sites in a single run, producing two artifacts:

 * `www.forshaw.tech` - resume/landing page: `index.html`, `assets/` (HTML5 UP template, Sass/JS)
 * `www.developdeploydeliver.com` - blog, built from `mkd-blog/`

If you're touching `buildspec.yml` itself, both the `aws-cf/` and `mkd-blog/` notes may be relevant.

## Other folders (no scoped file needed)

 * `bin/insert-article-dates.sh` - backfills a markdown `date` field from git history
 * `blog-examples/` - standalone example code written to accompany specific blog posts. Illustrative only, not deployed - don't confuse with `sls-pagetracker/`.
 * `.devcontainer/`, `Dockerfile` - dev environment (Python + Node + Serverless Framework + MKDocs + Claude Code CLI)
