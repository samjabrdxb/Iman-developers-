"""Build the 113 Residences landing page from inventory.json, one folder per language.

  site/ru/  Russian, for Yandex Direct    https://samjabrdxb.github.io/Iman-developers-/ru/
  site/en/  English, for Google Ads       https://samjabrdxb.github.io/Iman-developers-/en/
  site/ar/  Arabic, for Google Ads        https://samjabrdxb.github.io/Iman-developers-/ar/
  site/ja/  Japanese, for Google Ads      https://samjabrdxb.github.io/Iman-developers-/ja/

Each folder gets index.html (the page, opening in its language; the language
buttons still switch) and privacy.html (privacy policy in that language, which
Yandex Direct and Google Ads ask for on pages that collect personal data).

Fill in the settings below, then run: python3 site/landing_build.py
"""
import json, os

# --- Settings --------------------------------------------------------------
CONFIG = {
    "whatsapp": "971501752771",   # WhatsApp number, digits only
    "telegram": "",               # Telegram username without @ (empty hides the Telegram buttons)
    "email": "Sami@imandevelopers.com",  # Email that receives the form leads (empty: the form opens WhatsApp instead)
    "web3forms": "",              # Web3Forms access key (sent to the lead e-mail from web3forms.com); used instead of FormSubmit when set
    "metrika": 114052212,         # Yandex Metrica counter ID (0: no counter)
    # Google Ads tag and conversions, from Google Ads > Goals > Conversions, e.g.
    # {"id": "AW-123456789", "lead_form": "AW-123456789/AbCdEf", "click_whatsapp": "AW-123456789/GhIjKl"}
    "gads": {},
}
BASE = "https://samjabrdxb.github.io/Iman-developers-/"
# ---------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
inv = json.load(open(os.path.join(HERE, "inventory.json")))
tpl = open(os.path.join(HERE, "landing.tpl.html")).read()
for mark in ("/*INVENTORY*/", "/*CONFIG*/"):
    assert tpl.count(mark) == 1, mark
js = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

tags = ""
if CONFIG["metrika"]:
    mid = int(CONFIG["metrika"])
    tags += f"""<script>(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};m[i].l=1*new Date();
for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r)return}}
k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window,document,"script","https://mc.yandex.ru/metrika/tag.js?id={mid}","ym");
ym({mid},"init",{{ssr:true,webvisor:true,clickmap:true,ecommerce:"dataLayer",accurateTrackBounce:true,trackLinks:true}});</script>
<noscript><div><img src="https://mc.yandex.ru/watch/{mid}" style="position:absolute;left:-9999px" alt=""></div></noscript>
"""
if CONFIG["gads"].get("id"):
    gid = CONFIG["gads"]["id"]
    tags += f"""<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{gid}");</script>
"""

contact = lambda phone: " · ".join(x for x in [
    f"WhatsApp / {phone}: +971 50 175 2771",
    f"Telegram: @{CONFIG['telegram'].lstrip('@')}" if CONFIG["telegram"] else "",
    f"E-mail: {CONFIG['email']}" if CONFIG["email"] else ""] if x)

