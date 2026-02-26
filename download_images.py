import urllib.request
import os

images = {
    'fast-fashion.jpg': 'https://www.plasticcollective.co/wp-content/uploads/2024/02/fast-fashion.jpg',
    'pexels-clothing.jpg': 'https://www.plasticcollective.co/wp-content/uploads/2026/02/pexels-mikhail-nilov-8297480.jpg',
    'textile-waste.jpg': 'https://www.plasticcollective.co/wp-content/uploads/2026/02/naja-bertolt-jensen-iZP2Uwsc_wk-unsplash.jpg',
}

for name, url in images.items():
    print(f'Downloading {name}...')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    resp = urllib.request.urlopen(req)
    with open(os.path.join('.', name), 'wb') as f:
        f.write(resp.read())
    print(f'  Saved {name} ({os.path.getsize(name)} bytes)')

print('Done!')
