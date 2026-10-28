// uso: node motor-shorts/render.cjs <carpeta-del-short> [--preview t1,t2,...]
// La carpeta lleva: short.json, imagenes 01.png..NN.png (o .jpg/.webp), voz.mp3 (opcional), musica.mp3 (opcional)
const { chromium } = require('playwright');
const { spawn, spawnSync, execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const dir = path.resolve(args[0] || '.');
const pi = args.indexOf('--preview');
const preview = pi >= 0 ? args[pi + 1].split(',').map(Number) : null;
const spec = JSON.parse(fs.readFileSync(path.join(dir, 'short.json'), 'utf8'));
const segs = [...spec.items, spec.cierre];
const FPS = 30, PALABRAS_POR_SEG = 2.6;

const find = (base, exts) => exts.map(e => path.join(dir, base + e)).find(f => fs.existsSync(f));
const voz = find('voz', ['.mp3', '.wav', '.m4a']);
const musica = find('musica', ['.mp3', '.wav', '.m4a']);
const duracion = f => parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());

function silencios(f) {
  const r = spawnSync('ffmpeg', ['-hide_banner', '-i', f, '-af', 'silencedetect=noise=-35dB:d=0.25', '-f', 'null', '-'], { encoding: 'utf8' });
  const out = []; let st = null;
  for (const l of r.stderr.split('\n')) {
    let m = l.match(/silence_start: (-?[\d.]+)/); if (m) st = Math.max(0, +m[1]);
    m = l.match(/silence_end: ([\d.]+)/); if (m && st !== null) { out.push([st, +m[1]]); st = null; }
  }
  return out;
}

// Un bloque de voz por línea del guion: las pausas entre líneas marcan los cortes
function tiempos() {
  if (!voz) {
    let t = 0;
    return segs.map(s => {
      const d = s.narracion.split(/\s+/).length / PALABRAS_POR_SEG;
      const seg = { start: t, speechStart: t + .15, speechEnd: t + .15 + d, end: t + d + .55 }; t = seg.end; return seg;
    });
  }
  const total = duracion(voz), sil = silencios(voz);
  const lead = sil.length && sil[0][0] <= .05 ? sil[0][1] : 0;
  const tail = sil.length && sil[sil.length - 1][1] >= total - .05 ? sil[sil.length - 1][0] : total;
  const inner = sil.filter(([a, b]) => a > lead + .05 && b < tail - .05);
  if (inner.length < segs.length - 1)
    throw new Error(`La voz tiene ${inner.length + 1} bloques y el guion ${segs.length} líneas. Deja una pausa clara entre cada línea.`);
  const cuts = inner.sort((x, y) => (y[1] - y[0]) - (x[1] - x[0])).slice(0, segs.length - 1).sort((x, y) => x[0] - y[0]);
  return segs.map((s, i) => ({
    start: i === 0 ? 0 : Math.max(cuts[i - 1][0], cuts[i - 1][1] - .12),
    speechStart: i === 0 ? lead : cuts[i - 1][1],
    speechEnd: i === segs.length - 1 ? tail : cuts[i][0],
    end: i === segs.length - 1 ? total + .6 : Math.max(cuts[i][0], cuts[i][1] - .12),
  }));
}

function imagen(s, i) {
  const f = find(s.imagen || String(i + 1).padStart(2, '0'), ['.png', '.jpg', '.jpeg', '.webp']);
  if (!f) { console.log(`  falta imagen ${i + 1}: se usa placeholder`); return null; }
  const mime = { '.png': 'png', '.jpg': 'jpeg', '.jpeg': 'jpeg', '.webp': 'webp' }[path.extname(f).toLowerCase()];
  return `data:image/${mime};base64,${fs.readFileSync(f).toString('base64')}`;
}

(async () => {
  const timing = tiempos(), dur = timing[timing.length - 1].end;
  console.log(`${segs.length} bloques · ${dur.toFixed(1)} s · voz: ${voz ? path.basename(voz) : 'no (tiempos estimados)'} · música: ${musica ? path.basename(musica) : 'no'}`);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(__dirname, 'plantilla.html'));
  await page.evaluate(() => Promise.all(['500 40px Inter', '900 40px Inter'].map(f => document.fonts.load(f))));
  await page.evaluate(([s, t, im]) => init(s, t, im), [spec, timing, segs.map(imagen)]);
  const grab = t => page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', 0.92); }, t)
    .then(u => Buffer.from(u.split(',')[1], 'base64'));

  if (preview) {
    const pd = path.join(dir, 'preview'); fs.mkdirSync(pd, { recursive: true });
    for (const t of preview) fs.writeFileSync(path.join(pd, `t${t.toFixed(1)}.jpg`), await grab(t));
    console.log(`preview en ${pd}`);
  } else {
    const out = path.join(dir, (spec.salida || 'short') + '.mp4'), tmp = out.replace(/\.mp4$/, '.tmp.mp4');
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round(dur * FPS);
    for (let i = 0; i < n; i++) {
      const buf = await grab(i / FPS);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 150 === 0) console.log(`  frame ${i}/${n}`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));

    const a = ['-y', '-v', 'error', '-i', tmp], mix = [], f = []; let k = 1;
    if (voz) { a.push('-i', voz); mix.push(`[${k++}:a]`); }
    if (musica) { a.push('-stream_loop', '-1', '-i', musica); f.push(`[${k++}:a]volume=${spec.volumen_musica ?? 0.12}[m]`); mix.push('[m]'); }
    if (!mix.length) { a.push('-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo'); mix.push(`[${k++}:a]`); }
    f.push(mix.length > 1 ? `${mix.join('')}amix=inputs=${mix.length}:duration=longest:normalize=0[a]` : `${mix[0]}anull[a]`);
    spawnSync('ffmpeg', [...a, '-filter_complex', f.join(';'), '-map', '0:v', '-map', '[a]', '-t', dur.toFixed(2),
      '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], { stdio: 'inherit' });
    fs.unlinkSync(tmp);
    console.log(`listo: ${out}`);
  }
  await browser.close();
})();
