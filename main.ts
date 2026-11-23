// make.fun bounty: news-image-20261123
// Entry point for "Sum up 23 November's world news in one image".
// Writes entry.png to the output directory (MAKEFUN_OUTPUT_DIR overrides /output).
// Deterministic: produces identical bytes on every run.
// Node 22, standard library only.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const outPath = join(outDir, 'entry.png');

const image = readFileSync(join(here, 'entry.png'));
mkdirSync(outDir, { recursive: true });
writeFileSync(outPath, image);
