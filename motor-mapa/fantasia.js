// Estilo "fantasia": mapa de atlas ilustrado (pergamino, tinta, acuarela) con clima animado.
// Se carga después del script principal de mapa.html y usa sus funciones (proj, ws, setCam, fade, pr, hs...).
const DEG = 1000 / 360;
let AT = null, REG = {}, ECUP = null;
const TINTAF = '#3a2a18';
// límites aproximados entre Costa | Sierra | Amazonía (lon, lat), de norte a sur
const BORDE_OESTE = [[-78.1, 1.6], [-78.75, .3], [-79.0, -.3], [-79.1, -1.0], [-79.25, -1.7], [-79.4, -2.4], [-79.45, -3.0], [-79.7, -3.6], [-80.0, -4.1], [-80.0, -5.4]];
const BORDE_ESTE = [[-77.3, 1.0], [-77.7, .1], [-77.9, -.5], [-78.1, -1.2], [-78.3, -1.8], [-78.6, -2.5], [-78.8, -3.2], [-78.9, -3.9], [-79.0, -5.4]];
const VOLCANES = [[-78.82, -1.47, 1.35, 'Chimborazo'], [-78.44, -.68, 1.2, 'Cotopaxi'], [-77.99, .03, 1.1, 'Cayambe'], [-78.14, -.48, 1.0, 'Antisana'], [-78.44, -1.47, .95, 'Tungurahua'], [-78.34, -2.0, .95, 'Sangay'],
  [-78.6, -.17, .85, 'Pichincha'], [-78.71, -.66, .9, 'Illiniza'], [-78.41, -1.68, .95, 'Altar'], [-78.35, .36, .85, 'Cotacachi']];
const RIOS_F = [
  [[-78.15, -.95], [-77.75, -1.05], [-77.4, -1.05], [-77.0, -.95], [-76.5, -.6], [-76.0, -.75], [-75.4, -.95], [-74.9, -1.3]], // Napo
  [[-78.45, -1.4], [-78.1, -1.45], [-77.75, -1.7], [-77.3, -2.05], [-76.9, -2.4], [-76.6, -2.65], [-76.2, -3.1], [-75.9, -3.8]], // Pastaza
  [[-77.6, .15], [-77.0, 0], [-76.4, -.15], [-75.8, -.35], [-75.25, -.55]], // Aguarico
  [[-77.4, -1.4], [-76.8, -1.5], [-76.2, -1.6], [-75.6, -1.7], [-75.1, -2.0]], // Curaray
  [[-78.25, -2.4], [-77.95, -2.9], [-77.7, -3.4], [-77.75, -3.9], [-77.55, -4.4]], // Santiago / Morona
  [[-79.45, -.6], [-79.55, -1.2], [-79.75, -1.75], [-79.88, -2.2], [-79.9, -2.5]], // Guayas
  [[-79.25, 0], [-79.45, .4], [-79.62, .75], [-79.65, .98]], // Esmeraldas
];
const CIUDADES = [[-78.47, -.18, 8], [-79.9, -2.19, 8], [-79.0, -2.9, 6], [-78.0, -1.49, 4], [-80.96, -2.21, 4], [-79.7, .97, 4], [-80.72, -.95, 5], [-79.2, -4.0, 4], [-77.81, -.99, 3], [-78.62, -1.24, 5], [-79.96, -3.26, 5]];
const P = (lo, la) => proj(lo, la);
function polyW(list) { const p = new Path2D(); list.forEach(([lo, la], i) => { const [x, y] = P(lo, la); i ? p.lineTo(x, y) : p.moveTo(x, y); }); p.closePath(); return p; }
function lineaW(list) { const p = new Path2D(); list.forEach(([lo, la], i) => { const [x, y] = P(lo, la); i ? p.lineTo(x, y) : p.moveTo(x, y); }); return p; }
function desplazar(list, dlon) { return list.map(([lo, la]) => [lo + dlon, la]); }
function muestrear(list, paso) { const out = []; for (let i = 0; i < list.length - 1; i++) { const [a, b] = list[i], [c, d] = list[i + 1], L = Math.hypot(c - a, d - b), n = Math.max(1, Math.round(L / paso)); for (let k = 0; k < n; k++) out.push([lerp(a, c, k / n), lerp(b, d, k / n)]); } out.push(list[list.length - 1]); return out; }
function setCamOff(dx, dy, c2 = ctx) { c2.setTransform(CAM.z, 0, 0, CAM.z, W / 2 - CAM.x * CAM.z + dx, H / 2 - CAM.y * CAM.z + dy); }

// ---------- glifos del atlas (dibujados en coordenadas del mundo) ----------
function gMonte(g, x, y, s, nieve, alfa = 1, seed = 0) { // s = ancho en unidades del mundo
  g.save(); g.translate(x, y); g.scale(s / 100, s / 100); g.globalAlpha = alfa; const h = 62 + hs(seed, 3, 9) * 22, px = (hs(seed, 4, 9) - .5) * 14;
  g.beginPath(); g.moveTo(-50, 0); g.lineTo(px - 6, -h + 4); g.lineTo(px, -h); g.lineTo(px + 7, -h + 6); g.lineTo(50, 0); g.closePath(); g.fillStyle = '#cdb68a'; g.fill();
  g.beginPath(); g.moveTo(px, -h); g.lineTo(px + 7, -h + 6); g.lineTo(50, 0); g.lineTo(px + 10, 0); g.closePath(); g.fillStyle = '#8c7450'; g.fill();
  if (nieve) { g.beginPath(); g.moveTo(px - 6 - 9, -h + 22); g.lineTo(px - 6, -h + 4); g.lineTo(px, -h); g.lineTo(px + 7, -h + 6); g.lineTo(px + 17, -h + 24); g.lineTo(px + 8, -h + 18); g.lineTo(px + 2, -h + 27); g.lineTo(px - 6, -h + 17); g.closePath(); g.fillStyle = '#f7f4ec'; g.fill(); }
  g.strokeStyle = TINTAF; g.lineWidth = 3.2; g.lineJoin = 'round'; g.beginPath(); g.moveTo(-50, 0); g.lineTo(px - 6, -h + 4); g.lineTo(px, -h); g.lineTo(px + 7, -h + 6); g.lineTo(50, 0); g.stroke();
  g.lineWidth = 2; for (let k = 1; k <= 4; k++) { const u = k / 5; g.beginPath(); g.moveTo(px + 10 + u * 30, -h * (1 - u) + 6); g.lineTo(px + 4 + u * 30, -h * (1 - u) + 22); g.stroke(); }
  g.restore(); }
function gVolcan(g, x, y, s, nombre) {
  g.save(); g.translate(x, y); g.scale(s / 100, s / 100);
  g.beginPath(); g.moveTo(-58, 0); g.quadraticCurveTo(-24, -40, -10, -86); g.lineTo(10, -86); g.quadraticCurveTo(24, -40, 58, 0); g.closePath();
  const gr = g.createLinearGradient(-58, 0, 58, 0); gr.addColorStop(0, '#c9b088'); gr.addColorStop(.5, '#b0946a'); gr.addColorStop(1, '#7c6342'); g.fillStyle = gr; g.fill();
  g.beginPath(); g.moveTo(-24, -54); g.quadraticCurveTo(-16, -72, -10, -86); g.lineTo(10, -86); g.quadraticCurveTo(16, -72, 25, -55); g.lineTo(15, -60); g.lineTo(8, -50); g.lineTo(0, -62); g.lineTo(-9, -49); g.lineTo(-16, -60); g.closePath(); g.fillStyle = '#fbf9f3'; g.fill();
  g.strokeStyle = TINTAF; g.lineWidth = 3.4; g.beginPath(); g.moveTo(-58, 0); g.quadraticCurveTo(-24, -40, -10, -86); g.lineTo(10, -86); g.quadraticCurveTo(24, -40, 58, 0); g.stroke();
  g.lineWidth = 2; for (let k = 0; k < 5; k++) { g.beginPath(); g.moveTo(14 + k * 7, -40 + k * 8); g.lineTo(8 + k * 7, -26 + k * 8); g.stroke(); }
  if (nombre === 'Sangay' || nombre === 'Tungurahua') { g.fillStyle = 'rgba(120,110,100,.45)'; for (let k = 0; k < 4; k++) { g.beginPath(); g.arc(4 + k * 9, -96 - k * 12, 7 + k * 3, 0, Math.PI * 2); g.fill(); } }
  g.restore(); }
