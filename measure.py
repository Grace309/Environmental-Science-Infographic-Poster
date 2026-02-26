from playwright.sync_api import sync_playwright
import os, time

p = sync_playwright().start()
b = p.chromium.launch()
pg = b.new_page(viewport={'width': 816, 'height': 1344}, device_scale_factor=2)

html_path = os.path.abspath('Fast_Fashion_Environmental_Impact_Canada.html').replace('\\', '/')
pg.goto('file:///' + html_path, wait_until='networkidle')
pg.evaluate('() => document.fonts.ready')
time.sleep(2)

# Measure key positions
info = pg.evaluate('''() => {
    const inf = document.querySelector('.infographic');
    const footer = document.querySelector('.footer');
    const solWrap = document.querySelector('.solutions-wrap');
    return {
        scrollHeight: inf.scrollHeight,
        footerTop: footer.getBoundingClientRect().top,
        footerHeight: footer.offsetHeight,
        solBottom: solWrap.getBoundingClientRect().bottom,
        gap: footer.getBoundingClientRect().top - solWrap.getBoundingClientRect().bottom
    };
}''')

print(f"Content scrollHeight: {info['scrollHeight']}px")
print(f"Footer top: {info['footerTop']}px, Footer height: {info['footerHeight']}px")
print(f"Solutions bottom: {info['solBottom']}px")
print(f"Gap (solutions->footer): {info['gap']}px")
print(f"Slack (1344 - scrollHeight): {1344 - info['scrollHeight']}px")

b.close()
p.stop()
