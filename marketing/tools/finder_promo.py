"""Image promoting the unit finder link to brokers (post 1080x1350 and story 1080x1920), in the style of the 113 type images."""
import base64, io, os
import qrcode
from playwright.sync_api import sync_playwright
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "marketing", "out"); os.makedirs(OUT, exist_ok=True)
T = os.path.join(REPO, "availability", "tools")
A = os.path.join(REPO, "marketing", "assets", "113")
SAM = os.path.join(REPO, "site", "img", "sam-jabr.jpg")
LINK = "https://claude.ai/artifact/Eg5NZJCZRwriTRGYLCwTb7"
q = qrcode.QRCode(border=1, box_size=10); q.add_data(LINK); q.make()
buf = io.BytesIO(); q.make_image(fill_color="#16301f", back_color="white").save(buf, "PNG")
QR = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
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
h1 span{{color:#d79e85}}
.sub{{font-size:var(--fs);color:#b9c9bd;margin-top:8px}}
.steps{{display:flex;gap:10px}}
.st{{flex:1;background:#1f3e2b;border:1px solid #3a5a45;border-radius:16px;padding:12px 14px}}
.st b{{display:block;font-family:Marcellus,serif;font-weight:400;font-size:var(--ov);line-height:1;color:#d79e85}}
.st span{{font-size:var(--os);font-weight:700}}
.gets{{font-size:var(--fs);line-height:1.5}} .gets b{{color:#8fcfa4}}
.link{{display:flex;align-items:center;gap:20px;background:#f2f5f0;color:#17251c;border-radius:18px;padding:16px 20px}}
.link img{{width:var(--qr);height:var(--qr);flex:none}}
.link b{{display:block;font-size:var(--lb);font-weight:900}}
.link span{{display:block;font-size:var(--ls);color:#9a5f48;font-weight:700;word-break:break-all;margin-top:4px}}
.agent{{margin-top:auto;display:flex;align-items:center;gap:18px;border-top:1px solid #34573f;padding-top:var(--gap)}}
.agent img{{width:var(--av);height:var(--av);border-radius:50%;object-fit:cover;object-position:50% 12%;border:3px solid #c0866d}}
.agent .n{{font-weight:800;font-size:var(--an)}} .agent .r{{color:#b9c9bd;font-size:var(--os)}}
.agent .p{{margin-left:auto;text-align:right}}
.agent .p small{{display:block;color:#d79e85;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:calc(var(--os)*.85)}}
.agent .p b{{font-size:var(--ph)}}
"""
imgs = "".join(f'<img src="file://{A}/{f}.jpg" alt="">' for f in ("2BHK_2BHK06", "3BHK_3BHK11", "1BHK_1BHK002"))
body = f"""<div class=pics>{imgs}<div class=badge>For brokers</div></div>
<div class=panel>
 <div><div class=eb>IMAN Developers · Live availability</div>
 <h1>Find your client's unit <span>in seconds</span></h1>
 <div class=sub>Enter what your client needs. See every IMAN unit available today that fits.</div></div>
 <div class=steps><div class=st><b>1</b><span>Budget</span></div><div class=st><b>2</b><span>Location</span></div><div class=st><b>3</b><span>Payment plan</span></div><div class=st><b>4</b><span>Bedrooms</span></div></div>
 <div class=gets>For every unit: <b>price after discount</b> · <b>every instalment</b> · <b>cash price</b> · <b>floor plan</b> · <b>your 7%</b></div>
 <div class=link><img src="{QR}" alt=""><div><b>Scan or tap the link</b><span>{LINK.replace('https://','')}</span></div></div>
 <div class=agent><img src="file://{SAM}" alt=""><div><div class=n>Sam Jabr</div><div class=r>Senior Sales Manager · IMAN Developers</div></div>
  <div class=p><small>WhatsApp</small><b>+971 50 175 2771</b></div></div>
</div>"""
SIZES = {
 "post": dict(w=1080, h=1350, img=650, pad="40px", gap="18px", eb="18px", h1="54px", fs="22px", ov="38px", os="18px", qr="130px", lb="25px", ls="19px", av="72px", an="26px", ph="28px"),
 "story": dict(w=1080, h=1920, img=1000, pad="52px", gap="26px", eb="22px", h1="68px", fs="26px", ov="48px", os="21px", qr="170px", lb="30px", ls="23px", av="90px", an="31px", ph="33px"),
}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for k, v in SIZES.items():
        vars_ = ";".join(f"--{a}:{x}px" if isinstance(x, int) else f"--{a}:{x}" for a, x in v.items())
        f = os.path.join(OUT, f"finder-{k}.html")
        open(f, "w").write(f"<!doctype html><html><head><meta charset=utf-8><style>:root{{{vars_}}}{css}</style></head><body>{body}</body></html>")
        pg = b.new_page(viewport={"width": v["w"], "height": v["h"]}); pg.goto("file://" + f); pg.wait_for_timeout(700)
        pg.screenshot(path=os.path.join(OUT, f"Find your unit - Sam Jabr - {k}.jpg"), type="jpeg", quality=90)
    b.close()
print("ok")
