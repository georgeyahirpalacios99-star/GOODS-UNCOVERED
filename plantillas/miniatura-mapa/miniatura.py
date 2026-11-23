"""FORMATO ÚNICO de miniaturas · Lo Que el Mapa No Dice (1280x720).
Reglas fijas: fondo = mapa 3D del canal (país con cara) · texto arriba a la izquierda, 2 líneas
(blanca + amarilla, Anton, borde negro) · 1 tarjeta de foto real abajo a la izquierda con etiqueta amarilla ·
1 círculo o flecha roja sobre el protagonista · logo del canal (pin con ojo) arriba a la derecha.
    python3 plantillas/miniatura-mapa/miniatura.py            (hace todas las de MINIS)
    python3 plantillas/miniatura-mapa/miniatura.py colombia   (solo una)
"""
import sys, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
R = Path(__file__).resolve().parents[2]; D = Path(__file__).resolve().parent; FU = R / 'motor-mapa/datos/fuentes'
W, H = 1280, 720; AMA = (255, 210, 63); NEG = (8, 12, 18); ROJO = (230, 36, 41)
anton = lambda s: ImageFont.truetype(str(FU / 'Anton.woff2'), s)
V = R / 'videos-largos'
MINIS = {
    'arg-bra':  dict(salida=V / '008-argentina-vs-brasil/miniatura/miniatura-formato.jpg', lineas=('¿QUIÉN', 'GANA?'),
                     foto=V / '008-argentina-vs-brasil/fotos-reales/messi-2022-2.jpg', ffy=.15, etiqueta='10 RONDAS', marca=('vs', 805, 560, 60)),
    'sinaloa':  dict(salida=V / '007-sinaloa-desaparece/miniatura-formato.jpg', lineas=('¿SIN', 'SINALOA?'),
                     foto=V / '007-sinaloa-desaparece/fotos-reales/aguachile-1.jpg', ffy=.5, etiqueta='AGUACHILE', marca=('circulo', 717, 222, 58)),
    'colombia': dict(salida=V / '003-colombia-desaparece/miniatura/miniatura-formato.jpg', lineas=('¿SIN', 'COLOMBIA?'),
                     foto=D / 'fotos/cartagena-1.jpg', ffy=.4, etiqueta='CARTAGENA', marca=('circulo', 760, 300, 120)),
    'hispanos': dict(salida=V / '002-sin-paises-hispanos/miniaturas/miniatura-formato.jpg', lineas=('¿SOLO QUEDA', 'BRASIL?'),
                     foto=D / 'fotos/machu-picchu-1.jpg', ffy=.5, etiqueta='18 PAÍSES', marca=('circulo', 890, 352, 66)),
    'el-nino':  dict(salida=V / '001-el-nino-2026/miniaturas/miniatura-formato.jpg', lineas=('¿SIN LUZ', 'NI AGUA?'),
                     foto=V / '001-el-nino-2026/imagenes/mapa-anomalia-oct.jpg', recorte=(0, .14, 1, .82), etiqueta='MAR +3 °C', marca=('flecha', 770, 322, 0)),
}
def cubrir(im, w, h, fx=.5, fy=.5):
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - w) * fx); y = round((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
def sombra(lz, capa, xy, r=16, op=170):
    a = capa.split()[-1].point(lambda v: op if v else 0); s = Image.new('RGBA', capa.size, (0, 0, 0, 0)); s.putalpha(a)
    lz.alpha_composite(s.filter(ImageFilter.GaussianBlur(r)), (xy[0] + 8, xy[1] + 12)); lz.alpha_composite(capa, xy)
def pin(d=86):  # logo del canal: pin amarillo con ojo
    k = 4; S = d * k; im = Image.new('RGBA', (S, int(S * 1.25))); g = ImageDraw.Draw(im); r = S * .46; cx, cy = S / 2, S * .48
    g.polygon([(cx - r * .62, cy + r * .62), (cx + r * .62, cy + r * .62), (cx, S * 1.22)], fill=NEG); g.ellipse((cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10), fill=NEG)
    g.polygon([(cx - r * .55, cy + r * .6), (cx + r * .55, cy + r * .6), (cx, S * 1.15)], fill=AMA); g.ellipse((cx - r, cy - r, cx + r, cy + r), fill=AMA)
    g.ellipse((cx - r * .62, cy - r * .42, cx + r * .62, cy + r * .42), fill='white', outline=NEG, width=int(S * .045))
    g.ellipse((cx - r * .3, cy - r * .3, cx + r * .3, cy + r * .3), fill=NEG); g.ellipse((cx - r * .2, cy - r * .22, cx - r * .02, cy - r * .04), fill='white')
    return im.resize((d, int(d * 1.25)), Image.LANCZOS)
def hacer(clave):
    m = MINIS[clave]; lz = cubrir(Image.open(D / 'fondos' / f'{clave}.jpg').convert('RGB'), W, H).convert('RGBA')
    lz = Image.fromarray(__import__('numpy').array(ImageEnhance.Contrast(ImageEnhance.Color(lz.convert('RGB')).enhance(1.12)).enhance(1.06))).convert('RGBA')
    gr = Image.new('L', (W, H)); gd = ImageDraw.Draw(gr)
    for x in range(W): gd.line([(x, 0), (x, H)], fill=int(max(0, 1 - x / (W * .62)) ** 1.4 * 170))
    osc = Image.new('RGBA', (W, H), (4, 10, 22, 255)); osc.putalpha(gr); lz.alpha_composite(osc)
    dr = ImageDraw.Draw(lz); tipo, x, y, r = m['marca']
    if tipo == 'vs':  # duelo: insignia roja VS entre los dos países
        dr.ellipse((x - r - 6, y - r - 6, x + r + 6, y + r + 6), fill=NEG); dr.ellipse((x - r, y - r, x + r, y + r), fill=ROJO, outline='white', width=5)
        dr.text((x, y + 2), 'VS', font=anton(int(r * 1.1)), fill='white', anchor='mm', stroke_width=4, stroke_fill=NEG)
    elif tipo == 'circulo':
        for w_, c in ((16, NEG), (9, ROJO)): dr.ellipse((x - r, y - r * .8, x + r, y + r * .8), outline=c, width=w_)
    else:  # flecha roja curva hacia el protagonista, desde el mar
        pts = [(x - 170 + 170 * t + 20 * math.sin(t * 3), y + 120 - 120 * t ** 1.3) for t in [i / 30 for i in range(31)]]
        for w_, c in ((24, NEG), (14, ROJO)): dr.line(pts, fill=c, width=w_, joint='curve')
        a = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0]); tip = pts[-1]
        tri = [(tip[0] + 34 * math.cos(a), tip[1] + 34 * math.sin(a)), (tip[0] + 26 * math.cos(a + 2.3), tip[1] + 26 * math.sin(a + 2.3)), (tip[0] + 26 * math.cos(a - 2.3), tip[1] + 26 * math.sin(a - 2.3))]
        dr.polygon(tri, fill=ROJO, outline=NEG, width=4)
    # texto: 2 líneas, la segunda amarilla y más grande; se ajusta al ancho
    l1, l2 = m['lineas']; maxw = 640
    for i, (s, tam, col, yy) in enumerate(((l1, 112, (255, 255, 255), 108), (l2, 150, AMA, 228))):
        f = anton(tam)
        while dr.textlength(s, font=f) > maxw: tam -= 4; f = anton(tam)
        dr.text((44, yy), s, font=f, fill=col, stroke_width=10, stroke_fill=NEG, anchor='lm')
    # tarjeta con foto real
    tw, th = 330, 220; fo = Image.open(m['foto']).convert('RGB')
    if m.get('recorte'): l, t, r_, b = m['recorte']; fo = fo.crop((int(fo.width * l), int(fo.height * t), int(fo.width * r_), int(fo.height * b)))
    fo = cubrir(fo, tw, th, .5, m.get('ffy', .5))
    fo = ImageEnhance.Contrast(ImageEnhance.Color(fo).enhance(1.15)).enhance(1.06)
    c = Image.new('RGBA', (tw + 16, th + 16), 'white'); c.paste(fo, (8, 8)); cd = ImageDraw.Draw(c); fe = anton(40); ew = cd.textlength(m['etiqueta'], font=fe)
    cd.rectangle((8, th - 50, 8 + ew + 30, th + 8), fill=AMA); cd.text((23, th - 21), m['etiqueta'], font=fe, fill=NEG, anchor='lm')
    sombra(lz, c.rotate(4, expand=True, resample=Image.BICUBIC), (34, 392))
    lg = pin(74); sombra(lz, lg, (W - lg.width - 26, 20), 8, 140)
    m['salida'].parent.mkdir(parents=True, exist_ok=True); lz.convert('RGB').save(m['salida'], quality=95); print('miniatura', clave, '→', m['salida'].relative_to(R))
for k in (sys.argv[1:] or MINIS): hacer(k)
