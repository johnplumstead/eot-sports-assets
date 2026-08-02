# eot-sports-assets

Card engine for **East of Tampa Local Sports**. Renders 1080x1350 high school football
graphics from HTML templates via headless Chromium.

Throughput: ~700ms per card. 17 cards in 12 seconds. 250 cards in under 3 minutes.

## Layout

```
assets/mascots/      34 transparent mascot PNGs, one per school
assets/sponsors/     sponsor headshot + Red Sash Realty logo
templates/matchup.html    "WHO WILL WIN?" upcoming-game card
templates/final.html      "FINAL" score card
scripts/render.js         node scripts/render.js <rows.json> [template.html]
data/schools.json         34 schools: name, mascot, c1, c2, ink, art path
data/week1.json           example matchup rows
data/week1_scores.json    example score rows
images/                   rendered output, served over raw.githubusercontent.com
```

## Setup

```bash
npm install playwright-core @fontsource/anton @fontsource/barlow-condensed
node scripts/render.js data/week1.json                    # matchup cards
node scripts/render.js data/week1_scores.json final.html  # score cards
```

Chromium in the Cowork sandbox lives at
`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. Do not run `playwright install`.

## Image URLs

```
https://raw.githubusercontent.com/johnplumstead/eot-sports-assets/main/images/week1-finals/<file>.png
```

## Data notes

Colors and mascots researched Aug 2026 from school sites, district pages, Wikipedia and
apparel vendors. Confidence: 21 high, 11 medium, 2 low. Rows needing verification:

- **edgewater** - no such school in the Tampa Bay counties; values are Edgewater HS Orlando
- **s-f-a** - SFA Academy, Dover FL. Mascot Rams confirmed, colors unpublished, placeholder
- **armwood** - blue certain, secondary disputed between gray, black and white
- **carrollwood-day** - mascot art is currently the real New England Patriots logo, replace

Schedule fields in the example data are placeholders pending a MaxPreps pull.
