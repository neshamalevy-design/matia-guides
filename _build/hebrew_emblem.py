"""Emblem C without its English words: "found it together!" and "we've got you" are removed, and "where to click" on the
button becomes "לחצו כאן" (written in the browser, in Varela Round, so the Hebrew is shaped correctly).
Run from the repo root:  python -X utf8 _build/hebrew_emblem.py   ->  _build/emblem-c-he.jpg"""
import base64, io, pathlib, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).parent
WORD = sys.argv[1] if len(sys.argv) > 1 else 'לחצו כאן'                    # the button's text
OUT = sys.argv[2] if len(sys.argv) > 2 else 'emblem-c-he.jpg'
SIZE = int(sys.argv[3]) if len(sys.argv) > 3 else 92                        # font size; a long word needs less
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
im = Image.open(HERE / 'emblem-c.jpg').convert('RGB')
a = np.asarray(im).astype(float)
H, W = a.shape[:2]
lum = a.sum(axis=2)


def grow(m, n):
    return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(n))) > 0


mask = np.zeros((H, W), bool)
# dark navy words on the light page
for x0, y0, x1, y1 in [(826, 610, 1090, 745), (675, 1580, 885, 1705)]:
    m = np.zeros((H, W), bool); m[y0:y1, x0:x1] = lum[y0:y1, x0:x1] < 450
    mask |= grow(m, 7)
# peach words on the dark button (not the finger below them, not the lantern's glow)
x0, y0, x1, y1 = 560, 905, 1095, 1030
m = np.zeros((H, W), bool)
sub = a[y0:y1, x0:x1]
m[y0:y1, x0:x1] = (sub[..., 0] > 190) & (sub[..., 1] > 140)
m[1003:, 815:965] = False
mask |= grow(m, 9)

for x0, y0, x1, y1 in [(800, 585, 1115, 770), (650, 1555, 910, 1730), (530, 875, 1125, 1060)]:   # smooth fill, one area at a time
    w, mw = a[y0:y1, x0:x1], mask[y0:y1, x0:x1]
    for _ in range(1500):
        avg = (np.roll(w, 1, 0) + np.roll(w, -1, 0) + np.roll(w, 1, 1) + np.roll(w, -1, 1)) / 4
        w[mw] = avg[mw]
clean = Image.fromarray(a.clip(0, 255).astype(np.uint8))
buf = io.BytesIO(); clean.save(buf, 'PNG')
uri = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

# the Hebrew on the button: centred where "where to click" was, tilted like the button
html = (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
        f'<link href="https://fonts.googleapis.com/css2?family=Varela+Round&display=swap" rel="stylesheet"><style>'
        f'*{{margin:0}}body{{width:{W}px;height:{H}px;position:relative;overflow:hidden}}img{{display:block}}'
        f'.w{{position:absolute;left:830px;top:972px;transform:translate(-50%,-50%) rotate(-5.5deg);white-space:nowrap;'
        f'font:400 {SIZE}px "Varela Round";color:#fbbd8c;-webkit-text-stroke:3px #fbbd8c;'
        f'text-shadow:0 3px 0 rgba(120,50,20,.35),0 6px 14px rgba(0,0,0,.25)}}</style></head>'
        f'<body><img src="{uri}"><div class="w">{WORD}</div></body></html>')
with tempfile.TemporaryDirectory() as tmp:
    src, png = pathlib.Path(tmp) / 'e.html', pathlib.Path(tmp) / 'e.png'
    src.write_text(html, encoding='utf8')
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--virtual-time-budget=6000',
                    f'--window-size={W},{H}', f'--screenshot={png}', src.as_uri()], check=True, capture_output=True)
    Image.open(png).convert('RGB').crop((0, 0, W, H)).save(HERE / OUT, quality=92)
print('ok')
