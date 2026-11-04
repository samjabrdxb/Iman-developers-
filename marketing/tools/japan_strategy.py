"""Japanese sales strategy brochure: "affordable luxury, quality over quantity", for brokers in Japan.

Usage:  python3 marketing/tools/japan_strategy.py

Writes marketing/japan/iman-japan-sales-strategy.pdf (A4 portrait, 2 pages), from
Sam's "Sales Strategy for Japanese Brokers & International Investors" text.
Reuses the fonts, QR codes and links of japan_brochure.py.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from japan_brochure import fonts_css, qr, src, e, WA, FINDER, REPO, P
from playwright.sync_api import sync_playwright

OUT = os.path.join(REPO, "marketing", "japan", "iman-japan-sales-strategy.pdf")

# Track record (from Sam, November 2026)
LAUNCHED, DELIVERED, DEC_2026, PIPELINE = 18, 9, 2, 550


def quote(x):
    return f"<blockquote>{e(x)}</blockquote>"


def foot(n):
    return f"""<div class=foot><span>サム・ジャブル（Sam Jabr）· IMAN Developers · WhatsApp +971 50 175 2771</span><span>{n} / 2</span></div>"""


compare = [("販売価格", "同価格帯の物件と比べた実際の価格"), ("間取り", "無駄のない間取りと実際の図面"), ("天井高", "承認済みの実際の仕様"),
           ("ロビー・共用部", "デザインと仕上げの質"), ("アメニティ", "質・数・種類"), ("総戸数", "住環境の密度と住み心地"),
           ("引き渡し実績", "完成・引き渡し済みのプロジェクト"), ("支払いプラン", "分割の内容と工事の節目"), ("再販の可能性", "過去の取引と比較データ")]

p1 = f"""<section class=page>
 <div class=top><div class=tl><div class=logo>IMAN<small>DEVELOPERS</small></div>
   <div class=eb>日本の仲介パートナー様・海外投資家向け セールス戦略</div>
   <h1>手の届くラグジュアリー。<br>量より質。</h1>
   <p class=tp>住戸は少なく、アメニティは豊かに。細部まで丁寧に、価格は手の届く水準で。</p></div>
  <div class=ti style="background-image:url('{src(P['oxford-212']['image'])}')"><span>Oxford 212 · 完成済み</span></div></div>

 <div class=stats><div><b>{LAUNCHED}</b><span>発表済みプロジェクト</span></div><div><b>{DELIVERED}</b><span>引き渡し済み</span></div>
  <div><b>+{DEC_2026}</b><span>2026年12月に引き渡し予定</span></div><div><b>{DELIVERED + DEC_2026}</b><span>2026年末の引き渡し実績（予定）</span></div></div>

 <div class=cols>
  <div><h3 class=sh>1. 物件ではなく、デベロッパーの哲学を売る</h3>
   <p>IMAN Developersは「量より質」を重視するブティック型のデベロッパーです。数千戸を供給する大手とは違い、丁寧に設計した少数のレジデンスに集中しています。超高級価格帯に入らずに、上質な住まいを求める投資家に選ばれる理由です。</p></div>
  <div><h3 class=sh>2. 引き渡し実績で信頼をつくる</h3>
   <p>遠隔で購入する海外のお客様にとって、デベロッパーの実績は最も重要です。完成した建物で、仕上げ・共用部・アメニティの実際の質を確かめていただけます。</p>
   {quote("IMANなら、完成予想図だけで判断する必要はありません。完成したプロジェクトが、品質と暮らしへの姿勢を示しています。")}</div>
 </div>

 <h3 class=sh>3. 「手の届くラグジュアリー」とは：安い建物ではなく、価格以上の住体験</h3>
 <div class=grid3>
  <div class=card><h4>エントランスの体験</h4><ul><li>印象的なエントランスロビー</li><li>一部物件では吹き抜けの高い天井</li><li>上質な素材・色・建築ディテール</li><li>考え抜かれた動線</li></ul></div>
  <div class=card><h4>住戸の体験</h4><ul><li>広く使いやすい間取り</li><li>一部の設計で天井高 約3.2m</li><li>質の高い仕上げと素材</li><li>モダンな内外装デザイン</li></ul></div>
  <div class=card><h4>ライフスタイルの体験</h4><ul><li>プール</li><li>フィットネス・ウェルネス施設</li><li>くつろぎとファミリーの空間</li><li>屋上アメニティ（一部物件は複数のエリア）</li></ul></div>
 </div>
 {quote("IMANのラグジュアリーは、住戸のドアを開けた時ではなく、建物に足を踏み入れた瞬間から始まります。")}

 <div class=cols>
  <div><h3 class=sh>4. ブティック規模を投資の強みに</h3>
   <ul class=dots><li>落ち着いた、親密な住環境</li><li>プライバシーの感じやすさ</li><li>個性のある建築デザイン</li><li>計画的に配置された共用空間</li><li>高密度の大規模物件とは違う暮らし</li></ul>
   <p class=sm>2026年のブティック案件（Oxford Cove、113 Residences、ドバイ・サイエンスパークの新プロジェクト）は合計約{PIPELINE}戸です。</p>
   {quote("IMANが最大化するのは住戸の数ではなく、住まいの質です。")}
   <p class=warn>戸数が少ないことが、低密度・プライバシー・値上がりを自動的に保証するわけではありません。実際の図面と仕様で裏付けてください。</p></div>
  <div><h3 class=sh>5. 価格だけでなく、全体の価値を売る</h3>
   <p class=sm>割引だけを強調せず、同等の物件と次の項目で比べてください。</p>
   <table class=t><thead><tr><th>比較項目</th><th>パートナー様が示すこと</th></tr></thead><tbody>
   {''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in compare)}</tbody></table>
   {quote("大切なのは価格そのものではなく、その価格でどれだけの質・広さ・暮らし・長期的な価値が得られるかです。")}</div>
 </div>
 {foot(1)}</section>"""

steps = ["IMANのブティック型の哲学", "完成物件と引き渡し実績", "実際の品質・間取り・アメニティ", "同価格帯の物件との比較",
         "支払い・SPA・エスクロー・引き渡し・購入手続き（公式資料で）", "空室のご案内と質疑応答、その後に予約のご相談"]
p2 = f"""<section class=page>
 <div class=grid3>
  <div class=card><h4>6. 工事連動の支払いは「透明性」</h4><p>一部の支払いプランでは、合意した工事スケジュールに沿って分割払いを行います（例：113 Residencesは工事進捗40%時に10%）。支払いと工事の進み具合の関係が分かりやすくなります。</p>
   <p class=warn>必ず最新の公式支払いプランを使用してください。すべての支払いが工事連動である、または工事が進むまで支払い義務がない、とは説明しないでください。</p></div>
  <div class=card><h4>7. 完成物件で品質を見せる</h4><p>渡航できない日本のお客様には、目で見られる証拠が大切です。完成例として<b>Oxford 212</b>の外観、エントランスとロビー、内装、廊下とエレベーター、アメニティ、屋上、仕上げを実際の映像でご紹介ください。</p>
   <p class=warn>完成物件の映像を先に見せ、その後に新規物件の完成予想図へ。完成物件の特徴と、販売物件の仕様は必ず区別してください。</p></div>
  <div class=card><h4>8. 過去の実績は慎重に</h4><p>当初の購入価格、確認済みの再販価格、記録のある賃貸実績、周辺相場、管理費などの保有コストを比べてください。Oxford 212の値上がりは、根拠のない数字ではなく実際の取引で示します。</p>
   <p class=warn>過去の実績は将来の利回りを保証するものではありません。</p></div>
 </div>
 {quote("将来の予測だけに頼っていただく必要はありません。すでに完成した物件と、その実績をご自身で確かめてください。")}

 <h3 class=sh>9. 日本のお客様向けプレゼンテーションの順番</h3>
 <ol class=steps>{''.join(f'<li><span class=sn>{i+1}</span>{e(t)}</li>' for i, t in enumerate(steps))}</ol>
 <p class=sm style="margin-top:5px">日本のお客様には、分かりやすさ・正確さ・確認できる情報が何より大切です。誇張した表現、強引なクロージング、根拠のない約束は避け、図面・仕様・確認済みの価格・契約書類をそろえた資料でご案内ください。<b>証拠・透明性・一貫性で信頼を築きます。</b></p>

 <div class=cols>
  <div><h3 class=sh>10. 次の案件：ドバイ・サイエンスパーク</h3>
   <div class=dsp><img src="{src('img/dsp-teaser.jpg')}"><ul class=facts>
    <li><b>約170戸</b>スタジオ・1〜2ベッドルーム</li><li><b>B＋G＋10階</b>ブティック規模</li>
    <li><b>2026年11月末</b>発売予定</li><li><b>2029年Q3</b>引き渡し予定</li></ul></div>
   <p class=warn>仕様・価格・支払いプラン・空室・割引は最新の公式発表でご確認ください。規模の小ささを、希少性による値上がりの保証のように説明しないでください。</p>
   <h3 class=sh>おすすめのクロージング</h3>
   <p class=sm>実績と価値をご説明したあとに、こう伺います。</p>
   {quote("ご覧いただいた内容から、賃貸収入を重視したスタジオ（ドバイ・サイエンスパーク）と、賃貸需要と将来の売却のバランスが取れた広めの住戸（113 Residences）では、どちらがお好みですか？")}
   <p class=sm>お答えに合わせて住戸タイプを選び、確認済みの空室、公式の支払いプラン、購入にかかる費用の総額をご案内します。急いで予約を迫るのではなく、お客様に合う選択へご案内することが目的です。</p></div>
  <div><h3 class=sh>お客様へのトークスクリプト</h3>
   <div class=pitch><p>「ドバイへの投資先として、IMAN Developersをおすすめする理由をご説明します。</p>
    <p>IMANは数千戸を建てるデベロッパーではなく、量より質を大切にするブティック型のデベロッパーです。上質なデザイン、使いやすい間取り、美しいエントランスロビー、質の高い仕上げ、充実したアメニティを、手の届く価格で提供する「手の届くラグジュアリー」を掲げています。</p>
    <p>特に注目していただきたいのは引き渡しの実績です。すでに9つのプロジェクトを引き渡しており、将来の約束だけでなく、実際の建物でご判断いただけます。</p>
    <p>IMANの物件を買うことは、住戸だけでなく、エントランスからアメニティまで丁寧に設計された住環境に投資することです。ぜひ、ドバイの同等の物件と、実際の品質と価値を比べてみてください。</p>
    <p>手の届くラグジュアリー。量より質。暮らし全体の体験です。」</p></div></div>
 </div>

 <div class=final><div><span class=eb>パートナー様へ</span><h2>IMANを「最も安いデベロッパー」として売らないでください。</h2>
  <p class=formula><b>上質な品質</b>＋<b>ライフスタイル・アメニティ</b>＋<b>考え抜かれたデザイン</b>＋<b>手の届く価格</b>＋<b>引き渡し実績</b></p>
  <p>これがIMAN Developersの「手の届くラグジュアリー」の土台です。</p></div>
  <div class=qrs><figure><img src="{qr('https://wa.me/' + WA)}"><figcaption>サムにWhatsApp</figcaption></figure><figure><img src="{qr(FINDER)}"><figcaption>住戸検索ページ</figcaption></figure></div></div>
 {foot(2)}</section>"""

CSS = """
@page{size:A4;margin:0}
:root{--g:#1d3f2b;--g2:#264f37;--c:#c0866d;--cd:#9a5f48;--ink:#17251c;--mut:#5d6b61;--line:#dfe3dc;--bg2:#f3f1ea}
*{box-sizing:border-box}
body{margin:0;font:8.2pt/1.52 Figtree,'Noto Sans JP',sans-serif;color:var(--ink)}
h1,h2,h3,h4{margin:0;font-weight:700;line-height:1.3}
p{margin:0}
ul{margin:0;padding-left:13px}li{margin:1px 0}
.page{width:210mm;height:297mm;padding:11mm 12mm 14mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}
.eb{font-size:6.8pt;letter-spacing:.1em;color:var(--c);font-weight:700}
.foot{position:absolute;left:12mm;right:12mm;bottom:6mm;display:flex;justify-content:space-between;font-size:6.6pt;color:var(--mut);border-top:1px solid var(--line);padding-top:4px}
.sh{font-size:9pt;color:var(--g);margin:9px 0 5px;padding-bottom:2px;border-bottom:2px solid var(--c);display:inline-block}
.sm{font-size:7.8pt;color:#36443a;margin-top:4px}
.warn{font-size:6.9pt;color:var(--cd);background:#f8ede7;border-radius:5px;padding:4px 7px;margin-top:5px}
blockquote{margin:6px 0 0;padding:5px 9px;border-left:3px solid var(--c);background:var(--bg2);border-radius:0 6px 6px 0;color:var(--g);font-weight:500;font-size:8pt}
blockquote::before{content:"“";font-family:Marcellus,serif;color:var(--c);font-size:13pt;line-height:0;vertical-align:-4px;margin-right:3px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.cols>div>p{font-size:8pt;color:#36443a}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.card{background:var(--bg2);border-radius:7px;padding:7px 9px}
.card h4{font-size:8.6pt;color:var(--g);margin-bottom:3px}
.card p,.card li{font-size:7.7pt;color:#36443a}
.top{display:grid;grid-template-columns:1.15fr 1fr;background:var(--g);color:#f2f5f0;border-radius:10px;overflow:hidden;height:66mm}
.tl{padding:8mm 8mm 7mm}
.ti{background-size:cover;background-position:center;position:relative}
.ti span{position:absolute;left:0;bottom:0;background:var(--g2);color:#fff;font-size:6.8pt;padding:3px 9px;border-top-right-radius:7px}
.logo{color:var(--c);font-family:Marcellus,serif;letter-spacing:.42em;font-size:14pt;line-height:1;margin-bottom:6mm}
.logo small{display:block;font-size:5pt;letter-spacing:.62em;margin-top:5px}
h1{font-size:18pt;margin:5px 0 0;color:#fff;white-space:nowrap}
.tp{color:#c9d6cc;font-size:8.4pt;margin-top:7px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:7px}
.stats div{background:var(--g);color:#fff;border-radius:7px;padding:5px 11px}
.stats b{display:block;font-family:Marcellus,serif;font-weight:400;font-size:18pt;color:var(--c);line-height:1.15}
.stats span{font-size:7pt;color:#c9d6cc}
.dots{font-size:7.9pt;color:#36443a}
.t{width:100%;border-collapse:collapse;margin-top:4px;font-size:7.6pt}
.t th{text-align:left;background:var(--g);color:#fff;font-weight:500;padding:2px 6px;font-size:6.9pt}
.t td{border-bottom:1px solid var(--line);padding:2px 6px}
.t td:first-child{font-weight:700;color:var(--g);white-space:nowrap}
.steps{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(6,1fr);gap:4px}
.steps li{background:var(--bg2);border-radius:7px;padding:6px 7px;font-size:7.6pt;font-weight:500;color:var(--g);line-height:1.35;margin:0}
.sn{display:grid;place-items:center;width:17px;height:17px;border-radius:50%;background:var(--g);color:#fff;font-size:7.6pt;font-weight:700;margin-bottom:3px}
.dsp{display:grid;grid-template-columns:34mm 1fr;gap:7px}
.dsp img{width:100%;height:30mm;object-fit:cover;border-radius:6px}
.facts{list-style:none;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:4px}
.facts li{background:var(--bg2);border-radius:6px;padding:3px 7px;font-size:6.9pt;color:var(--mut);margin:0}
.facts b{display:block;color:var(--g);font-size:8.6pt}
.pitch{background:var(--g);color:#eef3ee;border-radius:8px;padding:8px 11px}
.pitch p{font-size:7.9pt;margin-top:4px}.pitch p:first-child{margin-top:0}
.final{display:flex;gap:10px;align-items:center;margin-top:9px;border:2px solid var(--c);border-radius:9px;padding:8px 11px}
.final h2{font-size:10.5pt;color:var(--g);margin:2px 0 3px}
.final p{font-size:7.6pt;color:#36443a}
.formula{font-size:8pt!important;margin-bottom:2px}.formula b{color:var(--cd)}
.qrs{display:flex;gap:7px;margin-left:auto}
.qrs figure{margin:0;text-align:center}.qrs img{width:17mm;height:17mm;display:block}
.qrs figcaption{font-size:6.3pt;color:var(--mut);margin-top:2px;white-space:nowrap}
"""


def main():
    at = os.path.join(REPO, "availability", "tools")
    doc = f"""<!doctype html><html lang=ja><head><meta charset=utf-8><style>
@font-face{{font-family:Marcellus;src:url(file://{at}/marcellus.woff2) format('woff2')}}
@font-face{{font-family:Figtree;src:url(file://{at}/figtree.woff2) format('woff2');font-weight:300 900}}
{fonts_css()}
{CSS}</style></head><body>{p1}{p2}</body></html>"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = os.path.join(os.path.dirname(OUT), "_strategy.html")
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
