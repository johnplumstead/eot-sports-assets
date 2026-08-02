#!/usr/bin/env python3
"""Generate mascot art prompts for every school lacking art, in priority order.

Style target: match the existing 34 -- stylized esports/sports-logo mascot heads,
bold outline, dramatic cel shading, isolated so rembg can cut them cleanly.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sc = json.load(open(f'{ROOT}/data/schools.json'))

PRIMARY = {
 "#C8102E":"red","#CE1126":"red","#9E1B32":"crimson","#A6192E":"crimson","#7A0019":"maroon",
 "#800000":"maroon","#6C1D45":"maroon","#6F263D":"burgundy","#782F40":"garnet",
 "#0C2340":"navy","#002147":"navy","#13294B":"navy","#002855":"navy","#002B5C":"navy",
 "#001F5B":"navy","#181C33":"navy","#002D72":"navy","#0033A0":"royal blue","#003087":"blue",
 "#003DA5":"blue","#00539B":"blue","#0057B8":"royal blue","#005EB8":"blue","#1D4ED8":"royal blue",
 "#00693E":"green","#006747":"green","#007A33":"kelly green","#154734":"forest green",
 "#1A5632":"dark green","#00492B":"dark green","#355E3B":"hunter green","#14532D":"forest green",
 "#1A1A1A":"black","#3F7686":"teal","#008080":"teal","#582C83":"purple","#4B2E83":"purple",
 "#6B21A8":"purple","#F47B20":"orange","#E87722":"orange","#FF6A13":"orange","#BF5700":"burnt orange",
 "#F26522":"orange","#2D2E6F":"deep blue",
}
ACCENT = {
 "#FFC72C":"gold","#FFB81C":"gold","#C5B358":"vegas gold","#CEB888":"old gold","#D3C577":"vegas gold",
 "#C0C6CC":"silver","#C8CDD1":"silver","#E8ECF2":"white","#E6F0EA":"white","#EFE3E7":"white",
 "#F0DADD":"white","#7BAFD4":"columbia blue","#6CACE4":"columbia blue","#9FD0DE":"pale blue",
 "#F98A2E":"orange","#FF8A3D":"orange","#FF8200":"orange","#FF5A5A":"bright red","#6FCF97":"mint green",
 "#00C264":"kelly green","#8FBCEC":"light blue",
}

# Mascots where a literal reading gives a bad prompt.
# Native-American-themed names deliberately resolve to an OBJECT emblem
# (spear, arrowhead, tomahawk) rather than a depiction of a person.
SUBJECT = {
 "Indians": "crossed spears and feather emblem",
 "Seminoles": "spear and feather emblem",
 "Braves": "tomahawk and feather emblem",
 "Yellow Jackets": "yellow jacket wasp",
 "Storm": "storm cloud crackling with lightning",
 "Patriots": "tricorn hat over crossed cavalry sabers",
 "Packers": "razorback hog",
 "Barons": "heraldic crowned lion crest",
 "Crusaders": "crusader helm over a shield",
 "Green Devils": "grinning devil face with horns",
 "Red Devils": "grinning devil face with horns",
 "Royals": "lion wearing a crown",
 "Spongers": "vintage brass sponge-diving helmet",
 "Tornadoes": "tornado funnel",
 "Hurricanes": "spiraling hurricane with a lightning core",
 "Highlanders": "highlander warrior in a tam o'shanter",
 "Spartans": "spartan war helmet",
 "Kings": "ornate crown",
 "Blazers": "roaring flame",
 "Flame": "roaring flame",
 "Thunder": "forked lightning bolt",
 "Lightning": "forked lightning bolt",
 "Senators": "roman senator bust in profile with laurel wreath",
 "Commodores": "naval officer cap over a ship anchor",
 "Marauders": "masked raider in a hood",
 "Conquerors": "conquistador helmet",
 "Dreadnaughts": "armored battleship prow",
 "Hustlers": "bold shield crest with crossed footballs",
 "Green Wave": "cresting ocean wave",
 "Buffalo": "american bison",
 "Bruins": "grizzly bear",
 "Goats": "mountain goat",
 "Gryphons": "gryphon",
 "Royal Knights": "knight helm with a plume",
 "Knights": "knight helm with a plume",
 "Raiders": "horned raider helmet",
 "Vikings": "horned viking helmet",
 "Warriors": "armored warrior helmet",
}

NO_STRIP = {"Storm", "Thunder", "Lightning", "Flame", "Buffalo", "Green Wave", "Dreadnaughts"}


def singular(m):
    if m in NO_STRIP:
        return m.lower()
    if m.endswith('ies'):
        return m[:-3].lower() + 'y'
    if m.endswith('s') and not m.endswith('ss'):
        return m[:-1].lower()
    return m.lower()


def subject(mascot):
    return SUBJECT.get(mascot, singular(mascot))


rows = [(k, v) for k, v in sc.items() if not v.get('art')]

out = ["# Mascot art prompt pack", "",
 f"{len(rows)} schools need art, in priority order (most games first).",
 "The first 26 are the schools that appear 3 or more times in the 2026-27",
 "schedule. They unlock the most games per unit of effort, so stop there if",
 "you only want to do one batch.", "",
 "## How to use", "",
 "1. Generate each image around 1024x1024, one mascot per image.",
 "2. Save as `<key>.png` using the key in each heading.",
 "3. Hand the folder back to me. I run background removal and wire them into",
 "   `data/schools.json` automatically. You do not need to edit anything.", "",
 "## Style rules that matter", "",
 "- Plain flat WHITE background, nothing else in frame. Background removal fails",
 "  on gradients, ground shadows, or busy scenes.",
 "- Head-and-shoulders crop, three-quarter angle, filling most of the frame.",
 "- No text, letters, numbers, banners or ribbons.",
 "- **Original design. Do not imitate any professional, college or existing team",
 "  logo.** The current Carrollwood Day art is literally the New England Patriots",
 "  logo and has to be replaced. Do not repeat that mistake.",
 "- Native-American-themed names (Indians, Seminoles, Braves) are drawn as",
 "  object emblems, spears and tomahawks, never as depictions of people.", "",
 "---", ""]

for i, (k, v) in enumerate(rows, 1):
    c = PRIMARY.get(v.get('primary', '').upper(), v.get('primary', ''))
    a = ACCENT.get(v['ink'].upper(), v['ink'])
    conf = v.get('confidence', '')
    warn = ""
    if conf == 'UNKNOWN':
        warn = "  \n> **Colors unverified.** Placeholder palette. Confirm before this card goes public."
    elif conf == 'low':
        warn = "  \n> Colors are low confidence. Worth a sanity check."
    out.append(f"### {i}. {v['name']} {v['mascot']}  `{k}`")
    out.append(f"*{v['city'].replace('-',' ').title()}  |  {c} and {a}*{warn}")
    out.append("")
    out.append("```")
    out.append(f"Stylized esports-style sports mascot logo of a {subject(v['mascot'])}, "
               f"three-quarter view, bold and confident. Thick outline, dramatic cel shading, "
               f"high contrast, vector illustration style. Color scheme: {c} and {a}. "
               f"Centered, filling the frame, isolated on a plain flat white background. "
               f"No text, no lettering, no background elements. Original design, not based on "
               f"any existing professional or college team logo.")
    out.append("```")
    out.append("")

open(f'{ROOT}/MASCOT_PROMPTS.md', 'w').write("\n".join(out))
print(f"{len(rows)} prompts -> MASCOT_PROMPTS.md")
