// Bocetos de estilo para el nuevo formato "historia en escalada" (3 estilos de personajes + una escena de muestra 9:16).
//   node bocetos-historia/bocetos.cjs   → bocetos-historia/estilo-A.jpg, estilo-B.jpg, estilo-C.jpg
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const R = path.join(__dirname, '..'), FU = path.join(R, 'motor-mapa/datos/fuentes');
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:M;src:url(file://${FU}/Montserrat.ttf);font-weight:100 900}
@font-face{font-family:Fr;src:url(file://${FU}/Fredoka.ttf);font-weight:300 700}
body{margin:0;background:#000}</style></head><body><canvas id=c width=1920 height=1080></canvas><script>
const cv=document.getElementById('c'), x=cv.getContext('2d'); const TN='#2a1d14';
const hx=h=>h[0]==='#'?[parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)]:h.match(/[\\d.]+/g).slice(0,3).map(Number);
const sh=(h,k)=>{const [r,g,b]=hx(h);const f=v=>Math.max(0,Math.min(255,Math.round(k>0?v+(255-v)*k:v*(1+k))));return 'rgb('+f(r)+','+f(g)+','+f(b)+')';};
function bola(cx,cy,rx,ry,base,lw){ const g=x.createRadialGradient(cx-rx*.35,cy-ry*.45,Math.min(rx,ry)*.1,cx,cy,Math.max(rx,ry)*1.1); g.addColorStop(0,sh(base,.35)); g.addColorStop(.55,base); g.addColorStop(1,sh(base,-.28));
  x.beginPath(); x.ellipse(cx,cy,rx,ry,0,0,7); x.fillStyle=g; x.fill(); if(lw){x.strokeStyle=TN;x.lineWidth=lw;x.stroke();} }
function rrect(cx,cy,w,h,r,base,lw){ const g=x.createLinearGradient(cx-w/2,cy-h/2,cx+w/2,cy+h/2); g.addColorStop(0,sh(base,.25)); g.addColorStop(.5,base); g.addColorStop(1,sh(base,-.25));
  x.beginPath(); x.roundRect(cx-w/2,cy-h/2,w,h,r); x.fillStyle=g; x.fill(); if(lw){x.strokeStyle=TN;x.lineWidth=lw;x.stroke();} }
function ojos(cx,cy,s,ex,sep){ sep=sep||s*.55;
  for(const k of [-1,1]){ const ox=cx+k*sep;
    if(ex==='risa'){ x.strokeStyle=TN; x.lineWidth=s*.11; x.lineCap='round'; x.beginPath(); x.arc(ox,cy+s*.08,s*.22,Math.PI*1.1,Math.PI*1.9); x.stroke(); continue; }
    const big=ex==='susto'?1.25:1; x.beginPath(); x.ellipse(ox,cy,s*.27*big,s*.33*big,0,0,7); x.fillStyle='#fff'; x.fill(); x.strokeStyle=TN; x.lineWidth=s*.06; x.stroke();
    const pr=ex==='susto'?s*.09:s*.15; x.beginPath(); x.arc(ox+k*s*.02,cy+s*.04,pr,0,7); x.fillStyle=TN; x.fill(); x.beginPath(); x.arc(ox-pr*.35,cy-pr*.2,pr*.38,0,7); x.fillStyle='#fff'; x.fill();
    x.strokeStyle=TN; x.lineWidth=s*.08; x.lineCap='round'; x.beginPath();
    if(ex==='susto'){ x.moveTo(ox-s*.22,cy-s*.55); x.quadraticCurveTo(ox,cy-s*.7,ox+s*.22,cy-s*.55); }
    else if(ex==='enojo'){ x.moveTo(ox-k*s*.25,cy-s*.5); x.lineTo(ox+k*s*.2,cy-s*.38); }
    else { x.moveTo(ox-s*.2,cy-s*.48); x.quadraticCurveTo(ox,cy-s*.56,ox+s*.2,cy-s*.48); } x.stroke(); } }
function boca(cx,cy,s,ex){ x.strokeStyle=TN; x.lineWidth=s*.08; x.lineCap='round';
  if(ex==='susto'){ x.beginPath(); x.ellipse(cx,cy+s*.05,s*.13,s*.18,0,0,7); x.fillStyle='#5a1a1a'; x.fill(); x.stroke(); }
  else if(ex==='risa'){ x.beginPath(); x.moveTo(cx-s*.28,cy-s*.04); x.quadraticCurveTo(cx,cy+s*.42,cx+s*.28,cy-s*.04); x.closePath(); x.fillStyle='#5a1a1a'; x.fill(); x.stroke(); x.save(); x.clip(); x.beginPath(); x.arc(cx,cy+s*.3,s*.14,0,7); x.fillStyle='#e8627a'; x.fill(); x.restore(); }
  else if(ex==='enojo'){ x.beginPath(); x.moveTo(cx-s*.2,cy+s*.06); x.quadraticCurveTo(cx,cy-s*.06,cx+s*.2,cy+s*.06); x.stroke(); }
  else { x.beginPath(); x.moveTo(cx-s*.18,cy); x.quadraticCurveTo(cx,cy+s*.14,cx+s*.18,cy); x.stroke(); } }
function gota(cx,cy,s){ x.beginPath(); x.moveTo(cx,cy-s); x.bezierCurveTo(cx+s*.7,cy-s*.1,cx+s*.6,cy+s*.6,cx,cy+s*.6); x.bezierCurveTo(cx-s*.6,cy+s*.6,cx-s*.7,cy-s*.1,cx,cy-s); x.fillStyle='#8fd8ff'; x.fill(); x.strokeStyle='#2b78b8'; x.lineWidth=s*.12; x.stroke(); }
// ---- tocados ----
function tocado(tipo,cx,top,r,lw){
  if(tipo==='casco'){ const g=x.createLinearGradient(cx-r,0,cx+r,0); g.addColorStop(0,'#c9d1d8'); g.addColorStop(.45,'#8c979f'); g.addColorStop(1,'#4c555c');
    x.beginPath(); x.ellipse(cx,top+r*.42,r*1.25,r*.2,0,0,7); x.fillStyle=g; x.fill(); x.strokeStyle=TN; x.lineWidth=lw; x.stroke();
    x.beginPath(); x.arc(cx,top+r*.42,r*.82,Math.PI,0); x.closePath(); x.fillStyle=g; x.fill(); x.stroke(); x.beginPath(); x.moveTo(cx,top-r*.4); x.lineTo(cx,top+r*.35); x.strokeStyle='rgba(255,255,255,.5)'; x.lineWidth=lw*.8; x.stroke(); }
  if(tipo==='capucha'){ x.beginPath(); x.moveTo(cx-r*1.08,top+r*1.5); x.quadraticCurveTo(cx-r*1.2,top-r*.2,cx,top-r*.55); x.quadraticCurveTo(cx+r*1.3,top-r*.1,cx+r*1.08,top+r*1.5); x.quadraticCurveTo(cx,top+r*.9,cx-r*1.08,top+r*1.5); x.closePath();
    const g=x.createLinearGradient(cx-r,top,cx+r,top+r); g.addColorStop(0,'#5f9a4c'); g.addColorStop(1,'#2e5e2a'); x.fillStyle=g; x.fill(); x.strokeStyle=TN; x.lineWidth=lw; x.stroke(); }
  if(tipo==='gorro'){ rrect(cx,top+r*.12,r*1.7,r*.55,r*.25,'#8a5a32',lw); x.beginPath(); x.ellipse(cx,top+r*.38,r*1.05,r*.14,0,0,7); x.fillStyle='#6b4325'; x.fill(); x.strokeStyle=TN; x.lineWidth=lw; x.stroke(); } }
function capuchaAtras(cx,hy,r,lw){ x.beginPath(); x.moveTo(cx,hy-r*1.6); x.quadraticCurveTo(cx+r*1.45,hy-r*.9,cx+r*1.28,hy+r*.95); x.quadraticCurveTo(cx,hy+r*1.25,cx-r*1.28,hy+r*.95); x.quadraticCurveTo(cx-r*1.45,hy-r*.9,cx,hy-r*1.6); x.closePath(); const g=x.createLinearGradient(cx-r,hy-r,cx+r,hy+r); g.addColorStop(0,'#6aa856'); g.addColorStop(1,'#2e5e2a'); x.fillStyle=g; x.fill(); x.strokeStyle=TN; x.lineWidth=lw; x.stroke(); }
function capuchaFrente(cx,hy,r,lw){ x.beginPath(); x.arc(cx,hy+r*.05,r*1.04,Math.PI*1.08,Math.PI*1.92); x.strokeStyle=TN; x.lineWidth=r*.3; x.lineCap='round'; x.stroke(); x.strokeStyle='#4f8a40'; x.lineWidth=r*.2; x.stroke(); }
function barba(cx,cy,r,lw){ x.beginPath(); x.moveTo(cx-r*.7,cy-r*.15); x.quadraticCurveTo(cx-r*.75,cy+r*.75,cx,cy+r*.95); x.quadraticCurveTo(cx+r*.75,cy+r*.75,cx+r*.7,cy-r*.15); x.quadraticCurveTo(cx,cy+r*.25,cx-r*.7,cy-r*.15); x.fillStyle='#7a4a24'; x.fill(); x.strokeStyle=TN; x.lineWidth=lw; x.stroke(); }
// ---- tres estilos de personaje (x, pies, altura) ----
function frijolito(cx,fy,h,o){ const lw=h*.012, w=h*.5, bh=h*.82, cy=fy-h*.1-bh/2;
  for(const k of [-1,1]){ rrect(cx+k*w*.22,fy-h*.06,w*.2,h*.12,h*.03,o.botas,lw); }
  if(o.tocado==='capucha') capuchaAtras(cx,cy-bh*.2,w*.5,lw);
  x.save(); x.beginPath(); x.ellipse(cx,cy,w/2,bh/2,0,0,7); x.clip(); bola(cx,cy,w/2,bh/2,o.piel); rrect(cx,cy+bh*.25,w*1.2,bh*.55,0,o.ropa); x.fillStyle=o.ribete; x.fillRect(cx-w,cy+bh*.03,w*2,bh*.05); x.restore();
  x.beginPath(); x.ellipse(cx,cy,w/2,bh/2,0,0,7); x.strokeStyle=TN; x.lineWidth=lw*1.3; x.stroke();
  for(const k of [-1,1]){ x.save(); x.translate(cx+k*w*.52,cy+bh*.05); x.rotate(k*(o.brazo||.35)); rrect(0,h*.08,w*.16,h*.2,w*.08,o.ropa,lw); bola(0,h*.19,w*.09,w*.09,o.piel,lw); x.restore(); }
  ojos(cx,cy-bh*.17,h*.12,o.ex); boca(cx,cy-bh*.02,h*.12,o.ex); if(o.barba) barba(cx,cy-bh*.02,h*.13,lw); if(o.tocado==='capucha') capuchaFrente(cx,cy-bh*.2,w*.5,lw); else if(o.tocado) tocado(o.tocado,cx,cy-bh/2+h*.02,w*.42,lw); if(o.ex==='susto') gota(cx+w*.42,cy-bh*.3,h*.04); }
function juguete(cx,fy,h,o){ const lw=h*.012, r=h*.25, hy=fy-h+r, ty=hy+r+h*.13;
  for(const k of [-1,1]){ x.strokeStyle=TN; x.lineWidth=h*.065; x.lineCap='round'; x.beginPath(); x.moveTo(cx+k*h*.07,ty+h*.1); x.lineTo(cx+k*h*.08,fy-h*.05); x.stroke(); x.strokeStyle=o.pantalon; x.lineWidth=h*.045; x.stroke(); bola(cx+k*h*.1,fy-h*.03,h*.07,h*.04,o.botas,lw); }
  rrect(cx,ty,h*.32,h*.28,h*.1,o.ropa,lw); x.fillStyle=o.ribete; x.fillRect(cx-h*.16,ty+h*.05,h*.32,h*.035);
  for(const k of [-1,1]){ x.save(); x.translate(cx+k*h*.16,ty-h*.08); x.rotate(k*(o.brazo||.3)); x.strokeStyle=TN; x.lineWidth=h*.07; x.lineCap='round'; x.beginPath(); x.moveTo(0,0); x.lineTo(0,h*.18); x.stroke(); x.strokeStyle=o.ropa; x.lineWidth=h*.05; x.stroke(); bola(0,h*.2,h*.045,h*.045,o.piel,lw); x.restore(); }
  if(o.tocado==='capucha') capuchaAtras(cx,hy,r,lw);
  bola(cx,hy,r,r*.96,o.piel,lw*1.3); x.fillStyle='rgba(255,120,120,.25)'; for(const k of [-1,1]){ x.beginPath(); x.ellipse(cx+k*r*.55,hy+r*.25,r*.16,r*.09,0,0,7); x.fill(); }
  bola(cx,hy+r*.12,r*.1,r*.08,sh(o.piel,-.08)); ojos(cx,hy-r*.1,r*.62,o.ex,r*.36); boca(cx,hy+r*.45,r*.62,o.ex); if(o.barba) barba(cx,hy+r*.45,r*.55,lw); if(o.tocado==='capucha') capuchaFrente(cx,hy,r,lw); else if(o.tocado) tocado(o.tocado,cx,hy-r*.95,r,lw); if(o.ex==='susto') gota(cx+r*.95,hy-r*.4,h*.04); }
function palito(cx,fy,h,o){ const lw=h*.012, r=h*.17, hy=fy-h+r, ty=hy+r+h*.1;
  x.strokeStyle=TN; x.lineCap='round'; x.lineWidth=h*.022; for(const k of [-1,1]){ x.beginPath(); x.moveTo(cx+k*h*.035,ty+h*.08); x.lineTo(cx+k*h*.06,fy-h*.03); x.stroke(); bola(cx+k*h*.08,fy-h*.02,h*.05,h*.025,o.botas,lw); }
  rrect(cx,ty,h*.18,h*.2,h*.06,o.ropa,lw); x.fillStyle=o.ribete; x.fillRect(cx-h*.09,ty+h*.03,h*.18,h*.03);
  for(const k of [-1,1]){ x.save(); x.translate(cx+k*h*.085,ty-h*.06); x.rotate(-k*(o.brazo||.35)); x.strokeStyle=TN; x.lineWidth=h*.02; x.beginPath(); x.moveTo(0,0); x.lineTo(0,h*.2); x.stroke(); bola(0,h*.21,h*.028,h*.028,'#ffffff',lw*.8); x.restore(); }
  if(o.tocado==='capucha') capuchaAtras(cx,hy,r,lw);
  bola(cx,hy,r,r*.98,'#ffffff',lw*1.2); ojos(cx,hy-r*.08,r*.48,o.ex,r*.3); boca(cx,hy+r*.38,r*.5,o.ex); if(o.barba) barba(cx,hy+r*.42,r*.5,lw); if(o.tocado==='capucha') capuchaFrente(cx,hy,r,lw); else if(o.tocado) tocado(o.tocado,cx,hy-r*.95,r,lw); if(o.ex==='susto') gota(cx+r*.95,hy-r*.35,h*.035); }
const DIB={A:frijolito,B:juguete,C:palito};
const PJ={ atacante:{piel:'#f1c59a',ropa:'#c7392f',ribete:'#f2c230',botas:'#4a3020',pantalon:'#6b4a2a',tocado:'casco'},
  defensor:{piel:'#e7b48a',ropa:'#2f5fa8',ribete:'#e8e1cf',botas:'#3a2a1a',pantalon:'#3d3d48',tocado:'capucha'},
  ingeniero:{piel:'#f3cfa8',ropa:'#7a5a3a',ribete:'#c9a46a',botas:'#3a2a1a',pantalon:'#55483a',tocado:'gorro',barba:true} };
// ---- escena de muestra 9:16 (asedio de un castillo) ----
function escena(est, X0, Y0, S){ x.save(); x.translate(X0,Y0); x.scale(S,S); x.beginPath(); x.rect(0,0,1080,1920); x.clip();
  const sk=x.createLinearGradient(0,0,0,1100); sk.addColorStop(0,'#5fb6ef'); sk.addColorStop(1,'#e4f5ff'); x.fillStyle=sk; x.fillRect(0,0,1080,1920);
  const sol=x.createRadialGradient(830,300,10,830,300,300); sol.addColorStop(0,'rgba(255,236,170,.95)'); sol.addColorStop(1,'rgba(255,236,170,0)'); x.fillStyle=sol; x.fillRect(500,0,600,700);
  for(const [cx,cy,s] of [[220,260,1],[640,190,.7],[930,420,.8]]) for(const [dx,dy,r] of [[-60,10,55],[0,-20,70],[65,5,55],[20,25,60]]) bola(cx+dx*s,cy+dy*s,r*s,r*s*.8,'#ffffff');
  x.fillStyle='#8fc07a'; x.beginPath(); x.moveTo(0,860); x.quadraticCurveTo(300,720,600,840); x.quadraticCurveTo(850,760,1080,830); x.lineTo(1080,1100); x.lineTo(0,1100); x.fill();
  // muralla
  const mt=640, mb=1180; for(let fila=0; fila*70<mb-mt; fila++) for(let c=-1; c<12; c++){ const bx=c*120+(fila%2)*60, by=mt+fila*70; const v=((c*7+fila*13)%5)/5; rrect(bx+60,by+35,116,66,8,sh('#b9a991',(v-.5)*.18)); }
  x.strokeStyle=TN; x.lineWidth=5; x.strokeRect(-10,mt,1100,mb-mt);
  for(let c=0;c<9;c++) { rrect(c*135+50,mt-45,90,90,6,'#c4b49a',5); }
  // torre
  rrect(930,560,230,700,10,'#b2a289',6); x.beginPath(); x.moveTo(800,230); x.lineTo(930,40); x.lineTo(1060,230); x.closePath(); const tg=x.createLinearGradient(800,0,1060,0); tg.addColorStop(0,'#e0574a'); tg.addColorStop(1,'#8e2a22'); x.fillStyle=tg; x.fill(); x.strokeStyle=TN; x.lineWidth=6; x.stroke();
  x.strokeStyle=TN; x.lineWidth=5; x.beginPath(); x.moveTo(930,40); x.lineTo(930,-60); x.stroke(); x.fillStyle='#2f5fa8'; x.beginPath(); x.moveTo(930,-60); x.lineTo(1010,-35); x.lineTo(930,-10); x.fill(); x.stroke();
  rrect(930,420,60,110,30,'#2b2420',4);
  // defensor en la muralla con barril de "FUEGO GRIEGO"
  DIB[est](380,mt-6,est==='A'?190:230,Object.assign({},PJ.defensor,{ex:'enojo',brazo:.8}));
  rrect(560,mt-60,120,130,22,'#9a6a3a',5); x.fillStyle='#5a3a1e'; x.fillRect(500,mt-100,120,10); x.fillRect(500,mt-30,120,10);
  x.save(); x.translate(560,mt-62); x.rotate(-.04); rrect(0,0,128,40,6,'#f1e3c2',3); x.font='800 21px M'; x.fillStyle='#8e2a22'; x.textAlign='center'; x.textBaseline='middle'; x.fillText('FUEGO',0,-6); x.font='700 13px M'; x.fillText('GRIEGO',0,12); x.restore();
  // suelo delantero
  const sg=x.createLinearGradient(0,1150,0,1920); sg.addColorStop(0,'#9c7a4d'); sg.addColorStop(1,'#6e5232'); x.fillStyle=sg; x.fillRect(0,1150,1080,800);
  for(let k=0;k<40;k++){ x.fillStyle='rgba(60,40,20,.25)'; x.beginPath(); x.ellipse((k*197)%1080,1200+((k*131)%700),18+(k%5)*6,6+(k%3)*3,0,0,7); x.fill(); }
  // catapulta
  x.save(); x.translate(250,1500); rrect(0,60,360,46,10,'#8a5a32',5); for(const k of [-1,1]) bola(k*150,110,52,52,'#6b4325',5);
  x.save(); x.rotate(-.75); rrect(0,-150,34,330,12,'#a0703f',5); bola(0,-320,62,42,'#6b4325',5); x.restore();
  rrect(-40,-30,40,180,8,'#8a5a32',5); rrect(40,-30,40,180,8,'#8a5a32',5); x.restore();
  // bola de fuego en vuelo
  for(let k=0;k<26;k++){ const u=k/25, px=300+u*420, py=1120-u*420+u*u*60, r=8+u*30; x.fillStyle='rgba(120,110,105,'+(0.18*(1-u))+')'; x.beginPath(); x.arc(px-20,py+10,r*1.4,0,7); x.fill(); x.fillStyle='rgba(255,'+Math.round(120+u*110)+',40,'+(0.15+u*.5)+')'; x.beginPath(); x.arc(px,py,r,0,7); x.fill(); }
  const fb=x.createRadialGradient(720,760,8,720,760,70); fb.addColorStop(0,'#fff6c2'); fb.addColorStop(.45,'#ffb43a'); fb.addColorStop(1,'rgba(230,70,20,0)'); x.fillStyle=fb; x.beginPath(); x.arc(720,760,70,0,7); x.fill(); bola(720,760,30,30,'#3a2a20',4);
  // atacantes
  DIB[est](560,1800,est==='A'?300:380,Object.assign({},PJ.atacante,{ex:'risa',brazo:-.9}));
  DIB[est](830,1860,est==='A'?290:360,Object.assign({},PJ.ingeniero,{ex:'susto',brazo:.5}));
  // subtítulo de una palabra
  x.font='900 112px M'; x.textAlign='center'; x.textBaseline='middle'; x.lineJoin='round'; x.lineWidth=22; x.strokeStyle='#000'; x.strokeText('fuego',540,1250); x.fillStyle='#fff'; x.fillText('fuego',540,1250);
  x.restore(); x.strokeStyle='#fff'; x.lineWidth=4; x.strokeRect(X0,Y0,1080*S,1920*S); }
function tablero(est, nombre, nota){
  x.fillStyle='#14181d'; x.fillRect(0,0,1920,1080);
  escena(est, 40, 20, 1040/1920);
  x.fillStyle='#fff'; x.font='800 54px M'; x.textAlign='left'; x.textBaseline='alphabetic'; x.fillText('ESTILO '+est+' · '+nombre, 690, 95);
  x.fillStyle='#ffd23f'; x.font='600 28px M'; x.fillText(nota, 690, 140);
  const fondo=x.createLinearGradient(0,170,0,820); fondo.addColorStop(0,'#2a3340'); fondo.addColorStop(1,'#1b2129'); x.fillStyle=fondo; x.beginPath(); x.roundRect(680,170,1200,690,24); x.fill();
  x.fillStyle='rgba(255,255,255,.07)'; x.fillRect(680,760,1200,8);
  const H=est==='A'?400:460;
  [['atacante','ATACANTE','normal',880],['defensor','DEFENSOR','enojo',1280],['ingeniero','INGENIERO','risa',1680]].forEach(([k,et,ex,cx])=>{ DIB[est](cx,770,H,Object.assign({},PJ[k],{ex})); x.fillStyle='#cfd6dc'; x.font='700 26px M'; x.textAlign='center'; x.fillText(et,cx,815); });
  x.fillStyle='#fff'; x.font='700 30px M'; x.textAlign='left'; x.fillText('Expresiones:', 690, 925);
  const HH={A:[230,.65],B:[250,.75],C:[300,.83]}[est]; ['normal','susto','enojo','risa'].forEach((ex,i)=>{ const cx=1010+i*240; x.fillStyle='#232b35'; x.beginPath(); x.roundRect(cx-105,880,210,180,20); x.fill(); x.save(); x.beginPath(); x.roundRect(cx-105,880,210,180,20); x.clip(); DIB[est](cx,985+HH[0]*HH[1],HH[0],Object.assign({},PJ.atacante,{ex})); x.fillStyle='rgba(10,14,18,.85)'; x.fillRect(cx-105,1028,210,32); x.restore(); x.fillStyle='#ffd23f'; x.font='700 22px M'; x.textAlign='center'; x.fillText(ex.toUpperCase(),cx,1052); });
  return cv.toDataURL('image/jpeg',.92); }
window.hacer=(est,nombre,nota)=>tablero(est,nombre,nota);
</script></body></html>`;
(async () => { const t = path.join(__dirname, '.b.html'); fs.writeFileSync(t, html); const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + t); await p.evaluate(() => Promise.all(['900 40px M', '800 40px M', '700 40px M', '600 40px M'].map(f => document.fonts.load(f))));
  for (const [e, n, nota] of [['A', 'FRIJOLITOS', 'Cuerpo de una pieza, ojos grandes. Muy reconocible y fácil de animar.'], ['B', 'CABEZONES DE JUGUETE', 'Cabeza grande, cuerpo de muñeco, nariz y mejillas. El más expresivo.'], ['C', 'PALITOS PRO', 'La fórmula del video de referencia, mejorada: ropa, manos y cejas.']]) {
    const u = await p.evaluate(([e, n, nota]) => hacer(e, n, nota), [e, n, nota]); fs.writeFileSync(path.join(__dirname, `estilo-${e}.jpg`), Buffer.from(u.split(',')[1], 'base64')); }
  fs.unlinkSync(t); await b.close(); console.log('listo'); })();
