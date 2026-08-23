# -*- coding: utf-8 -*-
"""בונה את מדריך ה-ICS כאקורדיון רספונסיבי, קובץ HTML יחיד עם תמונות מוטמעות."""
import os, base64, io
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def b64(p):
    return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()

IMG = {n: "img/step-%02d.png" % n for n in range(1, 8)}
DIM = {n: Image.open(p).size for n, p in IMG.items()}
SRC = {n: b64(p) for n, p in IMG.items()}

# (left, top, width, height, badge-position, label)
STEPS = [
    dict(n=1, img=1, title="נכנסים ליומן", sub="מעבר מתיבת הדואר אל אפליקציית היומן",
         cap="מסך הדואר — אייקון היומן בסרגל הימני",
         acts=[("1",
                'בסרגל האייקונים שבקצה <b>ימין</b> של החלון, לחצי על אייקון <b>היומן</b> — הריבוע הכחול עם הנקודות.',
                "הוא נמצא ישר מתחת לאייקון הדואר (המעטפה הכחולה).")],
         mk=[("93.6", "17.4", "5.3", "7.7", "out-s", "1", "circle")]),

    dict(n=2, img=2, title='פותחים את "הוסף לוח שנה"', sub="החלונית שממנה עושים את כל השאר",
         cap="הסרגל הצדדי של היומן",
         acts=[("2",
                'בסרגל הצדדי של היומן, מתחת ללוח החודשי, לחצי על <b>"הוסף לוח שנה"</b>.',
                "אם הסרגל סגור — לחצי על אייקון התפריט (☰) בפינה השמאלית העליונה כדי לפתוח אותו.")],
         mk=[("52.6", "35.6", "32.2", "5.1", "bl", "2", "")]),

    dict(n=3, img=3, title="יוצרים לוח שנה ייעודי", sub="ארבע פעולות במסך אחד",
         cap='מסך "צור לוח שנה ריק"',
         why='<b>למה לא ישר ליומן הראשי?</b> לוח נפרד אפשר להסתיר בלחיצה, לצבוע בצבע משלו, '
             'ולמחוק כולו בבת אחת אם התחרטת. ביומן הראשי האירועים מתערבבים ואי אפשר להפריד אותם בחזרה.',
         acts=[("3א", 'בתפריט הימני לחצי על <b>"צור לוח שנה ריק"</b>.', None),
               ("3ב", "הקלידי <b>שם</b> ללוח.",
                'שם שיהיה ברור בעוד חצי שנה — למשל "גאנט - תשפ״ז", לא "יומן 2".'),
               ("3ג", "בחרי <b>צבע</b>.",
                "זה הצבע שכל האירועים יקבלו ביומן. שווה לבחור צבע שלא בשימוש כבר."),
               ("3ד", 'לחצי <b>"שמור"</b>.',
                'אפשר גם לבחור "קמע" (אייקון קטן) מהרשימה שבאמצע — לא חובה.')],
         mk=[("82.2", "29.73", "17.8", "6.32", "tl", "3א", ""),
             ("49.0", "18.09", "32.4", "6.07", "tl", "3ב", ""),
             ("47.4", "32.58", "33.8", "5.70", "tl", "3ג", ""),
             ("74.2", "89.19", "7.2", "5.82", "out-e", "3ד", "")]),

    dict(n=4, img=4, title="פותחים את מסך ההעלאה", sub="חוזרים לאותה חלונית, לשורה אחרת בתפריט",
         cap='מסך "העלה מקובץ"',
         acts=[("4א", 'בתפריט הימני לחצי על <b>"העלה מקובץ"</b>.', None),
               ("4ב", 'לחצי על <b>"עיון"</b>.',
                "בצילום שדה הקובץ כבר מלא — אצלך הוא יהיה ריק בשלב הזה. זה בסדר.")],
         mk=[("82.8", "58.98", "17.2", "7.18", "tl", "4א", ""),
             ("41.9", "21.53", "7.2", "6.46", "tl", "4ב", "")]),

    dict(n=5, img=5, title="בוחרים את קובץ ה-ICS", sub="חלון בחירת הקבצים של Windows",
         cap="חלון בחירת הקבצים",
         acts=[("5א", 'אתרי את קובץ ה-<code>.ics</code> ולחצי עליו פעם אחת.',
                'ברוב המקרים הוא בתיקיית <b>Downloads</b>, תחת "היום".'),
               ("5ב", "לחצי <kbd>Open</kbd>.", None)],
         mk=[("30.4", "16.2", "21.8", "38.4", "tr", "5א", ""),
             ("82.5", "92.9", "6.6", "4.2", "out-s", "5ב", "")]),

    dict(n=6, img=4, title="בוחרים לאיזה לוח להעלות", sub="השלב שאסור לדלג עליו",
         cap="הרשימה הנפתחת של לוחות השנה",
         alert="אם לא תבחרי כאן לוח — האירועים ייכנסו ליומן הראשי, ואי אפשר להפריד אותם בחזרה.",
         acts=[("6א", 'לחצי על השדה <b>"בחר לוח שנה"</b> כדי לפתוח את הרשימה.', None),
               ("6ב", "בחרי מהרשימה את <b>הלוח שיצרת בשלב 3</b>.",
                "בצילום מופיעים כמה לוחות קיימים — אצלך הלוח החדש יופיע ברשימה עם הצבע שבחרת לו.")],
         mk=[("49.6", "31.57", "32.2", "6.46", "out-e", "6א", ""),
             ("49.8", "56.54", "32.0", "6.46", "out-e", "6ב", "")]),

    dict(n=7, img=6, title="מוסיפים ללוח השנה", sub="הלחיצה שמבצעת את הייבוא",
         cap="הלוח נבחר — נשאר ללחוץ",
         acts=[("7", 'ודאי ששם הלוח הנכון מופיע בשדה, ולחצי על <b>"הוספה ללוח השנה"</b>.',
                'רוצה לראות מה נכנס לפני שמאשרים? לחצי קודם על "תצוגה מקדימה" שלידו.')],
         mk=[("69.0", "41.48", "13.2", "6.51", "tl", "7", "")]),

    dict(n=8, img=7, title="בודקים שהצליח", sub="איך יודעים שהאירועים באמת נכנסו",
         cap="האירועים ביומן, והלוח החדש מסומן ברשימה",
         acts=[("8", 'חזרי ליומן. הלוח החדש מופיע ברשימה <b>"לוחות השנה שלי"</b> עם סימון ✓, '
                     "והאירועים מופיעים בצבע שבחרת.",
                "לא רואה אירועים? ודאי שהעיגול ליד שם הלוח מסומן, ועברי לחודש שבו האירועים אמורים להיות.")],
         mk=[("90.2", "67.2", "9.1", "4.5", "out-s", "8", "")]),
]

