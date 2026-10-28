"""The cards' identity at the top of every guide: the small footprints "צעד צעד" in place of the kicker, and the fixed
picture beside the title, in one row: footprints right, picture left (desktop only; on a phone the footprints and the title stay, so the menu is seen at once).
Everything is embedded in the page (data URIs), so a guide still works as a single file.

Also a small signature at the bottom of every page (guides, course pages and the hub).
Run from the repo root:  python -X utf8 _build/brand_header.py            -> all pages
                         python -X utf8 _build/brand_header.py forms      -> one guide
⚠️ A guide's build overwrites this. After rebuilding a guide: run this again (like preview_cards.py)."""
import base64, io, pathlib, re, subprocess, sys, tempfile
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / '_build'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
sys.path.insert(0, str(B))
import preview_cards as pc                                                    # the same feet, picture and font as the cards

DARK = {'ics-outlook'}        # an older guide with a dark, right-aligned header: no picture, footprints on the right
DARK_CSS = '<style id="brand-css-dark">.hero .brand-art{display:none!important}.hero .brand-feet{margin:-6px 0 8px auto}</style>'
PAGES = ['', 'art-therapists', 'middle-school', 'kindergarten-inclusion-ai']                               # hub and course pages: the signature only
GUIDES = ['onedrive-folders', 'dictation', 'tzafonet-word', 'read-dictate', 'forms', 'ics-outlook', 'safe-domains', 'claplab', 'copy-shared-folder', 'share-document', 'open-shared-document', 'iep-copilot', 'tachi-agent', 'tachi-agent-lite', 'forms-copy']


def feet_png():
    """the footprints with "צעד" written in, on a transparent background, 2x for sharp screens."""
    html = (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
            f'<link href="https://fonts.googleapis.com/css2?family={pc.FEET_FONT[0].replace(" ", "+")}&display=swap" rel="stylesheet">'
            f'<style>*{{margin:0}}html,body{{background:transparent}}body{{padding:4px;direction:ltr}}'
            f'.feet{{position:relative}}.feet img{{width:100%;display:block}}'
            f'.feet b{{position:absolute;display:flex;align-items:center;justify-content:center;color:#fff3e8;line-height:1;white-space:nowrap;'
            f'-webkit-text-stroke:{pc.FEET_STROKE}px #fff3e8;paint-order:stroke fill;text-shadow:0 1px 0 rgba(0,0,0,.18),0 2px 4px rgba(0,0,0,.15)}}'
            f'</style></head><body>'
            f'{pc.feet_html("data:image/png;base64," + base64.b64encode(pc.FEET.read_bytes()).decode())}{pc.FIT}</body></html>')
    with tempfile.TemporaryDirectory() as tmp:
        src, png = pathlib.Path(tmp) / 'f.html', pathlib.Path(tmp) / 'f.png'
        src.write_text(html, encoding='utf8')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--virtual-time-budget=7000',
                        '--default-background-color=00000000', '--window-size=700,400', f'--screenshot={png}', src.as_uri()],
                       check=True, capture_output=True)
        im = Image.open(png).convert('RGBA')
    im = im.crop(im.getbbox()).quantize(colors=128, method=Image.Quantize.FASTOCTREE)   # small: ~20KB
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def emblem_jpg():
    im = Image.open(pc.EMBLEM).convert('RGB'); im.thumbnail((360, 450))
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=84, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


