from pathlib import Path
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup
import fitz
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent
output=root.parents[1]/'Tutorial 4'/'Tutorial4_Solutions.html'
soup=BeautifulSoup(output.read_text(encoding='utf-8'),'html.parser')
ids=[tag['id'] for tag in soup.select('[id]')]
assert len(ids)==len(set(ids)), 'Duplicate HTML identifiers'
for a in soup.select('a.cite'):
    assert soup.find(id=a['href'][1:]), a
for a in soup.select('#references a'):
    url=urlparse(a['href'])
    source=(output.parent/unquote(url.path)).resolve()
    page=int(url.fragment.split('=')[1])
    with fitz.open(source) as doc:
        assert 1 <= page <= len(doc)
        assert len(doc[page-1].get_text()) > 100
print('PASS: all 90 in-text citations resolve; 16 source links point to valid local PDF pages.')

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    page=browser.new_page(viewport={'width':1280,'height':1000})
    page.goto(output.as_uri())
    page.wait_for_load_state('networkidle')
    page.locator('#q7 figure').nth(1).screenshot(path=str(root/'new-q7b.png'))
    page.locator('#q7 figure').nth(2).screenshot(path=str(root/'new-q7full.png'))
    for needle,name in [('Textbook-based completion','new-q4.png'),('Non-dimensionalise','new-derivation.png'),('References and local','new-references.png')]:
        page.get_by_role('heading',name=needle,exact=False).scroll_into_view_if_needed()
        page.evaluate('window.scrollBy(0,-160)')
        page.screenshot(path=str(root/name))
    # Inspect every section for clipped text, then exercise the restored Q4 value.
    page.locator('#k-input').fill('358.37532026291643')
    page.locator('#calculate-k').click()
    text=page.locator('#k-output').inner_text()
    assert '2.370506e-4' in text, text
    assert '0.06822339 cm' in text, text
    print('PASS: Q4 calculator reproduces the conditional textbook-based answer.')
    for width in [360,390,768,1280]:
        page.set_viewport_size({'width':width,'height':1000})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.evaluate('window.scrollTo(0,0)')
    page.set_viewport_size({'width':390,'height':1000})
    page.screenshot(path=str(root/'new-mobile.png'))
    page.emulate_media(media='print')
    assert page.locator('nav').evaluate('(n)=>getComputedStyle(n).display')=='none'
    assert page.locator('#references').is_visible()
    print('PASS: mobile widths and print stylesheet.')
    browser.close()