LANGS = {
 "ru": dict(dir="ltr",
  desc="113 Residences от IMAN Developers в Аль-Суфух, Дубай: квартиры у парка и пляжа, рассрочка 40/60, скидка 14% при 100% оплате. Цены и планировки в WhatsApp.",
  og="113 Residences · Дубай · IMAN Developers",
  privacy=lambda url: f"""<p><a href="./">← На главную</a></p>
<h1>Политика конфиденциальности</h1>
<p><small>Редакция от {inv['inventoryDate']}</small></p>
<p>Настоящая политика описывает, как Сэм Джабр, старший менеджер по продажам IMAN Developers (Дубай, ОАЭ), далее «Оператор», обрабатывает персональные данные посетителей сайта {url}.</p>
<h2>1. Какие данные мы собираем</h2>
<ul><li>Имя, номер телефона, бюджет, интересующая планировка и удобный способ связи, которые вы указываете в форме заявки.</li>
<li>Технические данные о посещении (cookie, IP-адрес, сведения о браузере и устройстве, источник перехода), собираемые сервисами Яндекс Метрика и Google Ads.</li></ul>
<h2>2. Цели обработки</h2>
<ul><li>Связаться с вами и ответить на заявку: подобрать недвижимость, направить цены, планировки и условия оплаты.</li>
<li>Анализ посещаемости и улучшение работы сайта и рекламы.</li></ul>
<h2>3. Правовое основание</h2>
<p>Данные обрабатываются на основании вашего согласия, которое вы даёте, отправляя форму на сайте. Вы можете отозвать согласие в любой момент, написав Оператору.</p>
<h2>4. Передача данных</h2>
<p>Данные не продаются и не передаются третьим лицам, кроме сервисов, необходимых для работы сайта: сервиса доставки заявок на электронную почту, мессенджеров WhatsApp и Telegram при обращении через них, Яндекс Метрики и Google Ads. При заключении сделки данные могут быть переданы застройщику IMAN Developers и уполномоченным государственным органам ОАЭ (Земельный департамент Дубая) в объёме, необходимом для оформления.</p>
<h2>5. Срок хранения</h2>
<p>Данные хранятся до достижения целей обработки или до отзыва согласия, но не дольше 3 лет с момента последнего обращения.</p>
<h2>6. Ваши права</h2>
<p>Вы вправе запросить сведения о своих данных, их уточнение или удаление, а также отозвать согласие на обработку.</p>
<h2>7. Cookie</h2>
<p>Сайт использует cookie Яндекс Метрики и Google. Вы можете отключить cookie в настройках браузера; сайт продолжит работать.</p>
<h2>8. Контакты Оператора</h2>
<p>Сэм Джабр, IMAN Developers, Дубай, ОАЭ. {contact("тел.")}.</p>""",
  ptitle="Политика конфиденциальности · Сэм Джабр"),
 "en": dict(dir="ltr",
  desc="113 Residences by IMAN Developers in Al Sufouh, Dubai: 2 and 3 bedroom apartments by the park and the beach, 40/60 payment plan, 14% off on full payment. Prices and floor plans on WhatsApp.",
  og="113 Residences · Dubai · IMAN Developers",
  privacy=lambda url: f"""<p><a href="./">← Back to the page</a></p>
<h1>Privacy policy</h1>
<p><small>Version of {inv['inventoryDate']}</small></p>
<p>This policy explains how Sam Jabr, Senior Sales Manager at IMAN Developers (Dubai, UAE), "we", handles the personal data of visitors to {url}.</p>
<h2>1. What we collect</h2>
<ul><li>The name, phone number, budget, preferred layout and contact method you enter in the enquiry form.</li>
<li>Technical visit data (cookies, IP address, browser and device details, referring source) collected by Google Ads and Yandex Metrica.</li></ul>
<h2>2. Why we use it</h2>
<ul><li>To contact you and answer your enquiry: matching a property and sending prices, floor plans and payment terms.</li>
<li>To measure visits and improve the website and our advertising.</li></ul>
<h2>3. Legal basis</h2>
<p>We process your data with the consent you give by sending the form. You can withdraw it at any time by writing to us.</p>
<h2>4. Sharing</h2>
<p>We do not sell your data or share it with third parties, except the services the website needs to work: the service that delivers form enquiries by e-mail, WhatsApp and Telegram when you contact us through them, Google Ads and Yandex Metrica. If you buy, your data may be shared with IMAN Developers and the UAE authorities (Dubai Land Department) as far as the purchase requires.</p>
<h2>5. How long we keep it</h2>
<p>Until the purpose is fulfilled or you withdraw consent, and no longer than 3 years after your last contact.</p>
<h2>6. Your rights</h2>
<p>You can ask what data we hold about you, have it corrected or deleted, and withdraw your consent.</p>
<h2>7. Cookies</h2>
<p>The website uses Google and Yandex Metrica cookies. You can turn cookies off in your browser settings; the website will keep working.</p>
<h2>8. Contact</h2>
<p>Sam Jabr, IMAN Developers, Dubai, UAE. {contact("phone")}.</p>""",
  ptitle="Privacy policy · Sam Jabr"),
 "ar": dict(dir="rtl",
  desc="113 Residences من إيمان للتطوير العقاري في الصفوح، دبي: شقق بغرفتين و3 غرف جنب الحديقة والبحر، خطة دفع 40/60، وخصم 14% عند الدفع الكامل. الأسعار والمخططات على واتساب.",
  og="113 Residences · دبي · إيمان للتطوير العقاري",
  privacy=lambda url: f"""<p><a href="./">→ العودة للصفحة</a></p>
<h1>سياسة الخصوصية</h1>
<p><small>نسخة بتاريخ {inv['inventoryDate']}</small></p>
<p>توضّح هذه السياسة كيف يتعامل سام جبر، مدير مبيعات أول في إيمان للتطوير العقاري (دبي، الإمارات)، مع البيانات الشخصية لزوّار الموقع {url}.</p>
<h2>1. البيانات التي نجمعها</h2>
<ul><li>الاسم ورقم الهاتف والميزانية والمخطط المفضّل وطريقة التواصل التي تكتبها في نموذج الطلب.</li>
<li>بيانات تقنية عن الزيارة (ملفات تعريف الارتباط، عنوان IP، معلومات المتصفح والجهاز، مصدر الزيارة) تجمعها خدمتا Google Ads وYandex Metrica.</li></ul>
<h2>2. لماذا نستخدمها</h2>
<ul><li>للتواصل معك والرد على طلبك: اختيار العقار المناسب وإرسال الأسعار والمخططات وشروط الدفع.</li>
<li>لقياس الزيارات وتحسين الموقع والإعلانات.</li></ul>
<h2>3. الأساس القانوني</h2>
<p>نعالج بياناتك بناءً على موافقتك عند إرسال النموذج، ويمكنك سحبها في أي وقت بمراسلتنا.</p>
<h2>4. مشاركة البيانات</h2>
<p>لا نبيع بياناتك ولا نشاركها مع أي طرف، إلا الخدمات التي يحتاجها الموقع ليعمل: خدمة إيصال الطلبات بالبريد الإلكتروني، وواتساب وتيليغرام عند تواصلك عبرهما، وGoogle Ads وYandex Metrica. وعند الشراء قد تُشارك البيانات مع إيمان للتطوير العقاري والجهات الرسمية في الإمارات (دائرة الأراضي والأملاك في دبي) بالقدر الذي يتطلبه الشراء.</p>
<h2>5. مدة الحفظ</h2>
<p>حتى تحقيق الغرض أو سحب الموافقة، وبحد أقصى 3 سنوات من آخر تواصل.</p>
<h2>6. حقوقك</h2>
<p>يحق لك معرفة البيانات المحفوظة عنك، وتصحيحها أو حذفها، وسحب موافقتك.</p>
<h2>7. ملفات تعريف الارتباط</h2>
<p>يستخدم الموقع ملفات تعريف الارتباط من Google وYandex Metrica، ويمكنك إيقافها من إعدادات المتصفح وسيبقى الموقع يعمل.</p>
<h2>8. التواصل</h2>
<p>سام جبر، إيمان للتطوير العقاري، دبي، الإمارات. {contact("هاتف")}.</p>""",
  ptitle="سياسة الخصوصية · سام جبر"),
 "ja": dict(dir="ltr",
  desc="IMAN Developersの113 Residences（ドバイ、アル・スフー）：公園とビーチのそばの2・3ベッドルーム、40/60の分割払い、一括払いで14%割引。価格と間取り図はWhatsAppで。",
  og="113 Residences · ドバイ · IMAN Developers",
  privacy=lambda url: f"""<p><a href="./">← ページに戻る</a></p>
<h1>プライバシーポリシー</h1>
<p><small>{inv['inventoryDate']} 版</small></p>
<p>本ポリシーは、IMAN Developers（UAE・ドバイ）のシニア・セールスマネージャーであるサム・ジャブル（以下「当方」）が、ウェブサイト {url} の訪問者の個人情報をどのように取り扱うかを説明するものです。</p>
<h2>1. 収集する情報</h2>
<ul><li>お問い合わせフォームにご入力いただくお名前、電話番号、ご予算、ご希望の間取り、ご希望の連絡方法。</li>
<li>Google AdsおよびYandex Metricaが収集する訪問に関する技術情報（Cookie、IPアドレス、ブラウザ・端末の情報、参照元）。</li></ul>
<h2>2. 利用目的</h2>
<ul><li>ご連絡およびお問い合わせへの回答（物件のご提案、価格・間取り図・支払い条件の送付）。</li>
<li>アクセス解析、ならびにウェブサイトと広告の改善。</li></ul>
<h2>3. 法的根拠</h2>
<p>フォームの送信によりいただいたご同意に基づいて個人情報を取り扱います。ご同意は、当方へご連絡いただくことでいつでも撤回できます。</p>
<h2>4. 第三者への提供</h2>
<p>個人情報を販売することはなく、ウェブサイトの運営に必要なサービス（フォームの内容をメールで届けるサービス、ご連絡に使われた場合のWhatsAppおよびTelegram、Google Ads、Yandex Metrica）を除き、第三者に提供することはありません。ご購入の際は、手続きに必要な範囲で、IMAN DevelopersおよびUAEの関係当局（ドバイ土地局）に提供される場合があります。</p>
<h2>5. 保存期間</h2>
<p>利用目的の達成またはご同意の撤回まで保存し、最後のご連絡から3年を超えて保存することはありません。</p>
<h2>6. お客様の権利</h2>
<p>当方が保有するご自身の情報の開示、訂正または削除を求めること、およびご同意を撤回することができます。</p>
<h2>7. Cookie</h2>
<p>本ウェブサイトはGoogleおよびYandex MetricaのCookieを使用しています。ブラウザの設定でCookieを無効にしても、ウェブサイトは引き続きご利用いただけます。</p>
<h2>8. お問い合わせ先</h2>
<p>サム・ジャブル、IMAN Developers、UAE・ドバイ。{contact("電話")}。</p>""",
  ptitle="プライバシーポリシー · サム・ジャブル"),
}

