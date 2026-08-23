# -*- coding: utf-8 -*-
import os, re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))

BLUE   = RGBColor(0x1F, 0x4E, 0x79)
DEEP   = RGBColor(0x12, 0x38, 0x5A)
ORANGE = RGBColor(0xD9, 0x57, 0x00)
GREY   = RGBColor(0x58, 0x65, 0x73)

doc = Document()
sec = doc.sections[0]
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = Cm(29.7), Cm(21)
for s in ("top", "bottom", "left", "right"):
    setattr(sec, s + "_margin", Cm(1.6))
CONTENT_W = 29.7 - 3.2

st = doc.styles["Normal"]
st.font.name = "Assistant"
st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn("w:cs"), "Assistant")
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Assistant")


def rtl_p(p):
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement("w:bidi")
    b.set(qn("w:val"), "1")
    pPr.append(b)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    return p


def mark_rtl(run, size=None, bold=None):
    """עברית ב-Word נשלטת ע\"י מאפייני הכתב המורכב (szCs/bCs), לא ע\"י sz/b."""
    rPr = run._element.get_or_add_rPr()
    e = OxmlElement("w:rtl")
    e.set(qn("w:val"), "1")
    rPr.append(e)
    if size is None and run.font.size is not None:
        size = run.font.size.pt
    if size is not None:
        sz = OxmlElement("w:szCs")
        sz.set(qn("w:val"), str(int(round(size * 2))))
        rPr.append(sz)
    if bold is None:
        bold = bool(run.font.bold)
    b = OxmlElement("w:bCs")
    b.set(qn("w:val"), "1" if bold else "0")
    rPr.append(b)
    rf = OxmlElement("w:rFonts")
    for a in ("w:cs", "w:ascii", "w:hAnsi"):
        rf.set(qn(a), "Assistant")
    rPr.insert(0, rf)


def add(text="", size=11, bold=False, color=None, space_before=0, space_after=4):
    p = doc.add_paragraph()
    rtl_p(p)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    for i, chunk in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if not chunk:
            continue
        r = p.add_run(chunk)
        r.font.size = Pt(size)
        r.font.bold = bold or (i % 2 == 1)
        if color is not None:
            r.font.color.rgb = color
        elif i % 2 == 1:
            r.font.color.rgb = DEEP
        mark_rtl(r)
    return p


def action(tag, text, hint=None):
    p = doc.add_paragraph()
    rtl_p(p)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(tag + "   ")
    r.font.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = ORANGE
    mark_rtl(r)
    for i, chunk in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if not chunk:
            continue
        rr = p.add_run(chunk)
        rr.font.size = Pt(11)
        rr.font.bold = i % 2 == 1
        if i % 2 == 1:
            rr.font.color.rgb = DEEP
        mark_rtl(rr)
    if hint:
        h = add(hint, size=9.5, color=GREY, space_after=5)
        h.paragraph_format.right_indent = Cm(0.9)


def picture(path, avail_h_cm):
    W, H = Image.open(path).size
    w_cm = min(CONTENT_W, avail_h_cm * W / H)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Cm(w_cm))


