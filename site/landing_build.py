"""Build the Yandex Direct landing page for 113 Residences from inventory.json.

Writes site/ru/index.html (the landing page) and site/ru/privacy.html (privacy
policy, required by Yandex Direct for pages that collect personal data).
Published on GitHub Pages at https://samjabrdxb.github.io/Iman-developers-/ru/

Fill in the contact settings below, then run: python3 site/landing_build.py
"""
import json, os

# --- Settings --------------------------------------------------------------
CONFIG = {
    "whatsapp": "971501752771",   # WhatsApp number, digits only
    "telegram": "",               # Telegram username without @ (empty hides the Telegram buttons)
    "email": "",                  # Email that receives the form leads (empty: the form opens WhatsApp instead)
    "metrika": 0,                 # Yandex Metrica counter ID (0: no counter)
}
SITE_URL = "https://samjabrdxb.github.io/Iman-developers-/ru/"
# ---------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ru")
os.makedirs(OUT, exist_ok=True)
inv = json.load(open(os.path.join(HERE, "inventory.json")))
tpl = open(os.path.join(HERE, "landing.tpl.html")).read()
for mark in ("/*INVENTORY*/", "/*CONFIG*/"):
    assert tpl.count(mark) == 1, mark
js = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
page = tpl.replace("/*INVENTORY*/", js(inv)).replace("/*CONFIG*/", js(CONFIG))

metrika = ""
if CONFIG["metrika"]:
    mid = int(CONFIG["metrika"])
    metrika = f"""<script>(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};m[i].l=1*new Date();
for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r)return}}
k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
ym({mid},"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true}});</script>
<noscript><div><img src="https://mc.yandex.ru/watch/{mid}" style="position:absolute;left:-9999px" alt=""></div></noscript>
"""

desc = "113 Residences от IMAN Developers в Аль-Суфух, Дубай: квартиры у парка и пляжа, рассрочка 40/60, скидка 14% при 100% оплате. Цены и планировки в WhatsApp."
head = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="113 Residences · Дубай · IMAN Developers">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}../img/113-residences.jpg">
<link rel="canonical" href="{SITE_URL}">
{metrika}</head>
<body>
"""
open(os.path.join(OUT, "index.html"), "w").write(head + page + "\n</body>\n</html>\n")

contact = " · ".join(x for x in [
    "WhatsApp / тел.: +971 50 175 2771",
    f"Telegram: @{CONFIG['telegram'].lstrip('@')}" if CONFIG["telegram"] else "",
    f"E-mail: {CONFIG['email']}" if CONFIG["email"] else ""] if x)
privacy = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Политика конфиденциальности · Сэм Джабр</title>
{metrika}<style>
:root{{--bg:#f3f5f1;--ink:#17251c;--muted:#5b6b60;--green:#1d3f2b}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0e1712;--ink:#e6ece6;--muted:#9fb0a4;--green:#a9bcae;color-scheme:dark}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 system-ui,sans-serif}}
main{{max-width:760px;margin:0 auto;padding:32px 16px 64px}}
h1{{font-family:Georgia,serif;font-weight:400;font-size:32px;line-height:1.2}}
h2{{font-size:18px;margin-top:28px}}
p,li{{color:var(--ink)}} small{{color:var(--muted)}} a{{color:inherit}}
</style>
</head>
<body><main>
<p><a href="./">← На главную</a></p>
<h1>Политика конфиденциальности</h1>
<p><small>Редакция от {inv['inventoryDate']}</small></p>
<p>Настоящая политика описывает, как Сэм Джабр, старший менеджер по продажам IMAN Developers (Дубай, ОАЭ), далее «Оператор», обрабатывает персональные данные посетителей сайта {SITE_URL}.</p>
<h2>1. Какие данные мы собираем</h2>
<ul><li>Имя, номер телефона, бюджет, интересующий проект и удобный способ связи, которые вы указываете в форме заявки.</li>
<li>Технические данные о посещении (cookie, IP-адрес, сведения о браузере и устройстве, источник перехода), собираемые сервисом Яндекс Метрика.</li></ul>
<h2>2. Цели обработки</h2>
<ul><li>Связаться с вами и ответить на заявку: подобрать недвижимость, направить цены, планировки и условия оплаты.</li>
<li>Анализ посещаемости и улучшение работы сайта и рекламы.</li></ul>
<h2>3. Правовое основание</h2>
<p>Данные обрабатываются на основании вашего согласия, которое вы даёте, отправляя форму на сайте. Вы можете отозвать согласие в любой момент, написав Оператору.</p>
<h2>4. Передача данных</h2>
<p>Данные не продаются и не передаются третьим лицам, кроме сервисов, необходимых для работы сайта: сервиса доставки заявок на электронную почту (FormSubmit), мессенджеров WhatsApp и Telegram при обращении через них, и Яндекс Метрики. При заключении сделки данные могут быть переданы застройщику IMAN Developers и уполномоченным государственным органам ОАЭ (Земельный департамент Дубая) в объёме, необходимом для оформления.</p>
<h2>5. Срок хранения</h2>
<p>Данные хранятся до достижения целей обработки или до отзыва согласия, но не дольше 3 лет с момента последнего обращения.</p>
<h2>6. Ваши права</h2>
<p>Вы вправе запросить сведения о своих данных, их уточнение или удаление, а также отозвать согласие на обработку.</p>
<h2>7. Cookie</h2>
<p>Сайт использует cookie Яндекс Метрики. Вы можете отключить cookie в настройках браузера; сайт продолжит работать.</p>
<h2>8. Контакты Оператора</h2>
<p>Сэм Джабр, IMAN Developers, Дубай, ОАЭ. {contact}.</p>
</main></body></html>
"""
open(os.path.join(OUT, "privacy.html"), "w").write(privacy)
print("built landing:", sum(len(p["units"]) for p in inv["projects"]), "units ->", os.path.relpath(OUT))
