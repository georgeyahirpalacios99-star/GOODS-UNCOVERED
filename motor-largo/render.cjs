// uso: node motor-largo/render.cjs <carpeta-del-video> [--preview t1,t2,...] [--hasta segundos]
// La carpeta lleva: video.json, imagenes/ (cualquier nombre), voz/voz-01.mp3 … (opcional), musica.mp3 (opcional)
const { chromium } = require('playwright');
const { spawn, spawnSync, execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const dir = path.resolve(args[0] || '.');
const opt = k => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const preview = opt('--preview') ? opt('--preview').split(',').map(Number) : null;
const hasta = opt('--hasta') ? +opt('--hasta') : null, desde = opt('--desde') ? +opt('--desde') : 0;
const spec = JSON.parse(fs.readFileSync(path.join(dir, 'video.json'), 'utf8'));
const FPS = spec.fps || 30, PALABRAS_POR_SEG = 2.5, AIRE = .25;
const tmpDir = path.join(dir, '.tmp'); fs.mkdirSync(tmpDir, { recursive: true });

const duracion = f => parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());
function silencios(f) {
  const r = spawnSync('ffmpeg', ['-hide_banner', '-i', f, '-af', 'silencedetect=noise=-35dB:d=0.3', '-f', 'null', '-'], { encoding: 'utf8' });
  const out = []; let st = null;
  for (const l of r.stderr.split('\n')) {
    let m = l.match(/silence_start: (-?[\d.]+)/); if (m) st = Math.max(0, +m[1]);
    m = l.match(/silence_end: ([\d.]+)/); if (m && st !== null) { out.push([st, +m[1]]); st = null; }
  }
  return out;
}

// Parte el audio de cada bloque en párrafos usando las pausas más largas
function tramosDeVoz() {
  const porBloque = {};
  spec.timeline.forEach(it => { if (it.bloque) (porBloque[it.bloque] ||= []).push(it); });
  const tramos = new Map();
  for (const [b, items] of Object.entries(porBloque)) {
    const f = path.join(dir, 'voz', `voz-${String(b).padStart(2, '0')}.mp3`);
    if (!fs.existsSync(f)) continue;
    const total = duracion(f), sil = silencios(f), n = items.length;
    const lead = sil.length && sil[0][0] <= .05 ? sil[0][1] : 0;
    const tail = sil.length && sil[sil.length - 1][1] >= total - .05 ? sil[sil.length - 1][0] : total;
    const inner = sil.filter(([a, c]) => a > lead + .05 && c < tail - .05 && c - a >= .45);
    if (inner.length < n - 1) throw new Error(`voz-${b}: tiene ${inner.length + 1} párrafos y el guion ${n}. Revisa las pausas entre párrafos.`);
    // Dónde debería terminar cada párrafo según su cantidad de texto; se elige, en orden, la pausa que mejor cuadra
    // (cerca del punto esperado y larga). Las pausas entre frases duran casi lo mismo que las de párrafo.
    const largos = items.map(it => (it.voz || '').length), totalC = largos.reduce((x, y) => x + y, 0);
    let acc = 0; const esperado = largos.slice(0, -1).map(l => { acc += l; return lead + (tail - lead) * acc / totalC; });
    const m = inner.length, J = n - 1, INF = 1e9;
    const costo = (j, c) => { const mid = (inner[c][0] + inner[c][1]) / 2; return ((mid - esperado[j]) / 2.5) ** 2 - 3 * (inner[c][1] - inner[c][0]); };
    const D = Array.from({ length: J }, () => new Array(m).fill(INF)), P = Array.from({ length: J }, () => new Array(m).fill(-1));
    for (let c = 0; c < m; c++) D[0][c] = costo(0, c);
    for (let j = 1; j < J; j++) { let best = INF, bi = -1;
      for (let c = 0; c < m; c++) { if (c > 0 && D[j - 1][c - 1] < best) { best = D[j - 1][c - 1]; bi = c - 1; } if (bi >= 0) { D[j][c] = best + costo(j, c); P[j][c] = bi; } } }
    let c = D[J - 1].indexOf(Math.min(...D[J - 1])); const pick = [];
    for (let j = J - 1; j >= 0; j--) { pick.unshift(c); c = P[j][c]; }
    const cuts = pick.map(i => inner[i]);
    if (process.env.GU_DEBUG) console.log(`voz-${b}:`, cuts.map((x, j) => `${((x[0] + x[1]) / 2).toFixed(1)}~${esperado[j].toFixed(1)}`).join(' '));
    items.forEach((it, i) => tramos.set(it, { f, a: i ? cuts[i - 1][1] : lead, b: i < n - 1 ? cuts[i][0] : tail }));
  }
  return tramos;
}

