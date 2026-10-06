"""Build the availability & offers PDF that Sam sends to partners.

Usage:  python3 availability/tools/make_offers_pdf.py 2026-10-01

Reads the IMAN inventory PDFs in availability/<date>/, lays out one table per
project with the offers, one page per unit (payment plan and floor plan,
reached by tapping the unit number), appends the original lists, and stamps Sam's
name and number on every page. Writes the PDF into availability/<date>/.
Edit PROJECTS when offers change.
"""
import html, os, sys
import pymupdf
from playwright.sync_api import sync_playwright

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(TOOLS))
SITE = os.path.join(REPO, "site")

AGENT = "Sam Jabr · Senior Sales Manager · OG Team · IMAN Developers · WhatsApp +971 50 175 2771"
WA = "https://wa.me/971501752771"

# match: start of the inventory PDF file name. cash: discount on 100% payment.
# schedule: payment plan milestones. plans: floor plan file prefix in site/assets/plans/.
PROJECTS = [
    dict(match="113", name="113 Residences", area="Al Sufouh Gardens", img="img/113-residences.jpg",
         offer=["From AED 2M", "40/60 payment plan", "Up to 4% discount", "14% discount on 100% payment", "7% commission"],
         bonus="Bonus: 3 units = AED 50K · 5 units = AED 100K", plan="40/60", cash=0.14, plans="113-residences",
         schedule=[(20, "Within 30 days of booking"), (10, "Within 90 days of booking"), (10, "At 40% construction"), (60, "On handover")],
         loc="https://maps.app.goo.gl/WCMSqZvg8h2uBqjL9",
         mkt="https://drive.google.com/drive/folders/1kE-KUHmkLYhNm5r71XLE72S3g4WZqRBJ?usp=sharing"),
    dict(match="OXFORD COVE", name="Oxford Cove", area="Jumeirah Village Circle (JVC)", img="assets/oxford-cove-main.webp",
         offer=["4% discount", "50/50 payment plan", "14% discount on full cash payment", "7% commission"],
         plan="50/50", cash=0.14, plans="oxford-cove", loc="https://maps.app.goo.gl/orznbkhTdke94kGM7",
         schedule=[(50, "In instalments before handover"), (50, "On handover")],
         mkt="https://drive.google.com/drive/folders/1u3iiAnrIkTITz4lvnTTJzU6c8gaIwXiZ"),
    dict(match="SIERRA", name="Sierra by Iman · Retail", area="Motor City", img="assets/sierra-by-iman-main.webp",
         offer=["40/60 payment plan", "Up to 4% discount", "18% discount on full cash payment", "7% commission"],
         plan="40/60", cash=0.18, plans="sierra-by-iman", loc="https://www.google.com/maps?cid=2303450858755146668", mkt=None,
         schedule=[(40, "In instalments before handover"), (60, "On handover")]),
]

TYPE = {"one bedroom with study": "1 BR + Study", "two bedroom": "2 BR", "two bedroom with study": "2 BR + Study",
        "two bedroom with maid": "2 BR + Maid", "three bedroom with study": "3 BR + Study", "three bedroom with maid": "3 BR + Maid",
        "four bedroom duplex with pool": "4 BR Duplex + Pool", "studio": "Studio", "one bedroom": "1 BR", "retail": "Retail"}
e = html.escape
num = lambda s: float(s.replace(",", ""))
aed = lambda n: f"{round(n):,}"
anchor = lambda p, u: f"u-{p['plans']}-{u['no']}"
DISC = 0.04


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
            units.append(dict(no=no, floor=fl, view=view, type=typ, suite=int(num(s)), balcony=int(num(b)),
                              total=int(num(tot)), price=num(price)))
        i += 11
    return units


