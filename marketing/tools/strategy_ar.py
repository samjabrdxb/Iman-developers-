"""Arabic sales strategy brochure: "الفخامة بسعر في المتناول، الجودة قبل الكمية" (right to left).

Usage:  python3 marketing/tools/strategy_ar.py

Writes marketing/japan/iman-sales-strategy-ar.pdf (A4 portrait, 2 pages): the
Arabic twin of the English, French and Japanese strategy brochures, same layout
and numbers. Downloads IBM Plex Sans Arabic once into /tmp/iman-fonts-ar.
"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from japan_brochure import qr, src, e, WA, FINDER, REPO, P
from japan_strategy import CSS, LAUNCHED, DELIVERED, DEC_2026, PIPELINE
from playwright.sync_api import sync_playwright

OUT = os.path.join(REPO, "marketing", "japan", "iman-sales-strategy-ar.pdf")
FONTS = "/tmp/iman-fonts-ar"


def fonts_css():
    """IBM Plex Sans Arabic as local woff2 files (Chromium prints from file://, without the network)."""
    css_path = os.path.join(FONTS, "ar.css")
    if not os.path.exists(css_path):
        os.makedirs(FONTS, exist_ok=True)
        ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        css = subprocess.run(["curl", "-sS", "-A", ua, "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;700&display=swap"],
                             check=True, capture_output=True, text=True).stdout
        urls = sorted(set(re.findall(r"url\((https://[^)]+)\)", css)))
        jobs = "".join(f'url = "{u}"\noutput = "{FONTS}/{i}.woff2"\n' for i, u in enumerate(urls))
        subprocess.run(["curl", "-sS", "--parallel", "--parallel-max", "16", "-K", "-"], input=jobs, text=True, check=True)
        for i, u in enumerate(urls):
            css = css.replace(u, f"file://{FONTS}/{i}.woff2")
        open(css_path, "w").write(css)
    return open(css_path).read()


def quote(x):
    return f"<blockquote>{e(x)}</blockquote>"


def foot(n):
    return f"""<div class=foot><span>سام جبر · مدير مبيعات أول · إيمان للتطوير العقاري · واتساب <bdi dir=ltr>+971 50 175 2771</bdi></span><span>{n} / 2</span></div>"""


compare = [("سعر الدخول", "السعر الفعلي مقارنةً بالمشاريع المماثلة"), ("مخطط الشقة", "الاستفادة العملية من المساحة والمخطط"),
           ("ارتفاع السقف", "المواصفات الفعلية المعتمدة"), ("الردهة والمناطق المشتركة", "جودة التصميم والتشطيب"),
           ("المرافق", "الجودة والعدد والتنوع"), ("عدد الوحدات", "الكثافة السكنية وتجربة السكن"),
           ("سجل التسليم", "المشاريع المنجزة والمسلّمة"), ("خطة الدفع", "الأقساط ومراحل البناء"),
           ("إمكانية إعادة البيع", "الصفقات السابقة والبيانات المقارنة")]

p1 = f"""<section class=page>
 <div class=top><div class=tl><div class=logo dir=ltr>IMAN<small>DEVELOPERS</small></div>
   <div class=eb>استراتيجية البيع للوسطاء اليابانيين والمستثمرين الدوليين</div>
   <h1>الفخامة بسعر في المتناول.<br>الجودة قبل الكمية.</h1>
   <p class=tp>وحدات أقل. مرافق أكثر. عناية أكبر بالتفاصيل. أسعار دخول تنافسية.</p></div>
  <div class=ti style="background-image:url('{src(P['oxford-212']['image'])}')"><span>Oxford 212 · مشروع مُسلَّم</span></div></div>

 <div class=stats><div><b>{LAUNCHED}</b><span>مشروعاً تم إطلاقه</span></div><div><b>{DELIVERED}</b><span>مشاريع مُسلَّمة</span></div>
  <div><b><bdi dir=ltr>+{DEC_2026}</bdi></b><span>تسليم متوقع في ديسمبر 2026</span></div><div><b>{DELIVERED + DEC_2026}</b><span>مشروعاً مُسلَّماً بنهاية 2026 (متوقع)</span></div></div>

 <div class=cols>
  <div><h3 class=sh>1. بِع فلسفة المطوّر، لا الشقة فقط</h3>
   <p>إيمان للتطوير العقاري مطوّر بوتيكي يضع الجودة قبل الكمية. فبدلاً من تسليم آلاف الوحدات، تركّز إيمان على عدد محدود من المشاريع السكنية المصمّمة بعناية، ما يجعلها خياراً جذاباً للمستثمر الذي يبحث عن منتج سكني راقٍ دون دخول شريحة الفخامة الفائقة.</p></div>
  <div><h3 class=sh>2. استخدم سجل التسليم لبناء الثقة</h3>
   <p>بالنسبة للمشتري الدولي، خاصةً من يشتري عن بُعد، يُعدّ سجل تسليم المطوّر أمراً أساسياً. فالمباني المنجزة تتيح له تقييم جودة التشطيب والمناطق المشتركة والمرافق على أرض الواقع.</p>
   {quote("مع إيمان للتطوير العقاري، أنت لا تستثمر بناءً على التصاميم المعمارية وحدها، بل مع مطوّر تُثبت مشاريعه المنجزة نهجه في الجودة وأسلوب الحياة.")}</div>
 </div>

 <h3 class=sh>3. ما المقصود بالفخامة بسعر في المتناول: ليست بناءً رخيصاً، بل تجربة راقية بسعر تنافسي</h3>
 <div class=grid3>
  <div class=card><h4>تجربة الوصول</h4><ul><li>ردهات مدخل مُبهرة</li><li>أسقف مزدوجة الارتفاع في مشاريع مختارة</li><li>مواد وألوان وتفاصيل معمارية أنيقة</li><li>مداخل وممرات مدروسة</li></ul></div>
  <div class=card><h4>تجربة الشقة</h4><ul><li>مخططات واسعة وعملية</li><li>أسقف بارتفاع 3.2 متر تقريباً في تصاميم مختارة</li><li>تشطيبات ومواد عالية الجودة</li><li>عمارة داخلية وخارجية عصرية</li></ul></div>
  <div class=card><h4>تجربة أسلوب الحياة</h4><ul><li>مسابح</li><li>مرافق للياقة والعافية</li><li>مساحات للاسترخاء وللعائلة</li><li>مرافق على السطح، وعدة مناطق للمرافق في مشاريع مختارة</li></ul></div>
 </div>
 {quote("الفرق مع إيمان أن الفخامة تبدأ منذ لحظة دخول المبنى، لا عند فتح باب الشقة فقط.")}

 <div class=cols>
  <div><h3 class=sh>4. حوّل الحجم البوتيكي إلى ميزة استثمارية</h3>
   <ul class=dots><li>بيئة سكنية أكثر هدوءاً وألفة</li><li>إحساس أكبر بالخصوصية</li><li>هوية معمارية مميزة</li><li>مساحات مرافق موزّعة بعناية</li><li>تجربة سكن مختلفة عن المشاريع عالية الكثافة</li></ul>
   <p class=sm>تضم مشاريع إيمان البوتيكية لعام 2026 (Oxford Cove و113 Residences ومشروع دبي للعلوم القادم) نحو {PIPELINE} وحدة سكنية مجتمعة.</p>
   {quote("إيمان لا تسعى إلى زيادة عدد الشقق، بل إلى رفع جودة التجربة السكنية.")}
   <p class=warn>قلّة عدد الوحدات لا تضمن تلقائياً كثافة أقل أو خصوصية أكبر أو ارتفاعاً في القيمة. ادعم هذه النقاط بمخططات المشروع ومواصفاته الفعلية.</p></div>
  <div><h3 class=sh>5. بِع القيمة الكاملة، لا السعر وحده</h3>
   <p class=sm>لا تركّز على الخصومات وحدها، بل قارن المنتج كاملاً بالمشاريع المماثلة:</p>
   <table class=t><thead><tr><th>عامل الاستثمار</th><th>ما يجب أن يوضّحه الوسيط</th></tr></thead><tbody>
   {''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in compare)}</tbody></table>
   {quote("السؤال ليس كم تكلّف الشقة فقط، بل ما مقدار الجودة والمساحة وأسلوب الحياة والقيمة طويلة الأمد التي تحصل عليها مقابل هذا السعر.")}</div>
 </div>
 {foot(1)}</section>"""

steps = ["فلسفة إيمان البوتيكية", "المشاريع المنجزة وسجل التسليم", "الجودة والمخططات والمرافق الفعلية", "المقارنة مع عقارات من الفئة السعرية نفسها",
         "الدفعات وعقد البيع والضمان والتسليم وإجراءات الشراء، بالوثائق الرسمية", "الوحدات المتاحة والأسئلة، قبل الحديث عن الحجز"]
p2 = f"""<section class=page>
 <div class=grid3>
  <div class=card><h4>6. الدفعات المرتبطة بالإنشاء ميزة شفافية</h4><p>في بعض خطط الدفع، تُسدَّد الأقساط وفق جدول الإنشاء المتفق عليه (في 113 Residences مثلاً، تُستحق 10% عند إنجاز 40% من البناء)، فيرى المشتري العلاقة بين دفعاته وتقدّم المشروع.</p>
   <p class=warn>استخدم دائماً أحدث خطة دفع معتمدة رسمياً. لا تدّعِ أن كل الأقساط مرتبطة بالإنشاء، أو أن المشتري غير ملزم بالدفع ما لم يتقدّم البناء.</p></div>
  <div class=card><h4>7. أثبت الجودة بالمشاريع المنجزة</h4><p>العميل الذي لا يستطيع زيارة دبي يحتاج إلى دليل مرئي. اعرض <b>Oxford 212</b>: الواجهة، والمدخل والردهة، والتفاصيل الداخلية، والممرات والمصاعد، والمرافق، والسطح، ومستوى التشطيب، ويُفضَّل بجولة فيديو حقيقية.</p>
   <p class=warn>اعرض المشروع المنجز قبل تصاميم المشروع الجديد، وفرّق بوضوح بين مزايا المشروع المنجز ومواصفات المشروع المعروض للبيع.</p></div>
  <div class=card><h4>8. استخدم الأداء السابق بحذر</h4><p>قارن أسعار الشراء الأصلية، وأسعار إعادة البيع الموثّقة، وأداء الإيجار المسجّل، وأسعار السوق المماثلة، ورسوم الخدمة وتكاليف التملك الأخرى. أظهر ارتفاع قيمة Oxford 212 بصفقات فعلية موثّقة، لا بنسبة غير مدعومة.</p>
   <p class=warn>الأداء السابق لا يضمن العوائد المستقبلية.</p></div>
 </div>
 {quote("لا نريدك أن تعتمد على التوقعات المستقبلية وحدها، بل أن تطّلع على ما تم تسليمه فعلاً، وكيف كان أداء عقارات مختارة من إيمان.")}

 <h3 class=sh>9. ترتيب العرض للعملاء اليابانيين</h3>
 <ol class=steps>{''.join(f'<li><span class=sn>{i+1}</span>{e(t)}</li>' for i, t in enumerate(steps))}</ol>
 <p class=sm style="margin-top:5px">المستثمر الياباني يقدّر الوضوح والدقة والمعلومات القابلة للتحقق. تجنّب المبالغة وأساليب الإغلاق الضاغطة والوعود غير المدعومة، وقدّم ملفاً واضحاً يتضمن المخططات والمواصفات والأسعار الموثّقة والوثائق القانونية. <b>الثقة تُبنى بالدليل والشفافية والاتساق.</b></p>

 <div class=cols>
  <div><h3 class=sh>10. الفرصة القادمة: مشروع دبي للعلوم</h3>
   <div class=dsp><img src="{src('img/dsp-teaser.jpg')}"><ul class=facts>
    <li><b>نحو 170 وحدة</b>استوديو وغرفة وغرفتان</li><li><b>قبو + أرضي + 10</b>حجم بوتيكي</li>
    <li><b>نهاية نوفمبر 2026</b>الإطلاق المتوقع</li><li><b>الربع الثالث 2029</b>التسليم المتوقع</li></ul></div>
   <p class=warn>تُؤكَّد المواصفات والأسعار وخطط الدفع والوحدات المتاحة والخصومات من آخر إعلان رسمي. استخدم صغر حجم المشروع لشرح فلسفة إيمان، لا للإيحاء بارتفاع مضمون في القيمة بسبب الندرة.</p>
   <h3 class=sh>أسلوب الإغلاق المقترح</h3>
   <p class=sm>بعد عرض سجل المطوّر وقيمته، اسأل:</p>
   {quote("بناءً على ما رأيت، هل تفضّل استوديو يركّز على دخل الإيجار في مشروع دبي للعلوم، أم شقة أكبر في 113 Residences توازن بين الطلب الإيجاري وفرص إعادة البيع مستقبلاً؟")}
   <p class=sm>اختر نوع الوحدة بناءً على الإجابة، ثم اعرض الوحدات المتاحة الموثّقة وخطة الدفع الرسمية وتكاليف الشراء كاملة. الهدف توجيه المستثمر إلى الخيار المناسب، لا الضغط عليه للحجز فوراً.</p></div>
  <div><h3 class=sh>ما يقوله الوسيط للعميل</h3>
   <div class=pitch><p>«دعني أوضّح لك لماذا تستحق إيمان للتطوير العقاري أن تكون ضمن خياراتك للاستثمار في دبي.</p>
    <p>إيمان ليست مطوّراً يبني آلاف الشقق، بل مطوّر بوتيكي يؤمن بالجودة قبل الكمية: تصميم راقٍ، ومخططات عملية، وردهات مدخل أنيقة، وتشطيبات عالية الجودة، ومرافق استثنائية، بأسعار دخول تنافسية.</p>
    <p>وما يميّزها بشكل خاص سجل التسليم المُثبت؛ فقد سلّمت تسعة مشاريع، ما يتيح لك تقييم مبانٍ حقيقية بدلاً من الاعتماد على وعود مستقبلية.</p>
    <p>عندما تشتري عقاراً من إيمان، فأنت تستثمر في بيئة سكنية مصمّمة بعناية، من ردهة المدخل إلى الشقة والمرافق. ونحن ندعوك لمقارنة الجودة والقيمة الفعلية بعقارات مماثلة في دبي.</p>
    <p>الفخامة بسعر في المتناول. الجودة قبل الكمية. تجربة حياة متكاملة.»</p></div></div>
 </div>

 <div class=final><div><span class=eb>الرسالة الأخيرة للوسطاء</span><h2>لا تبِع إيمان على أنها المطوّر الأرخص.</h2>
  <p class=formula><b>جودة راقية</b> + <b>مرافق أسلوب الحياة</b> + <b>تصميم مدروس</b> + <b>سعر دخول تنافسي</b> + <b>سجل تسليم مُثبت</b></p>
  <p>هذا هو أساس تموضع إيمان للتطوير العقاري: الفخامة بسعر في المتناول.</p></div>
  <div class=qrs><figure><img src="{qr('https://wa.me/' + WA)}"><figcaption>واتساب سام</figcaption></figure><figure><img src="{qr(FINDER)}"><figcaption>البحث عن الوحدات</figcaption></figure></div></div>
 {foot(2)}</section>"""

# Right to left: Arabic type, and the edges the shared layout puts on the left move to the start side.
CSS_AR = """
body{font:8.1pt/1.65 'IBM Plex Sans Arabic',Figtree,sans-serif}
h1,h2,h3,h4{line-height:1.45}
h1{font-size:19pt;font-weight:700;white-space:normal}
.eb,.tp,.stats span{letter-spacing:0}
ul{padding-left:0;padding-right:13px}
blockquote{border-left:0;border-right:3px solid var(--c);border-radius:6px 0 0 6px}
blockquote::before{content:"«";margin:0 0 0 3px}
.ti span{left:auto;right:0;border-top-right-radius:0;border-top-left-radius:7px}
.qrs{margin-left:0;margin-right:auto}
.final h2{font-size:12pt}
.t th,.t td{text-align:right}
.logo{text-align:right}
.stats b,.terms b{font-family:Marcellus,'IBM Plex Sans Arabic',serif}
.card p,.card li{font-size:7.5pt}
.pitch p{font-size:7.8pt}
"""


def main():
    at = os.path.join(REPO, "availability", "tools")
    doc = f"""<!doctype html><html lang=ar dir=rtl><head><meta charset=utf-8><style>
@font-face{{font-family:Marcellus;src:url(file://{at}/marcellus.woff2) format('woff2')}}
@font-face{{font-family:Figtree;src:url(file://{at}/figtree.woff2) format('woff2');font-weight:300 900}}
{fonts_css()}
{CSS}{CSS_AR}</style></head><body>{p1}{p2}</body></html>"""
    # Keep Latin names and numbers in their own direction inside Arabic sentences.
    for name in ("113 Residences", "Oxford 212", "Oxford Cove"):
        doc = doc.replace(name, f"<bdi dir=ltr>{name}</bdi>")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = os.path.join(os.path.dirname(OUT), "_strategy_ar.html")
    open(tmp, "w").write(doc)
    with sync_playwright() as pw:
        exe = "/opt/pw-browsers/chromium"
        b = pw.chromium.launch(**({"executable_path": exe} if os.path.exists(exe) else {}))
        pg = b.new_page()
        pg.goto("file://" + tmp)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        over = pg.evaluate("[...document.querySelectorAll('.page')].map(p=>{const f=p.querySelector('.foot').getBoundingClientRect().top;return Math.max(...[...p.children].filter(c=>!c.classList.contains('foot')).map(c=>c.getBoundingClientRect().bottom))-f})")
        print("space above footer (px, negative = fits):", [round(o) for o in over])
        pg.pdf(path=OUT, format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    os.remove(tmp)
    print("wrote", os.path.relpath(OUT, REPO))


if __name__ == "__main__":
    main()
