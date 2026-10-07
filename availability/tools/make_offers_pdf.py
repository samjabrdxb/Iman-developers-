"""Build the availability & offers PDF that Sam sends to partners.

Usage:  python3 availability/tools/make_offers_pdf.py 2026-10-01

Reads the IMAN inventory PDFs in availability/<date>/, lays out a cover, an
overview of the offers, one page per project (offer, payment plan and a unit
table with instalments and commission), one page per unit (payment schedule
and floor plan, reached by tapping the unit number), appends the original lists, and stamps Sam's
name and number on every page. Writes the PDF into availability/<date>/.
Edit PROJECTS when offers change.
"""
import datetime, html, os, shutil, sys, urllib.parse
import pymupdf
from PIL import Image
from playwright.sync_api import sync_playwright

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(TOOLS))
SITE = os.path.join(REPO, "site")

AGENT = "Sam Jabr · Senior Sales Manager · OG Team · IMAN Developers · WhatsApp +971 50 175 2771"
WA = "https://wa.me/971501752771"

# match: start of the inventory PDF file name. disc: discount on the payment plan (default 4%). cash: discount on 100% payment.
# schedule: payment plan milestones as (percent, long label, short column label). plans: floor plan file prefix in site/assets/plans/.
PROJECTS = [
    dict(match="113", name="113 Residences", area="Al Sufouh Gardens", img="img/113-residences.jpg", handover="Q2 2029",
         offer=["4% discount", "40/60 payment plan", "14% off full cash", "7% commission"],
         bonus="Bonus: 3 units = AED 50K · 5 units = AED 100K", plan="40/60", cash=0.14, plans="113-residences",
         schedule=[(20, "Within 30 days of booking", "20% booking"), (10, "Within 90 days of booking", "10% at 90 days"),
                   (10, "At 40% construction", "10% at 40% built"), (60, "On handover", "60% handover")],
         loc="https://maps.app.goo.gl/WCMSqZvg8h2uBqjL9",
         mkt="https://drive.google.com/drive/folders/1kE-KUHmkLYhNm5r71XLE72S3g4WZqRBJ?usp=sharing"),
    dict(match="OXFORD COVE", name="Oxford Cove", area="Jumeirah Village Circle (JVC)", img="assets/oxford-cove-main.webp",
         offer=["4% discount", "50/50 payment plan", "14% off full cash", "7% commission"],
         plan="50/50", cash=0.14, plans="oxford-cove", loc="https://maps.app.goo.gl/orznbkhTdke94kGM7",
         schedule=[(50, "In instalments before handover", "50% before handover"), (50, "On handover", "50% handover")],
         mkt="https://drive.google.com/drive/folders/1u3iiAnrIkTITz4lvnTTJzU6c8gaIwXiZ"),
    dict(match="SIERRA RESIDENTIAL", key="sierra-res", name="Sierra by Iman · Residential", area="Motor City", img="assets/sierra-by-iman-main.webp",
         offer=["8% discount", "40/60 payment plan", "22% off full cash", "7% commission"],
         plan="40/60", disc=0.08, cash=0.22, plans="sierra-by-iman", loc="https://www.google.com/maps?cid=2303450858755146668", mkt=None,
         schedule=[(40, "In instalments during construction", "40% construction"), (60, "On handover", "60% handover")]),
    dict(match="SIERRA RETAIL", key="sierra-retail", name="Sierra by Iman · Retail", area="Motor City", img="assets/sierra-by-iman-main.webp",
         offer=["4% discount", "40/60 payment plan", "18% off full cash", "7% commission"],
         plan="40/60", cash=0.18, plans="sierra-by-iman", loc="https://www.google.com/maps?cid=2303450858755146668", mkt=None,
         schedule=[(40, "In instalments during construction", "40% construction"), (60, "On handover", "60% handover")]),
]
COMMISSION = 0.07
COMING = dict(name="The Element by IMAN", area="Dubai Science Park", img="img/dsp-teaser.jpg",
              points=["Pre-launch: expression of interest open", "AED 50,000 EOI, fully refundable", "Studio, 1 and 2 bedrooms plus retail",
                      "Priority token and unit selection, first come first served"])

