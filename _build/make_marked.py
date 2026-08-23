# -*- coding: utf-8 -*-
"""
מייצר את marked/ — צילומי המסך עם ההדגשות "צרובות" לתוך התמונה.

למה צריך את זה: במדריך ה-HTML ההדגשות הן שכבת CSS מעל התמונה, ולכן הן
מתעדכנות ומתכווננות בקלות. אבל Word ו-PDF לא יודעים לשאת שכבה כזו, אז
לגרסאות האלה מרנדרים כל צילום עם ההדגשה שלו ושומרים כתמונה אחת.

הקלט:  print-layout.html (מגדיר את מיקומי ההדגשות) + img/
הפלט:  marked/mk-1.png ... mk-8.png  (ברזולוציה כפולה)

דרוש Edge מותקן. הרצה:  python make_marked.py
"""
import base64
import io
import os
import re
import subprocess
import sys
from urllib.request import pathname2url

from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
PAD = 46          # שוליים סביב הצילום, כדי שתגיות המספור לא ייחתכו
SCALE = 2         # רזולוציה כפולה — נראה חד גם כשמוטמע ב-Word


def find_edge():
    for p in EDGE_CANDIDATES:
        if os.path.isfile(p):
            return p
    sys.exit("לא נמצא Edge. עדכני את EDGE_CANDIDATES בראש הקובץ.")


def extract_frames(html):
    """שולף כל <div class="frame"> שלם מקובץ הפריסה, כולל ההדגשות שבתוכו."""
    out = []
    for m in re.finditer(r'<div class="frame" id="f(\d+)" style="max-width:\d+px">', html):
        start, depth, i = m.start(), 0, m.start()
        while True:
            candidates = [x for x in (html.find("<div", i + 1), html.find("</div>", i + 1)) if x > 0]
            nxt = min(candidates)
            if html.startswith("<div", nxt):
                depth += 1
            else:
                if depth == 0:
                    end = nxt + 6
                    break
                depth -= 1
            i = nxt
        out.append((int(m.group(1)), html[start:end]))
    return out


def main():
    edge = find_edge()
    html = io.open("print-layout.html", encoding="utf-8").read()
    css = re.search(r"<style>(.*?)@page", html, re.S).group(1)
    frames = extract_frames(html)
    if not frames:
        sys.exit("לא נמצאו frames ב-print-layout.html")

    os.makedirs("marked", exist_ok=True)
    for fid, frag in frames:
        src = re.search(r'src="(img/step-\d+\.png)"', frag).group(1)
        w, h = Image.open(src).size
        data = base64.b64encode(open(src, "rb").read()).decode()

        frag = re.sub(r'src="img/step-\d+\.png"', 'src="data:image/png;base64,%s"' % data, frag)
        frag = re.sub(r'style="max-width:\d+px"', 'style="max-width:%dpx"' % w, frag)

        tmp = "_mk%d.html" % fid
        io.open(tmp, "w", encoding="utf-8").write(
            '<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
            '<link href="https://fonts.googleapis.com/css2?'
            'family=Assistant:wght@400;600;700;800&display=swap" rel="stylesheet">'
            "<style>%s\nhtml,body{margin:0;padding:0;background:#fff}"
            "body{padding:%dpx}.frame{margin:0!important}</style>"
            "</head><body>%s</body></html>" % (css, PAD, frag)
        )

        url = "file:///" + pathname2url(os.path.abspath(tmp)).lstrip("/")
        out = os.path.abspath(os.path.join("marked", "mk-%d.png" % fid))
        subprocess.run(
            [edge, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=%d" % SCALE,
             "--window-size=%d,%d" % (w + PAD * 2, h + PAD * 2),
             "--virtual-time-budget=5000", "--screenshot=" + out, url],
            capture_output=True,
        )
        os.remove(tmp)
        print("mk-%d.png  <- %s  (%dx%d)" % (fid, src, w, h))

    print("\nנוצרו %d צילומים ב-marked/" % len(frames))


if __name__ == "__main__":
    main()
