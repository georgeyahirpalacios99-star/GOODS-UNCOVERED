"""Bocetos de miniatura del video 008 (1280x720) con fotos reales de Commons y el estadio 3D."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
D = Path(__file__).resolve().parent; V = D.parent; F = V / 'fotos-reales'; R = V.parent.parent
FU = R / 'motor-mapa/datos/fuentes'; BAN = R / 'motor-mapa/datos/banderas'
FONDO = Path(sys.argv[1])  # cuadro limpio del estadio 3D
W, H = 1280, 720; AMA = (255, 210, 63); NEG = (8, 12, 18)
anton = lambda s: ImageFont.truetype(str(FU / 'Anton.woff2'), s)
barlow = lambda s: ImageFont.truetype(str(FU / 'BarlowCondensed-700.woff2'), s)

def cubrir(im, w, h, fx=.5, fy=.5):
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - w) * fx); y = round((im.height - h) * fy); return im.crop((x, y, x + w, y + h))

def bandera(iso, d):
    import subprocess, io
    png = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(BAN / f'{iso}.svg'), '-vf', f'scale={d * 3}:-1', '-f', 'image2pipe', '-c:v', 'png', '-'], capture_output=True).stdout
    b = cubrir(Image.open(io.BytesIO(png)).convert('RGBA'), d, d); m = Image.new('L', (d, d)); ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), 255)
    out = Image.new('RGBA', (d + 10, d + 10)); ImageDraw.Draw(out).ellipse((0, 0, d + 9, d + 9), (255, 255, 255)); out.paste(b, (5, 5), m); return out

def sombra(lienzo, capa, xy, r=18, op=170):
    a = capa.split()[-1].point(lambda v: op if v else 0); s = Image.new('RGBA', capa.size, (0, 0, 0, 0)); s.putalpha(a)
    s = s.filter(ImageFilter.GaussianBlur(r)); lienzo.alpha_composite(s, (xy[0] + 8, xy[1] + 12)); lienzo.alpha_composite(capa, xy)

def tarjeta(lienzo, img, w, h, xy, rot, fx=.5, fy=.3, etiqueta=None):
    f = cubrir(Image.open(F / img).convert('RGB'), w, h, fx, fy); f = ImageEnhance.Contrast(ImageEnhance.Color(f).enhance(1.15)).enhance(1.08)
    c = Image.new('RGBA', (w + 16, h + 16), (255, 255, 255, 255)); c.paste(f, (8, 8))
    if etiqueta:
        dr = ImageDraw.Draw(c); fn = anton(46); tw = dr.textlength(etiqueta, font=fn)
        dr.rectangle((8, h - 62, 8 + tw + 36, h + 8), fill=AMA); dr.text((26, h - 58), etiqueta, font=fn, fill=NEG)
    c = c.rotate(rot, expand=True, resample=Image.BICUBIC); sombra(lienzo, c, xy)

def texto(dr, s, xy, fn, col=AMA, borde=8, anchor='mm'):
    dr.text(xy, s, font=fn, fill=col, stroke_width=borde, stroke_fill=NEG, anchor=anchor)

def marcador(lienzo, cx, y, izq, der, reloj=None, esc=1.):
    w, h = int(560 * esc), int(120 * esc); m = Image.new('RGBA', (w, h)); dr = ImageDraw.Draw(m)
    dr.rounded_rectangle((0, 0, w - 1, h - 1), int(22 * esc), fill=(*NEG, 240)); d = int(84 * esc)
    m.alpha_composite(bandera('ar', d), (int(16 * esc), (h - d - 10) // 2)); m.alpha_composite(bandera('br', d), (w - d - 10 - int(16 * esc), (h - d - 10) // 2))
    fn = anton(int(92 * esc)); dr.text((w * .36, h / 2), str(izq), font=fn, fill='white', anchor='mm'); dr.text((w * .64, h / 2), str(der), font=fn, fill='white', anchor='mm')
    dr.text((w / 2, h / 2), '-', font=anton(int(70 * esc)), fill=(255, 255, 255, 110), anchor='mm')
    x = cx - w // 2
    if reloj:
        rw = int(150 * esc); r = Image.new('RGBA', (rw, int(74 * esc))); ImageDraw.Draw(r).rounded_rectangle((0, 0, rw - 1, int(74 * esc) - 1), int(14 * esc), fill=AMA)
        ImageDraw.Draw(r).text((rw / 2, int(37 * esc)), reloj, font=anton(int(52 * esc)), fill=NEG, anchor='mm'); x -= rw // 2 + 6
        sombra(lienzo, r, (x + w + 12, y + (h - int(74 * esc)) // 2), 10)
    sombra(lienzo, m, (x, y), 14)

def vineta(im, k=.55):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse((-W * .15, -H * .2, W * 1.15, H * 1.2), 255); m = m.filter(ImageFilter.GaussianBlur(160))
    osc = Image.new('RGBA', (W, H), (0, 0, 0, int(255 * k))); osc.putalpha(ImageOps.invert(m).point(lambda v: int(v * k))); im.alpha_composite(osc)

fondo = Image.open(FONDO).convert('RGBA')

# A · EL PARTIDO: estadio 3D al centro, Messi y Pelé en tarjetas, marcador 5-5 90:00
a = cubrir(fondo, W, H, .5, .45).convert('RGBA'); vineta(a)
tarjeta(a, 'messi-2022-2.jpg', 330, 430, (-6, 150), 5, .5, .15, 'MESSI')
tarjeta(a, 'pele-1970-2.jpg', 330, 430, (W - 360, 150), -5, .5, .25, 'PELÉ')
marcador(a, W // 2, 22, 5, 5, '90:00'); dr = ImageDraw.Draw(a)
texto(dr, '¿QUIÉN GANA?', (W // 2, 640), anton(118), borde=10)
a.convert('RGB').save(D / 'boceto-A-el-partido.jpg', quality=94)

# B · LEYENDAS: dos fotos reales a sangre en diagonal, VS al centro, 10 rondas
b = Image.new('RGBA', (W, H)); izq = Image.new('RGB', (W, H)); izq.paste(cubrir(Image.open(F / 'maradona-1.jpg').convert('RGB'), int(W * .6), H, .6, .32), (0, 0)); der = Image.new('RGB', (W, H)); der.paste(cubrir(Image.open(F / 'pele-1970-1.jpg').convert('RGB'), int(W * .6), H, .5, .05), (int(W * .4), 0))
izq = Image.blend(izq, Image.new('RGB', (W, H), (90, 170, 230)), .18); der = Image.blend(der, Image.new('RGB', (W, H), (20, 140, 60)), .18)
m = Image.new('L', (W, H)); ImageDraw.Draw(m).polygon([(0, 0), (W * .56, 0), (W * .44, H), (0, H)], 255)
b.paste(der, (0, 0)); b.paste(izq, (0, 0), m); dr = ImageDraw.Draw(b)
dr.line([(W * .56, 0), (W * .44, H)], fill=AMA, width=12); vineta(b, .45)
cir = Image.new('RGBA', (210, 210)); cd = ImageDraw.Draw(cir); cd.ellipse((0, 0, 209, 209), fill=NEG, outline=AMA, width=8); cd.text((105, 100), 'VS', font=anton(110), fill=AMA, anchor='mm'); sombra(b, cir, (W // 2 - 105, H // 2 - 130))
texto(dr, 'ARGENTINA', (300, 70), anton(92), col=(255, 255, 255)); texto(dr, 'BRASIL', (1010, 70), anton(92), col=(255, 255, 255))
texto(dr, '10 RONDAS. 1 GANADOR.', (W // 2, 645), anton(96), borde=9)
b.convert('RGB').save(D / 'boceto-B-leyendas.jpg', quality=94)

# C · EL MARCADOR: estadio 3D grande, marcador gigante 5-5 y pregunta
c = cubrir(fondo, W, H, .5, .55).convert('RGBA'); vineta(c, .6)
tarjeta(c, 'messi-2026-2.jpg', 300, 220, (30, 440), 6, .62, .2)
tarjeta(c, 'vinicius-1.jpg', 240, 260, (W - 290, 400), -6, .5, .12)
marcador(c, W // 2 - 10, 40, 5, 5, '90:00', 1.35); dr = ImageDraw.Draw(c)
texto(dr, '¿EMPATE?', (W // 2, 330), anton(150), borde=12)
c.convert('RGB').save(D / 'boceto-C-marcador.jpg', quality=94)
print('listo')

# D · Fondo de Flow (estadio dividido): Messi vs Pelé, marcador 5-5 y pregunta
FLOW = D / 'fondo-flow.jpg'
if FLOW.exists():
    d_ = cubrir(Image.open(FLOW).convert('RGB'), W, H, .5, .35).convert('RGBA')
    d_ = Image.alpha_composite(d_, Image.new('RGBA', (W, H), (0, 0, 0, 0))); vineta(d_, .5)
    tarjeta(d_, 'messi-2022-2.jpg', 320, 420, (12, 168), 5, .5, .15, 'MESSI')
    tarjeta(d_, 'pele-1970-2.jpg', 320, 420, (W - 360, 168), -5, .5, .25, 'PELÉ')
    marcador(d_, W // 2, 24, 5, 5, '90:00'); dr = ImageDraw.Draw(d_)
    texto(dr, '¿QUIÉN', (W // 2, 330), anton(120), borde=10); texto(dr, 'GANA?', (W // 2, 470), anton(150), borde=11)
    d_.convert('RGB').save(D / 'boceto-D-flow.jpg', quality=94)
    print('D listo')
