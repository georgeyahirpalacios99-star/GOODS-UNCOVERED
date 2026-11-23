"""Video 007 (Sinaloa) · sonido sintetizado sin derechos (música baja + efectos + ambientes) y mezcla con la voz.
    python3 videos-largos/007-sinaloa-desaparece/sonido.py
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


def leer(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
sp = json.load(open(D / 'mapa.json')); ev = sp['eventos']; dur = sp['duracion']; N = int(dur * SR); cam = sp['camara']
fv = D / '.tmp' / 'voz.wav'; CON_VOZ = fv.exists() and 'audio' in sp
voz = leer(fv) if CON_VOZ else np.zeros(N, np.float32); voz = np.pad(voz, (0, max(0, N - len(voz))))[:N]
FX = np.zeros((2, N + 8 * SR)); ENV = np.zeros(N + 8 * SR)
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
def arena(d, k=1.0):  # arena que corre: siseo agudo que va y viene con las ráfagas
    t = tt(d); r = .55 + .45 * np.sin(2 * np.pi * .45 * t + 1) * np.sin(2 * np.pi * .13 * t); return norm((filt(nz(d), 'band', [2500, 9000]) * .5 * r + viento(d, False) * .9) * k)
def tormenta(d): t = tt(d); return norm(viento(d, True) * 1.2 + filt(nz(d), 'low', 140) * (.6 + .4 * np.sin(2 * np.pi * .7 * t)) * 1.4 * np.minimum(1, t / .4) + filt(nz(d), 'band', [1800, 6000]) * .25 * (t / d))
def ciudad(d): t = tt(d); return norm(murmullo(d) * .5 + filt(nz(d), 'low', 220) * .8 + viento(d, False) * .7)
def pala(d):  # golpes de pala en arena + paja
    s = filt(nz(d), 'band', [1500, 6000]) * .08
    for k in range(int(d / .55) + 1): i = int((.12 + k * .55) * SR); x = papel(.3) * .9 + boom(.3, 90, 50, 1.2)[:int(.3 * SR)] * .5; j = min(len(s), i + len(x)); s[i:j] += x[:j - i]
    return norm(s)
def goteo(d):
    s = filt(nz(d), 'band', [300, 2000]) * .05
    for k in range(int(d / .7) + 1): i = int((.25 + k * .7) * SR); x = gota_agua(); j = min(len(s), i + len(x)); s[i:j] += x[:j - i] if j > i else 0
    return norm(s)
def seco(d):  # ramas secas que crujen con el viento
    s = viento(d, False) * .7
    for k in range(int(d * 1.6)): i = int(rng.uniform(0, max(.05, d - .1)) * SR); L = int(.03 * SR); s[i:i + L] += filt(nz(.03), 'high', 1800)[:len(s[i:i + L])] * np.exp(-np.arange(len(s[i:i + L])) / SR * 120) * rng.uniform(.3, .9)
    return norm(s)
def hojas(d): t = tt(d); return norm(filt(nz(d), 'band', [1800, 7000]) * (.5 + .5 * np.sin(2 * np.pi * .6 * t)) * .6 + viento(d, False) * .5)
def sala(d): t = tt(d); return norm(filt(nz(d), 'low', 200) * .6 + sum(np.sin(2 * np.pi * f * t) * (.5 + .5 * np.sin(2 * np.pi * .4 * t + f)) for f in (110, 164.8, 220)) * .12)
def billetes(d):
    s = filt(nz(d), 'low', 250) * .1
    for k in range(int(d / .42) + 1): i = int((.15 + k * .42) * SR); x = papel(.22); j = min(len(s), i + len(x)); s[i:j] += x[:max(0, j - i)]
    return norm(s)
def bodega(d):
    s = filt(nz(d), 'low', 300) * .5 + filt(nz(d), 'band', [3000, 7000]) * .04
    for k in range(int(d / 1.6) + 1): i = int((.5 + k * 1.6) * SR); x = boom(.35, 100, 55, 1.3); j = min(len(s), i + len(x)); s[i:j] += x[:max(0, j - i)] * .8
    return norm(s)
def caja():  # caja registradora: campanita doble + monedas
    a = campana(2093); b2 = campana(2637); n = len(a); x = a * .7; x[int(.07 * SR):] += b2[:n - int(.07 * SR)] * .6
    for _ in range(14): i = int(rng.uniform(.05, .5) * SR); L = int(.02 * SR); x[i:i + L] += np.sin(2 * np.pi * rng.uniform(4000, 7000) * tt(.02)) * np.exp(-tt(.02) * 200) * .35
    return norm(x[:int(.9 * SR)])
def puerto(d): t = tt(d); return norm(oleaje(d) * .8 + filt(nz(d), 'low', 160) * .6 + viento(d, False) * .4)
def tren(d): t = tt(d); return norm(filt(nz(d), 'low', 260) * (.7 + .3 * np.sin(2 * np.pi * 2.2 * t)) + filt(nz(d), 'band', [1800, 4500]) * .08 * (np.sin(2 * np.pi * 4.4 * t) > .7))
def fx(t0, s, g, p=0., rev=.15, mov=None):
    i = int(max(0, t0) * SR); j = min(FX.shape[1], i + len(s)); s = s[:j - i]
    pp = np.linspace(mov[0], mov[1], len(s)) if mov else np.full(len(s), p); FX[0, i:j] += g * s * np.cos((pp + 1) * np.pi / 4) * 1.41; FX[1, i:j] += g * s * np.sin((pp + 1) * np.pi / 4) * 1.41; ENV[i:j] += g * s * rev

# ======================= EFECTOS ATADOS A LAS CAPAS DEL ESTILO PRO =======================
def amb_clip(cod, d):
    return {'S01': (viento(d, True), .26), 'S02': (murmullo(d) * .8 + filt(nz(d), 'low', 200) * .3, .2), 'S05': (chisporroteo(d), .22), 'S10': (viento(d, False), .2),
            'S16': (viento(d, False) * .7 + hojas(d) * .3, .2), 'S22': (puerto(d), .3), 'S31': (murmullo(d) * 1.1, .28), 'S35': (murmullo(d) * 1.2 + filt(nz(d), 'low', 120) * .5, .32),
            'S41': (seco(d) * .6 + viento(d, True) * .6, .26), 'S45': (sala(d), .18)}.get(cod, (None, 0))
impactos = []; npin = 0; PENTA = [293.66, 349.23, 392.0, 440.0, 523.25, 587.33, 698.46, 783.99]
for e in sorted(ev, key=lambda e: e['desde']):
    tp, t0 = e['tipo'], e['desde']; t1 = e.get('hasta', t0 + 2)
    p = pan_lon(t0, e['en'][0]) if isinstance(e.get('en'), list) else (float(np.clip((e['en']['x'] - 960) / 960, -1, 1)) * .6 if isinstance(e.get('en'), dict) else 0)
    if tp == 'hueco':
        ts = e.get('t', t0 + 1.6); fx(ts - .9, succion(.9), .38, 0, .3); fx(ts - .05, grieta(), .42, 0, .2); fx(ts, impacto(), .62, 0, .5); fx(ts, boom(2.2, 170, 32, 3.2), .52, 0, .1); fx(ts + .2, ola(2.2), .3, 0, .3, mov=(-.5, .5)); impactos.append(ts)
    elif tp == 'dato' and e.get('num'):
        fx(t0 - .5, succion(.5), .22, 0, .2)
        for q in range(int(1.1 / .05)): fx(t0 + .1 + q * .05, tic(), .07, -.3 if q % 2 else .3, .03)
        fx(t0 + 1.2, impacto(), .45, 0, .4); fx(t0 + 1.2, boom(1.2, 160, 40, 2.6), .38, 0, .1); impactos.append(t0 + 1.2)
    elif tp == 'dato': fx(t0 - .5, succion(.5), .24, 0, .2); fx(t0, impacto(), .48, 0, .4); fx(t0, boom(1.2, 160, 40, 2.6), .4, 0, .1); impactos.append(t0)
    elif tp == 'capitulo': fx(t0 - .4, riser(.5), .22, 0, .2); fx(t0 + .15, boom(1.6, 150, 36, 3), .5, 0, .2); fx(t0 + .2, campana(659.3), .12, 0, .6); impactos.append(t0 + .15)
    elif tp == 'ficha': fx(t0 - .15, barrido(.3, 700, 3200, 1200, .15), .18, -.4, .1); fx(t0 + .05, pop(560), .18, -.4, .15)
    elif tp == 'barrido': fx(t0, barrido(.8, 300, 3400, 700, .2), .34, 0, .15, mov=(-.8, .8)); fx(t0 + .4, boom(.6, 130, 55, 1.6), .24, 0, .15)
    elif tp == 'pinPro': fx(t0, pluck(PENTA[npin % len(PENTA)]), .26, p, .35); fx(t0 + .25, pop(1100), .12, p, .1); npin += 1
    elif tp == 'circuloPro': fx(t0, barrido(.6, 900, 2600, 1400, .1), .14, p, .1); fx(t0 + .6, pop(880), .16, p, .2)
    elif tp == 'flechaPro': fx(t0, barrido(.8, 400, 2400, 900, .15), .16, 0, .1, mov=(-.5, .5)); fx(t0 + .8, pop(760), .12, p, .1)
    elif tp == 'rotulo2': fx(t0, pop(680 + (npin % 4) * 80), .16, p, .15); npin += 1
    elif tp in ('tarjetaFoto', 'tarjetaClip'): fx(t0, papel(.3), .22, .5, .15); fx(t0 + .05, pop(900), .14, .5, .1)
    elif tp == 'foto': fx(t0 - .2, barrido(.35, 500, 3000, 900, .15), .2, 0, .1)
    elif tp == 'fila':
        for q in range(e.get('n', 5)): fx(t0 + q * .1, pop(620 + q * 60), .12, -.4 + .8 * q / max(1, e.get('n', 5) - 1), .1)
    elif tp == 'gente' and e.get('modo') != 'caminar':
        for q in range(min(8, e.get('n', 5))): fx(t0 + q * e.get('paso', .12), pop(500 + q * 40), .09, p, .1)
    elif tp == 'camino':
        d = min(t1 - t0, e.get('dur', 3) + .3); s = {'camion': motor(d) * .8, 'tren': tren(d), 'barco': oleaje(d) * .7 + motor(d) * .3, 'avion': viento(d, True)}.get(e.get('vehiculo'))
        if s is not None: fx(t0, s * env_ar(len(s), .4, .5), .16, 0, .1, mov=(-.5, .5))
    elif tp == 'simbolo':
        f = e.get('forma')
        if f == 'notas':
            for q in range(6): fx(t0 + .1 + q * .22, pluck(PENTA[(q * 2) % 8]), .14, -.4 + .16 * q, .4)
        elif f == 'gotas':
            for q in range(4): fx(t0 + .1 + q * .35, gota_agua(), .2, rng.uniform(-.5, .5), .3)
        elif f == 'sol': fx(t0, riser(1.2), .16, 0, .3); fx(t0 + .2, brillo(1.0), .12, 0, .3)
        elif f == 'precio': fx(t0, caja(), .26, p, .25); fx(t0 + .05, boom(.5, 140, 70, 1.4), .2, 0, .1)
        elif f == 'olas': s = oleaje(min(4, t1 - t0)); fx(t0, s, .22, 0, .2)
        elif f == 'reloj':
            for q in range(10): fx(t0 + q * .5, tic(), .14, 0, .05)
        elif f == 'alerta': fx(t0, pop(420), .24, p, .2); fx(t0, boom(.7, 120, 50, 1.8), .3, 0, .15)
    elif tp == 'pregunta': fx(t0 - .3, barrido(.4, 700, 3200, 1200, .2), .22, 0, .1); fx(t0, campana(1318.5), .18, 0, .4)
for c in sp.get('clips', []):
    t0, t1 = c['desde'], c['hasta']
    if t0 > .2: fx(t0 - .28, barrido(.42, 400, 3600, 900, .2), .3, 0, .15, mov=(.7, -.7)); fx(t0, boom(.6, 130, 55, 1.6), .24, 0, .15)
    s, g = amb_clip(c['codigo'], t1 - t0 + .6)
    if s is not None: fx(t0 - .2, s * env_ar(len(s), .3, .45), g, 0, .1)
for e in ev:  # ambiente suave bajo las fotos a pantalla completa
    if e['tipo'] == 'foto':
        d = e['hasta'] - e['desde'] + .4; im = e['img']; s = (puerto(d) if any(k in im for k in ('S22', 'malecon', 'aguachile')) else murmullo(d) if any(k in im for k in ('tambora', 'carnaval')) else viento(d, False))
        fx(e['desde'] - .2, s * env_ar(len(s), .3, .4), .14, 0, .1)
for a, b in zip(cam, cam[1:]):  # movimientos de cámara
    d = b['t'] - a['t']
    if a.get('suave') is not False or not (0 < d < 1.9) or (a['lon'], a['lat'], a['ancho']) == (b['lon'], b['lat'], b['ancho']): continue
    if any(c['desde'] - .1 < a['t'] < c['hasta'] for c in sp.get('clips', [])): continue
    r = b['ancho'] / a['ancho']
    if r < .72: fx(a['t'] - .03, zoom_in(min(d, .9) + .05), .26, 0, .1)
    elif r > 1.35: fx(a['t'] - .03, zoom_out(min(d, .9) + .1), .26, 0, .15)
    else: fx(a['t'] - .03, barrido(max(.3, min(d, .9) + .05), 400, 3000, 800, .2), .24, 0, .1)

# ======================= MÚSICA (original, muy baja) =======================
cap = {e['n']: e['desde'] for e in ev if e['tipo'] == 'capitulo'}
secc = [(0, 'oscuro'), (cap[1], 'ligero'), (cap[2], 'ligero'), (cap[3], 'ligero'), (cap[4], 'completo'), (cap[5], 'oscuro'), (cap[6], 'oscuro'), (dur - 40, 'final')]
tape = [cap[5] - .7, cap[6] - .7]
mus = musica(dur, sorted(secc), sorted(set(round(i, 2) for i in impactos if i > 1)), tape)
mus *= np.clip(1 - (np.arange(N) / SR - (dur - 1.5)) / 1.5, 0, 1)
rv = reverb(ENV[:N], 1.5); fxL = FX[0, :N] + rv[0] * .5; fxR = FX[1, :N] + rv[1] * .5
envv = filt(np.abs(voz), 'low', 8); duck = 1 - .6 * np.clip(envv / (np.percentile(envv, 96) * .45 + 1e-9), 0, 1) if CON_VOZ else np.ones(N)
duck_fx = 1 - .45 * (1 - duck) / .6 if CON_VOZ else np.ones(N); gm = .11   # música muy bajita: solo para que no suene vacío
mix = np.stack([voz + mus[0] * duck * gm + fxL * duck_fx * .5, voz + mus[1] * duck * gm + fxR * duck_fx * .5]); mix /= max(1, np.abs(mix).max())
tmp = D / '.tmp'; tmp.mkdir(exist_ok=True)
with wave.open(str(tmp / 'mezcla.wav'), 'w') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix.T, -1, 1) * 32767).astype(np.int16).tobytes())
med = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(tmp / 'mezcla.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
med = json.loads(med[med.rindex('{'):med.rindex('}') + 1]); gan = min(6.0, -14.0 - float(med['input_i']))
video = D / (sp['salida'] + '.mp4'); out = D / (sp['salida'] + '-final.mp4')
if '--solo-audio' not in sys.argv:
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(video), '-i', str(tmp / 'mezcla.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', f'volume={gan:.2f}dB,alimiter=limit=0.8:attack=4:release=70:level=disabled', '-ar', '48000', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', str(out)], check=True)
print(f'{dur:.1f} s · {len(impactos)} golpes · ganancia {gan:.1f} dB · {out.name}')
