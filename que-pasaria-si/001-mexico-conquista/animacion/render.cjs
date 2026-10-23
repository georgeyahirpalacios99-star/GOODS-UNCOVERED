// usage: node render.cjs preview t1,t2,...  |  node render.cjs full out.mp4
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

(async () => {
  const [mode, arg] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(__dirname, 'video.html'));
  await page.evaluate(async () => {
    await Promise.all(['400 40px Inter', '500 40px Inter', '600 40px Inter', '900 40px Inter',
      'italic 700 40px "Liberation Serif"', 'italic 400 40px Inter'].map(f => document.fonts.load(f)));
  });
  const grab = t => page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', 0.93); }, t)
    .then(u => Buffer.from(u.split(',')[1], 'base64'));

  if (mode === 'preview') {
    const dir = path.join(__dirname, 'preview'); fs.mkdirSync(dir, { recursive: true });
    for (const t of arg.split(',').map(Number)) fs.writeFileSync(path.join(dir, `t${t.toFixed(1)}.jpg`), await grab(t));
  } else {
    const dur = await page.evaluate(() => DURATION), fps = 30, n = Math.round(dur * fps);
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-movflags', '+faststart', arg], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < n; i++) {
      const buf = await grab(i / fps);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 150 === 0) console.log(`frame ${i}/${n}`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
