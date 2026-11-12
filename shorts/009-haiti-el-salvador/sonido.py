"""Short 009 (El Salvador en Haití) · diseño de sonido estéreo tono noticiero (todo sintetizado aquí, sin derechos) + mezcla con la voz.
    python3 shorts/009-haiti-el-salvador/sonido.py      (después de construir.py y del render)
- Cada capa del mapa tiene su sonido: el país que desaparece (grieta + golpe + ola), cada cifra (succión + golpe de cine),
  cada título, cinta, pin, flujo (y el corte cuando se rompe), cada zoom o paneo de cámara (con paneo estéreo según el movimiento).
- Escenas reales: barrido de entrada y salida + su ambiente (olas, cascada, viento, selva, taza).
- Música original trap/cinemática a 130 BPM; frena en seco en el giro y vuelve con todo. La voz no se toca.
"""
import json, subprocess, wave
from pathlib import Path
import numpy as np
from scipy import signal
import sys
D = Path(__file__).resolve().parent; SR = 48000
rng = np.random.default_rng(7)
tt = lambda d: np.arange(int(d * SR)) / SR
nz = lambda d: rng.standard_normal(int(d * SR))
def filt(x, kind, f, order=2): return signal.sosfilt(signal.butter(order, f, btype=kind, fs=SR, output='sos'), x)
def norm(x, p=1.0): m = np.abs(x).max(); return (x / m * p if m > 0 else x).astype(np.float32)
def env_ar(n, a, r): e = np.ones(n); ia, ir = min(n, int(a * SR)), min(n, int(r * SR)); e[:ia] = np.linspace(0, 1, ia) if ia else e[:ia]; e[n - ir:] = np.minimum(e[n - ir:], np.linspace(1, 0, ir)) if ir else e[n - ir:]; return e
def fase(f): return 2 * np.pi * np.cumsum(f) / SR
def bandas(x, centro, ancho=.35):
    """Filtro de banda que se mueve en el tiempo (centro en Hz por muestra): mezcla 12 bandas fijas con pesos gaussianos en escala log."""
    fs = np.geomspace(150, 9000, 12); out = np.zeros_like(x); lc = np.log(np.maximum(centro, 60))
    for i, f in enumerate(fs):
        lo, hi = f / 1.35, min(f * 1.35, SR / 2 - 100); b = signal.sosfilt(signal.butter(2, [lo, hi], btype='band', fs=SR, output='sos'), x)
        out += b * np.exp(-((np.log(f) - lc) ** 2) / (2 * ancho ** 2))
    return out

# ======================= EFECTOS =======================
def gota_agua():  # "plip" con chirrido hacia arriba (como una gota real) + burbuja
    t = tt(.5); a = np.sin(fase(700 + 2100 * (1 - np.exp(-t * 60)))) * np.exp(-t * 38); b = np.sin(fase(420 + 380 * (1 - np.exp(-t * 25)))) * np.exp(-np.maximum(0, t - .02) * 22) * (t > .02) * .5
    return norm(a + b + filt(nz(.5), 'high', 3000) * np.exp(-t * 200) * .15)
def boom(d=1.6, f0=150, f1=40, dist=2.2):  # 808 / boom de cine
    t = tt(d); s = np.sin(fase(f1 + (f0 - f1) * np.exp(-t * 11))) * np.exp(-t * 2.3); s = np.tanh(s * dist) / np.tanh(dist)
    s[:int(.006 * SR)] += filt(nz(.006), 'high', 2000) * .5; return norm(s)
def impacto():  # golpe de tráiler: sub + golpe grave + metal + platillo
    d = 2.4; t = tt(d); s = boom(d, 160, 38) * .9 + filt(nz(d), 'low', 300) * np.exp(-t * 18) * 1.2
    metal = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in [(183, 5), (417, 6), (689, 7), (1131, 8), (1866, 10), (2937, 12)]) * .12
    plat = filt(nz(d), 'high', 3500) * np.exp(-t * 4) * .35; return norm(s + metal + plat)
