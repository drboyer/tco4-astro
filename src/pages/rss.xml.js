import { createFeed } from '../utils/rss';

export function GET(context) {
  return createFeed(context.site);
}