const norm = x => x.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
function construirLinea(tramos) {
  const escenas = [], audio = [], caps = [{ n: 0, ini: 0, titulo: null }]; let t = 0, k = 0, bloque = 1;
  for (const it of spec.timeline) {
    let d, hi = t + AIRE, hd;
    if (it.tarjeta) d = it.dur || 3.2;
    else if (it.bloque) {
      const tr = tramos.get(it);
      if (tr) { d = tr.b - tr.a + 2 * AIRE; }
      else d = (it.voz || '').split(/\s+/).length / PALABRAS_POR_SEG + 2 * AIRE;
      hd = d - 2 * AIRE;
      if (it.bloque !== bloque) { bloque = it.bloque; const ti = (spec.capitulos || {})[bloque];
        if (ti) { const dc = spec.dur_capitulo || 2.8; caps.push({ n: caps.length, ini: t, titulo: ti });
          escenas.push({ tipo: 'capitulo', n: caps.length - 1, titulo: ti, _i: k++, ini: t, fin: t + dc, capas: [] }); t += dc; hi = t + AIRE; } }
      if (tr) audio.push({ t: t + AIRE, ...tr });
    } else d = it.dur || 3;
    const lista = it.tarjeta ? [{ tipo: 'tarjeta', texto: it.tarjeta, tam: it.tam, glitch: it.glitch }] : it.escenas;
    const pesoTotal = lista.reduce((s, e) => s + (e.peso || 1), 0); let u = t; const propias = [];
    lista.forEach(e => { const dd = d * (e.peso || 1) / pesoTotal, esc = { ...e, _i: k++, ini: u, fin: u + dd, capas: [] }; propias.push([esc, e.capas || []]); escenas.push(esc); u += dd; });
    // cada capa aparece cuando la voz dice su palabra clave y se pega a la escena que está en pantalla en ese momento
    propias.forEach(([esc, capas]) => capas.forEach(c => {
      let tc = esc.ini + (c.en ?? .35);
      if (c.clave && it.voz && hd) { const pos = norm(it.voz).indexOf(norm(c.clave)); if (pos >= 0) tc = hi + hd * pos / it.voz.length; }
      tc = Math.min(Math.max(tc, t), t + d - .8);
      const lst = propias.map(p => p[0]); let dueña = lst.find(x => tc >= x.ini && tc < x.fin) || esc;
      const sig = lst[lst.indexOf(dueña) + 1]; if (sig && dueña.fin - tc < 1.2) { dueña = sig; tc = sig.ini + .1; } // no dejar una palabra pegada a un corte
      const resta = dueña.fin - tc, fija = ['sello', 'fuente', 'suscribete'].includes(c.tipo);
      dueña.capas.push({ ...c, _t: tc, _d: Math.max(.8, fija ? resta : Math.min(c.dur || 2.4, resta)) });
    }));
    t += d;
  }
  if (spec.pantalla_final) { escenas.push({ tipo: 'final', _i: k++, ini: t, fin: t + spec.pantalla_final, capas: [] }); t += spec.pantalla_final; }
  // transiciones: en el gancho cortes rápidos (barrido / destello); después, variadas
  const finGancho = caps[1] ? caps[1].ini : 0;
  escenas.forEach((e, i) => { if (e.trans) return;
    e.trans = e.ini < finGancho ? ['barrido', 'destello'][i % 2] : ['fundido', 'zoom', 'fundido', 'luz', 'barrido', 'fundido'][i % 6]; });
  return { escenas, audio, total: t, caps };
}

