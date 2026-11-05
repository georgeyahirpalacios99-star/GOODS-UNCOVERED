// Motor de mapas Goods Uncovered.
// Uso: node motor-mapa/render.cjs <carpeta con mapa.json> [--preview 1,5.5,12] [--hasta 10] [--hilos 3]
// Estilos: "documental" (relieve satelital, rutas, fotos de archivo) y "caricatura" (países con bandera y ojos).
// Datos: Natural Earth (dominio público) y banderas de flag-icons (licencia MIT), ya descargados en motor-mapa/datos.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');

const args = process.argv.slice(2), dir = path.resolve(args[0] || '.');
const opt = k => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const spec = JSON.parse(fs.readFileSync(path.join(dir, 'mapa.json'), 'utf8'));
const FPS = spec.fps || 30, preview = opt('--preview') ? opt('--preview').split(',').map(Number) : null;
const hasta = opt('--hasta') ? Number(opt('--hasta')) : null, HILOS = Number(opt('--hilos') || 3);
const DAT = path.join(__dirname, 'datos'), S = 1000;

const proj = (lon, lat) => { lat = Math.max(-85, Math.min(85, lat)); return [(lon + 180) / 360 * S, (1 - Math.log(Math.tan(Math.PI / 4 + lat * Math.PI / 360)) / Math.PI) / 2 * S]; };
const r3 = v => Math.round(v * 1000) / 1000;
function anillo(coords) { const out = []; for (const [lo, la] of coords) { const [x, y] = proj(lo, la); out.push(r3(x), r3(y)); } return out; }
function bbox(arr, bb = [1e9, 1e9, -1e9, -1e9]) { for (let i = 0; i < arr.length; i += 2) { bb[0] = Math.min(bb[0], arr[i]); bb[1] = Math.min(bb[1], arr[i + 1]); bb[2] = Math.max(bb[2], arr[i]); bb[3] = Math.max(bb[3], arr[i + 1]); } return bb; }
function area(a) { let s = 0; for (let i = 0; i < a.length - 2; i += 2) s += a[i] * a[i + 3] - a[i + 2] * a[i + 1]; return Math.abs(s / 2); }
const polysDe = g => g.type === 'Polygon' ? [g.coordinates] : g.type === 'MultiPolygon' ? g.coordinates : [];

function paises(archivo) {
  return JSON.parse(fs.readFileSync(path.join(DAT, archivo), 'utf8')).features.map(f => {
    const p = f.properties, iso = (p.ISO_A2 === '-99' ? p.ISO_A2_EH : p.ISO_A2) || '', polys = polysDe(f.geometry).map(pg => { const rings = pg.map(anillo); return { rings, bb: bbox(rings[0]), a: area(rings[0]) }; });
    if (!polys.length) return null; let main = 0; polys.forEach((q, i) => { if (q.a > polys[main].a) main = i; });
    const bb = polys.reduce((b, q) => bbox([q.bb[0], q.bb[1], q.bb[2], q.bb[3]], b), [1e9, 1e9, -1e9, -1e9]);
    return { adm: p.ADM0_A3, iso: iso === '-99' ? '' : iso.toLowerCase(), nombre: p.NAME_ES, lx: p.LABEL_X, ly: p.LABEL_Y, polys: polys.map(q => ({ rings: q.rings, bb: q.bb })), bb, mb: polys[main].bb, main };
  }).filter(Boolean);
}
function capas(archivo, filtro) {
  const out = []; for (const f of JSON.parse(fs.readFileSync(path.join(DAT, archivo), 'utf8')).features) { if (!filtro(f.properties)) continue;
    for (const pg of polysDe(f.geometry)) { const rings = pg.map(anillo); out.push({ rings, bb: bbox(rings[0]) }); } } return out;
}
function lineas(archivo) {
  const out = []; for (const f of JSON.parse(fs.readFileSync(path.join(DAT, archivo), 'utf8')).features) { const g = f.geometry; if (!g) continue;
    for (const l of g.type === 'LineString' ? [g.coordinates] : g.coordinates) { const c = anillo(l); out.push({ c, bb: bbox(c) }); } } return out;
}
function datos() {
  if (spec.estilo === 'documental') return {
    lo: paises('ne_50m_admin_0_countries.geojson'), hi: paises('ne_10m_admin_0_countries.geojson'),
    montes: capas('ne_10m_geography_regions_polys.geojson', p => ['Range/mtn', 'Plateau'].includes(p.FEATURECLA) && p.SCALERANK <= 4),
    desiertos: capas('ne_10m_geography_regions_polys.geojson', p => p.FEATURECLA === 'Desert' && p.SCALERANK <= 4),
    rios: lineas('ne_50m_rivers_lake_centerlines.geojson'),
  };
  if (spec.estilo === 'escena' || spec.motor) return {};
  if (spec.estilo === 'fantasia') { const [bx0, by0] = proj(-100, 18), [bx1, by1] = proj(-55, -22); return { paises: paises('ne_10m_admin_0_countries.geojson').filter(p => !(p.bb[2] < bx0 || p.bb[0] > bx1 || p.bb[3] < by0 || p.bb[1] > by1)) }; }
  if (spec.estilo === 'pergamino') return { paises: paises('ne_50m_admin_0_countries.geojson'), estados: estados('ne_50m_admin_1_states_provinces.geojson') };
  return { paises: paises('ne_50m_admin_0_countries.geojson') };
}
function estados(archivo) {
  return JSON.parse(fs.readFileSync(path.join(DAT, archivo), 'utf8')).features.map(f => {
    const p = f.properties, polys = polysDe(f.geometry).map(pg => { const rings = pg.map(anillo); return { rings, bb: bbox(rings[0]), a: area(rings[0]) }; });
    if (!polys.length) return null; let main = 0; polys.forEach((q, i) => { if (q.a > polys[main].a) main = i; });
    const bb = polys.reduce((b, q) => bbox([q.bb[0], q.bb[1], q.bb[2], q.bb[3]], b), [1e9, 1e9, -1e9, -1e9]);
    return { adm: `${p.adm0_a3}:${p.postal}`, iso: '', nombre: p.name, lx: p.longitude, ly: p.latitude, polys: polys.map(q => ({ rings: q.rings, bb: q.bb })), bb, mb: polys[main].bb, main };
  }).filter(Boolean);
}
function banderas(geo) {
  const usadas = new Set(); const ev = JSON.stringify(spec);
  if (spec.estilo !== 'caricatura') { for (const m of ev.matchAll(/"iso"\s*:\s*"([a-z]{2})"/g)) usadas.add(m[1]); }
  else geo.paises.forEach(p => p.iso && usadas.add(p.iso));
  const out = {}; for (const iso of usadas) { const f = path.join(DAT, 'banderas', iso + '.svg'); if (fs.existsSync(f)) out[iso] = 'data:image/svg+xml;base64,' + fs.readFileSync(f).toString('base64'); }
  // en caricatura las banderas se buscan por el iso del país; en el resto de capas se usa el iso en minúsculas
  return out;
}
function imagenes() {
  const out = {}, mime = { '.jpg': 'jpeg', '.jpeg': 'jpeg', '.png': 'png', '.webp': 'webp' };
  for (const e of [...spec.eventos, ...(spec.escenas || [])]) if (e.img && !out[e.img]) { const f = path.join(dir, e.img); if (!fs.existsSync(f)) { console.warn('falta imagen ' + e.img); continue; } out[e.img] = `data:image/${mime[path.extname(f).toLowerCase()]};base64,` + fs.readFileSync(f).toString('base64'); }
  return out;
}

