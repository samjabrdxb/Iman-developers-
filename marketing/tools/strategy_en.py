"""English sales strategy brochure: "affordable luxury, quality over quantity", for Japanese brokers and international investors.

Usage:  python3 marketing/tools/strategy_en.py

Writes marketing/japan/iman-sales-strategy-en.pdf (A4 portrait, 2 pages): the
English twin of iman-japan-sales-strategy.pdf, with the same layout and numbers.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from japan_brochure import qr, src, e, WA, FINDER, REPO, P
from japan_strategy import CSS, LAUNCHED, DELIVERED, DEC_2026, PIPELINE
from playwright.sync_api import sync_playwright

OUT = os.path.join(REPO, "marketing", "japan", "iman-sales-strategy-en.pdf")


def quote(x):
    return f"<blockquote>{e(x)}</blockquote>"


def foot(n):
    return f"""<div class=foot><span>Sam Jabr · Senior Sales Manager · IMAN Developers · WhatsApp +971 50 175 2771</span><span>{n} / 2</span></div>"""


compare = [("Entry price", "Actual price relative to comparable developments"), ("Apartment layout", "Practical use of space and the floor plan"),
           ("Ceiling height", "Actual approved specifications"), ("Lobby and common areas", "Design and finishing quality"),
           ("Amenities", "Quality, quantity and variety"), ("Unit count", "Residential density and experience"),
           ("Developer delivery", "Completed and handed-over projects"), ("Payment plan", "Instalments and construction milestones"),
           ("Resale potential", "Historical transactions and comparable data")]

p1 = f"""<section class=page>
 <div class=top><div class=tl><div class=logo>IMAN<small>DEVELOPERS</small></div>
   <div class=eb>Sales strategy for Japanese brokers &amp; international investors</div>
   <h1>Affordable luxury.<br>Quality over quantity.</h1>
   <p class=tp>Fewer residences. More lifestyle amenities. Better attention to detail. Competitive entry prices.</p></div>
  <div class=ti style="background-image:url('{src(P['oxford-212']['image'])}')"><span>Oxford 212 · completed</span></div></div>

 <div class=stats><div><b>{LAUNCHED}</b><span>projects launched</span></div><div><b>{DELIVERED}</b><span>projects handed over</span></div>
  <div><b>+{DEC_2026}</b><span>expected in December 2026</span></div><div><b>{DELIVERED + DEC_2026}</b><span>delivered by end of 2026 (expected)</span></div></div>

 <div class=cols>
  <div><h3 class=sh>1. Sell the developer's philosophy, not just the apartment</h3>
   <p>IMAN Developers is a boutique developer focused on quality over quantity. Unlike developers that deliver thousands of units, IMAN concentrates on a limited number of carefully designed residential developments: an attractive choice for investors who want a premium residential product without entering the ultra-luxury price segment.</p></div>
  <div><h3 class=sh>2. Use IMAN's delivery record to build trust</h3>
   <p>For international buyers, especially those buying remotely, the developer's delivery history is essential. Completed buildings let buyers judge the actual finishing quality, common areas and lifestyle amenities.</p>
   {quote("With IMAN Developers, you're not investing based only on architectural renders. You're investing with a developer whose completed projects demonstrate its approach to quality and lifestyle.")}</div>
 </div>

 <h3 class=sh>3. What affordable luxury actually means: not cheap construction, a premium experience at a competitive price</h3>
 <div class=grid3>
  <div class=card><h4>The arrival experience</h4><ul><li>Impressive entrance lobbies</li><li>Double-height ceilings in selected developments</li><li>Elegant materials, colours and details</li><li>Thoughtful access and circulation</li></ul></div>
  <div class=card><h4>The apartment experience</h4><ul><li>Spacious, practical layouts</li><li>Ceilings of about 3.2 m in selected designs</li><li>Quality finishes and materials</li><li>Modern interior and exterior architecture</li></ul></div>
  <div class=card><h4>The lifestyle experience</h4><ul><li>Swimming pools</li><li>Fitness and wellness facilities</li><li>Relaxation and family spaces</li><li>Rooftop amenities; several amenity areas in selected projects</li></ul></div>
 </div>
 {quote("The difference with IMAN is that luxury starts from the moment residents enter the building, not only when they open their apartment door.")}

 <div class=cols>
  <div><h3 class=sh>4. Turn boutique scale into an investment advantage</h3>
   <ul class=dots><li>A more intimate residential environment</li><li>A stronger sense of privacy</li><li>A distinctive architectural identity</li><li>Thoughtfully allocated lifestyle spaces</li><li>A different living experience from high-density developments</li></ul>
   <p class=sm>IMAN's 2026 boutique pipeline (Oxford Cove, 113 Residences and the upcoming Dubai Science Park development) is about {PIPELINE} homes in total.</p>
   {quote("IMAN doesn't focus on maximising the number of apartments. It focuses on maximising the quality of the residential experience.")}
   <p class=warn>Fewer units do not automatically guarantee lower density, privacy or appreciation. Support these points with actual project plans and specifications.</p></div>
  <div><h3 class=sh>5. Sell the complete package, not the price alone</h3>
   <p class=sm>Don't lead with discounts. Compare the complete product against similar developments:</p>
   <table class=t><thead><tr><th>Investment factor</th><th>What the broker should demonstrate</th></tr></thead><tbody>
   {''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in compare)}</tbody></table>
   {quote("The question isn't simply how much the apartment costs. It's how much quality, space, lifestyle and long-term value you receive for that price.")}</div>
 </div>
 {foot(1)}</section>"""

steps = ["IMAN's boutique philosophy", "Completed projects and delivery history", "Actual quality, layouts and amenities", "Comparison with similar properties in the same price range",
         "Payment schedule, SPA, escrow, handover and buying process, from official documents", "Available inventory and questions, before discussing booking"]
p2 = f"""<section class=page>
 <div class=grid3>
  <div class=card><h4>6. Construction-linked payments mean transparency</h4><p>In selected payment structures, instalments follow the agreed construction schedule (at 113 Residences, for example, 10% is due at 40% construction). Buyers can see how their payments relate to progress on site.</p>
   <p class=warn>Always use the latest officially approved payment plan. Do not claim that every instalment is construction-linked, or that nothing is due unless construction has progressed.</p></div>
  <div class=card><h4>7. Demonstrate quality through completed projects</h4><p>Clients who cannot visit Dubai need visual proof. Use <b>Oxford 212</b>: building exterior, entrance and lobby, interior details, corridors and lifts, amenities, rooftop and finishing standards, ideally in a real walkthrough.</p>
   <p class=warn>Show completed-project footage before renders of the new development, and keep completed-project features apart from the specifications of the project on offer.</p></div>
  <div class=card><h4>8. Use past performance carefully</h4><p>Compare original purchase prices, verified resale prices, documented rental performance, comparable market prices, and service charges and other ownership costs. Show Oxford 212's appreciation with actual verified transactions, not an unsupported percentage.</p>
   <p class=warn>Past performance does not guarantee future returns.</p></div>
 </div>
 {quote("We don't want you to rely only on future projections. We want you to examine what has already been delivered and how selected IMAN properties have performed.")}

 <h3 class=sh>9. The presentation order for Japanese clients</h3>
 <ol class=steps>{''.join(f'<li><span class=sn>{i+1}</span>{e(t)}</li>' for i, t in enumerate(steps))}</ol>
 <p class=sm style="margin-top:5px">Japanese investors value clarity, accuracy and verifiable information. Avoid exaggerated claims, aggressive closing and unsupported promises; give a clean pack with floor plans, specifications, verified prices and legal documents. <b>Build confidence through evidence, transparency and consistency.</b></p>

 <div class=cols>
  <div><h3 class=sh>10. Next: the Dubai Science Park project</h3>
   <div class=dsp><img src="{src('img/dsp-teaser.jpg')}"><ul class=facts>
    <li><b>About 170 homes</b>Studios, 1 and 2 BR</li><li><b>B + G + 10</b>Boutique scale</li>
    <li><b>End of Nov 2026</b>Expected launch</li><li><b>Q3 2029</b>Expected handover</li></ul></div>
   <p class=warn>Confirm specifications, prices, payment plans, inventory and discounts from the latest official release. Use its small scale to explain IMAN's philosophy, not to imply guaranteed scarcity-driven appreciation.</p>
   <h3 class=sh>Recommended closing</h3>
   <p class=sm>After presenting the track record and value, ask:</p>
   {quote("Based on what you've seen, would you prefer a studio focused on rental income at Dubai Science Park, or a larger apartment at 113 Residences that balances rental demand with future resale?")}
   <p class=sm>Use the answer to choose the unit type, then present verified availability, the official payment plan and the full purchase costs. Guide the investor to a suitable choice; don't push for an immediate booking.</p></div>
  <div><h3 class=sh>The pitch: what brokers tell clients</h3>
   <div class=pitch><p>"Let me explain why IMAN Developers is worth considering for your investment in Dubai.</p>
    <p>IMAN is not a developer focused on building thousands of apartments. It's a boutique developer that believes in quality over quantity: premium design, practical layouts, elegant lobbies, high-quality finishes and exceptional amenities at competitive entry prices.</p>
    <p>What makes IMAN particularly interesting is its proven delivery record. It has handed over nine projects, so you can evaluate real buildings rather than rely on future promises.</p>
    <p>When you buy an IMAN property, you're investing in a thoughtfully designed residential environment, from the entrance lobby to the apartment and the amenities. And we want you to compare the actual quality and value against similar properties in Dubai.</p>
    <p>Affordable luxury. Quality over quantity. A complete lifestyle experience."</p></div></div>
 </div>

 <div class=final><div><span class=eb>Final message for brokers</span><h2>Don't sell IMAN as the cheapest developer.</h2>
  <p class=formula><b>Premium quality</b> + <b>lifestyle amenities</b> + <b>thoughtful design</b> + <b>competitive entry price</b> + <b>delivered track record</b></p>
  <p>This is the foundation of IMAN Developers' affordable luxury positioning.</p></div>
  <div class=qrs><figure><img src="{qr('https://wa.me/' + WA)}"><figcaption>WhatsApp Sam</figcaption></figure><figure><img src="{qr(FINDER)}"><figcaption>Unit finder</figcaption></figure></div></div>
 {foot(2)}</section>"""

CSS_EN = """
body{font-family:Figtree,sans-serif}
h1{font-family:Marcellus,serif;font-weight:400;font-size:21pt;line-height:1.15;white-space:normal}
.final h2{font-family:Marcellus,serif;font-weight:400;font-size:13pt}
.eb{letter-spacing:.08em;text-transform:uppercase}
"""


def main():
    at = os.path.join(REPO, "availability", "tools")
    doc = f"""<!doctype html><html lang=en><head><meta charset=utf-8><style>
@font-face{{font-family:Marcellus;src:url(file://{at}/marcellus.woff2) format('woff2')}}
@font-face{{font-family:Figtree;src:url(file://{at}/figtree.woff2) format('woff2');font-weight:300 900}}
{CSS}{CSS_EN}</style></head><body>{p1}{p2}</body></html>"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = os.path.join(os.path.dirname(OUT), "_strategy_en.html")
    open(tmp, "w").write(doc)
    with sync_playwright() as pw:
        exe = "/opt/pw-browsers/chromium"
        b = pw.chromium.launch(**({"executable_path": exe} if os.path.exists(exe) else {}))
        pg = b.new_page()
        pg.goto("file://" + tmp)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        over = pg.evaluate("[...document.querySelectorAll('.page')].map(p=>{const f=p.querySelector('.foot').getBoundingClientRect().top;return Math.max(...[...p.children].filter(c=>!c.classList.contains('foot')).map(c=>c.getBoundingClientRect().bottom))-f})")
        print("space above footer (px, negative = fits):", [round(o) for o in over])
        pg.pdf(path=OUT, format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    os.remove(tmp)
    print("wrote", os.path.relpath(OUT, REPO))


if __name__ == "__main__":
    main()
