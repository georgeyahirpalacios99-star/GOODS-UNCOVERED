// Pone texto estilo miniatura (blanco con borde negro + palabra en recuadro), flecha y logo sobre el mapa base.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const D = __dirname, R = path.join(D, '..', '..', '..');
const base = 'data:image/jpeg;base64,' + fs.readFileSync(path.join(D, 'base', 'preview', 't3.0.jpg')).toString('base64');
const logo = 'data:image/png;base64,' + fs.readFileSync(path.join(R, 'canal-geografia', 'marca-de-agua.png')).toString('base64');
const VAR = { D: ['21 PAÍSES', 'BORRADOS', '#d6453d'], E: ['EL MUNDO', 'SIN ESPAÑOL', '#d6453d'], F: ['¿Y AHORA', 'QUÉ?', '#ffd23f'] };
const html = `<!doctype html><html><head><meta charset="utf-8"><style>@font-face{font-family:M;src:url(file://${path.join(R, 'motor-mapa/datos/fuentes/Montserrat.ttf')});font-weight:100 900}body{margin:0}</style></head><body><canvas id=c width=1920 height=1080></canvas><script>
const x=document.getElementById('c').getContext('2d');
window.pintar=async(l1,l2,col)=>{ const b=new Image(); b.src='${base}'; await b.decode(); const lg=new Image(); lg.src='${logo}'; await lg.decode();
  x.drawImage(b,0,0); x.lineJoin='round'; x.textAlign='center'; x.textBaseline='middle';
  const cx=1330;
  x.font='900 170px M'; x.lineWidth=34; x.strokeStyle='#000'; x.strokeText(l1,cx,230); x.fillStyle='#fff'; x.fillText(l1,cx,230);
  let fs2=165; x.font='900 165px M'; while(x.measureText(l2).width>820){fs2-=5; x.font='900 '+fs2+'px M';} const w=x.measureText(l2).width+80; x.save(); x.translate(cx,420); x.rotate(-.03);
  x.fillStyle='#000'; x.fillRect(-w/2-14,-105,w+28,210); x.fillStyle=col; x.fillRect(-w/2,-92,w,184);
  if(col!=='#ffd23f'){ x.lineWidth=20; x.strokeStyle='#000'; x.strokeText(l2,0,8); x.fillStyle='#fff'; } else x.fillStyle='#000'; x.fillText(l2,0,8); x.restore();
  // flecha blanca con borde negro hacia el hueco
  const flecha=(lw,c)=>{ x.save(); x.strokeStyle=c; x.lineWidth=lw; x.lineCap='round'; x.beginPath(); x.moveTo(900,560); x.quadraticCurveTo(720,640,610,520); x.stroke();
    x.translate(610,520); x.rotate(-2.35); x.beginPath(); x.moveTo(0,0); x.lineTo(-62,-38); x.moveTo(0,0); x.lineTo(-62,38); x.stroke(); x.restore(); };
  flecha(46,'#000'); flecha(24,'#fff');
  x.drawImage(lg,40,930,110,110);
  return document.getElementById('c').toDataURL('image/jpeg',.95); };
</script></body></html>`;
(async () => { const t = path.join(D, '.c.html'); fs.writeFileSync(t, html); const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + t); await p.evaluate(() => document.fonts.load('900 100px M'));
  for (const [k, [a, bb, col]] of Object.entries(VAR)) { const u = await p.evaluate(([a, bb, col]) => pintar(a, bb, col), [a, bb, col]); fs.writeFileSync(path.join(D, `grande-${k}.jpg`), Buffer.from(u.split(',')[1], 'base64')); }
  fs.unlinkSync(t); await b.close(); })();
