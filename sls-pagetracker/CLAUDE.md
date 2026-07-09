# sls-pagetracker/ - page view tracking API

Serverless Framework service `sls-page-tracker`. Deploys independently via `sls deploy` from this folder. Backs onto a single DynamoDB table `PageTrackTable` (PK `UserPages`, SK `SortKey`), defined in this folder's `serverless.yml`.

 * `handler.py`:
   - `handle_s3_view_log` - S3-triggered on new access-log objects, parses log lines and writes/increments per-page visit counters and history in DynamoDB
   - `handle_page_share` - `POST /pageshare`, records a share event (validates the page exists first)
   - `handle_blog_page_count_totals` - `GET /pagetotals`, aggregate view-count totals per page (optional path-prefix filter or `FULLSCAN`)
   - `handle_blog_page_visit_history` - `GET /pagehistory`, per-page daily visit history, optionally bounded by `from_date`/`to_date` or `from_time`/`to_time`
 * `dynamo_helpers.py` - builds the Dynamo key/query param structures used by `handler.py`
 * `helpers.py` - date parsing / array utilities
 * `test_*.py` - pytest unit tests; run with `pytest` from this folder

`serverless.yml` reads the access-log bucket and other outputs from `raf-tech-website-stack` via `${cf:...}` - see `aws-cf/CLAUDE.md` if those outputs change.

## Conventions

 * Query/update param builders belong in `dynamo_helpers.py`, not inline in `handler.py` - keep the key-schema logic in one place since `UserPages`/`SortKey` formatting is easy to get subtly wrong (see the `PAGES`/`VISITS`/`:SHARE#` sort-key prefix conventions in `README.md`'s Dynamo cheat-sheet).
 * This is a separate service from `sls/` (health check + contact form) - don't merge them.
