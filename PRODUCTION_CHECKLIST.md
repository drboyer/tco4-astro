# Production launch checklist

Release-preparation code is complete. The owner has reviewed the site's overall appearance. Detailed archive checks, hosted staging, DNS cutover, and VPS retirement remain separate launch steps.

## Completed preparation

- [x] Standardize on Node 24/npm 11 with a lockfile, runtime declaration, and generated-file ignores.
- [x] Make importer tests independent of edited articles; retain overwrite protection and draft exclusion.
- [x] Treat current Markdown as the publishing source of truth; keep Ghost import as an explicit migration command only.
- [x] Read ordinary YAML frontmatter in article inventories and release verification, including newly written posts.
- [x] Preserve all 21 imported article routes and original calendar dates; retain both unpublished drafts privately.
- [x] Recover 49 historical image paths; optimize the owner's portrait and hero assets; validate all built images.
- [x] Restore Twitter/X widgets with blockquote fallbacks; repair legacy image figures, preserve gist code, and provide Storify/YouTube fallback links.
- [x] Migrate all 25 Links entries in five categories and preserve `/links.json`.
- [x] Add header-image cards, chronological article navigation, a personal portrait, and the selected homepage hero.
- [x] Configure the owner's social profiles and consistent `thecloudonline.net` branding, including the header logo and RSS.
- [x] Add query-free canonical URLs, a branded noindex 404 page, and staging origin/noindex controls.
- [x] Redirect `/drought-relief` to the article about the retired project.
- [x] Identify `/blog/rss/` as the legacy feed and provide a compatibility redirect to `/rss.xml`.
- [x] Confirm Nginx migration scope is the main site and blog; no other application needs moving.
- [x] Prepare clean-publication instructions and retain the original development checkout privately. No historical commits have been pushed to GitHub.

## Hosted staging and final review

- [x] Push the clean publication repository to GitHub; `main` starts at the sanitized initial commit.
- [x] Add and locally validate the manual staging workflow for `staging.thecloudonline.net`, with a Pages hostname guard.
- [x] Configure GitHub Pages, add the staging CNAME in DigitalOcean, and run the first hosted staging deployment. See `docs/PUBLISHING.md`.
- [x] Verify direct article loads, canonical origins, RSS, media, navigation, social profiles, mobile layout, and real HTTP 404 behavior on the host.
- [x] Owner accepted the legacy RSS tradeoff on 2026-11-01: `/blog/rss/` remains an HTML refresh redirect that some feed readers may not follow. `/rss.xml` is the canonical working feed. No proxy/CDN redirect infrastructure is required for this launch.
- [x] Complete article-specific visual checks for tables, Twitter/X failure fallbacks, YouTube playback, and image alternative text. See `docs/ARTICLE_REVIEW.md`.
- [x] Approve the unrecovered Storify memorial fallback or supply replacement content.
- [x] Decide which failed/obsolete external destinations to update; see `docs/LINK_HEALTH.md`.
- [x] Copy the original export and both drafts from the private development checkout into durable private backup storage.

## Production cutover

- [ ] Verify domain ownership; configure `thecloudonline.net` in Pages settings before changing web DNS.
- [ ] Enable HTTPS and verify apex/`www`, redirects, the new RSS feed, and final production URLs.
- [ ] Back up Ghost's database, Nginx, images, and other VPS services; verify restoration.
- [ ] Keep the VPS available for rollback for at least seven days and until propagation/checks pass; then approve retirement.
- [ ] Optionally enable push-triggered deployments after launch.

The staging workflow is manual-only. No production DNS change or VPS retirement has been performed. A `public/CNAME` file does not configure a custom domain for Actions-based Pages publishing; use Pages settings.
