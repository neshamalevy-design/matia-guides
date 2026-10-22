"""כרטיסי תצוגה (og:image) לכל דפי האתר: מה שמופיע בווצאפ כששולחים קישור.
לכל דף: תמונה 1200x630 (preview.jpg בתיקייה שלו) + תגיות og בראש ה-index.html שלו.

הכרטיס: "צעד צעד" בתוך עקבות שהולכות מימין לשמאל, מתחתיו "מדריך בנושא:" ושם המדריך. משמאל תמונה קבועה לכל המדריכים.
המשפט שמתאר את המדריך מופיע בווצאפ מתחת לתמונה (og:description).

החלקים, ואיך נוצרו (כל קובץ-מקור יושב כאן):
- התמונה: emblem-c.jpg (נוצרה ב-GPT לפי logo-prompt.md) → hebrew_emblem.py מסיר את האנגלית וכותב "לחצו כאן" → emblem-c-he.jpg
- העקבות: feet2_src.jpg (ג'מיני) → rotatefeet.py מסובב אותן מימין לשמאל, בלי המילים → steps-feet2-blank.png
          → teal_feet.py צובע את שתיהן בגווני התכלת → steps-feet2-teal.png. המילה "צעד" נכתבת כאן, בגופן FEET_FONT.

הרצה (מתוך שורש הריפו):   python -X utf8 _build/preview_cards.py            → כל הדפים
                          python -X utf8 _build/preview_cards.py forms      → דף אחד
                          python -X utf8 _build/preview_cards.py --sheet    → גם דף-סקירה של כל הכרטיסים (_build/cards-sheet.png, לבדיקה בלבד: לא לשמור בריפו)

⚠️ אחרי בנייה מחדש של מדריך — להריץ שוב: הבנייה דורסת את התגיות.
מדריך חדש = שורה חדשה ב-CARDS.
קלפלב: הכרטיס שלו נבנה בכלי שלו (_build/claplab/), ולא כאן."""
import base64, pathlib, re, subprocess, sys, tempfile
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://neshamalevy-design.github.io/matia-guides/'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
EMBLEM = ROOT / '_build' / 'emblem-c-he.jpg'   # the fixed picture (GPT), English removed, "לחצו כאן" on the button (hebrew_emblem.py)
FEET = ROOT / '_build' / 'steps-feet2-teal.png'   # שתי העקבות בלי המילים, מימין לשמאל (נוצר ב-rotatefeet.py מ-feet2_src.jpg)
FEET_WORDS = [(284, 375, 454, 449), (178, 112, 352, 188)]   # where "צעד" sits in each sole, in the image's px — measured inside the coloured area
FEET_W = 230                                       # width of the footprints on the card
FEET_FONT = ('Varela Round', '400')                # the font of "צעד"
FEET_STROKE = 0.9                                  # Varela Round has no bold: a thin stroke in the letter colour thickens it

