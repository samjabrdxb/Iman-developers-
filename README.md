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