CSS = r"""
:root{
  --ink:#1B2430; --ink-soft:#55626F; --ink-faint:#8A96A3;
  --bg:#F5F8FB; --surface:#FFFFFF; --line:#E1E8F0;
  --brand:#1F4E79; --brand-deep:#12385A; --brand-tint:#E8F0F8;
  --mark:#FF6A00; --mark-glow:255,106,0;
  --warn:#A8560B; --warn-bg:#FEF6E7; --warn-line:#F0D9A8;
  --sh:27,36,48;
}
*{box-sizing:border-box}
html,body{overflow-x:hidden; max-width:100%}
html{scroll-behavior:smooth; -webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:"Assistant",-apple-system,Segoe UI,Arial,sans-serif;
  font-size:17px; line-height:1.6; letter-spacing:-0.01em;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1080px; margin:0 auto; padding:0 18px 60px}

/* ---------- כותרת ---------- */
.hero{
  margin-top:18px; padding:26px 28px 24px;
  background:linear-gradient(155deg,var(--brand-deep),var(--brand));
  color:#fff; border-radius:18px; position:relative; overflow:hidden;
  box-shadow:0 14px 32px -16px rgba(var(--sh),.5);
}
.hero::after{content:""; position:absolute; inset:auto -70px -120px auto;
  width:280px; height:280px; border-radius:50%; background:rgba(255,255,255,.05)}
.hero .kicker{font-size:11.5px; font-weight:700; letter-spacing:.1em;
  text-transform:uppercase; opacity:.7; margin:0 0 8px}
.hero h1{margin:0; font-size:27px; line-height:1.2; font-weight:800; letter-spacing:-0.02em}
.hero p{margin:9px 0 0; font-size:15.5px; opacity:.9; max-width:56ch}

/* ---------- לפני שמתחילים ---------- */
.pre{
  margin-top:14px; background:var(--surface); border:1px solid var(--line);
  border-radius:13px; padding:15px 18px;
  box-shadow:0 6px 18px -14px rgba(var(--sh),.4);
}
.pre h2{margin:0 0 7px; font-size:15px; font-weight:700; color:var(--brand-deep)}
.pre ul{margin:0; padding-inline-start:19px; color:var(--ink-soft); font-size:15px}
.pre li{margin:4px 0}
code{background:var(--brand-tint); color:var(--brand-deep); padding:1px 6px;
  border-radius:5px; font-family:inherit; font-weight:600; font-size:.94em}
kbd{font-family:inherit; font-weight:700; font-size:.92em; background:var(--ink);
  color:#fff; padding:1px 8px; border-radius:5px}

/* ---------- מד התקדמות ---------- */
.bar{display:flex; align-items:center; gap:10px; margin:18px 2px 9px}
.bar .lbl{font-size:12.5px; font-weight:700; color:var(--ink-faint);
  letter-spacing:.04em; white-space:nowrap}
.bar .track{flex:1; height:5px; background:var(--line); border-radius:99px; overflow:hidden}
.bar .fill{height:100%; width:0; background:var(--brand); border-radius:99px; transition:width .3s ease}

/* ---------- אקורדיון ---------- */
.steps{display:flex; flex-direction:column; gap:9px}
.step{
  background:var(--surface); border:1px solid var(--line); border-radius:14px;
  box-shadow:0 5px 16px -12px rgba(var(--sh),.4);
  scroll-margin-top:12px; overflow:hidden; transition:box-shadow .2s, border-color .2s;
}
.step.open{border-color:#C4D6E8; box-shadow:0 12px 30px -16px rgba(var(--sh),.45)}

.head{
  width:100%; margin:0; border:0; background:transparent; cursor:pointer;
  font:inherit; color:inherit; text-align:start;
  display:flex; align-items:center; gap:13px; padding:13px 15px;
  -webkit-tap-highlight-color:transparent;
}
.head:hover{background:var(--brand-tint)}
.head:focus-visible{outline:3px solid var(--brand); outline-offset:-3px}
.num{
  flex:0 0 36px; height:36px; border-radius:11px;
  background:var(--brand-tint); color:var(--brand-deep);
  display:grid; place-items:center; font-weight:800; font-size:17px;
  transition:background .2s, color .2s;
}
.step.open .num{background:var(--brand); color:#fff}
.step.done .num{background:#DCEBDD; color:#2E6B36}
.ttl{flex:1; min-width:0}
.ttl b{display:block; font-size:16.5px; font-weight:700; letter-spacing:-0.01em}
.ttl small{display:block; font-size:13px; color:var(--ink-faint); font-weight:400; margin-top:1px}
.chev{
  flex:0 0 auto; width:26px; height:26px; display:grid; place-items:center;
  color:var(--ink-faint); font-size:19px; line-height:1;
  transition:transform .25s ease; transform:rotate(90deg);
}
.step.open .chev{transform:rotate(-90deg); color:var(--brand)}

.body{display:none; border-top:1px solid var(--line)}
.step.open .body{display:block}

/* ---------- פעולות ---------- */
.acts{padding:15px 16px 4px}
.acts ol{list-style:none; margin:0; padding:0}
.acts li{display:flex; gap:11px; margin:0 0 13px}
.tag{
  flex:0 0 auto; min-width:36px; height:27px; padding:0 8px; border-radius:8px;
  background:var(--mark); color:#fff; display:grid; place-items:center;
  font-weight:800; font-size:14.5px; box-shadow:0 3px 8px -3px rgba(var(--mark-glow),.7);
}
.acts b{font-weight:700; color:var(--brand-deep)}
.hint{margin-top:5px; font-size:14px; color:var(--ink-soft);
  border-inline-start:3px solid var(--line); padding-inline-start:10px}
.why{background:var(--brand-tint); border-radius:10px; padding:11px 14px;
  font-size:14.5px; color:var(--brand-deep); margin:0 0 13px}
.alert{background:var(--warn-bg); border:1px solid var(--warn-line); border-radius:10px;
  padding:11px 14px; font-size:14.5px; color:var(--warn); margin:0 0 13px; font-weight:600}

/* ---------- צילום ---------- */
.shot{margin:0; padding:6px 16px 14px}
.shot > div{width:auto; max-width:100%; margin:0 auto}
.frame{
  position:relative; display:block; width:100%; margin:0 auto; cursor:zoom-in;
  border-radius:9px; box-shadow:0 10px 26px -16px rgba(var(--sh),.55);
}
.frame img{display:block; width:100%; height:auto; border-radius:9px; border:1px solid var(--line)}
.mk{
  position:absolute; box-sizing:border-box; pointer-events:none;
  border:3px solid var(--mark); border-radius:7px;
  box-shadow:0 0 0 3px rgba(var(--mark-glow),.2), 0 0 14px rgba(var(--mark-glow),.42);
}
.mk.circle{border-radius:50%}
.mk .lbl{
  position:absolute; min-width:30px; height:25px; padding:0 8px;
  background:var(--mark); color:#fff; border-radius:7px;
  font-weight:800; font-size:14px; line-height:25px; text-align:center; white-space:nowrap;
  box-shadow:0 3px 9px -2px rgba(var(--mark-glow),.85), 0 0 0 2px #fff;
}
.lbl.tl{bottom:calc(100% + 5px); inset-inline-start:-3px}
.lbl.tr{bottom:calc(100% + 5px); inset-inline-end:-3px}
.lbl.bl{top:calc(100% + 5px); inset-inline-start:-3px}
.lbl.out-s{top:50%; transform:translateY(-50%); inset-inline-start:calc(100% + 9px)}
.lbl.out-e{top:50%; transform:translateY(-50%); inset-inline-end:calc(100% + 9px)}

.caption{margin-top:9px; font-size:12.5px; color:var(--ink-faint); text-align:center}
.tapzoom{display:none}

/* ---------- ניווט בין שלבים ---------- */
.nav{display:flex; gap:9px; padding:0 16px 15px}
.nav button{
  font:inherit; font-weight:700; font-size:14.5px; cursor:pointer;
  border-radius:10px; padding:9px 16px; transition:.15s;
  -webkit-tap-highlight-color:transparent;
}
.nav .next{flex:1; background:var(--brand); color:#fff; border:1px solid var(--brand)}
.nav .next:hover{background:var(--brand-deep)}
.nav .prev{background:var(--surface); color:var(--ink-soft); border:1px solid var(--line)}
.nav .prev:hover{border-color:var(--brand); color:var(--brand)}

/* ---------- סיום ---------- */
.outro{margin-top:20px; background:var(--surface); border:1px solid var(--line);
  border-radius:16px; padding:20px 22px; box-shadow:0 10px 26px -18px rgba(var(--sh),.45)}
.outro h2{margin:0 0 4px; font-size:20px; font-weight:800; letter-spacing:-0.02em}
.outro > p{margin:0 0 15px; color:var(--ink-soft); font-size:15px}
.faq{display:grid; gap:11px; grid-template-columns:repeat(auto-fit,minmax(255px,1fr))}
.faq div{background:var(--bg); border:1px solid var(--line); border-radius:11px; padding:13px 15px}
.faq h4{margin:0 0 4px; font-size:15px; font-weight:700; color:var(--brand-deep)}
.faq p{margin:0; font-size:14.5px; color:var(--ink-soft)}
.sign{margin-top:22px; text-align:center; font-size:12.5px; color:var(--ink-faint)}

/* ---------- תצוגה מוגדלת ---------- */
.lb{
  position:fixed; top:0; inset-inline:0; z-index:200; display:none;
  width:100%; height:100vh; height:100dvh;
  background:rgba(12,22,34,.94); overscroll-behavior:contain;
}
.lb.on{display:block}
/* margin:auto ולא justify-content — אחרת תוכן רחב מהמסך נחתך ולא נגלל */
.lb .pane{position:absolute; inset:0; overflow:auto; -webkit-overflow-scrolling:touch;
  display:flex; padding:52px 10px 24px}
.lb .inner{position:relative; flex:0 0 auto; margin:auto}
.lb img{display:block; height:auto; border-radius:6px; background:#fff}
.lb .mk{border-width:3px}
.lb .close{
  position:absolute; top:10px; inset-inline-end:12px; z-index:2;
  width:40px; height:40px; border-radius:50%; border:0; cursor:pointer;
  background:rgba(255,255,255,.16); color:#fff; font-size:23px; line-height:1;
  display:grid; place-items:center; backdrop-filter:blur(6px);
}
.lb .close:hover{background:rgba(255,255,255,.3)}
.lb .tip{
  position:absolute; top:16px; inset-inline-start:14px; z-index:2;
  color:#fff; opacity:.75; font-size:13px; font-weight:600;
}

/* ================= נייד ================= */
@media (max-width:760px){
  body{font-size:16px}
  .wrap{padding:0 12px 46px}
  .hero{margin-top:12px; padding:20px 20px 18px; border-radius:15px}
  .hero h1{font-size:22px}
  .hero p{font-size:14.5px}
  .pre{padding:13px 15px}
  .head{padding:11px 12px; gap:11px}
  .num{flex-basis:32px; height:32px; font-size:15.5px; border-radius:10px}
  .ttl b{font-size:15.5px}
  .ttl small{font-size:12.5px}
  .acts{padding:13px 13px 2px}
  .acts li{gap:9px; margin-bottom:11px}
  .tag{min-width:33px; height:25px; font-size:13.5px}
  .hint{font-size:13.5px}
  .shot{padding:4px 12px 12px}
  /* הצילום קטן מכדי לקרוא — ההדגשות מתעדנות והלחיצה מגדילה */
  .mk{border-width:2px; border-radius:5px;
      box-shadow:0 0 0 2px rgba(var(--mark-glow),.22), 0 0 9px rgba(var(--mark-glow),.5)}
  .mk .lbl{min-width:20px; height:17px; padding:0 5px; font-size:10.5px;
           line-height:17px; border-radius:5px; box-shadow:0 2px 5px -1px rgba(var(--mark-glow),.85), 0 0 0 1.5px #fff}
  .lbl.tl,.lbl.tr{bottom:calc(100% + 3px)}
  .lbl.bl{top:calc(100% + 3px)}
  .lbl.out-s{inset-inline-start:calc(100% + 5px)}
  .lbl.out-e{inset-inline-end:calc(100% + 5px)}
  .tapzoom{
    display:flex; align-items:center; justify-content:center; gap:6px;
    margin-top:7px; font-size:13px; font-weight:700; color:var(--brand);
    background:var(--brand-tint); border-radius:8px; padding:7px 10px;
  }
  .caption{margin-top:6px; font-size:12px}
  .nav{padding:0 13px 13px}
  .nav button{font-size:14px; padding:10px 14px}
  .outro{padding:17px 16px}
  .lb .pane{padding:48px 6px 18px}
}

@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{transition-duration:.01ms !important; animation-duration:.01ms !important}
}

/* ---------- הדפסה ---------- */
@media print{
  .bar,.nav,.chev,.tapzoom,.lb{display:none !important}
  .body{display:block !important}
  .step{break-inside:avoid; box-shadow:none; margin-bottom:8px}
  body{background:#fff}
  *{-webkit-print-color-adjust:exact; print-color-adjust:exact}
}
"""