// ---------- efectos de sonido (sintetizados, sin derechos) ----------
function sfx() {
  const d = path.join(tmpDir, 'sfx'); fs.mkdirSync(d, { recursive: true });
  const gen = (n, src) => { const f = path.join(d, n + '.wav'); if (!fs.existsSync(f)) spawnSync('ffmpeg', ['-y', '-v', 'error', '-f', 'lavfi', '-i', src, '-ar', '48000', '-ac', '1', f]); return f; };
  return {
    whoosh: gen('whoosh', "anoisesrc=d=0.7:c=pink:a=0.6,highpass=f=400,lowpass=f=4000,afade=t=in:d=0.4,afade=t=out:st=0.4:d=0.3"),
    suave: gen('suave', "anoisesrc=d=0.5:c=pink:a=0.32,highpass=f=600,lowpass=f=5000,afade=t=in:d=0.3,afade=t=out:st=0.3:d=0.2"),
    golpe: gen('golpe', "aevalsrc='0.9*sin(2*PI*(70-45*t)*t)*exp(-5*t)+0.25*(random(0)-0.5)*exp(-30*t)':s=48000:d=0.9"),
    pop: gen('pop', "aevalsrc='0.5*sin(2*PI*(900-600*t)*t)*exp(-25*t)':s=48000:d=0.18"),
    glitch: gen('glitch', "anoisesrc=d=0.3:c=white:a=0.5,acrusher=bits=3:mode=log,afade=t=out:st=0.15:d=0.15"),
    tic: gen('tic', "aevalsrc='0.35*sin(2*PI*1800*t)*exp(-90*t)':s=48000:d=0.06"),
    subida: gen('subida', "anoisesrc=d=1.6:c=white:a=0.3,highpass=f=1200,afade=t=in:d=1.55:curve=exp[n];aevalsrc='0.3*sin(2*PI*(150+260*t)*t)*(t/1.6)^2':s=48000:d=1.6[w];[n][w]amix=inputs=2:normalize=0,afade=t=out:st=1.5:d=0.1[out0]"),
    trueno: gen('trueno', "anoisesrc=d=3.5:c=brown:a=1,lowpass=f=220,afade=t=in:d=0.05,afade=t=out:st=0.3:d=3.2:curve=exp,volume=2.5"),
  };
}
// Dos pistas de efectos para que no se pisen: principal (golpes, subidas, truenos) y secundaria (pops, tics, whoosh suaves)
function eventosDeSonido(escenas, caps) {
  const A = [], B = [];
  escenas.forEach(e => {
    if (['tarjeta', 'marca', 'capitulo'].includes(e.tipo)) A.push([e.ini, 'whoosh']);
    if (e.tipo === 'capitulo') B.push([e.ini + .45, 'golpe']);
    if (e.tipo === 'tarjeta' && (e.glitch || /¿/.test(e.texto || ''))) A.push([e.ini - 1.6, 'subida']);
    if (e.glitch) B.push([e.ini, 'glitch']);
    if (e.imagen === 'relampago-ciudad') A.push([e.ini + .25, 'trueno']);
    if (e.tipo === 'cifra') { const n = (e.items || [e]).length, seg = (e.fin - e.ini) / n; for (let j = 0; j < n; j++) A.push([e.ini + j * seg + .05, 'golpe']); }
    if (['barras', 'linea', 'esquema', 'calendario', 'tablero', 'perfil', 'costa'].includes(e.tipo)) B.push([e.ini + .3, 'pop']);
    if (['barrido', 'zoom'].includes(e.trans) && !['tarjeta', 'marca', 'capitulo'].includes(e.tipo)) B.push([e.ini - .15, 'suave']);
    (e.capas || []).forEach(c => c.tipo === 'sello' ? A.push([c._t + .14, 'golpe']) : B.push([c._t, c.tipo === 'fuente' ? 'tic' : 'pop']));
  });
  const ord = x => x.filter(e => e[0] >= 0).sort((a, b) => a[0] - b[0]);
  return [ord(A), ord(B)];
}
// Lluvia ambiente bajo las escenas de lluvia e inundación (ruido filtrado, sin derechos)
function pistaAmbiente(escenas, total) {
  const RE = /lluvia|inundad|agua-puerta|relampago|celular-lluvia|archivo-1998|archivo-bn|banano-inundado/;
  const seg = []; escenas.forEach(e => { if (e.imagen && RE.test(e.imagen)) { const l = seg[seg.length - 1]; if (l && e.ini - l[1] < 1.5) l[1] = e.fin; else seg.push([e.ini, e.fin]); } });
  if (!seg.length) return null;
  const env = seg.map(([a, b]) => `clip((t-${a.toFixed(2)})/0.8,0,1)*clip((${b.toFixed(2)}-t)/0.8,0,1)`).join('+');
  const f = path.join(tmpDir, 'ambiente.wav');
  spawnSync('ffmpeg', ['-y', '-v', 'error', '-f', 'lavfi', '-i', `anoisesrc=c=pink:a=0.5:d=${total.toFixed(2)}`, '-af', `highpass=f=300,lowpass=f=7500,volume='${env}':eval=frame`, '-ar', '48000', '-ac', '1', f]);
  return f;
}
function pistaDeEfectos(ev, total, nombre = 'sfx') {
  const S = sfx(), lista = []; let cur = 0;
  const sil = dd => { const f = path.join(tmpDir, `e${dd.toFixed(3)}.wav`); if (!fs.existsSync(f)) spawnSync('ffmpeg', ['-y', '-v', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', '-t', dd.toFixed(3), f]); return f; };
  const largo = {}; for (const [k, f] of Object.entries(S)) largo[k] = duracion(f);
  for (const [t, k] of ev) { if (t < cur) continue; if (t > cur + .001) lista.push(sil(t - cur)); lista.push(S[k]); cur = t + largo[k]; }
  if (total > cur) lista.push(sil(total - cur));
  const l = path.join(tmpDir, nombre + '.txt'); fs.writeFileSync(l, lista.map(f => `file '${f}'`).join('\n'));
  const out = path.join(tmpDir, nombre + '.wav'); spawnSync('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', l, '-c', 'copy', out]);
  return out;
}

const VIDEOS = {};
function imagenes(escenas) {
  const idir = path.join(dir, 'imagenes'), out = {};
  const files = fs.existsSync(idir) ? fs.readdirSync(idir) : [];
  const nombres = new Set();
  escenas.forEach(e => { if (e.imagen) nombres.add(e.imagen); (e.piezas || []).forEach(p => p.imagen && nombres.add(p.imagen)); });
  const mime = { '.png': 'png', '.jpg': 'jpeg', '.jpeg': 'jpeg', '.webp': 'webp' };
  let faltan = 0;
  for (const n of nombres) {
    const v = files.find(x => path.parse(x).name === n && /\.(mp4|mov|webm)$/i.test(x));
    if (v) { // clip de video (Veo): se pasa a cuadros una sola vez y se lee cuadro por cuadro
      const vd = path.join(tmpDir, 'vid', n); fs.mkdirSync(vd, { recursive: true });
      spawnSync('ffmpeg', ['-v', 'error', '-i', path.join(idir, v), '-vf', `fps=${FPS},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080`, '-q:v', '3', path.join(vd, '%05d.jpg')]);
      VIDEOS[n] = { dir: vd, n: fs.readdirSync(vd).length }; continue;
    }
    const f = files.find(x => path.parse(x).name === n && mime[path.extname(x).toLowerCase()]);
    if (!f) { faltan++; continue; }
    out[n] = `data:image/${mime[path.extname(f).toLowerCase()]};base64,${fs.readFileSync(path.join(idir, f)).toString('base64')}`;
  }
  console.log(`imágenes y videos: ${nombres.size - faltan} de ${nombres.size} (${Object.keys(VIDEOS).length} videos)${faltan ? ` (faltan ${faltan}: se ven como recuadro gris)` : ''}`);
  return out;
}

function pistaDeAudio(audio, total) {
  const sil = d => { const f = path.join(tmpDir, `s${d.toFixed(3)}.wav`); if (!fs.existsSync(f)) spawnSync('ffmpeg', ['-y', '-v', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', '-t', d.toFixed(3), f]); return f; };
  const lista = []; let cur = 0;
  audio.forEach((a, i) => {
    if (a.t > cur + .001) lista.push(sil(a.t - cur));
    const f = path.join(tmpDir, `p${i}.wav`);
    spawnSync('ffmpeg', ['-y', '-v', 'error', '-ss', a.a.toFixed(3), '-to', a.b.toFixed(3), '-i', a.f, '-ar', '48000', '-ac', '1', f]);
    lista.push(f); cur = a.t + (a.b - a.a);
  });
  if (total > cur) lista.push(sil(total - cur));
  const l = path.join(tmpDir, 'lista.txt'); fs.writeFileSync(l, lista.map(f => `file '${f}'`).join('\n'));
  const voz = path.join(tmpDir, 'voz.wav'); spawnSync('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', l, '-c', 'copy', voz]);
  return voz;
}

(async () => {
  const tramos = tramosDeVoz(), { escenas, audio, total, caps } = construirLinea(tramos);
  const dur = hasta ? Math.min(hasta, total) : total;
  if (args.includes('--lista')) { escenas.forEach(e => { console.log(`${e.ini.toFixed(1).padStart(6)}  ${e.tipo.padEnd(10)} ${e.imagen || e.texto || e.titulo || ''}`); (e.capas || []).forEach(c => console.log(`${c._t.toFixed(1).padStart(10)}    + ${c.tipo} ${c.texto || ''}`)); }); caps.forEach(c => console.log(`CAPITULO ${c.ini.toFixed(1)} ${c.titulo || 'inicio'}`)); console.log(`TOTAL ${total.toFixed(1)}`); return; }
  console.log(`${escenas.length} escenas · ${(total / 60).toFixed(1)} min · voz: ${audio.length ? `${audio.length} párrafos` : 'no (tiempos estimados)'}`);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(__dirname, 'plantilla.html'));
  await page.evaluate(() => Promise.all(['500 40px Inter', '600 40px Inter', '700 40px Inter', '800 40px Inter', 'italic 600 40px Inter'].map(f => document.fonts.load(f))));
  await page.evaluate(([e, im, c]) => init(e, im, c), [escenas, imagenes(escenas), caps]);
  const cuadros = t => { // cuadro actual de cada clip visible (escena actual y la anterior durante el cruce)
    const out = {};
    escenas.forEach(e => { const v = VIDEOS[e.imagen]; if (!v || t < e.ini - .01 || t > e.fin + .4) return;
      const i = Math.min(v.n, 1 + Math.floor(Math.max(0, t - e.ini) * FPS) % v.n);
      out[e.imagen] = 'data:image/jpeg;base64,' + fs.readFileSync(path.join(v.dir, String(i).padStart(5, '0') + '.jpg')).toString('base64'); });
    return out;
  };
  const grab = async t => {
    const vf = Object.keys(VIDEOS).length ? cuadros(t) : null;
    if (vf && Object.keys(vf).length) await page.evaluate(m => cuadrosDeVideo(m), vf);
    const u = await page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', 0.9); }, t);
    return Buffer.from(u.split(',')[1], 'base64');
  };

  if (preview) {
    const pd = path.join(dir, 'preview'); fs.mkdirSync(pd, { recursive: true });
    for (const t of preview) fs.writeFileSync(path.join(pd, `t${t.toFixed(1)}.jpg`), await grab(t));
    console.log(`preview en ${pd}`);
  } else {
    const out = path.join(dir, (spec.salida || 'video') + (hasta ? '-muestra' : '') + '.mp4'), tmp = path.join(tmpDir, 'video.mp4');
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', String(spec.crf || 21), '-maxrate', '8M', '-bufsize', '16M', '-preset', 'medium', tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round((dur - desde) * FPS);
    for (let i = 0; i < n; i++) {
      const buf = await grab(desde + i / FPS);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 900 === 0) console.log(`  ${(i / FPS / 60).toFixed(1)} / ${(dur / 60).toFixed(1)} min`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));

    const a = ['-y', '-v', 'error', '-i', tmp], mix = [], f = []; let k = 1;
    if (audio.length) { a.push('-i', pistaDeAudio(audio, total)); mix.push(`[${k++}:a]`); }
    if (spec.efectos !== false) {
      const [A, B] = eventosDeSonido(escenas, caps);
      a.push('-i', pistaDeEfectos(A, total, 'sfx1')); f.push(`[${k++}:a]volume=${spec.volumen_efectos ?? 0.45}[e1]`); mix.push('[e1]');
      a.push('-i', pistaDeEfectos(B, total, 'sfx2')); f.push(`[${k++}:a]volume=${(spec.volumen_efectos ?? 0.45) * .8}[e2]`); mix.push('[e2]');
      const amb = pistaAmbiente(escenas, total); if (amb) { a.push('-i', amb); f.push(`[${k++}:a]volume=${spec.volumen_ambiente ?? 0.14}[am]`); mix.push('[am]'); }
    }
    const mus = ['musica.mp3', 'musica.wav', 'musica.m4a'].map(x => path.join(dir, x)).find(fs.existsSync);
    if (mus) { a.push('-stream_loop', '-1', '-i', mus); f.push(`[${k++}:a]volume=${spec.volumen_musica ?? 0.1}[m]`); mix.push('[m]'); }
    if (!mix.length) { a.push('-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo'); mix.push(`[${k++}:a]`); }
    f.push(mix.length > 1 ? `${mix.join('')}amix=inputs=${mix.length}:duration=first:normalize=0[a]` : `${mix[0]}anull[a]`);
    spawnSync('ffmpeg', [...a, '-filter_complex', f.join(';'), '-map', '0:v', '-map', '[a]', '-t', (dur - desde).toFixed(2),
      '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], { stdio: 'inherit' });
    console.log(`listo: ${out}`);
  }
  await browser.close();
  if (!process.env.GU_KEEP) fs.rmSync(tmpDir, { recursive: true, force: true });
})();
