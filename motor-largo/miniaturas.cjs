// uso: node motor-largo/miniaturas.cjs <carpeta-del-video>  → miniaturas/miniatura-A.jpg, -B.jpg, -C.jpg
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const dir = path.resolve(process.argv[2]), img = n => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(dir, 'imagenes', n + '.jpg')).toString('base64');
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto('file://' + path.join(dir, 'miniaturas', 'miniaturas.html'));
  await p.evaluate(() => document.fonts.load('900 40px Inter'));
  await p.evaluate(async m => { await load('calle', m.calle); await load('arch', m.arch); await load('rayo', m.rayo); }, { calle: img('calle-inundada'), arch: img('archivo-1998-inundacion'), rayo: img('relampago-ciudad') });
  for (const v of ['A', 'B', 'C']) { const u = await p.evaluate(v => hacer(v), v); fs.writeFileSync(path.join(dir, 'miniaturas', `miniatura-${v}.jpg`), Buffer.from(u.split(',')[1], 'base64')); }
  await b.close(); console.log('listo');
})();