PRIV_CSS = """:root{--bg:#f7f5ef;--ink:#1d211c;--muted:#77796f}
@media (prefers-color-scheme:dark){:root{--bg:#141714;--ink:#ece9df;--muted:#9b9b90;color-scheme:dark}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.7 system-ui,"Segoe UI",Tahoma,sans-serif}
main{max-width:760px;margin:0 auto;padding:32px 16px 64px}
h1{font-weight:400;font-size:34px;line-height:1.2}
h2{font-size:18px;margin-top:28px}
small{color:var(--muted)} a{color:inherit}"""

for lang, L in LANGS.items():
    url = BASE + lang + "/"
    out = os.path.join(HERE, lang)
    os.makedirs(out, exist_ok=True)
    page = tpl.replace("/*INVENTORY*/", js(inv)).replace("/*CONFIG*/", js({**CONFIG, "lang": lang}))
    alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{l}/">\n' for l in LANGS)
    head = f"""<!doctype html>
<html lang="{lang}" dir="{L['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="{L['desc']}">
<meta property="og:type" content="website">
<meta property="og:title" content="{L['og']}">
<meta property="og:description" content="{L['desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/113-residences.jpg">
<link rel="canonical" href="{url}">
{alt}{tags}</head>
<body>
"""
    open(os.path.join(out, "index.html"), "w").write(head + page + "\n</body>\n</html>\n")
    open(os.path.join(out, "privacy.html"), "w").write(f"""<!doctype html>
<html lang="{lang}" dir="{L['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{L['ptitle']}</title>
{tags}<style>
{PRIV_CSS}
</style>
</head>
<body><main>
{L['privacy'](url)}
</main></body></html>
""")
    print("built", lang, "->", os.path.relpath(out, HERE))