GUIDE, COURSE = 'מדריך בנושא:', 'מדריכים להשתלמות:'
# folder: (שורת הפתיח, נושא, משפט התיאור שמופיע בווצאפ)
CARDS = {
    'onedrive-folders': (GUIDE, 'תיקיות ומסמכים ב-OneDrive',
                         'מהכניסה ל-OneDrive, דרך תיקייה לכל ילד, ועד מסמך שנשמר במקום הנכון'),
    'dictation': (GUIDE, 'הכתבה קולית ב-Word', 'ממסמך חדש, דרך ההכתבה, ועד תיקון טעויות בעזרת Copilot'),
    'tzafonet-word': (GUIDE, 'כניסה ל-Word דרך צפונט', 'מצפונט, דרך הזדהות משרד החינוך, ועד מסמך פתוח ב-Word'),
    'read-dictate': (GUIDE, 'הקראה והכתבה ב-Word', 'Word קורא את המסמך בקול, ועונים בקול על השאלות'),
    'forms': (GUIDE, 'יצירת טופס ב-Microsoft Forms', 'מהכניסה לאפליקציה, דרך בניית השאלות, ועד שיתוף הטופס'),
    'ics-outlook': (GUIDE, 'העלאת יומן מקובץ ICS ל-Outlook', 'מיצירת לוח שנה ייעודי ועד אימות שהאירועים נכנסו'),
    'safe-domains': (GUIDE, 'איסוף דומיינים בטוחים',
                     'לרכזות התקשוב: ייצוא אנשי הקשר מ-Outlook, וקופיילוט ממלא איתן את קובץ האיסוף'),
    'copy-shared-folder': (GUIDE, 'העתקת תיקייה משותפת לקבצים שלי',
                           'ממייל ההזמנה, דרך ״העתק אל״, ועד עותק שלך ב-OneDrive שאפשר לערוך'),
    'art-therapists': (COURSE, 'מטפלות באומנויות · תשפ״ז', 'OneDrive, הכתבה קולית ו-Forms, לפי סדר המפגשים'),
    'middle-school': (COURSE, 'טכנופדגוגיה לחט״ב · 2027', 'כניסה ל-Word דרך צפונט, והקראה והכתבה'),
    '': ('כל המדריכים במקום אחד:', 'מדריכי המתי״א',
         'מדריכי הפעלה קצרים, שלב אחרי שלב, עם סימון מדויק של כל מקום שלוחצים עליו'),
}

def css(bg, wide):
    """bg: the emblem's own background colour, so it blends into the card. wide: a landscape emblem gets more room."""
    box = 'width:620px' if wide else 'width:505px;height:630px'
    size = 'width:100%;height:auto' if wide else 'width:100%;height:100%;object-fit:cover'
    return f"""*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:{bg};font-family:'Assistant',Arial,sans-serif;display:flex;align-items:center;overflow:hidden}}
.t{{flex:1;padding:0 60px 0 10px}}
.feet{{position:relative;display:block;margin:0 -6px 30px 0}}
.feet img{{width:100%;display:block}}
.feet b{{position:absolute;display:flex;align-items:center;justify-content:center;color:#fff3e8;line-height:1;white-space:nowrap;-webkit-text-stroke:{FEET_STROKE}px #fff3e8;paint-order:stroke fill;text-shadow:0 1px 0 rgba(0,0,0,.18),0 2px 4px rgba(0,0,0,.15)}}
.lead{{font-size:44px;font-weight:600;color:#4f6467}}
h1{{font-size:80px;font-weight:800;color:#0f7c80;line-height:1.08;margin-top:4px}}
.nw{{white-space:nowrap}}
h1.long{{font-size:64px}}
h1 .sm{{font-size:56px;color:#5b6f72}}
.m{{{box};flex:none}}
.m img{{{size};display:block;object-position:center 55%;
  -webkit-mask-image:radial-gradient(ellipse 50% 50% at center,#000 82%,transparent 100%)}}"""


def title_html(title):
    """"ב-Word" לא נשבר באמצע, ו"· תשפ״ז" יורד לשורה משלו."""
    title = re.sub(r'(\S+-[A-Za-z]+(?: [A-Za-z]+)*)', r'<span class="nw">\1</span>', title)   # "ב-Microsoft Forms" stays together
    return title.replace(' · ', '<br><span class="sm">') + ('</span>' if ' · ' in title else '')


def feet_html(src):
    """the footprints, and "צעד" written in each sole as large as fits (fitted by a small script after the fonts load)."""
    fw, fh = Image.open(FEET).size
    k = FEET_W / fw
    words = ''.join(f'<b style="left:{x0 * k:.1f}px;top:{y0 * k:.1f}px;width:{(x1 - x0) * k:.1f}px;height:{(y1 - y0) * k:.1f}px;'
                    f'font-family:&quot;{FEET_FONT[0]}&quot;;font-weight:{FEET_FONT[1]}"><span>צעד</span></b>' for x0, y0, x1, y1 in FEET_WORDS)
    return f'<div class="feet" style="width:{FEET_W}px;height:{fh * k:.1f}px"><img src="{src}" alt="צעד צעד">{words}</div>'


