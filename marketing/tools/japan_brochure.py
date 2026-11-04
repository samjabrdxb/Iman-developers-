"""Japanese partner brochure: how to sell IMAN, for real estate brokers in Japan.

Usage:  python3 marketing/tools/japan_brochure.py

Writes marketing/japan/iman-japan-partner-guide.pdf (A4 portrait, 2 pages).
Prices come from site/inventory.json (113 Residences and Sierra retail); the
offers below follow availability/OFFERS.md. Yen is a guide only (JPY below).
"""
import html, json, os, re, subprocess, base64, io
import qrcode
from playwright.sync_api import sync_playwright

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(TOOLS))
SITE = os.path.join(REPO, "site")
OUT = os.path.join(REPO, "marketing", "japan", "iman-japan-partner-guide.pdf")
FONTS = "/tmp/iman-fonts-jp"   # Noto Sans JP from Google Fonts, downloaded once

JPY = 41.5                     # yen per dirham, a guide only
WA = "971501752771"
FINDER = "https://claude.ai/artifact/T6RPFxW5jAsAzdhcXZzqXX"          # Japanese unit finder for brokers
LANDING = "https://samjabrdxb.github.io/Iman-developers-/ja/"         # Japanese page for clients
MKT_113 = "https://drive.google.com/drive/folders/1kE-KUHmkLYhNm5r71XLE72S3g4WZqRBJ?usp=sharing"

e = html.escape
aed = lambda n: f"{round(n):,}"
yen = lambda n: f"{round(n * JPY / 10000):,}万円"           # e.g. 8,730万円
inv = json.load(open(os.path.join(SITE, "inventory.json")))
P = {p["id"]: p for p in inv["projects"]}


def fonts_css():
    """Noto Sans JP as local woff2 files (Chromium prints from file://, without the network)."""
    css_path = os.path.join(FONTS, "jp.css")
    if not os.path.exists(css_path):
        os.makedirs(FONTS, exist_ok=True)
        ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        css = subprocess.run(["curl", "-sS", "-A", ua, "https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap"],
                             check=True, capture_output=True, text=True).stdout
        urls = sorted(set(re.findall(r"url\((https://[^)]+)\)", css)))
        jobs = "".join(f'url = "{u}"\noutput = "{FONTS}/{i}.woff2"\n' for i, u in enumerate(urls))
        subprocess.run(["curl", "-sS", "--parallel", "--parallel-max", "16", "-K", "-"], input=jobs, text=True, check=True)
        for i, u in enumerate(urls):
            css = css.replace(u, f"file://{FONTS}/{i}.woff2")
        open(css_path, "w").write(css)
    return open(css_path).read()


def qr(url):
    img = qrcode.make(url, border=1, box_size=8)
    b = io.BytesIO(); img.save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


def src(path):
    return "file://" + os.path.join(SITE, path)


# --- 113 Residences layouts from the inventory --------------------------------
r113 = P["113-residences"]
DISC, CASH = r113.get("discount", 0.04), r113.get("cash", 0.14)
TYPE_JA = {"one bedroom with study": "1ベッドルーム＋書斎", "two bedroom": "2ベッドルーム", "two bedroom with study": "2ベッドルーム＋書斎",
           "two bedroom with maid": "2ベッドルーム＋メイドルーム", "three bedroom with study": "3ベッドルーム＋書斎",
           "three bedroom with maid": "3ベッドルーム＋メイドルーム"}
layouts = []
for k, name in TYPE_JA.items():
    us = [u for u in r113["units"] if u["type"].lower() == k]
    if us:
        layouts.append(dict(k=k, name=name, n=len(us), a0=min(u["area"] for u in us), a1=max(u["area"] for u in us),
                            p=min(u["op"] for u in us) * (1 - DISC), c=min(u["op"] for u in us) * (1 - CASH)))
sqm = lambda a: f"{round(a * 0.092903)}"
ex = next(l for l in layouts if l["k"] == "two bedroom")      # example for the payment page
retail = P["sierra-by-iman"]["units"]
RD, RC = P["sierra-by-iman"].get("discount", 0.04), P["sierra-by-iman"].get("cash", 0.18)

ready = [p for p in inv["projects"] if p["status"] == "ready"]
building = [p for p in inv["projects"] if p["status"] == "construction"]
AREA_JA = {"Jumeirah Village Circle": "JVC", "Arjan": "アルジャン", "Dubai Hills Estate": "ドバイ・ヒルズ・エステート",
           "Motor City": "モーターシティ", "Al Sufouh": "アル・スフー"}
