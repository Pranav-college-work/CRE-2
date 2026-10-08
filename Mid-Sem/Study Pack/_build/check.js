// Headless check of the built pack: console errors, KaTeX errors, overflow, and element screenshots.
// usage: node check.js <builtDir> <shotsDir> [theme=light|dark] [pageFilter]
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const DIR = path.resolve(process.argv[2]);
const OUT = path.resolve(process.argv[3]);
const theme = process.argv[4] || 'light';
const only = process.argv[5] || '';
fs.mkdirSync(OUT, { recursive: true });

const pages = ['index', 'm1-heterogeneous-catalysis', 'm2-rate-laws', 'm3-pore-diffusion', 'tutorials', 'formula-sheet-and-practice'];

(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new' });
  const manifest = [];
  for (const p of pages) {
    if (only && !p.includes(only)) continue;
    const pg = await b.newPage();
    const errs = [];
    pg.on('pageerror', (e) => errs.push('pageerror: ' + e.message));
    pg.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text()); });
    await pg.setViewport({ width: 1280, height: 900, deviceScaleFactor: 1 });
    await pg.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: theme }]);
    const url = 'file:///' + path.join(DIR, p + '.html').replace(/\\/g, '/');
    await pg.goto(url, { waitUntil: 'load' });
    await new Promise((r) => setTimeout(r, 1800));
    const info = await pg.evaluate(() => ({
      katexErr: [...document.querySelectorAll('span[style*="color:red"], .katex-error')].map((e) => e.textContent.slice(0, 80)),
      fo: document.querySelectorAll('foreignObject').length,
      foEmpty: [...document.querySelectorAll('foreignObject .fo')].filter((d) => !d.querySelector('.katex')).length,
      axisLabels: document.querySelectorAll('.ax-x .katex, .ax-y .katex').length,
      plots: document.querySelectorAll('.js-plotly-plot').length,
      emptyOutputs: [...document.querySelectorAll('output')].filter((o) => !o.textContent.trim()).map((o) => o.id),
    }));
    // screenshot figures and viz blocks
    const els = await pg.$$('main figure, main .viz');
    let i = 0;
    for (const e of els) {
      const cap = await e.evaluate((n) => {
        const c = n.querySelector('figcaption, .vh');
        const t = n.querySelector('svg title');
        return ((c && c.textContent) || (t && t.textContent) || '').trim().slice(0, 70);
      });
      const file = `${p}_${theme}_${String(i).padStart(2, '0')}.png`;
      await e.scrollIntoView();
      await e.screenshot({ path: path.join(OUT, file) });
      manifest.push({ file, cap });
      i++;
    }
    // mobile overflow
    await pg.setViewport({ width: 400, height: 800 });
    await new Promise((r) => setTimeout(r, 700));
    const mob = await pg.evaluate(() => {
      const out = [];
      for (const el of document.querySelectorAll('main *')) {
        const rc = el.getBoundingClientRect();
        if (rc.right <= 402 || rc.width === 0) continue;
        let clipped = false;
        for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
          const s = getComputedStyle(a);
          if (s.overflowX !== 'visible' && a.getBoundingClientRect().right <= 402) { clipped = true; break; }
        }
        if (!clipped) { out.push(el.tagName + '.' + (el.getAttribute('class') || '')); if (out.length > 4) break; }
      }
      return { scrollWidth: document.documentElement.scrollWidth, offenders: out };
    });
    console.log(JSON.stringify({ page: p, shots: i, errors: errs, ...info, mobile: mob }));
    await pg.close();
  }
  fs.writeFileSync(path.join(OUT, `manifest_${theme}.json`), JSON.stringify(manifest, null, 1));
  await b.close();
})();
