# thecloudonline.net — production candidate

Static Astro 7 site with 21 imported Ghost articles, preserved `/blog/<slug>/` routes, RSS, and a Links collection migrated from the existing site. Release-preparation code is complete; hosted staging, launch sign-off, and production cutover remain outstanding.

## Run locally

Use Node 24 (`nvm use` reads `.nvmrc`) and npm 11 or later:

```sh
npm ci
npm run dev
```

Open the URL printed by Astro, normally `http://localhost:4321`. Review `/links/`, `/blog/`, and the articles listed in [the article review inventory](docs/ARTICLE_REVIEW.md).

## Validate

```sh
npm test
npm run check
npm run build
npm run verify:build
```

The checks cover safe imports, draft exclusion, current YAML/Markdown content, timezone-independent dates, article routes, RSS, Links, canonical URLs, the 404 page, compatibility redirects, and decoding of every built image. Browser/visual review is intentionally left to the owner.

## Content and migration tools

- `npm run import:ghost`: migration-only regeneration from the sanitized export and versioned repairs. Preserves unrelated posts and refuses to overwrite edited imports. Edit current Markdown directly for routine publishing; never run this command automatically in CI. See [migration notes](MIGRATION_NOTES.md).
- `npm run audit:archive`: regenerate the offline article/media review inventory.
- `python3 scripts/restore_media.py`: optional, networked recovery from the existing site; skips existing images. All 49 historical same-origin image paths have already been recovered.
- `python3 scripts/review_external_links.py`: optional, networked destination checks; writes review reports without changing content.

The Links page builds from the committed `public/links.json` snapshot, also served at `/links.json`. It never fetches the old server during a build or page visit. Preserve the `categories` array with category `title`/`links` and link `title`/`url`, plus optional `description`/`city`, when editing it.

## Remaining launch work

A manual GitHub Pages staging workflow is included at `.github/workflows/staging.yml`. Next steps are enabling Pages, configuring the staging hostname and DigitalOcean CNAME, and running the hosted checks. Pushing commits alone does not deploy. The owner has reviewed the site's appearance and supplied biography, profiles, portrait, and hero imagery.

Canonical URLs use the production domain by default. Set `SITE_URL` and `SITE_ENV=staging` for an isolated staging build. The branded 404 page is noindex. `/drought-relief` redirects to the retired project's article, and `/blog/rss/` redirects to `/rss.xml`. Static HTML redirects need additional hosted validation, particularly for feed readers.

See [clean publication and staging instructions](docs/PUBLISHING.md). The clean repository contains no old Git history; retain the original development checkout privately.

See [the production checklist](PRODUCTION_CHECKLIST.md), [article review](docs/ARTICLE_REVIEW.md), and [Links review](docs/LINKS_REVIEW.md). This repository has not been deployed by this implementation.
