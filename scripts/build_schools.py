#!/usr/bin/env python3
"""Rebuild data/schools.json as the full county table.

SUPERSEDES the original version of this file, which derived palettes by sampling
the mascot PNGs. That produced muddy browns and is gone on purpose -- colours are
now researched per school. Do not reintroduce colour-sampling.

Keeps the original 34 keys untouched (renders depend on them) and appends every
opponent school found in the 2026-27 schedule crawl.

Colour model: `primary` drives c1 (very dark) and c2 (mid). `ink` is the bright
accent used for the mascot name and panel border, chosen by hand so it always
reads against c2 -- never a dark-on-dark pair.

Idempotent: safe to re-run.
"""
import json, colorsys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# key, name, mascot, city, maxpreps_slug, primary, ink, confidence
NEW = [
 # --- tier 1: appears in 3+ games ---
 ("bloomingdale","Bloomingdale","Bulls","valrico","bloomingdale-bulls","#C8102E","#E8ECF2","high"),
 ("leto","Leto","Falcons","tampa","leto-falcons","#C8102E","#FFC72C","high"),
 ("east-bay","East Bay","Indians","gibsonton","east-bay-indians","#C8102E","#C8CDD1","medium"),
 ("blake","Blake","Yellow Jackets","tampa","blake-yellow-jackets","#1A1A1A","#FFC72C","high"),
 ("steinbrenner","Steinbrenner","Warriors","lutz","steinbrenner-warriors","#0C2340","#FFC72C","high"),
 ("robinson","Robinson","Knights","tampa","robinson-knights","#1A1A1A","#C0C6CC","high"),
 ("st-pete-catholic","St. Petersburg Catholic","Barons","st-petersburg","st-petersburg-catholic-barons","#1A1A1A","#FFC72C","medium"),
 ("morgan","Morgan","Mustangs","wimauma","morgan-the-mustangs","#0C2340","#F98A2E","high"),
 ("chamberlain","Chamberlain","Storm","tampa","chamberlain-storm","#00693E","#FFC72C","high"),
 ("freedom","Freedom","Patriots","tampa","freedom-patriots","#C8102E","#E8ECF2","medium"),
 ("parrish-community","Parrish Community","Bulls","parrish","parrish-community-bulls","#0C2340","#C0C6CC","medium"),
 ("largo","Largo","Packers","largo","largo-packers","#0033A0","#FFC72C","high"),
 ("tampa-catholic","Tampa Catholic","Crusaders","tampa","tampa-catholic-crusaders","#00693E","#E6F0EA","high"),
 ("pinellas-park","Pinellas Park","Patriots","largo","pinellas-park-patriots","#C8102E","#E8ECF2","high"),
 ("st-petersburg","St. Petersburg","Green Devils","st-petersburg","st-petersburg-green-devils","#00693E","#E6F0EA","high"),
 ("sickles","Sickles","Gryphons","tampa","sickles-gryphons","#00693E","#C0C6CC","high"),
 ("palm-harbor","Palm Harbor University","Hurricanes","palm-harbor","palm-harbor-university-hurricanes","#7A0019","#7BAFD4","high"),
 ("land-o-lakes","Land O' Lakes","Gators","land-o-lakes","land-o-lakes-gators","#003087","#FFC72C","high"),
 ("wiregrass-ranch","Wiregrass Ranch","Bulls","wesley-chapel","wiregrass-ranch-bulls","#7A0019","#C0C6CC","high"),
 ("manatee","Manatee","Hurricanes","bradenton","manatee-hurricanes","#C8102E","#E8ECF2","high"),
 ("boca-ciega","Boca Ciega","Pirates","gulfport","boca-ciega-pirates","#002855","#FFC72C","high"),
 ("hollins","Hollins","Royals","st-petersburg","hollins-royals","#00539B","#E8ECF2","medium"),
 ("anclote","Anclote","Sharks","holiday","anclote-sharks","#003087","#C0C6CC","medium"),
 ("tarpon-springs","Tarpon Springs","Spongers","tarpon-springs","tarpon-springs-spongers","#800000","#EFE3E7","high"),
 ("countryside","Countryside","Cougars","clearwater","countryside-cougars","#800000","#FFC72C","medium"),
 ("clearwater","Clearwater","Tornadoes","clearwater","clearwater-tornadoes","#9E1B32","#C0C6CC","high"),
 # --- tier 2: 2 games ---
 ("lake-gibson","Lake Gibson","Braves","lakeland","lake-gibson-braves","#782F40","#CEB888","high"),
 ("east-lake","East Lake","Eagles","tarpon-springs","east-lake-eagles","#0033A0","#C0C6CC","medium"),
 ("calvary-christian","Calvary Christian","Warriors","clearwater","calvary-christian-warriors","#002147","#C0C6CC","high"),
 ("mulberry","Mulberry","Panthers","mulberry","mulberry-panthers","#0033A0","#E8ECF2","high"),
 ("kathleen","Kathleen","Red Devils","lakeland","kathleen-red-devils","#C8102E","#E8ECF2","high"),
 ("wesley-chapel","Wesley Chapel","Wildcats","wesley-chapel","wesley-chapel-wildcats","#001F5B","#E8ECF2","low"),
 ("lake-wales","Lake Wales","Highlanders","lake-wales","lake-wales-highlanders","#1A1A1A","#F98A2E","high"),
 ("lakewood","Lakewood","Spartans","st-petersburg","lakewood-spartans","#1A1A1A","#FFB81C","high"),
 ("southeast","Southeast","Seminoles","bradenton","southeast-seminoles","#0033A0","#F98A2E","high"),
 ("northside-christian","Northside Christian","Mustangs","st-petersburg","northside-christian-mustangs","#003DA5","#E8ECF2","low"),
 ("crystal-river","Crystal River","Pirates","crystal-river","crystal-river-pirates","#003087","#FFC72C","medium"),
 ("swfl-christian","Southwest Florida Christian","Kings","fort-myers","southwest-florida-christian-kings","#0C2340","#FFC72C","UNKNOWN"),
 ("sarasota-christian","Sarasota Christian","Blazers","sarasota","sarasota-christian-blazers","#003087","#FFC72C","medium"),
 ("bishop-mclaughlin","Bishop McLaughlin","Hurricanes","spring-hill","bishop-mclaughlin-catholic-hurricanes","#002147","#E8ECF2","low"),
 # --- tier 3: single game ---
 ("mitchell","Mitchell","Mustangs","new-port-richey","mitchell-mustangs","#002B5C","#FFC72C","medium"),
 ("sunlake","Sunlake","Seahawks","land-o-lakes","sunlake-seahawks","#3F7686","#9FD0DE","medium"),
 ("cypress-creek","Cypress Creek","Coyotes","wesley-chapel","cypress-creek-coyotes","#1A5632","#FFB81C","medium"),
 ("lake-region","Lake Region","Thunder","eagle-lake","lake-region-thunder","#1A1A1A","#C0C6CC","high"),
 ("jones","Jones","Tigers","orlando","jones-tigers","#00693E","#FF8A3D","high"),
 ("palmetto","Palmetto","Tigers","palmetto","palmetto-tigers","#C8102E","#E8ECF2","high"),
 ("fletcher","Fletcher","Senators","neptune-beach","fletcher-senators","#582C83","#E8ECF2","medium"),
 ("cardinal-mooney","Cardinal Mooney","Cougars","sarasota","cardinal-mooney-cougars","#C8102E","#E8ECF2","medium"),
 ("archbishop-carroll","Archbishop Carroll","Bulldogs","miami","archbishop-carroll-bulldogs","#1A1A1A","#7BAFD4","high"),
 ("ccc","Clearwater Central Catholic","Marauders","clearwater","clearwater-central-catholic-marauders","#C8102E","#FFB81C","high"),
 ("bayshore","Bayshore","Bruins","bradenton","bayshore-bruins","#1A1A1A","#FFC72C","medium"),
 ("palm-beach-lakes","Palm Beach Lakes","Rams","west-palm-beach","palm-beach-lakes-rams","#6F263D","#C0C6CC","medium"),
 ("hudson","Hudson","Cobras","hudson","hudson-cobras","#1A1A1A","#C5B358","medium"),
 ("north-port","North Port","Bobcats","north-port","north-port-bobcats","#13294B","#E8ECF2","medium"),
 ("venice","Venice","Indians","venice","venice-indians","#00693E","#E6F0EA","high"),
 ("lehigh","Lehigh","Lightning","lehigh-acres","lehigh-lightning","#13294B","#FFC72C","medium"),
 ("lakewood-ranch","Lakewood Ranch","Mustangs","bradenton","lakewood-ranch-mustangs","#1A5632","#E6F0EA","medium"),
 ("riverview-sarasota","Riverview (Sarasota)","Rams","sarasota","riverview-sarasota-rams","#6C1D45","#EFE3E7","high"),
 ("belen-jesuit","Belen Jesuit","Wolverines","miami","belen-jesuit-wolverines","#002D72","#FFC72C","high"),
 ("eau-gallie","Eau Gallie","Commodores","melbourne","eau-gallie-commodores","#13294B","#FFC72C","high"),
 ("river-ridge","River Ridge","Royal Knights","new-port-richey","river-ridge-royal-knights","#582C83","#C0C6CC","high"),
 ("trinity-christian","Trinity Christian Academy","Conquerors","jacksonville","trinity-christian-academy-conquerors","#0033A0","#E8ECF2","medium"),
 ("csn","Community School of Naples","Seahawks","naples","community-school-of-naples-seahawks","#0C2340","#FFC72C","UNKNOWN"),
 ("cardinal-newman","Cardinal Newman","Crusaders","west-palm-beach","cardinal-newman-crusaders","#003DA5","#FFC72C","high"),
 ("edgewater-orlando","Edgewater","Fighting Eagles","orlando","edgewater-eagles","#C8102E","#E8ECF2","high"),
 ("george-jenkins","George Jenkins","Eagles","lakeland","george-jenkins-eagles","#00693E","#FFC72C","high"),
 ("dunbar","Dunbar","Fighting Tigers","fort-myers","dunbar-fighting-tigers","#00693E","#FF8A3D","high"),
 ("bartow","Bartow","Yellow Jackets","bartow","bartow-yellow-jackets","#005EB8","#FF8200","high"),
 ("indian-rocks-christian","Indian Rocks Christian","Golden Eagles","largo","indian-rocks-christian-eagles","#0033A0","#FF5A5A","medium"),
 ("springstead","Springstead","Eagles","spring-hill","springstead-eagles","#C8102E","#E8ECF2","medium"),
 ("weeki-wachee","Weeki Wachee","Hornets","weeki-wachee","weeki-wachee-hornets","#006747","#6FCF97","high"),
 ("south-sumter","South Sumter","Raiders","bushnell","south-sumter-raiders","#C8102E","#E8ECF2","high"),
 ("citrus","Citrus","Hurricanes","inverness","citrus-hurricanes","#1A1A1A","#C5B358","high"),
 ("central-brooksville","Central","Bears","brooksville","central-bears","#0C2340","#C0C6CC","medium"),
 ("hernando","Hernando","Leopards","brooksville","hernando-leopards","#4B2E83","#FFC72C","high"),
 ("villages-charter","The Villages Charter","Buffalo","the-villages","the-villages-charter-buffalo","#00492B","#6FCF97","low"),
 ("south-marion","South Marion","Bears","ocala","south-marion-bears","#0C2340","#F98A2E","high"),
 ("santa-fe-catholic","Santa Fe Catholic","Crimson Hawks","lakeland","santa-fe-catholic-hawks","#A6192E","#E8ECF2","low"),
 ("father-lopez","Father Lopez","Green Wave","daytona-beach","father-lopez-green-wave","#007A33","#E6F0EA","high"),
 ("bishop-verot","Bishop Verot","Vikings","fort-myers","bishop-verot-vikings","#1A1A1A","#FFC72C","high"),
 ("vanguard","Vanguard","Knights","ocala","vanguard-knights","#C8102E","#E8ECF2","high"),
 ("buchholz","Buchholz","Bobcats","gainesville","buchholz-bobcats","#1A1A1A","#FFC72C","high"),
 ("central-fort-pierce","Fort Pierce Central","Cobras","fort-pierce","central-cobras","#4B2E83","#FFC72C","high"),
 ("lakeland","Lakeland","Dreadnaughts","lakeland","lakeland-dreadnaughts","#1A1A1A","#FF8A3D","medium"),
 ("mcc","Melbourne Central Catholic","Hustlers","melbourne","melbourne-central-catholic-hustlers","#154734","#FFC72C","medium"),
 ("west-oaks","West Oaks Academy","Flame","orlando","west-oaks-academy-flame","#800000","#C5B358","medium"),
 ("out-of-door","Out-of-Door Academy","Thunder","sarasota","out-of-door-academy-thunder","#0033A0","#E8ECF2","medium"),
 ("orangewood-christian","Orangewood Christian","Rams","maitland","orangewood-christian-rams","#C8102E","#FFC72C","low"),
 ("foundation-academy","Foundation Academy","Lions","winter-garden","foundation-academy-lions","#181C33","#C0C6CC","low"),
 ("seffner-christian","Seffner Christian","Crusaders","seffner","seffner-christian-crusaders","#800000","#EFE3E7","high"),
 ("wildwood","Wildwood","Wildcats","wildwood","wildwood-wildcats","#0057B8","#E8ECF2","medium"),
 ("smarten","SmartEn Sports Academy","Goats","miami","smarten-sports-academy-goats","#1A1A1A","#C0C6CC","UNKNOWN"),
 ("taylor","Taylor","Wildcats","pierson","taylor-wildcats","#C8102E","#E8ECF2","high"),
 ("eagles-view","Eagle's View","Warriors","jacksonville","eagles-view-warriors","#355E3B","#6FCF97","medium"),
]

