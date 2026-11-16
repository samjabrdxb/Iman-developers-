"""'IMAN selling playbook' image: Sam's sales strategy in one picture, for broker communities.

Usage:  python3 marketing/tools/playbook.py

Writes marketing/2026-11-16/IMAN Selling Playbook - Sam Jabr - post.jpg (1080x1350)
and - story.jpg (1080x1920). Every line says something different: no phrase is repeated.
"""
import os
from playwright.sync_api import sync_playwright

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "marketing", "2026-11-16"); os.makedirs(OUT, exist_ok=True)
T = os.path.join(REPO, "availability", "tools")
IMG = os.path.join(REPO, "site", "assets", "oxford-212-main.webp")
SAM = os.path.join(REPO, "site", "img", "sam-jabr.jpg")

STEPS = [("Lead with philosophy", "Boutique developer: fewer homes, richer amenities."),
         ("Prove delivery", "9 handed over, 2 more just completed. Real buildings, not renders."),
         ("Show the experience", "From lobby to living room to rooftop."),
         ("Compare value", "Layouts, ceilings and density against similar projects."),
         ("Explain payments", "Construction-linked milestones, official plan only."),
         ("Stay factual", "Verified resale data. No hype, no pressure.")]

css = f"""
@font-face{{font-family:Marcellus;src:url(file://{T}/marcellus.woff2)}}
@font-face{{font-family:Figtree;src:url(file://{T}/figtree.woff2);font-weight:300 900}}
*{{box-sizing:border-box;margin:0}}
body{{width:var(--w);height:var(--h);background:#f4f0e8;color:#17251c;font-family:Figtree,sans-serif;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;padding:var(--pad)}}
.top{{display:flex;align-items:center;justify-content:center;gap:18px;color:#9a5f48;font-weight:700;letter-spacing:.32em;font-size:var(--sm)}}
.top:before,.top:after{{content:"";width:60px;height:1px;background:#c0866d}}
.head{{display:grid;grid-template-columns:1fr var(--photo);gap:var(--gap);align-items:center}}
.k{{color:#9a5f48;font-weight:800;letter-spacing:.14em;text-transform:uppercase;font-size:var(--sm)}}
h1{{font-family:Marcellus,serif;font-weight:400;font-size:var(--h1);line-height:1.02;margin-top:10px;color:#1d3f2b}}
h1 span{{color:#b0735a}}
.photo{{height:var(--ph);border-radius:var(--photo) var(--photo) 14px 14px;overflow:hidden;position:relative}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:center 45%}}
.photo span{{position:absolute;left:0;right:0;bottom:0;background:rgba(29,63,43,.88);color:#f2f5f0;font-size:calc(var(--sm)*.95);font-weight:600;text-align:center;padding:7px}}
.steps{{display:grid;grid-template-columns:1fr 1fr;gap:var(--sg)}}
.s{{background:#fff;border:1px solid #e3dccd;border-radius:18px;padding:var(--sp);display:flex;gap:16px}}
.s i{{font-style:normal;font-family:Marcellus,serif;color:#c0866d;font-size:var(--n);line-height:.95}}
.s b{{display:block;font-size:var(--st);color:#1d3f2b;font-weight:800;line-height:1.2}}
.s span{{display:block;font-size:var(--sd);color:#4a584e;margin-top:5px;line-height:1.35}}
.close{{background:#1d3f2b;color:#f2f5f0;border-radius:18px;padding:var(--sp) calc(var(--sp)*1.3)}}
.close small{{display:block;color:#d79e85;font-weight:800;letter-spacing:.14em;text-transform:uppercase;font-size:var(--sm)}}
.close p{{font-family:Marcellus,serif;font-size:var(--q);line-height:1.2;margin-top:6px}}
.never{{text-align:center;font-size:var(--sd);color:#4a584e}}
.never b{{display:block;font-family:Marcellus,serif;font-weight:400;font-size:var(--nv);color:#1d3f2b;line-height:1.15}}
.never em{{font-style:normal;color:#9a5f48;font-weight:700}}
.agent{{display:flex;align-items:center;justify-content:center;gap:16px}}
.agent img{{width:var(--av);height:var(--av);border-radius:50%;object-fit:cover;object-position:50% 12%;border:3px solid #c0866d}}
.agent .n{{font-weight:800;font-size:var(--an)}} .agent .r{{color:#5d6b61;font-size:var(--sd)}} .agent .r b{{color:#9a5f48}}
"""

body = f"""<div class=top>IMAN DEVELOPERS</div>
<div class=head><div><div class=k>The selling playbook</div>
  <h1>Affordable luxury.<br><span>Quality over quantity.</span></h1></div>
 <div class=photo><img src="file://{IMG}" alt=""><span>Oxford 212 · completed</span></div></div>
<div class=steps>{''.join(f'<div class=s><i>{i+1:02d}</i><div><b>{t}</b><span>{d}</span></div></div>' for i, (t, d) in enumerate(STEPS))}</div>
<div class=close><small>Then ask</small><p>"A studio for rental income, or something bigger with resale in mind?"</p></div>
<div class=never><b>Never sell it as the cheapest.</b>Offer the whole package: <em>design, amenities, price, track record.</em></div>
<div class=agent><img src="file://{SAM}" alt=""><div><div class=n>Sam Jabr</div><div class=r>Senior Sales Manager · <b>+971 50 175 2771</b></div></div></div>"""

SIZES = {
 "post": dict(w=1080, h=1350, pad="48px", gap="28px", sm="17px", h1="66px", photo="300px", ph="300px", sg="14px", sp="20px", n="38px", st="24px", sd="20px", q="30px", nv="38px", av="70px", an="25px"),
 "story": dict(w=1080, h=1920, pad="60px", gap="44px", sm="21px", h1="74px", photo="330px", ph="440px", sg="22px", sp="32px", n="46px", st="31px", sd="26px", q="42px", nv="52px", av="88px", an="30px"),
}

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for k, v in SIZES.items():
        vars_ = ";".join(f"--{a}:{x}px" if isinstance(x, int) else f"--{a}:{x}" for a, x in v.items())
        f = os.path.join(OUT, f"_playbook-{k}.html")
        open(f, "w").write(f"<!doctype html><html><head><meta charset=utf-8><style>:root{{{vars_}}}{css}</style></head><body>{body}</body></html>")
        pg = b.new_page(viewport={"width": v["w"], "height": v["h"]}); pg.goto("file://" + f); pg.wait_for_timeout(600)
        over = pg.evaluate("document.body.scrollHeight - innerHeight")
        pg.screenshot(path=os.path.join(OUT, f"IMAN Selling Playbook - Sam Jabr - {k}.jpg"), type="jpeg", quality=90)
        os.remove(f)
        print(k, "overflow px:", over)
    b.close()
