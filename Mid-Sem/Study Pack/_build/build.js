// Pre-renders LaTeX in the study-pack sources with KaTeX.
//   Display math: $$ ... $$     Inline math: \( ... \)
//   Math inside SVG diagrams:  <m x=".." y=".." [w=".."] [h=".."] [a="start|middle|end"] [c="css classes"]>TeX</m>
//     -> <foreignObject> holding KaTeX HTML, centred vertically on y and anchored on x.
// <script> and <style> blocks are left untouched.
const fs = require('fs');
const path = require('path');
const katex = require('katex');

const SRC = process.env.SP_SRC || path.join(__dirname, 'src');
const OUT = process.argv[2];
if (!OUT) { console.error('usage: node build.js <outDir> [only]'); process.exit(1); }

const macros = { '\\dd': '\\mathrm{d}', '\\rr': '-r' };

let failures = 0;
function tex(src, display, file) {
  try {
    return katex.renderToString(src, { displayMode: display, throwOnError: true, strict: 'ignore', macros });
  } catch (e) {
    failures++;
    console.error(`\n[${file}] KaTeX error: ${e.message}\n  in: ${src.slice(0, 160)}`);
    return `<span style="color:red">${src}</span>`;
  }
}

const attr = (s, name, dflt) => {
  const m = s.match(new RegExp('\\b' + name + '="([^"]*)"'));
  return m ? m[1] : dflt;
};

function svgMath(html, file) {
  return html.replace(/<m\b([^>]*)>([\s\S]*?)<\/m>/g, (_, a, t) => {
    const x = parseFloat(attr(a, 'x', '0')), y = parseFloat(attr(a, 'y', '0'));
    const w = parseFloat(attr(a, 'w', '220')), h = parseFloat(attr(a, 'h', '34'));
    const anchor = attr(a, 'a', 'middle');
    // prefix label classes so they never collide with page classes such as .tw (table wrapper)
    const cls = attr(a, 'c', '').split(/\s+/).filter(Boolean).map((k) => 'fo-' + k).join(' ');
    const x0 = anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x;
    const body = tex(t.trim(), false, file);
    return `<foreignObject x="${x0}" y="${y - h / 2}" width="${w}" height="${h}" class="fo-box">` +
      `<div xmlns="http://www.w3.org/1999/xhtml" class="fo fo-${anchor} ${cls}">${body}</div></foreignObject>`;
  });
}

function render(html, file) {
  const parts = html.split(/(<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>)/);
  return parts.map((p, i) => {
    if (i % 2) return p;
    p = svgMath(p, file);
    p = p.replace(/\$\$([\s\S]+?)\$\$/g, (_, t) => tex(t.trim(), true, file));
    p = p.replace(/\\\(([\s\S]+?)\\\)/g, (_, t) => tex(t.trim(), false, file));
    return p;
  }).join('');
}

const only = process.argv[3];
for (const f of fs.readdirSync(SRC)) {
  if (!f.endsWith('.html')) continue;
  if (only && !f.includes(only)) continue;
  const html = fs.readFileSync(path.join(SRC, f), 'utf8');
  const out = render(html, f);
  const stripped = out.replace(/<script[\s\S]*?<\/script>/g, '');
  if (/\$\$|\\\(|\\\)|<m\b/.test(stripped)) { console.error(`[${f}] unbalanced math delimiters or unconverted <m> remain`); failures++; }
  fs.writeFileSync(path.join(OUT, f), out);
  console.log('built', f, (out.length / 1024).toFixed(0) + ' KB');
}
if (failures) { console.error(`\n${failures} problem(s)`); process.exit(1); }
