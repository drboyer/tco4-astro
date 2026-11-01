import data from '../../public/links.json' with { type: 'json' };

interface LinkSource {
  title: string;
  url: string;
  description?: string;
  city?: string;
}

export function normalizeLinkUrl(value: string): string {
  const url = new URL(/^[a-z][a-z\d+.-]*:/i.test(value) ? value : `https://${value}`);
  if (!['http:', 'https:'].includes(url.protocol) || !url.hostname || url.username || url.password) {
    throw new Error(`Invalid public link URL: ${value}`);
  }
  return url.href;
}

// Build from the committed snapshot; never fetch the old site at build or runtime.
export const linkGroups = data.categories.map(category => ({
  title: category.title,
  links: category.links.map((link: LinkSource) => ({
    label: link.title,
    url: normalizeLinkUrl(link.url),
    description: link.description,
    city: link.city,
  })),
}));
