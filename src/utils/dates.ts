// Imported calendar dates are parsed at midnight UTC. Keep display timezone-independent.
export function formatPostDate(date: Date, month: 'short' | 'long' = 'long'): string {
  return date.toLocaleDateString('en-US', {
    month, day: 'numeric', year: 'numeric', timeZone: 'UTC',
  });
}