function gArbol(g, x, y, s, seed) {
  const c = ['#2c6331', '#376f37', '#41803d', '#2f6a3a'][Math.floor(hs(seed, 1, 3) * 4)], l = ['#5f9e52', '#6dab5a', '#579a4c'][Math.floor(hs(seed, 2, 3) * 3)], r = s / 2;
  g.fillStyle = c; g.beginPath(); g.arc(x - r * .55, y + r * .2, r * .72, 0, 7); g.arc(x + r * .55, y + r * .2, r * .72, 0, 7); g.arc(x, y - r * .2, r * .85, 0, 7); g.fill();
  g.fillStyle = l; g.beginPath(); g.arc(x - r * .25, y - r * .45, r * .32, 0, 7); g.fill();
  g.strokeStyle = 'rgba(30,45,20,.55)'; g.lineWidth = s * .06; g.beginPath(); g.arc(x, y - r * .2, r * .85, Math.PI * .9, Math.PI * 2.1); g.stroke(); }
function gPalma(g, x, y, s) {
  g.save(); g.translate(x, y); g.scale(s / 100, s / 100); g.strokeStyle = '#6b4a26'; g.lineWidth = 7; g.beginPath(); g.moveTo(0, 0); g.quadraticCurveTo(8, -30, 2, -62); g.stroke();
  g.strokeStyle = '#3f7d36'; g.lineWidth = 6; g.lineCap = 'round'; for (const [dx, dy] of [[-34, -50], [34, -48], [-22, -78], [26, -76], [0, -86]]) { g.beginPath(); g.moveTo(2, -62); g.quadraticCurveTo((2 + dx) / 2, -70, dx, dy); g.stroke(); } g.restore(); }
function gCactus(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s / 100, s / 100); g.strokeStyle = '#4f7a3a'; g.lineWidth = 12; g.lineCap = 'round'; g.beginPath(); g.moveTo(0, 0); g.lineTo(0, -60); g.moveTo(0, -30); g.lineTo(-18, -32); g.lineTo(-18, -48); g.moveTo(0, -38); g.lineTo(16, -40); g.lineTo(16, -56); g.stroke(); g.restore(); }
function gCasas(g, x, y, s, n, seed) {
  for (let k = 0; k < n; k++) { const a = hs(seed, k, 21) * 6.28, d = hs(seed, k, 22) * s * 1.1, cx = x + Math.cos(a) * d, cy = y + Math.sin(a) * d * .7, w = s * .38;
    g.fillStyle = '#efe2c2'; g.fillRect(cx - w / 2, cy - w * .6, w, w * .6); g.fillStyle = '#a8432f'; g.beginPath(); g.moveTo(cx - w * .62, cy - w * .58); g.lineTo(cx, cy - w * 1.05); g.lineTo(cx + w * .62, cy - w * .58); g.closePath(); g.fill();
    g.strokeStyle = TINTAF; g.lineWidth = w * .08; g.strokeRect(cx - w / 2, cy - w * .6, w, w * .6); } }

