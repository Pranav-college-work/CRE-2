from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent
html = root.parent.parent / 'Tutorial 4' / 'Tutorial4_Solutions.html'
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1100}, device_scale_factor=1)
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(html.as_uri())
    page.wait_for_load_state('networkidle')
    assert page.title().startswith('Tutorial 4')
    assert page.locator('img').count() == 4
    assert page.locator('img').evaluate_all('(images)=>images.every(i=>i.complete && i.naturalWidth>0)')
    assert page.locator('a[href^="#"]').evaluate_all('(links)=>links.every(a=>document.querySelector(a.getAttribute("href")))')
    assert not page.locator('body').inner_text().count('{{')
    page.screenshot(path=str(root/'desktop.png'))
    page.locator('#q7 figure').first.screenshot(path=str(root/'q7-plot.png'))
    page.locator('#q8 figure').screenshot(path=str(root/'q8-plot.png'))
    page.locator('#k-input').fill('100')
    page.locator('#calculate-k').click()
    result=page.locator('#k-output').inner_text()
    assert '0.1291524 cm' in result, result
    print('Q4 calculator:', result)
    page.locator('#k-input').fill('-1')
    page.locator('#calculate-k').click()
    assert 'positive' in page.locator('#k-output').inner_text()
    with page.expect_download() as info:
        page.locator('a[download="tutorial4_code.py"]').click()
    destination=root/'downloaded_code.py'
    info.value.save_as(destination)
    assert destination.read_bytes() == (root/'tutorial4_code.py').read_bytes()
    for width in [390, 768, 1440]:
        page.set_viewport_size({'width':width,'height':1000})
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), width
    page.set_viewport_size({'width':390,'height':1000})
    page.evaluate('window.scrollTo(0,0)')
    page.screenshot(path=str(root/'mobile.png'))
    assert not errors, errors
    browser.close()
print('PASS: figures, navigation, calculator, Python download, and responsive widths.')
