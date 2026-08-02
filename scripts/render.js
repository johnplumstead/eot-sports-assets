const fs=require('fs'),path=require('path');
const {chromium}=require('/home/claude/eot-sports/node_modules/playwright-core');
const ROOT='/home/claude/eot-sports';
const b64=p=>'data:'+(p.endsWith('woff2')?'font/woff2':'image/png')+';base64,'+fs.readFileSync(p).toString('base64');
const FS=ROOT+'/node_modules/@fontsource';
const FONTS={
 FONT_ANTON:b64(FS+'/anton/files/anton-latin-400-normal.woff2'),
 FONT_BC800I:b64(FS+'/barlow-condensed/files/barlow-condensed-latin-800-italic.woff2'),
 FONT_BC800:b64(FS+'/barlow-condensed/files/barlow-condensed-latin-800-normal.woff2'),
 FONT_BC600:b64(FS+'/barlow-condensed/files/barlow-condensed-latin-600-normal.woff2')};

(async()=>{
 const rows=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
 const tpl=fs.readFileSync(ROOT+'/templates/'+(process.argv[3]||'matchup.html'),'utf8');
 const br=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox','--font-render-hinting=none']});
 const pg=await br.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
 const t0=Date.now();
 for(const r of rows){
  let h=tpl; for(const[k,v]of Object.entries(FONTS))h=h.split(k).join(v);
  for(const[k,v]of Object.entries(r)){
   let val=v;
   if(/IMG|PIC|LOGO/.test(k)&&typeof v==='string'&&!v.startsWith('data:'))val=b64(path.resolve(ROOT,v));
   h=h.split('{{'+k+'}}').join(val);
  }
  await pg.setContent(h,{waitUntil:'load'});
  await pg.evaluate(()=>document.fonts.ready);
  await pg.screenshot({path:ROOT+'/out/'+r.OUT,type:'png'});
  console.log('  '+r.OUT);
 }
 console.log(rows.length+' cards in '+((Date.now()-t0)/1000).toFixed(1)+'s  ('+((Date.now()-t0)/rows.length).toFixed(0)+'ms each)');
 await br.close();
})();