function prepFant() {
  ECUP = G.idx.ECU.path;
  const O = BORDE_OESTE, E = BORDE_ESTE, MEDIO = E.map((p, i) => [(p[0] + O[Math.min(i, O.length - 1)][0]) / 2, (p[1] + O[Math.min(i, O.length - 1)][1]) / 2]);
  REG.costa = polyW([[-86, O[0][1]], ...O, [-86, O[O.length - 1][1]]]);
  REG.sierra = polyW([...O, ...E.slice().reverse()]);
  REG.amazonia = polyW([...E, [-70, E[E.length - 1][1]], [-70, E[0][1]]]);
  const lon0 = -83.6, lon1 = -73.4, lat0 = -8.8, lat1 = 5.0, K = 100;
  const [ax0, ay0] = P(lon0, lat1), [ax1, ay1] = P(lon1, lat0);
  const c = document.createElement('canvas'); c.width = Math.ceil((ax1 - ax0) * K); c.height = Math.ceil((ay1 - ay0) * K);
  const g = c.getContext('2d'); const world = () => g.setTransform(K, 0, 0, K, -ax0 * K, -ay0 * K); world();
  AT = { c, x: ax0, y: ay0, w: ax1 - ax0, h: ay1 - ay0 };
  const bb = [ax0, ay0, ax1, ay1], tierra = new Path2D(); const vecinos = G.paises.filter(p => cruza(p.bb, bb)); vecinos.forEach(p => tierra.addPath(p.path));
  const dentro = (path, lo, la) => { const [x, y] = P(lo, la); return g.isPointInPath(path, (x - ax0) * K, (y - ay0) * K, 'evenodd'); };
  // 1 · líneas de costa concéntricas en el mar (de lejos a cerca)
  g.save(); g.lineJoin = 'round';
  for (const [d, al] of [[.78, .14], [.52, .22], [.31, .32], [.14, .45]]) { g.globalCompositeOperation = 'source-over'; g.strokeStyle = `rgba(28,62,66,${al})`; g.lineWidth = 2 * d + .035; g.stroke(tierra); g.globalCompositeOperation = 'destination-out'; g.lineWidth = 2 * d - .035; g.stroke(tierra); }
  g.globalCompositeOperation = 'source-over'; g.strokeStyle = 'rgba(190,232,222,.3)'; g.lineWidth = .7; g.filter = 'blur(6px)'; g.stroke(tierra); g.filter = 'none';
  g.restore(); world();
  // 2 · tierra de los vecinos (pergamino) con fronteras punteadas
  g.fillStyle = '#d9c99f'; g.fill(tierra, 'evenodd');
  g.save(); g.setLineDash([.09, .07]); g.strokeStyle = 'rgba(70,52,30,.55)'; g.lineWidth = .028; vecinos.forEach(p => g.stroke(p.path)); g.restore();
  // los Andes siguen (desvaídos) en Colombia y Perú
  const occ = desplazar(O, .22), ori = desplazar(E, -.22);
  const fuera = [...muestrear([[-76.9, 4.9], [-77.4, 2.9], [-77.75, 2.0], ...occ.slice(0, 2)], .17), ...muestrear([[-75.9, 4.9], [-76.6, 2.9], [-77.0, 1.9], ...ori.slice(0, 2)], .17), ...muestrear([occ[occ.length - 2], [-79.6, -5.6], [-79.0, -7.2], [-78.4, -8.7]], .17), ...muestrear([ori[ori.length - 2], [-78.7, -5.6], [-78.0, -7.2], [-77.3, -8.7]], .17)]
    .filter(([lo, la]) => !dentro(ECUP, lo, la)).sort((a, b) => b[1] - a[1]);
  fuera.forEach(([lo, la], i) => { const [x, y] = P(lo, la); gMonte(g, x, y, .62, false, .45, i + 500); });
  // 3 · Ecuador en acuarela por regiones
  g.save(); g.clip(ECUP, 'evenodd');
  g.fillStyle = '#bdb56f'; g.fill(REG.costa); g.fillStyle = '#bea77a'; g.fill(REG.sierra); g.fillStyle = '#5d9a50'; g.fill(REG.amazonia);
  const mancha = (lo, la, r, col) => { const [x, y] = P(lo, la), R = r * DEG, gr = g.createRadialGradient(x, y, 0, x, y, R); gr.addColorStop(0, col); gr.addColorStop(1, col.replace(/[\d.]+\)$/, '0)')); g.fillStyle = gr; g.fillRect(x - R, y - R, 2 * R, 2 * R); };
  g.save(); g.clip(REG.costa); mancha(-80.7, -2.25, 1.0, 'rgba(226,190,120,.95)'); mancha(-79.3, .55, 1.1, 'rgba(110,160,85,.75)'); mancha(-79.6, -1.4, .9, 'rgba(150,175,90,.5)'); g.restore();
  g.save(); g.clip(REG.sierra); g.strokeStyle = 'rgba(214,200,150,.85)'; g.lineWidth = .32 * DEG; g.lineCap = 'round'; g.filter = 'blur(10px)'; g.stroke(lineaW(muestrear(MEDIO, .3))); g.filter = 'none'; g.restore();
  g.save(); g.clip(REG.amazonia); mancha(-76.2, -1.8, 2.2, 'rgba(60,125,60,.55)'); g.restore();
  for (const k of ['costa', 'sierra', 'amazonia']) { g.save(); g.clip(REG[k]); g.strokeStyle = 'rgba(70,45,20,.28)'; g.lineWidth = .16; g.filter = 'blur(8px)'; g.stroke(REG[k]); g.stroke(ECUP); g.filter = 'none'; g.restore(); }
  // 4 · ríos
  g.lineCap = 'round'; g.lineJoin = 'round';
  for (const r of RIOS_F) { const p = lineaW(r); g.strokeStyle = 'rgba(40,80,100,.7)'; g.lineWidth = .085; g.stroke(p); g.strokeStyle = '#8fd0e6'; g.lineWidth = .05; g.stroke(p); }
  // 5 · Santa Elena seca: grietas y cactus
  const se = P(-80.72, -2.25); g.strokeStyle = 'rgba(120,82,40,.55)'; g.lineWidth = .012;
  for (let k = 0; k < 70; k++) { let x = se[0] + (hs(k, 1, 31) - .5) * 2.2, y = se[1] + (hs(k, 2, 31) - .5) * 1.5; g.beginPath(); g.moveTo(x, y); for (let j = 0; j < 4; j++) { x += (hs(k, j + 3, 31) - .5) * .18; y += (hs(k, j + 9, 31) - .5) * .18; g.lineTo(x, y); } g.stroke(); }
  // 6 · bosques: Amazonía densa, Chocó (norte de la Costa) y laderas occidentales
  const arboles = [];
  for (let la = 1.3; la > -5.2; la -= .075) for (let lo = -79.3; lo < -75.0; lo += .075) { const jl = lo + (hs(Math.round(lo * 100), Math.round(la * 100), 41) - .5) * .06, jt = la + (hs(Math.round(lo * 100), Math.round(la * 100), 42) - .5) * .06; if (dentro(ECUP, jl, jt) && dentro(REG.amazonia, jl, jt)) arboles.push([jl, jt, .26]); }
  for (let la = 1.4; la > .0; la -= .11) for (let lo = -80.1; lo < -78.5; lo += .11) { const jl = lo + (hs(Math.round(lo * 100), Math.round(la * 100), 43) - .5) * .08, jt = la + (hs(Math.round(lo * 100), Math.round(la * 100), 44) - .5) * .08; if (hs(Math.round(lo * 99), Math.round(la * 99), 45) < .6 && dentro(ECUP, jl, jt) && dentro(REG.costa, jl, jt)) arboles.push([jl, jt, .24]); }
  for (const [lo, la] of muestrear(desplazar(O, -.12), .09)) if (dentro(ECUP, lo, la)) arboles.push([lo + (hs(Math.round(lo * 100), 1, 46) - .5) * .08, la, .22]);
  arboles.sort((a, b) => b[1] - a[1]).forEach(([lo, la, s], i) => { const [x, y] = P(lo, la); gArbol(g, x, y, s, i); });
  // 7 · plantaciones de banano y palmeras en la Costa
  for (let k = 0; k < 16; k++) { const lo = -79.95 + hs(k, 1, 51) * .75, la = -.8 - hs(k, 2, 51) * 1.25; if (!dentro(ECUP, lo, la) || !dentro(REG.costa, lo, la)) continue; const [x, y] = P(lo, la), w = .32, h = .2;
    g.save(); g.translate(x, y); g.rotate((hs(k, 3, 51) - .5) * .5); g.fillStyle = 'rgba(120,160,70,.55)'; g.fillRect(-w / 2, -h / 2, w, h); g.strokeStyle = 'rgba(45,90,35,.8)'; g.lineWidth = .018; for (let r = 0; r < 5; r++) { g.beginPath(); g.moveTo(-w / 2 + .02, -h / 2 + .03 + r * .036); g.lineTo(w / 2 - .02, -h / 2 + .03 + r * .036); g.setLineDash([.03, .02]); g.stroke(); } g.setLineDash([]); g.strokeStyle = 'rgba(70,52,30,.5)'; g.strokeRect(-w / 2, -h / 2, w, h); g.restore(); }
  const palmas = []; for (let k = 0; k < 140; k++) { const lo = -80.9 + hs(k, 1, 52) * 1.7, la = 1.0 - hs(k, 2, 52) * 4.4; if (Math.hypot(lo + 80.72, la + 2.25) < .45) continue; if (dentro(ECUP, lo, la) && dentro(REG.costa, lo, la)) palmas.push([lo, la]); }
  palmas.sort((a, b) => b[1] - a[1]).forEach(([lo, la]) => { const [x, y] = P(lo, la); gPalma(g, x, y, .3); });
  for (let k = 0; k < 14; k++) { const lo = -80.85 + hs(k, 1, 53) * .55, la = -2.05 - hs(k, 2, 53) * .4; if (dentro(ECUP, lo, la)) { const [x, y] = P(lo, la); gCactus(g, x, y, .2); } }
  g.restore(); world();
  // 8 · cordilleras y volcanes
  const montes = [...muestrear(occ, .15).map(p => [...p, .58, 0]), ...muestrear(ori, .15).map(p => [...p, .62, 1]), ...muestrear(MEDIO.map(([a, b]) => [a + .05, b]), .32).map(p => [...p, .42, 2])]
    .filter(([lo, la]) => dentro(ECUP, lo, la)).map(([lo, la, s, k], i) => [lo + (hs(i, 1, 61) - .5) * .07, la + (hs(i, 2, 61) - .5) * .05, s * (.85 + hs(i, 3, 61) * .3), k]);
  const todo = [...montes.map(m => ['m', ...m]), ...VOLCANES.map(v => ['v', v[0], v[1], v[2], v[3]])].sort((a, b) => b[2] - a[2]);
  todo.forEach((m, i) => { const [x, y] = P(m[1], m[2]); if (m[0] === 'm') gMonte(g, x, y, m[3], m[4] === 1 && hs(i, 7, 62) < .35, 1, i); else gVolcan(g, x, y, m[3], m[4]); });
  // 9 · pueblos
  CIUDADES.forEach(([lo, la, n], i) => { const [x, y] = P(lo, la); gCasas(g, x, y, .11, n, i + 70); });
  // 10 · contorno de Ecuador a tinta
  g.strokeStyle = TINTAF; g.lineWidth = .06; g.lineJoin = 'round'; g.stroke(ECUP);
  g.strokeStyle = 'rgba(255,245,215,.35)'; g.lineWidth = .018; g.stroke(ECUP);
}

// ---------- capa viva del mapa ----------
function olasFant(t) {
  setCam(); const v = vista(.05); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.strokeStyle = 'rgba(175,220,212,.42)'; ctx.lineWidth = 2.4; ctx.lineCap = 'round'; ctx.beginPath();
  const paso = .42 * DEG, sz = cl(CAM.z * .32, 9, 26);
  for (let gx = Math.floor(v[0] / paso); gx <= Math.ceil(v[2] / paso); gx++) for (let gy = Math.floor(v[1] / paso); gy <= Math.ceil(v[3] / paso); gy++) {
    const wx = (gx + hs(gx, gy, 71) * .8) * paso, wy = (gy + hs(gx, gy, 72) * .8) * paso, [x, y] = wsx([wx, wy]), b = Math.sin(t * 1.4 + gx * 1.7 + gy) * 3;
    ctx.moveTo(x - sz, y + b); ctx.quadraticCurveTo(x - sz / 2, y - sz * .45 + b, x, y + b); ctx.quadraticCurveTo(x + sz / 2, y - sz * .45 + b, x + sz, y + b); }
  ctx.stroke(); }
