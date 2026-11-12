"""IMAN 'Affordable Luxury' image in a light editorial style: arched photo, ivory ground (post and story)."""
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
body{{width:var(--w);height:var(--h);background:#f3eee6;color:#1b2f23;font-family:Figtree,sans-serif;overflow:hidden;display:flex;flex-direction:column;align-items:center;text-align:center;padding:var(--pad) var(--side)}}
.top{{font-weight:700;letter-spacing:.5em;font-size:var(--tk);color:#9a5f48;display:flex;align-items:center;gap:18px}}
.top:before,.top:after{{content:"";width:60px;height:1px;background:#c0866d}}
.arch{{position:relative;width:var(--aw);height:var(--ah);border-radius:calc(var(--aw)/2) calc(var(--aw)/2) 0 0;overflow:hidden;margin-top:var(--g1);box-shadow:0 30px 60px -30px rgba(27,47,35,.45)}}
.arch img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 62%;transform:scale(var(--sc));transform-origin:var(--org)}}
.frame{{position:absolute;inset:14px;border:1px solid rgba(255,255,255,.55);border-radius:calc(var(--aw)/2 - 14px) calc(var(--aw)/2 - 14px) 0 0;border-bottom:0}}
h1{{font-family:Marcellus,serif;font-weight:400;font-size:var(--h1);line-height:1;margin-top:var(--g2);letter-spacing:-.01em}}
h1 i{{font-style:normal;color:#9a5f48}}
.three{{display:flex;justify-content:center;gap:0;margin-top:var(--g3);font-size:var(--th);font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:#1b2f23}}
.three span{{padding:0 18px}} .three span+span{{border-left:1px solid #c0866d}}
.proj{{margin-top:var(--g3);font-size:var(--pr);color:#4f5f54}} .proj b{{color:#1b2f23}}
.sam{{margin-top:auto;display:flex;align-items:center;gap:16px;text-align:left}}
.sam img{{width:var(--av);height:var(--av);border-radius:50%;object-fit:cover;object-position:50% 12%;border:2px solid #c0866d}}
.sam b{{display:block;font-size:var(--an)}} .sam span{{font-size:var(--pr);color:#4f5f54}}
.sam em{{font-style:normal;font-weight:800;color:#9a5f48;margin-left:6px}}
"""
body = f"""<div class=top>IMAN DEVELOPERS</div>
<div class=arch><img src="file://{HERO}" alt=""><div class=frame></div></div>
<h1>Affordable <i>Luxury</i></h1>
<div class=three><span>Premium quality</span><span>Competitive prices</span><span>Prime locations</span></div>
<div class=proj><b>113 Residences, Al Sufouh</b> · from AED 2.1M · 7% commission</div>
<div class=sam><img src="file://{SAM}" alt=""><div><b>Sam Jabr</b><span>Senior Sales Manager · IMAN Developers<em>+971 50 175 2771</em></span></div></div>"""
SIZES = {
 "post": dict(w="1080px", h="1350px", sc="1.32", org="36% 82%", pad="56px", side="60px", tk="17px", aw="700px", ah="740px", g1="34px", h1="92px", g2="34px", g3="20px", th="17px", pr="19px", av="64px", an="24px"),
 "story": dict(w="1080px", h="1920px", sc="1.45", org="36% 96%", pad="110px", side="60px", tk="20px", aw="860px", ah="1120px", g1="60px", h1="118px", g2="60px", g3="34px", th="20px", pr="23px", av="80px", an="29px"),
}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for k, v in SIZES.items():
        vars_ = ";".join(f"--{a}:{x}" for a, x in v.items())
        f = os.path.join(OUT, f"lux-{k}.html")
        open(f, "w").write(f"<!doctype html><html><head><meta charset=utf-8><style>:root{{{vars_}}}{css}</style></head><body>{body}</body></html>")
        pg = b.new_page(viewport={"width": int(v["w"][:-2]), "height": int(v["h"][:-2])}); pg.goto("file://" + f); pg.wait_for_timeout(700)
        pg.screenshot(path=os.path.join(OUT, f"IMAN Affordable Luxury - Sam Jabr - {k}.jpg"), type="jpeg", quality=92)
    b.close()
print("ok")
