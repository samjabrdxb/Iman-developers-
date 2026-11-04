"""Japanese partner brochure: how to sell IMAN, for real estate brokers in Japan.

Usage:  python3 marketing/tools/japan_brochure.py

Writes marketing/japan/iman-japan-partner-guide.pdf (A4 portrait, 8 pages).
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
    return f"""<div class=foot><span>サム・ジャブル（Sam Jabr）· IMAN Developers · WhatsApp +971 50 175 2771</span><span>{n} / 8</span></div>"""


def head(k, h, sub=""):
    return f"""<div class=eb>{k}</div><h2>{h}</h2>{f'<p class=lead>{sub}</p>' if sub else ''}"""


pages = []

# 1. Cover
pages.append(f"""<section class="page cover">
 <div class=cimg style="background-image:url('{src('img/113-residences.jpg')}')"><div class=logo>IMAN<small>DEVELOPERS</small></div></div>
 <div class=cbody>
  <div class=eb>日本の不動産会社・仲介パートナー様向け</div>
  <h1>IMANを売るための<br>パートナーガイド</h1>
  <p class=cp>ドバイの新築レジデンスを、日本のお客様へ。物件の魅力、お客様への伝え方、購入の流れ、パートナー条件をこの一冊にまとめました。</p>
  <ul class=hl>
   <li><b>7%</b>仲介手数料</li><li><b>40/60</b>金利なしの分割払い</li><li><b>10年</b>ゴールデンビザ（200万AED〜）</li>
  </ul>
  <div class=me><img src="{src('img/sam-jabr.jpg')}"><div><b>サム・ジャブル（Sam Jabr）</b><span>シニア・セールスマネージャー · IMAN Developers</span>
   <a href="https://wa.me/{WA}">WhatsApp +971 50 175 2771</a></div><span class=dt>{DATE}版</span></div>
 </div></section>""")

# 2. Why Dubai
why = [("外国人でも完全所有", "指定エリア（フリーホールド）では、外国人も土地・建物を100%所有でき、登記はドバイ土地局（DLD）が管理します。"),
       ("UAEでは個人所得税なし", "UAEには個人の所得税・キャピタルゲイン税がありません。※日本居住者は日本で課税されます。詳しくは税理士にご確認ください。"),
       ("米ドルに連動する通貨", "UAEディルハムは1米ドル＝3.6725 AEDで固定。円以外の資産を持ちたいお客様の分散先になります。"),
       ("10年のゴールデンビザ", "200万AED以上の不動産購入で、UAEの10年居住ビザ（ゴールデンビザ）の申請対象になります。"),
       ("前払い金はエスクローで保護", "完成前物件の支払いは、ドバイの規制当局（RERA）が監督するプロジェクト専用のエスクロー口座に入ります。"),
       ("ローン不要の分割払い", "デベロッパーへの直接分割払いで、銀行審査も金利もありません。海外からの送金で支払えます。")]
pages.append(f"""<section class=page>{head("01 · なぜドバイか", "日本のお客様に<br>ドバイを勧める理由", "円安・資産分散・海外拠点づくり。ドバイ不動産は、日本の投資家が求める条件をそろえています。")}
 <div class=grid2>{''.join(f'<div class=card><span class=no>{i+1:02d}</span><h3>{e(t)}</h3><p>{e(x)}</p></div>' for i, (t, x) in enumerate(why))}</div>
 <p class=fine>税制・ビザの要件は変更される場合があります。お客様には最新情報をご確認のうえご案内ください。</p>{foot(2)}</section>""")

# 3. About IMAN
ready_li = "".join(f"<li><b>{e(p['name'])}</b><span>{e(AREA_JA.get(p['area'], p['area']))} · {e(p['handover'])}年</span></li>" for p in ready)
build_li = "".join(f"<li><b>{e(p['name'])}</b><span>{e(AREA_JA.get(p['area'], p['area']))} · 進捗{p['progress']}%</span></li>" for p in building)
pics = ["the-grove-by-iman", "oxford-gardens", "oxford-terraces-2"]
pages.append(f"""<section class=page>{head("02 · IMAN Developersについて", "完成・引き渡しの<br>実績があるデベロッパー",
  f"IMAN Developersはドバイの住宅デベロッパーです。2017年以降に{len(ready)}つのプロジェクトを引き渡し、現在{len(building)}つが建設中。日本のお客様が最も気にする「本当に完成するのか」に、実績で答えられます。")}
 <div class=pics>{''.join(f'<figure><img src="{src(P[k]["image"])}"><figcaption>{e(P[k]["name"])} · 完成済み</figcaption></figure>' for k in pics)}</div>
 <div class=cols><div><h3 class=sh>引き渡し済み（{len(ready)}件）</h3><ul class=plist>{ready_li}</ul></div>
  <div><h3 class=sh>建設中（{len(building)}件）</h3><ul class=plist>{build_li}</ul>
  <h3 class=sh style="margin-top:14px">新規販売</h3><ul class=plist><li><b>113 Residences</b><span>アル・スフー · 販売中</span></li>
   <li><b>Oxford Cove</b><span>JVC · 完売</span></li><li><b>Sierra by Iman</b><span>モーターシティ · 住宅は完売、店舗のみ販売中</span></li></ul></div></div>
 <div class=tip><b>セールスのポイント</b>Oxford CoveとSierraの住宅は完売しました。人気のある物件は早く売れることを、お客様にお伝えください。</div>
 {foot(3)}</section>""")

# 4. 113 Residences
rows = "".join(f"<tr><td>{e(l['name'])}</td><td>{sqm(l['a0'])}{'' if l['a0'] == l['a1'] else '–' + sqm(l['a1'])} m²</td><td>AED {aed(l['p'])}〜<small>約{yen(l['p'])}〜</small></td><td>AED {aed(l['c'])}〜<small>約{yen(l['c'])}〜</small></td></tr>" for l in layouts)
pages.append(f"""<section class=page>{head("03 · 主力物件", "113 Residences<br>公園とビーチのそばに")}
 <div class=hero113><img src="{src('img/113-residences.jpg')}"><div class=facts>
  <div><b>アル・スフー</b><span>パーム・ジュメイラとドバイ・マリーナの間</span></div><div><b>B＋G＋9階</b><span>全113邸</span></div>
  <div><b>2029年Q2</b><span>引き渡し予定</span></div><div><b>{len(r113['units'])}戸</b><span>販売中（{DATE}時点）</span></div></div></div>
 <p class=lead style="margin-top:12px">アル・スフー・コミュニティパークの目の前。流れるようなファサード、広いテラス、上質な仕上げ。Hafeleのスマートロック、欧州製キッチン家電、ラグーンプールと屋上インフィニティプール、フィットネスセンターとヨガルーム。</p>
 <table class=t><thead><tr><th>間取り</th><th>面積</th><th>40/60プラン（4%割引）</th><th>一括払い（14%割引）</th></tr></thead><tbody>{rows}</tbody></table>
 <div class=cols><div><h3 class=sh>車での所要時間</h3><ul class=drive>{''.join(f'<li><span>{e(n)}</span><b>{m}分</b></li>' for n, m in DRIVE)}</ul></div>
  <div><h3 class=sh>こんなお客様に</h3><ul class=dots><li>ビーチと公園のそばで、ゆとりのある広さを求める方</li><li>200万AED以上でゴールデンビザも視野に入れたい方</li>
   <li>2029年の完成まで、金利なしで少しずつ支払いたい方</li><li>パーム・ジュメイラやマリーナに近い立地で賃貸も考える方</li></ul></div></div>
 <p class=fine>価格は「〜から」の最低価格（AED）。円は1 AED ≈ {JPY}円の目安です。DLD登録料（4%）と登記費用は別途です。</p>{foot(4)}</section>""")

# 5. Payment plans
sch = [(20, "予約から30日以内"), (10, "予約から90日以内"), (10, "工事進捗40%時"), (60, "引き渡し時（2029年Q2）")]
gv = ("113 Residencesは40/60プランなら全住戸が200万AED以上です。" if min(l["p"] for l in layouts) >= 2e6
      else "113 Residencesの多くの住戸が対象です。")
bars = "".join(f"<div class=bar style='flex:{pc + 18}'><b>{pc}%</b><span>{e(t)}</span><i>AED {aed(ex['p'] * pc / 100)}<br>約{yen(ex['p'] * pc / 100)}</i></div>" for pc, t in sch)
rt = "".join(f"<tr><td>{e(u['no'])}</td><td>{round(u['area'] * 0.092903)} m²</td><td>AED {aed(u['op'] * (1 - RD))}</td><td>AED {aed(u['op'] * (1 - RC))}</td></tr>" for u in retail)
pages.append(f"""<section class=page>{head("04 · お支払い", "40/60プランで<br>完成まで6割を後払いに", "建設中に40%、鍵の引き渡し時に60%。銀行ローンも金利もありません。")}
 <h3 class=sh>例：2ベッドルーム（AED {aed(ex['p'])}〜、約{yen(ex['p'])}〜）</h3>
 <div class=bars>{bars}</div>
 <div class=grid3><div class=card><h3>一括払い</h3><p>定価から<b class=big>14%</b>割引。最も大きな割引です。2ベッドルームならAED {aed(ex['c'])}〜。</p></div>
  <div class=card><h3>購入時の諸費用</h3><p>ドバイ土地局（DLD）登録料 <b class=big>4%</b> と登記手数料。売買価格とは別にお支払いいただきます。</p></div>
  <div class=card><h3>ゴールデンビザ</h3><p>200万AED以上の物件が対象（購入価格で判定）。{gv}</p></div></div>
 <h3 class=sh style="margin-top:18px">Sierra by Iman · 店舗（モーターシティ）</h3>
 <p class=lead>商業用の投資物件をお探しのお客様に。40/60プランで{round(RD * 100)}%割引、一括払いで{round(RC * 100)}%割引。</p>
 <table class=t><thead><tr><th>店舗</th><th>面積</th><th>40/60プラン</th><th>一括払い</th></tr></thead><tbody>{rt}</tbody></table>
 <div class=tip><b>近日公開</b>The Element by IMAN（ドバイ・サイエンスパーク）：スタジオ〜2ベッドルームの170邸と店舗。EOI（購入意向登録）の詳細は発表待ちです。ご興味のあるお客様はお早めにサムまで。</div>
 {foot(5)}</section>""")

# 6. How to sell
who = [("資産を分散したい経営者・富裕層", "円以外の通貨・海外の実物資産を持ちたい方。米ドル連動のAED建て資産として提案できます。"),
       ("ドバイ移住・二拠点生活を考える方", "200万AED以上の購入でゴールデンビザの申請対象に。住まいとビザを同時に検討できます。"),
       ("海外で賃貸運用をしたい投資家", "観光客・駐在員の多いドバイで、ビーチやマリーナに近い立地は貸しやすいエリアです。"),
       ("ご家族のセカンドホームに", "教育や休暇でドバイに滞在するご家族に。2〜3ベッドルームの広い間取りが合います。")]
qa = [("現地を見に行けない", "オンライン内覧、住戸の動画、間取り図、支払い表をサムがお送りします。契約まですべてリモートで完結し、ドバイへの渡航は不要です。"),
      ("完成前の物件は不安", "支払いはRERAが監督するエスクロー口座へ。IMANには{n}件の引き渡し実績があり、建設中の物件も工事が進んでいます。".format(n=len(ready))),
      ("為替が心配", "AEDは米ドルに固定されています。40/60プランなら支払いが2029年まで分散され、為替のタイミングも分けられます。"),
      ("税金はどうなるのか", "UAE側では個人の所得税・キャピタルゲイン税はありません。日本の税務については、お客様の税理士にご確認いただくようお伝えください。")]
pages.append(f"""<section class=page>{head("05 · 売り方", "日本のお客様への<br>伝え方")}
 <h3 class=sh>おすすめのお客様像</h3>
 <div class=grid2>{''.join(f'<div class=card><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in who)}</div>
 <h3 class=sh style="margin-top:16px">よくある質問と答え方</h3>
 <div class=qa>{''.join(f'<div><b>「{e(q)}」</b><p>{e(a)}</p></div>' for q, a in qa)}</div>
 <div class=tip><b>3つのキーワード</b>「米ドル連動の資産」「金利なしの分割払い」「完成実績のあるデベロッパー」。最初の説明はこの3点に絞ると伝わりやすくなります。</div>
 {foot(6)}</section>""")

# 7. Buying process
steps = [("住戸を選ぶ", "住戸検索ページで、ご予算・間取り・支払いプランから住戸を選びます。空室はサムにWhatsAppで確認。"),
         ("予約する", "お客様のパスポートのコピーと予約フォームで住戸を押さえます。最初の20%は予約から30日以内のお支払いです。"),
         ("売買契約（SPA）", "デベロッパーとの売買契約書に署名します。電子署名・リモートで対応できます。"),
         ("DLDに登録", "ドバイ土地局に購入を登録（Oqood）。登録料4%と登記手数料をお支払いいただきます。"),
         ("分割払い", "プランに沿って、海外送金で残りをお支払い。サムが支払い時期をご案内します。"),
         ("引き渡し", "完成後、残金を支払い鍵を受け取ります。権利証（タイトルディード）が発行されます。")]
pages.append(f"""<section class=page>{head("06 · 購入の流れ", "日本にいながら<br>6ステップで購入", "すべてリモートで進められます。各ステップでサムがお客様とパートナー様をサポートします。")}
 <ol class=steps>{''.join(f'<li><span class=sn>{i+1}</span><div><h3>{e(t)}</h3><p>{e(x)}</p></div></li>' for i, (t, x) in enumerate(steps))}</ol>
 <div class=tip><b>パートナー様の役割</b>お客様のご紹介と日本語でのフォロー。物件資料、価格、契約手続き、デベロッパーとのやり取りはサムが担当します。</div>
 {foot(7)}</section>""")

# 8. Partner terms and tools
tools = [("住戸検索ページ（パートナー様向け）", "本日の全空室を、ご予算・エリア・支払いプランで検索。お客様用の日本語説明をワンタップでコピーできます。", FINDER),
         ("お客様向け日本語ページ", "113 Residencesの日本語紹介ページ。お客様にそのまま送れます。", LANDING),
         ("113 Residences 販売資料", "パンフレット・画像・動画（Google ドライブ）。", MKT_113)]
pages.append(f"""<section class=page>{head("07 · パートナー条件", "一緒に売るための<br>条件とツール")}
 <div class=terms><div><b>7%</b><span>仲介手数料<br>（販売中の全物件）</span></div><div><b>AED 50K</b><span>ボーナス：3戸成約<br>（113 Residences）</span></div><div><b>AED 100K</b><span>ボーナス：5戸成約<br>（113 Residences）</span></div></div>
 <p class=fine style="margin-top:6px">手数料の支払い時期・条件は、パートナー契約の際にご確認ください。ボーナスの条件は変更される場合があります。</p>
 <h3 class=sh style="margin-top:16px">営業ツール</h3>
 <div class=tools>{''.join(f'<a class=tool href="{e(u)}"><img src="{qr(u)}"><div><h3>{e(t)}</h3><p>{e(x)}</p></div></a>' for t, x, u in tools)}</div>
 <div class=contact><img src="{src('img/sam-jabr.jpg')}"><div><span class=eb style="color:var(--c)">担当</span><h2>サム・ジャブル（Sam Jabr）</h2>
  <p>シニア・セールスマネージャー · IMAN Developers · ドバイ</p><p class=ph>WhatsApp +971 50 175 2771</p><p>英語・アラビア語で対応します。空室確認、価格、オンライン内覧、契約まで、お気軽にご連絡ください。</p></div>
  <img class=qr src="{qr('https://wa.me/' + WA)}"></div>
 <p class=fine>価格・空室・特典は{DATE}時点のもので、予約時に確定します。画像はイメージです。円換算は1 AED ≈ {JPY}円の目安です。本資料は販売の申込みではありません。</p>
 {foot(8)}</section>""")

CSS = """
@page{size:A4;margin:0}
:root{--g:#1d3f2b;--g2:#264f37;--c:#c0866d;--cd:#9a5f48;--ink:#17251c;--mut:#5d6b61;--line:#dfe3dc;--bg2:#f3f1ea}
*{box-sizing:border-box}
body{margin:0;font:9.2pt/1.6 Figtree,'Noto Sans JP',sans-serif;color:var(--ink)}
h1,h2,h3{margin:0;font-weight:700;line-height:1.3}
p{margin:0}
.page{width:210mm;height:297mm;padding:16mm 15mm 18mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}
.eb{font-size:7.5pt;letter-spacing:.12em;color:var(--cd);font-weight:700}
h2{font-size:21pt;margin-top:6px;color:var(--g)}
.lead{color:var(--mut);margin-top:8px;font-size:9.6pt}
.foot{position:absolute;left:15mm;right:15mm;bottom:8mm;display:flex;justify-content:space-between;font-size:7pt;color:var(--mut);border-top:1px solid var(--line);padding-top:5px}
.fine{font-size:7pt;color:var(--mut);margin-top:10px}
.sh{font-size:10pt;color:var(--g);margin-top:14px;margin-bottom:6px;padding-bottom:4px;border-bottom:2px solid var(--c);display:inline-block}
.card{background:var(--bg2);border-radius:8px;padding:11px 13px}
.card h3{font-size:10.5pt;color:var(--g);margin-bottom:4px}
.card p{font-size:8.6pt;color:#36443a}
.card .no{font-family:Marcellus,serif;color:var(--c);font-size:13pt;display:block;margin-bottom:2px}
.big{font-size:12pt;color:var(--cd)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:14px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:14px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:6px}
.tip{margin-top:14px;background:var(--g);color:#eef3ee;border-radius:8px;padding:10px 14px;font-size:8.8pt}
.tip b{display:block;color:var(--c);font-size:8pt;letter-spacing:.1em;margin-bottom:2px}
/* cover */
.cover{padding:0}
.cimg{height:150mm;background-size:cover;background-position:center 40%;position:relative}
.cimg::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,20,14,.55),rgba(10,20,14,0) 40%)}
.logo{position:absolute;z-index:1;left:15mm;top:14mm;color:#fff;font-family:Marcellus,serif;letter-spacing:.42em;font-size:20pt;line-height:1}
.logo small{display:block;font-size:6pt;letter-spacing:.62em;margin-top:6px}
.cbody{background:var(--g);color:#f2f5f0;height:147mm;padding:12mm 15mm}
.cbody .eb{color:var(--c)}
.cover h1{font-size:28pt;margin:8px 0 10px;color:#fff}
.cp{color:#c9d6cc;font-size:10pt;max-width:150mm}
.hl{list-style:none;padding:0;margin:14px 0 0;display:flex;gap:8px}
.hl li{border:1px solid #8a6a55;border-radius:8px;padding:7px 12px;font-size:8pt;color:#c9d6cc;flex:1}
.hl b{display:block;font-family:Marcellus,serif;font-size:20pt;color:var(--c);font-weight:400;line-height:1.2}
.me{display:flex;gap:12px;align-items:center;margin-top:16px;background:var(--g2);border-radius:10px;padding:10px 12px}
.me img{width:46px;height:46px;border-radius:50%;object-fit:cover;object-position:50% 15%}
.me b{display:block;font-size:11pt}.me span{display:block;color:#c9d6cc;font-size:8pt}.me a{color:#fff;font-weight:700;text-decoration:none;font-size:9.5pt}
.me .dt{margin-left:auto;align-self:flex-end}
/* about */
.pics{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:14px}
.pics figure{margin:0}.pics img{width:100%;height:36mm;object-fit:cover;border-radius:6px;display:block}
.pics figcaption{font-size:7.5pt;color:var(--mut);margin-top:3px}
.plist{list-style:none;padding:0;margin:0}
.plist li{display:flex;justify-content:space-between;gap:8px;border-bottom:1px solid var(--line);padding:3.5px 0;font-size:8.6pt}
.plist span{color:var(--mut)}
/* 113 */
.hero113{display:grid;grid-template-columns:1.25fr 1fr;gap:10px;margin-top:12px}
.hero113 img{width:100%;height:58mm;object-fit:cover;border-radius:8px}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.facts div{background:var(--bg2);border-radius:8px;padding:8px 10px}
.facts b{display:block;font-size:12pt;color:var(--g)}.facts span{font-size:7.6pt;color:var(--mut)}
.t{width:100%;border-collapse:collapse;margin-top:12px;font-size:8.6pt}
.t th{text-align:left;background:var(--g);color:#fff;font-weight:500;padding:5px 8px;font-size:8pt}
.t td{border-bottom:1px solid var(--line);padding:5px 8px;vertical-align:top}
.t td small{display:block;color:var(--mut);font-size:7.3pt}
.drive{list-style:none;padding:0;margin:0}
.drive li{display:flex;justify-content:space-between;border-bottom:1px solid var(--line);padding:2.5px 0;font-size:8.4pt}
.dots{margin:0;padding-left:16px;font-size:8.6pt}.dots li{margin:3px 0}
/* payment */
.bars{display:flex;gap:4px;margin-top:4px}
.bar{background:var(--bg2);border-top:4px solid var(--c);border-radius:4px;padding:8px 9px;min-width:0}
.bar:last-child{background:var(--g);color:#fff;border-top-color:var(--c)}
.bar b{display:block;font-size:15pt;font-family:Marcellus,serif;font-weight:400;color:var(--cd)}
.bar:last-child b{color:var(--c)}
.bar span{display:block;font-size:7.8pt}
.bar i{display:block;font-style:normal;font-size:7.6pt;margin-top:5px;opacity:.85}
/* how to sell */
.qa{display:grid;gap:6px}
.qa div{border-left:3px solid var(--c);padding:3px 0 3px 10px}
.qa b{color:var(--g);font-size:9.4pt}.qa p{font-size:8.6pt;color:#36443a}
/* steps */
.steps{list-style:none;padding:0;margin:16px 0 0;display:grid;gap:9px}
.steps li{display:flex;gap:12px;align-items:flex-start;background:var(--bg2);border-radius:8px;padding:11px 13px}
.sn{flex:none;width:28px;height:28px;border-radius:50%;background:var(--g);color:#fff;display:grid;place-items:center;font-weight:700;font-size:11pt}
.steps h3{font-size:11pt;color:var(--g)}.steps p{font-size:8.8pt;color:#36443a}
/* terms */
.terms{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:14px}
.terms div{background:var(--g);color:#fff;border-radius:8px;padding:11px 13px}
.terms b{display:block;font-family:Marcellus,serif;font-weight:400;font-size:21pt;color:var(--c);line-height:1.15}
.terms span{font-size:8pt;color:#c9d6cc}
.tools{display:grid;gap:7px}
.tool{display:flex;gap:12px;align-items:center;border:1px solid var(--line);border-radius:8px;padding:7px 10px;text-decoration:none;color:inherit}
.tool img{width:21mm;height:21mm;flex:none}
.tool h3{font-size:9.6pt;color:var(--g)}.tool p{font-size:8.2pt;color:var(--mut)}
.contact{display:flex;gap:14px;align-items:center;margin-top:14px;background:var(--bg2);border-radius:10px;padding:12px 14px}
.contact>img:first-child{width:24mm;height:24mm;border-radius:50%;object-fit:cover;object-position:50% 15%}
.contact h2{font-size:14pt;margin-top:2px}.contact p{font-size:8.4pt;color:#36443a}
.contact .ph{font-weight:700;font-size:10.5pt;color:var(--g)}
.contact .qr{width:24mm;height:24mm;margin-left:auto}
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
