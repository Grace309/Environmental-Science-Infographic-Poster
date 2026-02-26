from playwright.sync_api import sync_playwright
import os, time

p = sync_playwright().start()
b = p.chromium.launch()

# Use device scale factor 2 for high quality
pg = b.new_page(viewport={'width': 816, 'height': 1344}, device_scale_factor=2)

html_path = os.path.abspath('Fast_Fashion_Environmental_Impact_Canada.html').replace('\\', '/')
pg.goto('file:///' + html_path, wait_until='networkidle')

# Wait for all Google Fonts to load
pg.evaluate('() => document.fonts.ready')
time.sleep(3)

# Double-check font status
font_status = pg.evaluate('''() => {
    const result = [];
    document.fonts.forEach(f => { if (f.status === 'loaded') result.push(f.family + ' ' + f.weight + ' ' + f.style); });
    return result;
}''')
print(f"Loaded fonts: {len(font_status)}")
for f in font_status:
    print(f"  {f}")

# Check actual content height
height = pg.evaluate('document.querySelector(".infographic").scrollHeight')
# Check footer
footer_h = pg.evaluate('document.querySelector(".footer").offsetHeight')
# Check header
header_h = pg.evaluate('document.querySelector(".header").offsetHeight')
page_h = 14 * 96  # 14in at 96dpi
print(f"Content height: {height}px")
print(f"Header height: {header_h}px")
print(f"Footer height: {footer_h}px")
print(f"Page height (14in): {page_h}px")
print(f"Overflow: {height - page_h}px")

pg.pdf(
    path='Fast_Fashion_Environmental_Impact_Canada.pdf',
    width='8.5in',
    height='14in',
    margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
    print_background=True,
    prefer_css_page_size=True
)

# Also generate a high-quality screenshot-based PDF as backup
from PIL import Image
screenshot_bytes = pg.screenshot(full_page=False)
with open('_temp_screenshot.png', 'wb') as f:
    f.write(screenshot_bytes)

img = Image.open('_temp_screenshot.png')
# Convert to RGB (remove alpha)
img_rgb = img.convert('RGB')
# 8.5in x 14in at the screenshot DPI
# viewport is 816x1344 at scale 2 => 1632x2688 pixels
# For 8.5x14 inch PDF: DPI = 1632/8.5 = 192
dpi = img_rgb.width / 8.5
img_rgb.save(
    'Fast_Fashion_Environmental_Impact_Canada.pdf',
    'PDF',
    resolution=dpi
)
os.remove('_temp_screenshot.png')

b.close()
p.stop()
print("PDF generated successfully")