TYPE = {"one bedroom with study": "1 BR + Study", "two bedroom": "2 BR", "two bedroom with study": "2 BR + Study",
        "two bedroom with maid": "2 BR + Maid", "three bedroom with study": "3 BR + Study", "three bedroom with maid": "3 BR + Maid",
        "four bedroom duplex with pool": "4 BR Duplex + Pool", "studio": "Studio", "one bedroom": "1 BR", "retail": "Retail"}
e = html.escape
num = lambda s: float(s.replace(",", ""))
aed = lambda n: f"{round(n):,}"
anchor = lambda p, u: f"u-{p.get('key', p['plans'])}-{u['no']}"
DISC = 0.04
TMP = "/tmp/iman-offers-img"


def parse(path):
    """Return the available units in one IMAN inventory PDF."""
    lines = [l.strip() for p in pymupdf.open(path) for l in p.get_text("text").split("\n") if l.strip()]
    units = []
    if any(l.startswith("RETAIL-") for l in lines):  # retail layout: unit, floor, B/R, view, internal, total, price, status
        for i, l in enumerate(lines):
            if l.startswith("RETAIL-") and lines[i + 7].lower() == "available":
                units.append(dict(no=l, floor=lines[i + 1], view=lines[i + 3], type="Retail", suite=None,
                                  balcony=None, total=num(lines[i + 5]), price=num(lines[i + 6])))
        return units
    # residential layout: project, unit, floor, category, view, type, suite, balcony, total, price, status
    project = lines[lines.index("Status") + 1].upper()
    i = lines.index("Status") + 1
    while i + 10 < len(lines) and lines[i].upper() == project:
        no, fl, _cat, view, typ, s, b, tot, price, status = lines[i + 1:i + 11]
        if status.lower() == "available":
            whole = lambda v: int(v) if v == int(v) else v
            units.append(dict(no=no, floor=fl, view=view, type=typ, suite=whole(num(s)), balcony=whole(num(b)),
                              total=whole(num(tot)), price=num(price)))
        i += 11
    return units


