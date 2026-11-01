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

- [ ] Push only the clean publication repository, then create a manual GitHub Pages workflow and isolated staging site.
- [ ] Verify direct article loads, canonical origins, RSS, media, navigation, social profiles, mobile layout, and real HTTP 404 behavior on the host.
- [ ] Resolve legacy-feed HTTP compatibility: static Pages produces HTML refresh redirects, which feed readers may not follow. For seamless subscriber migration, configure a real HTTP 301/302 from `/blog/rss/` to `/rss.xml` at a proxy/CDN, or migrate existing subscribers explicitly before retiring Ghost.
- [ ] Complete article-specific visual checks for tables, Twitter/X failure fallbacks, YouTube playback, and image alternative text. See `docs/ARTICLE_REVIEW.md`.
- [ ] Approve the unrecovered Storify memorial fallback or supply replacement content.
- [ ] Decide which failed/obsolete external destinations to update; see `docs/LINK_HEALTH.md`.
- [ ] Copy the original export and both drafts from the private development checkout into durable private backup storage.

## Production cutover

- [ ] Verify domain ownership; configure `thecloudonline.net` in Pages settings before changing web DNS.
- [ ] Enable HTTPS and verify apex/`www`, redirects, feed migration, and final production URLs.
- [ ] Back up Ghost's database, Nginx, images, and other VPS services; verify restoration.
- [ ] Keep the VPS available for rollback for at least seven days and until propagation/checks pass; then approve retirement.
- [ ] Optionally enable push-triggered deployments after launch.

No Pages workflow, production DNS change, or VPS retirement is part of this release-preparation change set. A `public/CNAME` file does not configure a custom domain for Actions-based Pages publishing; use Pages settings.
