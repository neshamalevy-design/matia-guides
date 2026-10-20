"""מייצר את ../../claplab/index.html — מדריך הצטרפות למנוי בית-ספרי בקלפלב.

הפורמט = הסטנדרט של מדריכי חט״ב (צפונט, הקראה והכתבה):
מסך-תפריט עם פרקים · תיבות הסבר על הצילום · מספר אחד בכל "הבא".
הסגנון והסקריפט ב-guide-template.html (נגזרו מ-tzafonet-word/index.html).
בלי קישור "כל המדריכים" — לבקשת נחמה.

מקור הצילומים: דף ההדרכה של קלפלב (PDF, השם והמייל מטושטשים במקור) + צילומי ההתחברות של נחמה.

הרצה:  cd _build/claplab  &&  python build_guide.py
כרטיס התצוגה (../../claplab/preview.jpg) נוצר מ-preview-card.html: צילום מסך 1200x630 ב-Chrome headless.
"""
import base64
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "claplab" / "index.html"


# ---- תיבות הסבר על הצילום ----
# M(מספר, left, top, width, height, כיתוב, מיקום) — ארבעת המספרים באחוזים מגודל התמונה.
# מיקום התיבה: above / below (מחוץ לתמונה) · left / right (על התמונה, בגובה הסימון).
# ax (רשות) = נקודת החיבור של הקו, באחוזים מרוחב התמונה — כשהקו מאמצע הסימון חוצה תיבה אחרת.
def M(n, x, y, w, h, label, place, circle=False, ax=None):
    return dict(n=n, x=x, y=y, w=w, h=h, label=label, place=place, circle=circle, ax=ax)

def box_w(text, size):
    return (15.3 if size == 28 else 11.9) * len(text) + 34

def callout(img, alt, iw, ih, marks, W=560, max_w=None):
    b64 = base64.b64encode((HERE / "img" / img).read_bytes()).decode()
    imgw = W - 28
    imgh = ih * imgw / iw
    top = 90 if any(m["place"] == "above" for m in marks) else 10
    below = any(m["place"] == "below" for m in marks)
    H = top + imgh + (92 if below else 10)
    items = []
    for m in marks:
        mx, my = 14 + m["x"] / 100 * imgw, top + m["y"] / 100 * imgh
        mw, mh = m["w"] / 100 * imgw, m["h"] / 100 * imgh
        rx = min(mw, mh) / 2 if m["circle"] else 7
        side = m["place"] in ("left", "right")
        size, bh = (22, 44) if side else (28, 50)
        bw = box_w(m["label"], size)
        if side:
            cy = my + mh / 2
            bx = mx - 26 - bw if m["place"] == "left" else mx + mw + 26
            by = cy - bh / 2
            line = (mx if m["place"] == "left" else mx + mw, cy, bx + bw if m["place"] == "left" else bx, cy)
        else:
            cx = 14 + m["ax"] / 100 * imgw if m["ax"] is not None else mx + mw / 2
            bx = min(max(cx - bw / 2, 4), W - 4 - bw)
            lx = min(max(cx, bx + 14), bx + bw - 14)
            if m["place"] == "above":
                by = 10
                line = (lx, by + bh, lx, my)
            else:
                by = top + imgh + 30
                line = (lx, my + mh, lx, by)
        items.append(
            f'<g class="co-item" data-n="{m["n"]}">'
            f'<line x1="{line[0]:.1f}" y1="{line[1]:.1f}" x2="{line[2]:.1f}" y2="{line[3]:.1f}" class="co-line"/>'
            f'<rect x="{mx:.1f}" y="{my:.1f}" width="{mw:.1f}" height="{mh:.1f}" rx="{rx:.1f}" class="co-mark"/>'
            f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh}" rx="10" class="co-box"/>'
            f'<text x="{bx + bw / 2:.1f}" y="{by + bh / 2:.1f}" class="co-text" style="font-size:{size}px">{m["label"]}</text>'
            f'<circle cx="{mx + mw:.1f}" cy="{my:.1f}" r="15" class="co-pin"/>'
            f'<text x="{mx + mw:.1f}" y="{my:.1f}" class="co-num">{m["n"]}</text></g>')
    return (f'<figure class="co" style="max-width:{max_w or W}px"><svg viewBox="0 0 {W} {H:.0f}" role="img" aria-label="{alt}">'
            f'<image href="data:image/png;base64,{b64}" x="14" y="{top}" width="{imgw}" height="{imgh:.1f}"/>'
            f'{"".join(items)}</svg></figure>')


def step(n, title, text, media):
    return (f'<section class="step" id="s{n}"><button class="step-h" aria-expanded="false">'
            f'<span class="num">{n}</span><span class="st">{title}</span><span class="chev" aria-hidden="true"></span></button>'
            f'<div class="step-b"><div class="row one"><div class="text">{text}</div>'
            f'<div class="media">{media}</div></div></div></section>')

def chapter(cid, tag, title, steps):
    return (f'<section class="chap" id="{cid}"><a class="back-hub" href="#">→ חזרה לתוכן העניינים</a>'
            f'<div class="chapter"><span>{tag}</span>{title}</div>{"".join(steps)}</section>')


