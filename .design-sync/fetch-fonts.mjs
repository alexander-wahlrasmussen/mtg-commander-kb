// Scratch: fetch latin-subset woff2 from Google Fonts, base64-inline them as
// @font-face rules, write ui/src/theme/fonts.css. Self-hosts the fonts so the
// bundled CSS ships real fonts (no remote @import, clears the font warning).
import { writeFileSync } from 'node:fs';

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36';
const CSS_URL = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Spectral:wght@400;500;600;700&display=swap';

const cssRes = await fetch(CSS_URL, { headers: { 'User-Agent': UA } });
const css = await cssRes.text();

// Each @font-face is preceded by a /* subset */ comment. Keep only latin.
const re = /\/\*\s*([\w-]+)\s*\*\/\s*(@font-face\s*\{[^}]*\})/g;
let m, kept = 0, out = [];
out.push('/* Self-hosted Spectral + IBM Plex Mono (latin subset, base64). Generated from Google Fonts.');
out.push('   Ships real @font-face in the bundled CSS — no remote @import dependency. */');
while ((m = re.exec(css)) !== null) {
  const subset = m[1];
  let block = m[2];
  if (subset !== 'latin') continue;
  const urlMatch = block.match(/url\((https:\/\/[^)]+\.woff2)\)/);
  if (!urlMatch) continue;
  const woff2 = await (await fetch(urlMatch[1], { headers: { 'User-Agent': UA } })).arrayBuffer();
  const b64 = Buffer.from(woff2).toString('base64');
  const fam = block.match(/font-family:\s*'([^']+)'/)?.[1];
  const wght = block.match(/font-weight:\s*(\d+)/)?.[1];
  block = block.replace(/url\(https:\/\/[^)]+\.woff2\)/, `url(data:font/woff2;base64,${b64})`);
  // compact the block onto one line
  out.push(block.replace(/\s*\n\s*/g, ' ').trim());
  console.error(`  ${fam} ${wght} latin — ${(woff2.byteLength/1024).toFixed(1)}KB woff2`);
  kept++;
}
writeFileSync('ui/src/theme/fonts.css', out.join('\n') + '\n');
console.error(`wrote ui/src/theme/fonts.css — ${kept} @font-face rules`);
