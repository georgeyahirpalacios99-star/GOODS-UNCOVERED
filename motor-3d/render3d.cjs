// Motor 3D de Goods Uncovered: países como piezas sólidas (bandera arriba, canto, luz y sombras) con cara.
// Uso: node motor-3d/render3d.cjs <carpeta con escena.json> [--preview 1,4.5]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawnSync } = require('child_process');
const dir = path.resolve(process.argv[2]); const args = process.argv.slice(3);
const prev = args.includes('--preview') ? args[args.indexOf('--preview') + 1].split(',').map(Number) : null;
const sc = JSON.parse(fs.readFileSync(path.join(dir, 'escena.json'), 'utf8'));
const DAT = path.join(__dirname, '..', 'motor-mapa', 'datos'), S = 1000;
const proj = (lon, lat) => [(lon + 180) / 360 * S, (1 - Math.log(Math.tan(Math.PI / 4 + lat * Math.PI / 360)) / Math.PI) / 2 * S];
// geometría: solo los países de la escena, simplificada
const geo = JSON.parse(fs.readFileSync(path.join(DAT, 'ne_50m_admin_0_countries.geojson'), 'utf8'));
const quiero = new Set(sc.paises.map(p => p.adm)); const paises = [];
for (const f of geo.features) { const p = f.properties; if (!quiero.has(p.ADM0_A3)) continue;
  const polys = (f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates).map(pg => pg.map(r => { const step = Math.max(1, Math.floor(r.length / 600)); return r.filter((_, i) => i % step === 0).map(([lo, la]) => proj(lo, la)); }));
  const conf = sc.paises.find(q => q.adm === p.ADM0_A3); paises.push({ adm: p.ADM0_A3, iso: conf.iso, lx: p.LABEL_X, ly: p.LABEL_Y, polys, ...conf }); }
const flags = {}; for (const p of sc.paises) { const f = path.join(DAT, 'banderas', p.iso + '.svg'); if (fs.existsSync(f)) flags[p.iso] = 'data:image/svg+xml;base64,' + fs.readFileSync(f).toString('base64'); }
const imgs = {}; for (const c of sc.capas || []) for (const k of ['img']) if (c[k] && !imgs[c[k]]) { const f = path.join(dir, c[k]); if (fs.existsSync(f)) imgs[c[k]] = 'data:image/jpeg;base64,' + fs.readFileSync(f).toString('base64'); else console.warn('falta', c[k]); }
for (const c of sc.capas || []) for (const iso of [c.isoIzq, c.isoDer]) if (iso && !flags[iso]) { const f = path.join(DAT, 'banderas', iso + '.svg'); if (fs.existsSync(f)) flags[iso] = 'data:image/svg+xml;base64,' + fs.readFileSync(f).toString('base64'); }
const fuente = n => 'data:font/woff2;base64,' + fs.readFileSync(path.join(DAT, 'fuentes', n)).toString('base64');
const three = fs.readFileSync(path.join(__dirname, 'node_modules', 'three', 'build', 'three.min.js'), 'utf8');
const W = sc.ancho || 1080, H = sc.alto || 1920, FPS = 30;
const html = `<!doctype html><html><head><style>@font-face{font-family:Anton;src:url(${fuente('Anton.woff2')})}@font-face{font-family:Barlow;font-weight:700;src:url(${fuente('BarlowCondensed-700.woff2')})}
body{margin:0;background:#000}canvas{position:absolute;left:0;top:0}</style></head><body><canvas id="gl" width="${W}" height="${H}"></canvas><canvas id="ov" width="${W}" height="${H}"></canvas><script>${three}</script>
<script src="escena3d.js"></script></body></html>`;
fs.writeFileSync(path.join(__dirname, '.pagina.html'), html);
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  page.on('console', m => { if (m.type() === 'error') console.log('PAGINA:', m.text()); }); page.on('pageerror', e => console.log('ERROR:', e.message));
  await page.goto('file://' + path.join(__dirname, '.pagina.html'));
  await page.evaluate(async ([sc, paises, flags, imgs]) => { await document.fonts.load('80px Anton'); await document.fonts.load('700 40px Barlow'); await iniciar(sc, paises, flags, imgs); }, [sc, paises, flags, imgs]);
  const shot = async t => { await page.evaluate(t => cuadro(t), t); return page.screenshot({ type: 'jpeg', quality: 90 }); };
  if (prev) { const pd = path.join(dir, 'preview'); fs.mkdirSync(pd, { recursive: true }); for (const t of prev) fs.writeFileSync(path.join(pd, `t${t}.jpg`), await shot(t)); console.log('preview en', pd); }
  else {
    const fd = path.join(dir, '.cuadros'); fs.rmSync(fd, { recursive: true, force: true }); fs.mkdirSync(fd, { recursive: true }); const n = Math.round(sc.duracion * FPS);
    for (let i = 0; i < n; i++) { fs.writeFileSync(path.join(fd, String(i + 1).padStart(5, '0') + '.jpg'), await shot(i / FPS)); if (i % 60 === 0) console.log(`${(i / FPS).toFixed(0)} / ${sc.duracion} s`); }
    const out = path.join(dir, (sc.salida || 'escena3d') + '.mp4');
    spawnSync('ffmpeg', ['-y', '-v', 'error', '-framerate', String(FPS), '-i', path.join(fd, '%05d.jpg'), '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: 'inherit' }); console.log('listo:', out);
  }
  await browser.close();
})();