def table(p, units):
    us = sorted(units, key=lambda u: u["price"])
    retail = us[0]["type"] == "Retail"
    head = ("<tr><th>Unit</th><th>Floor</th><th>Type</th><th>View</th>"
            + ("<th class=r>Area (sq ft)</th>" if retail else "<th class=r>Suite</th><th class=r>Balcony</th><th class=r>Total sq ft</th>")
            + f"<th class=r>Price (AED)</th><th class=r>{p['plan']} with 4% off</th><th class=r>100% payment, {round(p['cash']*100)}% off</th></tr>")
    rows = []
    for u in us:
        size = (f"<td class=r>{u['total']:,.2f}</td>" if retail else
                f"<td class=r>{u['suite']:,}</td><td class=r>{u['balcony']:,}</td><td class=r><b>{u['total']:,}</b></td>")
        fl = "G" if u["floor"].lower().startswith("ground") else u["floor"].split()[0]
        rows.append(f"<tr><td><a class=ulink href='#{anchor(p, u)}'>{e(u['no'])}</a></td><td>{fl}</td><td>{e(TYPE.get(u['type'].lower(), u['type']))}</td>"
                    f"<td>{e(u['view'])}</td>{size}<td class='r b'>{aed(u['price'])}</td>"
                    f"<td class=r>{aed(u['price'] * (1 - DISC))}</td><td class='r cash'>{aed(u['price'] * (1 - p['cash']))}</td></tr>")
    return f"<table><thead>{head}</thead><tbody>{''.join(rows)}</tbody></table>"


def section(p, units):
    links = [f"<a href='{p['loc']}'>Location ↗</a>"] + ([f"<a href='{p['mkt']}'>Marketing materials ↗</a>"] if p["mkt"] else [])
    n = len(units)
    return f"""<section class=proj id="p-{p['plans']}"><div class=ph><img src="file://{os.path.join(SITE, p['img'])}" alt="">
  <div class=pt><div class=eb>{e(p['area'])} · {n} unit{'s' if n > 1 else ''} available</div><h2>{e(p['name'])}</h2>
  <ul class=offer>{''.join(f'<li>{e(o)}</li>' for o in p['offer'])}</ul>
  {f"<div class=bonus>{e(p['bonus'])}</div>" if p.get('bonus') else ''}
  <div class=links>{' '.join(links)}</div></div></div>{table(p, units)}</section>"""


def detail(p, u):
    """One page per unit: facts, payment plan with amounts, and the floor plan."""
    retail = u["type"] == "Retail"
    disc = u["price"] * (1 - DISC)
    cash = u["price"] * (1 - p["cash"])
    fl = u["floor"]
    facts = [("Floor", fl), ("View", u["view"])]
    if retail:
        facts.append(("Area", f"{u['total']:,.2f} sq ft"))
    else:
        facts += [("Suite", f"{u['suite']:,} sq ft"), ("Balcony", f"{u['balcony']:,} sq ft"),
                  ("Total", f"{u['total']:,} sq ft · {round(u['total'] * 0.092903):,} m²")]
    plan_img = os.path.join(SITE, "assets", "plans", f"{p['plans']}-{u['no']}.webp")
    rows = "".join(f"<tr><td>{pc}%</td><td>{e(label)}</td><td class='r b'>AED {aed(disc * pc / 100)}</td></tr>" for pc, label in p["schedule"])
    msg = f"Hi Sam, I'm interested in unit {u['no']} at {p['name']}. Is it still available?"
    wa = WA + "?text=" + html.escape(__import__("urllib.parse").parse.quote(msg))
    return f"""<section class=unitpage id="{anchor(p, u)}">
  <div class=uhead><div><div class=eb>{e(p['name'])} · {e(p['area'])}</div>
    <h1>Unit {e(u['no'])}</h1><div class=utype>{e(TYPE.get(u['type'].lower(), u['type']))}</div></div>
    <a class=back href="#p-{p['plans']}">← Back to {e(p['name'])} list</a></div>
  <dl class=facts>{''.join(f'<div><dt>{k}</dt><dd>{e(v)}</dd></div>' for k, v in facts)}</dl>
  <div class=pay>
    <div class=card><div class=ck>{p['plan']} payment plan · with 4% discount</div>
      <div class=cv>AED {aed(disc)}</div><div class=cs>Original price AED {aed(u['price'])} · discount up to 4%</div>
      <table class=sch><tbody>{rows}</tbody></table></div>
    <div class='card alt'><div class=ck>100% payment · {round(p['cash'] * 100)}% discount</div>
      <div class=cv>AED {aed(cash)}</div><div class=cs>Saving AED {aed(u['price'] - cash)} on the original price</div>
      <a class=ask href="{wa}">Ask Sam about unit {e(u['no'])} on WhatsApp</a></div>
  </div>
  {f'<div class=plan><img src="file://{plan_img}" alt=""></div>' if os.path.isfile(plan_img) else '<p class=note>Floor plan available on request.</p>'}
</section>"""


