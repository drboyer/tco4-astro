import assert from 'node:assert/strict';
import test from 'node:test';
import source from '../public/links.json' with { type: 'json' };
import { linkGroups, normalizeLinkUrl } from '../src/data/links.ts';
import { formatPostDate } from '../src/utils/dates.ts';

test('migration preserves all ordered categories, labels and optional fields', () => {
  assert.equal(linkGroups.length, 5);
  assert.equal(linkGroups.flatMap(group => group.links).length, 25);
  source.categories.forEach((category, i) => {
    assert.equal(linkGroups[i].title, category.title);
    category.links.forEach((link, j) => {
      const migrated = linkGroups[i].links[j];
      assert.equal(migrated.label, link.title);
      assert.equal(migrated.description, link.description);
      assert.equal(migrated.city, link.city);
      assert.ok(['http:', 'https:'].includes(new URL(migrated.url).protocol));
    });
  });
  assert.ok(linkGroups.flatMap(group => group.links).some(link => link.description === undefined));
  assert.equal(linkGroups.flatMap(group => group.links).filter(link => link.city).length, 5);
});

test('scheme-less destination becomes an external HTTPS URL', () => {
  assert.equal(normalizeLinkUrl('pivotalweather.com'), 'https://pivotalweather.com/');
  assert.equal(normalizeLinkUrl('http://example.org/path'), 'http://example.org/path');
  for (const bad of ['javascript:alert(1)', 'data:text/plain,bad', 'ftp://example.org', 'https://user:pass@example.org', 'not a domain']) {
    assert.throws(() => normalizeLinkUrl(bad));
  }
});

test('calendar dates remain stable in western and eastern build timezones', () => {
  const original = process.env.TZ;
  try {
    for (const tz of ['America/New_York', 'America/Los_Angeles', 'Pacific/Auckland', 'UTC']) {
      process.env.TZ = tz;
      assert.equal(formatPostDate(new Date('2010-12-18')), 'December 18, 2010');
      assert.equal(formatPostDate(new Date('2010-12-18'), 'short'), 'Dec 18, 2010');
    }
  } finally {
    if (original === undefined) delete process.env.TZ;
    else process.env.TZ = original;
  }
});
