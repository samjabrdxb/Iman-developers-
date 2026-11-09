"""French sales strategy brochure: "le luxe accessible, la qualité avant la quantité".

Usage:  python3 marketing/tools/strategy_fr.py

Writes marketing/japan/iman-sales-strategy-fr.pdf (A4 portrait, 2 pages): the
French twin of the English and Japanese strategy brochures, same layout and numbers.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from japan_brochure import qr, src, e, WA, FINDER, REPO, P
from japan_strategy import CSS, LAUNCHED, DELIVERED, DEC_2026, PIPELINE
from strategy_en import CSS_EN
from playwright.sync_api import sync_playwright

OUT = os.path.join(REPO, "marketing", "japan", "iman-sales-strategy-fr.pdf")


def quote(x):
    return f"<blockquote>{e(x)}</blockquote>"


def foot(n):
    return f"""<div class=foot><span>Sam Jabr · Senior Sales Manager · IMAN Developers · WhatsApp +971 50 175 2771</span><span>{n} / 2</span></div>"""


compare = [("Prix d'entrée", "Le prix réel face aux projets comparables"), ("Plan de l'appartement", "L'usage de l'espace et le plan"),
           ("Hauteur sous plafond", "Les spécifications réelles approuvées"), ("Hall et parties communes", "Le design et la qualité des finitions"),
           ("Équipements", "Qualité, nombre et variété"), ("Nombre de logements", "La densité et le cadre de vie"),
           ("Livraisons du promoteur", "Les projets achevés et livrés"), ("Plan de paiement", "Les échéances et les étapes du chantier"),
           ("Potentiel de revente", "Les transactions passées et les comparables")]

p1 = f"""<section class=page>
 <div class=top><div class=tl><div class=logo>IMAN<small>DEVELOPERS</small></div>
   <div class=eb>Stratégie de vente pour les agents japonais et les investisseurs internationaux</div>
   <h1>Le luxe accessible.<br>La qualité avant la quantité.</h1>
   <p class=tp>Moins de logements. Plus d'équipements. Plus de soin du détail. Des prix d'entrée compétitifs.</p></div>
  <div class=ti style="background-image:url('{src(P['oxford-212']['image'])}')"><span>Oxford 212 · livré</span></div></div>

 <div class=stats><div><b>{LAUNCHED}</b><span>projets lancés</span></div><div><b>{DELIVERED}</b><span>projets livrés</span></div>
  <div><b>+{DEC_2026}</b><span>livraisons prévues en décembre 2026</span></div><div><b>{DELIVERED + DEC_2026}</b><span>projets livrés fin 2026 (prévu)</span></div></div>

 <div class=cols>
  <div><h3 class=sh>1. Vendre la philosophie du promoteur, pas seulement l'appartement</h3>
   <p>IMAN Developers est un promoteur boutique qui privilégie la qualité à la quantité. Au lieu de livrer des milliers de logements, IMAN se concentre sur un petit nombre de résidences soigneusement conçues : un choix attractif pour l'investisseur qui veut un produit haut de gamme sans entrer dans le segment de l'ultra-luxe.</p></div>
  <div><h3 class=sh>2. S'appuyer sur les livraisons pour créer la confiance</h3>
   <p>Pour l'acheteur international, surtout à distance, l'historique de livraison du promoteur est essentiel. Les immeubles livrés permettent de juger les finitions, les parties communes et les équipements réels.</p>
   {quote("Avec IMAN Developers, vous n'investissez pas seulement sur des images de synthèse : vous investissez avec un promoteur dont les projets livrés démontrent son approche de la qualité et du cadre de vie.")}</div>
 </div>

 <h3 class=sh>3. Le luxe accessible : pas une construction bon marché, une expérience haut de gamme à prix compétitif</h3>
 <div class=grid3>
  <div class=card><h4>L'arrivée</h4><ul><li>Des halls d'entrée marquants</li><li>Double hauteur dans certains projets</li><li>Matériaux, couleurs et détails élégants</li><li>Accès et circulations pensés</li></ul></div>
  <div class=card><h4>L'appartement</h4><ul><li>Des plans spacieux et pratiques</li><li>Environ 3,2 m sous plafond dans certains plans</li><li>Finitions et matériaux de qualité</li><li>Architecture intérieure et extérieure moderne</li></ul></div>
  <div class=card><h4>Le cadre de vie</h4><ul><li>Piscines</li><li>Espaces fitness et bien-être</li><li>Espaces de détente et pour la famille</li><li>Équipements en rooftop ; plusieurs espaces dans certains projets</li></ul></div>
 </div>
 {quote("Chez IMAN, le luxe commence dès que l'on entre dans l'immeuble, pas seulement quand on ouvre la porte de l'appartement.")}

 <div class=cols>
  <div><h3 class=sh>4. Faire de la taille boutique un atout</h3>
   <ul class=dots><li>Un cadre de vie plus intime</li><li>Un sentiment d'intimité plus fort</li><li>Une identité architecturale distincte</li><li>Des espaces communs bien répartis</li><li>Une autre façon de vivre que dans les projets très denses</li></ul>
   <p class=sm>Les projets boutique d'IMAN en 2026 (Oxford Cove, 113 Residences et le futur projet de Dubai Science Park) totalisent environ {PIPELINE} logements.</p>
   {quote("IMAN ne cherche pas à maximiser le nombre d'appartements, mais la qualité de l'expérience résidentielle.")}
   <p class=warn>Moins de logements ne garantit pas automatiquement moins de densité, plus d'intimité ou une plus-value. Appuyez ces points sur les plans et les spécifications réels.</p></div>
  <div><h3 class=sh>5. Vendre l'ensemble, pas seulement le prix</h3>
   <p class=sm>Ne mettez pas les remises en avant. Comparez le produit complet avec des projets similaires :</p>
   <table class=t><thead><tr><th>Critère</th><th>Ce que l'agent doit montrer</th></tr></thead><tbody>
   {''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in compare)}</tbody></table>
   {quote("La question n'est pas seulement le prix de l'appartement, mais ce que ce prix vous apporte en qualité, en espace, en cadre de vie et en valeur à long terme.")}</div>
 </div>
 {foot(1)}</section>"""

steps = ["La philosophie boutique d'IMAN", "Les projets livrés et l'historique", "La qualité, les plans et les équipements réels", "La comparaison avec des biens de même prix",
         "Paiements, SPA, séquestre, livraison et achat, sur documents officiels", "Les disponibilités et les questions, avant de parler réservation"]
p2 = f"""<section class=page>
 <div class=grid3>
  <div class=card><h4>6. Les paiements liés au chantier : un gage de transparence</h4><p>Dans certains plans, les échéances suivent le calendrier de construction convenu (à 113 Residences, par exemple, 10 % à 40 % d'avancement). L'acheteur voit le lien entre ses paiements et l'avancement du chantier.</p>
   <p class=warn>Utilisez toujours le dernier plan de paiement officiel. Ne dites pas que toutes les échéances sont liées au chantier, ni que rien n'est dû tant que les travaux n'avancent pas.</p></div>
  <div class=card><h4>7. Prouver la qualité par les projets livrés</h4><p>Le client qui ne peut pas venir à Dubaï a besoin de preuves visuelles. Montrez <b>Oxford 212</b> : façade, entrée et hall, intérieurs, couloirs et ascenseurs, équipements, rooftop et finitions, idéalement en visite vidéo réelle.</p>
   <p class=warn>Montrez le projet livré avant les images du nouveau projet, et distinguez bien ses caractéristiques de celles du projet proposé.</p></div>
  <div class=card><h4>8. Utiliser les performances passées avec prudence</h4><p>Comparez les prix d'achat d'origine, les prix de revente vérifiés, les loyers documentés, les prix du marché, ainsi que les charges et autres coûts de détention. Montrez la plus-value d'Oxford 212 avec des transactions réelles vérifiées, pas un pourcentage non étayé.</p>
   <p class=warn>Les performances passées ne garantissent pas les rendements futurs.</p></div>
 </div>
 {quote("Nous ne voulons pas que vous vous fiiez seulement aux projections : regardez ce qui a déjà été livré et comment certains biens IMAN se sont comportés.")}

 <h3 class=sh>9. L'ordre de présentation pour les clients japonais</h3>
 <ol class=steps>{''.join(f'<li><span class=sn>{i+1}</span>{e(t)}</li>' for i, t in enumerate(steps))}</ol>
 <p class=sm style="margin-top:5px">L'investisseur japonais attend de la clarté, de la précision et des informations vérifiables. Évitez les exagérations, la vente agressive et les promesses sans fondement ; remettez un dossier propre avec plans, spécifications, prix vérifiés et documents juridiques. <b>La confiance se construit par les preuves, la transparence et la cohérence.</b></p>

 <div class=cols>
  <div><h3 class=sh>10. Ensuite : le projet de Dubai Science Park</h3>
   <div class=dsp><img src="{src('img/dsp-teaser.jpg')}"><ul class=facts>
    <li><b>Env. 170 logements</b>Studios, 1 et 2 ch.</li><li><b>S-sol + RDC + 10</b>Taille boutique</li>
    <li><b>Fin nov. 2026</b>Lancement prévu</li><li><b>T3 2029</b>Livraison prévue</li></ul></div>
   <p class=warn>Confirmez spécifications, prix, plans de paiement, disponibilités et remises dans la dernière annonce officielle. Sa petite taille illustre la philosophie d'IMAN ; elle ne garantit pas une plus-value liée à la rareté.</p>
   <h3 class=sh>La conclusion recommandée</h3>
   <p class=sm>Après l'historique et la valeur, demandez :</p>
   {quote("D'après ce que vous avez vu, préférez-vous un studio orienté revenu locatif à Dubai Science Park, ou un appartement plus grand à 113 Residences, entre demande locative et revente future ?")}
   <p class=sm>Choisissez le type de logement selon la réponse, puis présentez les disponibilités vérifiées, le plan de paiement officiel et le coût d'achat complet. Guidez sans pousser à réserver tout de suite.</p></div>
  <div><h3 class=sh>Le discours : ce que l'agent dit au client</h3>
   <div class=pitch><p>« Laissez-moi vous expliquer pourquoi IMAN Developers mérite votre attention pour investir à Dubaï.</p>
    <p>IMAN ne construit pas des milliers d'appartements. C'est un promoteur boutique qui croit à la qualité avant la quantité : un design soigné, des plans pratiques, de beaux halls d'entrée, des finitions de qualité et des équipements remarquables, à des prix d'entrée compétitifs.</p>
    <p>Ce qui le rend intéressant, c'est son historique : neuf projets déjà livrés. Vous jugez sur des immeubles réels, pas sur des promesses.</p>
    <p>Acheter chez IMAN, c'est investir dans un cadre de vie pensé dans son ensemble, du hall à l'appartement et aux équipements. Et nous vous invitons à comparer la qualité et la valeur réelles avec des biens similaires à Dubaï.</p>
    <p>Le luxe accessible. La qualité avant la quantité. Une expérience de vie complète. »</p></div></div>
 </div>

 <div class=final><div><span class=eb>Le message final aux agents</span><h2>Ne vendez pas IMAN comme le promoteur le moins cher.</h2>
  <p class=formula><b>Qualité</b> + <b>équipements</b> + <b>design soigné</b> + <b>prix d'entrée compétitif</b> + <b>livraisons prouvées</b></p>
  <p>C'est le socle du positionnement « luxe accessible » d'IMAN Developers.</p></div>
  <div class=qrs><figure><img src="{qr('https://wa.me/' + WA)}"><figcaption>WhatsApp Sam</figcaption></figure><figure><img src="{qr(FINDER)}"><figcaption>Recherche de logements</figcaption></figure></div></div>
 {foot(2)}</section>"""

# French runs longer than English: slightly smaller body text keeps it on two pages.
CSS_FR = """
body{font-size:8pt}
h1{font-size:19pt}
.cols>div>p{font-size:7.8pt}
.card p,.card li{font-size:7.5pt}
.pitch p{font-size:7.7pt}
"""


def main():
    at = os.path.join(REPO, "availability", "tools")
    doc = f"""<!doctype html><html lang=fr><head><meta charset=utf-8><style>
@font-face{{font-family:Marcellus;src:url(file://{at}/marcellus.woff2) format('woff2')}}
@font-face{{font-family:Figtree;src:url(file://{at}/figtree.woff2) format('woff2');font-weight:300 900}}
{CSS}{CSS_EN}{CSS_FR}</style></head><body>{p1}{p2}</body></html>"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = os.path.join(os.path.dirname(OUT), "_strategy_fr.html")
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