JS = r"""
(function(){
  var steps = Array.prototype.slice.call(document.querySelectorAll('.step'));
  var fill  = document.querySelector('.bar .fill');
  var label = document.querySelector('.bar .lbl');
  var TOTAL = steps.length;

  function render(){
    var openIdx = steps.findIndex(function(s){ return s.classList.contains('open'); });
    steps.forEach(function(s,i){
      s.querySelector('.head').setAttribute('aria-expanded', s.classList.contains('open'));
      s.classList.toggle('done', openIdx > -1 && i < openIdx);
    });
    var pos = openIdx > -1 ? openIdx + 1 : 0;
    fill.style.width = (pos / TOTAL * 100) + '%';
    label.textContent = pos ? ('שלב ' + pos + ' מתוך ' + TOTAL) : ('שמונה שלבים');
  }

  function open(i, scroll){
    steps.forEach(function(s,j){ s.classList.toggle('open', j === i); });
    render();
    if (scroll !== false){
      var el = steps[i];
      requestAnimationFrame(function(){
        var y = el.getBoundingClientRect().top + window.pageYOffset - 10;
        var smooth = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        window.scrollTo({ top:y, behavior: smooth ? 'smooth' : 'auto' });
      });
    }
  }

  steps.forEach(function(s,i){
    s.querySelector('.head').addEventListener('click', function(){
      if (s.classList.contains('open')){ s.classList.remove('open'); render(); }
      else open(i);
    });
  });
  document.querySelectorAll('[data-go]').forEach(function(b){
    b.addEventListener('click', function(){ open(parseInt(b.dataset.go,10), true); });
  });
  /* בשלב האחרון: סוגרים הכל וחוזרים לרשימה */
  document.querySelectorAll('[data-done]').forEach(function(b){
    b.addEventListener('click', function(){
      steps.forEach(function(s){ s.classList.remove('open'); });
      render();
      var smooth = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      var y = document.querySelector('.steps').getBoundingClientRect().top + window.pageYOffset - 10;
      window.scrollTo({ top:y, behavior: smooth ? 'smooth' : 'auto' });
    });
  });

  /* ---- תצוגה מוגדלת ---- */
  var lb    = document.querySelector('.lb');
  var inner = lb.querySelector('.inner');
  function showLB(frame){
    inner.innerHTML = frame.innerHTML;
    var img = inner.querySelector('img');
    img.style.width = frame.querySelector('img').naturalWidth + 'px';
    img.style.maxWidth = 'none';
    lb.classList.add('on');
    document.body.style.overflow = 'hidden';
    /* נפתח ממורכז על הסימון, כדי שלא יצטרכו לחפש אותו בגלילה */
    requestAnimationFrame(function(){
      var mk = inner.querySelector('.mk');
      if (mk && mk.scrollIntoView) mk.scrollIntoView({block:'center', inline:'center'});
    });
  }
  function hideLB(){ lb.classList.remove('on'); document.body.style.overflow=''; inner.innerHTML=''; }
  document.querySelectorAll('.frame').forEach(function(f){
    f.addEventListener('click', function(){ showLB(f); });
  });
  lb.querySelector('.close').addEventListener('click', hideLB);
  lb.querySelector('.pane').addEventListener('click', function(e){
    if (e.target === this || e.target.classList.contains('inner')) hideLB();
  });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape') hideLB(); });

  /* קישור ישיר לשלב: ‎#s3‎ */
  var m = (location.hash||'').match(/^#s([1-8])$/);
  open(m ? parseInt(m[1],10)-1 : 0, false);
  if (m) requestAnimationFrame(function(){
    steps[parseInt(m[1],10)-1].scrollIntoView({block:'start'});
  });
})();
"""

