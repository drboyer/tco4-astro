import { glob, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse } from 'yaml';

export async function readPublicPosts(root = fileURLToPath(new URL('../', import.meta.url))) {
  const base = path.join(root, 'src/content/blog');
  const posts = [];
  for await (const name of glob('**/*.md', { cwd: base })) {
    const text = await readFile(path.join(base, name), 'utf8');
    const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)([\s\S]*)$/);
    if (!match) throw new Error(`Missing frontmatter: ${name}`);
    const metadata = parse(match[1]);
    if (metadata.draft === true) continue;
    posts.push({
      ...metadata,
      slug: name.replace(/\.md$/, '').split(path.sep).join('/'),
      pubDate: new Date(metadata.pubDate).toISOString().slice(0, 10),
      body: match[2],
    });
  }
  return posts.sort((a, b) => a.slug.localeCompare(b.slug, 'en'));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  console.log(JSON.stringify(await readPublicPosts(process.argv[2])));
}
