"""Yandex Direct ad images in Russian, built from site/inventory.json.

Five designs, each in the three shapes Yandex Direct takes:
  1x1 1080x1080 (standard), 16x9 1920x1080 (wide), 3x4 1080x1440 (vertical).
Writes JPGs to marketing/<inventoryDate>/yandex/.
Run: python3 marketing/tools/yandex_ads.py
"""
import json, os
from playwright.sync_api import sync_playwright

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(REPO, "site")
inv = json.load(open(os.path.join(SITE, "inventory.json")))
OUT = os.path.join(REPO, "marketing", inv["inventoryDate"], "yandex")
os.makedirs(OUT, exist_ok=True)
USD = 1 / 3.6725
byId = {p["id"]: p for p in inv["projects"]}


def price(u, p):
    d = u.get("discount", p.get("discount")) or 0
    return u["op"] * (1 - d)


def from_usd(ids):
    lo = min(price(u, byId[i]) for i in ids for u in byId[i]["units"])
    return "$" + f"{int(lo * USD) // 1000 * 1000:,}".replace(",", " ")


LIVE = [i for i in ["113-residences", "sierra-by-iman", "15-cascade", "one-park-square", "one-sky-park"] if byId[i]["units"]]
img = lambda rel: "file://" + os.path.join(SITE, rel)

ADS = [
    dict(slug="01-dubai-general", photo=img("img/113-residences.jpg"), pos="50% 60%",
         eb="Дубай · от застройщика", h="Квартиры в Дубае<br>от <span>IMAN Developers</span>",
         chips=["Рассрочка 40/60", "0% налога на доход", "Покупка удалённо"],
         price=("цена от", from_usd(LIVE)), cta="Получить подборку"),
    dict(slug="02-113-residences", photo=img("img/113-residences.jpg"), pos="50% 40%",
         eb="113 Residences · Аль-Суфух", h="Новый проект<br>у <span>парка и пляжа</span>",
         chips=["Рассрочка 40/60", "−14% при 100% оплате", "Сдача Q2 2029"],
         price=("цена от", from_usd(["113-residences"])), cta="Узнать цены"),
    dict(slug="03-one-park-square", photo=img(byId["one-park-square"]["image"]), pos="50% 50%",
         eb="One Park Square · JVC", h="Квартиры в Дубае<br><span>50% до сдачи</span>",
         chips=["Студии и 1–2 спальни", "Сдача Q2 2028", "Рассрочка 50/50"],
         price=("цена от", from_usd(["one-park-square"])), cta="Смотреть квартиры"),
    dict(slug="04-15-cascade", photo=img(byId["15-cascade"]["image"]), pos="50% 50%",
         eb="15 Cascade · Motor City", h="Студии и 1 спальня<br><span>с рассрочкой</span>",
         chips=["Рассрочка 60/40", "Сдача Q4 2028", "От застройщика"],
         price=("цена от", from_usd(["15-cascade"])), cta="Узнать цены"),
    dict(slug="05-manager", photo=img("assets/one-sky-park-main.webp"), pos="50% 50%", sam=True,
         eb="Ваш менеджер в Дубае", h="Подберу квартиру<br>под <span>ваш бюджет</span>",
         chips=["Сэм Джабр · IMAN Developers", "WhatsApp · Telegram", "Онлайн-показ квартир"],
         price=None, cta="Написать в WhatsApp"),
]
SIZES = [("1x1", 1080, 1080), ("16x9", 1920, 1080), ("3x4", 1080, 1440)]

