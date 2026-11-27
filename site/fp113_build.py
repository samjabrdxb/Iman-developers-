"""Build the 113 Residences floor-plan page (site/fp113.html) from site/fp113.json and site/inventory.json.

Units on IMAN's newest 113 list are available (with list price and view); every other unit shows as sold.
Publish site/fp113.html with the images in site/assets/fp113/ as its own artifact.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
fp = json.load(open(os.path.join(HERE, "fp113.json")))
inv = json.load(open(os.path.join(HERE, "inventory.json")))
p = next(x for x in inv["projects"] if x["id"] == "113-residences")
known = {u["no"] for f in fp["floors"] for u in f["units"]}
avail = {u["no"]: dict(op=u["op"], view=u["view"]) for u in p["units"]}
assert set(avail) <= known, set(avail) - known
data = dict(floors=fp["floors"], avail=avail, date=inv["inventoryDate"])
tpl = open(os.path.join(HERE, "fp113.tpl.html")).read()
assert tpl.count("/*DATA*/") == 1
open(os.path.join(HERE, "fp113.html"), "w").write(tpl.replace("/*DATA*/", json.dumps(data, separators=(",", ":"))))
print("fp113:", len(known), "units,", len(avail), "available")
