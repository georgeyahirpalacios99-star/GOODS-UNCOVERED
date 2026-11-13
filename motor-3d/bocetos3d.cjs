// Bocetos 3D (Three.js con sombreado de dibujo animado): escena 9:16 + presentación de personajes, para los estilos A, B y C.
//   node motor-3d/bocetos3d.cjs [A B C]   → bocetos-historia/3d-estilo-X.jpg
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const R = path.join(__dirname, '..');
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.json': 'application/json' };
const srv = http.createServer((q, s) => { const f = path.join(R, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(R) || !fs.existsSync(f)) { s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(s); });
const NOMBRES = { A: ['FRIJOLITOS', 'Cuerpo de una pieza, ojos grandes. Muy reconocible.'], B: ['CABEZONES DE JUGUETE', 'Cabeza grande, nariz, orejas y mejillas. El más expresivo.'], C: ['PALITOS PRO', 'La fórmula del original mejorada: ropa, manos y cejas.'] };
(async () => {
  await new Promise(r => srv.listen(0, r)); const port = srv.address().port;
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } }); p.on('pageerror', e => console.log('ERROR página:', e.message)); p.on('console', m => m.type() === 'error' && console.log('consola:', m.text()));
  await p.goto(`http://localhost:${port}/motor-3d/escena.html`); await p.waitForFunction(() => window.listo, null, { timeout: 60000 }); await p.evaluate(() => document.fonts.load('900 40px M'));
  for (const est of (process.argv.slice(2).length ? process.argv.slice(2) : ['A', 'B', 'C'])) {
    console.time('estilo ' + est);
    const escena = await p.evaluate(e => escena3d(e, 1080, 1920, { pos: [-2.2, 2.4, 17.5], mira: [.6, 6.4, -12], fov: 50, palabra: 'fuego', y: .6 }), est);
    const est3 = await p.evaluate(e => estudio3d(e, 1200, 640), est);
    const [nom, nota] = NOMBRES[est];
    const tab = await p.evaluate(async ([escena, est3, est, nom, nota]) => {
      const carga = u => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = u; });
      const c = document.createElement('canvas'); c.width = 1920; c.height = 1080; const x = c.getContext('2d'); x.fillStyle = '#12161b'; x.fillRect(0, 0, 1920, 1080);
      const e1 = await carga(escena); x.drawImage(e1, 40, 20, 1040 * 1080 / 1920, 1040); x.strokeStyle = '#fff'; x.lineWidth = 4; x.strokeRect(40, 20, 1040 * 1080 / 1920, 1040);
      x.fillStyle = '#fff'; x.font = '800 52px M'; x.fillText('ESTILO ' + est + ' · ' + nom + ' · 3D', 680, 88); x.fillStyle = '#ffd23f'; x.font = '600 27px M'; x.fillText(nota, 680, 130);
      const e2 = await carga(est3.estudio); x.save(); x.beginPath(); x.roundRect(680, 160, 1200, 640, 24); x.clip(); x.drawImage(e2, 680, 160); x.restore();
      x.fillStyle = '#cfd6dc'; x.font = '700 24px M'; x.textAlign = 'center'; ['ATACANTE', 'DEFENSOR', 'INGENIERO'].forEach((t, i) => x.fillText(t, 680 + 1200 * (.27 + i * .23), 785));
      x.textAlign = 'left'; x.fillStyle = '#fff'; x.font = '700 28px M'; x.fillText('Expresiones:', 680, 900);
      for (let i = 0; i < 4; i++) { const im = await carga(est3.caras[i]), X = 905 + i * 245; x.save(); x.beginPath(); x.roundRect(X, 825, 225, 225, 20); x.clip(); x.drawImage(im, X - 37, 825 - 37); x.fillStyle = 'rgba(10,14,18,.8)'; x.fillRect(X, 1015, 225, 35); x.restore();
        x.fillStyle = '#ffd23f'; x.font = '700 21px M'; x.textAlign = 'center'; x.fillText(['NORMAL', 'SUSTO', 'ENOJO', 'RISA'][i], X + 112, 1040); x.textAlign = 'left'; }
      return c.toDataURL('image/jpeg', .92); }, [escena, est3, est, nom, nota]);
    fs.writeFileSync(path.join(R, 'bocetos-historia', `3d-estilo-${est}.jpg`), Buffer.from(tab.split(',')[1], 'base64'));
    fs.writeFileSync(path.join(R, 'bocetos-historia', `3d-escena-${est}.jpg`), Buffer.from(escena.split(',')[1], 'base64'));
    console.timeEnd('estilo ' + est);
  }
  await b.close(); srv.close();
})();