CSS = """<style id="brand-css">
  header.hero{position:relative}
  .hero .brand-row{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:28px;margin:6px 0 10px}
  .hero .brand-row h1{margin:0}
  .hero .brand-feet{display:block;height:110px;width:auto;margin:0;justify-self:end}
  .hero .brand-art{display:block;height:170px;width:auto;margin:-30px -14px -30px 0;justify-self:start;pointer-events:none;
    -webkit-mask-image:radial-gradient(ellipse 50% 50% at center,#000 70%,transparent 100%);mask-image:radial-gradient(ellipse 50% 50% at center,#000 70%,transparent 100%)}
  .hero .kicker{display:none}
  @media (max-width:820px){ .hero .brand-row{display:block} .hero .brand-art{display:none} .hero .brand-feet{height:auto;width:104px;margin:-6px auto 8px} }
</style>"""
# an older guide with a dark header (DARK): no row, the footprints alone above the title, as before
OLD_CSS = """<style id="brand-css">
  header.hero{position:relative}
  .hero .brand-feet{display:block;width:118px;height:auto;margin:-6px auto 8px}
  .hero .brand-art{position:absolute;top:10px;left:14px;width:140px;height:auto;pointer-events:none;
    -webkit-mask-image:radial-gradient(ellipse 50% 50% at center,#000 70%,transparent 100%);mask-image:radial-gradient(ellipse 50% 50% at center,#000 70%,transparent 100%)}
  .hero .kicker{display:none}
  @media (max-width:820px){ .hero .brand-art{display:none} .hero .brand-feet{width:104px} }
</style>"""

SIGN_CSS = """<style id="brand-sign-css">
  .brand-sign{margin:-30px auto 28px;text-align:center;font:400 13.5px/1.55 'Assistant',Calibri,Arial,sans-serif;color:#7d8f92}
  .brand-sign b{font-weight:600;color:#5b6f72}
</style>"""
SIGN = '<footer class="brand-sign">נבנה ע״י <b>נחמה לוי</b>{cc}<br>רכזת תקשוב · מתי״א טבריה · מתי״א כרמיאל</footer>'
CLAUDE_CODE = {'forms-copy'}   # guides whose signature adds "(בעזרת קלוד קוד)" after the name (Nechama, 2026-10-28)


def sign(h, folder=''):
    """the small signature at the bottom of the page (every screen of a guide)."""
    h = re.sub(r'\n?<style id="brand-sign-css">.*?</style>', '', h, flags=re.S)
    h = re.sub(r'<footer class="brand-sign">.*?</footer>\n?', '', h, flags=re.S)
    h = h.replace('</head>', SIGN_CSS + '\n</head>', 1)
    i = h.rindex('</body>')
    return h[:i] + SIGN.format(cc=' (בעזרת קלוד קוד)' if folder in CLAUDE_CODE else '') + '\n' + h[i:]


def inject(folder, feet, art):
    p = ROOT / folder / 'index.html'
    h = p.read_text(encoding='utf8')
    h = re.sub(r'\n?<style id="brand-css(?:-dark)?">.*?</style>', '', h, flags=re.S)    # a re-run replaces the old one
    h = re.sub(r'<img class="brand-(?:feet|art)"[^>]*>', '', h)
    h = h.replace('<div class="brand-row">', '').replace('</div><!--/brand-row-->', '')
    h = sign(h, folder)
    dark = folder in DARK
    h = h.replace('</head>', (OLD_CSS + '\n' + DARK_CSS if dark else CSS) + '\n</head>', 1)
    art_tag = f'<img class="brand-art" src="{art}" alt="">'
    feet_tag = f'<img class="brand-feet" src="{feet}" alt="צעד צעד">'
    i = h.index('<h1>', h.index('<header class="hero">'))
    j = h.index('</h1>', i) + len('</h1>')
    if dark:
        h = h.replace('<header class="hero">', '<header class="hero">' + art_tag, 1)
        h = h[:i + len(art_tag)] + feet_tag + h[i + len(art_tag):]
    else:
        # one row (Nechama 2026-10-26): the footprints right of the title, the picture left of it, at the same distance
        h = h[:i] + '<div class="brand-row">' + feet_tag + h[i:j] + art_tag + '</div><!--/brand-row-->' + h[j:]
    p.write_text(h, encoding='utf8')


if __name__ == '__main__':
    feet, art = feet_png(), emblem_jpg()
    print('assets', len(feet) // 1024, 'KB +', len(art) // 1024, 'KB')
    for f in (sys.argv[1:] or GUIDES + PAGES):
        if f in GUIDES:
            inject(f, feet, art)
        else:
            p = ROOT / f / 'index.html'; p.write_text(sign(p.read_text(encoding='utf8')), encoding='utf8')
        print('ok', f or '(דף המפתח)')
