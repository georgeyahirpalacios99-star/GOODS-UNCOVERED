import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT = sys.argv[1]
W, H, FPS, DUR = 1920, 1080, 30, 4.4
SS = 2  # supersampling
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34 * SS)
RED, GREY, BLUE, INK = (230, 33, 58), (190, 190, 190), (38, 113, 230), (30, 30, 30)

def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
def lerp(a, b, k): return a + (b - a) * k

# geometría (en coordenadas finales)
PX0, PY0, PX1, PY1 = 510, 430, 1410, 650
LIKE, DIS, BELL = (640, 528), (765, 528), (1300, 530)
BTN = (905, 494, 1195, 566)
PTS = [(1560, 900), (650, 545), (1050, 545), (1305, 548), (1600, 920)]  # recorrido del cursor
T_LIKE, T_SUB, T_BELL = 1.0, 1.9, 2.8

def thumb(d, cx, cy, s, fill, down=False):
    def p(x, y): return (cx + x * s, cy + (-y if down else y) * s)
    d.rounded_rectangle([p(-24, -2)[0], min(p(-24, -2)[1], p(-14, 24)[1]), p(-14, 24)[0], max(p(-24, -2)[1], p(-14, 24)[1])], radius=3 * s, fill=fill)
    d.rounded_rectangle([p(-10, -2)[0], min(p(-10, -2)[1], p(22, 24)[1]), p(22, 24)[0], max(p(-10, -2)[1], p(22, 24)[1])], radius=6 * s, fill=fill)
    d.polygon([p(-8, 0), p(2, -22), p(10, -20), p(8, 0)], fill=fill)
    c = p(6, -22); r = 5 * s; d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=fill)

def bell(d, cx, cy, s, filled):
    col = INK
    w = 6 * SS
    body = [(cx - 18 * s, cy + 14 * s), (cx - 15 * s, cy - 6 * s), (cx - 9 * s, cy - 18 * s), (cx, cy - 22 * s), (cx + 9 * s, cy - 18 * s), (cx + 15 * s, cy - 6 * s), (cx + 18 * s, cy + 14 * s)]
    if filled:
        d.polygon(body, fill=col)
        d.rounded_rectangle([cx - 24 * s, cy + 12 * s, cx + 24 * s, cy + 19 * s], radius=3 * s, fill=col)
    else:
        d.line(body, fill=col, width=w, joint="curve")
        d.line([(cx - 24 * s, cy + 16 * s), (cx + 24 * s, cy + 16 * s)], fill=col, width=w)
    d.ellipse([cx - 5 * s, cy + 20 * s, cx + 5 * s, cy + 29 * s], fill=col)
    d.ellipse([cx - 4 * s, cy - 28 * s, cx + 4 * s, cy - 20 * s], fill=col)

