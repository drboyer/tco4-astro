import assert from 'node:assert/strict';
import test from 'node:test';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { readPublicPosts } from '../scripts/read-content.mjs';

test('release inventory reads current YAML, includes new writing and excludes drafts', async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'tco-inventory-'));
  try {
    const directory = path.join(root, 'src/content/blog');
    await mkdir(directory, { recursive: true });
    await writeFile(path.join(directory, 'new-post.md'), '---\ntitle: New writing\npubDate: 2026-11-01\ntags: [development, weather]\nimage: /images/new.webp\n---\nEdited article body.\n');
    await writeFile(path.join(directory, 'draft.md'), '---\ntitle: Unpublished\npubDate: 2026-11-02\ndraft: true\n---\nPrivate draft.\n');
    const posts = await readPublicPosts(root);
    assert.equal(posts.length, 1);
    assert.equal(posts[0].slug, 'new-post');
    assert.equal(posts[0].pubDate, '2026-11-01');
    assert.deepEqual(posts[0].tags, ['development', 'weather']);
    assert.equal(posts[0].image, '/images/new.webp');
    assert.match(posts[0].body, /Edited article body/);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
