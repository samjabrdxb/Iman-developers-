import os
from playwright.sync_api import sync_playwright
HERE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out")
os.makedirs(HERE, exist_ok=True)
T = "/home/user/Iman-developers-/availability/tools"
IMG = "/home/user/Iman-developers-/site/assets/sierra-by-iman-main.webp"
SAM = "/home/user/Iman-developers-/site/img/sam-jabr.jpg"
units = [("RETAIL-2", 2873.96, 7919913.0), ("RETAIL-3", 2987.42, 8261387.0), ("RETAIL-4", 3075.46, 8484112.0), ("RETAIL-5", 3933.35, 10079595.0)]
m = lambda v: f"{v/1e6:.2f}M"
rows = "".join(f"<tr><td><b>{n.replace('RETAIL-','Shop ')}</b></td><td>{a:,.0f} sq ft</td><td>AED {m(p*.96)}</td><td class=c>AED {m(p*.82)}</td><td class=k>AED {round(p*.96*.07/1e3):,}K</td></tr>" for n, a, p in units)
css = f"""
@font-face{{font-family:Marcellus;src:url(file://{T}/marcellus.woff2)}}
@font-face{{font-family:Figtree;src:url(file://{T}/figtree.woff2);font-weight:300 900}}
*{{box-sizing:border-box;margin:0}}
body{{width:var(--w);height:var(--h);background:#16301f;color:#f2f5f0;font-family:Figtree,sans-serif;overflow:hidden;display:flex;flex-direction:column}}
.hero{{flex:none;height:var(--img);background:url(file://{IMG}) center var(--pos)/cover;position:relative}}
.badge{{position:absolute;left:var(--pad);top:var(--pad);background:#c0866d;color:#1b120d;font-weight:900;letter-spacing:.14em;text-transform:uppercase;border-radius:99px;padding:14px 26px;font-size:var(--fs)}}
.panel{{flex:1;display:flex;flex-direction:column;padding:var(--pad);gap:var(--gap)}}
.eb{{color:#d79e85;font-weight:800;letter-spacing:.18em;text-transform:uppercase;font-size:var(--eb)}}
h1{{font-family:Marcellus,serif;font-weight:400;font-size:var(--h1);line-height:1.02}}
h1 span{{color:#d79e85}}
.sub{{color:#b9c9bd;font-size:var(--fs)}}
.offer{{display:flex;gap:14px}}
.o{{flex:1;background:#1f3e2b;border:1px solid #3a5a45;border-radius:18px;padding:16px 18px}}
.o.hot{{background:#c0866d;border-color:#c0866d;color:#1b120d}}
.o b{{display:block;font-family:Marcellus,serif;font-weight:400;font-size:var(--ov);line-height:1}}
.o span{{font-size:var(--os);font-weight:700;opacity:.85}}
table{{width:100%;border-collapse:collapse;font-size:var(--ts);font-variant-numeric:tabular-nums}}
th{{text-align:left;color:#d79e85;font-size:calc(var(--ts)*.72);letter-spacing:.12em;text-transform:uppercase;padding:0 8px 8px;font-weight:800}}
td{{padding:var(--tp) 8px;border-top:1px solid #34573f}}
td.c{{color:#d79e85;font-weight:700}} td.k{{color:#8fcfa4;font-weight:800}}
.plan{{color:#b9c9bd;font-size:var(--os)}} .plan b{{color:#f2f5f0}}
.agent{{margin-top:auto;display:flex;align-items:center;gap:18px;border-top:1px solid #34573f;padding-top:var(--gap)}}
.agent img{{width:var(--av);height:var(--av);border-radius:50%;object-fit:cover;object-position:50% 12%;border:3px solid #c0866d}}
.agent .n{{font-weight:800;font-size:var(--an)}} .agent .r{{color:#b9c9bd;font-size:var(--os)}}
.agent .p{{margin-left:auto;text-align:right}}
.agent .p small{{display:block;color:#d79e85;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:calc(var(--os)*.85)}}
.agent .p b{{font-size:var(--ph)}}
"""
body = f"""<div class=hero><div class=badge>Only 4 shops left</div></div>
<div class=panel>
 <div><div class=eb>Sierra by Iman · Motor City · Retail</div>
 <h1>Ground-floor shops on the <span>main road</span></h1>
 <div class=sub style="margin-top:8px">Roadside frontage under a landmark residential tower. From 2,874 sq ft.</div></div>
 <div class=offer><div class="o hot"><b>7%</b><span>Commission</span></div><div class=o><b>4%</b><span>Off on 40/60</span></div><div class=o><b>18%</b><span>Off full cash</span></div></div>
 <table><tr><th>Unit</th><th>Size</th><th>40/60 price</th><th>Cash price</th><th>Your 7%</th></tr>{rows}</table>
 <div class=plan><b>40/60 plan:</b> 40% during construction, 60% on handover. Prices after discount.</div>
 <div class=agent><img src="file://{SAM}" alt=""><div><div class=n>Sam Jabr</div><div class=r>Senior Sales Manager · IMAN Developers</div></div>
  <div class=p><small>WhatsApp</small><b>+971 50 175 2771</b></div></div>
</div>"""
SIZES = {
 "post": dict(w=1080, h=1350, img=430, pos="35%", pad="44px", gap="22px", eb="20px", h1="62px", fs="24px", ov="52px", os="20px", ts="25px", tp="11px", av="80px", an="28px", ph="30px"),
 "story": dict(w=1080, h=1920, img=760, pos="30%", pad="56px", gap="30px", eb="24px", h1="76px", fs="28px", ov="64px", os="23px", ts="28px", tp="15px", av="96px", an="32px", ph="34px"),
}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for k, v in SIZES.items():
        vars_ = ";".join(f"--{a}:{x}px" if isinstance(x, int) else f"--{a}:{x}" for a, x in v.items())
        html = f"<!doctype html><html><head><meta charset=utf-8><style>:root{{{vars_}}}{css}</style></head><body>{body}</body></html>"
        f = os.path.join(HERE, k + ".html"); open(f, "w").write(html)
        pg = b.new_page(viewport={"width": v["w"], "height": v["h"]}); pg.goto("file://" + f); pg.wait_for_timeout(600)
        pg.screenshot(path=os.path.join(HERE, f"Sierra Retail - Sam Jabr - {k}.jpg"), type="jpeg", quality=90)
    b.close()
print("ok")
