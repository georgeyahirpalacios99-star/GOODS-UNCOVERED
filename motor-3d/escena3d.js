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
    P[p.adm] = { grp, mesh, cara, alto, p, ring: p.polys.reduce((a, b) => (b[0].length > a[0].length ? b : a))[0], colores: [lado, new THREE.Color('#ffffff')], fc };
  }
  OV = document.getElementById('ov'); OX = OV.getContext('2d');
}
function expr(adm, t) { const l = (SC.caras || {})[adm] || (SC.caras || {})['*'] || [[0, 'normal']]; let e = 'normal'; for (const [a, x] of l) if (t >= a) e = x; return e; }
function dibujaCara(k, t, mira) {
  const o = P[k]; if (!o.cara) return; const { cc, ct } = o.cara.userData, c = cc.getContext('2d'), ex = expr(k, t); c.clearRect(0, 0, 256, 256);
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