function brujula(t) {
  const [x, y] = ws(-81.3, .15), r = cl(.62 * DEG * CAM.z, 40, 260); if (x < -r || x > W + r || y < -r || y > H + r) return;
  let giro = t * .05; for (const e of SP.eventos) if (e.tipo === 'girar') giro += eio(pr(t, e.desde, e.dur || 1.4)) * (e.vueltas || 2) * Math.PI * 2;
  ctx.save(); ctx.translate(x, y); ctx.rotate(giro); ctx.fillStyle = 'rgba(246,234,200,.85)'; ctx.beginPath(); ctx.arc(0, 0, r * .62, 0, 7); ctx.fill(); ctx.strokeStyle = TINTAF; ctx.lineWidth = 2.5; ctx.stroke(); ctx.beginPath(); ctx.arc(0, 0, r * .52, 0, 7); ctx.lineWidth = 1.2; ctx.stroke();
  for (let k = 0; k < 16; k++) { const a = k * Math.PI / 8, L = k % 4 === 0 ? r : k % 2 === 0 ? r * .66 : r * .42, wd = k % 4 === 0 ? r * .13 : r * .08; ctx.save(); ctx.rotate(a);
    ctx.beginPath(); ctx.moveTo(0, -wd); ctx.lineTo(L, 0); ctx.lineTo(0, 0); ctx.closePath(); ctx.fillStyle = k % 4 === 0 ? '#c8962e' : '#efe1bd'; ctx.fill(); ctx.beginPath(); ctx.moveTo(0, wd); ctx.lineTo(L, 0); ctx.lineTo(0, 0); ctx.closePath(); ctx.fillStyle = k % 4 === 0 ? '#6e4b16' : '#a8916a'; ctx.fill();
    ctx.strokeStyle = TINTAF; ctx.lineWidth = 1.3; ctx.beginPath(); ctx.moveTo(0, -wd); ctx.lineTo(L, 0); ctx.lineTo(0, wd); ctx.stroke(); ctx.restore(); }
  ctx.fillStyle = '#c8962e'; ctx.beginPath(); ctx.arc(0, 0, r * .08, 0, 7); ctx.fill(); ctx.stroke(); ctx.restore(); }
function rumbos() { const [x, y] = ws(-81.3, .15); ctx.save(); ctx.strokeStyle = 'rgba(30,24,14,.14)'; ctx.lineWidth = 1.4; for (let k = 0; k < 16; k++) { const a = k * Math.PI / 8; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(a) * 3000, y + Math.sin(a) * 3000); ctx.stroke(); } ctx.restore(); }
function barcosFant(t) { for (const [lo, la, i] of [[-80.95, -1.55, 0], [-80.35, .95, 1], [-81.45, -3.35, 2], [-80.55, -3.0, 3]]) { const [x, y] = ws(lo, la); if (x > -60 && x < W + 60 && y > -60 && y < H + 60) { ctx.save(); const s = cl(CAM.z / 60, .55, 1.6); ctx.translate(x, y); ctx.scale(s, s); barco(0, 0, t + i, .95, i % 2); ctx.restore(); } } }
function mapaFant(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#2b737c'; ctx.fillRect(0, 0, W, H);
  const sg = ctx.createRadialGradient(W * .35, H * .45, 60, W * .35, H * .45, H * .95); sg.addColorStop(0, 'rgba(120,195,190,.35)'); sg.addColorStop(1, 'rgba(8,36,46,.45)'); ctx.fillStyle = sg; ctx.fillRect(0, 0, W, H);
  olasFant(t); rumbos();
  for (const e of SP.eventos) if (e.mar && activo(t, e) && C[e.tipo]) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); C[e.tipo](e, t); ctx.restore(); }
  setCam(); const v = vista(); ctx.fillStyle = '#d9c99f'; for (const c of G.paises) if (cruza(c.bb, v)) ctx.fill(c.path, 'evenodd');
  ctx.imageSmoothingQuality = 'high'; ctx.drawImage(AT.c, AT.x, AT.y, AT.w, AT.h);
  ctx.setTransform(1, 0, 0, 1, 0, 0); brujula(t); barcosFant(t);
  // papel encima (multiplicar) + viñeta
  ctx.save(); ctx.globalCompositeOperation = 'multiply'; const p = PAT.papel || (PAT.papel = ctx.createPattern(papel(), 'repeat'));
  const ts = 900, ox = ((W / 2 - CAM.x * CAM.z * .02) % ts), oy = ((H / 2 - CAM.y * CAM.z * .02) % ts); p.setTransform(new DOMMatrix([ts / N, 0, 0, ts / N, ox, oy])); ctx.fillStyle = p; ctx.globalAlpha = .42; ctx.fillRect(0, 0, W, H); ctx.restore();
  const vg = ctx.createRadialGradient(W / 2, H / 2, Math.min(W, H) * .4, W / 2, H / 2, Math.max(W, H) * .72); vg.addColorStop(0, 'rgba(50,32,14,0)'); vg.addColorStop(1, 'rgba(50,32,14,.42)'); ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
}
function marcoFant(t) {
  const a = cl((t - 1.0) / .5); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = 'rgba(40,28,14,.85)'; ctx.lineWidth = 5; ctx.strokeRect(20, 20, W - 40, H - 40); ctx.lineWidth = 1.6; ctx.strokeRect(32, 32, W - 64, H - 64);
  ctx.fillStyle = '#c8962e'; for (const [x, y] of [[26, 26], [W - 26, 26], [26, H - 26], [W - 26, H - 26]]) { ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI / 4); ctx.fillRect(-9, -9, 18, 18); ctx.strokeRect(-9, -9, 18, 18); ctx.restore(); } ctx.restore(); }
function desenfoqueFant(t) { // barrido de movimiento cuando la cámara viaja rápido
  const c1 = Object.assign({}, CAM); camara(t - 1 / 30); const c0 = Object.assign({}, CAM); CAM = c1;
  const dx = (c0.x - c1.x) * c1.z, dy = (c0.y - c1.y) * c1.z, z = Math.abs(Math.log(c1.z / c0.z)), v = Math.hypot(dx, dy);
  if (v < 14 && z < .03) return; octx.setTransform(1, 0, 0, 1, 0, 0); octx.clearRect(0, 0, W, H); octx.drawImage(cv, 0, 0);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = .32;
  if (v >= 14) { const k = Math.min(1, 60 / v); ctx.drawImage(OFF, dx * .5 * k, dy * .5 * k); ctx.drawImage(OFF, -dx * .5 * k, -dy * .5 * k); }
  if (z >= .03) { const s = 1 + Math.min(.05, z * .6); ctx.drawImage(OFF, W / 2 - W * s / 2, H / 2 - H * s / 2, W * s, H * s); }
  ctx.restore(); }

// ---------- clima ----------
let NUB = null; function capaNubes() { if (!NUB) { NUB = document.createElement('canvas'); NUB.width = W; NUB.height = H; } const c = NUB.getContext('2d'); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, H); return c; }
function pegarNubes(a) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = a; ctx.drawImage(NUB, 0, 0); ctx.restore(); }
function nube(x, y, s, oscura, a, c2) {
  const ctx = c2 || window.ctx || document.getElementById('c').getContext('2d'); ctx.save(); ctx.globalAlpha = a; const pts = [[-.55, .12, .48], [-.22, -.22, .6], [.26, -.26, .54], [.6, .06, .44], [0, .16, .62], [-.85, .26, .3], [.88, .26, .3]];
  const path = new Path2D(); for (const [dx, dy, r] of pts) { path.moveTo(x + dx * s + r * s, y + dy * s); path.arc(x + dx * s, y + dy * s, r * s, 0, Math.PI * 2); }
  const g = ctx.createLinearGradient(0, y - s * .8, 0, y + s * .7); g.addColorStop(0, oscura ? '#e9ecef' : '#ffffff'); g.addColorStop(1, oscura ? '#5d6875' : '#cfd6de');
  ctx.strokeStyle = 'rgba(40,40,55,.45)'; ctx.lineWidth = Math.max(2.4, s * .05); ctx.lineJoin = 'round'; ctx.stroke(path);
  ctx.shadowColor = 'rgba(0,0,0,.25)'; ctx.shadowBlur = s * .25; ctx.shadowOffsetY = s * .12; ctx.fillStyle = g; ctx.fill(path); ctx.shadowColor = 'transparent'; ctx.restore(); }
function lluviaEn(cx, cy, R, t, a, sem, ang = .22) {
  if (a <= 0) return; const n = Math.round(cl(R * R / 160, 60, 900)), sp = R * 2.4; ctx.save(); ctx.strokeStyle = `rgba(232,242,255,${.78 * a})`; ctx.lineWidth = cl(R / 90, 1.8, 3.6); ctx.lineCap = 'round'; ctx.beginPath();
  for (let i = 0; i < n; i++) { const x0 = cx + (hs(i, 1, sem) * 2 - 1) * R, ph = hs(i, 2, sem) * sp, vel = sp * (1.1 + .5 * hs(i, 3, sem)), yy = ((ph + t * vel) % sp) - sp * .5, y = cy + yy * .8, x = x0 - yy * ang;
    const q = ((x - cx) / R) ** 2 + ((y - cy) / (R * .85)) ** 2; if (q > 1) continue; const L = R * (.07 + .05 * hs(i, 4, sem)); ctx.moveTo(x, y); ctx.lineTo(x - L * ang, y + L); }
  ctx.stroke(); ctx.restore(); }