def cursor(d, x, y, s):
    pts = [(0, 0), (0, 34), (9, 26), (16, 41), (22, 38), (15, 23), (27, 23)]
    poly = [(x + px * s, y + py * s) for px, py in pts]
    d.polygon(poly, fill=(255, 255, 255), outline=(0, 0, 0))
    d.line(poly + [poly[0]], fill=(0, 0, 0), width=3 * SS // 2 + 1, joint="curve")

def cursor_pos(t):
    keys = [(0.3, PTS[0]), (0.85, PTS[1]), (1.15, PTS[1]), (1.75, PTS[2]), (2.05, PTS[2]), (2.65, PTS[3]), (3.6, PTS[3]), (4.1, PTS[4])]
    if t <= keys[0][0]: return keys[0][1]
    for (t0, a), (t1, b) in zip(keys, keys[1:]):
        if t <= t1:
            k = ease((t - t0) / (t1 - t0)); return (lerp(a[0], b[0], k), lerp(a[1], b[1], k))
    return keys[-1][1]

n = int(DUR * FPS)
for i in range(n):
    t = i / FPS
    img = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    lay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # entrada / salida del panel
    a_in = ease(t / 0.35); a_out = 1 - ease((t - 3.9) / 0.4)
    alpha = max(0, min(a_in, a_out)); dy = (1 - ease(t / 0.35)) * 60
    S = lambda v: int(v * SS)
    box = [S(PX0), S(PY0 + dy), S(PX1), S(PY1 + dy)]
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([box[0] + 8, box[1] + 14, box[2] + 8, box[3] + 14], radius=S(40), fill=(0, 0, 0, 90))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(S(14))))
    d.rounded_rectangle(box, radius=S(40), fill=(242, 242, 244, 255))
    oy = dy * SS
    liked = t >= T_LIKE; subbed = t >= T_SUB; bell_on = t >= T_BELL
    pr = lambda tc: 0.88 if tc <= t < tc + 0.12 else 1.0  # rebote al hacer clic
    s_like = SS * pr(T_LIKE) * (1.15 if T_LIKE + 0.12 <= t < T_LIKE + 0.3 else 1)
    thumb(d, S(LIKE[0]), S(LIKE[1]) + oy, s_like, BLUE if liked else INK)
    thumb(d, S(DIS[0]), S(DIS[1]) + oy + S(4), SS, INK, down=True)
    if liked:
        k = ease((t - T_LIKE) / 0.25)
        d.rounded_rectangle([S(590), S(592) + oy, S(590 + 225 * k), S(598) + oy], radius=S(3), fill=BLUE)
    # botón suscribirse
    sc = pr(T_SUB); cx, cy = (BTN[0] + BTN[2]) / 2, (BTN[1] + BTN[3]) / 2
    bw, bh = (BTN[2] - BTN[0]) * sc / 2, (BTN[3] - BTN[1]) * sc / 2
    d.rounded_rectangle([S(cx - bw), S(cy - bh) + oy, S(cx + bw), S(cy + bh) + oy], radius=S(12), fill=(GREY if subbed else RED))
    label = "Subscribed" if subbed else "Subscribe"
    tw = d.textlength(label, font=F)
    d.text((S(cx) - tw / 2, S(cy) + oy - S(21)), label, font=F, fill=(70, 70, 70) if subbed else (255, 255, 255))
    # campana
    ang = 0
    if bell_on and t < T_BELL + 0.6: ang = 18 * math.sin((t - T_BELL) * 40) * (1 - (t - T_BELL) / 0.6)
    bl = Image.new("RGBA", (S(120), S(120)), (0, 0, 0, 0)); bd = ImageDraw.Draw(bl)
    bell(bd, S(60), S(60), SS * pr(T_BELL), bell_on)
    bl = bl.rotate(ang, resample=Image.BICUBIC, center=(S(60), S(36)))
    lay.alpha_composite(bl, (S(BELL[0] - 60), S(BELL[1] - 60) + int(oy)))
    if bell_on and t < T_BELL + 0.8:  # rayitas de sonido
        k = ease((t - T_BELL) / 0.25); fa = int(255 * (1 - max(0, (t - T_BELL - 0.4) / 0.4)))
        for sgn in (-1, 1):
            for j, r in enumerate((34, 46)):
                x0 = S(BELL[0] + sgn * r); y0 = S(BELL[1] - 18) + oy
                d.line([(x0, y0), (x0 + sgn * S(8 * k), y0 - S(10 * k))], fill=(30, 30, 30, fa), width=S(4))
    # ondas de clic
    for tc, pt in ((T_LIKE, PTS[1]), (T_SUB, PTS[2]), (T_BELL, PTS[3])):
        if tc <= t < tc + 0.35:
            k = (t - tc) / 0.35; r = S(10 + 40 * k)
            d.ellipse([S(pt[0]) - r, S(pt[1]) + oy - r, S(pt[0]) + r, S(pt[1]) + oy + r], outline=(120, 120, 120, int(200 * (1 - k))), width=S(4))
    # cursor
    if 0.3 <= t <= 4.1:
        x, y = cursor_pos(t); cs = SS * (0.85 if any(tc <= t < tc + 0.12 for tc in (T_LIKE, T_SUB, T_BELL)) else 1.0) * 1.6
        cursor(d, S(x), S(y) + oy, cs)
    if alpha < 1:
        a = lay.getchannel("A").point(lambda v: int(v * alpha)); lay.putalpha(a)
    img.alpha_composite(lay)
    img.resize((W, H), Image.LANCZOS).save(f"{OUT}/f{i:04d}.png")
print(n)