FIT = """<script>document.fonts.ready.then(()=>{document.querySelectorAll('.feet b').forEach(d=>{const s=d.firstChild;let f=6;
d.style.fontSize=f+'px';while(f<200){d.style.fontSize=(f+1)+'px';const r=s.getBoundingClientRect();
if(r.width>d.clientWidth*0.97||r.height>d.clientHeight*1.15)break;f++}d.style.fontSize=f+'px'})})</script>"""


def render(folder, emblem_path=EMBLEM, out=None):
    lead, title, _ = CARDS[folder]
    em = Image.open(emblem_path).convert('RGB')
    border = [em.getpixel((x, y)) for x in range(0, em.width, 20) for y in (3, em.height - 4)] +              [em.getpixel((x, y)) for y in range(0, em.height, 20) for x in (3, em.width - 4)]
    bg = '#%02x%02x%02x' % tuple(sorted(c[i] for c in border)[len(border) // 2] for i in range(3))   # median edge colour
    emblem = 'data:image/jpeg;base64,' + base64.b64encode(pathlib.Path(emblem_path).read_bytes()).decode()
    feet = 'data:image/png;base64,' + base64.b64encode(FEET.read_bytes()).decode()
    html = (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
            f'<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@600;800&family={FEET_FONT[0].replace(" ", "+")}:wght@{FEET_FONT[1]}&display=swap" rel="stylesheet">'
            f'<style>{css(bg, em.width > em.height)}</style></head><body><div class="t">{feet_html(feet)}'
            f'<div class="lead">{lead}</div><h1{" class=long" if len(title) > 24 else ""}>{title_html(title)}</h1></div>'
            f'<div class="m"><img src="{emblem}"></div>{FIT}</body></html>')
    with tempfile.TemporaryDirectory() as tmp:
        src, png = pathlib.Path(tmp) / 'card.html', pathlib.Path(tmp) / 'card.png'
        src.write_text(html, encoding='utf8')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--virtual-time-budget=7000',
                        '--window-size=1200,630', f'--screenshot={png}', src.as_uri()], check=True, capture_output=True)
        Image.open(png).convert('RGB').crop((0, 0, 1200, 630)).save(out or ROOT / folder / 'preview.jpg', quality=86, optimize=True)


def tags(folder):
    lead, title, sub = CARDS[folder]
    url = SITE + (folder + '/' if folder else '')
    return ('<!--og-->\n'
            f'<meta name="description" content="{sub}">\n'
            '<meta property="og:type" content="website">\n<meta property="og:locale" content="he_IL">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{sub}">\n'
            f'<meta property="og:image" content="{url}preview.jpg">\n'
            '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            '<meta name="twitter:card" content="summary_large_image">\n<!--/og-->')


def inject(folder):
    p = ROOT / folder / 'index.html'
    h = p.read_text(encoding='utf8')
    h = re.sub(r'\n?<!--og-->.*?<!--/og-->', '', h, flags=re.S)                # ריצה חוזרת: מחליפים את הבלוק הקודם
    h = re.sub(r'\n?<meta name="description"[^>]*>', '', h)                   # התיאור יושב בתוך הבלוק
    h = h.replace('</title>', '</title>\n' + tags(folder), 1)
    p.write_text(h, encoding='utf8')


def sheet():
    ims = [Image.open(ROOT / f / 'preview.jpg') for f in CARDS]
    w, h = 600, 315
    out = Image.new('RGB', (w * 2 + 30, (h + 15) * ((len(ims) + 1) // 2) + 15), '#ffffff')
    for i, im in enumerate(ims):
        out.paste(im.resize((w, h)), (10 + (i % 2) * (w + 10), 15 + (i // 2) * (h + 15)))
    out.save(ROOT / '_build' / 'cards-sheet.png')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    for f in (args or CARDS):
        render(f); inject(f); print('ok', f or '(דף המפתח)')
    if '--sheet' in sys.argv:
        sheet(); print('sheet: _build/cards-sheet.png')
