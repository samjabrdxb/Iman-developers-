"""'Why sell IMAN' image for broker communities (post 1080x1350 and story 1080x1920)."""
import os
from playwright.sync_api import sync_playwright
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "marketing", "out"); os.makedirs(OUT, exist_ok=True)
T = os.path.join(REPO, "availability", "tools")
IMG = os.path.join(REPO, "site", "img", "113-residences.jpg")
SAM = os.path.join(REPO, "site", "img", "sam-jabr.jpg")
css = f"""
@font-face{{font-family:Marcellus;src:url(file://{T}/marcellus.woff2)}}
@font-face{{font-family:Figtree;src:url(file://{T}/figtree.woff2);font-weight:300 900}}
*{{box-sizing:border-box;margin:0}}
body{{width:var(--w);height:var(--h);background:#16301f;color:#f2f5f0;font-family:Figtree,sans-serif;overflow:hidden;display:flex;flex-direction:column}}
.hero{{flex:none;height:var(--img);position:relative;overflow:hidden}}
.hero>img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center var(--pos);transform:scale(1.06)}}
.hero:after{{content:"";position:absolute;left:0;right:0;bottom:0;height:45%;background:linear-gradient(to bottom,rgba(22,48,31,0),#16301f)}}
.logo{{position:absolute;z-index:1;left:var(--pad);top:var(--pad);color:#fff;font-family:Marcellus,serif;letter-spacing:.4em;font-size:var(--lg);text-shadow:0 2px 12px rgba(0,0,0,.4)}}
.panel{{flex:1;display:flex;flex-direction:column;padding:0 var(--pad) var(--pad);gap:var(--gap);margin-top:calc(var(--h1) * -1.2);position:relative}}
h1{{font-family:Marcellus,serif;font-weight:400;font-size:var(--h1);line-height:1.05}}
h1 span{{color:#d79e85}}
.stats{{display:flex;flex-direction:column;gap:12px}}
.s{{display:flex;align-items:center;gap:18px;background:#1f3e2b;border:1px solid #3a5a45;border-radius:18px;padding:14px 20px}}
.s b{{font-family:Marcellus,serif;font-weight:400;font-size:var(--sv);color:#d79e85;min-width:var(--sw);line-height:1}}
.s span{{font-size:var(--ss);font-weight:600;line-height:1.25}}
.s span small{{display:block;color:#b9c9bd;font-weight:500;font-size:calc(var(--ss)*.8)}}
.trust{{font-family:Marcellus,serif;font-size:var(--tr);line-height:1.2}} .trust span{{color:#d79e85}}
.now{{background:#f2f5f0;color:#17251c;border-radius:16px;padding:14px 20px;font-size:var(--ss);font-weight:700}}
.now em{{font-style:normal;color:#9a5f48}}
.fast{{background:#c0866d;color:#1b120d;border-radius:16px;padding:16px 20px}}
.fast b{{display:block;font-size:var(--fb);font-weight:900}}
.fast span{{font-size:var(--ss);font-weight:600}}
.agent{{margin-top:auto;display:flex;align-items:center;gap:18px;border-top:1px solid #34573f;padding-top:var(--gap)}}
.agent img{{width:var(--av);height:var(--av);border-radius:50%;object-fit:cover;object-position:50% 12%;border:3px solid #c0866d}}
.agent .n{{font-weight:800;font-size:var(--an)}} .agent .r{{color:#b9c9bd;font-size:calc(var(--ss)*.85)}}
.agent .p{{margin-left:auto;text-align:right}}
.agent .p small{{display:block;color:#d79e85;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:calc(var(--ss)*.7)}}
.agent .p b{{font-size:var(--ph)}}
"""
body = f"""<div class=hero><img src="file://{IMG}" alt=""><div class=logo>IMAN</div></div>
<div class=panel>
 <h1>Your clients want trust.<br>You want <span>7%</span>.<br>IMAN gives you both.</h1>
 <div class=stats>
  <div class=s><b>9</b><span>Projects delivered<small>and 2 more just received their BCC</small></span></div>
  <div class=s><b>7</b><span>Projects under construction<small>all sold out</small></span></div>
  <div class=s><b>7%</b><span>Commission<small>plus up to AED 100K bonus</small></span></div>
 </div>
 <div class=trust>When every project sells out, it means one thing: <span>buyers trust IMAN.</span></div>
 <div class=now>Now selling: <em>113 Residences, Al Sufouh</em>, from AED 2.1M</div>
 <div class=fast><b>Want your commission fast? IMAN &amp; Sam.</b><span>Everyone who works with me knows it.</span></div>
 <div class=agent><img src="file://{SAM}" alt=""><div><div class=n>Sam Jabr</div><div class=r>Senior Sales Manager · IMAN Developers</div></div>
  <div class=p><small>WhatsApp</small><b>+971 50 175 2771</b></div></div>
</div>"""
SIZES = {
 "post": dict(w=1080, h=1350, img=480, pos="40%", pad="44px", gap="18px", lg="26px", h1="52px", sv="48px", sw="84px", ss="23px", tr="28px", fb="26px", av="72px", an="27px", ph="29px"),
 "story": dict(w=1080, h=1920, img=860, pos="40%", pad="56px", gap="26px", lg="32px", h1="66px", sv="62px", sw="106px", ss="28px", tr="36px", fb="32px", av="92px", an="32px", ph="34px"),
}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for k, v in SIZES.items():
        vars_ = ";".join(f"--{a}:{x}px" if isinstance(x, int) else f"--{a}:{x}" for a, x in v.items())
        f = os.path.join(OUT, f"why-{k}.html")
        open(f, "w").write(f"<!doctype html><html><head><meta charset=utf-8><style>:root{{{vars_}}}{css}</style></head><body>{body}</body></html>")
        pg = b.new_page(viewport={"width": v["w"], "height": v["h"]}); pg.goto("file://" + f); pg.wait_for_timeout(600)
        pg.screenshot(path=os.path.join(OUT, f"Why IMAN - Sam Jabr - {k}.jpg"), type="jpeg", quality=90)
    b.close()
print("ok")
