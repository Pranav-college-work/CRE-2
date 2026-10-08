from pathlib import Path
from playwright.sync_api import sync_playwright, expect

root=Path(__file__).resolve().parent
source=(root/'tutorial4_code.py').read_text(encoding='utf-8')
output=root.parents[1]/'Tutorial 4'/'Tutorial4_Solutions.html'
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000},permissions=['clipboard-read','clipboard-write'])
    page=context.new_page()
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(output.as_uri())
    assert page.locator('#python-code').text_content()==source
    page.locator('#copy-code').click()
    expect(page.locator('#copy-status')).to_have_text('Copied.')
    # Windows clipboard may normalise line endings; Python code is identical.
    assert page.evaluate('navigator.clipboard.readText()').replace('\r\n','\n')==source
    code_panel=page.locator('details').filter(has=page.locator('#python-code'))
    code_panel.locator('summary').click()
    page.locator('#python-code').scroll_into_view_if_needed()
    page.evaluate('document.querySelector("#python-code").scrollIntoView({block:"start"});window.scrollBy(0,-100)')
    page.screenshot(path=str(root/'annotated-code.png'))
    for width in [375,768,1440]:
        page.set_viewport_size({'width':width,'height':1000})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
    page.get_by_role('heading',name='Trace one calculation from inputs to results').scroll_into_view_if_needed()
    page.screenshot(path=str(root/'code-walkthrough.png'))
    assert not errors,errors
    browser.close()
print('PASS: highlighted text, real clipboard copy and source are identical; open code fits all widths.')
