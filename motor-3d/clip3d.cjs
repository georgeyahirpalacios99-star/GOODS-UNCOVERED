// Clip de prueba 3D (3 s): cámara que entra rápido, bola de fuego volando e impacto con sacudida.
//   node motor-3d/clip3d.cjs B   → bocetos-historia/3d-clip-B.mp4
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const R = path.join(__dirname, '..'), est = process.argv[2] || 'B', W = 720, H = 1280, FPS = 30, DUR = 3.0;
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf' };
const srv = http.createServer((q, s) => { const f = path.join(R, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(R) || !fs.existsSync(f)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(s); });
(async () => { await new Promise(r => srv.listen(0, r)); const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage(); p.on('pageerror', e => console.log('ERROR:', e.message)); await p.goto(`http://localhost:${srv.address().port}/motor-3d/escena.html`); await p.waitForFunction(() => window.listo); await p.evaluate(() => document.fonts.load('900 40px M'));
  const dir = fs.mkdtempSync('/tmp/clip3d-'); const n = Math.round(DUR * FPS); console.time('cuadros');
  for (let i = 0; i < n; i++) { const u = await p.evaluate(([e, w, h, t]) => clip3d(e, w, h, t), [est, W, H, i / FPS]); fs.writeFileSync(path.join(dir, `f${String(i).padStart(4, '0')}.jpg`), Buffer.from(u.split(',')[1], 'base64')); }
  console.timeEnd('cuadros'); await b.close(); srv.close();
  const out = path.join(R, 'bocetos-historia', `3d-clip-${est}.mp4`); execFileSync('ffmpeg', ['-y', '-v', 'error', '-framerate', String(FPS), '-i', path.join(dir, 'f%04d.jpg'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', out]); fs.rmSync(dir, { recursive: true }); console.log('listo:', out); })();
