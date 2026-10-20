"""מייצר את ../../claplab/index.html — מדריך הצטרפות למנוי בית-ספרי בקלפלב.

מקור הצילומים: דף ההדרכה של קלפלב (PDF). השם והמייל בצילום הטופס כבר מטושטשים במקור.
הסגנון והסקריפט ב-guide-template.html (נגזרו ממדריך ההכתבה).

הרצה:  cd _build/claplab  &&  python build_guide.py
"""
import base64
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "claplab" / "index.html"

# הדגשה: (left, top, width, height, צורה, מספר, pin_left, pin_top) — אחוזים מגודל התמונה
def shot(img, alt, w, h, marks, max_w):
    b64 = base64.b64encode((HERE / "img" / img).read_bytes()).decode()
    spans = ""
    for (l, t, mw, mh, shape, n, pl, pt) in marks:
        spans += (f'<span class="mk {shape}" style="left:{l}%;top:{t}%;width:{mw}%;height:{mh}%"></span>'
                  f'<span class="pin" style="left:{pl}%;top:{pt}%">{n}</span>')
    return (f'<figure class="mat" style="max-width:{max_w}px"><div class="shot" data-zoom>'
            f'<img src="data:image/png;base64,{b64}" alt="{alt}" width="{w}" height="{h}">{spans}</div></figure>')

def row(text, media, one=False):
    cls = "row one" if one else "row"
    return f'<div class="{cls}"><div class="text">{text}</div><div class="media">{media}</div></div>'

# pre = שורות (טקסט, תמונה) שבאות בתוך השלב לפני השורה הראשית
def step(n, title, text, media, one=False, pre=()):
    rows = "".join(row(*r) for r in pre) + row(text, media, one)
    return (f'<section class="step" id="s{n}"><button class="step-h" aria-expanded="false">'
            f'<span class="num">{n}</span><span class="st">{title}</span><span class="chev" aria-hidden="true"></span></button>'
            f'<div class="step-b">{rows}</div></section>')

STEPS = [
    step(1, "נכנסים לקלפלב בהזדהות אחידה",
         '<h4>נכנסים לאזור האישי</h4>'
         '<p>אחרי הכניסה לוחצים על <b>אייקון הדמות</b> <span class="n">1</span>, באזור האישי.</p>'
         '<div class="rule">לוחצים על העיגול של הדמות, <b>לא</b> על הכפתור הכתום "המשחקים שלי".</div>',
         shot("step-1-profile.png", "אייקון הדמות באזור האישי", 2170, 412,
              [(84.25, 11.8, 12.5, 65.8, "circ", 1, 84.5, 80)], 760), one=True,
         pre=[
             ('<p>נכנסים לאתר קלפלב, ולוחצים על <span style="white-space:nowrap"><b>"התחברות"</b> <span class="n">1</span>.</span></p>'
              '<a class="go" href="https://clap-lab.com/" target="_blank" rel="noopener">לכניסה לקלפלב ←</a>'
              '<div class="rule">לוחצים על <b>"התחברות"</b>, <b>לא</b> על הכפתור הכתום "ליצירת משחק".</div>',
              shot("step-1a-login.png", "מסך הפתיחה של קלפלב", 557, 577,
                   [(40.5, 70.5, 15.6, 6.2, "box", 1, 56.1, 70.5)], 360)),
             ('<h4>מאשרים את תנאי השימוש</h4>'
              '<p>נפתח מסך ההתחברות. בראשו כתוב CloseApp: זה המסך שאליו קלפלב מעבירה, הכול תקין.</p><p><b>קודם</b> מסמנים וי בתיבה של אישור התנאים <span class="n">1</span>.</p>'
              '<div class="tip soft">בלי הווי מופיעה הודעה אדומה, וההתחברות לא עוברת.</div>',
              shot("step-1b-terms.png", "תיבת אישור תנאי השימוש", 690, 836,
                   [(82.6, 61.7, 6.4, 5.3, "circ", 1, 89.0, 61.7)], 420)),
             ('<h4>מתחברים דרך משרד החינוך</h4>'
              '<p>לוחצים על <b>"התחברות משרד החינוך"</b> <span class="n">1</span>, ומתחברים ב<b>הזדהות אחידה</b>.</p>',
              shot("step-1c-moe.png", "הכפתור התחברות משרד החינוך", 717, 855,
                   [(16.5, 19.0, 70.6, 7.0, "box", 1, 87.1, 19.0)], 420)),
         ]),
    step(2, "בוחרים \"הצטרפות למוסד\"",
         '<p>נפתח תפריט. לוחצים על <b>"הצטרפות למוסד"</b>&nbsp;<span class="n">1</span>.</p>',
         shot("step-2-menu.png", "הפריט הצטרפות למוסד בתפריט", 534, 142,
              [(12.0, 22.0, 81.0, 55.0, "box", 1, 93.0, 22.0)], 440), one=True),
    step(3, "ממלאים את הטופס ושולחים בקשה",
         '<p>נפתח הטופס "הצטרפות למוסד". ממלאים רק שני שדות:</p>'
         '<ol><li><b>סמל מוסד</b> <span class="n">1</span>.</li>'
         '<li><b>טלפון</b> <span class="n">2</span>.</li>'
         '<li>לוחצים <b>"שליחת בקשה"</b> <span class="n">3</span>.</li></ol>'
         '<div class="tip soft">השם והמייל מופיעים לבד, ואי אפשר לשנות אותם.</div>'
         '<div class="tip">לא יודעים מה סמל המוסד? פונים לאיש הקשר במוסד.</div>',
         shot("step-3-form.png", "טופס הצטרפות למוסד", 1171, 990,
              [(3.1, 22.8, 93.7, 10.6, "box", 1, 96.8, 22.8),
               (3.1, 72.6, 93.7, 10.6, "box", 2, 96.8, 72.6),
               (76.9, 89.0, 20.0, 6.9, "box", 3, 76.9, 89.0)], 560)),
]

