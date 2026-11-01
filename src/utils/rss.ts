import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { siteName, siteDescription } from '../config/site';

export async function createFeed(site: URL) {
  const posts = (await getCollection('blog', ({ data }) => !data.draft))
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
  return rss({
    title: siteName,
    description: siteDescription,
    site,
    items: posts.map(post => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/blog/${post.id}/`,
    })),
  });
}
