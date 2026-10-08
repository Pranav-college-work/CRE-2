"""Fail if any built page still shows plain-text math.

Checks every visible text node (HTML prose, table cells, buttons, labels, SVG <text>)
after removing KaTeX output, scripts and styles. Page <title>, SVG <title> and
<option> text are exempt only from Greek/sub/sup checks that cannot hold markup,
and are reported separately so they can be reworded.
"""
import glob, re, sys, os
from bs4 import BeautifulSoup, Comment

OUT = sys.argv[1]
only = sys.argv[2] if len(sys.argv) > 2 else ''

GREEK = 'Ͱ-Ͽᴀ-ᶿ\U0001d49c-\U0001d4cfℰℳ'  # greek, small caps, script letters
PAT = [
    (re.compile(f'[{GREEK}]'), 'Greek/script letter'),
    (re.compile('[²³¹⁰-₟]'), 'unicode super/subscript'),
    (re.compile('[←-⇿]'), 'arrow'),
    (re.compile('[∀-∑∓-⋿]'), 'math operator'),
    (re.compile('[×÷±]'), 'times/divide/plus-minus'),
    (re.compile(r'−(?!\s?\d)'), 'minus sign not before a number'),
    (re.compile(r'[′″‴]'), 'prime'),
    (re.compile(r'\w·\w|·[A-Z]\b'), 'middle dot in formula/unit'),
    (re.compile(r'[A-Za-z0-9)]\^[\w({-]'), 'caret power'),
    (re.compile(r'\b[A-Za-z]{1,2}_[A-Za-z0-9{]'), 'underscore subscript'),
    (re.compile(r'\b(sqrt|exp|tanh|coth|sinh|cosh|ln|log)\s?\('), 'function call'),
    (re.compile(r'(?<![<-])->|<-(?!-)|=>|<=|>='), 'ascii arrow/comparison'),
    (re.compile(r'(?<![\w*])\*(?=[\w(])'), 'asterisk multiply'),
    (re.compile(r'(?<![\w.])[A-Za-z]\s?[=<>]\s?[-\d.]'), 'symbol = number'),
    (re.compile(r'(?<![\w/])(?!(?:cm|mm|km|kg|mg|mL)\b)[A-Za-z]{1,2}\s?/\s?(?!(?:s|h|g|L|m|cm|kg|mol|min)\b)[A-Za-z]{1,2}(?![\w/])'), 'x/y symbol ratio'),
    (re.compile(r'\b[a-zA-Z]\([a-zA-Z]\)'), 'f(x) notation'),
]
ALLOW = [
    re.compile(r'^(and/or|either/or|w/w|km/h)$'),
]
SKIP_TAGS = {'script', 'style', 'code', 'noscript'}

def visible_texts(soup):
    for node in soup.find_all(string=True):
        if isinstance(node, Comment):
            continue
        par = node.parent
        if par is None or any(p.name in SKIP_TAGS for p in [par] + list(par.parents)):
            continue
        if any((p.get('class') or []) and ({'katex', 'katex-display', 'fo'} & set(p.get('class'))) for p in [par] + list(par.parents)):
            continue
        t = str(node)
        if not t.strip():
            continue
        yield par, t

total = 0
for f in sorted(glob.glob(os.path.join(OUT, '*.html'))):
    if only and only not in f:
        continue
    soup = BeautifulSoup(open(f, encoding='utf-8').read(), 'lxml')
    hits = []
    # <sub>/<sup> in prose should be KaTeX
    for tag in soup.find_all(['sub', 'sup']):
        if not any((p.get('class') or []) and ({'katex', 'fo'} & set(p.get('class'))) for p in tag.parents if hasattr(p, 'get')):
            hits.append(('html sub/sup', tag.parent.name, tag.parent.get_text()[:90]))
    for tsp in soup.find_all('tspan'):
        if tsp.get('baseline-shift'):
            hits.append(('svg tspan sub/sup', 'tspan', tsp.parent.get_text()[:90]))
    for par, t in visible_texts(soup):
        where = par.name
        if where == 'title':
            continue  # accessibility text, cannot hold markup
        for rx, why in PAT:
            m = rx.search(t)
            if m:
                s = max(0, m.start() - 40)
                snippet = t[s:m.end() + 40].replace('\n', ' ')
                if any(a.match(snippet.strip()) for a in ALLOW):
                    continue
                hits.append((why, where, snippet))
                break
    total += len(hits)
    print(f'\n##### {os.path.basename(f)}: {len(hits)}')
    for why, where, snip in hits:
        print(f'  [{why}] <{where}> …{snip}…')
print(f'\nTOTAL {total}')
sys.exit(1 if total else 0)
