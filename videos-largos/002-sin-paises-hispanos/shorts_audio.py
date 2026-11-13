"""Música original (sintetizada, sin derechos) + efectos sincronizados para los Shorts del video 002.
    python3 videos-largos/002-sin-paises-hispanos/shorts_audio.py 2 3
Lee shorts/NN/mapa.json para saber cuándo pasa cada cosa, toma la voz del Short ya renderizado y entrega
entregas-partes/Short N - ... (con musica).mp4
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np
D = Path(__file__).resolve().parent; RAIZ = D.parent.parent; SR = 48000
rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR
def norm(s): m = np.abs(s).max(); return (s / m if m > 0 else s).astype(np.float32)
def suave(x, n): k = np.ones(n) / n; return np.convolve(x, k, 'same')

# ---------------- efectos ----------------
def whoosh(d=.45): t = T(d); env = np.sin(np.pi * t / t[-1]) ** 2; n = rng.standard_normal(len(t)); return norm((suave(n, 24) * .7 + (n - suave(n, 6)) * .15) * env)
def impacto(): t = T(.9); s = np.sin(2 * np.pi * np.cumsum(40 + 55 * np.exp(-t * 7)) / SR) * np.exp(-t * 4.5); s += suave(rng.standard_normal(len(t)), 8) * np.exp(-t * 28) * 1.2; return norm(s)
def golpe(): t = T(.35); s = np.sin(2 * np.pi * np.cumsum(90 + 130 * np.exp(-t * 18)) / SR) * np.exp(-t * 11) + suave(rng.standard_normal(len(t)), 4) * np.exp(-t * 45) * .6; return norm(s)
def pop(f0=520): t = T(.1); return norm(np.sin(2 * np.pi * np.cumsum(f0 + f0 * 1.3 * t / t[-1]) / SR) * np.exp(-t * 40))
def ding(f=1568): t = T(.7); return norm(sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * k) for m, a, k in [(1, .6, 5), (1.5, .3, 8), (2, .15, 11)]))
def riser(d=1.2): t = T(d); n = rng.standard_normal(len(t)); f = 200 + 2200 * (t / d) ** 2; s = np.sin(2 * np.pi * np.cumsum(f) / SR) * .4 + (n - suave(n, 3)) * .5 * (t / d); return norm(s * (t / d) ** 1.5)

# ---------------- música ----------------
BPM = 118; BEAT = 60 / BPM
ACORDES = [(110.0, [220, 261.63, 329.63, 440]), (87.31, [174.61, 220, 261.63, 349.23]), (130.81, [261.63, 329.63, 392, 523.25]), (98.0, [196, 246.94, 293.66, 392])]
def musica(dur, golpes):
    N = int(dur * SR) + SR; m = np.zeros(N, np.float32)
    def put(t0, s, g):
        i = int(t0 * SR); j = min(N, i + len(s))
        if i < N: m[i:j] += g * s[:j - i]
    t = T(.35); kick = norm(np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-t * 30)) / SR) * np.exp(-t * 9))
    t = T(.2); n = rng.standard_normal(len(t)); clap = norm((n - suave(n, 3)) * np.exp(-t * 22))
    t = T(.05); n = rng.standard_normal(len(t)); hat = norm((n - suave(n, 2)) * np.exp(-t * 90))
    def pluck(f, d=.22): t = T(d); s = sum(np.sin(2 * np.pi * f * k * t) / k * np.exp(-t * (14 + 3 * k)) for k in range(1, 7)); return norm(s)
    def bajo(f, d): t = T(d); s = np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t); env = np.minimum(1, t / .01) * np.exp(-t * 1.2); return norm(s * env)
    def pad(fs, d): t = T(d); s = sum(np.sin(2 * np.pi * f * t) + .3 * np.sin(6 * np.pi * f * t) / 3 for f in fs); env = np.minimum(1, t / .4) * np.minimum(1, (d - t) / .4); return norm(s * env)
    nb = int(dur / BEAT) + 2
    for b in range(nb):
        t0 = b * BEAT; compas = (b // 4) % 4; raiz, notas = ACORDES[compas]
        if b < 2: continue  # entra tras el golpe inicial
        put(t0, kick, .55)
        if b % 2 == 1: put(t0, clap, .28)
        for h in range(2): put(t0 + h * BEAT / 2 + (.02 if h else 0), hat, .1 + .05 * h)
        if b % 4 == 0: put(t0, bajo(raiz, BEAT * 4), .32); put(t0, pad([f / 2 for f in notas[:3]], BEAT * 4), .06)
        for s16 in range(4):
            nota = notas[(b * 4 + s16) % 4] * (2 if (b // 8) % 2 and s16 % 2 else 1); put(t0 + s16 * BEAT / 4, pluck(nota), .09)
    for g in golpes:  # silencio de un tiempo antes del golpe y sube con un riser
        i0, i1 = int((g - BEAT) * SR), int(g * SR)
        if i0 > 0: m[i0:i1] *= np.linspace(1, .15, i1 - i0)
        put(g - 1.0, riser(1.0), .18)
    return m[:int(dur * SR)]

def leer_wav(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def escribir(f, x):
    with wave.open(str(f), 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())

NOMBRES = {2: 'adios canal de panama', 3: 'brasil se queda solo', 1: '21 paises borrados', 4: 'portugal se vuelve isla', 5: 'el nuevo hogar del espanol'}
for n in [int(x) for x in sys.argv[1:]]:
    sp = json.load(open(D / 'shorts' / f'{n:02d}' / 'mapa.json')); ev = sp['eventos']
    ini = [e for e in ev if e['tipo'] == 'cabecera'][0]['desde']; fin = sp['duracion']; dur = fin - ini
    video = RAIZ / 'entregas-partes' / f'Short {n} - {NOMBRES[n]}.mp4'
    voz = leer_wav(video); dur = len(voz) / SR
    sfx = np.zeros(len(voz) + SR, np.float32)
    def put(t0, s, g):
        i = int(max(0, t0) * SR); j = min(len(sfx), i + len(s)); sfx[i:j] += g * s[:j - i]
    put(0.0, impacto(), .55); golpes = []
    seq = 0
    for e in sorted(ev, key=lambda e: e['desde']):
        t0 = e['desde'] - ini
        if t0 < 0 or t0 > dur: continue
        tp = e['tipo']
        if tp == 'nombre': put(t0, pop(480 + seq * 70), .32); seq += 1
        elif tp == 'region' and t0 > .5: put(t0 - .2, whoosh(.5), .3)
        elif tp in ('cinta', 'sello'): put(t0, golpe(), .5)
        elif tp == 'titulo': put(t0, impacto(), .5); golpes.append(t0)
        elif tp == 'cifra': put(t0, golpe(), .4); put(t0 + .1, ding(1320), .18)
        elif tp == 'pin': put(t0, pop(880), .35); put(t0 + .12, ding(), .2)
        elif tp == 'flujo': put(t0, whoosh(1.0), .25)
        elif tp == 'resaltar': put(t0, pop(700 + 120 * (len(golpes) % 3)), .3)
        elif tp == 'globo': put(t0, pop(950), .35)
        elif tp == 'pregunta': put(t0 - .3, whoosh(.5), .3); put(t0, ding(), .25)
    for k in sp.get('camara', []):
        t0 = k['t'] - ini
        if .5 < t0 < dur - .5: put(t0, whoosh(.55), .18)
    if not golpes:  # golpe musical en la primera cifra fuerte o a la mitad
        c = [e['desde'] - ini for e in ev if e['tipo'] in ('cifra', 'cinta') and 0 < e['desde'] - ini < dur]; golpes = [c[1] if len(c) > 1 else dur / 2]
    mus = musica(dur, golpes)[:len(voz)]
    # la música baja sola cuando habla la voz
    envv = np.sqrt(suave(voz ** 2, 4800)); duck = 1 - .65 * np.clip(envv / (envv.max() * .25 + 1e-9), 0, 1); duck = suave(duck, 2400)
    mezcla = voz * 1.0 + mus * duck * .32 + sfx[:len(voz)] * .85
    tmp = D / '.tmp' / f'short{n}-mezcla.wav'; tmp.parent.mkdir(exist_ok=True); escribir(tmp, mezcla / max(1, np.abs(mezcla).max()))
    out = RAIZ / 'entregas-partes' / f'Short {n} - {NOMBRES[n]} (con musica).mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(video), '-i', str(tmp), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(out)], check=True)
    print(f'Short {n}: {dur:.1f} s · golpes musicales en {[round(g, 1) for g in golpes]} · {out.name}')