DRIVE = [("アル・スフー・コミュニティパーク", 1), ("シェイク・ザイード・ロード", 1), ("アル・スフー・ビーチ", 3), ("パーム・ジュメイラ", 8),
         ("モール・オブ・ジ・エミレーツ", 10), ("ドバイ・マリーナ", 10), ("ドバイモール＆ダウンタウン", 18), ("ドバイ国際空港", 24)]

d = inv["inventoryDate"].split("-")
DATE = f"{int(d[0])}年{int(d[1])}月{int(d[2])}日"


def foot(n):
    return f"""<div class=foot><span>サム・ジャブル（Sam Jabr）· IMAN Developers · WhatsApp +971 50 175 2771</span><span>{n} / 2</span></div>"""


def head(k, h, sub=""):
    return f"""<div class=eb>{k}</div><h2>{h}</h2>{f'<p class=lead>{sub}</p>' if sub else ''}"""


pages = []
gv = ("113 Residencesは40/60プランなら全住戸が200万AED以上。" if min(l["p"] for l in layouts) >= 2e6 else "113 Residencesの多くの住戸が対象。")

# Page 1: why Dubai, IMAN, 113 Residences
why = [("外国人でも完全所有", "フリーホールド地区では外国人も100%所有。登記はドバイ土地局（DLD）。"),
       ("UAEでは個人所得税なし", "所得税・キャピタルゲイン税なし。※日本居住者は日本で課税（税理士にご確認を）。"),
       ("米ドル連動の通貨", "1米ドル＝3.6725 AEDで固定。円以外の資産への分散に。"),
       ("10年のゴールデンビザ", "200万AED以上の不動産購入で申請対象。"),
       ("前払い金はエスクローで保護", "完成前物件の支払いはRERA監督の専用口座へ。"),
       ("ローン不要・金利なし", "デベロッパーへの直接分割払い。海外送金でOK。")]
rows = "".join(f"<tr><td>{e(l['name'])}</td><td>{sqm(l['a0'])}{'' if l['a0'] == l['a1'] else '–' + sqm(l['a1'])} m²</td><td>AED {aed(l['p'])}〜 <small>約{yen(l['p'])}〜</small></td><td>AED {aed(l['c'])}〜 <small>約{yen(l['c'])}〜</small></td></tr>" for l in layouts)
pages.append(f"""<section class=page>
 <div class=top><div class=tl><div class=logo>IMAN<small>DEVELOPERS</small></div>
   <div class=eb>日本の不動産会社・仲介パートナー様向け</div><h1>IMANを売るための<br>パートナーガイド</h1>
   <ul class=hl><li><b>7%</b>仲介手数料</li><li><b>40/60</b>金利なしの分割払い</li><li><b>10年</b>ゴールデンビザ</li></ul></div>
  <div class=ti style="background-image:url('{src('img/113-residences.jpg')}')"></div></div>
 <h3 class=sh>なぜドバイか：日本のお客様に勧める6つの理由</h3>
 <div class=grid3>{''.join(f'<div class=card><h3><span class=no>{i+1:02d}</span>{e(t)}</h3><p>{e(x)}</p></div>' for i, (t, x) in enumerate(why))}</div>
 <h3 class=sh>IMAN Developers：完成・引き渡しの実績</h3>
 <div class=stats><div><b>{len(ready)}</b><span>引き渡し済み<br>（2017年〜）</span></div><div><b>{len(building)}</b><span>建設中</span></div>
  <div><b>完売</b><span>Oxford Cove・<br>Sierra（住宅）</span></div>
  <p>ドバイの住宅デベロッパー。JVC、アルジャン、ドバイ・ヒルズ・エステートなどで完成済み。日本のお客様が気にする「本当に完成するのか」に、実績で答えられます。</p></div>
 <h3 class=sh>主力物件：113 Residences（アル・スフー）</h3>
 <div class=r113><img src="{src('img/113-residences.jpg')}"><div>
  <p>アル・スフー・コミュニティパークの目の前、ビーチまで車で3分。パーム・ジュメイラとドバイ・マリーナまで8〜10分。B＋G＋9階・全113邸、2029年Q2引き渡し予定。屋上インフィニティプール、ラグーンプール、フィットネス、Hafeleスマートロック。</p>
  <table class=t><thead><tr><th>間取り</th><th>面積</th><th>40/60プラン（4%割引）</th><th>一括払い（14%割引）</th></tr></thead><tbody>{rows}</tbody></table></div></div>
 <p class=fine>{DATE}時点の「〜から」の最低価格。円は1 AED ≈ {JPY}円の目安。DLD登録料（4%）と登記費用は別途。税制・ビザの要件は変更される場合があります。</p>
 {foot(1)}</section>""")

