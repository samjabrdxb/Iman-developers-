"""Build the portfolio page from inventory.json.

Writes two files next to this script:
  sam-jabr.html  page body, published as the claude.ai artifact
  index.html     the same page as a full HTML document, for GitHub Pages
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
inv = json.load(open(os.path.join(HERE, "inventory.json")))
tpl = open(os.path.join(HERE, "sam-jabr.tpl.html")).read()
assert tpl.count("/*INVENTORY*/") == 1
data = json.dumps(inv, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
page = tpl.replace("/*INVENTORY*/", data)

open(os.path.join(HERE, "sam-jabr.html"), "w").write(page)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="description" content="IMAN Developers projects, prices and available units with Sam Jabr, Senior Sales Manager.">\n'
        '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n')
open(os.path.join(HERE, "index.html"), "w").write(head + page + "\n</body>\n</html>\n")
print("built", sum(len(p["units"]) for p in inv["projects"]), "units")
