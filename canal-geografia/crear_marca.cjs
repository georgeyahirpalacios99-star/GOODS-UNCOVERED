// Genera la identidad visual del canal: foto de perfil (800x800), banner (2560x1440) y marca de agua (150x150).
// Uso: node canal-geografia/crear_marca.cjs
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const D = __dirname, FUENTE = path.join(D, '..', 'motor-mapa', 'datos', 'fuentes', 'Montserrat.ttf');
const fondo = 'data:image/jpeg;base64,' + fs.readFileSync(path.join(D, 'fondo', 'preview', 't1.0.jpg')).toString('base64');

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:M;src:url(file://${FUENTE});font-weight:100 900}
body{margin:0;background:#000} canvas{display:block}
</style></head><body><canvas id="c"></canvas><script>
const NAVY='#07121b', ACC='#ffd23f', RED='#d6453d';
const c=document.getElementById('c'), x=c.getContext('2d');
function pin(cx, cy, s, sombra=true){ // alfiler de mapa con un ojo adentro
  x.save(); x.translate(cx, cy); x.scale(s, s);
  if (sombra){ x.shadowColor='rgba(0,0,0,.55)'; x.shadowBlur=40; x.shadowOffsetY=14; }
  x.fillStyle=ACC; x.beginPath(); x.moveTo(0,150); x.bezierCurveTo(-40,90,-120,30,-120,-40); x.arc(0,-40,120,Math.PI,0); x.bezierCurveTo(120,30,40,90,0,150); x.fill();
  x.shadowColor='transparent';
  x.strokeStyle=NAVY; x.lineWidth=12; x.stroke();
  // ojo
  x.fillStyle='#fff'; x.beginPath(); x.ellipse(0,-40,78,60,0,0,Math.PI*2); x.fill(); x.lineWidth=11; x.stroke();
  x.fillStyle=NAVY; x.beginPath(); x.arc(14,-34,34,0,Math.PI*2); x.fill();
  x.fillStyle='#fff'; x.beginPath(); x.arc(2,-48,11,0,Math.PI*2); x.fill();
  x.restore();
}
function curvas(w, h, n, col){ x.save(); x.strokeStyle=col; x.lineWidth=2;
  for(let k=0;k<n;k++){ const cx=(Math.sin(k*12.9898)*43758.5453%1+1)%1*w, cy=(Math.sin(k*78.233)*12345.678%1+1)%1*h;
    for(let r=40;r<260;r+=34){ x.beginPath(); for(let a=0;a<=Math.PI*2+.01;a+=.08){ const rr=r*(1+.18*Math.sin(a*3+k)+.08*Math.sin(a*7+k*2)); const px=cx+Math.cos(a)*rr, py=cy+Math.sin(a)*rr*.8; a?x.lineTo(px,py):x.moveTo(px,py);} x.stroke(); } }
  x.restore(); }
window.perfil=()=>{ c.width=c.height=800;
  const g=x.createRadialGradient(400,380,60,400,400,560); g.addColorStop(0,'#123247'); g.addColorStop(1,NAVY); x.fillStyle=g; x.fillRect(0,0,800,800);
  curvas(800,800,5,'rgba(255,210,63,.10)');
  x.save(); x.setLineDash([18,16]); x.strokeStyle='rgba(255,210,63,.55)'; x.lineWidth=7; x.beginPath(); x.moveTo(70,640); x.quadraticCurveTo(250,520,390,600); x.stroke(); x.restore();
  pin(400,380,1.55); return c.toDataURL('image/png'); };
window.marca=()=>{ c.width=c.height=150; x.clearRect(0,0,150,150); pin(75,62,.36,false); return c.toDataURL('image/png'); };
window.banner=async()=>{ c.width=2560; c.height=1440; const im=new Image(); im.src='${fondo}'; await im.decode();
  x.drawImage(im,0,0,2560,1440);
  const g=x.createLinearGradient(0,0,0,1440); g.addColorStop(0,'rgba(7,18,27,.55)'); g.addColorStop(.5,'rgba(7,18,27,.25)'); g.addColorStop(1,'rgba(7,18,27,.6)'); x.fillStyle=g; x.fillRect(0,0,2560,1440);
  const v=x.createRadialGradient(1280,720,300,1280,720,1500); v.addColorStop(0,'rgba(7,18,27,0)'); v.addColorStop(1,'rgba(7,18,27,.8)'); x.fillStyle=v; x.fillRect(0,0,2560,1440);
  // franja central (zona segura 1546x423)
  x.fillStyle='rgba(7,18,27,.72)'; x.fillRect(0,520,2560,400); x.fillStyle=ACC; x.fillRect(0,516,2560,6); x.fillRect(0,918,2560,6);
  pin(700,705,.95);
  x.textBaseline='alphabetic'; x.fillStyle='#fff'; x.font='900 118px M'; x.letterSpacing='6px'; x.fillText('LO QUE EL MAPA',870,690);
  x.fillStyle=ACC; x.font='900 150px M'; x.fillText('NO DICE',866,835);
  x.fillStyle='#e6edf2'; x.font='600 40px M'; x.letterSpacing='2px'; x.fillText('Mapas que explican por qué el mundo es como es',874,895);
  // ruta punteada decorativa
  x.save(); x.setLineDash([16,14]); x.strokeStyle='rgba(255,210,63,.8)'; x.lineWidth=6; x.beginPath(); x.moveTo(330,1180); x.quadraticCurveTo(900,1020,1500,1130); x.quadraticCurveTo(1950,1210,2250,1060); x.stroke(); x.restore();
  x.fillStyle='rgba(255,255,255,.9)'; x.font='700 34px M'; x.letterSpacing='4px'; x.textAlign='center'; x.fillText('NUEVO VIDEO CADA SEMANA  ·  CON DATOS Y FUENTES',1280,1010);
  return c.toDataURL('image/jpeg',.92); };
</script></body></html>`;

(async () => {
  const b = await chromium.launch(), p = await b.newPage();
  const tmp = path.join(D, '.marca.html'); fs.writeFileSync(tmp, html); await p.goto('file://' + tmp); await p.evaluate(() => Promise.all(['900 40px M', '700 40px M', '600 40px M'].map(f => document.fonts.load(f))));
  const guardar = (url, f) => fs.writeFileSync(path.join(D, f), Buffer.from(url.split(',')[1], 'base64'));
  guardar(await p.evaluate(() => perfil()), 'foto-de-perfil.png');
  guardar(await p.evaluate(() => marca()), 'marca-de-agua.png');
  guardar(await p.evaluate(() => banner()), 'banner.jpg');
  fs.unlinkSync(tmp); await b.close(); console.log('listo: foto-de-perfil.png, banner.jpg, marca-de-agua.png');
})();
