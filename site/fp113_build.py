"""Build the 113 Residences floor-plan page (site/fp113.html) from site/fp113.json and site/inventory.json.

Units on IMAN's newest 113 list are available (with list price and view); every other unit shows as sold.
Publish site/fp113.html with the images in site/assets/fp113/ as its own artifact. The same page, as a full
HTML document, goes to site/sam-jabr-113/index.html for GitHub Pages: https://samjabrdxb.github.io/Iman-developers-/sam-jabr-113/
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
page = tpl.replace("/*DATA*/", json.dumps(data, separators=(",", ":")))
open(os.path.join(HERE, "fp113.html"), "w").write(page)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="description" content="113 Residences by IMAN, Al Sufouh: live availability floor by floor, with Sam Jabr, Senior Sales Manager.">\n'
        '<meta property="og:title" content="113 Residences · Live availability · Sam Jabr">\n'
        '<style>[hidden]{display:none!important}</style>\n</head>\n<body>\n')
os.makedirs(os.path.join(HERE, "sam-jabr-113"), exist_ok=True)
open(os.path.join(HERE, "sam-jabr-113", "index.html"), "w").write(head + page.replace("assets/fp113/", "../assets/fp113/") + "\n</body>\n</html>\n")
print("fp113:", len(known), "units,", len(avail), "available")
