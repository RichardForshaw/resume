# mkd-blog/ - blog source (MKDocs)

Framework and content for `www.developdeploydeliver.com` website.

 * `docs/blog/articles/`, `docs/blog/books/` - markdown content
 * `cinder/` - custom MKDocs theme
 * `mkdocs.yml` - site config, nav, plugins (`mkdocs-blogging-plugin`, custom `mkdocs-social-buttons-plugin`)

Build/requirements notes:

 * Python deps for the build are pinned in the **root** `requirements.txt`, not inside this folder.
 * The production build (`buildspec.yml` at repo root) stamps the build date into `docs/index.md`, points `mkdocs.yml` at the production URL, then runs `mkdocs build -d ../blog`. Locally you can just run `mkdocs build`/`mkdocs serve` from this folder against a `pip install -r ../requirements.txt` environment (or the dev container).
 * The social-buttons plugin's share callback reports to the `sls-pagetracker/` `POST /pageshare` endpoint - if you change share button behaviour, check that integration.
 * `hooks/git_fallback.py` (registered via `hooks:` in `mkdocs.yml`) patches `mkdocs-blogging-plugin`'s date resolution: an explicit `date`/`time` front-matter field still always wins, and git log is still tried first, but when git isn't available (true for the build image, which has no git installed and no `.git` in its build context) it falls back to the file's filesystem mtime instead of the plugin's default of "now" - otherwise every undated post collapses to the build date. See the file's docstring for the mechanism (it monkeypatches `mkdocs_blogging_plugin.util.Util.get_git_commit_timestamp`).

## Conventions

 * `bin/insert-article-dates.sh` (repo root) backfills a markdown `date` field from an article's first git commit - use it rather than hand-writing dates on new articles pulled from another source.
 * `blog-examples/` (repo root) holds illustrative code referenced by specific posts - not part of the build, don't wire it in.