def succion(d=.9):  # "reverse": se aspira hacia el golpe
    t = tt(d); x = filt(nz(d), 'band', [500, 6000]) * (t / d) ** 3 + sum(np.sin(2 * np.pi * f * t) for f in (220, 330, 495)) * (t / d) ** 4 * .08
    return norm(x * env_ar(len(t), .01, .01))
def barrido(d=.45, f0=500, fp=3200, f1=900, aire=.25):  # whoosh real: banda de ruido que sube y baja (sin silbido)
    t = tt(d); u = t / d; c = np.where(u < .42, f0 * (fp / f0) ** (u / .42), fp * (f1 / fp) ** ((u - .42) / .58)); x = bandas(nz(d), c, .32)
    e = np.where(u < .45, (u / .45) ** 1.6, ((1 - u) / .55) ** 1.4); x = x * e + filt(nz(d), 'high', 5000) * e * aire * .3; return norm(x)
def zoom_in(d=.55):  # sube hacia el detalle y termina en un clic
    t = tt(d); u = t / d; ruido = bandas(nz(d), 300 * (5000 / 300) ** u, .3) * u ** 1.5
    saw = sum(np.sin(k * fase(70 + 220 * u ** 2)) / k for k in range(1, 9)); saw = filt(saw, 'low', 1400) * u ** 2 * .35
    x = ruido + saw; x[-int(.008 * SR):] += filt(nz(.008), 'high', 2500) * 1.5; return norm(x)
def zoom_out(d=.6): x = zoom_in(d)[::-1].copy(); t = tt(d); return norm(x * np.exp(-t * 1.5) + boom(d, 90, 45, 1.5)[:len(x)] * .35)
def pop(f=620):  # pop de interfaz nítido
    t = tt(.12); s = np.sin(fase(f * (1 + .9 * np.exp(-t * 90)))) * np.exp(-t * 42); s[:int(.003 * SR)] += filt(nz(.003), 'high', 3000) * .6; return norm(s)
def tic(): t = tt(.02); return norm((np.sin(2 * np.pi * 2600 * t) + .3 * np.sin(2 * np.pi * 7800 * t)) * np.exp(-t * 260))
def campana(f=1318.5):  # campana FM brillante
    t = tt(1.6); idx = 3.5 * np.exp(-t * 4); return norm(np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * 3.5 * t)) * np.exp(-t * 3.2))
def papel(d=.32):  # hoja que se voltea (crujido real con chasquidos)
    t = tt(d); x = filt(nz(d), 'band', [700, 7000]) * np.exp(-((t - d * .4) / (d * .25)) ** 2)
    for _ in range(40): i = int(rng.uniform(.05, .8) * d * SR); L = int(.002 * SR); x[i:i + L] += rng.uniform(-1, 1) * 1.5
    return norm(x + filt(nz(d), 'low', 180) * np.exp(-t * 25) * .8)
def plegar(): a = papel(.42); b = boom(.44, 110, 50, 1.4) * .35; n = max(len(a), len(b)); return norm(np.pad(a, (0, n - len(a))) + np.pad(b, (0, n - len(b))))
def trueno(d=3.2):
    t = tt(d); crack = filt(nz(d), 'high', 1400) * np.exp(-t * 22) * 1.3; br = filt(np.cumsum(nz(d)) * .02, 'high', 25)
    am = filt(np.abs(nz(d)), 'low', 6); rumble = filt(br, 'low', 170) * (am / am.max()) * np.minimum(1, t / .12) * np.exp(-t / 1.1) * 3; return norm(crack + rumble)
