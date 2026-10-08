/* CRE II Mid-Sem study pack — shared helpers: theme, charts, TOC, self-test, math utils */
(function () {
  const root = document.documentElement;
  const css = (n) => getComputedStyle(root).getPropertyValue(n).trim();

  /* ---------- theme toggle (system / light / dark) ---------- */
  try { const t = localStorage.getItem('sp-theme'); if (t) root.setAttribute('data-theme', t); } catch (e) {}

  const redraws = [];
  const redrawAll = () => redraws.forEach((f) => { try { f(); } catch (e) { console.error(e); } });
  if (window.matchMedia) matchMedia('(prefers-color-scheme: dark)').addEventListener('change', redrawAll);

  function isPlain(o) { return o && typeof o === 'object' && !Array.isArray(o); }
  function merge(a, b) {
    const out = Array.isArray(a) ? a.slice() : Object.assign({}, a);
    for (const k in b) out[k] = isPlain(a[k]) && isPlain(b[k]) ? merge(a[k], b[k]) : b[k];
    return out;
  }

  /* ---------- KaTeX at run time (axis titles, readouts, dynamic labels) ---------- */
  const texHTML = (t) => {
    try { return window.katex ? katex.renderToString(String(t), { throwOnError: false, strict: 'ignore' }) : String(t); }
    catch (e) { return String(t); }
  };
  function axisLabels(el) {
    if (el._xl) return;
    const wrap = document.createElement('div');
    wrap.className = 'pwrap';
    el.parentNode.insertBefore(wrap, el);
    const yl = document.createElement('div'); yl.className = 'ax-y';
    const xl = document.createElement('div'); xl.className = 'ax-x';
    wrap.append(yl, el, xl);
    el._xl = xl; el._yl = yl;
  }

  const SP = {
    css,
    tex: texHTML,
    series(i) { return css('--s' + i); },
    layout(extra) {
      const axis = {
        gridcolor: css('--grid'), zerolinecolor: css('--rule-strong'), linecolor: css('--rule-strong'),
        ticks: 'outside', tickcolor: css('--rule-strong'), ticklen: 4, showline: true, automargin: true,
        title: { font: { size: 13, color: css('--ink-2') }, standoff: 8 },
      };
      const base = {
        paper_bgcolor: css('--surface'), plot_bgcolor: css('--surface'),
        font: { family: css('--font-ui') || 'Segoe UI, system-ui, sans-serif', color: css('--ink-2'), size: 12.5 },
        margin: { l: 58, r: 16, t: 34, b: 40 },
        xaxis: axis, yaxis: axis,
        legend: { orientation: 'h', x: 0, y: 1.02, yanchor: 'bottom', bgcolor: 'rgba(0,0,0,0)', font: { size: 12, color: css('--ink-2') } },
        hoverlabel: { bgcolor: css('--surface'), bordercolor: css('--rule-strong'), font: { color: css('--ink'), family: css('--font-ui') } },
        hovermode: 'closest',
        shapes: [], annotations: [],
      };
      return merge(base, extra || {});
    },
    /* build() -> {data, layout}; re-runs on theme change and whenever the returned fn is called.
       layout.xaxis.tex / layout.yaxis.tex are TeX strings rendered with KaTeX outside the plot. */
    plot(id, build) {
      const el = typeof id === 'string' ? document.getElementById(id) : id;
      const draw = () => {
        const r = build();
        const lay = Object.assign({}, r.layout || {});
        ['xaxis', 'yaxis'].forEach((ax) => {
          if (lay[ax] && 'tex' in lay[ax]) {
            axisLabels(el);
            const node = ax === 'xaxis' ? el._xl : el._yl;
            node.innerHTML = lay[ax].tex ? texHTML(lay[ax].tex) : '';
            lay[ax] = Object.assign({}, lay[ax], { title: { text: '' } });
            delete lay[ax].tex;
          }
        });
        Plotly.react(el, r.data, SP.layout(lay), {
          responsive: true, displaylogo: false,
          modeBarButtonsToRemove: ['lasso2d', 'select2d', 'autoScale2d', 'toggleSpikelines'],
        });
      };
      redraws.push(draw);
      draw();
      return draw;
    },
    bind(ids, fn) {
      ids.forEach((id) => {
        const el = document.getElementById(id);
        if (el) { el.addEventListener('input', fn); el.addEventListener('change', fn); }
      });
      fn();
    },
    val(id) { return parseFloat(document.getElementById(id).value); },
    out(id, html) { const el = document.getElementById(id); if (el) el.innerHTML = html; },
    /* write TeX into an element */
    outTex(id, t) { const el = document.getElementById(id); if (el) el.innerHTML = texHTML(t); },
    /* segmented button group: returns getter */
    seg(id, onChange) {
      const g = document.getElementById(id);
      const btns = [...g.querySelectorAll('button')];
      btns.forEach((b) => b.addEventListener('click', () => {
        btns.forEach((x) => x.classList.toggle('on', x === b));
        onChange && onChange(b.dataset.v);
      }));
      return () => (btns.find((b) => b.classList.contains('on')) || btns[0]).dataset.v;
    },
    /* number as TeX string */
    fmtTex(x, sig = 3) {
      if (!isFinite(x)) return '\\text{—}';
      if (x === 0) return '0';
      const ax = Math.abs(x), sgn = x < 0 ? '-' : '';
      if (ax >= 1e-3 && ax < 1e5) {
        const d = Math.max(0, sig - 1 - Math.floor(Math.log10(ax)));
        return sgn + ax.toFixed(Math.min(d, 6));
      }
      const e = Math.floor(Math.log10(ax));
      const m = ax / Math.pow(10, e);
      return sgn + m.toFixed(sig - 1) + '\\times10^{' + e + '}';
    },
    /* number rendered with KaTeX (proper minus sign and ×10ⁿ) */
    fmt(x, sig = 3) { return texHTML(SP.fmtTex(x, sig)); },
    linspace(a, b, n) { const r = []; for (let i = 0; i < n; i++) r.push(a + (b - a) * i / (n - 1)); return r; },
    logspace(a, b, n) { return SP.linspace(Math.log10(a), Math.log10(b), n).map((v) => Math.pow(10, v)); },
    linfit(x, y) {
      const n = x.length; let sx = 0, sy = 0, sxx = 0, sxy = 0, syy = 0;
      for (let i = 0; i < n; i++) { sx += x[i]; sy += y[i]; sxx += x[i] * x[i]; sxy += x[i] * y[i]; syy += y[i] * y[i]; }
      const slope = (n * sxy - sx * sy) / (n * sxx - sx * sx);
      const icpt = (sy - slope * sx) / n;
      const r = (n * sxy - sx * sy) / Math.sqrt((n * sxx - sx * sx) * (n * syy - sy * sy));
      return { slope, icpt, r2: r * r };
    },
  };

  /* ---------- effectiveness-factor maths (Levenspiel M_T, L = V/A_ext) ---------- */
  function besselI(nu, x) {
    let term = Math.pow(x / 2, nu), sum = 0;
    for (let k = 0; k < 400; k++) {
      if (k > 0) term *= (x / 2) * (x / 2) / (k * (k + nu));
      sum += term;
      if (term < sum * 1e-15) break;
    }
    return sum;
  }
  SP.eta = {
    slab(M) { return M < 1e-6 ? 1 : Math.tanh(M) / M; },
    cyl(M) {
      if (M < 1e-6) return 1;
      const x = 2 * M;
      if (x > 60) return (1 - 1 / (2 * x) - 1 / (8 * x * x)) / M; // asymptotic I1/I0
      return besselI(1, x) / besselI(0, x) / M;
    },
    sph(M) {
      if (M < 1e-4) return 1 - 9 * M * M / 15;
      return (1 / M) * (1 / Math.tanh(3 * M) - 1 / (3 * M));
    },
    /* invert Wagner modulus Mw = M_T² η(M_T) for M_T */
    fromWagner(Mw, shape) {
      const f = (M) => M * M * SP.eta[shape](M) - Mw;
      let lo = 1e-6, hi = 1e4;
      for (let i = 0; i < 200; i++) { const mid = Math.sqrt(lo * hi); if (f(mid) > 0) hi = mid; else lo = mid; }
      return Math.sqrt(lo * hi);
    },
  };

  window.SP = SP;

  document.addEventListener('DOMContentLoaded', () => {
    /* theme button */
    const tb = document.getElementById('themeBtn');
    if (tb) {
      const label = () => { const t = root.getAttribute('data-theme'); tb.textContent = t === 'dark' ? 'Theme: dark' : t === 'light' ? 'Theme: light' : 'Theme: system'; };
      label();
      tb.addEventListener('click', () => {
        const t = root.getAttribute('data-theme');
        const next = !t ? 'light' : t === 'light' ? 'dark' : null;
        if (next) root.setAttribute('data-theme', next); else root.removeAttribute('data-theme');
        try { next ? localStorage.setItem('sp-theme', next) : localStorage.removeItem('sp-theme'); } catch (e) {}
        label(); redrawAll();
      });
    }
    /* reveal-all answers */
    const rb = document.getElementById('revealBtn');
    if (rb) rb.addEventListener('click', () => {
      const all = [...document.querySelectorAll('details.qa')];
      const open = all.some((d) => !d.open);
      all.forEach((d) => (d.open = open));
      rb.textContent = open ? 'Hide answers' : 'Show all answers';
    });
    /* TOC highlight */
    const links = [...document.querySelectorAll('.toc a[href^="#"]')];
    if (links.length && 'IntersectionObserver' in window) {
      const map = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));
      const io = new IntersectionObserver((ents) => {
        ents.forEach((en) => {
          if (en.isIntersecting) { links.forEach((l) => l.classList.remove('on')); const a = map.get(en.target.id); if (a) a.classList.add('on'); }
        });
      }, { rootMargin: '-15% 0px -75% 0px' });
      map.forEach((_, id) => { const el = document.getElementById(id); if (el) io.observe(el); });
    }
    /* checklists */
    const checks = [...document.querySelectorAll('.check input[data-key]')];
    const bar = document.querySelector('.progress > i');
    const upd = () => {
      checks.forEach((c) => c.closest('.check').classList.toggle('done', c.checked));
      if (bar && checks.length) bar.style.width = (100 * checks.filter((c) => c.checked).length / checks.length) + '%';
    };
    checks.forEach((c) => {
      try { c.checked = localStorage.getItem('sp-chk-' + c.dataset.key) === '1'; } catch (e) {}
      c.addEventListener('change', () => { try { localStorage.setItem('sp-chk-' + c.dataset.key, c.checked ? '1' : '0'); } catch (e) {} upd(); });
    });
    upd();
  });
})();
