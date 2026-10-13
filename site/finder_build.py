"""Build the unit finder page for brokers from inventory.json.

Writes site/finder.html (published as its own claude.ai artifact). Only the
projects in FINDER are included: the ones in the daily partner availability.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
inv = json.load(open(os.path.join(HERE, "inventory.json")))

FINDER = {
    "113-residences": dict(name="113 Residences", loc="sufouh", plan="40/60", handover="Q2 2029",
                           schedule=[[20, "Within 30 days of booking", "خلال 30 يوم من الحجز"],
                                     [10, "Within 90 days of booking", "خلال 90 يوم من الحجز"],
                                     [10, "At 40% construction", "عند إنجاز 40% من البناء"],
                                     [60, "On handover", "عند التسليم"]]),
    "oxford-cove": dict(name="Oxford Cove", loc="jvc", plan="50/50", handover=None,
                        schedule=[[50, "In instalments before handover", "أقساط قبل التسليم"],
                                  [50, "On handover", "عند التسليم"]]),
    "sierra-by-iman": dict(name="Sierra by Iman", loc="motorcity", plan="40/60", handover=None,
                           schedule=[[40, "In instalments during construction", "أقساط خلال البناء"],
                                     [60, "On handover", "عند التسليم"]]),
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
note = open(os.path.join(HERE, "note.txt")).read().strip() if os.path.exists(os.path.join(HERE, "note.txt")) else ""
data = dict(note=note, date=inv["inventoryDate"], projects={k: {**v, "image": next(p["image"] for p in inv["projects"] if p["id"] == k)}
                                                 for k, v in FINDER.items()}, units=units)
tpl = open(os.path.join(HERE, "finder.tpl.html")).read()
assert tpl.count("/*DATA*/") == 1
out = tpl.replace("/*DATA*/", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
open(os.path.join(HERE, "finder.html"), "w").write(out)
print("finder:", len(units), "units")
