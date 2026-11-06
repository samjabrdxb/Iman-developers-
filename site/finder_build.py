"""Build the unit finder page for brokers from inventory.json.

Writes site/finder.html (English/Arabic) and site/finder-ja.html (Japanese/English),
each published as its own claude.ai artifact. Only the
projects in FINDER are included: the ones in the daily partner availability.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
inv = json.load(open(os.path.join(HERE, "inventory.json")))

FINDER = {
    "113-residences": dict(name="113 Residences", loc="sufouh", plan="40/60", handover="Q2 2029",
                           mkt="https://drive.google.com/drive/folders/123km8i0fk4-WMbpkqIHhTNS4DhTcpuOZ",
                           schedule=[[20, "Within 30 days of booking", "خلال 30 يوم من الحجز", "予約から30日以内"],
                                     [10, "Within 90 days of booking", "خلال 90 يوم من الحجز", "予約から90日以内"],
                                     [10, "At 40% construction", "عند إنجاز 40% من البناء", "工事進捗40%時"],
                                     [60, "On handover", "عند التسليم", "引き渡し時"]]),
    "oxford-cove": dict(name="Oxford Cove", loc="jvc", plan="50/50", handover=None,
                        schedule=[[50, "In instalments before handover", "أقساط قبل التسليم", "引き渡し前に分割"],
                                  [50, "On handover", "عند التسليم", "引き渡し時"]]),
    "sierra-by-iman": dict(name="Sierra by Iman", loc="motorcity", plan="40/60", handover=None,
                           schedule=[[40, "In instalments during construction", "أقساط خلال البناء", "建設期間中に分割"],
                                     [60, "On handover", "عند التسليم", "引き渡し時"]]),
}

units = []
for p in inv["projects"]:
    f = FINDER.get(p["id"])
    if not f:
        continue
    for u in p["units"]:
        units.append(dict(pid=p["id"], no=u["no"], type=u["type"], floor=u["floor"], view=u["view"],
                          area=u["area"], op=u["op"], disc=u.get("discount", p.get("discount") or 0),
                          cash=u.get("cash", p.get("cash") or 0), img=u.get("planImg")))
read = lambda f: open(os.path.join(HERE, f)).read().strip() if os.path.exists(os.path.join(HERE, f)) else ""
note, note_ja = read("note.txt"), read("note.ja.txt")  # note.ja.txt: the same note in Japanese, for finder-ja.html
featured = []  # site/featured.txt: Sam's best units, by bedroom count
for line in read("featured.txt").splitlines():
    line = line.split("#")[0].strip()
    if ":" in line:
        k, v = line.split(":", 1)
        featured.append(dict(beds=k.strip().split()[0], units=[x.strip() for x in v.split(",") if x.strip()]))
ALL_MKT = "https://drive.google.com/drive/folders/1LbabUTGbian6qUDhNoAPbbHC9Aelw4uq"  # IMAN sales & marketing folder, all projects
data = dict(allMkt=ALL_MKT, featured=featured, note=note, noteJa=note_ja, date=inv["inventoryDate"], projects={k: {**v, "image": next(p["image"] for p in inv["projects"] if p["id"] == k)}
                                                 for k, v in FINDER.items()}, units=units)
tpl = open(os.path.join(HERE, "finder.tpl.html")).read()
assert tpl.count("/*DATA*/") == 1
assert tpl.count("/*LANGS*/") == 1
page = tpl.replace("/*DATA*/", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
# finder.html: English and Arabic. finder-ja.html: Japanese first, then English, for brokers in Japan.
for name, langs, title in [("finder.html", ["en", "ar"], "IMAN Unit Finder"), ("finder-ja.html", ["ja", "en"], "IMAN 住戸検索")]:
    out = page.replace("/*LANGS*/", json.dumps(langs)).replace("<title>IMAN Unit Finder</title>", f"<title>{title}</title>")
    open(os.path.join(HERE, name), "w").write(out)
print("finder:", len(units), "units")