def mk_html(m):
    l, t, w, h, pos, lab, shape = m
    cls = "mk circle" if shape else "mk"
    return ('<div class="%s" style="left:%s%%;top:%s%%;width:%s%%;height:%s%%">'
            '<span class="lbl %s">%s</span></div>') % (cls, l, t, w, h, pos, lab)

def act_html(tag, text, hint):
    h = '<div class="hint">%s</div>' % hint if hint else ""
    return ('<li><span class="tag">%s</span><div class="txt">%s%s</div></li>'
            % (tag, text, h))

parts = []
for s in STEPS:
    n = s["n"]; W, H = DIM[s["img"]]
    notes = ""
    if s.get("why"):   notes += '<p class="why">%s</p>' % s["why"]
    if s.get("alert"): notes += '<p class="alert">⚠️ %s</p>' % s["alert"]
    acts = "".join(act_html(*a) for a in s["acts"])
    mks  = "".join(mk_html(m) for m in s["mk"])
    prev = ('<button class="prev" data-go="%d">‹ השלב הקודם</button>' % (n - 2)) if n > 1 else ""
    nxt  = ('<button class="next" data-go="%d">השלב הבא ›</button>' % n) if n < 8 else \
           '<button class="next" data-done="1">סיימתי ✓</button>'
    parts.append(f"""
  <section class="step" id="s{n}">
    <button class="head" aria-expanded="false" aria-controls="b{n}">
      <span class="num">{n}</span>
      <span class="ttl"><b>{s['title']}</b><small>{s['sub']}</small></span>
      <span class="chev">›</span>
    </button>
    <div class="body" id="b{n}">
      <div class="acts">{notes}<ol>{acts}</ol></div>
      <figure class="shot"><div>
        <div class="frame" style="max-width:{W}px">
          <img src="{SRC[s['img']]}" alt="{s['cap']}" width="{W}" height="{H}">
          {mks}
        </div>
        <div class="tapzoom">🔍 הקישי על התמונה כדי להגדיל</div>
        <figcaption class="caption">{s['cap']}</figcaption>
      </div></figure>
      <div class="nav">{nxt}{prev}</div>
    </div>
  </section>""")

