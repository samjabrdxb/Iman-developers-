"""One broker image per 113 Residences apartment type (post 1080x1350 and story 1080x1920), from site/inventory.json.
Renders: marketing/assets/113 (from IMAN's 113 marketing folder on Google Drive)."""
import json, os
from playwright.sync_api import sync_playwright
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "marketing", "out"); os.makedirs(OUT, exist_ok=True)
T = os.path.join(REPO, "availability", "tools")
A = os.path.join(REPO, "marketing", "assets", "113")
SAM = os.path.join(REPO, "site", "img", "sam-jabr.jpg")
inv = json.load(open(os.path.join(REPO, "site", "inventory.json")))
units = next(x for x in inv["projects"] if x["id"] == "113-residences")["units"]
GROUPS = [
 ("1 BR", "1 Bedroom + Study", "1BHK_1BHK", ["005", "011", "002"], [("one bedroom with study", "1 BR + Study")]),
 ("2 BR", "2 Bedroom Apartments", "2BHK_2BHK", ["06", "17", "02"], [("two bedroom", "2 BR"), ("two bedroom with study", "2 BR + Study"), ("two bedroom with maid", "2 BR + Maid")]),
 ("3 BR", "3 Bedroom Apartments", "3BHK_3BHK", ["05", "11", "13"], [("three bedroom with maid", "3 BR + Maid"), ("three bedroom with study", "3 BR + Study")]),
 ("4 BR", "4 Bedroom Duplex with Private Pool", "4BHKDUPLEX_4BHK-DUPLEX", ["06", "01", "34"], [("four bedroom duplex with pool", "4 BR Duplex + Pool")]),
]
css = f"""
@font-face{{font-family:Marcellus;src:url(file://{T}/marcellus.woff2)}}
@font-face{{font-family:Figtree;src:url(file://{T}/figtree.woff2);font-weight:300 900}}
*{{box-sizing:border-box;margin:0}}
body{{width:var(--w);height:var(--h);background:#16301f;color:#f2f5f0;font-family:Figtree,sans-serif;overflow:hidden;display:flex;flex-direction:column}}
.pics{{flex:none;height:var(--img);display:grid;grid-template-columns:1.55fr 1fr;grid-template-rows:repeat(2,minmax(0,1fr));gap:6px;position:relative;overflow:hidden}}
.pics img{{width:100%;height:100%;min-height:0;min-width:0;object-fit:cover;display:block}}
.pics img:first-child{{grid-row:1/3}}
.badge{{position:absolute;left:var(--pad);top:var(--pad);background:#c0866d;color:#1b120d;font-weight:900;letter-spacing:.12em;text-transform:uppercase;border-radius:99px;padding:12px 22px;font-size:var(--fs)}}
.panel{{flex:1;display:flex;flex-direction:column;padding:var(--pad);gap:var(--gap)}}
.eb{{color:#d79e85;font-weight:800;letter-spacing:.18em;text-transform:uppercase;font-size:var(--eb)}}
h1{{font-family:Marcellus,serif;font-weight:400;font-size:var(--h1);line-height:1.05;margin-top:6px}}
.from{{font-size:var(--fs);color:#b9c9bd;margin-top:6px}} .from b{{color:#f2f5f0;font-size:calc(var(--fs)*1.25)}}
table{{width:100%;border-collapse:collapse;font-size:var(--ts);font-variant-numeric:tabular-nums}}
th{{text-align:left;color:#d79e85;font-size:calc(var(--ts)*.7);letter-spacing:.12em;text-transform:uppercase;padding:0 8px 6px;font-weight:800}}
td{{padding:var(--tp) 8px;border-top:1px solid #34573f}} td.k{{color:#8fcfa4;font-weight:800}}
.offer{{display:flex;gap:10px}}
.o{{flex:1;background:#1f3e2b;border:1px solid #3a5a45;border-radius:16px;padding:12px 14px}}
.o.hot{{background:#c0866d;border-color:#c0866d;color:#1b120d}}
.o b{{display:block;font-family:Marcellus,serif;font-weight:400;font-size:var(--ov);line-height:1}}
.o span{{font-size:var(--os);font-weight:700;opacity:.85}}
.agent{{margin-top:auto;display:flex;align-items:center;gap:18px;border-top:1px solid #34573f;padding-top:var(--gap)}}
.agent img{{width:var(--av);height:var(--av);border-radius:50%;object-fit:cover;object-position:50% 12%;border:3px solid #c0866d}}
.agent .n{{font-weight:800;font-size:var(--an)}} .agent .r{{color:#b9c9bd;font-size:var(--os)}}
.agent .p{{margin-left:auto;text-align:right}}
.agent .p small{{display:block;color:#d79e85;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:calc(var(--os)*.85)}}
.agent .p b{{font-size:var(--ph)}}
"""
SIZES = {
 "post": dict(w=1080, h=1350, img=600, pad="40px", gap="18px", eb="18px", h1="52px", fs="22px", ts="23px", tp="9px", ov="40px", os="18px", av="72px", an="26px", ph="28px"),
 "story": dict(w=1080, h=1920, img=1120, pad="52px", gap="26px", eb="22px", h1="64px", fs="26px", ts="27px", tp="13px", ov="50px", os="21px", av="90px", an="31px", ph="33px"),
}
M = lambda v: f"{v/1e6:.2f}M"
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for short, title, pre, pics, types in GROUPS:
        rows, allu = "", []
        for k, label in types:
            us = [u for u in units if u["type"].lower() == k]
            if not us:
                continue
            allu += us
            lo = min(u["op"] for u in us) * 0.96
            a0, a1 = min(u["area"] for u in us), max(u["area"] for u in us)
            size = f"{a0:,.0f}" if a0 == a1 else f"{a0:,.0f} to {a1:,.0f}"
            n = ", ".join(u["no"] for u in us) if len(us) <= 3 else f"{len(us)} units"
            rows += f"<tr><td><b>{label}</b></td><td>{n}</td><td>{size} sq ft</td><td>AED {M(lo)}</td><td class=k>AED {round(lo*.07/1e3):,}K</td></tr>"
        if not allu:
            continue
        low = min(u["op"] for u in allu) * 0.96
        badge = f"{len(allu)} unit{'s' if len(allu) > 1 else ''} available" if len(allu) > 1 else "Only 1 unit"
        imgs = "".join(f'<img src="file://{A}/{pre}{x}.jpg" alt="">' for x in pics)
        body = f"""<div class=pics>{imgs}<div class=badge>{badge}</div></div>
<div class=panel>
 <div><div class=eb>113 Residences · Al Sufouh Gardens · Handover Q2 2029</div><h1>{title}</h1>
 <div class=from>From <b>AED {M(low)}</b> with 4% off on the 40/60 plan</div></div>
 <table><tr><th>Type</th><th>Units</th><th>Size</th><th>From</th><th>Your 7%</th></tr>{rows}</table>
 <div class=offer><div class="o hot"><b>7%</b><span>Commission</span></div><div class=o><b>4%</b><span>Off on 40/60</span></div><div class=o><b>14%</b><span>Off full cash</span></div></div>
 <div class=agent><img src="file://{SAM}" alt=""><div><div class=n>Sam Jabr</div><div class=r>Senior Sales Manager · IMAN Developers</div></div>
  <div class=p><small>WhatsApp</small><b>+971 50 175 2771</b></div></div>
</div>"""
        for k, v in SIZES.items():
            vars_ = ";".join(f"--{a}:{x}px" if isinstance(x, int) else f"--{a}:{x}" for a, x in v.items())
            f = os.path.join(OUT, f"113-{short.replace(' ','')}-{k}.html")
            open(f, "w").write(f"<!doctype html><html><head><meta charset=utf-8><style>:root{{{vars_}}}{css}</style></head><body>{body}</body></html>")
            pg = b.new_page(viewport={"width": v["w"], "height": v["h"]}); pg.goto("file://" + f); pg.wait_for_timeout(700)
            pg.screenshot(path=os.path.join(OUT, f"113 {short} - Sam Jabr - {k}.jpg"), type="jpeg", quality=90)
    b.close()
print("ok")
