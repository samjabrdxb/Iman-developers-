# Iman-developers-

Sam Jabr's IMAN Developers portfolio page: projects, prices and available units, in English and Arabic.

## Files

- `site/inventory.json`: all projects and available units. Prices are the original prices from IMAN's daily inventory lists.
- `site/sam-jabr.tpl.html`: page layout, styles, text and logic.
- `site/build.py`: puts the inventory into the page and writes `site/index.html` and `site/sam-jabr.html`.
- `site/img/`, `site/assets/`: photos, project images and floor plans.

- `site/finder.tpl.html`, `site/finder_build.py`: the unit finder for brokers (budget, location, payment plan), published as its own artifact: https://claude.ai/artifact/Eg5NZJCZRwriTRGYLCwTb7. Run `python3 site/finder_build.py` after updating the inventory and publish `site/finder.html` with its images.

- `site/note.txt`: Sam's note of the day. It shows at the top of the unit finder and on the cover of the partner PDF; change it when Sam asks and rebuild both.

## 113 Residences landing page (Yandex Direct and Google Ads)

- `site/landing.tpl.html`, `site/landing_build.py`: landing page about 113 Residences only (five layouts, 2BR to 3BR + maid, with "from" prices; no unit list), built into one folder per language, each with its own privacy policy:
  - `site/ru/`: Russian, for Yandex Direct: https://samjabrdxb.github.io/Iman-developers-/ru/
  - `site/en/`: English, for Google Ads: https://samjabrdxb.github.io/Iman-developers-/en/
  - `site/ar/`: Arabic, for Google Ads: https://samjabrdxb.github.io/Iman-developers-/ar/
- GitHub Pages publishes the `site/` folder on every push to `main` (`.github/workflows/pages.yml`).
- Settings at the top of `site/landing_build.py`: Telegram username, lead e-mail, Web3Forms key, Yandex Metrica counter (114052212) and Google Ads tag and conversion labels (`gads`).
- Conversion events: `lead_form`, `lead_wa_fallback`, `click_whatsapp`, `click_telegram`, `click_email`, `call`, `open_plan`. Each goes to Metrica and, when a label is set in `gads`, to Google Ads.
- Run `python3 site/landing_build.py` after updating the inventory (step 2 of the daily update).

## Daily update

1. Update the units in `site/inventory.json` from the new inventory lists, and set `inventoryDate`.
2. Run `python3 site/build.py` and `python3 site/landing_build.py`.
3. Publish `site/sam-jabr.html` with its images, and commit.

## Availability lists and offers

`availability/` keeps every inventory list IMAN sends, one folder per date (`availability/YYYY-MM-DD/`), and `availability/OFFERS.md` holds the current offers and payment plans.

To make the PDF for partners, put the day's IMAN lists in `availability/YYYY-MM-DD/`, update the offers in `availability/tools/make_offers_pdf.py`, and run `python3 availability/tools/make_offers_pdf.py YYYY-MM-DD`. The PDF is landscape: a cover with Sam's photo, name, title (Senior Sales Manager) and WhatsApp number; an overview of every project's offer; one page per project with a unit table (offer price, each instalment, cash price, broker commission); and one page per unit with its payment schedule and floor plan. Every page carries Sam's name and number at the foot.

## Rules from Sam

- A unit that is missing from the newest IMAN list for its project is sold: remove it from `site/inventory.json` and from the PDF.
- When Sam says a unit is sold before IMAN sends a new list, remove it from `site/inventory.json` and add it to `availability/sold.txt`; the PDF leaves it out everywhere, including the attached IMAN lists (its row is blanked).