function rayo(x, y0, y1, f, sem) {
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = `rgba(255,250,225,${.22 * f})`; ctx.fillRect(0, 0, W, H); ctx.restore();
  ctx.save(); ctx.shadowColor = '#fff3a8'; ctx.shadowBlur = 26; ctx.lineJoin = 'round'; const pts = [[x, y0]]; let xx = x; for (let k = 1; k <= 7; k++) { xx += (hs(Math.round(sem * 10), k, 81) - .5) * (y1 - y0) * .22; pts.push([xx, lerp(y0, y1, k / 7)]); }
  for (const [lw, col] of [[7, `rgba(255,245,190,${f})`], [2.6, `rgba(255,255,255,${f})`]]) { ctx.strokeStyle = col; ctx.lineWidth = lw; ctx.beginPath(); pts.forEach(([a, b], i) => i ? ctx.lineTo(a, b) : ctx.moveTo(a, b)); ctx.stroke(); } ctx.restore(); }
function gotaDib(x, y, r, a = 1) { ctx.save(); ctx.globalAlpha = a; ctx.shadowColor = 'rgba(150,220,255,.9)'; ctx.shadowBlur = r * 1.4; const g = ctx.createLinearGradient(x - r, y - r * 1.6, x + r, y + r); g.addColorStop(0, '#e6f7ff'); g.addColorStop(1, '#3a9ad6'); ctx.fillStyle = g;
  ctx.beginPath(); ctx.moveTo(x, y - r * 1.7); ctx.bezierCurveTo(x + r * 1.1, y - r * .2, x + r, y + r, x, y + r); ctx.bezierCurveTo(x - r, y + r, x - r * 1.1, y - r * .2, x, y - r * 1.7); ctx.fill(); ctx.shadowColor = 'transparent';
  ctx.fillStyle = 'rgba(255,255,255,.85)'; ctx.beginPath(); ctx.ellipse(x - r * .35, y - r * .1, r * .18, r * .35, -.4, 0, 7); ctx.fill(); ctx.restore(); }
const anclaF = e => e.lon !== undefined ? ws(e.lon, e.lat) : [e.x, e.y];

// ---------- corte lateral de Ecuador (Pacífico · Costa · Andes · Amazonía) ----------
const PERFIL = [[-20, 1270], [190, 1268], [240, 1250], [400, 1232], [470, 1150], [530, 930], [575, 790], [612, 905], [655, 960], [700, 900], [745, 760], [790, 880], [850, 1060], [930, 1170], [1100, 1200]];
function sueloY(x) { for (let i = 1; i < PERFIL.length; i++) if (x <= PERFIL[i][0]) { const [x0, y0] = PERFIL[i - 1], [x1, y1] = PERFIL[i], u = (x - x0) / (x1 - x0), s = u * u * (3 - 2 * u); return lerp(y0, y1, s); } return PERFIL[PERFIL.length - 1][1]; }
function corteEscena(u, e) {
  const nubeQ = eo(cl((u - (e.tNube ?? 2.2)) / 1.4)), lluQ = cl((u - (e.tLluvia ?? 3.2)) / .6), aireQ = cl((u - (e.tAire ?? .7)) / 1.8), frio = cl((u - (e.tFrio ?? 1.9)) / .8);
  // cielo
  const sk = ctx.createLinearGradient(0, 0, W, 0); sk.addColorStop(0, '#f2dfb2'); sk.addColorStop(.55, '#e4d6b5'); sk.addColorStop(1, rgbMix('#d9d2bd', '#8c96a3', nubeQ * .8)); ctx.fillStyle = sk; ctx.fillRect(0, 0, W, H);
  const sol = ctx.createRadialGradient(240, 520, 10, 240, 520, 330); sol.addColorStop(0, 'rgba(255,214,120,.75)'); sol.addColorStop(1, 'rgba(255,214,120,0)'); ctx.fillStyle = sol; ctx.fillRect(0, 150, 640, 760);
  ctx.save(); ctx.shadowColor = 'rgba(255,200,80,.9)'; ctx.shadowBlur = 40; ctx.fillStyle = '#ffd36b'; ctx.beginPath(); ctx.arc(240, 520, 46, 0, 7); ctx.fill(); ctx.restore(); ctx.strokeStyle = TINTAF; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(240, 520, 46, 0, 7); ctx.stroke();
  // mar
  ctx.fillStyle = '#2f7d86'; ctx.fillRect(0, 1262, 240, 260); ctx.strokeStyle = 'rgba(190,232,226,.6)'; ctx.lineWidth = 2.4; ctx.beginPath(); for (let i = 0; i < 8; i++) { const x = 12 + i * 28 + Math.sin(u * 2 + i) * 4, y = 1290 + (i % 3) * 30; ctx.moveTo(x, y); ctx.quadraticCurveTo(x + 8, y - 8, x + 16, y); } ctx.stroke();
  // estratos de tierra
  const suelo = new Path2D(); suelo.moveTo(-20, 1600); for (let x = -20; x <= 1100; x += 10) suelo.lineTo(x, sueloY(x)); suelo.lineTo(1100, 1600); suelo.closePath();
  ctx.save(); ctx.clip(suelo); const bandas = [['#c6ab78', 0], ['#a98a5c', 70], ['#8c6d45', 150], ['#6e5536', 240]]; for (const [col, off] of bandas) { ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(-20, 1600); for (let x = -20; x <= 1100; x += 10) ctx.lineTo(x, sueloY(x) + off + Math.sin(x * .02) * 8); ctx.lineTo(1100, 1600); ctx.closePath(); ctx.fill(); }
  ctx.restore();
  // selva a la derecha, bosque nublado en las laderas y costa verde-ocre
  for (let x = 1100; x >= 840; x -= 19) { const y = sueloY(x); gArbolPx(x + (hs(x, 1, 91) - .5) * 8, y - 10, 34 + hs(x, 2, 91) * 14, x); }
  for (let x = 800; x >= 770; x -= 15) gArbolPx(x, sueloY(x) - 8, 24, x + 7);
  for (let x = 480; x <= 515; x += 14) gArbolPx(x, sueloY(x) - 8, 22, x + 3);
  ctx.save(); ctx.strokeStyle = 'rgba(60,40,20,.45)'; ctx.lineWidth = 2.2; for (const [x0, x1] of [[540, 575], [585, 610], [705, 745], [752, 790]]) for (let x = x0; x <= x1; x += 9) { const y = sueloY(x); ctx.beginPath(); ctx.moveTo(x, y + 8); ctx.lineTo(x + 6, y + 30); ctx.stroke(); } ctx.restore();
  ctx.fillStyle = '#b8b06c'; ctx.beginPath(); ctx.moveTo(240, 1262); for (let x = 240; x <= 470; x += 10) ctx.lineTo(x, sueloY(x)); ctx.lineTo(470, sueloY(470) + 18); ctx.lineTo(240, 1280); ctx.closePath(); ctx.fill();
  // nieve en los picos
  for (const [px, py] of [[575, 790], [745, 760]]) { ctx.fillStyle = '#fbf9f3'; ctx.beginPath(); ctx.moveTo(px - 46, py + 70); ctx.lineTo(px, py); ctx.lineTo(px + 44, py + 66); ctx.lineTo(px + 22, py + 52); ctx.lineTo(px + 8, py + 70); ctx.lineTo(px - 10, py + 50); ctx.lineTo(px - 26, py + 64); ctx.closePath(); ctx.fill(); }
  ctx.strokeStyle = TINTAF; ctx.lineWidth = 4; ctx.beginPath(); for (let x = -20; x <= 1100; x += 10) x === -20 ? ctx.moveTo(x, sueloY(x)) : ctx.lineTo(x, sueloY(x)); ctx.stroke();
  ctx.fillStyle = 'rgba(30,20,10,.85)'; ctx.fillRect(-20, 1598, W + 40, 6);
  // casitas en el valle interandino (Quito)
  for (let k = 0; k < 4; k++) { const x = 628 + k * 14, y = sueloY(x) - 2; ctx.fillStyle = '#efe2c2'; ctx.fillRect(x - 6, y - 10, 12, 10); ctx.fillStyle = '#a8432f'; ctx.beginPath(); ctx.moveTo(x - 8, y - 10); ctx.lineTo(x, y - 18); ctx.lineTo(x + 8, y - 10); ctx.fill(); }
  // aire húmedo que llega desde la Amazonía, choca, sube y se enfría
  if (aireQ > 0) for (let k = 0; k < 4; k++) {
    const off = 50 + k * 42, pts = []; for (let x = 1120; x >= 600; x -= 12) { const sube = x < 900 ? (900 - x) * (.55 + k * .08) : 0; pts.push([x, Math.min(sueloY(x) - off, 1180 - off) - sube * .35]); }
    const n = Math.max(2, Math.floor(pts.length * aireQ)); ctx.save(); ctx.lineCap = 'round';
    for (let i = 1; i < n; i++) { const [x0, y0] = pts[i - 1], [x1, y1] = pts[i], fr = cl((900 - x1) / 280) * frio; ctx.strokeStyle = rgbMix('#3fd0c4', '#ffffff', fr); ctx.globalAlpha = .55 + .3 * fr; ctx.lineWidth = 14 - k * 2; ctx.beginPath(); ctx.moveTo(x0, y0 + Math.sin(i * .5 + u * 5 + k) * 4); ctx.lineTo(x1, y1 + Math.sin((i + 1) * .5 + u * 5 + k) * 4); ctx.stroke(); }
    ctx.globalAlpha = .9; ctx.fillStyle = '#e8fbff'; for (let d = 0; d < 6; d++) { const ph = ((u * .45 + d / 6 + k * .13) % 1) * (n - 1), i = Math.floor(ph), [xa, ya] = pts[i] || pts[0]; ctx.beginPath(); ctx.arc(xa, ya, 4.5, 0, 7); ctx.fill(); }
    ctx.restore(); }
  // escarcha al subir
  if (frio > 0) { ctx.save(); ctx.fillStyle = '#ffffff'; for (let k = 0; k < 26; k++) { const x = 620 + hs(k, 1, 93) * 260, y = 640 + hs(k, 2, 93) * 260, tw = Math.max(0, Math.sin(u * 7 + k * 1.7)); ctx.globalAlpha = frio * tw; ctx.beginPath(); ctx.moveTo(x, y - 7); ctx.lineTo(x + 2, y); ctx.lineTo(x, y + 7); ctx.lineTo(x - 2, y); ctx.closePath(); ctx.fill(); ctx.beginPath(); ctx.moveTo(x - 7, y); ctx.lineTo(x, y + 2); ctx.lineTo(x + 7, y); ctx.lineTo(x, y - 2); ctx.closePath(); ctx.fill(); } ctx.restore(); }
  // nubes que crecen sobre la ladera oriental
  if (nubeQ > 0) { const nc = capaNubes(); nc.setTransform(ctx.getTransform()); for (const [x, y, s] of [[700, 640, 150], [820, 600, 170], [930, 650, 140], [760, 520, 120], [880, 500, 110]]) nube(x, y + (1 - nubeQ) * 90, s * (.35 + .65 * nubeQ), true, 1, nc); pegarNubes(nubeQ); }
  // la cortina de lluvia y los ríos que regresan a la Amazonía
  if (lluQ > 0) { lluviaEn(820, 900, 230, u, lluQ, 97, .12); ctx.save(); ctx.strokeStyle = 'rgba(120,200,235,.95)'; ctx.lineWidth = 7; ctx.setLineDash([26, 16]); ctx.lineDashOffset = -u * 90; ctx.beginPath(); for (let x = 800; x <= 1100; x += 10) x === 800 ? ctx.moveTo(x, sueloY(x) - 4) : ctx.lineTo(x, sueloY(x) - 4); ctx.globalAlpha = lluQ; ctx.stroke(); ctx.restore(); }
  for (const r of e.rayos || []) { const q = u - r; if (q >= 0 && q < .35) rayo(800 + (hs(Math.round(r * 10), 2, 95) - .5) * 160, 640, 940, Math.exp(-q * 9), r); }
}
function gArbolPx(x, y, s, seed) { ctx.save(); const save = ctx; gArbol(save, x, y, s, seed); ctx.restore(); }

