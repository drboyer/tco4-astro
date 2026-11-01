#!/usr/bin/env python3
"""Import published Ghost content without deleting posts or overwriting local edits."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def description(markdown):
    text = re.sub(r'<script\b[^>]*>.*?</script>', '', markdown, flags=re.S | re.I)
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = html.unescape(re.sub(r'<[^>]+>', '', text))
    return re.sub(r'\s+', ' ', re.sub(r'[#*_`>|]', '', text)).strip()[:180]


def render_post(post, tags, repairs=()):
    markdown = post.get('markdown') or ''
    for repair in repairs:
        if markdown.count(repair['old']) != 1:
            raise ValueError(f"Repair no longer matches exactly once: {post['slug']}: {repair['reason']}")
        markdown = markdown.replace(repair['old'], repair['new'], 1)
    front = {
        'title': post['title'], 'description': description(markdown) or post['title'],
        'pubDate': post['published_at'][:10], 'tags': tags, 'archived': True,
    }
    if post.get('image'):
        front['image'] = post['image'].replace('https://thecloudonline.net/', '/')
    fm = ''.join(f'{key}: {json.dumps(value, ensure_ascii=False)}\n' for key, value in front.items())
    return '---\n' + fm + '---\n\n' + markdown + '\n'


def import_posts(root=ROOT, force=False):
    data = json.loads((root / 'scripts/ghost-export.json').read_text())['db'][0]['data']
    repairs = json.loads((root / 'scripts/archive-repairs.json').read_text())
    tags = {tag['id']: tag['name'] for tag in data['tags']}
    post_tags = {}
    for rel in data['posts_tags']:
        post_tags.setdefault(rel['post_id'], []).append(tags[rel['tag_id']])
    out = root / 'src/content/blog'
    state_path = root / 'scripts/import-state.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    outputs = {}
    media = set()
    complex_posts = []
    for post in data['posts']:
        if post['status'] != 'published' or post.get('page'):
            continue
        slug = post['slug']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            raise ValueError(f'Unsafe post slug: {slug}')
        if slug in outputs:
            raise ValueError(f'Duplicate post slug: {slug}')
        text = render_post(post, post_tags.get(post['id'], []), repairs.get(slug, []))
        target = out / f'{slug}.md'
        if target.exists() and not force:
            current = target.read_text()
            expected = state.get(slug)
            if current != text and (expected is None or digest(current) != expected):
                raise ValueError(f'Local changes in {target}; preserve them in archive-repairs.json before importing, or explicitly use --force.')
        outputs[slug] = text
        for value in (post.get('markdown') or '', post.get('html') or '', post.get('image') or ''):
            media.update(path.split('?', 1)[0].rstrip('.,;') for path in re.findall(r'(?:/blog)?/content/images/[^\s)\"\'<>]+', value))
        markers = [marker for marker in ('<iframe', '<script', '<table', 'storify.com', 'twitter-tweet') if marker in (post.get('markdown') or '').lower()]
        if markers:
            complex_posts.append(f"{slug}: {', '.join(markers)}")
    unknown = set(repairs) - set(outputs)
    if unknown:
        raise ValueError(f'Repairs reference missing posts: {sorted(unknown)}')
    # All conflicts and repairs are checked before any content is written.
    out.mkdir(parents=True, exist_ok=True)
    for slug, text in outputs.items():
        (out / f'{slug}.md').write_text(text)
    state_path.write_text(json.dumps({slug: digest(text) for slug, text in sorted(outputs.items())}, indent=2) + '\n')
    (root / 'scripts/media-paths.txt').write_text('\n'.join(sorted(media)) + '\n')
    (root / 'scripts/complex-posts.txt').write_text('\n'.join(complex_posts) + '\n')
    print(f'Imported {len(outputs)} published posts; preserved unrelated files; {len(media)} historical media paths')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true', help='Overwrite local edits to imported posts only; never deletes other posts')
    args = parser.parse_args()
    import_posts(force=args.force)
