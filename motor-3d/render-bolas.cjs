// Render del motor "bolas" (mundo 3D + bolas-país 2D) a MP4.
//   node motor-3d/render-bolas.cjs <carpeta con escenas.json> [--preview 1,5.5] [--hilos 3]
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const R = path.join(__dirname, '..'), dir = path.resolve(process.argv[2]); const spec = JSON.parse(fs.readFileSync(path.join(dir, 'escenas.json'), 'utf8'));
const opt = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const FPS = spec.fps || 30, N = Math.round(spec.duracion * FPS), HILOS = +(opt('--hilos') || 3), preview = opt('--preview') ? opt('--preview').split(',').map(Number) : null;
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.json': 'application/json', '.svg': 'image/svg+xml' };
const srv = http.createServer((q, s) => { const f = path.join(R, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(R) || !fs.existsSync(f)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(s); });
(async () => { await new Promise(r => srv.listen(0, r)); const url = `http://localhost:${srv.address().port}/motor-3d/bolas.html`;
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pagina = async () => { const p = await b.newPage(); p.on('pageerror', e => console.log('ERROR:', e.message)); await p.goto(url); await p.waitForFunction(() => window.listo, null, { timeout: 60000 }); await p.evaluate(() => Promise.all(['700 40px Fr', '900 40px M'].map(f => document.fonts.load(f)))); await p.evaluate(s => init(s), spec); return p; };
  const grab = async (p, t) => Buffer.from((await p.evaluate(t => render(t), t)).split(',')[1], 'base64');
  if (preview) { const p = await pagina(), pd = path.join(dir, 'preview'); fs.mkdirSync(pd, { recursive: true }); for (const t of preview) { console.time('cuadro ' + t); fs.writeFileSync(path.join(pd, `t${t.toFixed(1)}.jpg`), await grab(p, t)); console.timeEnd('cuadro ' + t); } await b.close(); srv.close(); return; }
  const tmp = opt('--tmp') || fs.mkdtempSync('/tmp/bolas-'); console.log('cuadros en', tmp); // --tmp <carpeta>: retoma un render cortado let hechos = 0; const t0 = Date.now();
  await Promise.all(Array.from({ length: HILOS }, async (_, h) => { const p = await pagina(); for (let i = h; i < N; i += HILOS) { if (fs.existsSync(path.join(tmp, `f${String(i).padStart(5, '0')}.jpg`))) { ++hechos; continue; } fs.writeFileSync(path.join(tmp, `f${String(i).padStart(5, '0')}.jpg`), await grab(p, i / FPS)); if (++hechos % 150 === 0) console.log(`  ${(hechos / FPS).toFixed(0)} / ${spec.duracion.toFixed(0)} s  (${((Date.now() - t0) / 1000).toFixed(0)} s)`); } }));
  await b.close(); srv.close();
  const out = path.join(dir, (spec.salida || 'video') + '.mp4'), args = ['-y', '-v', 'error', '-framerate', String(FPS), '-i', path.join(tmp, 'f%05d.jpg')];
  if (spec.audio) args.push('-i', path.join(dir, spec.audio), '-c:a', 'aac', '-b:a', '192k', '-shortest');
  args.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-maxrate', '10M', '-bufsize', '20M', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out);
  execFileSync('ffmpeg', args); fs.rmSync(tmp, { recursive: true }); console.log('listo:', out); })();
