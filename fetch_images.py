import urllib.request
import re

req = urllib.request.Request(
    'https://www.plasticcollective.co/how-fast-fashion-is-bad-for-the-environment/',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)
resp = urllib.request.urlopen(req)
html = resp.read().decode('utf-8')

imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', html)
for i in imgs:
    if 'wp-content' in i.lower() or 'fashion' in i.lower() or 'plastic' in i.lower():
        print(i)