(async () => {
  console.time('datos'); const geo = datos(), fl = banderas(geo), im = imagenes(); console.timeEnd('datos');
  const browser = await chromium.launch();
  const nuevaPagina = async () => {
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    await page.goto('file://' + path.join(__dirname, spec.motor ? spec.motor + '.html' : 'mapa.html'));
    await page.evaluate(() => Promise.all(['700 40px Fredoka', '600 40px Fredoka', '500 40px Fredoka', '400 40px Fredoka', '900 40px Montserrat', '800 40px Montserrat', '700 40px Montserrat', '600 40px Montserrat', '500 40px Montserrat', '400 40px Fell', 'italic 400 40px Fell'].map(f => document.fonts.load(f))));
    await page.evaluate(([g, s, f, i]) => init(g, s, f, i), [geo, spec, fl, im]);
    return page;
  };
  const grab = async (page, t) => Buffer.from((await page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', 0.92); }, t)).split(',')[1], 'base64');
  const dur = hasta ? Math.min(hasta, spec.duracion) : spec.duracion;

  if (preview) {
    const page = await nuevaPagina(), pd = path.join(dir, 'preview'); fs.mkdirSync(pd, { recursive: true });
    for (const t of preview) { console.time('cuadro ' + t); fs.writeFileSync(path.join(pd, `t${t.toFixed(1)}.jpg`), await grab(page, t)); console.timeEnd('cuadro ' + t); }
    console.log('preview en ' + pd);
  } else {
    const pages = await Promise.all(Array.from({ length: HILOS }, nuevaPagina));
    const desde = opt('--desde') ? Number(opt('--desde')) : 0, tramo = desde > 0 || hasta;
    const out = path.join(dir, (spec.salida || 'demo') + (tramo ? `-tramo-${desde}-${dur}` : '') + '.mp4');
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', ...(tramo ? [] : spec.audio ? ['-i', path.resolve(dir, spec.audio)] : ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']),
      ...(tramo ? ['-an'] : ['-shortest']), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', String(spec.crf || 23), '-maxrate', '9M', '-bufsize', '18M', '-preset', 'medium', ...(tramo ? [] : ['-c:a', 'aac', '-b:a', '128k']), '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round((dur - desde) * FPS), t0 = Date.now();
    for (let i = 0; i < n; i += HILOS) {
      const bufs = await Promise.all(pages.map((p, k) => i + k < n ? grab(p, desde + (i + k) / FPS) : null));
      for (const b of bufs) if (b && !ff.stdin.write(b)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % (FPS * 5) < HILOS) console.log(`  ${(i / FPS).toFixed(0)} / ${dur.toFixed(0)} s  (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    console.log('listo: ' + out);
  }
  await browser.close();
})();
