#!/usr/bin/env python3
"""Observe outbound destinations without changing their historical URLs or copy."""
import concurrent.futures
from datetime import datetime, timezone
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def check(url):
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; TheCloudOnline-Migration/1.0)'})
        with urlopen(request, timeout=8) as response:
            response.read(1)
            return {'status': response.status, 'final_url': response.url}
    except HTTPError as error:
        return {'status': error.code, 'final_url': error.url}
    except (URLError, TimeoutError, OSError, ValueError) as error:
        return {'status': None, 'error': str(error)}


def review(url):
    result = {'url': url, **check(url)}
    if url.startswith('http://'):
        candidate = 'https://' + url[len('http://'):]
        result['https_candidate'] = {'url': candidate, **check(candidate)}
    return result


if __name__ == '__main__':
    data = json.loads((ROOT / 'public/links.json').read_text())
    links = [link for category in data['categories'] for link in category['links']]
    urls = {link['url'] if '://' in link['url'] else 'https://' + link['url'] for link in links}
    if not (ROOT / 'dist/links/index.html').exists():
        raise SystemExit('Run npm run build before checking rendered outbound URLs.')

    class Destinations(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag not in ('a', 'img', 'iframe'):
                return
            attrs = dict(attrs)
            value = attrs.get('href') if tag == 'a' else attrs.get('src')
            if value and value.startswith(('http://', 'https://')):
                urls.add(value)

    for page in (ROOT / 'dist').rglob('*.html'):
        Destinations().feed(page.read_text())
    urls = {urldefrag(url)[0] for url in urls if urlsplit(url).hostname != 'thecloudonline.net'}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        results = sorted(pool.map(review, sorted(urls)), key=lambda row: row['url'])
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'note': 'Observations only. Failures may reflect bot blocking or temporary outages. No destinations were silently replaced.', 'results': results}
    (ROOT / 'docs/external-links-review.json').write_text(json.dumps(report, indent=2) + '\n')
    by_url = {row['url']: row for row in results}
    lines = ['# Links collection review', '', 'Source: https://thecloudonline.net/links.json. Snapshot committed in `public/links.json`.', '',
             'All 25 links and five categories retain their original order and wording. The page normalizes the scheme-less `pivotalweather.com` to HTTPS. Optional descriptions and webcam cities are rendered when present.', '',
             'Network failures may reflect anti-bot rules, DNS, or temporary outages. Proposed replacements and copy edits need owner approval; no links have been dropped.', '',
             '| Category | Link | Observed response | HTTPS candidate |', '| --- | --- | --- | --- |']
    for category in data['categories']:
        for link in category['links']:
            url = link['url'] if '://' in link['url'] else 'https://' + link['url']
            row = by_url[url]
            candidate = row.get('https_candidate', {})
            result = str(row.get('status') or 'Network error')
            if row.get('final_url') != url and row.get('final_url'):
                result += f" → {row['final_url']}"
            lines.append(f"| {category['title']} | [{link['title']}]({url}) | {result} | {candidate.get('status') or ('Network error' if candidate else '—')} |")
    lines += ['', 'Editorial candidates: confirm outdated destinations before replacing them; consider the existing “prod alum!” and “stomr reports” wording. Approve the new page introduction before launch.', '',
              'See `external-links-review.json` for article references, external images, redirects, errors, and HTTPS alternatives.']
    (ROOT / 'docs/LINKS_REVIEW.md').write_text('\n'.join(lines) + '\n')
    print(f'Reviewed {len(results)} external URLs; {sum(bool(row.get("status") and row["status"] < 400) for row in results)} responded below HTTP 400')