# Page 2: payment, how to sell, buying steps, partner terms
sch = [(20, "予約から30日以内"), (10, "予約から90日以内"), (10, "工事進捗40%時"), (60, "引き渡し時（2029年Q2）")]
bars = "".join(f"<div class=bar style='flex:{pc + 18}'><b>{pc}%</b><span>{e(t)}</span><i>AED {aed(ex['p'] * pc / 100)}<br>約{yen(ex['p'] * pc / 100)}</i></div>" for pc, t in sch)
qa = [("現地を見に行けない", "オンライン内覧・動画・間取り図をサムがお送りします。契約まですべてリモートで、渡航は不要です。"),
      ("完成前の物件は不安", f"支払いはRERA監督のエスクロー口座へ。IMANには{len(ready)}件の引き渡し実績があります。"),
      ("為替が心配", "AEDは米ドルに固定。40/60なら支払いが2029年まで分散されます。"),
      ("税金は？", "UAE側では個人の所得税なし。日本の税務はお客様の税理士にご確認ください。")]
steps = ["住戸を選ぶ", "予約（パスポート＋予約フォーム）", "売買契約（SPA）に電子署名", "DLD登録（Oqood・4%）", "分割払い（海外送金）", "引き渡し・権利証"]
tools = [("住戸検索ページ", "パートナー様向け・本日の全空室", FINDER), ("お客様向け日本語ページ", "113 Residences紹介", LANDING), ("販売資料", "画像・動画（Google ドライブ）", MKT_113)]
pages.append(f"""<section class=page>
 <h3 class=sh style="margin-top:0">お支払い：40/60プラン（例：2ベッドルーム AED {aed(ex['p'])}〜、約{yen(ex['p'])}〜）</h3>
 <div class=bars>{bars}</div>
 <p class=note>一括払いなら定価から<b>14%割引</b>（AED {aed(ex['c'])}〜）。ゴールデンビザは200万AED以上が対象（購入価格で判定）、{gv}</p>
 <h3 class=sh>日本のお客様への売り方</h3>
 <div class=cols><div><b class=st>おすすめのお客様像</b><ul class=dots>
   <li><b>資産分散したい経営者・富裕層</b>：米ドル連動のAED建て資産として</li><li><b>ドバイ移住・二拠点生活</b>：住まいとゴールデンビザを同時に</li>
   <li><b>海外で賃貸運用したい投資家</b>：ビーチ・マリーナに近い貸しやすい立地</li><li><b>ご家族のセカンドホーム</b>：2〜3ベッドルームの広い間取り</li></ul>
   <div class=tip><b>3つのキーワード</b>「米ドル連動の資産」「金利なしの分割払い」「完成実績のあるデベロッパー」</div></div>
  <div><b class=st>よくある質問と答え方</b><div class=qa>{''.join(f'<div><b>「{e(q)}」</b><p>{e(a)}</p></div>' for q, a in qa)}</div></div></div>
 <h3 class=sh>購入の流れ：日本にいながら6ステップ</h3>
 <ol class=steps>{''.join(f'<li><span class=sn>{i+1}</span>{e(t)}</li>' for i, t in enumerate(steps))}</ol>
 <p class=note>最初の20%は予約から30日以内。資料・価格・契約・デベロッパーとのやり取りはサムが担当し、パートナー様はお客様のご紹介と日本語でのフォローをお願いします。</p>
 <h3 class=sh>パートナー条件とツール</h3>
 <div class=terms><div><b>7%</b><span>仲介手数料（販売中の全物件）</span></div><div><b>AED 50K</b><span>ボーナス：3戸成約（113 Residences）</span></div><div><b>AED 100K</b><span>ボーナス：5戸成約（113 Residences）</span></div></div>
 <div class=tools>{''.join(f'<a class=tool href="{e(u)}"><img src="{qr(u)}"><div><h3>{e(t)}</h3><p>{e(x)}</p></div></a>' for t, x, u in tools)}</div>
 <div class=contact><img src="{src('img/sam-jabr.jpg')}"><div><span class=eb>担当</span><h2>サム・ジャブル（Sam Jabr）</h2>
  <p>シニア・セールスマネージャー · IMAN Developers · ドバイ</p><p class=ph>WhatsApp +971 50 175 2771</p><p>空室確認・価格・オンライン内覧・契約まで、お気軽にご連絡ください（英語・アラビア語で対応）。</p></div>
  <img class=qr src="{qr('https://wa.me/' + WA)}"></div>
 <p class=fine>手数料の支払い時期・条件はパートナー契約の際にご確認ください。価格・空室・特典は{DATE}時点のもので、予約時に確定します。画像はイメージです。本資料は販売の申込みではありません。</p>
 {foot(2)}</section>""")