# MaxPreps duplicate slugs that resolve to a school already in the table
ALIASES = {
 "seminole-seminoles": "seminole",   # Pinellas Seminole; legacy slug, mascot is Warhawks
 "sfa-rams": "s-f-a",                # same SFA Academy as specially-fit-academy-rams
}

# MaxPreps slugs for the original 34
MP34 = {
 "riverview":"riverview-sharks","spoto":"spoto-spartans","gaither":"gaither-cowboys",
 "strawberry-crest":"strawberry-crest-chargers","king":"king-lions","durant":"durant-cougars",
 "wharton":"wharton-wildcats","brandon":"brandon-eagles","sumner":"sumner-stingrays",
 "plant":"plant-panthers","berkeley-prep":"berkeley-prep-buccaneers","hillsborough":"hillsborough-terriers",
 "sarasota":"sarasota-sailors","tampa-bay-tech":"tampa-bay-tech-titans","carrollwood-day":"carrollwood-day-patriots",
 "armwood":"armwood-hawks","edgewater":"edgewater-eagles","seminole":"seminole-warhawks",
 "jefferson":"jefferson-dragons","dunedin":"dunedin-falcons","lennard":"lennard-longhorns",
 "osceola":"osceola-warriors","middleton":"middleton-tigers","gibbs":"gibbs-gladiators",
 "newsome":"newsome-wolves","northeast":"northeast-vikings","plant-city":"plant-city-raiders",
 "nature-coast-tech":"nature-coast-tech-sharks","alonso":"alonso-ravens",
 "zephyrhills-christian":"zephyrhills-christian-warriors","jesuit":"jesuit-tigers",
 "s-f-a":"specially-fit-academy-rams","cambridge-christian":"cambridge-christian-lancers",
 "keswick-christian":"keswick-christian-crusaders",
}