def jpg(path, width=1400):
    """file:// URL of a JPEG copy of an image, so Chromium embeds a small JPEG instead of a lossless copy."""
    os.makedirs(TMP, exist_ok=True)
    out = os.path.join(TMP, os.path.basename(path).rsplit(".", 1)[0] + f"-{width}.jpg")
    if not os.path.exists(out):
        im = Image.open(path).convert("RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(out, quality=80, optimize=True)
    return "file://" + out


def key(p):
    return p.get("key", p["plans"])


def short(u):
    return TYPE.get(u["type"].lower(), u["type"])


def beds(u):
    t = u["type"].lower()
    return 0 if "studio" in t else next((n for w, n in (("one", 1), ("two", 2), ("three", 3), ("four", 4), ("five", 5)) if t.startswith(w)), None)


def money(n):
    """AED amount in short form: 2.10M, 950K."""
    return f"{n / 1e6:.2f}M" if n >= 1e6 else f"{round(n / 1e3):,}K"


def stats(p, units):
    d = p.get("disc", DISC)
    low = min(u["price"] for u in units)
    b = sorted({beds(u) for u in units if beds(u) is not None})
    if units[0]["type"] == "Retail":
        kind = "Retail shops"
        rng = f"{min(u['total'] for u in units):,.0f} to {max(u['total'] for u in units):,.0f} sq ft"
    else:
        name = lambda n: "Studio" if n == 0 else f"{n} BR"
        kind = "Apartments"
        rng = name(b[0]) if len(b) == 1 else f"{name(b[0])} to {name(b[-1])}"
    return dict(n=len(units), kind=kind, rng=rng, offer=low * (1 - d), cash=low * (1 - p["cash"]))


def card(p, units):
    """Project card on the overview page."""
    s = stats(p, units)
    chips = "".join(f"<li>{e(o)}</li>" for o in p["offer"])
    return f"""<a class=pcard href="#p-{key(p)}"><img src="{jpg(os.path.join(SITE, p['img']), 900)}" alt="">
  <div class=pcb><div class=eb>{e(p['area'])}</div><h3>{e(p['name'])}</h3>
  <div class=pn><b>{s['n']}</b> unit{'s' if s['n'] > 1 else ''} · {e(s['rng'])}</div>
  <div class=pf><span>From</span> AED {money(s['offer'])}</div>
  <ul class=chips>{chips}</ul><div class=go>View units →</div></div></a>"""


def tiles(p):
    sch = p["schedule"]
    t = '<span class=arr>›</span>'.join(f"<div class=tile><b>{pc}%</b><span>{e(lbl)}</span></div>" for pc, lbl, _ in sch)
    shade = ["#c0866d", "#d6a893", "#e8cbbd", "#f3e4dc"]
    bar = "".join(f"<i style='flex:{pc};background:{shade[min(i, 3)] if pc < 50 or i < len(sch) - 1 else '#fff'}'></i>" for i, (pc, _, _) in enumerate(sch))
    return f"<div class=tiles>{t}</div><div class=bar>{bar}</div>"


def table(p, units):
    d = p.get("disc", DISC)
    retail = units[0]["type"] == "Retail"
    head = ("<tr><th>Unit</th><th>Floor</th>" + ("" if retail else "<th>Type</th>") + "<th>View</th><th class=r>Sq ft</th>"
            f"<th class=r>List price</th><th class='r hl'>Offer −{round(d * 100)}%</th>"
            + "".join(f"<th class=r>{e(sh)}</th>" for _, _, sh in p["schedule"])
            + f"<th class='r ca'>Full cash −{round(p['cash'] * 100)}%</th><th class='r co'>Your {round(COMMISSION * 100)}%</th></tr>")
    cols = (8 if retail else 9) + len(p["schedule"])
    groups = {}
    for u in sorted(units, key=lambda u: u["price"]):
        groups.setdefault(short(u), []).append(u)
    rows = []
    for g, us in sorted(groups.items(), key=lambda kv: ((beds(kv[1][0]) or 0), kv[1][0]["price"])):
        if not retail:
            rows.append(f"<tr class=grp><td colspan={cols}>{e(g)} <span>· {len(us)} unit{'s' if len(us) > 1 else ''} · from AED {money(us[0]['price'] * (1 - d))}</span></td></tr>")
        for u in us:
            o = u["price"] * (1 - d)
            fl = "G" if u["floor"].lower().startswith("ground") else u["floor"].split()[0]
            rows.append(f"<tr><td><a class=ulink href='#{anchor(p, u)}'>{e(u['no'])}</a></td><td>{fl}</td>"
                        + ("" if retail else f"<td>{e(short(u))}</td>") + f"<td>{e(u['view'])}</td>"
                        f"<td class=r>{u['total']:,.0f}</td><td class='r lp'>{aed(u['price'])}</td><td class='r hl'>{aed(o)}</td>"
                        + "".join(f"<td class=r>{aed(o * pc / 100)}</td>" for pc, _, _ in p["schedule"])
                        + f"<td class='r ca'>{aed(u['price'] * (1 - p['cash']))}</td><td class='r co'>{aed(o * COMMISSION)}</td></tr>")
    return f"<table class=units><thead>{head}</thead><tbody>{''.join(rows)}</tbody></table>"


def section(p, units):
    s = stats(p, units)
    links = [f"<a href='{p['loc']}'>Location ↗</a>"] + ([f"<a href='{p['mkt']}'>Brochure &amp; marketing ↗</a>"] if p["mkt"] else [])
    facts = [(s["n"], "Units available"), (s["rng"], s["kind"]), ("AED " + money(s["offer"]), f"From, {p['plan']} offer price"),
             ("AED " + money(s["cash"]), "From, full cash price")]
    if p.get("handover"):
        facts.append((p["handover"], "Handover"))
    return f"""<section class=proj id="p-{key(p)}">
  <div class=band><div><h2>{e(p['name'])}</h2><div class=bs>{e(s['kind'])} · {e(s['rng'])} · {e(p['area'])}</div></div>
    <a class=toc href="#overview">All projects ↑</a></div>
  <div class=intro><img src="{jpg(os.path.join(SITE, p['img']), 900)}" alt="">
    <div class=facts>{''.join(f'<div><b>{e(str(v))}</b><span>{e(k)}</span></div>' for v, k in facts)}</div>
    <div class=offerbox><div class=ok>The offer</div><ul class=chips>{''.join(f'<li>{e(o)}</li>' for o in p['offer'])}</ul>
      {f"<div class=bonus>{e(p['bonus'])}</div>" if p.get('bonus') else ''}
      <div class=ok style='margin-top:10px'>{e(p['plan'])} payment plan</div>{tiles(p)}
      <div class=links>{' '.join(links)}</div></div></div>
  <p class=hint>{'Sorted by price' if units[0]['type'] == 'Retail' else 'Sorted by bedrooms, then price'}. Tap a unit number for its payment schedule and floor plan.</p>
  {table(p, units)}
</section>"""


def detail(p, u):
    """One page per unit: facts, payment schedule with amounts, and the floor plan."""
    retail = u["type"] == "Retail"
    pd = p.get("disc", DISC)
    offer = u["price"] * (1 - pd)
    cash = u["price"] * (1 - p["cash"])
    facts = [("Floor", u["floor"]), ("View", u["view"])]
    if retail:
        facts.append(("Area", f"{u['total']:,.2f} sq ft"))
    else:
        facts += [("Suite", f"{u['suite']:,} sq ft"), ("Balcony", f"{u['balcony']:,} sq ft"),
                  ("Total", f"{u['total']:,} sq ft · {round(u['total'] * 0.092903):,} m²")]
    plan_img = os.path.join(SITE, "assets", "plans", f"{p['plans']}-{u['no']}.webp")
    rows = "".join(f"<tr><td class=pc>{pc}%</td><td>{e(label)}</td><td class='r b'>AED {aed(offer * pc / 100)}</td></tr>" for pc, label, _ in p["schedule"])
    msg = f"Hi Sam, I'm interested in unit {u['no']} at {p['name']}. Is it still available?"
    wa = WA + "?text=" + html.escape(urllib.parse.quote(msg))
    plan = (f'<img src="{jpg(plan_img, 1100)}" alt="">' if os.path.isfile(plan_img) else "<p class=noplan>Floor plan available on request.</p>")
    return f"""<section class=unitpage id="{anchor(p, u)}">
  <div class=ucol>
    <a class=back href="#p-{key(p)}">← {e(p['name'])} list</a>
    <div class=eb style='margin-top:10px'>{e(p['name'])} · {e(p['area'])}</div>
    <h1>Unit {e(u['no'])}</h1><div class=utype>{e(short(u))}</div>
    <dl class=ufacts>{''.join(f'<div><dt>{k}</dt><dd>{e(v)}</dd></div>' for k, v in facts)}</dl>
    <div class=card><div class=ck>{p['plan']} payment plan · {round(pd * 100)}% off</div>
      <div class=cv>AED {aed(offer)}</div><div class=cs>List price <s>AED {aed(u['price'])}</s> · you save AED {aed(u['price'] - offer)}</div>
      <table class=sch><tbody>{rows}</tbody></table></div>
    <div class='card alt'><div class=ck>Full cash · {round(p['cash'] * 100)}% off</div>
      <div class=cv>AED {aed(cash)}</div><div class=cs>You save AED {aed(u['price'] - cash)}</div></div>
    <div class=comm>Your commission ({round(COMMISSION * 100)}%): <b>AED {aed(offer * COMMISSION)}</b> on the plan price · <b>AED {aed(cash * COMMISSION)}</b> on cash</div>
    <a class=ask href="{wa}">Reserve unit {e(u['no'])} with Sam on WhatsApp</a>
  </div>
  <div class=plan>{plan}</div>
</section>"""


def cover(date_long, parts):
    best = max((p for p, _ in parts), key=lambda p: p["cash"])
    n = sum(len(us) for _, us in parts)
    return f"""<section class=cover><img class=bg src="{jpg(os.path.join(SITE, 'img', '113-residences.jpg'))}" alt="">
  <div class=cin>
    <div class=logo>IMAN<small>DEVELOPERS</small></div>
    <div class=ct><div class=eb>Partner availability · {e(date_long)}</div><h1>Availability<br>&amp; Offers</h1>
      <div class=cp>{' · '.join(e(p['name'].split(' · ')[0]) for p in dict((p['plans'], p) for p, _ in parts).values())}</div>
      <ul class=hl3><li><b>{round(COMMISSION * 100)}%</b>commission</li><li><b>{n}</b>units available</li><li><b>{round(best['cash'] * 100)}%</b>off full cash · {e(best['name'].replace(' by Iman · ', ' '))} only</li></ul></div>
    <div class=me><img src="{jpg(os.path.join(SITE, 'img', 'sam-jabr.jpg'), 300)}" alt="">
      <div><b>Sam Jabr</b> <span class=og>OG TEAM</span><br><span>Senior Sales Manager · IMAN Developers</span><br>
      <a href="{WA}">WhatsApp +971 50 175 2771</a></div></div>
  </div></section>"""


def overview(parts):
    cards = "".join(card(p, us) for p, us in parts)
    c = COMING
    bonus = next((p["bonus"] for p, _ in parts if p.get("bonus")), None)
    return f"""<section class=over id=overview>
  <div class=band><div><h2>Today's offers at a glance</h2><div class=bs>Tap a project to see its units</div></div></div>
  <div class=cards>{cards}</div>
  <div class=row2>
    <div class=soon><img src="{jpg(os.path.join(SITE, c['img']), 900)}" alt=""><div><div class=eb>Coming soon · {e(c['area'])}</div>
      <h3>{e(c['name'])}</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in c['points'])}</ul>
      <a href="{WA}?text={urllib.parse.quote('Hi Sam, I would like to register an EOI for The Element by IMAN, Dubai Science Park.')}">Register EOI with Sam →</a></div></div>
    <div class=how>{f"<div class=bonus>{e(bonus)} (113 Residences)</div>" if bonus else ''}
      <div class=ok>How to use this file</div><ol><li>Tap a project card.</li><li>Tap any unit number to open its payment schedule, cash price, your commission and floor plan.</li>
      <li>Tap the green bar at the foot of any page to WhatsApp Sam.</li></ol></div>
  </div></section>"""


CSS = f"""
@font-face{{font-family:Marcellus;src:url(file://{TOOLS}/marcellus.woff2) format('woff2')}}
@font-face{{font-family:Figtree;src:url(file://{TOOLS}/figtree.woff2) format('woff2');font-weight:300 900}}
@page{{size:A4 landscape;margin:0 0 11mm}}
@page cover{{margin:0}}
:root{{--g:#1d3f2b;--g2:#16301f;--c:#c0866d;--cd:#9a5f48;--cr:#f6f3ee;--ln:#e3e8e2;--mu:#5b6b60}}
*{{box-sizing:border-box}}
body{{margin:0;font:9pt/1.4 Figtree,'DejaVu Sans',sans-serif;color:#17251c}}
h1,h2,h3{{font-family:Marcellus,'DejaVu Serif',serif;font-weight:400;margin:0;line-height:1.05}}
a{{color:inherit}}
.eb{{font-size:7pt;letter-spacing:.16em;text-transform:uppercase;color:var(--cd);font-weight:700}}
.og{{display:inline-block;border:1px solid var(--c);color:var(--c);border-radius:99px;padding:0 7px;font-size:7pt;font-weight:800;letter-spacing:.08em;vertical-align:2px}}
.logo{{color:var(--c);font-family:Marcellus,serif;letter-spacing:.42em;font-size:20pt;line-height:1}}
.logo small{{display:block;font-size:6pt;letter-spacing:.62em;margin-top:5px}}
.cover{{page:cover;position:relative;width:297mm;height:210mm;overflow:hidden;background:var(--g2);color:#f2f5f0}}
.cover .bg{{position:absolute;right:0;top:0;width:47%;height:100%;object-fit:cover;border-left:3px solid var(--c)}}
.cin{{position:relative;height:100%;padding:16mm 14mm 20mm 16mm;display:flex;flex-direction:column;justify-content:space-between;width:53%}}
.ct .eb{{color:var(--c)}} .ct h1{{font-size:46pt;margin:8px 0 10px}}
.cp{{color:#c9d6cc;font-size:11pt}}
.hl3{{list-style:none;padding:0;margin:16px 0 0;display:flex;gap:10px}}
.hl3 li{{border:1px solid #8a6a55;border-radius:10px;padding:8px 12px;font-size:8pt;color:#c9d6cc;text-transform:uppercase;letter-spacing:.08em}}
.hl3 b{{display:block;font-family:Marcellus,serif;font-size:19pt;color:var(--c);letter-spacing:0;text-transform:none}}
.me{{display:flex;align-items:center;gap:12px;background:#24452f;border:1px solid #3a5a45;border-radius:14px;padding:10px 16px 10px 10px;width:max-content}}
.me img{{width:62px;height:62px;border-radius:50%;object-fit:cover;object-position:50% 12%;border:2px solid var(--c)}}
.me b{{font-size:13pt}} .me span{{color:#c9d6cc;font-size:8.5pt}} .me a{{color:#fff;font-weight:700;text-decoration:none;font-size:10pt}}
.band{{background:var(--g);color:#f2f5f0;padding:9mm 12mm 6mm;display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid var(--c)}}
.band h2{{font-size:24pt}} .bs{{color:#c9d6cc;font-size:9pt;margin-top:4px}}
a.toc{{color:#f2f5f0;font-weight:700;font-size:8.5pt;text-decoration:none;border:1px solid #6f8a78;border-radius:99px;padding:3px 11px}}
.over,.proj{{break-before:page}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;padding:8mm 12mm 0}}
.pcard{{display:block;text-decoration:none;border:1px solid var(--ln);border-radius:12px;overflow:hidden;background:#fff}}
.pcard img{{width:100%;height:30mm;object-fit:cover;display:block}}
.pcb{{padding:9px 11px 11px}} .pcb h3{{font-size:13.5pt;margin:3px 0 4px}}
.pn{{font-size:8.5pt;color:var(--mu)}} .pn b{{color:#17251c}}
.pf{{font-family:Marcellus,serif;font-size:15pt;color:var(--g);margin:5px 0 6px}} .pf span{{font-family:Figtree,sans-serif;font-size:7.5pt;color:var(--mu);text-transform:uppercase;letter-spacing:.1em}}
.chips{{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:4px}}
.chips li{{background:#eaf0e9;color:var(--g);border-radius:99px;padding:2px 8px;font-weight:700;font-size:7.5pt}}
.chips li:first-child{{background:var(--c);color:#1b120d}}
.go{{margin-top:8px;font-weight:800;color:var(--cd);font-size:8.5pt}}
.row2{{display:grid;grid-template-columns:1.45fr 1fr;gap:9px;padding:9px 12mm 0}}
.soon{{display:flex;gap:12px;border:1px solid var(--ln);border-radius:12px;overflow:hidden;background:var(--cr)}}
.soon img{{width:42%;object-fit:cover}} .soon>div{{padding:10px 12px 10px 0}} .soon h3{{font-size:14pt;margin:3px 0 4px}}
.soon ul{{margin:0;padding-left:15px;font-size:8.5pt}} .soon a{{display:inline-block;margin-top:7px;font-weight:800;color:var(--cd);text-decoration:none}}
.how{{border:1px solid var(--ln);border-radius:12px;padding:11px 13px}} .how ol{{margin:5px 0 0;padding-left:16px;font-size:8.5pt}}
.ok{{font-size:7pt;letter-spacing:.14em;text-transform:uppercase;font-weight:800;color:var(--cd)}}
.bonus{{background:var(--c);color:#1b120d;border-radius:8px;padding:6px 10px;font-weight:800;font-size:9pt;margin-bottom:9px;display:inline-block}}
.offerbox .bonus{{margin:8px 0 0}}
.intro{{display:grid;grid-template-columns:90mm 55mm 1fr;gap:10px;padding:7mm 12mm 0}}
.intro img{{width:100%;height:62mm;object-fit:cover;border-radius:12px}}
.facts{{display:flex;flex-direction:column;justify-content:space-between;border-left:3px solid var(--c);padding-left:10px}}
.facts b{{display:block;font-family:Marcellus,serif;font-size:14pt;color:var(--g);font-weight:400;line-height:1.1}}
.facts span{{font-size:6.8pt;text-transform:uppercase;letter-spacing:.1em;color:var(--mu);font-weight:700}}
.offerbox{{background:var(--g);color:#f2f5f0;border-radius:12px;padding:11px 13px}}
.offerbox .ok{{color:var(--c)}} .offerbox .chips{{margin-top:5px}} .offerbox .chips li{{background:#34573f;color:#fff}} .offerbox .chips li:first-child{{background:var(--c);color:#1b120d}}
.tiles{{display:flex;align-items:center;gap:3px;margin-top:6px}}
.tile{{flex:1;background:#fbf8f4;color:#17251c;border-radius:8px;padding:5px 4px;text-align:center}}
.tile b{{display:block;font-size:14pt;color:var(--g);line-height:1.05}} .tile span{{font-size:6.5pt;line-height:1.15;display:block}}
.arr{{color:var(--c);font-weight:900}}
.bar{{display:flex;height:5px;border-radius:3px;overflow:hidden;margin-top:6px;gap:1px}}
.links{{margin-top:9px;display:flex;gap:14px;font-weight:700;font-size:8.5pt}} .links a{{color:#fff}}
.hint{{margin:7px 12mm 0;font-size:7.5pt;color:var(--mu)}}
table.units{{width:calc(100% - 24mm);margin:4px 12mm 0;border-collapse:collapse;font-size:8.2pt}}
.units thead{{display:table-header-group}}
.units th{{background:var(--g);color:#f2f5f0;text-align:left;padding:5px 5px;font-weight:700;font-size:7pt;white-space:nowrap}}
.units th.hl{{background:var(--c);color:#1b120d}} .units th.ca{{background:#7b4a37}} .units th.co{{background:#2f5a40}}
.units td{{padding:3.6px 5px;border-bottom:1px solid var(--ln);font-variant-numeric:tabular-nums;white-space:nowrap}}
.units tr{{break-inside:avoid}}
.units tr.grp td{{background:var(--cr);font-weight:800;color:var(--g);padding-top:5px;font-size:8pt;border-bottom:1px solid #d9d2c6}} .grp span{{font-weight:600;color:var(--mu)}}
.units td.lp{{color:#8a958d;text-decoration:line-through;text-decoration-color:rgba(138,149,141,.5)}}
.units td.hl{{font-weight:800;color:var(--g);background:#fbf3ee}} .units td.ca{{font-weight:700;color:var(--cd)}} .units td.co{{font-weight:700;color:#2f5a40}}
.r{{text-align:right}} .units th.r{{text-align:right}} .b{{font-weight:700}}
a.ulink{{display:inline-block;min-width:44px;text-align:center;background:var(--g);color:#fff;border-radius:5px;padding:1px 6px;font-weight:800;text-decoration:none}}
.note{{margin:12px 12mm 0;font-size:7pt;color:var(--mu);border-top:1px solid var(--ln);padding-top:6px}}
.unitpage{{break-before:page;display:grid;grid-template-columns:100mm 1fr;gap:10mm;padding:9mm 12mm 0;height:199mm}}
.ucol h1{{font-size:30pt;margin-top:3px}} .utype{{font-size:12pt;font-weight:700;margin-top:3px}}
a.back{{display:inline-block;font-size:8.5pt;font-weight:800;color:var(--g);border:1.5px solid var(--g);border-radius:99px;padding:3px 12px;text-decoration:none}}
.ufacts{{display:flex;flex-wrap:wrap;gap:5px 18px;margin:9px 0;padding:7px 0;border-block:1px solid var(--ln)}}
.ufacts dt{{font-size:6.5pt;text-transform:uppercase;letter-spacing:.1em;color:var(--mu)}} .ufacts dd{{margin:0;font-weight:700;font-size:8.5pt}}
.card{{border:1px solid var(--ln);border-radius:12px;padding:9px 12px;margin-bottom:7px}}
.card.alt{{background:var(--g);color:#f2f5f0;border-color:var(--g)}}
.ck{{font-size:7pt;text-transform:uppercase;letter-spacing:.12em;font-weight:800;color:var(--cd)}} .alt .ck{{color:var(--c)}}
.cv{{font-family:Marcellus,serif;font-size:19pt;margin-top:1px}}
.cs{{font-size:7.5pt;color:var(--mu)}} .alt .cs{{color:#c9d6cc}}
table.sch{{width:100%;border-collapse:collapse;margin-top:5px;font-size:8.3pt}} .sch td{{padding:3px 2px;border-bottom:1px solid var(--ln)}} .sch tr:last-child td{{border:0}}
.sch td.pc{{font-weight:800;color:var(--cd);width:34px}}
.comm{{background:#eaf0e9;border-radius:10px;padding:7px 11px;font-size:8.3pt;color:var(--g)}}
a.ask{{display:block;text-align:center;margin-top:7px;background:var(--c);color:#1b120d;border-radius:99px;padding:7px 12px;font-weight:800;font-size:9pt;text-decoration:none}}
.plan{{border:1px solid var(--ln);border-radius:12px;overflow:hidden;display:flex;align-items:center;justify-content:center;background:#fff;height:186mm}}
.plan img{{max-width:100%;max-height:100%;object-fit:contain}}
.noplan{{color:var(--mu)}}
"""

def direct_links(doc):
    """Turn the browser's named jumps into plain page links, which every PDF viewer follows."""
    names = doc.resolve_names()
    for page in doc:
        for link in page.get_links():
            if link["kind"] != pymupdf.LINK_NAMED:
                continue
            target = names.get(link.get("nameddest") or link.get("name") or "")
            if target is None:
                continue
            page.delete_link(link)
            page.insert_link({"kind": pymupdf.LINK_GOTO, "from": link["from"], "page": target["page"], "to": pymupdf.Point(0, 0)})


def stamp(doc):
    """Put Sam's name and number at the foot of every page, with a WhatsApp link."""
    for page in doc:
        r = page.rect
        page.draw_rect(pymupdf.Rect(0, r.height - 26, r.width, r.height), color=None, fill=(0.114, 0.247, 0.169))
        w = pymupdf.get_text_length(AGENT, fontname="helv", fontsize=9)
        page.insert_text(((r.width - w) / 2, r.height - 10), AGENT, fontname="helv", fontsize=9, color=(1, 1, 1))
        num_ = f"{page.number + 1} / {len(doc)}"
        page.insert_text((r.width - 14 - pymupdf.get_text_length(num_, fontname="helv", fontsize=7.5), r.height - 10.5), num_,
                         fontname="helv", fontsize=7.5, color=(0.75, 0.53, 0.43))
        page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(0, r.height - 26, r.width, r.height), "uri": WA})


