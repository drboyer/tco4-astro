# Clean publication and staging

## Repository boundary

The owner created `git@github.com:drboyer/tco4-astro.git` and confirmed that no commits have been pushed. Publish only the clean release repository, initialized on `main` from the validated current files with one initial commit. The original development checkout retains its history and private export for reference; do not push or merge its historical branches into the clean repository.

The clean repository excludes the old `.git` directory, `.private/`, credentials/environment files, local agent/account directories, dependencies, and generated output. Its Ghost export contains only public posts and tag relationships. The original export and both drafts remain in `.private/ghost-export.original.json` in the **private development checkout**, not the clean publication repository.

After SSH authentication is available, from the clean repository:

```sh
git remote -v
git status --short
git push -u origin main
```

The remote should be `git@github.com:drboyer/tco4-astro.git`. Do not force-push if GitHub already contains commits; inspect the difference first. There is no deployment workflow yet, so pushing source does not deploy this project.

## Validation

```sh
npm ci
npm test
npm run check
npm run build
npm run verify:build
```

Edit posts directly in `src/content/blog/`; add new posts there with `title`, `description`, and `pubDate`. Optional fields include `tags`, `image`, and `draft`. Do not run `import:ghost` during CI or routine publishing: it is a migration command and deliberately refuses to overwrite local article changes.

## Staging build

Use a separate staging repository/hostname served from `/` to match the production route layout. The deploy workflow is a later step. Set these as build environment variables:

```sh
SITE_URL=https://staging.thecloudonline.net SITE_ENV=staging npm run build
SITE_URL=https://staging.thecloudonline.net SITE_ENV=staging npm run verify:build
```

`SITE_URL` defaults to `https://thecloudonline.net`; `SITE_ENV=staging` adds noindex metadata to regular HTML pages. Use the same values for building and verifying. Staging noindex is an indexing instruction, not access control.

## Compatibility and hosted acceptance

| Old URL | New behavior |
| --- | --- |
| `/blog/<slug>/` | Preserved article route |
| `/blog/content/images/...` | Preserved image paths |
| `/links.json` | Preserved public Links data |
| `/drought-relief` and `/drought-relief/` | Redirect to `/blog/building-an-interactive-drought-relief-map/` |
| `/blog/rss` and `/blog/rss/` | Compatibility redirect to `/rss.xml` |
| Unknown path | Branded `404.html`; confirm the host returns HTTP 404 |

The legacy `/blog/rss/` endpoint was checked on the existing site and returned 200. `/rss/`, `/feed/`, and `/rss.xml` returned 404 there; no compatibility aliases were invented for those old paths. The new canonical feed is `/rss.xml`.

Astro redirects are HTTP redirects in development. On static Pages hosting, they are generated HTML refresh pages with fallback links. Feed readers may not follow HTML refreshes. Seamless migration of old feed subscribers therefore needs a real HTTP 301/302 at a proxy/CDN, or an explicit subscriber migration before retiring Ghost. Do not mark this requirement complete merely because the redirect works in a browser.

Before production, inspect the hosted site's 404 status, slash handling, XML content type, query-free canonical links, indexing metadata, redirects, images, and RSS. Then follow `PRODUCTION_CHECKLIST.md` for domain setup, backups, cutover, and rollback.
