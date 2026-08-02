// Build render rows from schedule.json + schools.json
// usage: node scripts/build_rows.js <week> [--final]
const fs=require('fs');
const R=__dirname+'/..';
const sc=JSON.parse(fs.readFileSync(R+'/data/schools.json','utf8'));
const sched=JSON.parse(fs.readFileSync(R+'/data/schedule.json','utf8'));
const week=+process.argv[2], final=process.argv.includes('--final');
const SPON={SPONSOR_PIC:'assets/sponsors/plumstead_headshot.png',SPONSOR_BY:'BROUGHT TO YOU BY',
 SPONSOR_NAME:'TEAM PLUMSTEAD',SPONSOR_ROLE:'REAL ESTATE',SPONSOR_PHONE:'813.495.2136',
 SPONSOR_WEB:'TeamPlumstead.com',SPONSOR_LOGO:'assets/sponsors/red_sash_logo.png'};
const CALL=["TAG YOUR PLAYER OF THE GAME","WHO WAS YOUR PLAYER OF THE GAME?",
 "TAG SOMEONE WHO WAS IN THE STANDS","GOT PHOTOS FROM TONIGHT? DROP THEM BELOW",
 "SHARE THIS IF YOU WERE THERE"];
const SKIP=new Set(['the','of','at','for','and']);
function initials(name){
  const w=name.replace(/[^A-Za-z' ]/g,'').split(/\s+/)
    .filter(x=>x && !SKIP.has(x.toLowerCase()) && x.replace(/'/g,'').length>1);
  return w.slice(0,2).map(x=>x[0].toUpperCase()).join('') || name[0].toUpperCase();
}
// A school with mascot art gets the art. Everything else gets a typographic crest,
// so every game on the schedule is renderable, not just the 34 with art.
function artSlot(s){
  if(s.art && s.img) return `<img src="${s.img}">`;
  return `<div class="crest" style="--cr:${s.ink}"><span class="sh"></span><b>${initials(s.name)}</b></div>`;
}

// shrink the mascot line when the name is long, so it never crowds the panel edge
function msize(name, base){
  const n=name.length;
  if(n>15) return Math.round(base*0.68)+'px';
  if(n>12) return Math.round(base*0.78)+'px';
  if(n>9)  return Math.round(base*0.90)+'px';
  return base+'px';
}

const rows=sched.filter(g=>g.week===week).map((g,i)=>{
  const a=sc[g.home], b=sc[g.away];
  const r={OUT:`${final?'F':'W'}${week}_${String(i+1).padStart(2,'0')}_${g.home}_vs_${g.away}.png`,
    WEEK:`WEEK ${week}`,EDGE:a.ink,
    A1:a.c1,A2:a.c2,AINK:a.ink,AART:artSlot(a),ASCHOOL:a.name.toUpperCase(),AMASCOT:a.mascot.toUpperCase(),AMS:msize(a.mascot, final?66:74),
    B1:b.c1,B2:b.c2,BINK:b.ink,BART:artSlot(b),BSCHOOL:b.name.toUpperCase(),BMASCOT:b.mascot.toUpperCase(),BMS:msize(b.mascot, final?66:74),
    DATE:g.label,VENUE:`AT ${a.name.toUpperCase()}`,...SPON};
  // the info row is a single flex line; long venue names clip it, so scale to fit
  const infoLen=g.label.length+g.time.length+a.name.length+3;
  r.INFOSZ = infoLen>38 ? '38px' : infoLen>33 ? '44px' : '52px';
  r.INFOGAP = infoLen>33 ? '16px' : '26px';
  if(final){ Object.assign(r,{L2:'FINAL',ASCORE:'',BSCORE:'',ACLS:'win',BCLS:'lose',
    ADIM:'',BDIM:'dim',WINLINE:`${a.name.toUpperCase()} WINS`,CTA:CALL[i%CALL.length]}); }
  else { Object.assign(r,{L1:'WHO WILL',L2:'WIN?',TIME:g.time,
    CTA:'Comment SCHOOL for the free Hillsborough County High School Guide'}); }
  return r;
});
const out=`${R}/data/week${week}${final?'_scores':''}.json`;
fs.writeFileSync(out,JSON.stringify(rows,null,1));
console.log(`${rows.length} rows -> ${out.split('/').pop()}`);