CSS = """
*{box-sizing:border-box;margin:0}
body{width:var(--w);height:var(--h);overflow:hidden;background:#16301f;color:#f2f5f0;font-family:Manrope,sans-serif;position:relative}
.ph{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.shade{position:absolute;inset:0}
.logo{position:absolute;top:var(--pad);left:var(--pad);display:flex;flex-direction:column;color:#d79e85;line-height:1;z-index:2}
.logo b{font-family:Marcellus,serif;font-weight:400;font-size:calc(var(--u)*4.4);letter-spacing:.32em}
.logo small{font-size:calc(var(--u)*1.5);letter-spacing:.55em;margin-top:.5em;font-weight:700}
.box{position:absolute;z-index:2;display:flex;flex-direction:column;gap:calc(var(--u)*2.2)}
.eb{color:#d79e85;font-weight:800;letter-spacing:.14em;text-transform:uppercase;font-size:calc(var(--u)*2.3)}
h1{font-variant-numeric:lining-nums;font-family:"Cormorant Garamond",serif;font-weight:600;font-size:calc(var(--u)*8.6);line-height:.98;letter-spacing:-.01em}
h1 span{color:#e2ad95}
.chips{display:flex;flex-wrap:wrap;gap:calc(var(--u)*1.2)}
.chips span{background:rgba(242,245,240,.12);border:1px solid rgba(242,245,240,.28);backdrop-filter:blur(6px);border-radius:99px;padding:.45em .95em;font-size:calc(var(--u)*2.3);font-weight:700}
.row{display:flex;align-items:flex-end;justify-content:space-between;gap:calc(var(--u)*3);margin-top:calc(var(--u)*1)}
.pr small{display:block;font-size:calc(var(--u)*2.2);color:#cfdad2;font-weight:700}
.pr b{font-variant-numeric:lining-nums;display:block;font-family:"Cormorant Garamond",serif;font-weight:700;font-size:calc(var(--u)*9);line-height:.9;color:#f2f5f0}
.cta{background:#c0866d;color:#1b120d;font-weight:800;border-radius:99px;padding:.85em 1.5em;font-size:calc(var(--u)*2.8);white-space:nowrap}
.sam{position:absolute;z-index:1;object-fit:cover;object-position:50% 10%;border:calc(var(--u)*.6) solid #c0866d;border-radius:50%}
/* square + vertical: text at the bottom over a dark fade */
.tall .shade{background:linear-gradient(180deg,rgba(14,28,19,.55) 0%,rgba(14,28,19,0) 22%,rgba(14,28,19,.25) 42%,rgba(14,28,19,.92) 68%,#10241a 100%)}
.tall .box{left:var(--pad);right:var(--pad);bottom:var(--pad)}
/* wide: text on the left over a side fade */
.wide .shade{background:linear-gradient(90deg,#10241a 0%,rgba(16,36,26,.94) 38%,rgba(16,36,26,.35) 62%,rgba(16,36,26,0) 80%),linear-gradient(180deg,rgba(14,28,19,.45),rgba(14,28,19,0) 25%)}
.wide .box{left:var(--pad);bottom:var(--pad);width:52%}
.wide .ph{left:28%;width:72%}
"""


def page(ad, shape, w, h):
    tall = shape != "16x9"
    u = (w if tall else h) / 100  # one unit = 1% of the short side
    pad = u * 6
    sam = ""
    if ad.get("sam"):
        d = u * (30 if shape == "3x4" else 26 if shape == "1x1" else 40)
        pos = (f"top:{pad + u*10}px;right:{pad}px" if tall else f"top:50%;right:{u*12}px;transform:translateY(-50%)")
        sam = f'<img class="sam" src="{img("img/sam-jabr.jpg")}" style="width:{d}px;height:{d}px;{pos}">'
    chips = "".join(f"<span>{c}</span>" for c in ad["chips"])
    pr = f'<div class="pr"><small>{ad["price"][0]}</small><b>{ad["price"][1]}</b></div>' if ad["price"] else "<div></div>"
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Manrope:wght@500;700;800&family=Marcellus&display=swap">
<style>:root{{--w:{w}px;--h:{h}px;--u:{u}px;--pad:{pad}px}}{CSS}</style></head>
<body class="{'tall' if tall else 'wide'}">
<img class="ph" src="{ad['photo']}" style="object-position:{ad['pos']}"><div class="shade"></div>{sam}
<div class="logo"><b>IMAN</b><small>DEVELOPERS</small></div>
<div class="box"><div class="eb">{ad['eb']}</div><h1>{ad['h']}</h1><div class="chips">{chips}</div>
<div class="row">{pr}<div class="cta">{ad['cta']}</div></div></div>
</body></html>"""


with sync_playwright() as pw:
    try:
        b = pw.chromium.launch()
    except Exception:  # Python playwright whose own browser is missing: use the preinstalled one
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for ad in ADS:
        for shape, w, h in SIZES:
            pg = b.new_page(viewport={"width": w, "height": h})
            tmp = os.path.join(OUT, ".tmp.html")
            open(tmp, "w").write(page(ad, shape, w, h))
            pg.goto("file://" + tmp, wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            path = os.path.join(OUT, f"{ad['slug']}-{shape}.jpg")
            pg.screenshot(path=path, type="jpeg", quality=90)
            pg.close()
            print(os.path.relpath(path, REPO))
    os.remove(os.path.join(OUT, ".tmp.html"))
    b.close()
