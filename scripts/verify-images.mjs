import assert from 'node:assert/strict';
import { readdir } from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

let count = 0;
async function verify(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) await verify(file);
    else if (/\.(png|jpe?g|gif|webp)$/i.test(file)) {
      const metadata = await sharp(file).metadata();
      assert.ok(metadata.width > 0 && metadata.height > 0, `Invalid dimensions: ${file}`);
      // Decode every frame, including restored animated GIFs, without changing assets.
      await sharp(file, { animated: true }).raw().toBuffer();
      count++;
    }
  }
}
await verify('dist');
console.log(`Decoded ${count} built images successfully`);
