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
const rows=sched.filter(g=>g.week===week).map((g,i)=>{
  const a=sc[g.home], b=sc[g.away];
  const r={OUT:`${final?'F':'W'}${week}_${String(i+1).padStart(2,'0')}_${g.home}_vs_${g.away}.png`,
    WEEK:`WEEK ${week}`,EDGE:a.ink,
    A1:a.c1,A2:a.c2,AINK:a.ink,AIMG:a.img,ASCHOOL:a.name.toUpperCase(),AMASCOT:a.mascot.toUpperCase(),
    B1:b.c1,B2:b.c2,BINK:b.ink,BIMG:b.img,BSCHOOL:b.name.toUpperCase(),BMASCOT:b.mascot.toUpperCase(),
    DATE:g.label,VENUE:`AT ${a.name.toUpperCase()}`,...SPON};
  if(final){ Object.assign(r,{L2:'FINAL',ASCORE:'',BSCORE:'',ACLS:'win',BCLS:'lose',
    ADIM:'',BDIM:'dim',WINLINE:`${a.name.toUpperCase()} WINS`,CTA:CALL[i%CALL.length]}); }
  else { Object.assign(r,{L1:'WHO WILL',L2:'WIN?',TIME:g.time,
    CTA:'Comment SCHOOL for the free Hillsborough County High School Guide'}); }
  return r;
});
const out=`${R}/data/week${week}${final?'_scores':''}.json`;
fs.writeFileSync(out,JSON.stringify(rows,null,1));
console.log(`${rows.length} rows -> ${out.split('/').pop()}`);
