// Uso: node motor-palitos/render.cjs <carpeta con escena.json> [--preview 1,5] [--desde X] [--hasta Y] [--hilos 3]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const args = process.argv.slice(2), dir = path.resolve(args[0] || '.'), opt = k => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const spec = JSON.parse(fs.readFileSync(path.join(dir, 'escena.json'), 'utf8')), FPS = spec.fps || 30, HILOS = Number(opt('--hilos') || 3);
const preview = opt('--preview') ? opt('--preview').split(',').map(Number) : null, desde = Number(opt('--desde') || 0), hasta = Math.min(Number(opt('--hasta') || 1e9), spec.duracion);
(async () => {
  const b = await chromium.launch();
  const pagina = async () => { const p = await b.newPage({ viewport: { width: 1920, height: 1080 } }); await p.goto('file://' + path.join(__dirname, 'palitos.html'));
    await p.evaluate(() => Promise.all(['700 40px Fredoka', '600 40px Fredoka', '400 40px Fredoka'].map(f => document.fonts.load(f)))); await p.evaluate(s => init(s), spec); return p; };
  const grab = async (p, t) => Buffer.from((await p.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', .92); }, t)).split(',')[1], 'base64');
  if (preview) { const p = await pagina(), pd = path.join(dir, 'preview'); fs.mkdirSync(pd, { recursive: true }); for (const t of preview) fs.writeFileSync(path.join(pd, `t${t.toFixed(1)}.jpg`), await grab(p, t)); console.log('preview en ' + pd); }
  else {
    const pages = await Promise.all(Array.from({ length: HILOS }, pagina)), out = path.join(dir, (spec.salida || 'video') + '.mp4');
    const au = spec.audio ? ['-ss', String(desde), '-i', path.resolve(dir, spec.audio)] : ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo'];
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', ...au, '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round((hasta - desde) * FPS);
    for (let i = 0; i < n; i += HILOS) { const bufs = await Promise.all(pages.map((p, k) => i + k < n ? grab(p, desde + (i + k) / FPS) : null)); for (const x of bufs) if (x && !ff.stdin.write(x)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log('listo: ' + out);
  }
  await b.close();
})();
