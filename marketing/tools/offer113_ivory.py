"""113 Residences, new offer image, ivory / espresso / bronze version for brokers (post and story): 6% off on 40/60, 16% off full cash,
7% commission and the agency cash bonus by unit type. Render: marketing/assets/113/elev1-building.jpg
(IMAN's elevation render, cut below its 113 logo and above its QR code)."""
import os
from playwright.sync_api import sync_playwright
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "marketing", "out"); os.makedirs(OUT, exist_ok=True)
T = os.path.join(REPO, "availability", "tools")
IMG = os.path.join(REPO, "marketing", "assets", "113", "elev1-building.jpg")
SAM = os.path.join(REPO, "site", "img", "sam-jabr.jpg")
css = f"""
@font-face{{font-family:Marcellus;src:url(file://{T}/marcellus.woff2)}}
@font-face{{font-family:Figtree;src:url(file://{T}/figtree.woff2);font-weight:300 900}}
*{{box-sizing:border-box;margin:0}}
body{{width:var(--w);height:var(--h);background:#f6f1e9;color:#2a1f17;font-family:Figtree,sans-serif;overflow:hidden;display:flex;flex-direction:column}}
.hero{{flex:none;height:var(--img);position:relative;overflow:hidden}}
.hero img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 40%}}
.hero:after{{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba(42,31,23,.45) 0%,rgba(246,241,233,0) 26%,rgba(246,241,233,0) 55%,#f6f1e9 100%)}}
.pill{{position:absolute;z-index:1;left:var(--pad);top:var(--pad);display:flex;align-items:center;gap:12px;background:#2a1f17;color:#f6f1e9;border-radius:99px;padding:10px 22px;font-weight:900;letter-spacing:.2em;font-size:var(--sm)}}
.loc{{position:absolute;z-index:1;right:var(--pad);top:var(--pad);font-family:Marcellus,serif;font-size:var(--md);color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.5)}}
.panel{{flex:1;display:flex;flex-direction:column;padding:0 var(--pad) var(--pad);gap:var(--gap);margin-top:calc(var(--t1) * -0.6);position:relative}}
.title small{{display:block;color:#a8763e;font-weight:800;letter-spacing:.32em;font-size:var(--sm)}}
.title h1{{font-family:Marcellus,serif;font-weight:400;font-size:var(--t1);line-height:.95;letter-spacing:.04em}}
.title h1 span{{color:#a8763e}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.s{{border:1px solid #e3d6c2;border-radius:16px;padding:16px 16px;background:#fff}}
.s b{{display:block;font-family:Marcellus,serif;font-weight:400;font-size:var(--sv);line-height:1;color:#2a1f17}}
.s span{{display:block;margin-top:8px;font-size:var(--sl);font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8a7560}}
.s.gold{{background:linear-gradient(135deg,#c4955a,#9a6a33);border:0}} .s.gold b,.s.gold span{{color:#fff}}
.bonus{{background:#2a1f17;color:#f6f1e9;border-radius:18px;padding:var(--bp)}}
.bonus .k{{font-size:var(--sl);font-weight:900;letter-spacing:.2em;color:#d9b27c;display:flex;justify-content:space-between;gap:10px}}
.bonus .k em{{font-style:normal;letter-spacing:.06em;color:#bfae98;font-weight:700}}
.bonus .row{{display:grid;grid-template-columns:repeat(3,1fr);margin-top:10px}}
.bonus .row div{{text-align:center;border-left:1px solid #4a3a2c}} .bonus .row div:first-child{{border:0}}
.bonus .row b{{display:block;font-family:Marcellus,serif;font-weight:400;font-size:var(--bv);line-height:1.05}}
.bonus .row b small{{font-size:.45em;color:#d9b27c;margin-right:6px;vertical-align:.5em;font-family:Figtree;font-weight:800}}
.bonus .row span{{display:block;font-size:var(--md2);font-weight:700;color:#e9dfcf;margin-top:4px}}
.from .k{{font-size:var(--sl);font-weight:900;letter-spacing:.2em;color:#a8763e;margin-bottom:10px}}
.fr{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}
.fr div{{border-left:2px solid #a8763e;padding-left:12px}} .fr span{{display:block;font-size:var(--md2);color:#8a7560}} .fr b{{font-size:var(--fb);font-weight:800}}
.line{{display:flex;justify-content:space-between;gap:16px;font-size:var(--md2);color:#5c4a3a;border-top:1px solid #e3d6c2;padding-top:var(--lp)}}
.line b{{color:#2a1f17}}
.agent{{margin-top:auto;display:flex;align-items:center;gap:18px;border-top:1px solid #e3d6c2;padding-top:var(--ap)}}
.agent img{{width:var(--av);height:var(--av);border-radius:50%;object-fit:cover;object-position:50% 15%;border:2px solid #a8763e}}
.agent .n{{font-weight:800;font-size:var(--an)}} .agent .r{{color:#8a7560;font-size:var(--md2)}}
.agent .p{{margin-left:auto;text-align:right;white-space:nowrap}} .agent .p b{{font-size:var(--ph);font-weight:800}}
.agent .p small{{display:block;color:#a8763e;font-weight:800;letter-spacing:.14em;font-size:var(--sl)}}
"""
body = f"""<div class=hero><img src="file://{IMG}" alt=""><div class=pill>NEW OFFER</div><div class=loc>Al Sufouh · Dubai</div></div>
<div class=panel>
 <div class=title><small>BY IMAN DEVELOPERS</small><h1>113 <span>RESIDENCES</span></h1></div>
 <div class=stats><div class="s gold"><b>6%</b><span>Discount</span></div><div class=s><b>40/60</b><span>Payment plan</span></div>
  <div class=s><b>16%</b><span>Off full cash</span></div><div class=s><b>7%</b><span>Commission</span></div></div>
 <div class=bonus><div class=k>AGENCY CASH BONUS<em>by unit type</em></div>
  <div class=row><div><b><small>AED</small>25K</b><span>2 Bedrooms</span></div><div><b><small>AED</small>35K</b><span>3 Bedrooms</span></div><div><b><small>AED</small>50K</b><span>4 Bedrooms</span></div></div></div>
 <div class=from><div class=k>PRICES FROM · AFTER 6% DISCOUNT</div><div class=fr>
  <div><span>1 BR + Study</span><b>AED 2.06M</b></div><div><span>2 Bedrooms</span><b>AED 2.57M</b></div><div><span>3 Bedrooms</span><b>AED 3.58M</b></div><div><span>4 BR Duplex</span><b>AED 5.12M</b></div></div></div>
 <div class=line><span>Only <b>15 units</b> left</span><span>Handover <b>Q2 2029</b></span></div>
 <div class=agent><img src="file://{SAM}" alt=""><div><div class=n>Sam Jabr</div><div class=r>Senior Sales Manager · IMAN Developers</div></div>
  <div class=p><small>CALL / WHATSAPP</small><b>+971 50 175 2771</b></div></div>
</div>"""
SIZES = {
 "post": dict(w=1080, h=1350, img=600, pad="44px", gap="22px", fb="24px", sm="16px", md="26px", md2="20px", t1="92px", sv="50px", sl="14px", bp="20px 24px", bv="52px", lp="14px", ap="18px", av="70px", an="26px", ph="28px"),
 "story": dict(w=1080, h=1920, img=900, pad="60px", gap="40px", fb="32px", sm="22px", md="36px", md2="26px", t1="118px", sv="64px", sl="17px", bp="30px 32px", bv="70px", lp="22px", ap="26px", av="100px", an="34px", ph="36px"),
}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for k, v in SIZES.items():
        vars_ = ";".join(f"--{a}:{x}px" if isinstance(x, int) else f"--{a}:{x}" for a, x in v.items())
        f = os.path.join(OUT, f"offer113-ivory-{k}.html")
        open(f, "w").write(f"<!doctype html><html><head><meta charset=utf-8><style>:root{{{vars_}}}{css}</style></head><body>{body}</body></html>")
        pg = b.new_page(viewport={"width": v["w"], "height": v["h"]}); pg.goto("file://" + f); pg.wait_for_timeout(700)
        pg.screenshot(path=os.path.join(OUT, f"113 Residences offer - Sam Jabr - ivory {k}.jpg"), type="jpeg", quality=92)
    b.close()
print("ok")
