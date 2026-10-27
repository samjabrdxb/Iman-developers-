"""Broker image for 113 Residences (post 1080x1350 and story 1080x1920), built from site/inventory.json."""
import json, os
from playwright.sync_api import sync_playwright
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "marketing", "out"); os.makedirs(OUT, exist_ok=True)
T = os.path.join(REPO, "availability", "tools")
IMG = os.path.join(REPO, "site", "img", "113-residences.jpg")
SAM = os.path.join(REPO, "site", "img", "sam-jabr.jpg")
inv = json.load(open(os.path.join(REPO, "site", "inventory.json")))
p = next(x for x in inv["projects"] if x["id"] == "113-residences")
NAMES = [("one bedroom with study", "1 BR + Study"), ("two bedroom", "2 BR"), ("two bedroom with study", "2 BR + Study"),
         ("two bedroom with maid", "2 BR + Maid"), ("three bedroom with maid", "3 BR + Maid"), ("three bedroom with study", "3 BR + Study")]
rows = ""
for k, label in NAMES:
    us = [u for u in p["units"] if u["type"].lower() == k]
    if not us:
        continue
    lo = min(u["op"] for u in us) * 0.96
    a0, a1 = min(u["area"] for u in us), max(u["area"] for u in us)
    size = f"{a0:,.0f}" if a0 == a1 else f"{a0:,.0f} to {a1:,.0f}"
    rows += f"<tr><td><b>{label}</b></td><td>{len(us)}</td><td>{size} sq ft</td><td>AED {lo/1e6:.2f}M</td><td class=k>AED {round(lo*.07/1e3):,}K</td></tr>"
