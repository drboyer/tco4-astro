#!/usr/bin/env python3
"""Check generated routes, dates, media, Links snapshot, RSS and excluded source files."""
import calendar
import os
import subprocess
from datetime import date
from html.parser import HTMLParser
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
SITE = os.environ.get('SITE_URL', 'https://thecloudonline.net').rstrip('/')
STAGING = os.environ.get('SITE_ENV') == 'staging'


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.images, self.scripts, self.anchors, self.headings, self.times, self.text = [], [], [], [], [], []
        self.canonical = None
        self.robots = None
        self.refresh = None
        self.tweet_count = 0
        self.heading = None
        self.anchor = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical = attrs['href']
        if tag == 'meta' and attrs.get('name') == 'robots': self.robots = attrs['content']
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh': self.refresh = attrs['content']
        if tag == 'img': self.images.append(attrs['src'])
        if tag == 'script' and attrs.get('src'): self.scripts.append(attrs['src'])
        if tag == 'blockquote' and 'twitter-tweet' in attrs.get('class', '').split():
            self.tweet_count += 1
        if tag == 'script' and attrs.get('src') == 'https://platform.twitter.com/widgets.js':
            assert 'async' in attrs, 'Twitter widget script must load asynchronously'
        if tag == 'a': self.anchor = [attrs.get('href'), '']
        if tag == 'h2': self.heading = ''
        if tag == 'time': self.times.append(attrs.get('datetime'))
        if tag == 'iframe':
            assert attrs.get('title'), 'Iframe lacks an accessible title'
            assert attrs.get('loading') == 'lazy', 'Iframe lacks lazy loading'

    def handle_data(self, text):
        self.text.append(text)
        if self.heading is not None: self.heading += text
        if self.anchor is not None: self.anchor[1] += text

    def handle_endtag(self, tag):
        if tag == 'h2' and self.heading is not None:
            self.headings.append(self.heading)
            self.heading = None
        if tag == 'a' and self.anchor is not None:
            self.anchors.append(self.anchor)
            self.anchor = None


posts = json.loads(subprocess.check_output(['node', str(ROOT / 'scripts/read-content.mjs')], text=True, cwd=ROOT))
expected_paths = {DIST / 'blog' / post['slug'] / 'index.html' for post in posts}
actual_paths = set((DIST / 'blog').rglob('index.html')) - {DIST / 'blog/index.html', DIST / 'blog/rss/index.html'}
assert actual_paths == expected_paths, 'Missing or unexpected article route'
for post in posts:
    path = DIST / 'blog' / post['slug'] / 'index.html'
    doc = Document(path.read_text())
    day = date.fromisoformat(post['pubDate'])
    expected_date = f'{calendar.month_name[day.month]} {day.day}, {day.year}'
    assert expected_date in ''.join(doc.text), f'Displayed date mismatch: {post["slug"]}'
    assert doc.times[0].startswith(day.isoformat()), f'Machine-readable date mismatch: {post["slug"]}'
    # File existence alone misses Markdown images swallowed by raw HTML blocks.
    for source_image in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', post['body']):
        assert source_image in doc.images, f'Article image did not render: {post["slug"]}: {source_image}'
    expected_tweets = (post['body']).count('class="twitter-tweet"')
    assert doc.tweet_count == expected_tweets, f'Tweet blockquote fallback missing: {path}'
    expected_scripts = ['https://platform.twitter.com/widgets.js'] if expected_tweets else []
    assert doc.scripts == expected_scripts, f'Missing, duplicate or unexpected widget script: {path}'
for path in DIST.rglob('*.html'):
    for image in Document(path.read_text()).images:
        url = urlsplit(urljoin(SITE + '/' + str(path.relative_to(DIST)), image))
        if url.hostname == urlsplit(SITE).hostname:
            assert (DIST / unquote(url.path).lstrip('/')).is_file(), f'Missing built image: {image}'
source = json.loads((ROOT / 'public/links.json').read_text())
assert json.loads((DIST / 'links.json').read_text()) == source, 'Public JSON snapshot changed'
links = Document((DIST / 'links/index.html').read_text())
assert links.headings == [category['title'] for category in source['categories']], 'Category order changed'
for category in source['categories']:
    for link in category['links']:
        url = link['url'] if '://' in link['url'] else 'https://' + link['url']
        if urlsplit(url).path == '': url += '/'
        assert any(href == url and label.startswith(link['title']) for href, label in links.anchors), f'Missing link: {link["title"]}'
        for key in ['description', 'city']:
            if link.get(key): assert link[key] in ''.join(links.text), f'Missing {key}: {link["title"]}'
assert 'placeholders' not in ''.join(links.text).lower()
items = ET.parse(DIST / 'rss.xml').findall('./channel/item')
assert len(items) == len(posts), 'RSS count mismatch'
assert ET.parse(DIST / 'rss.xml').findtext('./channel/title') == 'thecloudonline.net', 'RSS branding mismatch'
assert {item.findtext('link') for item in items} == {f'{SITE}/blog/{post["slug"]}/' for post in posts}, 'RSS URL mismatch'
# Ordinary HTML pages use query-free canonical URLs; the 404 is never indexed.
for path in DIST.rglob('*.html'):
    doc = Document(path.read_text())
    if path.name == '404.html':
        assert doc.robots and 'noindex' in doc.robots, '404 must be noindex'
        assert doc.canonical is None, '404 must not canonicalize unknown URLs'
        assert any(href == '/blog/' for href, _ in doc.anchors), '404 lacks a recovery link'
    elif doc.refresh is None:
        relative = path.relative_to(DIST).as_posix()
        pathname = '/' + relative.removesuffix('index.html')
        assert doc.canonical == SITE + pathname, f'Canonical mismatch: {path}'
        assert ('noindex' in (doc.robots or '')) == STAGING, f'Incorrect indexing mode: {path}'
        assert 'thecloudline.net' not in ''.join(doc.text), 'Header logo typo remains'
for old, target in {
    'drought-relief': '/blog/building-an-interactive-drought-relief-map/',
    'blog/rss': SITE + '/rss.xml',
}.items():
    doc = Document((DIST / old / 'index.html').read_text())
    assert doc.refresh and doc.refresh.split('url=', 1)[-1] == target, f'Redirect mismatch: {old}'
    assert any(href == target for href, _ in doc.anchors), f'Redirect lacks fallback: {old}'
for path in DIST.rglob('*'):
    assert path.name not in {'.private', 'ghost-export.json', 'ghost-export.original.json', 'archive-repairs.json'}, f'Source leaked into build: {path}'
print(f'Verified {len(posts)} published posts, media, Links, RSS, canonicals, 404, redirects and source exclusions (staging={STAGING})')