Object.assign(C, {
  girar() {},
  tormenta(e, t) {
    const a = fade(t, e, e.fi ?? .5, e.fo ?? .6) * (e.int ?? 1); if (a <= 0) return; const [cx, cy] = ws(e.lon, e.lat), R = (e.r || 1) * DEG * CAM.z, sem = e.sem || 7;
    ctx.save(); ctx.globalCompositeOperation = 'multiply'; const g = ctx.createRadialGradient(cx, cy, R * .15, cx, cy, R * 1.2); g.addColorStop(0, `rgba(60,80,115,${.6 * a})`); g.addColorStop(1, 'rgba(60,80,115,0)'); ctx.fillStyle = g; ctx.fillRect(cx - R * 1.3, cy - R * 1.3, R * 2.6, R * 2.6); ctx.restore();
    lluviaEn(cx, cy + R * .1, R, t, a * (e.lluvia ?? 1), sem);
    const crece = e.crece ? eo(pr(t, e.desde, e.crece)) : 1, n = e.n || 7, entra = e.desdeMar ? (1 - eo(pr(t, e.desde, 1.6))) * R * 1.6 : 0;
    const nc = capaNubes(); for (let k = 0; k < n; k++) { const x = cx + (hs(k, 4, sem) * 2 - 1) * R * .8 + Math.sin(t * .35 + k) * R * .05 - entra, y = cy - R * .45 + (hs(k, 5, sem) * 2 - 1) * R * .3; nube(x, y, R * (.26 + .2 * hs(k, 6, sem)) * crece, e.oscura ?? true, 1, nc); } pegarNubes(a);
    for (const r of e.rayos || []) { const u = t - r; if (u < 0 || u > .35) continue; rayo(cx + (hs(Math.round(r * 10), 1, 5) - .5) * R * .9, cy - R * .4, cy + R * .55, Math.exp(-u * 9), r); } },
  seco(e, t) {
    const a = fade(t, e, .4, .5); if (a <= 0) return; const [cx, cy] = ws(e.lon, e.lat), R = (e.r || .5) * DEG * CAM.z;
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 1.4); g.addColorStop(0, `rgba(255,185,70,${.42 * a})`); g.addColorStop(1, 'rgba(255,185,70,0)'); ctx.fillStyle = g; ctx.fillRect(cx - R * 1.5, cy - R * 1.5, R * 3, R * 3);
    ctx.translate(cx, cy); ctx.rotate(t * .12); ctx.fillStyle = `rgba(255,225,150,${.12 * a})`; for (let k = 0; k < 12; k++) { ctx.rotate(Math.PI / 6); ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(R * 1.7, -R * .07); ctx.lineTo(R * 1.7, R * .07); ctx.closePath(); ctx.fill(); } ctx.restore();
    ctx.save(); ctx.strokeStyle = `rgba(255,236,200,${.3 * a})`; ctx.lineWidth = 2; for (let k = 0; k < 7; k++) { const y = cy + R * .5 - ((t * R * .35 + k * R * .16) % (R * 1.1)); ctx.globalAlpha = cl(1 - (cy + R * .5 - y) / (R * 1.1)); ctx.beginPath(); for (let x = cx - R * .8; x <= cx + R * .8; x += 8) { const yy = y + Math.sin(x * .05 + t * 6 + k) * 4; x === cx - R * .8 ? ctx.moveTo(x, yy) : ctx.lineTo(x, yy); } ctx.stroke(); } ctx.restore();
    if (e.remolino) { const [x, y] = [cx + R * .25, cy + R * .2], s = R / 70; ctx.save(); ctx.strokeStyle = `rgba(170,128,70,${.65 * a})`; ctx.lineWidth = 3 * s; for (let j = 0; j < 12; j++) { const h = j * 9 * s, rx = (5 + j * 3.2) * s; ctx.beginPath(); ctx.ellipse(x + Math.sin(t * 3 + j * .5) * 4 * s, y - h, rx, rx * .28, 0, t * 9 + j, t * 9 + j + 4); ctx.stroke(); } ctx.restore(); } },
  trazo(e, t) {
    const q = eo(pr(t, e.desde, e.dur || .8)), a = fade(t, e, .05, .4); if (q <= 0) return; const [x0, y0] = ws(...e.de), [x1, y1] = ws(...e.a), mx = (x0 + x1) / 2, my = (y0 + y1) / 2 - Math.hypot(x1 - x0, y1 - y0) * (e.arco ?? .18);
    const pt = u => [(1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1];
    ctx.save(); ctx.globalAlpha = a; ctx.lineCap = 'round'; ctx.shadowColor = '#ffd23f'; ctx.shadowBlur = 16; ctx.strokeStyle = '#ffd23f'; ctx.lineWidth = 7; ctx.setLineDash([18, 14]); ctx.lineDashOffset = -t * 70; ctx.beginPath();
    for (let k = 0; k <= 60; k++) { const [x, y] = pt(q * k / 60); k ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); ctx.setLineDash([]);
    for (const [u, [x, y]] of [[0, [x0, y0]], [q, pt(q)]]) { const r = 12 + Math.sin(t * 6 + u * 3) * 3; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fillStyle = '#fff4c2'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = TINTAF; ctx.stroke(); } ctx.restore(); },
  regiones3(e, t) {
    const a = fade(t, e, .2, .45); if (a <= 0) return; const orden = ['costa', 'sierra', 'amazonia'];
    let foco = null; for (const [ft, k] of e.foco || []) if (t >= ft) foco = k;
    orden.forEach((k, i) => { const q = eob(pr(t, e.desde + i * (e.paso ?? .22), .45)) * a; if (q <= 0) return; const lift = (e.alto ?? 26) * q * (foco === k ? 1.5 : 1);
      ctx.save(); setCamOff(9 * q, 12 * q); ctx.clip(ECUP, 'evenodd'); ctx.fillStyle = `rgba(30,18,6,${.4 * q})`; ctx.fill(REG[k]); ctx.restore();
      ctx.save(); setCamOff(0, -lift); ctx.clip(ECUP, 'evenodd'); ctx.clip(REG[k]); ctx.drawImage(AT.c, AT.x, AT.y, AT.w, AT.h);
      if (foco && foco !== k) { ctx.fillStyle = 'rgba(25,18,10,.32)'; ctx.fill(REG[k]); } if (foco === k) { ctx.fillStyle = 'rgba(255,240,200,.12)'; ctx.fill(REG[k]); }
      ctx.strokeStyle = foco === k ? '#ffd23f' : TINTAF; ctx.lineWidth = (foco === k ? 9 : 6) / CAM.z; ctx.stroke(REG[k]); ctx.stroke(ECUP); ctx.restore(); }); },
  nubesPaso(e, t) { // transición: la cámara se mete en las nubes
    const u = pr(t, e.desde, e.dur || 1), a = Math.sin(Math.PI * u); if (a <= 0) return;
    const nc = capaNubes(); for (let k = 0; k < 9; k++) { const s = lerp(160, 900, eio(u)) * (.7 + hs(k, 1, 99) * .6), x = W / 2 + (hs(k, 2, 99) - .5) * W * 1.2 * (1 + u), y = H / 2 + (hs(k, 3, 99) - .5) * H * (1 + u); nube(x, y, s, false, 1, nc); } pegarNubes(a);
    ctx.fillStyle = `rgba(250,250,248,${cl((a - .55) * 2.6)})`; ctx.fillRect(0, 0, W, H); },
  corte(e, t) {
    const u = t - e.desde, abre = eo(cl(u / .55)), cierra = e.hasta !== undefined ? eo(cl((e.hasta - t) / .55)) : 1, k = Math.min(abre, cierra); if (k <= 0) return;
    ctx.save(); ctx.translate(0, H / 2); ctx.scale(1, k); ctx.translate(0, -H / 2); const z = 1 + .07 * cl((u - (e.tZoom ?? 5)) / 3); ctx.translate(800, 900); ctx.scale(z, z); ctx.translate(-800, -900);
    corteEscena(u, e); ctx.restore();
    if (k < 1) { ctx.fillStyle = `rgba(40,28,14,${(1 - k) * .55})`; ctx.fillRect(0, 0, W, H); } },
  corriente(e, t) {
    const a = fade(t, e, .1, .6); if (a <= 0) return; const pts = e.ruta.map(([lo, la]) => ws(lo, la)); const L = [0]; for (let i = 1; i < pts.length; i++) L.push(L[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    const q = eio(pr(t, e.desde, e.dur || 1.3)) * L[L.length - 1], wid = (e.ancho || .5) * DEG * CAM.z; const parcial = []; for (let i = 0; i < pts.length; i++) { if (L[i] <= q) parcial.push(pts[i]); else { const f = (q - L[i - 1]) / (L[i] - L[i - 1]); parcial.push([lerp(pts[i - 1][0], pts[i][0], f), lerp(pts[i - 1][1], pts[i][1], f)]); break; } }
    if (parcial.length < 2) return; const camino = () => { ctx.beginPath(); parcial.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); };
    ctx.save(); ctx.globalAlpha = a; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.shadowColor = e.color; ctx.shadowBlur = 30; ctx.strokeStyle = e.color; ctx.globalAlpha = a * .55; ctx.lineWidth = wid; camino(); ctx.stroke(); ctx.shadowColor = 'transparent';
    ctx.globalAlpha = a * .85; ctx.strokeStyle = e.brillo || '#ffffff'; ctx.lineWidth = wid * .16; ctx.setLineDash([wid * .9, wid * .8]); ctx.lineDashOffset = -t * wid * 1.6; camino(); ctx.stroke(); ctx.setLineDash([]);
    if (e.frio) { ctx.fillStyle = '#ffffff'; for (let k = 0; k < 40; k++) { const f = hs(k, 1, 101) * q, i = L.findIndex(l => l >= f); if (i < 1) continue; const g = (f - L[i - 1]) / (L[i] - L[i - 1]), x = lerp(pts[i - 1][0], pts[i][0], g) + (hs(k, 2, 101) - .5) * wid, y = lerp(pts[i - 1][1], pts[i][1], g) + (hs(k, 3, 101) - .5) * wid * .5; ctx.globalAlpha = a * Math.max(0, Math.sin(t * 6 + k)); ctx.fillRect(x - 2, y - 2, 4, 4); } }
    ctx.restore(); },
  nubesBajas(e, t) {
    const a = fade(t, e, .5, .5); if (a <= 0) return; for (const [k, [lo, la]] of e.puntos.entries()) { const [x, y] = ws(lo + Math.sin(t * .3 + k) * .05, la), w = .75 * DEG * CAM.z, h = w * .22;
      ctx.save(); ctx.globalAlpha = a * .6; ctx.filter = 'blur(2.5px)'; const g = ctx.createLinearGradient(0, y - h, 0, y + h); g.addColorStop(0, '#eef0f2'); g.addColorStop(1, '#9aa3ad'); ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, y, w, h, 0, 0, 7); ctx.ellipse(x - w * .45, y + h * .25, w * .55, h * .8, 0, 0, 7); ctx.ellipse(x + w * .5, y + h * .2, w * .5, h * .75, 0, 0, 7); ctx.fill(); ctx.strokeStyle = 'rgba(40,40,50,.25)'; ctx.lineWidth = 2; ctx.stroke(); ctx.restore();
      if (e.llovizna) lluviaEn(x, y + h * 2.2, w * .9, t, a * .35, 120 + k, .1); } },
  calor(e, t) {
    const q = eio(pr(t, e.desde, e.dur || 1.8)), a = fade(t, e, .05, .8); if (a <= 0) return; const fx = lerp(-W * .35, W * 1.4, q);
    ctx.save(); const g = ctx.createLinearGradient(fx - W * 1.2, 0, fx, 0); g.addColorStop(0, `rgba(214,52,38,${.72 * a})`); g.addColorStop(.6, `rgba(255,128,52,${.62 * a})`); g.addColorStop(1, 'rgba(255,170,80,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, Math.max(0, fx), H);
    ctx.globalCompositeOperation = 'lighter'; ctx.strokeStyle = `rgba(255,210,150,${.22 * a})`; ctx.lineWidth = 2.5; for (let k = 0; k < 18; k++) { const y = (k / 18) * H + Math.sin(t * 2 + k) * 10; ctx.beginPath(); for (let x = 0; x < Math.min(fx, W); x += 14) { const yy = y + Math.sin(x * .03 + t * 4 + k) * 6; x ? ctx.lineTo(x, yy) : ctx.moveTo(x, yy); } ctx.stroke(); } ctx.restore();
    ctx.save(); ctx.strokeStyle = `rgba(255,255,255,${.4 * a})`; ctx.lineWidth = 4; ctx.lineCap = 'round'; for (let k = 0; k < 28; k++) { const x0 = hs(k, 1, 111) * W, ph = (t * .5 + hs(k, 2, 111)) % 1, y0 = H * (.15 + hs(k, 3, 111) * .8) - ph * 120; if (x0 > fx - 60) continue; ctx.globalAlpha = a * Math.sin(ph * Math.PI) * .8; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.bezierCurveTo(x0 + 18, y0 - 25, x0 - 18, y0 - 50, x0, y0 - 78); ctx.stroke(); } ctx.restore(); },
  inundacion(e, t) {
    const q = eo(pr(t, e.desde, e.dur || 2.4)), a = fade(t, e, .1, .6); if (q <= 0 || a <= 0) return; const [cx, cy] = ws(e.lon, e.lat), R = (e.r || .6) * DEG * CAM.z * q;
    ctx.save(); setCam(); ctx.clip(ECUP, 'evenodd'); ctx.clip(REG.costa); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = a; ctx.fillStyle = 'rgba(55,125,200,.5)'; ctx.beginPath();
    for (let k = 0; k < 11; k++) { const an = hs(k, 1, 121) * 6.28, d = hs(k, 2, 121) * R * .7, r = R * (.35 + hs(k, 3, 121) * .35); ctx.moveTo(cx + Math.cos(an) * d + r, cy + Math.sin(an) * d * .8); ctx.arc(cx + Math.cos(an) * d, cy + Math.sin(an) * d * .8, r, 0, 7); }
    ctx.fill(); ctx.strokeStyle = 'rgba(210,240,255,.7)'; ctx.lineWidth = 2.5; for (let k = 0; k < 3; k++) { const rr2 = ((t * 60 + k * R * .33) % (R * .9)); ctx.globalAlpha = a * (1 - rr2 / (R * .9)); ctx.beginPath(); ctx.ellipse(cx, cy, rr2, rr2 * .7, 0, 0, 7); ctx.stroke(); } ctx.restore(); },
  tinte(e, t) { const a = fade(t, e, .8, .6) * (e.alfa ?? .45); if (a <= 0) return; ctx.save(); setCam(); ctx.clip(ECUP, 'evenodd'); ctx.globalCompositeOperation = e.modo || 'multiply'; ctx.fillStyle = e.color; ctx.globalAlpha = a; ctx.fill(REG[e.region]); ctx.restore(); },
  noche(e, t) {
    const a = fade(t, e, .5, .7); if (a <= 0) return; ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = `rgba(30,42,92,${.78 * a})`; ctx.fillRect(0, 0, W, H); ctx.restore();
    ctx.save(); for (let k = 0; k < 70; k++) { const x = hs(k, 1, 131) * W, y = hs(k, 2, 131) * H * .55, tw = .5 + .5 * Math.sin(t * 3 + k); ctx.globalAlpha = a * tw * .9; ctx.fillStyle = '#fffbe6'; ctx.fillRect(x, y, 2.5, 2.5); } ctx.restore();
    const [sx, sy] = [e.estrella?.[0] ?? 760, e.estrella?.[1] ?? 330], s = 30 + Math.sin(t * 4) * 4; ctx.save(); ctx.globalAlpha = a; ctx.shadowColor = '#fff1a8'; ctx.shadowBlur = 40; ctx.fillStyle = '#fff6c9'; ctx.beginPath(); ctx.moveTo(sx, sy - s * 2); ctx.lineTo(sx + s * .3, sy - s * .3); ctx.lineTo(sx + s * 1.4, sy); ctx.lineTo(sx + s * .3, sy + s * .3); ctx.lineTo(sx, sy + s * 2); ctx.lineTo(sx - s * .3, sy + s * .3); ctx.lineTo(sx - s * 1.4, sy); ctx.lineTo(sx - s * .3, sy - s * .3); ctx.closePath(); ctx.fill(); ctx.restore();
    if (e.lon !== undefined) { const [bx, by] = ws(e.lon, e.lat); ctx.save(); ctx.globalAlpha = a; ctx.globalCompositeOperation = 'lighter'; const g = ctx.createRadialGradient(bx + 10, by - 26, 0, bx + 10, by - 26, 120); g.addColorStop(0, 'rgba(255,190,90,.75)'); g.addColorStop(1, 'rgba(255,190,90,0)'); ctx.fillStyle = g; ctx.fillRect(bx - 130, by - 160, 280, 280); ctx.restore();
      ctx.save(); ctx.translate(bx, by); ctx.scale(1.9, 1.9); barco(0, 0, t, a, false); ctx.fillStyle = '#ffd27a'; ctx.beginPath(); ctx.arc(8, -20, 3.2, 0, 7); ctx.fill(); ctx.restore(); } },
  gota(e, t) {
    const u = t - e.desde, cae = e.cae || .55; if (u < cae) { ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H); gotaDib(W / 2, lerp(-70, H * .46, eio(u / cae) ** 1.4), 30); return; }
    const q = eo(cl((u - cae) / (e.abre || .85))); if (q >= 1) return; const R = q * Math.hypot(W, H) * .62, cy = H * .46 + 30;
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, H); ctx.arc(W / 2, cy, R, 0, Math.PI * 2); ctx.fillStyle = '#000'; ctx.fill('evenodd'); ctx.restore();
    ctx.save(); for (const [f, lw] of [[1, 12], [.72, 6], [.48, 3]]) { ctx.strokeStyle = `rgba(200,236,255,${(1 - q) * .9})`; ctx.lineWidth = lw; ctx.beginPath(); ctx.arc(W / 2, cy, R * f, 0, 7); ctx.stroke(); }
    if (u - cae < .35) for (let k = 0; k < 10; k++) { const an = -Math.PI * (.1 + .8 * hs(k, 1, 141)), d = (u - cae) * 900 * (.5 + hs(k, 2, 141)), x = W / 2 + Math.cos(an) * d, y = cy + Math.sin(an) * d + (u - cae) ** 2 * 1800; gotaDib(x, y, 7, 1 - (u - cae) / .35); } ctx.restore(); },
  contador(e, t) { const v = lerp(e.de ?? 0, e.a, eo(pr(t, e.desde + .1, e.dur || 1))); const txt = (e.pre || '') + (e.dec ? v.toFixed(e.dec) : Math.round(v).toLocaleString('en-US')) + (e.suf || ''); C.cifra(Object.assign({}, e, { texto: txt }), t); },
  caja(e, t) { // recuadro rojo de impacto con texto blanco (golpe al entrar)
    const p = pr(t, e.desde, .3), a = fade(t, e, .01, .3); if (p <= 0) return; const sc = 1 + (1 - eo(p)) * 1.4, sz = e.tam || 120; ctx.save(); ctx.globalAlpha = a * Math.min(1, p * 3); ctx.translate(e.x ?? W / 2, e.y ?? 330); ctx.rotate(-.04); ctx.scale(sc, sc);
    ctx.font = F(700, sz); const w = ctx.measureText(e.texto).width + sz * .7, h = sz * 1.25; ctx.fillStyle = '#000'; ctx.fillRect(-w / 2 - 12, -h / 2 - 12, w + 24, h + 24); ctx.fillStyle = e.color || '#e41e1e'; ctx.fillRect(-w / 2, -h / 2, w, h);
    texto(e.texto, 0, sz * .06, F(700, sz), '#fff', 'center', 'middle', '#000', sz * .14); ctx.restore(); },
  chip(e, t) {
    const p = eob(pr(t, e.desde, .4)), a = fade(t, e, .05, .3); if (p <= 0) return; const [x, y] = anclaF(e), sz = e.tam || 40; ctx.save(); ctx.globalAlpha = a; ctx.translate(x + (e.dx || 0), y + (e.dy || 0)); ctx.scale(p, p); ctx.rotate(e.rot || 0);
    ctx.font = F(700, sz); const w = ctx.measureText(e.texto).width + sz * 1.1, h = sz * 1.55; ctx.shadowColor = 'rgba(0,0,0,.45)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 5; rr(-w / 2, -h / 2, w, h, h / 2, e.fondo || 'rgba(12,22,32,.92)'); ctx.shadowColor = 'transparent'; rr(-w / 2 + 3, -h / 2 + 3, w - 6, h - 6, h / 2 - 3, null, e.color || ACC, 3);
    texto(e.texto, 0, 2, F(700, sz), e.colorTexto || '#fff'); if (e.flecha) { ctx.fillStyle = e.color || ACC; ctx.beginPath(); ctx.moveTo(-10, h / 2 - 2); ctx.lineTo(10, h / 2 - 2); ctx.lineTo(0, h / 2 + 18); ctx.closePath(); ctx.fill(); } ctx.restore(); },
});
