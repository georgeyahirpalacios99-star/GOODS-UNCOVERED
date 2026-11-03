"""Video 003 · música original (sintetizada, sin derechos) + efectos atados a cada evento del mapa + mezcla final.
    python3 videos-largos/003-colombia-desaparece/construir.py      # deja mapa.json y .tmp/voz.wav
    node motor-mapa/render.cjs videos-largos/003-colombia-desaparece
    python3 videos-largos/003-colombia-desaparece/sonido.py
La voz NO se toca (ni velocidad, ni tono, ni ecualización): solo se le suma música por debajo y efectos.
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

def leer(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def escribir(f, x):
    with wave.open(str(f), 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())

sp = json.load(open(D / 'mapa.json')); ev = sp['eventos']; dur = sp['duracion']
voz = leer(D / '.tmp' / 'voz.wav'); N = int(dur * SR); voz = np.pad(voz, (0, max(0, N - len(voz))))[:N]
sfx = np.zeros(N + 3 * SR, np.float32)
def put(t0, s, g):
    i = int(max(0, t0) * SR); j = min(len(sfx), i + len(s)); sfx[i:j] += g * s[:j - i]
cuando = lambda tipo, **kw: [e['desde'] for e in ev if e['tipo'] == tipo and all(e.get(k) == v for k, v in kw.items())]

# --- el gancho: latidos, desaparición, agua ---
T_DES = sp['desaparece'][0]['t']
for k, t0 in enumerate([.25, 1.15, 2.05]): put(t0, latido(), .55 - k * .08)
put(T_DES - .05, grieta(), .5); put(T_DES, impacto(), .7); put(T_DES + .1, agua(2.2), .5); put(T_DES, retumbo(1.2), .45)
golpes = []; ultimo_resaltar = -9; seq = 0
for e in sorted(ev, key=lambda e: e['desde']):
    t0, tp = e['desde'], e['tipo']
    if tp == 'despertar': continue
    if tp == 'nombre': put(t0, pop(480 + (seq % 6) * 70), .3); seq += 1
    elif tp == 'region': put(t0 - .3, whoosh(.6), .32)
    elif tp == 'cinta': put(t0, golpe(), .45); put(t0 + .05, pop(760), .2)
    elif tp == 'sello': put(t0, sello(), .55)
    elif tp == 'titulo': put(t0, impacto(), .6); golpes.append(t0)
    elif tp == 'cifra': put(t0, golpe(), .42); put(t0 + .1, ding(1320), .18); [put(t0 - .5 + q * .07, tic(), .08) for q in range(6)]
    elif tp == 'pin': put(t0, pop(880), .35); put(t0 + .12, ding(), .2)
    elif tp == 'flujo':
        put(t0, whoosh(1.1), .22)
        if e.get('roto'): put(t0 + .8, grieta(), .3); put(t0 + .8, pop(300), .2)
    elif tp == 'resaltar':
        if t0 - ultimo_resaltar > .8: put(t0, pop(700), .28); put(t0 + .05, ding(1760), .1)
        ultimo_resaltar = t0
    elif tp == 'globo': put(t0, pop(950), .35)
    elif tp == 'pregunta': put(t0 - .3, whoosh(.5), .3); put(t0, ding(), .25)
    elif tp == 'apagon': put(t0, zap(1.3), .5); put(t0 + .05, retumbo(.8), .25)
    elif tp == 'iconos':
        for i, _ in enumerate(e['items']): put(t0 + i * e.get('paso', .35), pop(620 + i * 110), .3)
    elif tp == 'tarjeta': put(t0 - .15, whoosh(.45), .25); put(t0 + .3, pop(820), .25)
for k in sp.get('camara', []):
    if 3 < k['t'] < dur - 2 and not k.get('suave') is False: put(k['t'], whoosh(.55), .14)
for s in sp.get('sacudidas', []):
    if abs(s['t'] - T_DES) > .5: put(s['t'], retumbo(s.get('dur', .8)), .35)

# --- música por secciones: tensión en el gancho, entra el beat cuando Sudamérica se vuelve isla ---
isla = min(cuando('cinta', texto='SUDAMÉRICA ES UNA ISLA'))
tit = [e['desde'] for e in ev if e['tipo'] == 'titulo' and 'DESAPARECIERA' in e['texto']][0]
reg = {e['texto']: e['desde'] for e in ev if e['tipo'] == 'region'}
ecu_luz = [e['desde'] for e in ev if e['tipo'] == 'apagon']
secciones = [(0, 'nada'), (2.6, 'tension'), (T_DES, 'nada'), (T_DES + 1.6, 'tension'), (isla, 'completo'), (ecu_luz[0] - .3, 'oscuro'), (tit, 'completo')]
for nombre, modo in [('EL CAFÉ', 'ligero'), ('LAS FLORES', 'completo'), ('ECUADOR', 'oscuro'), ('EL AGUA', 'ambiente'), ('LO QUE NO TIENE PRECIO', 'ambiente')]:
    if nombre in reg: secciones.append((reg[nombre], modo))
cierre = [e['desde'] for e in ev if e['tipo'] == 'titulo' and 'SON' in e['texto']]
if cierre: secciones.append((cierre[0] - 6, 'final'))
secciones.sort()
golpes = sorted(set([isla] + [g for g in golpes if g > 5]))
mus = musica(dur, secciones, golpes)
mus *= np.clip(1 - (np.arange(N) / SR - (dur - 3)) / 3, 0, 1)  # se apaga en los últimos 3 s

# la música baja sola cuando habla la voz
envv = np.sqrt(suave(voz ** 2, 4800)); duck = 1 - .62 * np.clip(envv / (np.percentile(envv, 95) * .3 + 1e-9), 0, 1); duck = suave(duck, 2400)
mezcla = voz * 1.0 + mus * duck * .3 + sfx[:N] * .8
tmp = D / '.tmp' / 'mezcla.wav'; escribir(tmp, mezcla / max(1, np.abs(mezcla).max()))
if '--solo-audio' in sys.argv: print('mezcla en', tmp); sys.exit()
video = D / (sp['salida'] + '.mp4'); out = D / (sp['salida'] + '-final.mp4')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(video), '-i', str(tmp), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(out)], check=True)
print(f'{dur:.1f} s · secciones {[(round(a, 1), b) for a, b in secciones]} · golpes {[round(g, 1) for g in golpes]} · {out.name}')
