"""IMAN main selling point image: premium quality, competitive prices, prime locations (post and story)."""
import os
from playwright.sync_api import sync_playwright
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "marketing", "out"); os.makedirs(OUT, exist_ok=True)
T = os.path.join(REPO, "availability", "tools")
HERO = os.path.join(REPO, "marketing", "assets", "113", "grand.jpg")
SAM = os.path.join(REPO, "site", "img", "sam-jabr.jpg")
css = f"""
@font-face{{font-family:Marcellus;src:url(file://{T}/marcellus.woff2)}}
@font-face{{font-family:Figtree;src:url(file://{T}/figtree.woff2);font-weight:300 900}}
*{{box-sizing:border-box;margin:0}}
body{{width:var(--w);height:var(--h);background:#0f241a;color:#f2f5f0;font-family:Figtree,sans-serif;overflow:hidden;display:flex;flex-direction:column}}
.hero{{flex:none;height:var(--img);position:relative;overflow:hidden}}
.hero img{{position:absolute;inset:0;width:100%;height:auto;min-height:100%;object-fit:cover;object-position:center top}}
.hero:after{{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba(15,36,26,0) 35%,rgba(15,36,26,.55) 62%,#0f241a 100%)}}
.head{{position:absolute;z-index:1;left:var(--pad);right:var(--pad);bottom:var(--hb)}}
.kick{{display:inline-block;color:#d79e85;font-weight:800;letter-spacing:.3em;text-transform:uppercase;font-size:var(--eb);border-bottom:2px solid #c0866d;padding-bottom:8px;margin-bottom:18px}}
h1{{font-family:Marcellus,serif;font-weight:400;font-size:var(--h1);line-height:1.04}}
h1 i{{font-style:normal;color:#d79e85}}
.pillars{{display:grid;grid-template-columns:repeat(3,1fr);padding:0 var(--pad);margin-top:var(--gap)}}
.p{{padding:0 18px;border-left:1px solid #3a5a45}} .p:first-child{{padding-left:0;border-left:0}}
.p small{{display:block;color:#d79e85;font-weight:800;letter-spacing:.16em;text-transform:uppercase;font-size:var(--ps)}}
.p b{{display:block;font-family:Marcellus,serif;font-weight:400;font-size:var(--pv);line-height:1.1;margin:8px 0 6px}}
.p span{{display:block;color:#b9c9bd;font-size:var(--pt);line-height:1.35}}
.foot{{margin-top:auto;padding:var(--gap) var(--pad) var(--pad);display:flex;align-items:center;gap:18px}}
.foot img{{width:var(--av);height:var(--av);border-radius:50%;object-fit:cover;object-position:50% 12%;border:2px solid #c0866d}}
.foot .n{{font-weight:800;font-size:var(--an)}} .foot .r{{color:#b9c9bd;font-size:var(--pt)}}
.foot .ph{{margin-left:auto;text-align:right}}
.foot .ph b{{display:block;font-size:var(--phs)}} .foot .ph span{{color:#d79e85;font-size:var(--pt);font-weight:700}}
"""
body = f"""<div class=hero><img src="file://{HERO}" alt="">
 <div class=head><div class=kick>IMAN Developers</div>
 <h1>Premium <i>quality</i>.<br>Competitive <i>prices</i>.<br>Prime <i>locations</i>.</h1></div></div>
<div class=pillars>
 <div class=p><small>Quality</small><b>Built to impress</b><span>Smart locks, European appliances, rooftop infinity pool</span></div>
 <div class=p><small>Price</small><b>From AED 2.1M</b><span>40/60 payment plan, 4% off, 14% off on cash</span></div>
 <div class=p><small>Location</small><b>Al Sufouh</b><span>Facing Al Sufouh Park, 10 min to Dubai Marina</span></div>
</div>
<div class=foot><img src="file://{SAM}" alt=""><div><div class=n>Sam Jabr</div><div class=r>Senior Sales Manager · IMAN Developers</div></div>
 <div class=ph><b>+971 50 175 2771</b><span>113 Residences · Al Sufouh</span></div></div>"""
SIZES = {
 "post": dict(w=1080, h=1350, img=860, pad="52px", hb="36px", gap="30px", eb="17px", h1="74px", ps="15px", pv="34px", pt="18px", av="70px", an="25px", phs="27px"),
 "story": dict(w=1080, h=1920, img=1180, pad="60px", hb="50px", gap="44px", eb="20px", h1="92px", ps="17px", pv="40px", pt="21px", av="86px", an="30px", phs="32px"),
}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for k, v in SIZES.items():
        vars_ = ";".join(f"--{a}:{x}px" if isinstance(x, int) else f"--{a}:{x}" for a, x in v.items())
        f = os.path.join(OUT, f"usp-{k}.html")
        open(f, "w").write(f"<!doctype html><html><head><meta charset=utf-8><style>:root{{{vars_}}}{css}</style></head><body>{body}</body></html>")
        pg = b.new_page(viewport={"width": v["w"], "height": v["h"]}); pg.goto("file://" + f); pg.wait_for_timeout(700)
        pg.screenshot(path=os.path.join(OUT, f"IMAN Premium Quality - Sam Jabr - {k}.jpg"), type="jpeg", quality=90)
    b.close()
print("ok")
