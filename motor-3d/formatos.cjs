// Maquetas de formatos virales (bolas-país 3D/2D, fusión de banderas, países dentro de Brasil, podio).
//   node motor-3d/formatos.cjs   → bocetos-historia/formatos/*.jpg
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const R = path.join(__dirname, '..'), OUT = path.join(R, 'bocetos-historia', 'formatos');
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.json': 'application/json', '.svg': 'image/svg+xml' };
const srv = http.createServer((q, s) => { const f = path.join(R, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(R) || !fs.existsSync(f)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(s); });
const TAREAS = [
  ['1-fusion-3d', () => fusion3d('ec', 'jp', 'ECUADOR', 'JAPÓN', '¿ECUAPÓN?')],
  ['2-fusion-2d', () => fusion2d('mx', 'co', 'MÉXICO', 'COLOMBIA', '¿MEXIBIA?')],
  ['3-caben-atlas', () => caben('atlas')],
  ['4-caben-neon', () => caben('neon')],
  ['5-podio-3d', () => podio3d([['sr', 'SURINAM', 'shock', '~0,6 M'], ['gy', 'GUYANA', 'normal', '~0,8 M'], ['uy', 'URUGUAY', 'feliz', '~3,4 M']], 'LOS PAÍSES CON MENOS', 'HABITANTES DE SUDAMÉRICA')],
];
(async () => { await new Promise(r => srv.listen(0, r)); fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] }); const p = await b.newPage();
  p.on('pageerror', e => console.log('ERROR:', e.message)); p.on('console', m => m.type() === 'error' && console.log('consola:', m.text()));
  await p.goto(`http://localhost:${srv.address().port}/motor-3d/formatos.html`); await p.waitForFunction(() => window.listo, null, { timeout: 60000 }); await p.evaluate(() => Promise.all(['900 40px M', '800 40px M'].map(f => document.fonts.load(f))));
  const solo = process.argv.slice(2);
  for (const [n, fn] of TAREAS) { if (solo.length && !solo.some(s => n.startsWith(s))) continue; console.time(n); const u = await p.evaluate(fn); fs.writeFileSync(path.join(OUT, n + '.jpg'), Buffer.from(u.split(',')[1], 'base64')); console.timeEnd(n); }
  await b.close(); srv.close(); })();
