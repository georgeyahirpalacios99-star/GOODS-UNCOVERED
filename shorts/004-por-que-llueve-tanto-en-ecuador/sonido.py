"""Short 004 · música original (sintetizada, sin derechos) + efectos atados a cada evento + mezcla con la voz.
    python3 shorts/004-por-que-llueve-tanto-en-ecuador/sonido.py      (después de construir.py y del render)
La voz NO se toca: solo se le suma música por debajo y efectos. Sin voz, deja una vista previa con música y efectos.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np
D = Path(__file__).resolve().parent; SR = 48000
rng = np.random.default_rng(3)
T = lambda d: np.arange(int(d * SR)) / SR
def norm(s): m = np.abs(s).max(); return (s / m if m > 0 else s).astype(np.float32)
def suave(x, n): k = np.ones(n) / n; return np.convolve(x, k, 'same')
def ruido(d): return rng.standard_normal(int(d * SR))

# ---------------- efectos ----------------
def whoosh(d=.45): t = T(d); env = np.sin(np.pi * t / t[-1]) ** 2; n = ruido(d); return norm((suave(n, 24) * .7 + (n - suave(n, 6)) * .15) * env)
def impacto(): t = T(1.1); s = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t * 7)) / SR) * np.exp(-t * 4); s += suave(ruido(1.1), 8) * np.exp(-t * 26) * 1.2; return norm(s)
def golpe(): t = T(.35); s = np.sin(2 * np.pi * np.cumsum(90 + 130 * np.exp(-t * 18)) / SR) * np.exp(-t * 11) + suave(ruido(.35), 4) * np.exp(-t * 45) * .6; return norm(s)
def pop(f0=520): t = T(.1); return norm(np.sin(2 * np.pi * np.cumsum(f0 + f0 * 1.3 * t / t[-1]) / SR) * np.exp(-t * 40))
def ding(f=1568): t = T(.8); return norm(sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * k) for m, a, k in [(1, .6, 5), (1.5, .3, 8), (2, .15, 11)]))
def riser(d=1.2): t = T(d); n = ruido(d); f = 200 + 2200 * (t / d) ** 2; s = np.sin(2 * np.pi * np.cumsum(f) / SR) * .4 + (n - suave(n, 3)) * .5 * (t / d); return norm(s * (t / d) ** 1.5)
def latido():  # dos golpes graves de corazón
    t = T(.18); g = np.sin(2 * np.pi * np.cumsum(48 + 40 * np.exp(-t * 30)) / SR) * np.exp(-t * 22)
    s = np.zeros(int(.5 * SR)); s[:len(g)] += g; i = int(.2 * SR); s[i:i + len(g)] += .7 * g; return norm(s)
def agua(d=1.8):  # ola que entra donde estaba el país
    t = T(d); n = ruido(d); env = np.minimum(1, t / .35) * np.exp(-np.maximum(0, t - .35) * 1.9)
    s = suave(n, 40) * .9 + suave(n, 9) * .35 * (.6 + .4 * np.sin(2 * np.pi * 7 * t)); return norm(s * env)
def grieta():  # crujido seco
    t = T(.45); s = np.zeros(len(t))
    for k in range(9):
        i = int(rng.uniform(0, .25) * SR); L = int(.03 * SR); s[i:i + L] += ruido(.03)[:len(s[i:i + L])] * np.exp(-np.arange(min(L, len(s) - i)) / SR * 90) * rng.uniform(.4, 1)
    return norm(s + .3 * np.sin(2 * np.pi * 70 * t) * np.exp(-t * 9))
def zap(d=1.2):  # chispazo eléctrico + bajón de tensión
    t = T(d); zum = np.sign(np.sin(2 * np.pi * 120 * t)) * .25 * (np.sin(2 * np.pi * 9 * t) > -.2)
    caida = np.sin(2 * np.pi * np.cumsum(420 * np.exp(-t * 2.4) + 40) / SR) * .6
    chis = (ruido(d) - suave(ruido(d), 3)) * (np.exp(-t * 18) + .3 * (np.sin(2 * np.pi * 13 * t) > .7))
    return norm((zum + caida + chis * .5) * np.exp(-t * 1.6))
def retumbo(d=1.0): t = T(d); return norm(suave(ruido(d), 120) * np.exp(-t * 3) + .5 * np.sin(2 * np.pi * 42 * t) * np.exp(-t * 4))
def sello(): g = golpe(); p = np.concatenate([np.zeros(int(.02 * SR)), pop(260)]); g[:len(p)] += .4 * p; return norm(g)
def tic(): t = T(.04); return norm(np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 160))

# ---------------- música ----------------
BPM = 112; BEAT = 60 / BPM
# Re menor · Si bemol · Fa · Do  (y una variante tensa con La mayor)
PROG = {'n': [(73.42, [293.66, 349.23, 440, 587.33]), (58.27, [233.08, 293.66, 349.23, 466.16]), (87.31, [349.23, 440, 523.25, 698.46]), (65.41, [261.63, 329.63, 392, 523.25])],
        't': [(73.42, [293.66, 349.23, 440, 587.33]), (58.27, [233.08, 293.66, 349.23, 466.16]), (49.0, [196, 233.08, 293.66, 392]), (55.0, [220, 277.18, 329.63, 440])]}
def musica(dur, secciones, golpes):
    N = int(dur * SR) + 2 * SR; m = np.zeros(N, np.float32)
    def put(t0, s, g):
        i = int(t0 * SR); j = min(N, i + len(s))
        if 0 <= i < N: m[i:j] += g * s[:j - i]
    t = T(.35); kick = norm(np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-t * 30)) / SR) * np.exp(-t * 9))
    t = T(.2); n = ruido(.2); clap = norm((n - suave(n, 3)) * np.exp(-t * 22))
    t = T(.05); n = ruido(.05); hat = norm((n - suave(n, 2)) * np.exp(-t * 90))
    def pluck(f, d=.24): t = T(d); return norm(sum(np.sin(2 * np.pi * f * k * t) / k * np.exp(-t * (13 + 3 * k)) for k in range(1, 7)))
    def marimba(f, d=.5): t = T(d); return norm((np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)) * np.exp(-t * 7))
    def bajo(f, d): t = T(d); s = np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t); return norm(s * np.minimum(1, t / .01) * np.exp(-t * 1.1))
    def pad(fs, d): t = T(d); s = sum(np.sin(2 * np.pi * f * t) + .3 * np.sin(6 * np.pi * f * t) / 3 for f in fs); return norm(s * np.minimum(1, t / .5) * np.minimum(1, (d - t) / .5))
    def modo(t0):
        mo = secciones[0][1]
        for ts, x in secciones:
            if t0 >= ts: mo = x
        return mo
    nb = int(dur / BEAT) + 2
    for b in range(nb):
        t0 = b * BEAT; mo = modo(t0)
        if mo == 'nada': continue
        prog = PROG['t' if mo in ('tension', 'oscuro') else 'n']; raiz, notas = prog[(b // 4) % 4]
        if b % 4 == 0: put(t0, pad([f / 2 for f in notas[:3]], BEAT * 4), .07 if mo != 'ambiente' else .1)
        if mo in ('tension', 'oscuro'):
            if b % 2 == 0: put(t0, kick, .42)
            if b % 4 == 0: put(t0, bajo(raiz, BEAT * 4), .3)
            if mo == 'tension': put(t0 + BEAT / 2, hat, .06)
            continue
        if mo == 'ambiente':
            if b % 4 == 0: put(t0, bajo(raiz, BEAT * 4), .2)
            for s8 in range(2): put(t0 + s8 * BEAT / 2, marimba(notas[(b * 2 + s8) % 4]), .07)
            continue
        # completo / ligero / final
        if mo != 'ligero':
            put(t0, kick, .55)
            if b % 2 == 1: put(t0, clap, .26)
        for h in range(2): put(t0 + h * BEAT / 2 + (.02 if h else 0), hat, .09 + .05 * h)
        if b % 4 == 0: put(t0, bajo(raiz, BEAT * 4), .32)
        for s16 in range(4):
            nota = notas[(b * 4 + s16) % 4] * (2 if (b // 8) % 2 and s16 % 2 else 1); put(t0 + s16 * BEAT / 4, pluck(nota), .08)
        if mo == 'final' and b % 2 == 0: put(t0, marimba(notas[(b // 2) % 4] * 2, .6), .08)
    for g in golpes:  # un tiempo de vacío antes del golpe, sube un riser, y el golpe entra con todo
        i0, i1 = int((g - BEAT) * SR), int(g * SR)
        if i0 > 0: m[i0:i1] *= np.linspace(1, .1, i1 - i0)
        put(g - 1.0, riser(1.0), .16)
    return m[:int(dur * SR)]


# ---------------- efectos propios de este Short ----------------
def plink():  # gota que cae sobre el mapa
    t = T(1.4); s = np.sin(2 * np.pi * np.cumsum(1250 * np.exp(-t * 9) + 380) / SR) * np.exp(-t * 6)
    eco = np.zeros_like(s)
    for d, g in [(.11, .45), (.23, .28), (.37, .16)]: i = int(d * SR); eco[i:] += g * s[:len(s) - i]
    return norm(s + eco)
def trueno(d=1.8):
    t = T(d); n = ruido(d); crack = (n - suave(n, 2)) * np.exp(-t * 30)
    rumble = suave(n, 220) * np.exp(-t * 1.6) * (1 + .5 * np.sin(2 * np.pi * 3 * t)); return norm(crack * .5 + rumble * 2.2)
def lluvia(d):  # lecho de lluvia: ruido brillante + gotas
    n = ruido(d); s = (n - suave(n, 3)) * .5 + suave(n, 6) * .3
    for _ in range(int(d * 60)): i = int(rng.uniform(0, d) * SR); L = int(.01 * SR); s[i:i + L] += rng.uniform(-1, 1) * np.exp(-np.arange(min(L, len(s) - i)) / SR * 400) * 2
    env = np.minimum(1, T(d) / .4) * np.minimum(1, (d - T(d)) / .4); return norm(s * env)
def viento(d, sube=True):
    t = T(d); n = ruido(d); s = suave(n, 60) * (1 + .4 * np.sin(2 * np.pi * .7 * t)); env = (t / d) ** 1.2 if sube else np.sin(np.pi * t / d); return norm(s * env)
def papel(): t = T(.28); n = ruido(.28); return norm((n - suave(n, 4)) * np.exp(-t * 14) * (1 + np.sin(2 * np.pi * 38 * t)))
def chisporroteo(d=2.0): t = T(d); n = ruido(d); s = (n - suave(n, 2)) * (np.abs(n) > 1.8) * 2 + (n - suave(n, 5)) * .3; return norm(s * np.minimum(1, t / .5) * np.exp(-np.maximum(0, t - 1.2) * 2))
def campana(f=1046.5): t = T(2.2); return norm(sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * k) for m, a, k in [(1, .7, 2.2), (2.76, .35, 3.5), (5.4, .2, 5), (8.9, .1, 7)]))
def leer(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def escribir(f, x):
    with wave.open(str(f), 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


sp = json.load(open(D / 'mapa.json')); ev = sp['eventos']; dur = sp['duracion']; N = int(dur * SR)
fv = D / '.tmp' / 'voz.wav'; CON_VOZ = fv.exists() and 'audio' in sp
voz = leer(fv) if CON_VOZ else np.zeros(N, np.float32); voz = np.pad(voz, (0, max(0, N - len(voz))))[:N]
sfx = np.zeros(N + 4 * SR, np.float32)
def put(t0, s, g):
    i = int(max(0, t0) * SR); j = min(len(sfx), i + len(s)); sfx[i:j] += g * s[:j - i]
def lecho(t0, t1, s_fn, g):
    if t1 - t0 > .2: put(t0, s_fn(t1 - t0), g)
golpes, seq, npin = [], 0, 0
for e in sorted(ev, key=lambda e: e['desde']):
    tp, t0 = e['tipo'], e['desde']; t1 = e.get('hasta', t0 + 2)
    if tp == 'gota': hit = t0 + e.get('cae', .55); put(hit - .02, plink(), .75); put(hit, whoosh(.9), .22); put(hit + .05, agua(1.3), .18); golpes.append(hit)
    elif tp == 'tormenta':
        lecho(t0, t1, lluvia, .11 * min(1.4, e.get('r', 1)))
        for r in e.get('rayos', []): put(r, trueno(), .5)
    elif tp == 'seco': lecho(t0, t1, lambda d: viento(d, False), .05)
    elif tp == 'chip':
        put(t0, pop(600 + (seq % 6) * 70), .28); seq += 1
        if 'NAVIDAD' in e.get('texto', ''): put(t0 + .05, campana(), .3)
    elif tp in ('cifra', 'contador'):
        put(t0, golpe(), .45); put(t0 + .08, ding(1320), .16)
        if tp == 'contador':
            d = e.get('dur', 1)
            for q in range(int(d / .07)): put(t0 + .1 + q * .07, tic(), .07)
            put(t0 + .1 + d, golpe(), .3)
    elif tp == 'trazo': put(t0, whoosh(1.0), .25); put(t0 + e.get('dur', .8), ding(1760), .16)
    elif tp == 'titulo': put(t0 - .25, whoosh(.5), .22); put(t0, pop(420), .22)
    elif tp == 'caja': put(t0, impacto(), .62); put(t0, golpe(), .45); golpes.append(t0)
    elif tp == 'regiones3':
        for i in range(3): put(t0 + i * e.get('paso', .22), papel(), .4); put(t0 + i * e.get('paso', .22), pop(360 + i * 120), .2)
    elif tp == 'nubesPaso': put(t0, whoosh(1.3), .5)
    elif tp == 'corte':
        put(t0, papel(), .45); put(t1 - .3, papel(), .35)
        lecho(t0 + e.get('tAire', .7), t0 + e.get('tLluvia', 3), viento, .14); lecho(t0 + e.get('tLluvia', 3), t1, lluvia, .15)
        for r in e.get('rayos', []): put(t0 + r, trueno(), .5)
    elif tp == 'corriente': put(t0, agua(1.6), .2); put(t0, whoosh(1.2), .15)
    elif tp == 'calor': put(t0, chisporroteo(2.2), .2); put(t0, riser(1.4), .14)
    elif tp == 'inundacion': put(t0, agua(2.4), .28)
    elif tp == 'pin': put(t0, pop(780 + npin * 85), .28); npin += 1
    elif tp == 'girar':
        for q in range(int(e.get('dur', 1.2) / .06)): put(t0 + q * .06, tic(), .06)
cam = sp['camara']
for a, b in zip(cam, cam[1:]):
    if a.get('suave') is False and 0 < b['t'] - a['t'] < .7 and (a['lon'], a['lat'], a['ancho']) != (b['lon'], b['lat'], b['ancho']): put(a['t'] - .05, whoosh(.5), .2)
for s in sp.get('sacudidas', []): put(s['t'], retumbo(s.get('dur', .5)), .3)
# música por secciones
secc = [(0, 'nada'), (golpes[0] if golpes else .5, 'completo')]
for e in ev:
    if e['tipo'] == 'corte': secc += [(e['desde'], 'ligero'), (e['hasta'], 'completo')]
    if e['tipo'] == 'noche': secc += [(e['desde'], 'oscuro'), (e['hasta'], 'completo')]
fin = [e['desde'] for e in ev if e['tipo'] == 'titulo' and 'CIUDAD' in e.get('texto', '')]
if fin: secc.append((fin[0], 'final'))
secc.sort()
gm = sorted(set([g for g in golpes[1:]] + [e['desde'] + e.get('dur', 1) for e in ev if e['tipo'] == 'contador' and e.get('a') in (25, 29)] + [e['desde'] for e in ev if e['tipo'] == 'cifra']))
mus = musica(dur, secc, gm); mus *= np.clip(1 - (np.arange(N) / SR - (dur - 1.2)) / 1.2, 0, 1)
envv = np.sqrt(suave(voz ** 2, 4800)); duck = 1 - .62 * np.clip(envv / (np.percentile(envv, 95) * .3 + 1e-9), 0, 1) if CON_VOZ else np.ones(N); duck = suave(duck, 2400)
mezcla = voz + mus * duck * (.3 if CON_VOZ else .42) + sfx[:N] * .8
tmp = D / '.tmp'; tmp.mkdir(exist_ok=True); escribir(tmp / 'mezcla.wav', mezcla / max(1, np.abs(mezcla).max()))
med = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(tmp / 'mezcla.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
med = json.loads(med[med.rindex('{'):med.rindex('}') + 1]); gan = min(4.0, -14.0 - float(med['input_i']))
video = D / (sp['salida'] + '.mp4'); out = D / (sp['salida'] + ('-final.mp4' if CON_VOZ else '-vista-previa.mp4'))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(video), '-i', str(tmp / 'mezcla.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', f'volume={gan:.2f}dB,alimiter=limit=0.79:attack=5:release=80:level=disabled', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(out)], check=True)
print(('CON VOZ' if CON_VOZ else 'SIN VOZ (vista previa)'), f'· {dur:.1f} s · secciones {[(round(a, 1), b) for a, b in secc]} · {out.name}')
