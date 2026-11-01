#!/usr/bin/env python3
"""Recover historical same-origin images from the existing site; never replace files."""
import concurrent.futures
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, unquote
from urllib.request import Request, urlopen
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://thecloudonline.net'


def is_image(data):
    return (data.startswith(b'\x89PNG\r\n\x1a\n') or data.startswith(b'\xff\xd8\xff')
            or data.startswith((b'GIF87a', b'GIF89a'))
            or (data.startswith(b'RIFF') and data[8:12] == b'WEBP'))


def media_paths():
    paths = set((ROOT / 'scripts/media-paths.txt').read_text().splitlines())
    for post in (ROOT / 'src/content/blog').glob('*.md'):
        text = post.read_text()
        candidates = re.findall(r'!\[[^\]]*\]\(([^)]+)\)|<img[^>]*src=[\"\x27]([^\"\x27]+)|^image: "([^\"]+)"', text, re.M)
        for candidate in candidates:
            url = urlsplit(next(part for part in candidate if part))
            if not url.netloc or url.netloc == 'thecloudonline.net':
                paths.add(url.path)
    return sorted(paths)


def restore(path):
    target = ROOT / 'public' / unquote(path).lstrip('/')
    if not target.resolve().is_relative_to((ROOT / 'public').resolve()):
        raise ValueError(f'Unsafe media path: {path}')
    if target.exists():
        if not is_image(target.read_bytes()):
            raise ValueError(f'Existing media is not a supported image: {path}')
        return {'path': path, 'status': 'present'}
    request = Request(ORIGIN + path, headers={'User-Agent': 'TheCloudOnline-archive-migration/1.0'})
    try:
        with urlopen(request, timeout=20) as response:
            data = response.read(25 * 1024 * 1024 + 1)
            if not response.headers.get('Content-Type', '').startswith('image/') or not is_image(data):
                return {'path': path, 'status': 'failed', 'error': 'Response is not a supported image'}
            if len(data) > 25 * 1024 * 1024:
                return {'path': path, 'status': 'failed', 'error': 'Image exceeds 25 MiB recovery limit'}
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return {'path': path, 'status': 'restored', 'bytes': len(data)}
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        return {'path': path, 'status': 'failed', 'error': str(error)}


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(restore, media_paths()))
    (ROOT / 'docs/media-restoration.json').write_text(json.dumps({'source': ORIGIN, 'files': results}, indent=2) + '\n')
    failures = [result for result in results if result['status'] == 'failed']
    print(f'{len(results) - len(failures)}/{len(results)} image paths available locally')
    for failure in failures:
        print(f"MISSING {failure['path']}: {failure['error']}")
    raise SystemExit(bool(failures))
