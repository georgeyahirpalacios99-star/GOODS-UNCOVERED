// Página del motor 3D (la carga render3d.cjs). Usa three.js.
let R, SC, CAM, ESC, OV, OX, P = {}, CTR, PART = [], FANT = null;
const lerp = (a, b, p) => a + (b - a) * p, cl = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v)), pr = (t, a, d) => cl((t - a) / d);
const eio = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2, eo = p => 1 - Math.pow(1 - p, 3), eob = p => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); };
const hs = s => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) % 9973; return h / 9973; };
const projM = (lon, lat) => [(lon + 180) / 360 * 1000, (1 - Math.log(Math.tan(Math.PI / 4 + lat * Math.PI / 360)) / Math.PI) / 2 * 1000];
const W3 = (lon, lat) => { const [x, y] = projM(lon, lat); return [x - CTR[0], y - CTR[1]]; };

async function imagen(src) { const im = new Image(); im.src = src; await im.decode(); return im; }
async function iniciar(sc, paises, flags) {
  SC = sc; CTR = projM(...sc.centro);
  R = new THREE.WebGLRenderer({ canvas: document.getElementById('gl'), antialias: true, preserveDrawingBuffer: true });
  R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap; R.outputColorSpace = THREE.SRGBColorSpace; R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.05;
  ESC = new THREE.Scene(); ESC.background = new THREE.Color(sc.cielo || '#0b3150'); ESC.fog = new THREE.Fog(sc.cielo || '#0b3150', 260, 700);
  CAM = new THREE.PerspectiveCamera(34, R.domElement.width / R.domElement.height, 1, 3000);
  ESC.add(new THREE.HemisphereLight('#cfe9ff', '#123247', 1.1));
  const sol = new THREE.DirectionalLight('#fff1d6', 2.4); sol.position.set(-160, 320, 120); sol.castShadow = true; sol.shadow.mapSize.set(2048, 2048);
  Object.assign(sol.shadow.camera, { left: -220, right: 220, top: 220, bottom: -220, near: 10, far: 900 }); sol.shadow.bias = -.0008; ESC.add(sol); ESC.add(sol.target);
  // mar con ondas suaves (textura dibujada)
  const mc = document.createElement('canvas'); mc.width = mc.height = 512; const m = mc.getContext('2d'); const g = m.createLinearGradient(0, 0, 0, 512); g.addColorStop(0, sc.mar || '#1f7fc0'); g.addColorStop(1, sc.mar2 || '#1a6aa6'); m.fillStyle = g; m.fillRect(0, 0, 512, 512);
  m.strokeStyle = 'rgba(255,255,255,.10)'; m.lineWidth = 3; for (let i = 0; i < 40; i++) { const x = (i * 97) % 512, y = (i * 53) % 512; m.beginPath(); m.arc(x, y, 14, Math.PI * 1.1, Math.PI * 1.9); m.stroke(); m.beginPath(); m.arc(x + 26, y, 14, Math.PI * 1.1, Math.PI * 1.9); m.stroke(); }
  const mt = new THREE.CanvasTexture(mc); mt.wrapS = mt.wrapT = THREE.RepeatWrapping; mt.repeat.set(40, 40); mt.colorSpace = THREE.SRGBColorSpace;
  const mar = new THREE.Mesh(new THREE.PlaneGeometry(3000, 3000), new THREE.MeshStandardMaterial({ map: mt, roughness: .55, metalness: .05 })); mar.rotation.x = -Math.PI / 2; mar.receiveShadow = true; ESC.add(mar); P._mar = mt;
  for (const p of paises) {
    const im = flags[p.iso] ? await imagen(flags[p.iso]) : null, fc = document.createElement('canvas'); fc.width = 640; fc.height = 480; const f = fc.getContext('2d');
    if (im) f.drawImage(im, 0, 0, 640, 480); else { f.fillStyle = '#e3ddce'; f.fillRect(0, 0, 640, 480); }
    const px = f.getImageData(0, 0, 640, 480).data; let r = 0, gg = 0, b = 0, n = 0; for (let i = 0; i < px.length; i += 4 * 97) { r += px[i]; gg += px[i + 1]; b += px[i + 2]; n++; }
    const lado = new THREE.Color(`rgb(${Math.round(r / n * .55)},${Math.round(gg / n * .55)},${Math.round(b / n * .55)})`);
    const shapes = []; let main = null, amax = 0;
    for (const pg of p.polys) { const pts = pg[0].map(([x, y]) => new THREE.Vector2(x - CTR[0], -(y - CTR[1]))); if (pts.length < 4) continue; const sh = new THREE.Shape(pts);
      for (const h of pg.slice(1)) sh.holes.push(new THREE.Path(h.map(([x, y]) => new THREE.Vector2(x - CTR[0], -(y - CTR[1])))));
      const bb = new THREE.Box2().setFromPoints(pts), a = (bb.max.x - bb.min.x) * (bb.max.y - bb.min.y); if (a > amax) { amax = a; main = bb; } if (a > (p.minArea ?? .4)) shapes.push(sh); }
    if (!shapes.length) continue;
    const alto = p.alto ?? 2.4, geo = new THREE.ExtrudeGeometry(shapes, { depth: alto, bevelEnabled: true, bevelThickness: alto * .25, bevelSize: Math.min(.5, alto * .2), bevelSegments: 2, curveSegments: 1 });
    const tex = new THREE.CanvasTexture(fc); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
    const w = main.max.x - main.min.x, h = main.max.y - main.min.y, s = Math.max(w / 4, h / 3) * 1.04, cx = (main.min.x + main.max.x) / 2, cy = (main.min.y + main.max.y) / 2;
    tex.repeat.set(1 / (4 * s), 1 / (3 * s)); tex.offset.set(-(cx - 2 * s) / (4 * s), -(cy - 1.5 * s) / (3 * s));
    const mesh = new THREE.Mesh(geo, [new THREE.MeshStandardMaterial({ map: tex, roughness: .62 }), new THREE.MeshStandardMaterial({ color: lado, roughness: .8 })]);
    mesh.rotation.x = -Math.PI / 2; mesh.castShadow = mesh.receiveShadow = true;
    const [lx, lz] = W3(p.lx + (p.off ? p.off[0] : 0), p.ly + (p.off ? p.off[1] : 0)), grp = new THREE.Group(); grp.position.set(lx, 0, lz); mesh.position.set(-lx, 0, -lz); grp.add(mesh); ESC.add(grp);
    let cara = null; if (p.cara !== false) { const cc = document.createElement('canvas'); cc.width = cc.height = 256; const ct = new THREE.CanvasTexture(cc); ct.colorSpace = THREE.SRGBColorSpace;
      cara = new THREE.Sprite(new THREE.SpriteMaterial({ map: ct, depthTest: false })); const t = p.tamCara || Math.min(26, Math.sqrt(w * h) * .32); cara.scale.set(t, t, 1); cara.position.set(0, alto * 1.3 + t * .18, 0); cara.renderOrder = 5; grp.add(cara); cara.userData = { cc, ct }; }
    if (cara && SC.estiloCara === 'ojos3d') { grp.remove(cara); cara = null; }
    if (cara && SC.estiloCara === 'marca') { cara.scale.multiplyScalar(1.45); cara.position.y *= 1.2; }
    let haz = null; if (cara && SC.estiloCara === 'holo') { const tt = cara.scale.x; cara.position.y += tt * .35; haz = new THREE.Mesh(new THREE.ConeGeometry(tt * .32, cara.position.y, 24, 1, true), new THREE.MeshBasicMaterial({ color: '#5ef2ff', transparent: true, opacity: .2, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide })); haz.position.y = cara.position.y / 2; grp.add(haz); }
    P[p.adm] = { grp, mesh, cara, alto, p, haz, caraY: cara ? cara.position.y : 0, ring: p.polys.reduce((a, b) => (b[0].length > a[0].length ? b : a))[0], colores: [lado, new THREE.Color('#ffffff')], fc };
  }
  if (SC.estiloCara === 'ojos3d') for (const k of Object.keys(P)) { const o = P[k]; if (k.startsWith('_') || o.p.cara === false) continue; const m = new THREE.Box3().setFromObject(o.mesh), tam = o.p.tamCara || Math.min(26, Math.sqrt((m.max.x - m.min.x) * (m.max.z - m.min.z)) * .32); crearOjos3d(o, tam); }
  OV = document.getElementById('ov'); OX = OV.getContext('2d');
}
function ojos3d(k, t) {
  const o = P[k], ex = expr(k, t), blink = ((t + hs(k) * 9) % (3.3 + hs(k + 'b') * 2)) < .12 && ex === 'normal', { ojos, boca, r } = o.ojos;
  const prot = SC.desaparece && P[SC.desaparece.pais]; const objetivo = (prot && k !== SC.desaparece.pais) ? prot.grp.position.clone() : CAM.position.clone();
  for (const e of ojos) { const wp = new THREE.Vector3(); e.globo.getWorldPosition(wp); const hacia = CAM.position.clone().sub(wp).normalize().multiplyScalar(.7).add(objetivo.clone().sub(wp).setY(0).normalize().multiplyScalar(.45)).normalize();
    e.pupila.position.copy(hacia.multiplyScalar(r * .82)); const sy = blink ? .12 : ex === 'shock' ? 1.25 : ex === 'duda' ? .55 : 1; e.grupo.scale.set(ex === 'shock' ? 1.2 : 1, sy, ex === 'shock' ? 1.2 : 1);
    e.parpado.visible = ex === 'duda'; }
  boca.scale.set(ex === 'shock' ? 1 : 1.6, ex === 'shock' ? 1.5 : ex === 'feliz' ? .9 : .35, 1); boca.position.y = o.ojos.by + (ex === 'feliz' ? -.2 : 0);
}
function crearOjos3d(o, tam) {
  const r = tam * .16, blanco = new THREE.MeshStandardMaterial({ color: '#ffffff', roughness: .15, metalness: 0 }), negro = new THREE.MeshStandardMaterial({ color: '#0b0f14', roughness: .3 }), piel = new THREE.MeshStandardMaterial({ color: '#0b0f14', roughness: .5 });
  const raiz = new THREE.Group(); raiz.position.set(0, o.alto * 1.25 + r * .9, 0); o.grp.add(raiz); const ojos = [];
  for (const sx of [-1, 1]) { const grupo = new THREE.Group(); grupo.position.set(sx * r * 1.15, 0, 0); const globo = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 20), blanco); globo.castShadow = true;
    const pupila = new THREE.Mesh(new THREE.SphereGeometry(r * .42, 20, 14), negro); globo.add(pupila); const parpado = new THREE.Mesh(new THREE.SphereGeometry(r * 1.03, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), piel); parpado.visible = false; grupo.add(globo); grupo.add(parpado); raiz.add(grupo); ojos.push({ grupo, globo, pupila, parpado }); }
  const boca = new THREE.Mesh(new THREE.SphereGeometry(r * .35, 20, 12), negro); boca.position.set(0, -r * 1.25, r * .4); raiz.add(boca);
  o.ojos = { ojos, boca, r, by: -r * 1.25 };
}
function expr(adm, t) { const l = (SC.caras || {})[adm] || (SC.caras || {})['*'] || [[0, 'normal']]; let e = 'normal'; for (const [a, x] of l) if (t >= a) e = x; return e; }
function caraHolo(c, ex, t, k, mira) {
  const blink = ((t + hs(k) * 9) % (3.3 + hs(k + 'b') * 2)) < .12 && ex === 'normal', C = '#5ef2ff', px = 13;
  c.save(); c.shadowColor = 'rgba(94,242,255,.9)'; c.shadowBlur = 18; c.fillStyle = 'rgba(6,14,24,.92)'; c.strokeStyle = C; c.lineWidth = 6; c.beginPath(); c.roundRect(18, 52, 220, 150, 26); c.fill(); c.stroke(); c.restore();
  const cel = (x, y) => { c.fillRect(x * px, y * px, px - 2, px - 2); }; c.fillStyle = C; c.shadowColor = C; c.shadowBlur = 10; const ox = Math.round(mira[0] * 1.4), oy = Math.round(mira[1] * 1.2);
  const ojo = (cx) => { const X = cx + ox, Y = 8 + oy;
    if (blink) { for (let i = -1; i <= 1; i++) cel(X + i, Y + 1); return; }
    if (ex === 'feliz') { cel(X - 1, Y + 1); cel(X, Y); cel(X + 1, Y + 1); return; }
    if (ex === 'shock') { for (const [i, j] of [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1], [-1, 2], [0, 2], [1, 2]]) cel(X + i, Y + j - 1); return; }
    if (ex === 'duda' && cx > 9) { for (let i = -1; i <= 1; i++) cel(X + i, Y); return; }
    for (const [i, j] of [[0, 0], [0, 1], [-1, 0], [-1, 1]]) cel(X + i, Y + j); };
  ojo(7); ojo(12);
  if (ex === 'shock') { for (const [i, j] of [[0, 0], [1, 0], [0, 1], [1, 1]]) cel(9 + i, 12 + j); } else if (ex === 'feliz') { for (let i = 0; i < 5; i++) cel(7 + i + .5, 12 + (i === 0 || i === 4 ? 0 : 1)); } else { for (let i = 0; i < 4; i++) cel(8 + i, 13); }
  c.shadowBlur = 0; c.fillStyle = 'rgba(94,242,255,.08)'; for (let y = 56; y < 200; y += 6) c.fillRect(22, y, 212, 2);
}
function caraMarca(c, ex, t, k, mira) {
  const blink = ((t + hs(k) * 9) % (3.3 + hs(k + 'b') * 2)) < .12 && ex === 'normal', Y = '#ffd23f', INK = '#0b0f14', mx = mira[0] * 12, my = mira[1] * 10;
  c.lineJoin = 'round'; c.lineCap = 'round';
  const capsula = (x) => { c.save(); c.translate(x + mx, 112 + my); c.shadowColor = 'rgba(0,0,0,.45)'; c.shadowBlur = 12; c.fillStyle = Y; c.strokeStyle = INK; c.lineWidth = 10;
    if (blink) { c.beginPath(); c.moveTo(-26, 0); c.lineTo(26, 0); c.lineWidth = 16; c.strokeStyle = INK; c.stroke(); c.lineWidth = 9; c.strokeStyle = Y; c.stroke(); }
    else if (ex === 'feliz') { c.beginPath(); c.arc(0, 14, 28, 1.05 * Math.PI, 1.95 * Math.PI); c.lineWidth = 26; c.strokeStyle = INK; c.stroke(); c.lineWidth = 15; c.strokeStyle = Y; c.stroke(); }
    else if (ex === 'shock') { c.beginPath(); c.arc(0, -6, 38, 0, 7); c.fill(); c.stroke(); c.fillStyle = INK; c.beginPath(); c.arc(0, -6, 9, 0, 7); c.fill(); }
    else if (ex === 'duda' && x > 128) { c.beginPath(); c.roundRect(-30, -9, 60, 18, 9); c.fill(); c.stroke(); }
    else { c.beginPath(); c.roundRect(-22, -42, 44, 84, 22); c.fill(); c.stroke(); }
    c.restore(); };
  capsula(84); capsula(172); c.strokeStyle = INK; c.lineWidth = 10; c.fillStyle = INK;
  if (ex === 'shock') { c.beginPath(); c.ellipse(128 + mx * .5, 200, 16, 20, 0, 0, 7); c.fill(); }
  else if (ex === 'feliz') { c.beginPath(); c.arc(128 + mx * .5, 182, 22, .15 * Math.PI, .85 * Math.PI); c.stroke(); }
  else { c.beginPath(); c.moveTo(112 + mx * .5, 196); c.lineTo(144 + mx * .5, 196); c.stroke(); }
}
function dibujaCara(k, t, mira) {
  const o = P[k]; if (o.ojos) return ojos3d(k, t); if (!o.cara) return;
  if (SC.estiloCara === 'holo' || SC.estiloCara === 'marca') { const { cc, ct } = o.cara.userData, c = cc.getContext('2d'); c.clearRect(0, 0, 256, 256); (SC.estiloCara === 'holo' ? caraHolo : caraMarca)(c, expr(k, t), t, k, mira); ct.needsUpdate = true;
    if (o.haz) { o.haz.material.opacity = .18 + .06 * Math.sin(t * 6 + hs(k) * 9); } o.cara.position.y = o.caraY + Math.sin(t * 2.4 + hs(k) * 7) * .6; return; } const { cc, ct } = o.cara.userData, c = cc.getContext('2d'), ex = expr(k, t); c.clearRect(0, 0, 256, 256);
  const parp = ((t + hs(k) * 9) % (3.3 + hs(k + 'b') * 2)) < .12 && ex === 'normal', ojo = (x) => { c.fillStyle = '#fff'; c.strokeStyle = '#15191e'; c.lineWidth = 9; c.beginPath(); c.ellipse(x, 104, ex === 'shock' ? 40 : 34, parp ? 5 : (ex === 'shock' ? 50 : 42), 0, 0, 7); c.fill(); c.stroke();
    if (!parp) { c.fillStyle = '#15191e'; c.beginPath(); c.arc(x + mira[0] * 14, 108 + mira[1] * 14, ex === 'shock' ? 12 : 17, 0, 7); c.fill(); c.fillStyle = '#fff'; c.beginPath(); c.arc(x + mira[0] * 14 - 6, 100 + mira[1] * 14, 5, 0, 7); c.fill(); } };
  c.shadowColor = 'rgba(0,0,0,.35)'; c.shadowBlur = 10; ojo(86); ojo(170); c.shadowBlur = 0; c.strokeStyle = '#15191e'; c.lineWidth = 9; c.lineCap = 'round';
  if (ex === 'shock') { c.fillStyle = '#5a1a1a'; c.beginPath(); c.ellipse(128, 196, 22, 30, 0, 0, 7); c.fill(); c.stroke(); c.beginPath(); c.arc(86, 46, 30, 1.15 * Math.PI, 1.85 * Math.PI); c.stroke(); c.beginPath(); c.arc(170, 46, 30, 1.15 * Math.PI, 1.85 * Math.PI); c.stroke(); }
  else if (ex === 'feliz') { c.fillStyle = '#5a1a1a'; c.beginPath(); c.arc(128, 172, 40, .1 * Math.PI, .9 * Math.PI); c.closePath(); c.fill(); c.stroke(); }
  else if (ex === 'duda') { c.beginPath(); c.moveTo(98, 190); c.lineTo(160, 182); c.stroke(); c.beginPath(); c.moveTo(60, 50); c.lineTo(110, 60); c.stroke(); }
  else { c.beginPath(); c.arc(128, 168, 26, .2 * Math.PI, .8 * Math.PI); c.stroke(); }
  ct.needsUpdate = true;
}
function camara(t) {
  const k = SC.camara; let a = k[0], b = k[0]; for (let i = 0; i < k.length; i++) { if (k[i].t <= t) { a = k[i]; b = k[i + 1] || k[i]; } }
  const u = b === a ? 0 : eio(cl((t - a.t) / (b.t - a.t))), q = x => lerp(a[x], b[x], u), [x, z] = W3(q('lon'), q('lat')), d = q('dist'), inc = q('inclin') * Math.PI / 180;
  CAM.position.set(x, d * Math.cos(inc), z + d * Math.sin(inc)); CAM.lookAt(x, 0, z);
}
function particulas(t, o, t0) {
  if (!o.part) { o.part = []; for (let i = 0; i < 70; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(1.6, .5, 1.1), new THREE.MeshStandardMaterial({ color: ['#1c9b3f', '#f2d21b', '#22409a', '#ffffff'][i % 4] })); m.castShadow = true; ESC.add(m);
      const a = hs('a' + i) * Math.PI * 2, v = 30 + hs('v' + i) * 70; o.part.push({ m, vx: Math.cos(a) * v, vz: Math.sin(a) * v, vy: 40 + hs('y' + i) * 60, r: hs('r' + i) * 10 }); } }
  const dt = t - t0; for (const q of o.part) { const vis = dt > 0 && dt < 2.6; q.m.visible = vis; if (!vis) continue; q.m.position.set(o.grp.position.x + q.vx * dt, Math.max(.3, q.vy * dt - 45 * dt * dt), o.grp.position.z + q.vz * dt); q.m.rotation.set(q.r * dt, q.r * dt * .7, 0); }
}
function texto(t) {
  const W = OV.width, H = OV.height; OX.clearRect(0, 0, W, H);
  for (const e of SC.textos || []) { if (t < e.desde || t > e.hasta) continue; const a = cl(Math.min((t - e.desde) / .25, (e.hasta - t) / .25)), p = eob(pr(t, e.desde, .45)); OX.save(); OX.globalAlpha = a; OX.translate(W / 2, e.y); OX.scale(p, p); OX.textAlign = 'center'; OX.textBaseline = 'middle'; OX.lineJoin = 'round';
    if (e.tipo === 'pregunta') { OX.font = '700 54px Barlow'; const w = OX.measureText(e.texto).width + 70; OX.fillStyle = '#ffd23f'; OX.beginPath(); OX.roundRect(-w / 2, -44, w, 88, 44); OX.fill(); OX.fillStyle = '#0b0f14'; OX.fillText(e.texto, 0, 4); OX.restore(); continue; }
    let txt = e.texto; if (e.num) { const q = eo(pr(t, e.desde + .1, 1)); txt = Math.round(e.num[0] + (e.num[1] - e.num[0]) * q).toLocaleString('en-US') + (e.suf || ''); }
    const lines = txt.split('\n'), sz = e.tam || 110; OX.font = `${sz}px Anton`; OX.letterSpacing = '2px';
    lines.forEach((ln, i) => { const yy = (i - (lines.length - 1) / 2) * sz * 1.15, parts = ln.split('*'); let tot = 0; parts.forEach(s => tot += OX.measureText(s).width); let x = -tot / 2;
      parts.forEach((s, j) => { OX.textAlign = 'left'; OX.strokeStyle = '#0b0f14'; OX.lineWidth = sz * .16; OX.strokeText(s, x, yy); OX.fillStyle = j % 2 ? '#ffd23f' : '#fff'; OX.fillText(s, x, yy); x += OX.measureText(s).width; }); });
    if (e.sub) { OX.font = '700 44px Barlow'; OX.textAlign = 'center'; OX.strokeStyle = '#0b0f14'; OX.lineWidth = 8; OX.strokeText(e.sub, 0, lines.length * sz * .62 + 20); OX.fillStyle = '#fff'; OX.fillText(e.sub, 0, lines.length * sz * .62 + 20); }
    OX.restore(); }
}
function cuadro(t) {
  camara(t); P._mar.offset.set(t * .01, t * .006);
  const prot = SC.desaparece; let vx = 0, vz = 0; if (prot && P[prot.pais]) { vx = P[prot.pais].grp.position.x; vz = P[prot.pais].grp.position.z; }
  CAM.updateMatrixWorld(); const pv = new THREE.Vector3(vx, 0, vz).project(CAM);
  for (const k of Object.keys(P)) { if (k.startsWith('_')) continue; const o = P[k]; o.grp.position.y = Math.sin(t * 2 + hs(k) * 6) * .25; o.grp.rotation.set(0, 0, 0); o.grp.scale.set(1, 1, 1); o.grp.visible = true;
    const pp = o.grp.position.clone().project(CAM); let mira = [pv.x - pp.x, -(pv.y - pp.y)]; const n = Math.hypot(...mira) || 1; mira = k === (prot && prot.pais) ? [0, 0] : [mira[0] / n, mira[1] / n]; dibujaCara(k, t, mira); }
  if (prot && P[prot.pais]) { const o = P[prot.pais], dt = t - prot.t;
    if (dt > 0) { if (dt < .5) { o.grp.position.x += Math.sin(t * 80) * .8; }
      else { const up = eo(pr(dt, .5, .55)), fall = eio(pr(dt, 1.05, .7)); o.grp.position.y = up * 22 - fall * 70; o.grp.rotation.z = Math.sin(dt * 6) * .08 * up; o.grp.rotation.x = fall * .6; const s = 1 - fall * .5; o.grp.scale.set(s, s, s); if (dt > 1.75) o.grp.visible = false; }
      if (dt > 1.6) { CAM.position.x += Math.sin(t * 60) * cl(1 - (dt - 1.6) / .6) * 2.5; CAM.position.y += Math.cos(t * 53) * cl(1 - (dt - 1.6) / .6) * 2; } }
    particulas(t, o, prot.t + 1.6);
    if (!FANT) { const pts = o.ring.map(([x, y]) => new THREE.Vector3(x - CTR[0], .35, y - CTR[1])); const g = new THREE.BufferGeometry().setFromPoints(pts); FANT = new THREE.Line(g, new THREE.LineDashedMaterial({ color: '#ffffff', dashSize: 2, gapSize: 1.5, transparent: true })); FANT.computeLineDistances(); ESC.add(FANT); }
    FANT.material.opacity = cl((dt - 1.7) / .5) * .9; FANT.visible = dt > 1.7; }
  R.render(ESC, CAM); texto(t);
}
