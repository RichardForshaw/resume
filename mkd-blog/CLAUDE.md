# mkd-blog/ - blog source (MKDocs)

Framework and content for `www.developdeploydeliver.com` website.

 * `docs/blog/articles/`, `docs/blog/books/` - markdown content
 * `cinder/` - custom MKDocs theme
 * `mkdocs.yml` - site config, nav, plugins (`mkdocs-blogging-plugin`, custom `mkdocs-social-buttons-plugin`)

Build/requirements notes:

 * Python deps for the build are pinned in the **root** `requirements.txt`, not inside this folder.
 * The production build (`buildspec.yml` at repo root) stamps the build date into `docs/index.md`, points `mkdocs.yml` at the production URL, then runs `mkdocs build -d ../blog`. Locally you can just run `mkdocs build`/`mkdocs serve` from this folder against a `pip install -r ../requirements.txt` environment (or the dev container).
 * The social-buttons plugin's share callback reports to the `sls-pagetracker/` `POST /pageshare` endpoint - if you change share button behaviour, check that integration.

## Conventions

 * `bin/insert-article-dates.sh` (repo root) backfills a markdown `date` field from an article's first git commit - use it rather than hand-writing dates on new articles pulled from another source.
 * `blog-examples/` (repo root) holds illustrative code referenced by specific posts - not part of the build, don't wire it in.
