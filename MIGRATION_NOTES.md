# Ghost archive migration notes

## Sources and private backup

The repository's `scripts/ghost-export.json` now contains only the 21 published articles and their tag relationships. Original slugs, date portions, Markdown, HTML, and feature image references are preserved there. Account metadata, credentials, operational settings, and unpublished drafts were removed from the working export.

The original full export, including the two drafts, is preserved at `.private/ghost-export.original.json` with owner-only permissions in the private development checkout. It is excluded from the clean publication repository. Copy it from the development checkout to durable private backup storage. This is an export backup, not a full Ghost database/VPS backup.

**Repository history:** the original development checkout retains the original export in earlier commits and must remain private. The clean publication repository starts with one sanitized initial commit and no parent history. Publish only that repository; see `docs/PUBLISHING.md`. No development history was rewritten.

## Safe regeneration and editorial repairs

For migration-only regeneration, run `npm run import:ghost`. Current Markdown is authoritative for normal editing and publishing; do not run the importer in CI or during routine builds. The importer updates only published export slugs; it never deletes other Markdown files. `scripts/import-state.json` records imported content hashes. If an imported file has local edits, the importer fails before writing articles. Capture intended repairs in `scripts/archive-repairs.json`, then regenerate. `--force` explicitly permits overwriting local edits to imported posts and should only be used after preserving them.

Repairs use exact, guarded old/new fragments and remain reproducible:

- Tweet text, attribution, and source links remain in blockquotes as readable fallbacks. Each article containing tweets loads the HTTPS Twitter/X widget script once, asynchronously, to restore rich embeds when available. Duplicate legacy per-tweet script tags are removed during import.
- The drought-relief code gist is preserved as a local code block at revision `3c795459a2ec69fc895a6bb67d7d52ebd241907a`, with its source link.
- The obsolete Storify embed is replaced by an archive note, original URL, and archive-search link. **The memorial contents have not been recovered.** Owner approval or replacement content remains necessary.
- The two figures in the Twisted News article use HTML images/figure captions instead of Markdown inside a malformed layout table, so both images render. Original captions are preserved.
- Three YouTube iframes retain their source URLs, gain titles/lazy loading, and have independent watch links. Playback needs owner review.
- Descriptions retain Markdown link labels. Same-origin absolute feature image paths become local paths; original image references remain in the export.

Publication dates retain the date portion of `published_at`. Display formatting explicitly uses UTC so local build timezones cannot shift the calendar day. Historical article titles, slugs, and prose are otherwise retained, including the substantive `samplepost` and `untitled` articles.

## Media recovery

All 48 paths in `scripts/media-paths.txt`, plus `/images/drought-relief.png`, were recovered from `https://thecloudonline.net` into `public/` at their existing paths. See `docs/media-restoration.json`. Case and GIF animation are preserved; the build verifier decodes all frames. The export also references two external Wikimedia images, retained as external dependencies.

`npm run audit:archive` checks references in current Markdown, raw image HTML, and feature images. The historical manifest also includes paths from original Ghost HTML that may no longer be referenced in rendered articles.

## Links migration and review

`public/links.json` is a committed snapshot of `https://thecloudonline.net/links.json`, retaining all 25 links across five categories in source order. The page uses this local file and preserves optional descriptions and webcam cities. The scheme-less `pivotalweather.com` becomes an external HTTPS URL in rendered output; the public source JSON remains unchanged.

See `docs/LINKS_REVIEW.md` for observed responses and editorial candidates, and `docs/external-links-review.json` for all 142 checked external destinations, including article references and images. These observations are not guarantees of availability: failures can reflect bot blocking or transient outages. Destinations and original wording have not been silently replaced.

## Verification and owner review

`npm test`, `npm run check`, `npm run build`, and `npm run verify:build` pass on Node 24. The generated site has 21 article routes and 21 RSS entries; all local article media resolve and all built images decode, including the added portrait and hero assets.

Review every article using `docs/ARTICLE_REVIEW.md`, especially the nine historical complex posts listed in `scripts/complex-posts.txt`. Visual layout, empty image alternative text, embedded-video playback, and editorial decisions remain pending owner review. No browser tooling was installed or used.