def lluvia(d, k=1.0):
    t = tt(d); x = filt(filt(nz(d), 'high', 500), 'low', 7500) * .35
    gotas = np.zeros(len(t)); idx = rng.integers(0, len(t), int(d * 420 * k)); gotas[idx] = rng.uniform(-1, 1, len(idx)); x += filt(gotas, 'high', 2500) * 1.6
    return norm(x * env_ar(len(t), .5, .6) * (1 + .15 * np.sin(2 * np.pi * .3 * t)))
def viento(d, sube=True):
    t = tt(d); u = t / d; c = 260 + 420 * (.5 + .5 * np.sin(2 * np.pi * .35 * t + 1)); x = bandas(nz(d), c, .45)
    return norm(x * ((u ** 1.3) if sube else np.sin(np.pi * u)) * env_ar(len(t), .05, .3))
def brillo(d=.7):  # destellos cortos (escarcha / chispas), sin notas largas
    t = tt(d); x = np.zeros(len(t))
    for _ in range(int(d * 34)): i = int(rng.uniform(0, d - .03) * SR); f = rng.uniform(2200, 5200); n = int(.025 * SR); x[i:i + n] += np.sin(2 * np.pi * f * tt(.025)) * np.exp(-tt(.025) * 160) * rng.uniform(.3, 1)
    return norm(x * env_ar(len(t), .05, .2))
def chisporroteo(d=2.2):
    t = tt(d); g = np.zeros(len(t)); idx = rng.integers(0, len(t), int(d * 700)); g[idx] = rng.uniform(-1, 1, len(idx)); x = filt(g, 'high', 1800) * 1.5 + filt(nz(d), 'high', 4500) * .12
    return norm(x * np.minimum(1, t / .8) * env_ar(len(t), .01, .4))
def agua_corre(d=2.4):
    t = tt(d); x = filt(nz(d), 'low', 900) * (.6 + .4 * np.sin(2 * np.pi * .8 * t)) * .6
    for _ in range(int(d * 22)): i = int(rng.uniform(0, d - .05) * SR); n = int(.04 * SR); tb = tt(.04); x[i:i + n] += np.sin(fase(rng.uniform(220, 520) * (1 + 1.5 * tb / .04))) * np.exp(-tb * 60) * .5
    return norm(x * env_ar(len(t), .25, .6))
def oleaje(d): t = tt(d); return norm(filt(nz(d), 'low', 520) * (.55 + .45 * np.sin(2 * np.pi * t / 3.2 - 1.5)) * env_ar(len(t), .6, .8))
def cascabeles(d=1.6, paso=.16):  # cascabeles de Navidad
    t = tt(d); x = np.zeros(len(t)); parciales = [(2950, 1), (4120, .7), (5330, .5), (6810, .35)]
    for k in range(int(d / paso)):
        for _ in range(10):
            i = int((k * paso + rng.uniform(0, .04)) * SR); n = int(.06 * SR)
            if i + n >= len(t): continue
            tb = tt(.06); x[i:i + n] += sum(a * np.sin(2 * np.pi * f * rng.uniform(.97, 1.03) * tb) for f, a in parciales) * np.exp(-tb * 70) * rng.uniform(.2, .6)
    return norm(x * env_ar(len(t), .02, .5))
def trinquete(d=1.2):  # la rosa de los vientos girando
    x = np.zeros(int(d * SR)); t = 0.0
    while t < d - .02: u = t / d; i = int(t * SR); n = int(.012 * SR); x[i:i + n] += filt(nz(.012), 'band', [1400, 3400]) * np.exp(-tt(.012) * 300); t += .02 + .07 * (2 * abs(u - .5)) ** 1.5
    return norm(x)
def pluck(f, d=.5):  # marimba/pluck para los pines
    t = tt(d); return norm((np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30) + .2 * np.sin(2 * np.pi * f * 2.01 * t)) * np.exp(-t * 7))
def riser(d=1.6):
    t = tt(d); u = t / d; return norm(bandas(nz(d), 600 * (7000 / 600) ** u, .4) * u ** 2.2 + filt(nz(d), 'high', 6000) * u ** 4 * .4)