HTML = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#1F4E79">
<title>מדריך ICS ל-Outlook</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">

  <header class="hero">
    <p class="kicker">מדריך הפעלה</p>
    <h1>העלאת יומן מקובץ ICS ליומן Outlook</h1>
    <p>שמונה שלבים, מהרגע שפותחים את Outlook ועד שהאירועים מופיעים ביומן. הקישי על שלב כדי לפתוח אותו.</p>
  </header>

  <section class="pre">
    <h2>לפני שמתחילים</h2>
    <ul>
      <li>קובץ <code>.ics</code> שמור על המחשב — בדרך כלל בתיקיית <code>Downloads</code>.</li>
      <li>Outlook פתוח — גרסת הדפדפן או אפליקציית שולחן העבודה, המסכים זהים.</li>
      <li>המדריך יוצר <b>לוח שנה נפרד</b>, כדי שהאירועים לא יתערבבו ביומן האישי.</li>
    </ul>
  </section>

  <div class="bar">
    <span class="lbl">שמונה שלבים</span>
    <span class="track"><span class="fill"></span></span>
  </div>

  <div class="steps">{''.join(parts)}
  </div>

  <section class="outro">
    <h2>אם משהו השתבש</h2>
    <p>שלוש התקלות שחוזרות הכי הרבה — וכולן הפיכות.</p>
    <div class="faq">
      <div><h4>האירועים נכנסו ליומן הלא נכון</h4>
        <p>אם הם נכנסו ללוח נפרד — לחצי ימני על שם הלוח ברשימה ובחרי "הסר". הכול נמחק בבת אחת, ואפשר להתחיל מחדש משלב 4.</p></div>
      <div><h4>לא רואים שום אירוע</h4>
        <p>בדקי שהעיגול ליד שם הלוח מסומן — לוח לא מסומן פשוט מוסתר. אחר כך עברי לחודש שבו האירועים אמורים להיות.</p></div>
      <div><h4>אירועים כפולים</h4>
        <p>סימן שהקובץ הועלה פעמיים. הסירי את הלוח כולו וחזרי על שלבים 3–7 פעם אחת.</p></div>
    </div>
  </section>

  <p class="sign">מדריך פנימי · העלאת קובץ ICS ליומן Outlook</p>
</div>

<div class="lb" role="dialog" aria-modal="true" aria-label="תצוגה מוגדלת">
  <span class="tip">אפשר לגלול ולהגדיל</span>
  <button class="close" aria-label="סגירה">✕</button>
  <div class="pane"><div class="inner"></div></div>
</div>

<script>{JS}</script>
</body>
</html>
"""

out = os.path.join("..", "ics-outlook", "index.html")
io.open(out, "w", encoding="utf-8").write(HTML)
print("saved:", out, "%.2f MB" % (len(HTML.encode("utf-8")) / 1048576))