CSS = f"""
@font-face{{font-family:Marcellus;src:url(file://{TOOLS}/marcellus.woff2) format('woff2')}}
@font-face{{font-family:Figtree;src:url(file://{TOOLS}/figtree.woff2) format('woff2');font-weight:300 900}}
@page{{size:A4;margin:12mm 12mm 16mm}}
*{{box-sizing:border-box}}
body{{margin:0;font:9.5pt/1.45 Figtree,'DejaVu Sans',sans-serif;color:#17251c}}
h2{{font-family:Marcellus,'DejaVu Serif',serif;font-weight:400;margin:3px 0 6px;line-height:1.1;font-size:18pt}}
.proj{{margin-top:16px}} .proj:first-child{{margin-top:0}}
.ph{{display:flex;gap:14px;border:1px solid #dde4dc;border-radius:10px;overflow:hidden;break-inside:avoid}}
.ph img{{width:34%;object-fit:cover}}
.pt{{padding:12px 14px 12px 0;flex:1}}
.eb{{font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:#9a5f48;font-weight:700}}
.offer{{margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:5px}}
.offer li{{background:#e9eee8;border-radius:99px;padding:2px 9px;font-weight:600;font-size:8.5pt}}
.bonus{{margin-top:7px;background:#c0866d;color:#1b120d;border-radius:6px;padding:4px 9px;font-weight:700;display:inline-block}}
.links{{margin-top:8px;display:flex;gap:14px;font-weight:600}} .links a{{color:#1d3f2b}}
table{{width:100%;border-collapse:collapse;margin-top:8px;font-size:8.5pt}}
thead{{display:table-header-group}}
th{{background:#1d3f2b;color:#f2f5f0;text-align:left;padding:5px 6px;font-weight:600;font-size:7.5pt}}
td{{padding:4px 6px;border-bottom:1px solid #e3e8e2;font-variant-numeric:tabular-nums}}
tr{{break-inside:avoid}} tbody tr:nth-child(even) td{{background:#f6f8f5}}
.r{{text-align:right}} .b{{font-weight:700}} td.cash{{color:#9a5f48;font-weight:600}}
.note{{margin-top:14px;font-size:7.5pt;color:#5b6b60;border-top:1px solid #dde4dc;padding-top:8px}}
.top{{display:flex;justify-content:space-between;align-items:center;gap:12px;border-bottom:2px solid #1d3f2b;padding-bottom:8px;margin-bottom:12px}}
.logo{{color:#9a5f48;font-family:Marcellus,serif;letter-spacing:.3em;font-size:13pt;line-height:1}}
.logo small{{display:block;font-size:5.5pt;letter-spacing:.5em;margin-top:3px}}
.agent{{display:flex;align-items:center;gap:10px;text-align:right;line-height:1.3}} .agent img{{width:52px;height:52px;border-radius:50%;object-fit:cover;object-position:50% 12%;border:2px solid #c0866d}}
.agent b{{font-size:12pt}} .agent .t{{color:#5b6b60;font-size:8.5pt}} .og{{display:inline-block;border:1px solid #9a5f48;color:#9a5f48;border-radius:99px;padding:0 6px;font-size:7pt;font-weight:700;margin-left:4px}}
.agent a{{color:#1d3f2b;font-weight:700;text-decoration:none;font-size:10pt}}
.hint{{font-size:8pt;color:#5b6b60;margin:0 0 10px}}
a.ulink{{color:#9a5f48;font-weight:700;text-decoration:underline}}
.unitpage{{break-before:page}}
.uhead{{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}}
.uhead h1{{font-family:Marcellus,'DejaVu Serif',serif;font-weight:400;font-size:28pt;margin:4px 0 0;line-height:1}}
.utype{{font-size:12pt;font-weight:600;margin-top:4px}}
a.back{{font-size:9pt;font-weight:700;color:#1d3f2b;border:1px solid #1d3f2b;border-radius:99px;padding:4px 12px;text-decoration:none;white-space:nowrap}}
.facts{{display:flex;flex-wrap:wrap;gap:6px 22px;margin:12px 0;padding:10px 0;border-block:1px solid #dde4dc}}
.facts dt{{font-size:7pt;text-transform:uppercase;letter-spacing:.1em;color:#5b6b60}} .facts dd{{margin:0;font-weight:600}}
.pay{{display:grid;grid-template-columns:1.3fr 1fr;gap:10px}}
.card{{border:1px solid #dde4dc;border-radius:10px;padding:12px 14px;break-inside:avoid}}
.card.alt{{background:#1d3f2b;color:#f2f5f0;border-color:#1d3f2b}}
.ck{{font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;font-weight:700;color:#9a5f48}} .alt .ck{{color:#d79e85}}
.cv{{font-family:Marcellus,serif;font-size:20pt;margin-top:2px}}
.cs{{font-size:8pt;color:#5b6b60}} .alt .cs{{color:#b9c9bd}}
table.sch{{margin-top:8px}} table.sch td{{padding:4px 4px}}
a.ask{{display:inline-block;margin-top:12px;background:#c0866d;color:#1b120d;border-radius:99px;padding:5px 12px;font-weight:700;font-size:8.5pt;text-decoration:none}}
.plan{{margin-top:12px;border:1px solid #dde4dc;border-radius:10px;overflow:hidden;text-align:center;break-inside:avoid}}
.plan img{{max-width:100%;max-height:150mm;object-fit:contain}}
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
        page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(0, r.height - 26, r.width, r.height), "uri": WA})


def main(date):
    folder = os.path.join(REPO, "availability", date)
    pdfs = sorted(f for f in os.listdir(folder) if f.lower().endswith(".pdf") and not f.startswith("IMAN Availability"))
    parts, sources, details = [], [], []
    for p in PROJECTS:
        f = next((f for f in pdfs if f.upper().startswith(p["match"])), None)
        if not f:
            continue
        units = parse(os.path.join(folder, f))
        if units:
            parts.append(section(p, units))
            details += [detail(p, u) for u in sorted(units, key=lambda u: u["price"])]
            sources.append(os.path.join(folder, f))
            print(f"{p['name']}: {len(units)} units from {f}")
    d = "-".join(reversed(date.split("-")))
    note = (f"Prices in AED as listed in IMAN's inventory dated {d.replace('-', '.')}, sorted from lowest price. "
            "\"With 4% off\" shows the maximum discount on the payment plan (\"up to 4%\"); the 100% payment column applies to full payment. "
            "Final price, availability and offer terms are subject to confirmation at booking. Excludes DLD and registration fees. "
            "The original IMAN inventory lists are attached at the end of this file.")
    top = ("<div class=top><div class=logo>IMAN<small>DEVELOPERS</small></div>"
           f"<div class=agent><div><b>Sam Jabr</b><span class=og>OG TEAM</span><br><span class=t>Senior Sales Manager · IMAN Developers</span><br>"
           f"<a href='{WA}'>WhatsApp +971 50 175 2771</a></div><img src='file://{os.path.join(SITE, 'img', 'sam-jabr.jpg')}' alt=''></div></div>"
           "<p class=hint>Tap a unit number to see its payment plan and floor plan.</p>")
    page = (f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{top}{''.join(parts)}"
            f"<p class=note>{e(note)}</p>{''.join(details)}</body></html>")
    tmp_html = os.path.join(folder, ".offers.html")
    tmp_pdf = os.path.join(folder, ".offers.pdf")
    open(tmp_html, "w").write(page)
    with sync_playwright() as pw:
        exe = "/opt/pw-browsers/chromium"
        b = pw.chromium.launch(executable_path=exe) if os.path.isfile(exe) else pw.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + tmp_html)
        pg.wait_for_timeout(500)
        pg.pdf(path=tmp_pdf, format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    doc = pymupdf.open(tmp_pdf)
    for s in sources:
        doc.insert_pdf(pymupdf.open(s))
    direct_links(doc)
    stamp(doc)
    doc.set_metadata({"title": f"IMAN Availability & Offers · {d.replace('-', '.')}", "author": "Sam Jabr, IMAN Developers"})
    out = os.path.join(folder, f"IMAN Availability & Offers - Sam Jabr - {d.replace('-', '.')}.pdf")
    doc.rewrite_images(dpi_threshold=170, dpi_target=150, quality=72)  # keeps the file small enough for WhatsApp
    doc.save(out, garbage=4, deflate=True)
    os.remove(tmp_html)
    os.remove(tmp_pdf)
    print(f"wrote {out} ({len(doc)} pages)")


if __name__ == "__main__":
    main(sys.argv[1])