def main(date):
    folder = os.path.join(REPO, "availability", date)
    pdfs = sorted(f for f in os.listdir(folder) if f.lower().endswith(".pdf") and not f.startswith("IMAN Availability"))
    parts, sources = [], []
    for p in PROJECTS:
        f = next((f for f in pdfs if f.upper().startswith(p["match"] + " ") or f.upper().startswith(p["match"] + "-")), None)
        if not f:
            continue
        units = parse(os.path.join(folder, f))
        if units:
            parts.append((p, units))
            sources.append(os.path.join(folder, f))
            print(f"{p['name']}: {len(units)} units from {f}")
    dt = datetime.date.fromisoformat(date)
    d = dt.strftime("%d.%m.%Y")
    note = (f"Prices in AED from IMAN's inventory lists dated {d}. Offer price = list price less the project's plan discount; "
            "instalments are calculated on the offer price. Commission shown is an estimate on the price paid. "
            "Final price, availability and offer terms are subject to confirmation at booking. Excludes DLD and registration fees. "
            "The original IMAN inventory lists are attached at the end of this file.")
    sections = "".join(section(p, us) for p, us in parts)
    details = "".join(detail(p, u) for p, us in parts for u in sorted(us, key=lambda u: u["price"]))
    page = (f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>"
            f"{cover(f'{dt.day} {dt:%B %Y}', parts)}{overview(parts)}{sections}<p class=note>{e(note)}</p>{details}</body></html>")
    tmp_html = os.path.join(folder, ".offers.html")
    tmp_pdf = os.path.join(folder, ".offers.pdf")
    open(tmp_html, "w").write(page)
    with sync_playwright() as pw:
        exe = "/opt/pw-browsers/chromium"
        b = pw.chromium.launch(executable_path=exe) if os.path.isfile(exe) else pw.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + tmp_html)
        pg.wait_for_timeout(500)
        pg.pdf(path=tmp_pdf, print_background=True, prefer_css_page_size=True)
        b.close()
    doc = pymupdf.open(tmp_pdf)
    names = doc.resolve_names()
    made = len(doc)
    toc = [[1, "Cover", 1], [1, "Offers at a glance", names["overview"]["page"] + 1]]
    for p, us in parts:
        toc.append([1, p["name"], names[f"p-{key(p)}"]["page"] + 1])
        toc += [[2, f"Unit {u['no']} · {short(u)}", names[anchor(p, u)]["page"] + 1] for u in sorted(us, key=lambda u: u["price"])]
    toc.append([1, "Original IMAN lists", made + 1])
    for s in sources:
        doc.insert_pdf(pymupdf.open(s))
    direct_links(doc)
    stamp(doc)
    doc.set_toc(toc)
    doc.set_metadata({"title": f"IMAN Availability & Offers · {d}", "author": "Sam Jabr, IMAN Developers"})
    out = os.path.join(folder, f"IMAN Availability & Offers - Sam Jabr - {d}.pdf")
    doc.save(out, garbage=4, deflate=True)
    os.remove(tmp_html)
    os.remove(tmp_pdf)
    shutil.rmtree(TMP, ignore_errors=True)
    print(f"wrote {out} ({len(doc)} pages, {os.path.getsize(out) // 1024} KB)")

if __name__ == "__main__":
    main(sys.argv[1])
