# Clean publication and staging

## Repository boundary

The owner created `git@github.com:drboyer/tco4-astro.git` and has now pushed the clean release repository. Its `main` branch starts with the sanitized initial commit `8e7fcd0`; no original development-history commits were included. The original development checkout retains its history and private export for reference; do not push or merge its historical branches into the clean repository.

The clean repository excludes the old `.git` directory, `.private/`, credentials/environment files, local agent/account directories, dependencies, and generated output. Its Ghost export contains only public posts and tag relationships. The original export and both drafts remain in `.private/ghost-export.original.json` in the **private development checkout**, not the clean publication repository.

SSH authentication is configured and the initial push is complete. For future updates, from the clean repository:

```sh
git remote -v
git status --short
git push -u origin main
```

The remote should be `git@github.com:drboyer/tco4-astro.git`. Do not force-push if GitHub already contains commits; inspect the difference first. The staging workflow is manual-only; pushing source does not deploy this project.

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

For this first launch, use the existing repository's Pages site at `staging.thecloudonline.net`, served from `/`. Production remains on the VPS. After staging approval, a separate change will switch the Pages domain and build configuration to production; this workflow cannot deploy to a production hostname.

`.github/workflows/staging.yml` runs only through **Actions → Deploy staging to GitHub Pages → Run workflow**, using `main`. It installs locked dependencies, runs tests and Astro checks, builds, verifies all generated pages/images, and uploads only `dist`. It checks the Pages hostname before publishing. Actions are pinned to verified release commit IDs. No personal token or DigitalOcean secret is needed by this workflow.

To reproduce the staging build locally, set these environment variables:

```sh
SITE_URL=https://staging.thecloudonline.net SITE_ENV=staging npm run build
SITE_URL=https://staging.thecloudonline.net SITE_ENV=staging npm run verify:build
```

`SITE_URL` defaults to `https://thecloudonline.net`; `SITE_ENV=staging` adds noindex metadata to regular HTML pages. Use the same values for building and verifying. Staging noindex is an indexing instruction, not access control.

## One-time GitHub Pages and DigitalOcean setup

1. Open [the repository's Pages settings](https://github.com/drboyer/tco4-astro/settings/pages). Under **Build and deployment**, select **GitHub Actions** as the source. Do not install GitHub's generated starter workflow; this repository already contains one.
2. Set **Custom domain** to `staging.thecloudonline.net` and save it **before adding DNS**. GitHub may initially report a DNS check failure; the next step supplies the record. If domain ownership verification is requested, use the exact TXT name/value GitHub provides.
3. In DigitalOcean, open **Networking → Domains → thecloudonline.net** and add this record:

   | Field | Value |
   | --- | --- |
   | Type | `CNAME` |
   | Hostname | `staging` |
   | Target / alias | `drboyer.github.io.` |
   | TTL | `300` seconds |

   The target excludes the repository name. If a conflicting `staging` A/AAAA/CNAME record already exists, replace only that staging record. Leave the apex (`@`), `www`, mail records, and existing production VPS records unchanged.
4. After DNS propagates and GitHub's DNS check passes, run **Deploy staging to GitHub Pages** from `main`. Watch both the build and deploy jobs. The workflow intentionally fails if the Pages hostname is not the approved staging domain, avoiding broken `/tco4-astro/` project-path links or an accidental production deployment.
5. Enable **Enforce HTTPS** in Pages settings when available. Certificate provisioning can take up to 24 hours. Open `https://staging.thecloudonline.net/` and complete the hosted acceptance checks below. Do not switch production DNS yet.

Useful DNS check:

```sh
nslookup -type=CNAME staging.thecloudonline.net
```

Expected alias target: `drboyer.github.io`. `public/CNAME` is not used with Actions-based Pages publishing; the domain is configured in Pages settings.

References: [GitHub custom-domain setup](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site), [DigitalOcean DNS records](https://docs.digitalocean.com/products/networking/dns/how-to/manage-records/).

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

Astro redirects are HTTP redirects in development. On static Pages hosting, they are generated HTML refresh pages with fallback links. Feed readers may not follow HTML refreshes. On 2026-11-01 the owner explicitly accepted this limitation, given the long period without new posts. The launch will keep the browser-compatible HTML redirect and publish the new working feed at `/rss.xml`; preserving existing reader subscriptions is not a launch blocker. No proxy/CDN redirect is required for this release. A real HTTP redirect can be added later if desired.

Before production, inspect the hosted site's 404 status, slash handling, XML content type, query-free canonical links, indexing metadata, redirects, images, and RSS. Then follow `PRODUCTION_CHECKLIST.md` for domain setup, backups, cutover, and rollback.