def caption(text):
    p = add(text, size=9, color=GREY, space_after=0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


TITLES = [
    "נכנסים ליומן",
    'פותחים את "הוסף לוח שנה"',
    "יוצרים לוח שנה ייעודי",
    "פותחים את מסך ההעלאה",
    "בוחרים את קובץ ה-ICS",
    "בוחרים לאיזה לוח להעלות",
    "מוסיפים ללוח השנה",
    "בודקים שהצליח",
]


def step_head(n, sub):
    p = doc.add_paragraph()
    rtl_p(p)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run("%d.  %s" % (n, TITLES[n - 1]))
    r.font.size = Pt(19)
    r.font.bold = True
    r.font.color.rgb = BLUE
    mark_rtl(r)
    add(sub, size=10, color=GREY, space_after=7)


# ---------- עמוד פתיחה ----------
add("העלאת יומן מקובץ ICS ליומן Outlook", size=27, bold=True, color=BLUE, space_after=5)
add(
    "שמונה שלבים, מהרגע שפותחים את Outlook ועד שהאירועים מופיעים ביומן — "
    "עם סימון מדויק של כל מקום שצריך ללחוץ עליו.",
    size=12.5, color=GREY, space_after=16,
)

add("לפני שמתחילים", size=14, bold=True, color=DEEP, space_after=5)
for b in [
    "קובץ **.ics** שמור על המחשב — בדרך כלל בתיקיית Downloads.",
    "Outlook פתוח (גרסת הדפדפן או אפליקציית שולחן העבודה — המסכים זהים).",
    "המדריך יוצר **לוח שנה נפרד** לאירועים החדשים, כדי שלא יתערבבו ביומן האישי.",
]:
    p = add("•   " + b, size=11, space_after=3)
    p.paragraph_format.right_indent = Cm(0.5)

add("", space_after=10)
add("שמונה השלבים", size=14, bold=True, color=DEEP, space_after=5)
for i, tt in enumerate(TITLES, 1):
    p = add("%d.   %s" % (i, tt), size=11, space_after=2)
    p.paragraph_format.right_indent = Cm(0.5)

QUOTE = chr(0x05F4)  # גרש כפול עברי

STEPS = [
    (1, "מעבר מתיבת הדואר אל אפליקציית היומן",
     [("1", "בסרגל האייקונים שבקצה **ימין** של החלון, לחצי על אייקון **היומן** — הריבוע הכחול עם הנקודות.",
       "הוא נמצא ישר מתחת לאייקון הדואר (המעטפה הכחולה).")],
     None, "מסך הדואר — אייקון היומן בסרגל הימני"),
    (2, "החלונית שממנה עושים את כל השאר",
     [("2", 'בסרגל הצדדי של היומן, מתחת ללוח החודשי, לחצי על **"הוסף לוח שנה"**.',
       "אם הסרגל סגור — לחצי על אייקון התפריט בפינה השמאלית העליונה כדי לפתוח אותו.")],
     None, "הסרגל הצדדי של היומן"),
    (3, "ארבע פעולות במסך אחד",
     [("3א", 'בתפריט הימני לחצי על **"צור לוח שנה ריק"**.', None),
      ("3ב", "הקלידי **שם** ללוח.",
       'שם שיהיה ברור בעוד חצי שנה — למשל "גאנט - תשפ' + QUOTE + 'ז", לא "יומן 2".'),
      ("3ג", "בחרי **צבע**.",
       "זה הצבע שכל האירועים יקבלו ביומן. שווה לבחור צבע שלא בשימוש כבר."),
      ("3ד", 'לחצי **"שמור"**.',
       'אפשר גם לבחור "קמע" (אייקון קטן) מהרשימה שבאמצע — לא חובה.')],
     "למה לא ישר ליומן הראשי? לוח נפרד אפשר להסתיר בלחיצה, לצבוע בצבע משלו, "
     "ולמחוק כולו בבת אחת אם התחרטת. ביומן הראשי האירועים מתערבבים ואי אפשר להפריד אותם בחזרה.",
     'מסך "צור לוח שנה ריק"'),
    (4, "חוזרים לאותה חלונית, לשורה אחרת בתפריט",
     [("4א", 'בתפריט הימני לחצי על **"העלה מקובץ"**.', None),
      ("4ב", 'לחצי על **"עיון"**.',
       "בצילום שדה הקובץ כבר מלא — אצלך הוא יהיה ריק בשלב הזה. זה בסדר.")],
     None, 'מסך "העלה מקובץ"'),
    (5, "חלון בחירת הקבצים של Windows",
     [("5א", "אתרי את קובץ ה-**.ics** ולחצי עליו פעם אחת.",
       'ברוב המקרים הוא בתיקיית Downloads, תחת "היום".'),
      ("5ב", "לחצי **Open**.", None)],
     None, "חלון בחירת הקבצים"),
    (6, "השלב שאסור לדלג עליו",
     [("6א", 'לחצי על השדה **"בחר לוח שנה"** כדי לפתוח את הרשימה.', None),
      ("6ב", "בחרי מהרשימה את **הלוח שיצרת בשלב 3**.",
       "בצילום מופיעים כמה לוחות קיימים — אצלך הלוח החדש יופיע ברשימה עם הצבע שבחרת לו.")],
     "שימי לב — אם לא תבחרי כאן לוח, האירועים ייכנסו ליומן הראשי, ואי אפשר להפריד אותם בחזרה.",
     "הרשימה הנפתחת של לוחות השנה"),
    (7, "הלחיצה שמבצעת את הייבוא",
     [("7", 'ודאי ששם הלוח הנכון מופיע בשדה, ולחצי על **"הוספה ללוח השנה"**.',
       'רוצה לראות מה נכנס לפני שמאשרים? לחצי קודם על "תצוגה מקדימה" שלידו.')],
     None, "הלוח נבחר — נשאר ללחוץ"),
    (8, "איך יודעים שהאירועים באמת נכנסו",
     [("8", 'חזרי ליומן. הלוח החדש מופיע ברשימה **"לוחות השנה שלי"** עם סימון, '
            "והאירועים מופיעים בצבע שבחרת.",
       "לא רואה אירועים? ודאי שהעיגול ליד שם הלוח מסומן, ועברי לחודש שבו האירועים אמורים להיות.")],
     None, "האירועים ביומן, והלוח החדש מסומן ברשימה"),
]

AVAIL = {1: 13.5, 2: 13.5, 3: 9.6, 4: 13.0, 5: 12.8, 6: 12.0, 7: 13.2, 8: 13.5}

for n, sub, acts, note, cap in STEPS:
    doc.add_page_break()
    step_head(n, sub)
    if note:
        col = ORANGE if n == 6 else DEEP
        p = add(note, size=10.5, color=col, space_after=6)
        p.paragraph_format.left_indent = Cm(0.3)
        p.paragraph_format.right_indent = Cm(0.3)
    for tag, text, hint in acts:
        action(tag, text, hint)
    picture("marked/mk-%d.png" % n, AVAIL[n])
    caption(cap)

doc.add_page_break()
add("אם משהו השתבש", size=20, bold=True, color=BLUE, space_after=3)
add("שלוש התקלות שחוזרות הכי הרבה — וכולן הפיכות.", size=11, color=GREY, space_after=12)
for h, b in [
    ("האירועים נכנסו ליומן הלא נכון",
     'אם הם נכנסו ללוח נפרד — לחצי ימני על שם הלוח ברשימה ובחרי "הסר". '
     "הכול נמחק בבת אחת, ואפשר להתחיל מחדש משלב 4."),
    ("לא רואים שום אירוע",
     "בדקי שהעיגול ליד שם הלוח מסומן — לוח לא מסומן פשוט מוסתר. "
     "אחר כך עברי לחודש שבו האירועים אמורים להיות."),
    ("אירועים כפולים",
     "סימן שהקובץ הועלה פעמיים. הסירי את הלוח כולו וחזרי על שלבים 3–7 פעם אחת."),
]:
    add(h, size=12, bold=True, color=DEEP, space_before=6, space_after=2)
    add(b, size=11, space_after=4)

out = "מדריך-העלאת-ICS-ל-Outlook.docx"
doc.save(out)
print("saved:", out, os.path.getsize(out), "bytes")
