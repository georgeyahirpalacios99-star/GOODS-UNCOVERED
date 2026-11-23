// Página del motor 3D (la carga render3d.cjs). Usa three.js.
let R, SC, CAM, ESC, OV, OX, P = {}, CTR, PART = [], FANT = null;
const lerp = (a, b, p) => a + (b - a) * p, cl = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v)), pr = (t, a, d) => cl((t - a) / d);
const eio = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2, eo = p => 1 - Math.pow(1 - p, 3), eob = p => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); };
const hs = s => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) % 9973; return h / 9973; };
const projM = (lon, lat) => [(lon + 180) / 360 * 1000, (1 - Math.log(Math.tan(Math.PI / 4 + lat * Math.PI / 360)) / Math.PI) / 2 * 1000];
const W3 = (lon, lat) => { const [x, y] = projM(lon, lat); return [x - CTR[0], y - CTR[1]]; };

async function imagen(src) { const im = new Image(); im.src = src; await im.decode(); return im; }
let IMGS = {}, FLAGIM = {};
async function iniciar(sc, paises, flags, imgs) {
  for (const [k, v] of Object.entries(imgs || {})) IMGS[k] = await imagen(v); for (const [k, v] of Object.entries(flags)) FLAGIM[k] = await imagen(v);
  SC = sc; CTR = projM(...sc.centro);
  R = new THREE.WebGLRenderer({ canvas: document.getElementById('gl'), antialias: true, preserveDrawingBuffer: true });
  R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap; R.outputColorSpace = THREE.SRGBColorSpace; R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.05;
  ESC = new THREE.Scene(); ESC.background = new THREE.Color(sc.cielo || '#0b3150'); ESC.fog = new THREE.Fog(sc.cielo || '#0b3150', 260, 700);
  CAM = new THREE.PerspectiveCamera(34, R.domElement.width / R.domElement.height, 8, 2600);
  ESC.add(new THREE.HemisphereLight('#cfe9ff', '#123247', 1.1));
  const sol = new THREE.DirectionalLight('#fff1d6', 2.4); sol.position.set(-160, 320, 120); sol.castShadow = true; sol.shadow.mapSize.set(SC.sombra || 2048, SC.sombra || 2048);
  Object.assign(sol.shadow.camera, { left: -220, right: 220, top: 220, bottom: -220, near: 10, far: 900 }); sol.shadow.bias = -.0004; sol.shadow.normalBias = .6; ESC.add(sol); ESC.add(sol.target);
  // mar con ondas suaves (textura dibujada)
  const mc = document.createElement('canvas'); mc.width = mc.height = 512; const m = mc.getContext('2d'); m.fillStyle = sc.mar || '#1f7fc0'; m.fillRect(0, 0, 512, 512);
  m.strokeStyle = 'rgba(255,255,255,.045)'; m.lineWidth = 2; for (let i = 0; i < 40; i++) { const x = hs('x' + i) * 512, y = hs('y' + i) * 512; m.beginPath(); m.arc(x, y, 14, Math.PI * 1.1, Math.PI * 1.9); m.stroke(); m.beginPath(); m.arc(x + 26, y, 14, Math.PI * 1.1, Math.PI * 1.9); m.stroke(); }
  const mt = IMGS['tex:T01'] ? new THREE.Texture(IMGS['tex:T01']) : new THREE.CanvasTexture(mc); mt.needsUpdate = true; mt.wrapS = mt.wrapT = THREE.RepeatWrapping; mt.repeat.set(IMGS['tex:T01'] ? 26 : 70, IMGS['tex:T01'] ? 26 : 70); mt.colorSpace = THREE.SRGBColorSpace;
  const mar = new THREE.Mesh(new THREE.PlaneGeometry(3000, 3000), new THREE.MeshStandardMaterial({ map: mt, roughness: .55, metalness: .05 })); mar.rotation.x = -Math.PI / 2; mar.receiveShadow = true; ESC.add(mar); P._mar = mt; P._marMesh = mar;
  for (const p of paises) {
    const im = flags[p.iso] ? await imagen(flags[p.iso]) : null, fc = document.createElement('canvas'); fc.width = 640; fc.height = 480; const f = fc.getContext('2d');
    if (im) f.drawImage(im, 0, 0, 640, 480); else { f.fillStyle = p.neutro ? (SC.tierra || '#4a5d4a') : '#e3ddce'; f.fillRect(0, 0, 640, 480); if (p.neutro && IMGS['tex:T04']) { const pt = f.createPattern(IMGS['tex:T04'], 'repeat'); f.fillStyle = pt; f.fillRect(0, 0, 640, 480); f.fillStyle = 'rgba(10,20,12,.25)'; f.fillRect(0, 0, 640, 480); } else if (p.neutro) for (let i = 0; i < 2600; i++) { f.fillStyle = `rgba(${hs('r' + i) > .5 ? '255,240,210' : '20,30,20'},${.05 + hs('a' + i) * .08})`; f.fillRect(hs('x' + i) * 640, hs('y' + i) * 480, 3 + hs('s' + i) * 9, 3 + hs('t' + i) * 9); } }
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
  entorno(paises); if (SC.estadio) estadio();
  for (const c of SC.columnas || []) { const o = P[c.pais]; if (!o) continue; const m = new THREE.Mesh(new THREE.CylinderGeometry(c.radio || 5, c.radio || 5, 1, 40), new THREE.MeshStandardMaterial({ color: c.color || '#ffd23f', metalness: .55, roughness: .25, emissive: c.color || '#ffd23f', emissiveIntensity: .12 })); m.castShadow = true; ESC.add(m); c._m = m; }
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
  const parp = ((t + hs(k) * 9) % (3.3 + hs(k + 'b') * 2)) < .12 && ex === 'normal', ojo = (x) => { const rx = ex === 'shock' ? 40 : 34, ry = parp ? 5 : (ex === 'shock' ? 50 : 42); c.save(); c.shadowColor = 'rgba(0,0,0,.5)'; c.shadowBlur = 14; c.shadowOffsetY = 7; const gw = c.createRadialGradient(x - rx * .35, 104 - ry * .4, 4, x, 104, Math.max(rx, ry) * 1.15); gw.addColorStop(0, '#ffffff'); gw.addColorStop(.65, '#f1f3f5'); gw.addColorStop(1, '#b9c2cc'); c.fillStyle = gw; c.strokeStyle = '#15191e'; c.lineWidth = 9; c.beginPath(); c.ellipse(x, 104, rx, ry, 0, 0, 7); c.fill(); c.restore(); c.strokeStyle = '#15191e'; c.lineWidth = 9; c.stroke();
    if (!parp) { const px = x + mira[0] * 14, py = 108 + mira[1] * 14, pr0 = ex === 'shock' ? 12 : 17, gp = c.createRadialGradient(px - pr0 * .3, py - pr0 * .3, 1, px, py, pr0); gp.addColorStop(0, '#3a4048'); gp.addColorStop(1, '#0b0e12'); c.fillStyle = gp; c.beginPath(); c.arc(px, py, pr0, 0, 7); c.fill(); c.fillStyle = 'rgba(255,255,255,.95)'; c.beginPath(); c.arc(px - pr0 * .38, py - pr0 * .42, pr0 * .32, 0, 7); c.fill(); c.fillStyle = 'rgba(255,255,255,.6)'; c.beginPath(); c.arc(px + pr0 * .35, py + pr0 * .3, pr0 * .14, 0, 7); c.fill(); }
    if (!parp) { c.fillStyle = 'rgba(255,255,255,.55)'; c.beginPath(); c.ellipse(x - rx * .45, 104 - ry * .55, rx * .22, ry * .12, -.5, 0, 7); c.fill(); } };
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
  if (ESC.fog && !ESC.userData.fijaNiebla) { ESC.fog.near = d * 1.1; ESC.fog.far = d * 2.6; }
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
  camara(t); P._mar.offset.set(t * .01, t * .006); animaEntorno(t);
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
  for (const e of SC.elevar || []) { const o = P[e.pais]; if (!o || t < e.desde) continue; const q = eo(pr(t, e.desde, .8)) * (1 - eio(pr(t, e.hasta ?? 1e9, .8))); o.grp.position.y += q * (e.altura || 8); o.grp.rotation.z += Math.sin(t * 1.6 + hs(e.pais)) * .02 * q; }
  for (const k of Object.keys(P)) { if (k.startsWith('_')) continue; let f = 1; for (const a of SC.atenuar || []) { if (a.paises.includes(k)) continue; const q = pr(t, a.desde, .6) * (1 - pr(t, a.hasta, .6)); f = Math.min(f, 1 - .6 * q); } P[k].mesh.material[0].color.setScalar(f); P[k].mesh.material[1].color.multiplyScalar(1); }
  for (const c of SC.columnas || []) { if (!c._m) continue; const o = P[c.pais], q = eo(pr(t, c.desde, c.dur || 1.2)) * (1 - pr(t, c.hasta ?? 1e9, .4)), h = Math.max(.01, q * (c.alto || 40)); c._m.visible = t >= c.desde && q > .01; c._m.scale.y = h; c._m.position.set(o.grp.position.x + (c.dx || 0), o.alto * 1.3 + h / 2, o.grp.position.z + (c.dz || 0)); c._top = new THREE.Vector3(c._m.position.x, o.alto * 1.3 + h + 3, c._m.position.z); c._q = q; }
  if (SC.estadio) animaEstadio(t);
  const varOn = (SC.capas || []).some(e => e.tipo === 'var' && t >= e.desde && t <= e.hasta); R.domElement.style.filter = varOn ? 'grayscale(1) contrast(1.15)' : 'none';
  const tapado = (SC.capas || []).some(e => e.tipo === 'foto' && t > e.desde + .35 && t < e.hasta - .35);
  if (!tapado) R.render(ESC, CAM); texto(t); capas2d(t); reloj(t);
}

// ---------- capas 2D encima del 3D (mismo lenguaje visual del video de Sinaloa) ----------
const ACC = '#ffd23f';
function aPantalla(v) { const p = v.clone().project(CAM); return [(p.x + 1) / 2 * OV.width, (1 - p.y) / 2 * OV.height]; }
function puntoGeo(lon, lat, y = 4) { const [x, z] = W3(lon, lat); return new THREE.Vector3(x, y, z); }
function rr(x, y, w, h, r, fill) { OX.beginPath(); OX.roundRect(x, y, w, h, r); OX.fillStyle = fill; OX.fill(); }
function txt(s, x, y, f, col, al = 'left', borde) { OX.font = f; OX.textAlign = al; OX.textBaseline = 'middle'; if (borde) { OX.lineJoin = 'round'; OX.strokeStyle = borde; OX.lineWidth = 7; OX.strokeText(s, x, y); } OX.fillStyle = col; OX.fillText(s, x, y); }
function capas2d(t) {
  const W = OV.width, H = OV.height;
  for (const e of SC.capas || []) { if (t < e.desde - .01 || t > e.hasta + .01) continue; const a = e.sinFundido ? 1 : cl(Math.min((t - e.desde) / .3, (e.hasta - t) / .3)), p = eo(pr(t, e.desde, .55)); OX.save(); OX.globalAlpha = a;
    if (e.tipo === 'tarjeta') { const im = IMGS[e.img]; const w = e.w || 560, h = e.h || Math.round(w * .62), cx = e.x ?? W / 2, cy = e.y ?? H * .3;
      if (e.lon !== undefined) { const [px, py] = aPantalla(puntoGeo(e.lon, e.lat)); OX.strokeStyle = 'rgba(255,255,255,.9)'; OX.lineWidth = 3; OX.setLineDash([9, 8]); OX.beginPath(); OX.moveTo(px, py); OX.lineTo(lerp(px, cx, p), lerp(py, cy + h / 2, p)); OX.stroke(); OX.setLineDash([]); OX.fillStyle = ACC; OX.beginPath(); OX.arc(px, py, 9, 0, 7); OX.fill(); OX.globalAlpha = a * (.5 + .5 * Math.sin(t * 5)); OX.beginPath(); OX.arc(px, py, 18, 0, 7); OX.strokeStyle = ACC; OX.stroke(); OX.globalAlpha = a; }
      OX.translate(cx, cy + (1 - p) * 50); OX.rotate((e.rot || 0) * Math.PI / 180); OX.shadowColor = 'rgba(0,0,0,.6)'; OX.shadowBlur = 40; OX.shadowOffsetY = 16; rr(-w / 2 - 8, -h / 2 - 8, w + 16, h + 86, 14, 'rgba(9,16,22,.94)'); OX.shadowColor = 'transparent';
      if (im) { OX.save(); OX.beginPath(); OX.roundRect(-w / 2, -h / 2, w, h, 8); OX.clip(); const q = pr(t, e.desde, e.hasta - e.desde), z = 1.05 + .1 * q, s = Math.max(w / im.width, h / im.height) * z; OX.drawImage(im, -im.width * s / 2 + (q - .5) * 40 * (e.px ?? 1), -im.height * s / 2, im.width * s, im.height * s); OX.restore(); }
      OX.fillStyle = ACC; OX.fillRect(-w / 2, h / 2 + 18, 6, 52); OX.letterSpacing = '3px'; txt((e.texto || '').toUpperCase(), -w / 2 + 22, h / 2 + 34, '700 34px Barlow', '#fff'); OX.letterSpacing = '2px'; txt((e.credito || '').toUpperCase(), -w / 2 + 22, h / 2 + 64, '700 19px Barlow', 'rgba(255,255,255,.6)'); }
    else if (e.tipo === 'marcador') { const y = e.y ?? 330, w = W - 120; OX.translate(W / 2, y + (1 - p) * -60); OX.shadowColor = 'rgba(0,0,0,.6)'; OX.shadowBlur = 30; rr(-w / 2, -120, w, 240, 28, 'rgba(8,14,20,.92)'); OX.shadowBlur = 0;
      OX.letterSpacing = '10px'; txt((e.titulo || '').toUpperCase(), 0, -86, '700 30px Barlow', ACC, 'center'); OX.letterSpacing = '0px';
      const q = eo(pr(t, e.desde + .2, SC.ritmo === 'rapido' ? .55 : 1.1)); for (const [lado, iso, val, nom] of [[-1, e.isoIzq, e.izq, e.nomIzq], [1, e.isoDer, e.der, e.nomDer]]) { const fx = lado * (w / 2 - 110), fl = FLAGIM[iso]; OX.save(); OX.beginPath(); OX.arc(fx, 10, 62, 0, 7); OX.clip(); if (fl) OX.drawImage(fl, fx - 83, 10 - 62, 166, 124); OX.restore(); OX.lineWidth = 6; OX.strokeStyle = '#fff'; OX.beginPath(); OX.arc(fx, 10, 62, 0, 7); OX.stroke();
        txt((nom || '').toUpperCase(), fx, 96, '700 26px Barlow', '#fff', 'center'); const gana = e.gana ? (e.gana === 'izq') === (lado < 0) : (e.izq !== e.der && ((lado < 0) === (e.izq > e.der))); const v = typeof val === 'number' ? Math.round(val * q).toLocaleString('en-US') : val;
        OX.save(); if (gana && q > .98) { OX.shadowColor = ACC; OX.shadowBlur = 30; } txt(v + (e.suf || ''), lado * (w / 2 - (typeof val === 'number' ? 300 : 420)), 14, `${e.tam || 130}px Anton`, gana && q > .98 ? ACC : '#fff', 'center'); OX.restore(); }
      txt('VS', 0, 14, '60px Anton', 'rgba(255,255,255,.35)', 'center'); }
    else if (e.tipo === 'ficha') { const x = 70, y = e.y ?? H - 420, g = OX.createLinearGradient(0, y - 120, 0, H); g.addColorStop(0, 'rgba(3,9,14,0)'); g.addColorStop(1, 'rgba(3,9,14,.75)'); OX.fillStyle = g; OX.fillRect(0, y - 120, W, H - y + 120);
      OX.fillStyle = ACC; OX.fillRect(x, y, 8, 150 * p); OX.letterSpacing = '8px'; txt((e.kicker || '').toUpperCase(), x + 32 - (1 - p) * 60, y + 22, '700 28px Barlow', ACC); OX.letterSpacing = '2px'; txt((e.texto || '').toUpperCase(), x + 30 - (1 - p) * 60, y + 84, `${e.tam || 78}px Anton`, '#fff'); if (e.sub) { OX.letterSpacing = '1px'; txt(e.sub, x + 32 - (1 - p) * 60, y + 144, '700 32px Barlow', 'rgba(235,240,242,.9)'); } }
    else if (e.tipo === 'foto') { const im = IMGS[e.img]; if (im) { const q = pr(t, e.desde, e.hasta - e.desde), z = (e.z0 || 1.03) + ((e.z1 || 1.14) - (e.z0 || 1.03)) * q, s = Math.max(W / im.width, H / im.height) * z; OX.drawImage(im, (W - im.width * s) / 2 + (q - .5) * 60 * (e.px ?? 0), (H - im.height * s) / 2, im.width * s, im.height * s);
        const vg = OX.createRadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1300); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,.6)'); OX.fillStyle = vg; OX.fillRect(0, 0, W, H); OX.letterSpacing = '3px'; txt((e.credito || '').toUpperCase(), W - 40, H - 40, '700 20px Barlow', 'rgba(255,255,255,.7)', 'right'); } }
    else if (e.tipo === 'barrido') { const u = eio(pr(t, e.desde, e.hasta - e.desde)), x = lerp(-W * .6, W * 1.6, u), sk = 420; OX.globalAlpha = 1; OX.fillStyle = '#0a1218'; OX.beginPath(); OX.moveTo(x - W, 0); OX.lineTo(x + sk, 0); OX.lineTo(x, H); OX.lineTo(x - W - sk, H); OX.closePath(); OX.fill(); OX.fillStyle = ACC; OX.beginPath(); OX.moveTo(x + sk, 0); OX.lineTo(x + sk + 34, 0); OX.lineTo(x + 34, H); OX.lineTo(x, H); OX.closePath(); OX.fill(); }
    else if (e.tipo === 'var') { OX.strokeStyle = 'rgba(255,255,255,.85)'; OX.lineWidth = 6; OX.strokeRect(60, 60, W - 120, H - 120); OX.fillStyle = 'rgba(255,255,255,.04)'; for (let y = 0; y < H; y += 6) OX.fillRect(0, y, W, 2);
      rr(W / 2 - 230, 90, 460, 90, 10, '#0b0f14'); txt('VAR · ' + (e.texto || 'REVISIÓN').toUpperCase(), W / 2, 136, '52px Anton', '#fff', 'center'); OX.globalAlpha = a * (.5 + .5 * Math.sin(t * 8)); OX.fillStyle = '#e0262b'; OX.beginPath(); OX.arc(W / 2 - 200, 136, 12, 0, 7); OX.fill(); OX.globalAlpha = a;
      if (e.veredicto && t > e.desde + (e.hasta - e.desde) * .55) { const k = eob(pr(t, e.desde + (e.hasta - e.desde) * .55, .4)); OX.save(); OX.translate(W / 2, H / 2 + 260); OX.scale(k, k); OX.font = '72px Anton'; const vw = OX.measureText(e.veredicto.toUpperCase()).width + 80; rr(-vw / 2, -60, vw, 120, 16, e.ok ? '#2a8f3c' : '#e0262b'); txt(e.veredicto.toUpperCase(), 0, 4, '72px Anton', '#fff', 'center'); OX.restore(); } }
    else if (e.tipo === 'adelanto') { const k = eob(pr(t, e.desde, .5)); OX.translate(W / 2, e.y ?? 880); OX.scale(k, k); rr(-470, -70, 940, 140, 20, 'rgba(8,12,18,.93)'); rr(-470, -70, 160, 140, 20, '#ffd23f'); txt(e.minuto || "45'", -390, 4, '64px Anton', '#0b0f14', 'center'); OX.letterSpacing = '4px'; txt((e.kicker || 'MÁS ADELANTE').toUpperCase(), -280, -26, '700 26px Barlow', '#ffd23f'); OX.letterSpacing = '1px'; txt(e.texto || '', -280, 22, '46px Anton', '#fff'); }
    else if (e.tipo === 'columnaTexto') { const c = (SC.columnas || [])[e.col]; if (c && c._top && c._q > .05) { const [sx, sy] = aPantalla(c._top); txt(Math.round((e.valor || 0) * c._q) + (e.suf || ''), sx, sy - 30, '90px Anton', '#fff', 'center', '#0b0f14'); txt((e.texto || '').toUpperCase(), sx, sy + 26, '700 30px Barlow', ACC, 'center', '#0b0f14'); } }
    OX.restore(); }
}

// ---------- entornos: lo que rodea al mapa (mundo vivo, cancha, órbita) ----------
let NUBES = [], BARCOS = [], AVIONES = [];
function entorno(paises) {
  const E = SC.entorno || 'simple'; if (E === 'simple') return;
  const R0 = 1400, cv = document.createElement('canvas'); cv.width = cv.height = 4096; const g = cv.getContext('2d'), k = 4096 / (2 * R0), X = x => (x + R0) * k, Z = z => (z + R0) * k;
  if (E === 'cancha') {
    for (let i = 0; i < 40; i++) { g.fillStyle = i % 2 ? '#2f7a34' : '#357f39'; g.fillRect(i * 4096 / 40, 0, 4096 / 40 + 1, 4096); }
    for (let i = 0; i < 30000; i++) { g.fillStyle = `rgba(${hs('g' + i) > .5 ? '20,60,20' : '120,180,90'},.12)`; g.fillRect(hs('x' + i) * 4096, hs('y' + i) * 4096, 2, 7); }
    g.strokeStyle = 'rgba(255,255,255,.85)'; g.lineWidth = 14; const cx = 2048, cy = 2048, L = 1150, A = 740; g.lineWidth = 7; g.strokeRect(cx - L / 2, cy - A / 2, L, A); g.beginPath(); g.moveTo(cx, cy - A / 2); g.lineTo(cx, cy + A / 2); g.stroke(); g.beginPath(); g.arc(cx, cy, 130, 0, 7); g.stroke();
    for (const s of [-1, 1]) { g.strokeRect(cx + s * L / 2 - (s > 0 ? 190 : 0), cy - 240, 190, 480); g.strokeRect(cx + s * L / 2 - (s > 0 ? 70 : 0), cy - 110, 70, 220); g.beginPath(); g.arc(cx + s * (L / 2 - 135), cy, 7, 0, 7); g.fillStyle = '#fff'; g.fill(); }
    g.beginPath(); g.arc(cx, cy, 8, 0, 7); g.fill();
  } else {
    g.fillStyle = SC.mar || '#0d2a4f'; g.fillRect(0, 0, 4096, 4096); if (IMGS['tex:T01']) { const pt = g.createPattern(IMGS['tex:T01'], 'repeat'); g.save(); g.scale(.35, .35); g.fillStyle = pt; g.globalAlpha = .9; g.fillRect(0, 0, 4096 / .35, 4096 / .35); g.restore(); }
    const prof = g.createRadialGradient(2048, 2048, 200, 2048, 2048, 2600); prof.addColorStop(0, 'rgba(30,80,130,.35)'); prof.addColorStop(1, 'rgba(0,0,0,.35)'); g.fillStyle = prof; g.fillRect(0, 0, 4096, 4096);
    g.strokeStyle = 'rgba(140,200,255,.13)'; g.lineWidth = 3; for (let lo = -180; lo <= 180; lo += 10) { const [x] = W3(lo, 0); g.beginPath(); g.moveTo(X(x), 0); g.lineTo(X(x), 4096); g.stroke(); }
    for (let la = -70; la <= 70; la += 10) { const [, z] = W3(0, la); g.beginPath(); g.moveTo(0, Z(z)); g.lineTo(4096, Z(z)); g.stroke(); }
    { const [, z] = W3(0, 0); g.strokeStyle = 'rgba(255,210,63,.25)'; g.setLineDash([30, 22]); g.lineWidth = 4; g.beginPath(); g.moveTo(0, Z(z)); g.lineTo(4096, Z(z)); g.stroke(); g.setLineDash([]); }
    g.save(); g.shadowColor = 'rgba(80,200,230,.9)'; g.shadowBlur = 70; g.fillStyle = 'rgba(60,160,200,.55)';
    for (const p of paises) for (const pg of p.polys) { g.beginPath(); pg[0].forEach(([x, y], i) => { const xx = X(x - CTR[0]), zz = Z(y - CTR[1]); i ? g.lineTo(xx, zz) : g.moveTo(xx, zz); }); g.closePath(); g.fill(); g.fill(); }
    g.restore(); g.fillStyle = 'rgba(190,225,255,.22)'; g.textAlign = 'center'; g.font = '700 30px Barlow'; g.letterSpacing = '12px';
    for (const [lo, la, n] of SC.oceanos || [[-100, -18, 'OCÉANO PACÍFICO'], [-22, -18, 'OCÉANO ATLÁNTICO'], [-75, 14.5, 'MAR CARIBE']]) { const [x, z] = W3(lo, la); g.fillText(n, X(x), Z(z)); }
  }
  const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  const pl = new THREE.Mesh(new THREE.PlaneGeometry(2 * R0, 2 * R0), new THREE.MeshStandardMaterial({ map: tx, roughness: E === 'cancha' ? .95 : .5, metalness: .05 })); pl.rotation.x = -Math.PI / 2; pl.position.y = .3; pl.receiveShadow = true; pl.material.polygonOffset = true; pl.material.polygonOffsetFactor = 1; pl.material.polygonOffsetUnits = 1; ESC.add(pl); P._fondo = pl;
  if (E === 'cancha') { // estadio alrededor: gradas con público y reflectores
    const gc = document.createElement('canvas'); gc.width = 4096; gc.height = 512; const q = gc.getContext('2d'); q.fillStyle = '#10151c'; q.fillRect(0, 0, 4096, 512);
    for (let i = 0; i < 26000; i++) { const y = hs('cy' + i) * 470 + 30; q.fillStyle = ['#d9d9d9', '#74acdf', '#f7e35c', '#2a8f3c', '#c0392b', '#ffffff', '#1f2a36'][Math.floor(hs('cc' + i) * 7)]; q.globalAlpha = .55 + hs('ca' + i) * .45; q.fillRect(hs('cx' + i) * 4096, y, 4, 5); }
    q.globalAlpha = 1; for (let i = 0; i < 24; i++) { const x = i * 4096 / 24 + 80; q.fillStyle = 'rgba(255,255,230,.9)'; q.shadowColor = '#fff'; q.shadowBlur = 30; q.fillRect(x, 6, 70, 18); q.shadowBlur = 0; }
    const tg = new THREE.CanvasTexture(gc); tg.colorSpace = THREE.SRGBColorSpace; tg.wrapS = THREE.RepeatWrapping; tg.repeat.set(3, 1);
    const ring = new THREE.Mesh(new THREE.CylinderGeometry(560, 470, 170, 80, 1, true), new THREE.MeshBasicMaterial({ map: tg, side: THREE.BackSide })); ring.position.y = 70; ESC.add(ring); ESC.background = new THREE.Color('#070b12'); ESC.userData.fijaNiebla = true; ESC.fog = new THREE.Fog('#0b1220', 700, 1800);
  }
  if (E === 'orbita') { const bc = document.createElement('canvas'); bc.width = 4; bc.height = 512; const q = bc.getContext('2d'), gr = q.createLinearGradient(0, 0, 0, 512); gr.addColorStop(0, '#000208'); gr.addColorStop(.55, '#04122a'); gr.addColorStop(.8, '#1d6fb0'); gr.addColorStop(1, '#8fd6ff'); q.fillStyle = gr; q.fillRect(0, 0, 4, 512); const bt = new THREE.CanvasTexture(bc); bt.colorSpace = THREE.SRGBColorSpace; ESC.background = bt; ESC.userData.fijaNiebla = true; ESC.fog = new THREE.Fog('#4f93c8', 380, 1100); }
  // nubes con sombra
  let nubeAlfa = null; if (IMGS['tex:T06']) { const c0 = document.createElement('canvas'); c0.width = c0.height = 1024; const q0 = c0.getContext('2d'); q0.drawImage(IMGS['tex:T06'], 0, 0, 1024, 1024); const d0 = q0.getImageData(0, 0, 1024, 1024); for (let k = 0; k < d0.data.length; k += 4) { const l = (d0.data[k] + d0.data[k + 1] + d0.data[k + 2]) / 3; d0.data[k + 3] = Math.min(255, Math.max(0, (l - 25) * 1.6)); } q0.putImageData(d0, 0, 0); nubeAlfa = c0; }
  for (let i = 0; i < (SC.nubes ?? 14); i++) { const nc = document.createElement('canvas'); nc.width = nc.height = 256; const q = nc.getContext('2d'); if (nubeAlfa) { const sx = Math.floor(hs('nqx' + i) * 3) * 341, sy = Math.floor(hs('nqy' + i) * 3) * 341; q.drawImage(nubeAlfa, sx, sy, 341, 341, 0, 0, 256, 256); q.globalCompositeOperation = 'destination-in'; const mk = q.createRadialGradient(128, 128, 60, 128, 128, 128); mk.addColorStop(0, 'rgba(0,0,0,1)'); mk.addColorStop(1, 'rgba(0,0,0,0)'); q.fillStyle = mk; q.fillRect(0, 0, 256, 256); q.globalCompositeOperation = 'source-over'; } else for (let j = 0; j < 9; j++) { const gx = 128 + (hs('nx' + i + j) - .5) * 120, gy = 128 + (hs('ny' + i + j) - .5) * 60, rr = 40 + hs('nr' + i + j) * 50, gg = q.createRadialGradient(gx, gy, 0, gx, gy, rr); gg.addColorStop(0, 'rgba(255,255,255,.75)'); gg.addColorStop(1, 'rgba(255,255,255,0)'); q.fillStyle = gg; q.beginPath(); q.arc(gx, gy, rr, 0, 7); q.fill(); }
    const tx2 = new THREE.CanvasTexture(nc), m = new THREE.Mesh(new THREE.PlaneGeometry(70, 70), new THREE.MeshBasicMaterial({ map: tx2, transparent: true, opacity: E === 'cancha' ? 0 : .55, depthWrite: false })); m.rotation.x = -Math.PI / 2; const sh = new THREE.Mesh(new THREE.PlaneGeometry(70, 70), new THREE.MeshBasicMaterial({ map: tx2, transparent: true, opacity: .07, color: '#000000', depthWrite: false })); sh.rotation.x = -Math.PI / 2;
    ESC.add(m); ESC.add(sh); NUBES.push({ m, sh, x: (hs('nx' + i) - .5) * 900, z: (hs('nz' + i) - .5) * 700, v: 3 + hs('nv' + i) * 4 }); if (E === 'cancha') { m.visible = sh.visible = false; } }
  // barcos con estela
  for (let i = 0; i < (E === 'cancha' ? 0 : (SC.barcos ?? 6)); i++) { const b = new THREE.Group(), cas = new THREE.Mesh(new THREE.BoxGeometry(6, 1.6, 2), new THREE.MeshStandardMaterial({ color: '#e8e2d4' })), cab = new THREE.Mesh(new THREE.BoxGeometry(2, 1.6, 1.6), new THREE.MeshStandardMaterial({ color: '#c0392b' }));
    cab.position.set(-1.2, 1.4, 0); cas.castShadow = true; b.add(cas); b.add(cab); const es = new THREE.Mesh(new THREE.PlaneGeometry(26, 2.4), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: .25, depthWrite: false })); es.rotation.x = -Math.PI / 2; es.position.set(-16, -.7, 0); b.add(es); ESC.add(b);
    const [x0, z0] = SC.rutasBarco && SC.rutasBarco[i] ? W3(...SC.rutasBarco[i]) : [(hs('bx' + i) - .3) * 600, (hs('bz' + i) - .5) * 500]; BARCOS.push({ b, x0, z0, ang: hs('ba' + i) * 6.28, v: 6 + hs('bv' + i) * 5 }); }
  for (let i = 0; i < (E === 'cancha' ? 0 : (SC.aviones ?? 2)); i++) { const a = new THREE.Group(), cuerpo = new THREE.Mesh(new THREE.CylinderGeometry(.7, .7, 9, 10), new THREE.MeshStandardMaterial({ color: '#ffffff' })); cuerpo.rotation.z = Math.PI / 2; a.add(cuerpo); const ala = new THREE.Mesh(new THREE.BoxGeometry(2, .3, 10), new THREE.MeshStandardMaterial({ color: '#dfe6ee' })); a.add(ala);
    const est = new THREE.Mesh(new THREE.PlaneGeometry(60, .8), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: .35, depthWrite: false })); est.position.set(-34, 0, 0); a.add(est); ESC.add(a); AVIONES.push({ a, z: (hs('az' + i) - .5) * 400, y: 70 + i * 15, v: 60 + i * 20, x0: -500 + i * 300 }); }
}
function animaEntorno(t) {
  for (const n of NUBES) { const x = n.x + t * n.v * 3, z = n.z; n.m.position.set(x, 55, z); n.sh.position.set(x + 20, .4, z + 12); }
  for (const b of BARCOS) { const d = t * b.v; b.b.position.set(b.x0 + Math.cos(b.ang) * d, .7 + Math.sin(t * 2 + b.ang) * .15, b.z0 + Math.sin(b.ang) * d); b.b.rotation.y = -b.ang; }
  for (const a of AVIONES) { a.a.position.set(a.x0 + t * a.v, a.y, a.z); }
}

