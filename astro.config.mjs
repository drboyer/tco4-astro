import { defineConfig } from 'astro/config';

const site = process.env.SITE_URL || 'https://thecloudonline.net';

export default defineConfig({
  site,
  trailingSlash: 'always',
  output: 'static',
  redirects: {
    // An absolute URL prevents trailingSlash from turning rss.xml into rss.xml/.
    '/blog/rss': { status: 302, destination: new URL('/rss.xml', site).href },
    '/drought-relief': {
      status: 302,
      destination: '/blog/building-an-interactive-drought-relief-map/',
    },
  },
});