n = len(p["units"])
low = min(u["op"] for u in p["units"]) * 0.96
css = f"""
@font-face{{font-family:Marcellus;src:url(file://{T}/marcellus.woff2)}}
@font-face{{font-family:Figtree;src:url(file://{T}/figtree.woff2);font-weight:300 900}}
*{{box-sizing:border-box;margin:0}}
body{{width:var(--w);height:var(--h);background:#16301f;color:#f2f5f0;font-family:Figtree,sans-serif;overflow:hidden;display:flex;flex-direction:column}}
.hero{{flex:none;height:var(--img);position:relative;overflow:hidden}}
.hero>img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center var(--pos);transform:scale(1.06)}}
.badge{{z-index:1;position:absolute;left:var(--pad);top:var(--pad);background:#c0866d;color:#1b120d;font-weight:900;letter-spacing:.14em;text-transform:uppercase;border-radius:99px;padding:14px 26px;font-size:var(--fs)}}
.panel{{flex:1;display:flex;flex-direction:column;padding:var(--pad);gap:var(--gap)}}
.eb{{color:#d79e85;font-weight:800;letter-spacing:.18em;text-transform:uppercase;font-size:var(--eb)}}
h1{{font-family:Marcellus,serif;font-weight:400;font-size:var(--h1);line-height:1.02}}
h1 span{{color:#d79e85}}
.sub{{color:#b9c9bd;font-size:var(--fs)}}
.offer{{display:flex;gap:12px}}
.o{{flex:1;background:#1f3e2b;border:1px solid #3a5a45;border-radius:18px;padding:14px 16px}}
.o.hot{{background:#c0866d;border-color:#c0866d;color:#1b120d}}
.o b{{display:block;font-family:Marcellus,serif;font-weight:400;font-size:var(--ov);line-height:1}}
.o span{{font-size:var(--os);font-weight:700;opacity:.85}}
.bonus{{background:#f2f5f0;color:#17251c;border-radius:14px;padding:12px 18px;font-weight:800;font-size:var(--os)}}
.bonus em{{font-style:normal;color:#9a5f48}}
table{{width:100%;border-collapse:collapse;font-size:var(--ts);font-variant-numeric:tabular-nums}}
th{{text-align:left;color:#d79e85;font-size:calc(var(--ts)*.7);letter-spacing:.12em;text-transform:uppercase;padding:0 8px 6px;font-weight:800}}
td{{padding:var(--tp) 8px;border-top:1px solid #34573f}}
td.k{{color:#8fcfa4;font-weight:800}}
.plan{{display:flex;gap:6px;align-items:stretch}}
.plan div{{background:#1f3e2b;border-radius:12px;padding:8px 10px;text-align:center;font-size:calc(var(--os)*.85);color:#b9c9bd;line-height:1.2}}
.plan b{{display:block;color:#f2f5f0;font-size:var(--pv)}}
.agent{{margin-top:auto;display:flex;align-items:center;gap:18px;border-top:1px solid #34573f;padding-top:var(--gap)}}
.agent img{{width:var(--av);height:var(--av);border-radius:50%;object-fit:cover;object-position:50% 12%;border:3px solid #c0866d}}
.agent .n{{font-weight:800;font-size:var(--an)}} .agent .r{{color:#b9c9bd;font-size:var(--os)}}
.agent .p{{margin-left:auto;text-align:right}}
.agent .p small{{display:block;color:#d79e85;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:calc(var(--os)*.85)}}
.agent .p b{{font-size:var(--ph)}}
"""
body = f"""<div class=hero><img src="file://{IMG}" alt=""><div class=badge>{n} units available</div></div>
<div class=panel>
 <div><div class=eb>113 Residences · Al Sufouh Gardens · Handover Q2 2029</div>
 <h1>From <span>AED {low/1e6:.1f}M</span>, next to Al Sufouh Park</h1></div>
 <div class=offer><div class="o hot"><b>7%</b><span>Commission</span></div><div class=o><b>4%</b><span>Off on 40/60</span></div><div class=o><b>14%</b><span>Off full cash</span></div></div>
 <div class=bonus>Broker bonus: <em>3 units = AED 50K</em> · <em>5 units = AED 100K</em></div>
 <table><tr><th>Type</th><th>Units</th><th>Size</th><th>From</th><th>Your 7%</th></tr>{rows}</table>
 <div class=plan><div style="flex:2"><b>20%</b>Within 30 days</div><div style="flex:1.4"><b>10%</b>90 days</div><div style="flex:1.4"><b>10%</b>40% built</div><div style="flex:4"><b>60%</b>On handover</div></div>
 <div class=agent><img src="file://{SAM}" alt=""><div><div class=n>Sam Jabr</div><div class=r>Senior Sales Manager · IMAN Developers</div></div>
  <div class=p><small>WhatsApp</small><b>+971 50 175 2771</b></div></div>
</div>"""
SIZES = {
 "post": dict(w=1080, h=1350, img=400, pos="45%", pad="42px", gap="18px", eb="19px", h1="56px", fs="23px", ov="48px", os="20px", ts="23px", tp="8px", pv="26px", av="76px", an="28px", ph="30px"),
 "story": dict(w=1080, h=1920, img=720, pos="45%", pad="54px", gap="26px", eb="22px", h1="70px", fs="27px", ov="60px", os="23px", ts="27px", tp="13px", pv="32px", av="94px", an="32px", ph="34px"),
}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for k, v in SIZES.items():
        vars_ = ";".join(f"--{a}:{x}px" if isinstance(x, int) else f"--{a}:{x}" for a, x in v.items())
        f = os.path.join(OUT, f"113-{k}.html")
        open(f, "w").write(f"<!doctype html><html><head><meta charset=utf-8><style>:root{{{vars_}}}{css}</style></head><body>{body}</body></html>")
        pg = b.new_page(viewport={"width": v["w"], "height": v["h"]}); pg.goto("file://" + f); pg.wait_for_timeout(600)
        pg.screenshot(path=os.path.join(OUT, f"113 Residences - Sam Jabr - {k}.jpg"), type="jpeg", quality=90)
    b.close()
print("ok")