// ---------- ESTADIO: el mar se vuelve cancha, gradas que reaccionan, arcos con red, balón, papelitos, humo y pantalla gigante ----------
let EST = null;
function canchaCanvas() {
  const cv = document.createElement('canvas'); cv.width = cv.height = 4096; const g = cv.getContext('2d');
  for (let i = 0; i < 40; i++) { g.fillStyle = i % 2 ? '#2f7a34' : '#378a3b'; g.fillRect(i * 4096 / 40, 0, 4096 / 40 + 1, 4096); }
  if (IMGS['tex:T02']) { g.save(); g.translate(2048, 2048); g.rotate(Math.PI / 2); g.translate(-2048, -2048); for (let x = -1024; x < 5120; x += 512) for (let y = -1024; y < 5120; y += 512) g.drawImage(IMGS['tex:T02'], x, y, 512, 512); g.restore(); }
  for (let i = 0; i < (IMGS['tex:T02'] ? 0 : 30000); i++) { g.fillStyle = `rgba(${hs('g' + i) > .5 ? '20,60,20' : '120,180,90'},.12)`; g.fillRect(hs('x' + i) * 4096, hs('y' + i) * 4096, 2, 7); }
  const v = g.createRadialGradient(2048, 2048, 400, 2048, 2048, 2300); v.addColorStop(0, 'rgba(255,255,220,.10)'); v.addColorStop(1, 'rgba(0,0,0,.55)'); g.fillStyle = v; g.fillRect(0, 0, 4096, 4096);
  g.strokeStyle = 'rgba(255,255,255,.9)'; g.lineWidth = 7; const cx = 2048, cy = 2048, L = 1150, A = 740; g.strokeRect(cx - L / 2, cy - A / 2, L, A); g.beginPath(); g.moveTo(cx, cy - A / 2); g.lineTo(cx, cy + A / 2); g.stroke(); g.beginPath(); g.arc(cx, cy, 130, 0, 7); g.stroke();
  for (const s of [-1, 1]) { g.strokeRect(cx + s * L / 2 - (s > 0 ? 190 : 0), cy - 240, 190, 480); g.strokeRect(cx + s * L / 2 - (s > 0 ? 70 : 0), cy - 110, 70, 220); }
  return cv;
}
function estadio() {
  const R0 = 1400, u = 2 * R0 / 4096, L = 1150 * u, A = 740 * u; EST = { L, A, conf: [], humo: [], tarj: [] };
  const tx = new THREE.CanvasTexture(canchaCanvas()); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  EST.pl = new THREE.Mesh(new THREE.PlaneGeometry(2 * R0, 2 * R0), new THREE.MeshStandardMaterial({ map: tx, roughness: .95, transparent: true, opacity: 0 })); EST.pl.rotation.x = -Math.PI / 2; EST.pl.position.y = .7; EST.pl.receiveShadow = true; EST.pl.renderOrder = 2; ESC.add(EST.pl);
  // gradas
  const gc = document.createElement('canvas'); gc.width = 4096; gc.height = 512; const q = gc.getContext('2d'); q.fillStyle = '#0c1118'; q.fillRect(0, 0, 4096, 512);
  for (let i = 0; i < 30000; i++) { const y = hs('cy' + i) * 460 + 40, x = hs('cx' + i) * 4096, lado = x < 2048; q.fillStyle = (lado ? ['#74acdf', '#ffffff', '#74acdf', '#d9d9d9'] : ['#f7e35c', '#2a8f3c', '#f7e35c', '#1f5aa6'])[Math.floor(hs('cc' + i) * 4)]; q.globalAlpha = .5 + hs('ca' + i) * .5; q.fillRect(x, y, 4, 5); }
  q.globalAlpha = 1; for (let i = 0; i < 24; i++) { const x = i * 4096 / 24 + 80; q.fillStyle = 'rgba(255,255,230,.95)'; q.shadowColor = '#fff'; q.shadowBlur = 30; q.fillRect(x, 6, 70, 18); q.shadowBlur = 0; }
  const tg = IMGS['tex:T03'] ? new THREE.Texture(IMGS['tex:T03']) : new THREE.CanvasTexture(gc); tg.needsUpdate = true; tg.colorSpace = THREE.SRGBColorSpace; tg.wrapS = THREE.RepeatWrapping; tg.repeat.set(IMGS['tex:T03'] ? 6 : 2, 1);
  EST.ring = new THREE.Mesh(new THREE.CylinderGeometry(560, 470, 170, 90, 1, true), new THREE.MeshBasicMaterial({ map: tg, side: THREE.BackSide, transparent: true, opacity: 0 })); EST.ring.position.y = 70; ESC.add(EST.ring); EST.tg = tg;
  // arcos con red
  EST.arcos = {}; for (const lado of [-1, 1]) { const g = new THREE.Group(), blanco = new THREE.MeshStandardMaterial({ color: '#ffffff', roughness: .3 }), an = 96, al = 32, pr = 22;
    for (const z of [-an / 2, an / 2]) { const p = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.6, al, 10), blanco); p.position.set(0, al / 2, z); p.castShadow = true; g.add(p); }
    const tra = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.6, an, 10), blanco); tra.rotation.x = Math.PI / 2; tra.position.set(0, al, 0); g.add(tra);
    const nc = document.createElement('canvas'); nc.width = nc.height = 256; const n = nc.getContext('2d'); n.strokeStyle = 'rgba(255,255,255,.8)'; n.lineWidth = 2; for (let i = 0; i <= 256; i += 16) { n.beginPath(); n.moveTo(i, 0); n.lineTo(i, 256); n.stroke(); n.beginPath(); n.moveTo(0, i); n.lineTo(256, i); n.stroke(); }
    const nt = new THREE.CanvasTexture(nc); nt.wrapS = nt.wrapT = THREE.RepeatWrapping; nt.repeat.set(4, 2); const red = new THREE.Mesh(new THREE.PlaneGeometry(an, al), new THREE.MeshBasicMaterial({ map: nt, transparent: true, side: THREE.DoubleSide, depthWrite: false }));
    red.rotation.y = Math.PI / 2; red.position.set(lado * pr, al / 2, 0); g.add(red); const top = new THREE.Mesh(new THREE.PlaneGeometry(pr, an), new THREE.MeshBasicMaterial({ map: nt, transparent: true, side: THREE.DoubleSide, depthWrite: false })); top.rotation.x = -Math.PI / 2; top.position.set(lado * pr / 2, al, 0); g.add(top);
    g.position.set(lado * L / 2, 0, 0); g.visible = false; ESC.add(g); EST.arcos[lado] = { g, red }; }
  // balón
  const bc = document.createElement('canvas'); bc.width = 256; bc.height = 128; const b = bc.getContext('2d'); b.fillStyle = '#fff'; b.fillRect(0, 0, 256, 128); b.fillStyle = '#111'; for (let i = 0; i < 12; i++) { b.beginPath(); b.arc((i % 6) * 46 + 18 + (i > 5 ? 23 : 0), i > 5 ? 92 : 36, 13, 0, 7); b.fill(); }
  const bt = new THREE.CanvasTexture(bc); bt.colorSpace = THREE.SRGBColorSpace; EST.balon = new THREE.Mesh(new THREE.SphereGeometry(7, 28, 18), new THREE.MeshStandardMaterial({ map: bt, roughness: .4 })); EST.balon.castShadow = true; EST.balon.visible = false; ESC.add(EST.balon);
  // papelitos
  for (let i = 0; i < 420; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(3, 1.9), new THREE.MeshBasicMaterial({ color: '#ffffff', side: THREE.DoubleSide })); m.visible = false; ESC.add(m); EST.conf.push(m); }
  // humo de bengalas
  for (let i = 0; i < 26; i++) { const sc2 = document.createElement('canvas'); sc2.width = sc2.height = 128; const h = sc2.getContext('2d'), gr = h.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,.8)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); h.fillStyle = gr; h.fillRect(0, 0, 128, 128);
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(sc2), transparent: true, opacity: 0, depthWrite: false })); sp.scale.set(60, 60, 1); ESC.add(sp); EST.humo.push(sp); }
  // pantalla gigante
  const pc = document.createElement('canvas'); pc.width = 960; pc.height = 540; EST.pc = pc; EST.pt = new THREE.CanvasTexture(pc); EST.pt.colorSpace = THREE.SRGBColorSpace; const marco = new THREE.Mesh(new THREE.BoxGeometry(200, 117, 4), new THREE.MeshStandardMaterial({ color: '#111820' }));
  EST.pant = new THREE.Group(); EST.pant.add(marco); const scr = new THREE.Mesh(new THREE.PlaneGeometry(188, 106), new THREE.MeshBasicMaterial({ map: EST.pt })); scr.position.z = 2.2; EST.pant.add(scr); EST.pant.position.set(0, 52, -150); EST.pant.lookAt(0, 30, 300); EST.pant.visible = false; ESC.add(EST.pant); EST.ultImg = null;
  for (const c of SC.tarjetas3d || []) { const m = new THREE.Mesh(new THREE.BoxGeometry(18, .8, 26), new THREE.MeshStandardMaterial({ color: c.color === 'roja' ? '#e0262b' : '#ffd23f', roughness: .4 })); m.castShadow = true; m.visible = false; ESC.add(m); EST.tarj.push({ m, c }); }
}
function marcadorEn(t) { const s = { izq: 0, der: 0 }; for (const g of SC.goles || []) if (t >= g.t + 1.0) s[g.lado === 1 ? 'izq' : 'der']++; return s; }
function animaEstadio(t) {
  const E = SC.estadio, q = eio(pr(t, E.t, E.dur || 1.6)); EST.pl.material.opacity = q; EST.ring.material.opacity = q;
  // al terminar la transformación la cancha queda opaca y sola: se apagan el océano y el mapa del mundo (así no hay nada debajo que parpadee)
  const lista = q >= .999; EST.pl.material.transparent = !lista; EST.pl.material.depthWrite = lista || q > .5; EST.pl.material.needsUpdate = true;
  if (P._marMesh) P._marMesh.visible = !lista; if (P._fondo) { P._fondo.visible = !lista; P._fondo.material.transparent = q > 0; P._fondo.material.opacity = 1 - q * .6; }
  EST.ring.material.transparent = !lista; EST.ring.material.depthWrite = lista;
  for (const k of Object.keys(P)) if (!k.startsWith('_') && P[k].p.neutro) { P[k].grp.position.y = -q * 8; P[k].grp.visible = q < .55; }
  for (const n of NUBES) { n.m.visible = n.sh.visible = q < .5; } for (const b of BARCOS) b.b.visible = q < .3; for (const a of AVIONES) a.a.visible = q < .5;
  if (q > .3 && !ESC.userData.estadioNiebla) { ESC.userData.estadioNiebla = true; ESC.userData.fijaNiebla = true; ESC.fog = new THREE.Fog('#0b1220', 700, 1900); ESC.background = new THREE.Color('#070b12'); }
  for (const l of [-1, 1]) EST.arcos[l].g.visible = q > .6;
  // gradas que saltan y hacen la ola
  let fiesta = 0; for (const g of SC.goles || []) fiesta = Math.max(fiesta, cl(1 - (t - g.t - 1) / 3) * (t > g.t + 1 ? 1 : 0)); EST.ring.position.y = 70 + Math.abs(Math.sin(t * 11)) * 3 * fiesta + Math.sin(t * 2) * .4; EST.tg.offset.x = Math.sin(t * .3) * .01 + fiesta * Math.sin(t * 20) * .002;
  // goles: el balón sale del país, vuela al arco y mueve la red
  EST.balon.visible = false; for (const l of [-1, 1]) EST.arcos[l].red.scale.set(1, 1, 1);
  for (const g of SC.goles || []) { const dt = t - g.t, o = P[g.pais]; if (!o) continue;
    if (dt >= 0 && dt < 1.0) { const a = o.grp.position.clone().setY(o.alto * 1.5 + 4), b = new THREE.Vector3(-g.lado * EST.L / 2 - g.lado * 8, 8, 0), u = eio(dt / 1.0); EST.balon.visible = true; EST.balon.position.set(lerp(a.x, b.x, u), lerp(a.y, b.y, u) + Math.sin(u * Math.PI) * 60, lerp(a.z, b.z, u)); EST.balon.rotation.set(t * 14, t * 9, 0); o.grp.position.y += Math.max(0, Math.sin(dt * 8)) * 3; }
    if (dt >= 1.0 && dt < 2.2) { const k = Math.exp(-(dt - 1) * 3) * Math.sin((dt - 1) * 18); EST.arcos[-g.lado].red.scale.set(1 + Math.abs(k) * .6, 1, 1); EST.balon.visible = dt < 1.6; EST.balon.position.set(-g.lado * (EST.L / 2 + 6), 4, 0); }
    if (dt >= 1.0 && dt < 4.5) { const cols = g.lado === 1 ? ['#74acdf', '#ffffff', '#74acdf'] : ['#f7e35c', '#2a8f3c', '#1f5aa6']; EST.conf.forEach((m, i) => { const ex = dt - 1, x0 = (hs('cfx' + i) - .5) * 520, z0 = (hs('cfz' + i) - .5) * 360; m.visible = true; m.material.color.set(cols[i % 3]); m.position.set(x0 + Math.sin(ex * 3 + i) * 5, 95 - ex * (26 + hs('cv' + i) * 16), z0); m.rotation.set(ex * 5 + i, ex * 4, ex * 3); if (m.position.y < .5) m.position.y = .5; });
      EST.humo.forEach((sp, i) => { const lado = i % 2 ? 1 : -1, ang = hs('ha' + i) * Math.PI * 2; sp.material.opacity = cl((dt - 1) / .5) * cl(1 - (dt - 3.2) / 1.3) * .5; sp.material.color.set(g.lado === 1 ? (i % 2 ? '#74acdf' : '#ffffff') : (i % 2 ? '#f7e35c' : '#2a8f3c')); sp.position.set(Math.cos(ang) * 470, 40 + (dt - 1) * 18 + i % 3 * 10, Math.sin(ang) * 400); sp.scale.setScalar(50 + (dt - 1) * 25); }); } }
  if (!(SC.goles || []).some(g => t >= g.t + 1 && t < g.t + 4.5)) { EST.conf.forEach(m => m.visible = false); EST.humo.forEach(sp => sp.material.opacity = 0); }
  // pantalla gigante
  const pa = (SC.pantalla || []).find(e => t >= e.desde && t <= e.hasta); EST.pant.visible = !!pa && q > .9;
  if (pa) { const im = IMGS[pa.img], c = EST.pc.getContext('2d'), k = pr(t, pa.desde, pa.hasta - pa.desde), z = 1.05 + .1 * k; if (im) { const s2 = Math.max(960 / im.width, 540 / im.height) * z; c.drawImage(im, (960 - im.width * s2) / 2, (540 - im.height * s2) / 2, im.width * s2, im.height * s2); }
    c.fillStyle = 'rgba(0,0,0,.55)'; c.fillRect(0, 470, 960, 70); c.fillStyle = '#ffd23f'; c.font = '44px Anton'; c.textAlign = 'left'; c.fillText((pa.texto || '').toUpperCase(), 24, 522); for (let y = 0; y < 540; y += 4) { c.fillStyle = 'rgba(0,0,0,.08)'; c.fillRect(0, y, 960, 1); } EST.pt.needsUpdate = true; }
  // tarjetas que caen
  for (const { m, c } of EST.tarj) { const o = P[c.pais], dt = t - c.t; m.visible = !!o && dt > 0 && t < (c.hasta ?? 1e9); if (!m.visible) continue; const u = cl(dt / .9), top = o.grp.position.y + o.alto * 1.4 + .3; m.position.set(o.grp.position.x + 6, lerp(120, top, eob(u)), o.grp.position.z - 4); m.rotation.set(0, (1 - u) * 8, (1 - u) * 1.2 + .15); }
}
function reloj(t) { // marcador de TV con reloj de partido (00:00 → 90:00)
  const r = SC.reloj; if (!r || t < r.desde) return; const a = cl((t - r.desde) / .4), min = Math.min(90, (t - r.desde) / ((r.hasta || SC.duracion) - r.desde) * 90 * (r.escala || 1)), mm = Math.floor(min), ss = min >= 90 ? 0 : Math.floor((min - mm) * 60), s = marcadorEn(t);
  OX.save(); OX.globalAlpha = a; const x = 46, y = 40; rr(x, y, 430, 74, 12, 'rgba(8,12,18,.92)'); rr(x + 300, y, 130, 74, 12, '#ffd23f');
  for (const [i, iso] of [[0, r.isoIzq], [1, r.isoDer]]) { const fl = FLAGIM[iso], fx = x + 22 + i * 150; if (fl) { OX.save(); OX.beginPath(); OX.roundRect(fx, y + 18, 52, 38, 6); OX.clip(); OX.drawImage(fl, fx, y + 18, 52, 38); OX.restore(); } }
  const gol = (SC.goles || []).find(g => t >= g.t + 1 && t < g.t + 2.4), pulso = gol ? 1 + .25 * Math.abs(Math.sin((t - gol.t) * 12)) : 1;
  OX.save(); OX.translate(x + 112, y + 39); OX.scale(pulso, pulso); txt(String(s.izq), 0, 0, '52px Anton', '#fff', 'center'); OX.restore(); txt('-', x + 150, y + 37, '40px Anton', 'rgba(255,255,255,.5)', 'center'); OX.save(); OX.translate(x + 248, y + 39); OX.scale(pulso, pulso); txt(String(s.der), 0, 0, '52px Anton', '#fff', 'center'); OX.restore();
  txt(`${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}`, x + 365, y + 39, '40px Anton', '#0b0f14', 'center');
  if (gol) { const k = pr(t, gol.t + 1, .3); OX.globalAlpha = a * cl(1 - pr(t, gol.t + 2.1, .3)); rr(x, y + 84, 430, 58, 10, gol.lado === 1 ? '#74acdf' : '#2a8f3c'); txt('¡GOL! ' + (gol.texto || '').toUpperCase(), x + 22 + (1 - k) * -40, y + 113, '700 30px Barlow', '#fff'); }
  OX.restore();
}