CSS = """
@page{size:A4;margin:0}
:root{--g:#1d3f2b;--g2:#264f37;--c:#c0866d;--cd:#9a5f48;--ink:#17251c;--mut:#5d6b61;--line:#dfe3dc;--bg2:#f3f1ea}
*{box-sizing:border-box}
body{margin:0;font:8.4pt/1.5 Figtree,'Noto Sans JP',sans-serif;color:var(--ink)}
h1,h2,h3{margin:0;font-weight:700;line-height:1.3}
p{margin:0}
.page{width:210mm;height:297mm;padding:12mm 13mm 15mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}
.eb{font-size:7pt;letter-spacing:.12em;color:var(--c);font-weight:700}
.foot{position:absolute;left:13mm;right:13mm;bottom:7mm;display:flex;justify-content:space-between;font-size:6.8pt;color:var(--mut);border-top:1px solid var(--line);padding-top:4px}
.fine{font-size:6.6pt;color:var(--mut);margin-top:6px}
.note{font-size:8pt;color:#36443a;margin-top:5px}.note b{color:var(--cd)}
.sh{font-size:9.6pt;color:var(--g);margin:11px 0 6px;padding-bottom:3px;border-bottom:2px solid var(--c);display:inline-block}
.card{background:var(--bg2);border-radius:7px;padding:7px 10px}
.card h3{font-size:8.8pt;color:var(--g);margin-bottom:2px}
.card p{font-size:7.6pt;color:#36443a}
.no{font-family:Marcellus,serif;color:var(--c);font-weight:400;margin-right:6px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.st{display:block;color:var(--g);font-size:8.6pt;margin-bottom:3px}
.tip{margin-top:7px;background:var(--g);color:#eef3ee;border-radius:7px;padding:7px 11px;font-size:8pt}
.tip b{display:block;color:var(--c);font-size:7pt;letter-spacing:.1em}
/* top band */
.top{display:grid;grid-template-columns:1.1fr 1fr;background:var(--g);color:#f2f5f0;border-radius:10px;overflow:hidden;height:68mm}
.tl{padding:9mm 9mm 8mm}
.ti{background-size:cover;background-position:center 35%}
.logo{color:var(--c);font-family:Marcellus,serif;letter-spacing:.42em;font-size:15pt;line-height:1;margin-bottom:9mm}
.logo small{display:block;font-size:5pt;letter-spacing:.62em;margin-top:5px}
h1{font-size:19pt;margin:5px 0 0;color:#fff}
.hl{list-style:none;padding:0;margin:10px 0 0;display:flex;gap:6px}
.hl li{border:1px solid #8a6a55;border-radius:7px;padding:4px 8px;font-size:7pt;color:#c9d6cc;flex:1}
.hl b{display:block;font-family:Marcellus,serif;font-size:15pt;color:var(--c);font-weight:400;line-height:1.2}
/* IMAN stats */
.stats{display:grid;grid-template-columns:auto auto auto 1fr;gap:6px;align-items:stretch}
.stats>div{background:var(--g);color:#fff;border-radius:7px;padding:6px 12px}
.stats b{display:block;font-family:Marcellus,'Noto Sans JP',serif;font-weight:400;font-size:17pt;color:var(--c);line-height:1.15}
.stats span{font-size:7pt;color:#c9d6cc;line-height:1.35;display:block}
.stats p{font-size:7.8pt;color:#36443a;padding-left:6px;align-self:center}
/* 113 */
.r113{display:grid;grid-template-columns:52mm 1fr;gap:9px}
.r113 img{width:100%;height:100%;max-height:78mm;object-fit:cover;border-radius:7px}
.r113 p{font-size:7.8pt;color:#36443a}
.t{width:100%;border-collapse:collapse;margin-top:6px;font-size:7.6pt}
.t th{text-align:left;background:var(--g);color:#fff;font-weight:500;padding:3px 6px;font-size:7pt}
.t td{border-bottom:1px solid var(--line);padding:4px 6px;vertical-align:top}
.t td small{display:block;color:var(--mut);font-size:6.8pt}
.t td{white-space:nowrap}.t td:first-child{white-space:normal}
/* payment */
.bars{display:flex;gap:4px}
.bar{background:var(--bg2);border-top:3px solid var(--c);border-radius:4px;padding:5px 8px;min-width:0}
.bar:last-child{background:var(--g);color:#fff}
.bar b{display:block;font-size:13pt;font-family:Marcellus,serif;font-weight:400;color:var(--cd);line-height:1.2}
.bar:last-child b{color:var(--c)}
.bar span{display:block;font-size:7.4pt}
.bar i{display:block;font-style:normal;font-size:7pt;opacity:.85;white-space:nowrap}
.dots{margin:0;padding-left:14px;font-size:7.8pt}.dots li{margin:2px 0}.dots b{color:var(--g)}
.qa{display:grid;gap:4px}
.qa div{border-left:3px solid var(--c);padding:1px 0 1px 8px}
.qa b{color:var(--g);font-size:8.2pt}.qa p{font-size:7.6pt;color:#36443a}
.steps{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(6,1fr);gap:4px}
.steps li{background:var(--bg2);border-radius:7px;padding:6px 7px;font-size:7.6pt;font-weight:500;color:var(--g);line-height:1.35}
.sn{display:grid;place-items:center;width:18px;height:18px;border-radius:50%;background:var(--g);color:#fff;font-size:8pt;font-weight:700;margin-bottom:3px}
/* terms and tools */
.terms{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.terms div{background:var(--g);color:#fff;border-radius:7px;padding:6px 11px}
.terms b{display:block;font-family:Marcellus,serif;font-weight:400;font-size:16pt;color:var(--c);line-height:1.2}
.terms span{font-size:7pt;color:#c9d6cc}
.tools{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:6px}
.tool{display:flex;gap:7px;align-items:center;border:1px solid var(--line);border-radius:7px;padding:5px 7px;text-decoration:none;color:inherit}
.tool img{width:17mm;height:17mm;flex:none}
.tool h3{font-size:8.2pt;color:var(--g)}.tool p{font-size:7pt;color:var(--mut)}
.contact{display:flex;gap:12px;align-items:center;margin-top:7px;background:var(--bg2);border-radius:9px;padding:8px 12px}
.contact>img:first-child{width:19mm;height:19mm;border-radius:50%;object-fit:cover;object-position:50% 15%}
.contact h2{font-size:12pt;color:var(--g)}.contact p{font-size:7.6pt;color:#36443a}
.contact .ph{font-weight:700;font-size:9.5pt;color:var(--g)}
.contact .qr{width:19mm;height:19mm;margin-left:auto}
"""

def main():
    at = os.path.join(REPO, "availability", "tools")
    doc = f"""<!doctype html><html lang=ja><head><meta charset=utf-8><style>
@font-face{{font-family:Marcellus;src:url(file://{at}/marcellus.woff2) format('woff2')}}
@font-face{{font-family:Figtree;src:url(file://{at}/figtree.woff2) format('woff2');font-weight:300 900}}
{fonts_css()}
{CSS}</style></head><body>{''.join(pages)}</body></html>"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = os.path.join(os.path.dirname(OUT), "_brochure.html")
    open(tmp, "w").write(doc)
    with sync_playwright() as pw:
        exe = "/opt/pw-browsers/chromium"  # the pre-installed browser, when the Python Playwright has none of its own
        b = pw.chromium.launch(**({"executable_path": exe} if os.path.exists(exe) else {}))
        pg = b.new_page()
        pg.goto("file://" + tmp)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        pg.pdf(path=OUT, format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    os.remove(tmp)
    print("wrote", os.path.relpath(OUT, REPO))


if __name__ == "__main__":
    main()