CH1 = [
    step(1, "לוחצים על \"התחברות\"",
         '<p>נכנסים לאתר קלפלב:</p>'
         '<a class="go" href="https://clap-lab.com/" target="_blank" rel="noopener">לכניסה לקלפלב ←</a>'
         '<p>לוחצים על <b>"התחברות"</b> <span class="n">1</span>.</p>'
         '<div class="rule">לוחצים על <b>"התחברות"</b>, <b>לא</b> על הכפתור הכתום "ליצירת משחק".</div>',
         callout("step-1a-login.png", "מסך הפתיחה של קלפלב", 557, 577,
                 [M(1, 40.5, 70.5, 15.6, 6.2, "התחברות", "below")], W=440)),
    step(2, "מסמנים וי באישור תנאי השימוש",
         '<p>נפתח מסך ההתחברות. בראשו כתוב CloseApp: זה המסך שאליו קלפלב מעבירה, הכול תקין.</p>'
         '<p><b>קודם</b> מסמנים וי בתיבה של אישור התנאים <span class="n">1</span>.</p>'
         '<div class="tip soft">בלי הווי מופיעה הודעה אדומה, וההתחברות לא עוברת.</div>',
         callout("step-1b-terms.png", "תיבת אישור תנאי השימוש", 690, 836,
                 [M(1, 82.6, 61.7, 6.4, 5.3, "מסמנים וי", "left", circle=True)], W=480)),
    step(3, "מתחברים דרך משרד החינוך",
         '<p>לוחצים על <b>"התחברות משרד החינוך"</b> <span class="n">1</span>, ומתחברים ב<b>הזדהות אחידה</b>.</p>',
         callout("step-1c-moe.png", "הכפתור התחברות משרד החינוך", 717, 855,
                 [M(1, 16.5, 19.0, 70.6, 7.0, "התחברות משרד החינוך", "above")], W=480)),
]

CH2 = [
    step(4, "לוחצים על אייקון הדמות",
         '<p>אחרי ההתחברות נפתח האזור האישי. לוחצים על <b>אייקון הדמות</b> <span class="n">1</span>.</p>'
         '<div class="rule">לוחצים על העיגול של הדמות, <b>לא</b> על הכפתור הכתום "המשחקים שלי".</div>',
         callout("step-1-profile.png", "אייקון הדמות באזור האישי", 2170, 412,
                 [M(1, 84.25, 11.8, 12.5, 65.8, "אייקון הדמות", "above", circle=True)])),
    step(5, "בוחרים \"הצטרפות למוסד\"",
         '<p>נפתח תפריט. לוחצים על <b>"הצטרפות למוסד"</b> <span class="n">1</span>.</p>',
         callout("step-2-menu.png", "הפריט הצטרפות למוסד בתפריט", 534, 142,
                 [M(1, 12.0, 22.0, 81.0, 55.0, "הצטרפות למוסד", "below")], W=440)),
    step(6, "ממלאים את הטופס ושולחים בקשה",
         '<p>נפתח הטופס "הצטרפות למוסד". ממלאים רק שני שדות:</p>'
         '<ol><li><b>סמל מוסד</b> <span class="n">1</span>.</li>'
         '<li><b>טלפון</b> <span class="n">2</span>.</li>'
         '<li>לוחצים <b>"שליחת בקשה"</b> <span class="n">3</span>.</li></ol>'
         '<div class="tip soft">השם והמייל מופיעים לבד, ואי אפשר לשנות אותם.</div>'
         '<div class="tip">לא יודעים מה סמל המוסד? פונים לאיש הקשר במוסד.</div>'
         '<div class="tip soft">ההצטרפות תושלם אחרי שהגורם המנהל במוסד יאשר אותה.</div>',
         callout("step-3-form.png", "טופס הצטרפות למוסד", 1171, 990,
                 [M(1, 3.1, 22.8, 93.7, 10.6, "סמל מוסד", "above"),
                  M(2, 3.1, 72.6, 93.7, 10.6, "טלפון", "below", ax=22),
                  M(3, 76.9, 89.0, 20.0, 6.9, "שליחת בקשה", "below")])),
]

TOC = ('<nav class="toc">'
       '<button type="button" data-ch="ch-1"><b>פרק א׳</b> מתחברים לקלפלב<small>שלבים 1 עד 3</small></button>'
       '<button type="button" data-ch="ch-2"><b>פרק ב׳</b> מצטרפים למוסד<small>שלבים 4 עד 6</small></button>'
       '</nav>')

SUB = "מתחברים לקלפלב, ומשייכים את החשבון למוסד"

BODY = f'''<div class="wrap">
  <header class="hero">
    <div class="kicker">הדרכה צעד אחר צעד</div>
    <h1>הצטרפות למנוי בית-ספרי בקלפלב</h1>
    <p class="sub">{SUB}</p>
    {TOC}
    <p class="scope">לוחצים על פרק כדי להיכנס אליו. כבר מחוברים לקלפלב? מתחילים מפרק ב׳.</p>
  </header>

  <main>{chapter("ch-1", "פרק א׳", "מתחברים לקלפלב", CH1)}{chapter("ch-2", "פרק ב׳", "מצטרפים למוסד", CH2)}</main>
</div>'''

# כרטיס התצוגה לווטסאפ ולרשתות — התמונה קובץ נפרד, כי תמונה מוטמעת לא נקראת כתצוגה מקדימה.
URL = "https://neshamalevy-design.github.io/matia-guides/claplab/"
META = f'''<meta name="description" content="{SUB}">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="הצטרפות למנוי בית-ספרי בקלפלב">
<meta property="og:description" content="{SUB} — הדרכה צעד אחר צעד">
<meta property="og:image" content="{URL}preview.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">'''

html = (HERE / "guide-template.html").read_text(encoding="utf8")
html = html.replace("{{TITLE}}", "הצטרפות למנוי בית-ספרי בקלפלב").replace("{{BODY}}", BODY)
html = html.replace("</title>", "</title>\n" + META, 1)
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html, encoding="utf8")
print("נכתב:", OUT, f"({OUT.stat().st_size // 1024}KB)")