BODY = f'''<div class="wrap">
  <header class="hero">
    <div class="kicker">הדרכה צעד אחר צעד</div>
    <h1>הצטרפות למנוי בית-ספרי בקלפלב</h1>
    <p class="sub">משייכים את החשבון שלכם למוסד, בשלושה שלבים</p>
    <div class="tools"><button id="openAll">לפתוח את כל השלבים</button><button id="closeAll">לסגור הכול</button></div>
    <p class="scope">לוחצים על כל שלב כדי לפתוח אותו. לוחצים על תמונה כדי להגדיל אותה.</p>
  </header>
  <main style="margin-top:28px">{"".join(STEPS)}</main>

  <div class="done">
    <h2><span class="check"></span>הבקשה נשלחה!</h2>
    <p>ההצטרפות תושלם אחרי שהגורם המנהל במוסד יאשר אותה.</p>
  </div>
</div>'''

html = (HERE / "guide-template.html").read_text(encoding="utf8")
# כרטיס תצוגה לווטסאפ ולרשתות. התמונה ../../claplab/preview.jpg נוצרת מ-preview-card.html
# (צילום מסך 1200x630 ב-Chrome headless) — היא קובץ נפרד, כי תמונה מוטמעת לא נקראת כתצוגה מקדימה.
URL = "https://neshamalevy-design.github.io/matia-guides/claplab/"
META = f'''<meta name="description" content="משייכים את החשבון למוסד, בשלושה שלבים">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="הצטרפות למנוי בית-ספרי בקלפלב">
<meta property="og:description" content="משייכים את החשבון למוסד, בשלושה שלבים — הדרכה צעד אחר צעד">
<meta property="og:image" content="{URL}preview.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">'''
html = html.replace("{{TITLE}}", "הצטרפות למנוי בית-ספרי בקלפלב").replace("{{BODY}}", BODY)
html = html.replace("</title>", "</title>\n" + META, 1)
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html, encoding="utf8")
print("נכתב:", OUT, f"({OUT.stat().st_size // 1024}KB)")
