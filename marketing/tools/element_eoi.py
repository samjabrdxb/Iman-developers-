"""The Element by IMAN, Dubai Science Park: EOI open image for brokers (post and story).
Render: marketing/assets/element-rooftop.jpg, cut from IMAN's EOI announcement image."""
import os
from playwright.sync_api import sync_playwright
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "marketing", "out"); os.makedirs(OUT, exist_ok=True)
T = os.path.join(REPO, "availability", "tools")
IMG = os.path.join(REPO, "marketing", "assets", "element-rooftop.jpg")
SAM = os.path.join(REPO, "site", "img", "sam-jabr.jpg")
css = f"""
@font-face{{font-family:Marcellus;src:url(file://{T}/marcellus.woff2)}}
@font-face{{font-family:Figtree;src:url(file://{T}/figtree.woff2);font-weight:300 900}}
*{{box-sizing:border-box;margin:0}}
body{{width:var(--w);height:var(--h);background:#0a1430;color:#f4efe6;font-family:Figtree,sans-serif;overflow:hidden;display:flex;flex-direction:column}}
.hero{{flex:none;height:var(--img);position:relative;overflow:hidden}}
.hero img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:60% 70%}}
.hero:after{{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba(10,20,48,.55) 0%,rgba(10,20,48,0) 30%,rgba(10,20,48,0) 55%,#0a1430 100%)}}
.live{{position:absolute;z-index:1;left:var(--pad);top:var(--pad);display:flex;align-items:center;gap:12px;background:rgba(10,20,48,.75);border:1px solid #c9a96a;border-radius:99px;padding:10px 20px;font-weight:800;letter-spacing:.2em;font-size:var(--sm);color:#f4efe6}}
.live i{{width:12px;height:12px;border-radius:50%;background:#7ee08f;box-shadow:0 0 0 6px rgba(126,224,143,.25)}}
.loc{{position:absolute;z-index:1;right:var(--pad);top:var(--pad);font-family:Marcellus,serif;font-size:var(--md);color:#f4efe6;text-shadow:0 2px 10px rgba(0,0,0,.5)}}
.panel{{flex:1;display:flex;flex-direction:column;padding:0 var(--pad) var(--pad);gap:var(--gap);margin-top:calc(var(--t1) * -0.55);position:relative}}
.title small{{display:block;color:#c9a96a;font-weight:800;letter-spacing:.32em;font-size:var(--sm)}}
.title h1{{font-family:Marcellus,serif;font-weight:400;font-size:var(--t1);line-height:.95;letter-spacing:.06em}}
.title h1 span{{color:#c9a96a}}
.price{{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;border-top:1px solid #2b3a63;border-bottom:1px solid #2b3a63;padding:var(--pp) 0}}
.price .k{{font-size:var(--sm);letter-spacing:.24em;color:#a9b3cc;font-weight:700}}
.price .v{{font-family:Marcellus,serif;font-size:var(--pv);line-height:1;color:#fff}} .price .v span{{font-size:.45em;color:#c9a96a;margin-right:10px;vertical-align:.55em}}
.price .mix{{text-align:right;font-size:var(--md2);color:#d9d2c4;line-height:1.45}}
.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.s{{border:1px solid #2b3a63;border-radius:16px;padding:16px 18px;background:#0f1c40}}
.s.gold{{background:linear-gradient(135deg,#d8bd85,#b8955a);border-color:#c9a96a;color:#1a1408}}
.s b{{display:block;font-family:Marcellus,serif;font-weight:400;font-size:var(--sv);line-height:1}}
.s span{{display:block;margin-top:8px;font-size:var(--sl);font-weight:800;letter-spacing:.12em;text-transform:uppercase;opacity:.85}}
.eoi{{display:flex;align-items:center;justify-content:space-between;gap:16px;background:#f4efe6;color:#0a1430;border-radius:16px;padding:var(--ep)}}
.eoi .a{{font-size:var(--sl);font-weight:800;letter-spacing:.16em;color:#8a6a34}}
.eoi .b{{font-family:Marcellus,serif;font-size:var(--ev);line-height:1.05}}
.eoi .c{{text-align:right;font-weight:700;font-size:var(--md2);line-height:1.3}}
.eoi .c em{{font-style:normal;color:#8a6a34;display:block;font-size:var(--sl);letter-spacing:.1em}}
.near .k{{font-size:var(--sl);font-weight:800;letter-spacing:.24em;color:#c9a96a;margin-bottom:10px}}
.chips{{display:flex;flex-wrap:wrap;gap:8px}}
.chips span{{border:1px solid #2b3a63;border-radius:99px;padding:6px 14px;font-size:var(--md2);color:#d9d2c4}}
.agent{{margin-top:auto;display:flex;align-items:center;gap:18px;border-top:1px solid #2b3a63;padding-top:var(--gap)}}
.agent img{{width:var(--av);height:var(--av);border-radius:50%;object-fit:cover;object-position:50% 12%;border:2px solid #c9a96a}}
.agent .n{{font-weight:800;font-size:var(--an)}} .agent .r{{color:#a9b3cc;font-size:var(--md2)}}
.agent .p{{margin-left:auto;text-align:right}}
.agent .p{{white-space:nowrap}} .agent .p small{{display:block;color:#c9a96a;font-weight:800;letter-spacing:.14em;font-size:var(--sl)}}
.agent .p b{{font-size:var(--ph)}}
"""
body = f"""<div class=hero><img src="file://{IMG}" alt=""><div class=live><i></i>EOI NOW OPEN</div><div class=loc>Dubai Science Park</div></div>
<div class=panel>
 <div class=title><small>BY IMAN DEVELOPERS</small><h1>THE <span>ELEMENT</span></h1></div>
 <div class=price><div><div class=k>STARTING FROM</div><div class=v><span>AED</span>684K</div></div>
  <div class=mix>Studio · 1 BR · 2 BR<br>Retail units</div></div>
 <div class=stats><div class="s gold"><b>4%</b><span>Pre-launch discount</span></div><div class=s><b>40/60</b><span>Payment plan</span></div><div class=s><b>7%</b><span>Broker commission</span></div></div>
 <div class=eoi><div><div class=a>EXPRESSION OF INTEREST</div><div class=b>AED 50,000</div></div><div class=c>100% refundable<em>PRIORITY: FIRST COME, FIRST SERVED</em></div></div>
 <div class=near><div class=k>NEARBY</div><div class=chips><span>Dubai Hills Mall</span><span>My City Centre Al Barsha</span><span>Mediclinic Parkview</span><span>Repton School</span><span>Miracle Garden</span><span>Dubai Autodrome</span></div></div>
 <div class=agent><img src="file://{SAM}" alt=""><div><div class=n>Sam Jabr</div><div class=r>Senior Sales Manager · IMAN Developers</div></div>
  <div class=p><small>BOOK YOUR EOI</small><b>+971 50 175 2771</b></div></div>
</div>"""
SIZES = {
 "post": dict(w=1080, h=1350, img=500, pad="44px", gap="20px", sm="16px", md="26px", md2="20px", t1="104px", pp="18px", pv="92px", sv="52px", sl="15px", ep="18px 24px", ev="44px", av="70px", an="26px", ph="28px"),
 "story": dict(w=1080, h=1920, img=620, pad="60px", gap="44px", sm="22px", md="38px", md2="26px", t1="132px", pp="30px", pv="140px", sv="72px", sl="19px", ep="32px 36px", ev="60px", av="104px", an="34px", ph="36px"),
}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for k, v in SIZES.items():
        vars_ = ";".join(f"--{a}:{x}px" if isinstance(x, int) else f"--{a}:{x}" for a, x in v.items())
        f = os.path.join(OUT, f"element-{k}.html")
        open(f, "w").write(f"<!doctype html><html><head><meta charset=utf-8><style>:root{{{vars_}}}{css}</style></head><body>{body}</body></html>")
        pg = b.new_page(viewport={"width": v["w"], "height": v["h"]}); pg.goto("file://" + f); pg.wait_for_timeout(700)
        pg.screenshot(path=os.path.join(OUT, f"The Element EOI - Sam Jabr - {k}.jpg"), type="jpeg", quality=92)
    b.close()
print("ok")
