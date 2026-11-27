"""One-off: make the 113 Residences floor-plan assets from IMAN's per-floor brochure PDFs.

Usage: python3 site/fp113_assets.py <dir>
<dir> holds F<floor>/pNN.png (each brochure page rendered at 16 dpi; page 0 cover, last page the floor
overview, the rest one page per unit) and analysis.json (unit titles, areas and the traced key-plan
outline of each unit, made by comparing each unit page's key plan with the floor's median key plan).
Writes site/assets/fp113/floor-<F>.webp, site/assets/fp113/<unit>.webp and site/fp113.json.
Views were then added to site/fp113.json by hand from the units on past IMAN lists (the brochure has none).
"""
import json, os, re, sys
from PIL import Image
SRC = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "fp113")
os.makedirs(OUT, exist_ok=True)
A = json.load(open(os.path.join(SRC, "analysis.json")))
TYPES = {"1 BEDROOM": "1 Bedroom", "1 BEDROOM WITH STUDY": "1 Bedroom + Study", "2 BEDROOM": "2 Bedroom",
         "2 BEDROOM WITH STUDY": "2 Bedroom + Study", "2 BEDROOM WITH MAID": "2 Bedroom + Maid",
         "3 BEDROOM WITH MAID": "3 Bedroom + Maid", "3 BEDROOM WITH STUDY": "3 Bedroom + Study",
         "4 BEDROOM DUPLEX WITH POOL": "4 Bedroom Duplex + Pool"}
ORDER = ["G"] + [str(i) for i in range(1, 10)]
floors = []
for fl in ORDER:
    v = A[fl]
    Image.open(os.path.join(SRC, f"F{fl}", "base.png")).save(os.path.join(OUT, f"floor-{fl}.webp"), quality=80)
    units = []
    for i, u in enumerate(v["units"], 1):
        no = f"G0{i}" if fl == "G" else f"{fl}{i:02d}"
        t = re.sub(r"\s+", " ", u["title"].upper().replace("IBEDROOM", "1 BEDROOM").replace("BEDROOM", " BEDROOM")).strip()
        m = re.search(r"UNIT\s+(\w+)", t)
        assert not m or m.group(1) == no, (fl, i, t)  # pages run in unit order; duplex pages have no number
        kind = re.sub(r"^UNIT\s+\w+\s*-\s*", "", t).replace("  ", " ").strip()
        kind = re.sub(r"(\d)\s+BEDROOM", r"\1 BEDROOM", kind)
        assert kind in TYPES, (no, kind)
        im = Image.open(os.path.join(SRC, f"F{fl}", u["page"])).convert("RGB")
        W, H = im.size
        plan = im.crop((int(W * .03), int(H * .01), int(W * .97), int(H * .5)))
        plan.thumbnail((1000, 1000))
        plan.save(os.path.join(OUT, f"{no}.webp"), quality=72)
        s, b, tot = u["areas"]
        units.append(dict(no=no, type=TYPES[kind], suite=s, balcony=b, total=tot, poly=max(u["polys"], key=len)))
    floors.append(dict(id=fl, name="Ground Floor" if fl == "G" else f"{fl}{'st' if fl == '1' else 'nd' if fl == '2' else 'rd' if fl == '3' else 'th'} Floor",
                       size=v["size"], units=units))
json.dump(dict(floors=floors), open(os.path.join(HERE, "fp113.json"), "w"), indent=1)
print(sum(len(f["units"]) for f in floors), "units")
