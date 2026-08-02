/* MaxPreps schedule scraper.
 *
 * MaxPreps is NOT reachable from the Cowork sandbox (returns 000). Run this
 * through Claude in Chrome instead: open any MaxPreps school schedule page,
 * then paste this into javascript_tool. Same-origin fetch does the rest.
 *
 * Gotchas this code already handles, learned the hard way:
 *   - The date cell renders as "8/147:30pm" with no separator, so a naive
 *     /\d+\/\d+/ grabs "8/147". Strip the known date prefix first.
 *   - The real date comes from the game URL (/M-D-YYYY/), not the cell text.
 *   - Opponent names in cell text carry a leading logo letter ("NNewsome").
 *     Use the opponent's school URL slug instead of the visible text.
 *   - Prefix matching school names collides: "plant" matches "plant-city".
 *     Pin ambiguous slugs in OVERRIDE.
 *   - javascript_tool truncates output near 1000 chars. Dump in chunks.
 */
const E = (window.__EOT = window.__EOT || {});
E.schoolRe = /^\/fl\/[^\/]+\/[^\/]+\/football\/$/;
E.seen = new Map();
E.sched = {};

E.OVERRIDE = { plant: '/fl/tampa/plant-panthers/football/' };

E.fetchSched = async function (schoolUrl) {
  const url = schoolUrl.replace(/\/$/, '') + '/schedule/';
  const html = await (await fetch(url, { credentials: 'omit' })).text();
  const doc = new DOMParser().parseFromString(html, 'text/html');
  const rows = [...doc.querySelectorAll('tr')].filter(r => r.querySelector('a[href*="/football/"]'));
  const games = [];
  for (const r of rows) {
    const cells = [...r.querySelectorAll('td,th')].map(c => c.textContent.replace(/\s+/g, ' ').trim());
    const hrefs = [...r.querySelectorAll('a')].map(a => a.getAttribute('href') || '');
    const oppUrl = hrefs.find(h => E.schoolRe.test(h)) || null;
    const gameUrl = hrefs.find(h => /\/fl\/football\/game\//.test(h)) || '';
    const dm = gameUrl.match(/\/(\d{1,2})-(\d{1,2})-(\d{4})\//);
    if (!dm || !oppUrl) continue;

    const datePrefix = `${+dm[1]}/${+dm[2]}`;
    let c0 = cells[0] || '';
    if (c0.startsWith(datePrefix)) c0 = c0.slice(datePrefix.length);
    const tm = c0.match(/(\d{1,2}):(\d{2})\s*([ap])m/i);
    let hr = tm ? +tm[1] : null;
    if (hr !== null && hr > 12) hr = +String(tm[1]).slice(-1);

    games.push({
      date: `${+dm[1]}/${+dm[2]}/${dm[3]}`,
      time: tm ? `${hr}:${tm[2]}${tm[3].toLowerCase()}m` : '',
      ha: /^\s*vs/i.test(cells[1] || '') ? 'H' : /^\s*@/.test(cells[1] || '') ? 'A' : '?',
      oppSlug: oppUrl.split('/')[3],
    });
    E.seen.set(oppUrl, (cells[1] || '').replace(/^\s*(vs|@)\s*/i, ''));
  }
  E.sched[schoolUrl] = games;
  return games.length;
};

E.crawl = async function (urls) {
  const res = [];
  for (const u of urls) {
    if (E.sched[u]) { res.push([u, 'cached']); continue; }
    try { res.push([u, await E.fetchSched(u)]); }
    catch (e) { res.push([u, 'ERR:' + e.message.slice(0, 30)]); }
    await new Promise(r => setTimeout(r, 250));
  }
  return res;
};

/* Usage:
 *   1. E.want = [...34 slugs from data/schools.json...]
 *   2. Seed-crawl one school, then BFS over E.seen until all 34 resolve.
 *      Private and out-of-county schools will not appear via BFS; probe their
 *      URLs directly as /fl/<city>/<slug>-<mascot>/football/.
 *   3. Apply E.OVERRIDE, build slug->url map, dedupe games by date+home+away.
 *   4. Keep only games where BOTH teams are in the 34 (both mascots exist).
 *   5. Dump in <=35 row chunks and paste into data/schedule.json.
 *
 * Aug 2026 run: 344 games across 34 schools, 12 game dates Aug 14 to Oct 30.
 * Only 73 had both teams in the art library. 96 distinct opponents missing.
 */