def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))


def rgb2hex(r):
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(c*255))) for c in r)


def ramp(primary, light):
    r, g, b = hex2rgb(primary)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.12:                       # near-neutral primary: keep it neutral
        return rgb2hex(colorsys.hls_to_rgb(h, light, s))
    return rgb2hex(colorsys.hls_to_rgb(h, light, min(1.0, s*1.05)))


sc = json.load(open(f'{ROOT}/data/schools.json'))

for slug, mp in MP34.items():
    if slug in sc:
        sc[slug]['maxpreps'] = mp
        sc[slug]['art'] = True

for key, name, mascot, city, mp, prim, ink, conf in NEW:
    existing = sc.get(key, {})
    if existing.get('art'):
        raise SystemExit(f'key collision with an art-bearing school: {key}')
    sc[key] = {
        'name': name, 'mascot': mascot, 'city': city, 'maxpreps': mp,
        'primary': prim, 'c1': ramp(prim, 0.09), 'c2': ramp(prim, 0.26), 'ink': ink,
        'img': None, 'art': False, 'confidence': conf,
    }

json.dump(sc, open(f'{ROOT}/data/schools.json', 'w'), indent=1)
json.dump(ALIASES, open(f'{ROOT}/data/maxpreps_aliases.json', 'w'), indent=1)

have = sum(1 for v in sc.values() if v.get('art'))
unk = [k for k, v in sc.items() if v.get('confidence') == 'UNKNOWN']
low = [k for k, v in sc.items() if v.get('confidence') == 'low']
print(f'schools: {len(sc)}  |  with art: {have}  |  needing art: {len(sc)-have}')
print(f'colors unknown ({len(unk)}): {", ".join(unk)}')
print(f'colors low confidence ({len(low)}): {", ".join(low)}')
