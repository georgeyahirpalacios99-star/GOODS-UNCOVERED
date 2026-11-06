// Miniatura de impacto del video 004 (misma plantilla que Colombia, para que se vea como serie): 3 niveles de texto (blanco · recuadro rojo · palabra gigante amarilla), flecha roja al hueco y caras en shock.
//   node motor-mapa/render.cjs videos-largos/004-brasil-desaparece/miniatura/base --preview 3
//   node videos-largos/004-brasil-desaparece/miniatura/componer.cjs
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const D = __dirname, R = path.join(D, '..', '..', '..');
const b64 = f => fs.readFileSync(f).toString('base64');
const base = 'data:image/jpeg;base64,' + b64(path.join(D, 'base', 'preview', 't3.0.jpg'));
const logo = 'data:image/png;base64,' + b64(path.join(R, 'canal-geografia', 'marca-de-agua.png'));
const VAR = { A: ['¿Y SI MAÑANA', 'DESAPARECE', 'BRASIL?'], B: ['¿QUÉ PASARÍA SI', 'DESAPARECE', 'BRASIL?'] };
const html = `<!doctype html><html><head><meta charset="utf-8"><style>@font-face{font-family:M;src:url(file://${path.join(R, 'motor-mapa/datos/fuentes/Montserrat.ttf')});font-weight:100 900}body{margin:0}</style></head><body><canvas id=c width=1920 height=1080></canvas><script>
const x=document.getElementById('c').getContext('2d');
const ajustar=(t,peso,tam,max)=>{ let s=tam; x.font=peso+' '+s+'px M'; while(x.measureText(t).width>max){ s-=4; x.font=peso+' '+s+'px M'; } return s; };
const contorno=(t,cx,cy,lw,relleno)=>{ x.lineWidth=lw; x.strokeStyle='#000'; x.strokeText(t,cx,cy); x.fillStyle=relleno; x.fillText(t,cx,cy); };
window.pintar=async(l1,l2,l3)=>{ const b=new Image(); b.src='${base}'; await b.decode(); const lg=new Image(); lg.src='${logo}'; await lg.decode();
  x.drawImage(b,0,0);
  // viñeta suave a la derecha para que el texto respire
  const g=x.createLinearGradient(900,0,1920,0); g.addColorStop(0,'rgba(5,20,40,0)'); g.addColorStop(1,'rgba(5,20,40,.55)'); x.fillStyle=g; x.fillRect(900,0,1020,1080);
  x.lineJoin='round'; x.textAlign='center'; x.textBaseline='middle'; const cx=1360, ancho=880;
  ajustar(l1,900,118,ancho); contorno(l1,cx,175,26,'#fff');
  // recuadro rojo con borde negro, levemente girado
  const s2=ajustar(l2,900,150,ancho-90); const w=x.measureText(l2).width+90; x.save(); x.translate(cx,350); x.rotate(-.025);
  x.fillStyle='#000'; x.fillRect(-w/2-14,-s2*.62-14,w+28,s2*1.24+28); x.fillStyle='#e41e1e'; x.fillRect(-w/2,-s2*.62,w,s2*1.24);
  contorno(l2,0,6,18,'#fff'); x.restore();
  // palabra gigante amarilla con sombra dura
  const s3=ajustar(l3,900,230,ancho+40); x.save(); x.translate(cx,585); x.rotate(-.02);
  x.fillStyle='rgba(0,0,0,.55)'; x.fillText(l3,10,14); contorno(l3,0,0,34,'#ffd400'); x.restore();
  // flecha roja gruesa con borde negro hacia el hueco de Brasil
  const flecha=(lw,c)=>{ x.save(); x.strokeStyle=c; x.fillStyle=c; x.lineWidth=lw; x.lineCap='round'; x.beginPath(); x.moveTo(1640,985); x.quadraticCurveTo(1350,1010,1180,820); x.stroke();
    x.translate(1180,820); x.rotate(-2.3); x.beginPath(); x.moveTo(36+lw*.3,0); x.lineTo(-70,-70-lw*.3); x.lineTo(-70,70+lw*.3); x.closePath(); x.fill(); x.restore(); };
  flecha(78,'#000'); flecha(52,'#e41e1e');
  x.drawImage(lg,1780,940,110,110);
  return document.getElementById('c').toDataURL('image/jpeg',.94); };
</script></body></html>`;
(async () => { const t = path.join(D, '.c.html'); fs.writeFileSync(t, html); const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + t); await p.evaluate(() => document.fonts.load('900 100px M'));
  for (const [k, ls] of Object.entries(VAR)) { const u = await p.evaluate(ls => pintar(...ls), ls); fs.writeFileSync(path.join(D, `miniatura-${k}.jpg`), Buffer.from(u.split(',')[1], 'base64')); }
  fs.unlinkSync(t); await b.close(); console.log('listo'); })();
