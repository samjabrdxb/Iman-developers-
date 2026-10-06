# Iman-developers-

Sam Jabr's IMAN Developers portfolio page: projects, prices and available units, in English and Arabic.

## Files

- `site/inventory.json`: all projects and available units. Prices are the original prices from IMAN's daily inventory lists.
- `site/sam-jabr.tpl.html`: page layout, styles, text and logic.
- `site/build.py`: puts the inventory into the page and writes `site/index.html` and `site/sam-jabr.html`.
- `site/img/`, `site/assets/`: photos, project images and floor plans.

## Daily update

1. Update the units in `site/inventory.json` from the new inventory lists, and set `inventoryDate`.
2. Run `python3 site/build.py`.
3. Publish `site/sam-jabr.html` with its images, and commit.

## Availability lists and offers

`availability/` keeps every inventory list IMAN sends, one folder per date (`availability/YYYY-MM-DD/`), and `availability/OFFERS.md` holds the current offers and payment plans.

To make the PDF for partners, put the day's IMAN lists in `availability/YYYY-MM-DD/`, update the offers in `availability/tools/make_offers_pdf.py`, and run `python3 availability/tools/make_offers_pdf.py YYYY-MM-DD`. The first page shows Sam's photo, name, title (Senior Sales Manager, OG Team) and WhatsApp number, and every page carries his name and number at the foot.

## Rules from Sam

- A unit that is missing from the newest IMAN list for its project is sold: remove it from `site/inventory.json` and from the PDF.