def nube_paso(d=1.1): return norm(barrido(d, 220, 1500, 300, .1) + filt(nz(d), 'low', 260) * np.sin(np.pi * tt(d) / d) * .6)

# ======================= MÚSICA =======================
BPM = 130; BEAT = 60 / BPM; PASO = BEAT / 4
ACORDES = [(73.42, [293.66, 349.23, 440.0]), (58.27, [233.08, 293.66, 349.23]), (87.31, [349.23, 440.0, 523.25]), (65.41, [261.63, 329.63, 392.0])]  # Rem · Sib · Fa · Do
def musica(dur, secc, golpes, tape):
    N = int((dur + 3) * SR); L = np.zeros(N); R = np.zeros(N); envio = np.zeros(N); kicks = []
    def put(t0, s, g, p=0., rev=0.):
        i = int(t0 * SR)
        if i < 0 or i >= N: return
        j = min(N, i + len(s)); s = s[:j - i]; L[i:j] += g * s * np.cos((p + 1) * np.pi / 4) * 1.41; R[i:j] += g * s * np.sin((p + 1) * np.pi / 4) * 1.41; envio[i:j] += g * s * rev
    t = tt(.5); kick = norm(np.tanh(np.sin(fase(45 + 115 * np.exp(-t * 28))) * np.exp(-t * 7) * 2.5)); kick[:int(.004 * SR)] += filt(nz(.004), 'high', 3000) * .4
    t = tt(.3); n = nz(.3); palma = norm(sum(filt(n, 'band', [900, 5200]) * np.exp(-np.maximum(0, t - k * .011) * 28) * (t >= k * .011) for k in range(3)))
    t = tt(.05); hat = norm(filt(nz(.05), 'high', 7000) * np.exp(-t * 95)); t = tt(.25); hato = norm(filt(nz(.25), 'high', 6500) * np.exp(-t * 16))
    def bajo808(f, f2, d):
        t = tt(d); fr = np.where(t > d - .07, f * (f2 / f) ** ((t - (d - .07)) / .07), f); s = np.sin(fase(fr)); s = np.tanh(s * 1.8) * np.minimum(1, t / .005) * np.exp(-t * .9); return norm(s * env_ar(len(t), .003, .03))
    def pad(fs, d):
        t = tt(d); s = sum(sum(np.sin(2 * np.pi * f * k * (1 + dt) * t) / k for k in range(1, 7)) for f in fs for dt in (-.004, .004)); return norm(filt(s, 'low', 1700) * env_ar(len(t), .5, .6))
    def plk(f, d=.28): t = tt(d); s = sum(np.sin(2 * np.pi * f * k * t) / k * np.exp(-t * (10 + 4 * k)) for k in range(1, 8)); return norm(s)
    def modo(t0):
        m = secc[0][1]
        for ts, x in secc:
            if t0 >= ts - 1e-6: m = x
        return m
    nb = int(dur / BEAT) + 2
    for bt in range(nb):
        t0 = bt * BEAT; mo = modo(t0); raiz, notas = ACORDES[(bt // 4) % 4]; sig = ACORDES[((bt // 4) + 1) % 4][0]
        if mo == 'nada': continue
        if bt % 4 == 0: put(t0, pad([f / 2 for f in notas], BEAT * 4), .1 if mo != 'oscuro' else .13, 0, .5)
        if mo in ('completo', 'final', 'oscuro') and bt % 4 == 0: put(t0, bajo808(raiz, sig, BEAT * (4 if mo != 'oscuro' else 2)), .42 if mo != 'oscuro' else .32)
        for s16 in range(4):
            ts = t0 + s16 * PASO; paso_bar = (bt % 4) * 4 + s16
            if mo in ('completo', 'final'):
                if paso_bar in (0, 7, 10): put(ts, kick, .62); kicks.append(ts)
                if paso_bar == 8: put(ts, palma, .34, 0, .35)
                if s16 % 2 == 0: put(ts, hat, .09 + .03 * (s16 == 2), .25 * (1 if s16 == 2 else -1))
                if paso_bar in (14, 15) and (bt // 4) % 2 == 1:
                    for k in range(3): put(ts + k * PASO / 3, hat, .07, .3)
                if paso_bar == 6 and (bt // 4) % 4 == 3: put(ts, hato, .06, -.3)
                nota = notas[[0, 1, 2, 1][paso_bar % 4]] * (2 if paso_bar % 8 >= 4 else 1); put(ts, plk(nota), .055 if mo == 'completo' else .07, .35 * np.sin(paso_bar), .4)
                if mo == 'final' and s16 == 0 and bt % 2 == 0: put(ts, plk(notas[(bt // 2) % 3] * 2, .5), .06, 0, .5)
            elif mo == 'ligero':
                if s16 % 2 == 0: put(ts, hat, .05, .2)
                if s16 in (0, 3) : put(ts, plk(notas[(bt + s16) % 3] * 2, .4), .045, -.3 + .6 * (s16 == 3), .6)
            elif mo == 'oscuro':
                if bt % 2 == 0 and s16 == 0: put(ts, kick, .4); kicks.append(ts)
    for g in golpes:  # un tiempo de vacío antes del golpe + subida
        i0, i1 = int((g - BEAT) * SR), int(g * SR)
        if i0 > 0: f = np.linspace(1, .12, i1 - i0); L[i0:i1] *= f; R[i0:i1] *= f
    # bombeo de los pads con el bombo
    bomb = np.ones(N)
    for k in kicks: i = int(k * SR); n = min(N - i, int(.22 * SR)); bomb[i:i + n] = np.minimum(bomb[i:i + n], .45 + .55 * (np.arange(n) / n) ** .6)
    rv = reverb(envio, 1.8); L = (L + rv[0] * .45) * bomb ** .4; R = (R + rv[1] * .45) * bomb ** .4
    # frenazo de cinta en el giro de la historia
    for t0 in tape:
        i = int(t0 * SR); d = int(.7 * SR); vel = np.linspace(1, 0, d) ** 1.4; pos = np.cumsum(vel); pos = (pos / pos[-1] * d * .5).astype(int)
        for ch in (L, R): seg = ch[i:i + d].copy(); ch[i:i + d] = seg[np.clip(pos, 0, len(seg) - 1)] * np.linspace(1, 0, d) ** .5
    return np.stack([L, R])[:, :int(dur * SR)]
def reverb(x, rt=1.6):
    n = int(rt * SR); t = np.arange(n) / SR; out = []
    for s in (11, 23):
        ir = np.random.default_rng(s).standard_normal(n) * np.exp(-6.9 * t / rt); ir = filt(ir, 'low', 6500); ir[:int(.012 * SR)] = 0; out.append(signal.fftconvolve(x, ir)[:len(x)] / np.sqrt(n) * 3)
    return out


# ======================= MEZCLA =======================
def leer(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
sp = json.load(open(D / 'mapa.json')); ev = sp['eventos']; dur = sp['duracion']; N = int(dur * SR); cam = sp['camara']
fv = D / '.tmp' / 'voz.wav'; CON_VOZ = fv.exists() and 'audio' in sp
voz = leer(fv) if CON_VOZ else np.zeros(N, np.float32); voz = np.pad(voz, (0, max(0, N - len(voz))))[:N]
FX = np.zeros((2, N + 8 * SR)); ENV = np.zeros(N + 8 * SR)
def fx(t0, s, g, p=0., rev=.15, mov=None):
    i = int(max(0, t0) * SR); j = min(FX.shape[1], i + len(s)); s = s[:j - i]
    pp = np.linspace(mov[0], mov[1], len(s)) if mov else np.full(len(s), p); FX[0, i:j] += g * s * np.cos((pp + 1) * np.pi / 4) * 1.41; FX[1, i:j] += g * s * np.sin((pp + 1) * np.pi / 4) * 1.41; ENV[i:j] += g * s * rev
def cam_en(t):
    k = cam[0]
    for a, b in zip(cam, cam[1:]):
        if a['t'] <= t <= b['t']: u = (t - a['t']) / max(1e-3, b['t'] - a['t']); return {q: a[q] + (b[q] - a[q]) * u for q in ('lon', 'lat', 'ancho')}
        k = b
    return k
def pan_lon(t, lon): c = cam_en(t); return float(np.clip((lon - c['lon']) / (c['ancho'] / 2), -1, 1)) * .7
def grieta(d=.5):
    s = np.zeros(int(d * SR))
    for k in range(10): i = int(rng.uniform(0, d * .6) * SR); L = int(.025 * SR); s[i:i + L] += filt(nz(.025), 'high', 1500)[:len(s[i:i + L])] * np.exp(-np.arange(min(L, len(s) - i)) / SR * 110) * rng.uniform(.4, 1)
    return norm(s + .25 * boom(d, 90, 40, 1.5)[:len(s)])
def ola(d=2.2): t = tt(d); return norm(filt(nz(d), 'low', 700) * np.minimum(1, t / .3) * np.exp(-np.maximum(0, t - .3) * 1.6))
def cascada(d): return norm(filt(nz(d), 'low', 1400) * .8 + filt(nz(d), 'band', [1500, 5000]) * .25)
def selva(d):
    s = filt(nz(d), 'low', 300) * .15
    for k in range(int(d * 2.5)):
        f0 = rng.uniform(2300, 4300); L = int(rng.uniform(.06, .15) * SR); x = np.arange(L) / SR; i = int(rng.uniform(0, max(.01, d - .2)) * SR)
        ch = np.sin(fase(f0 + 900 * np.sin(2 * np.pi * rng.uniform(18, 40) * x))) * np.sin(np.pi * x / x[-1]) ** 2; s[i:i + L] += ch[:len(s[i:i + L])] * rng.uniform(.3, .9)
    return norm(s)
def taza(): t = tt(.7); return norm(sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in [(2637, .6, 9), (3951, .3, 14), (5274, .15, 20)]))
def rotor(d):  # helicóptero: golpes de pala ~17 Hz + turbina
    t = tt(d); golpe = (np.sin(2 * np.pi * 17 * t) > .6).astype(float); s = filt(nz(d), 'low', 500) * (.35 + .65 * filt(golpe, 'low', 60)) + .15 * filt(nz(d), 'band', [2500, 6000])
    return norm(s * np.minimum(1, t / .5))
def motor(d): t = tt(d); return norm(filt(nz(d), 'low', 180) * (.8 + .2 * np.sin(2 * np.pi * 3 * t)) + .3 * np.sin(2 * np.pi * 48 * t))
def murmullo(d): return norm(filt(nz(d), 'band', [300, 1800]) * (.6 + .4 * filt(np.abs(nz(d)), 'low', 3)))
def ambiente(cod, d):
    if cod == 'N01': return viento(d, False) * .7 + murmullo(d) * .3, .2
    if cod == 'N02': return viento(d, False), .26
    if cod == 'N03': return motor(d) * .7 + viento(d, False) * .3, .32
    if cod == 'N04': return rotor(d), .38
    if cod == 'N05': return motor(d) * .8 + viento(d, False) * .4, .3
    if cod == 'N06': return murmullo(d), .18
    return None, 0
impactos = []; npin = 0; PENTA = [293.66, 349.23, 392.0, 440.0, 523.25, 587.33, 698.46, 783.99]
for d in sp.get('desaparece', []):  # el país que desaparece
    t0 = d['t']; fx(t0 - .9, succion(.9), .42, 0, .3); fx(t0 - .05, grieta(), .5, 0, .2); fx(t0, impacto(), .75, 0, .55); fx(t0, boom(2.4, 170, 32, 3.4), .62, 0, .1); fx(t0 + .25, ola(2.4), .45, 0, .3, mov=(-.5, .5)); impactos.append(t0)
for e in sorted(ev, key=lambda e: e['desde']):
    tp, t0 = e['tipo'], e['desde']; t1 = e.get('hasta', t0 + 2); p = pan_lon(t0, e['lon']) if 'lon' in e else 0
    if tp == 'cifra': fx(t0 - .8, succion(.8), .3, 0, .2); fx(t0, impacto(), .58, 0, .45); fx(t0, boom(1.5, 160, 38, 3), .5, 0, .1); impactos.append(t0)
    elif tp == 'titulo': fx(t0 - .3, barrido(.34, 600, 3000, 1100, .15), .26, 0, .1); fx(t0, boom(.7, 120, 50, 1.8), .36, 0, .15); fx(t0, pop(420), .3, 0, .2)
    elif tp == 'cinta': fx(t0 - .15, barrido(.25, 900, 3800, 1600, .1), .2, 0, .05); fx(t0, boom(.5, 140, 60, 1.6), .34, 0, .15); fx(t0 + .03, pop(760), .3, 0, .2)
    elif tp == 'sello': fx(t0 - .5, succion(.5), .3, 0, .2); fx(t0, impacto(), .6, 0, .5); impactos.append(t0)
    elif tp == 'pin': fx(t0, pluck(PENTA[npin % len(PENTA)]), .32, p, .35); fx(t0, pop(1100), .14, p, .1); npin += 1
    elif tp == 'nombre': fx(t0, pop(640 + (npin % 4) * 90), .3, p, .2); npin += 1
    elif tp == 'globo': fx(t0, pop(950), .34, p, .2); fx(t0 + .08, pop(1250), .2, p, .2)
    elif tp == 'resaltar': fx(t0, brillo(.5), .14, p, .3); fx(t0, pop(700), .2, p, .15)
    elif tp == 'iconos':
        for i, _ in enumerate(e['items']): fx(t0 + i * e.get('paso', .35), pop(620 + i * 120), .32, -.3 + .6 * i, .2); fx(t0 + i * e.get('paso', .35), boom(.4, 160, 80, 1.2), .2, 0, .1)
    elif tp == 'flujo':
        fx(t0, barrido(1.0, 300, 1800, 600, .1), .18, 0, .1, mov=(-.5, .5)); ic = e.get('icono')
        if ic == 'gota' and not e.get('roto'): fx(t0 + .1, agua_corre(min(2.4, t1 - t0)), .16, 0, .2)
        if ic == 'nube' and not e.get('roto'): fx(t0, nube_paso(1.2), .3, 0, .3)
        if e.get('roto'): fx(t0 + .6, grieta(.4), .32, 0, .2); fx(t0 + .6, boom(.6, 120, 50, 1.6), .26, 0, .1)
    elif tp == 'apagon': fx(t0, chisporroteo(1.6), .3, 0, .2); fx(t0 + .05, boom(1.8, 110, 30, 2.2), .45, 0, .3); fx(t0 + .3, succion(.6)[::-1].copy(), .22, 0, .2); impactos.append(t0)
    elif tp == 'pregunta': fx(t0 - .3, barrido(.4, 700, 3200, 1200, .2), .26, 0, .1); fx(t0, campana(1318.5), .2, 0, .4)
for c in sp.get('clips', []):  # escenas reales
    t0, t1 = c['desde'], c['hasta']
    if t0 > .2: fx(t0 - .28, barrido(.42, 400, 3600, 900, .2), .34, 0, .15, mov=(.7, -.7)); fx(t0, boom(.6, 130, 55, 1.6), .26, 0, .15)
    s, g = ambiente(c['codigo'], t1 - t0 + .6)
    if s is not None: fx(t0 - .2, s * env_ar(len(s), .3, .45), g, 0, .1)
for a, b in zip(cam, cam[1:]):  # cámara
    d = b['t'] - a['t']
    if a.get('suave') is not False or not (0 < d < 1.9) or (a['lon'], a['lat'], a['ancho']) == (b['lon'], b['lat'], b['ancho']): continue
    if any(c['desde'] - .1 < a['t'] < c['hasta'] for c in sp.get('clips', [])): continue
    r = b['ancho'] / a['ancho']; dirx = float(np.sign(b['lon'] - a['lon'])) if abs(b['lon'] - a['lon']) > .3 else 0
    if r < .72: fx(a['t'] - .03, zoom_in(min(d, .9) + .05), .34, 0, .1)
    elif r > 1.35: fx(a['t'] - .03, zoom_out(min(d, .9) + .1), .34, 0, .15)
    else: fx(a['t'] - .03, barrido(max(.3, min(d, .9) + .05), 400, 3000, 800, .2), .32, 0, .1, mov=(dirx * .8, -dirx * .8))
for p in sp.get('palabras', []): fx(p['t0'], tic(), .03, 0, .02)  # un clic suave en cada palabra
# música: arranca con todo, frena en seco antes del final y vuelve con el cierre
cl = sp.get('clips', []); giro = [e['desde'] for e in ev if e['tipo'] == 'titulo'][1:2]
secc = [(0, 'oscuro')]; tape = []
tit = {e.get('texto', ''): e['desde'] for e in ev if e['tipo'] == 'titulo'}
resp = next((v for k, v in tit.items() if 'RESPUESTA' in k), None); fin = next((v for k, v in tit.items() if 'APARECER' in k), None)
if resp: secc += [(resp - .05, 'completo')]
if fin: tape.append(fin - .6); secc += [(fin - .05, 'nada'), (fin + 1.0, 'oscuro')]
secc += [(dur - 4.0, 'final')]; secc.sort()
mus = musica(dur, secc, sorted(set(round(i, 2) for i in impactos if i > 1)), tape)
mus *= np.clip(1 - (np.arange(N) / SR - (dur - 1.0)) / 1.0, 0, 1)
rv = reverb(ENV[:N], 1.5); fxL = FX[0, :N] + rv[0] * .5; fxR = FX[1, :N] + rv[1] * .5
envv = filt(np.abs(voz), 'low', 8); duck = 1 - .6 * np.clip(envv / (np.percentile(envv, 96) * .45 + 1e-9), 0, 1) if CON_VOZ else np.ones(N)
duck_fx = 1 - .45 * (1 - duck) / .6 if CON_VOZ else np.ones(N); gm = .2 if CON_VOZ else .48
mix = np.stack([voz + mus[0] * duck * gm + fxL * duck_fx * .56, voz + mus[1] * duck * gm + fxR * duck_fx * .56]); mix /= max(1, np.abs(mix).max())
tmp = D / '.tmp'; tmp.mkdir(exist_ok=True)
with wave.open(str(tmp / 'mezcla.wav'), 'w') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix.T, -1, 1) * 32767).astype(np.int16).tobytes())
med = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(tmp / 'mezcla.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
med = json.loads(med[med.rindex('{'):med.rindex('}') + 1]); gan = min(5.0, -14.0 - float(med['input_i']))
video = D / (sp['salida'] + '.mp4'); out = D / (sp['salida'] + ('-final.mp4' if CON_VOZ else '-vista-previa.mp4'))
if '--solo-audio' not in sys.argv:
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(video), '-i', str(tmp / 'mezcla.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', f'volume={gan:.2f}dB,alimiter=limit=0.8:attack=4:release=70:level=disabled', '-ar', '48000', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', str(out)], check=True)
print(('CON VOZ' if CON_VOZ else 'SIN VOZ'), f'· {dur:.1f} s · {len(impactos)} golpes · {out.name}')
