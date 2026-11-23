"""Sonido de estadio sintetizado (sin derechos) para escenas del motor 3D.
    python3 motor-3d/sonido_estadio.py <carpeta con escena.json y el .mp4>
Murmullo de hinchada, silbato, patada, rugido de gol, red, papelitos, barridos, VAR y golpes en los datos.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np
from scipy import signal
SR = 48000; rng = np.random.default_rng(3)
D = Path(sys.argv[1]).resolve(); sc = json.load(open(D / 'escena.json')); dur = sc['duracion']; N = int((dur + 1) * SR)
tt = lambda d: np.arange(int(d * SR)) / SR
nz = lambda d: rng.standard_normal(int(d * SR))
def filt(x, k, f, o=2): return signal.sosfilt(signal.butter(o, f, btype=k, fs=SR, output='sos'), x)
def norm(x): m = np.abs(x).max(); return x / m if m else x
L = np.zeros(N); R = np.zeros(N)
def put(t0, s, g, p=0.):
    i = int(max(0, t0) * SR); j = min(N, i + len(s)); s = s[:j - i]; L[i:j] += g * s * np.cos((p + 1) * np.pi / 4) * 1.41; R[i:j] += g * s * np.sin((p + 1) * np.pi / 4) * 1.41
def hinchada(d, k=1.):  # murmullo de miles de personas: ruido de banda vocal con ondulación lenta
    t = tt(d); x = filt(nz(d), 'band', [250, 2200]) * (.7 + .3 * filt(np.abs(nz(d)), 'low', 1.5) * 6); return norm(x) * (.8 + .2 * np.sin(2 * np.pi * .13 * t)) * k
def rugido(d=3.5):  # explosión de la grada en el gol
    t = tt(d); env = np.minimum(1, t / .25) * np.exp(-np.maximum(0, t - .6) * .9); return norm(filt(nz(d), 'band', [300, 3500]) * env + filt(nz(d), 'band', [2500, 6000]) * env * .3)
def silbato(d=.9):
    t = tt(d); f = 2900 + 120 * np.sin(2 * np.pi * 38 * t); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + .4 * np.sign(np.sin(2 * np.pi * 9 * t))); env = np.minimum(1, t / .02) * np.minimum(1, (d - t) / .05); return norm(s * env + filt(nz(d), 'band', [2500, 4000]) * .3 * env)
def patada(): t = tt(.25); return norm(np.sin(2 * np.pi * (90 + 120 * np.exp(-t * 40)) * t) * np.exp(-t * 22) + filt(nz(.25), 'band', [800, 3000]) * np.exp(-t * 60) * .6)
def red(): t = tt(.6); return norm(filt(nz(.6), 'band', [1500, 6000]) * np.exp(-t * 7) * (1 + .5 * np.sin(2 * np.pi * 30 * t)))
def whoosh(d=.7):  # barrido: banda de ruido que sube y baja
    t = tt(d); x = nz(d); a = filt(x, 'band', [400, 1200]); b = filt(x, 'band', [1200, 3500]); m = np.sin(np.pi * t / d); return norm(a * (1 - t / d) * m + b * (t / d) * m)
def boom(d=1.2): t = tt(d); return norm(np.sin(2 * np.pi * (45 + 90 * np.exp(-t * 9)) * t) * np.exp(-t * 3.2))
def pitido(): t = tt(.18); return norm(np.sin(2 * np.pi * 1200 * t) * np.minimum(1, (.18 - t) / .02))
def papelitos(d=3): t = tt(d); return norm(filt(nz(d), 'high', 5000) * (rng.random(len(t)) > .997) * 4 + filt(nz(d), 'high', 6000) * .1) * np.exp(-t * .4)
def tic(): t = tt(.02); return norm(np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 260))
# fondo: hinchada todo el video (sube cuando aparece el estadio)
E = sc.get('estadio'); te = E['t'] if E else 0
amb = hinchada(dur + 1); env = np.clip((tt(dur + 1) - te) / 1.5, 0, 1) * .75 + .25; put(0, amb * env, .16, -.2); put(0, hinchada(dur + 1)[::-1].copy() * env, .16, .2)
if E: put(te - .1, whoosh(1.4), .4); put(te + 1.2, boom(1.4), .45); put(te + 1.3, rugido(3), .35)
for g in sc.get('goles', []):
    put(g['t'], patada(), .7); put(g['t'] + .05, whoosh(1.0), .25, -.5 * g['lado']); put(g['t'] + 1.0, red(), .5, .6 * -g['lado']); put(g['t'] + 1.0, rugido(3.8), .75); put(g['t'] + 1.05, boom(1.2), .5); put(g['t'] + 1.2, papelitos(3), .25)
for c in sc.get('capas', []):
    t0 = c['desde']; tp = c['tipo']
    if tp == 'barrido': put(t0, whoosh(.8), .45)
    elif tp == 'ficha': put(t0, whoosh(.4), .2); put(t0 + .1, tic(), .25)
    elif tp == 'marcador':
        for q in range(10): put(t0 + .3 + q * .055, tic(), .12, -.3 if q % 2 else .3)
        put(t0 + .9, boom(.9), .45)
    elif tp == 'var':
        for q in range(3): put(t0 + q * .25, pitido(), .22)
        put(t0 + (c['hasta'] - t0) * .55, boom(1.3), .55)
    elif tp == 'tarjeta': put(t0, whoosh(.5), .25, .5)
    elif tp == 'adelanto': put(t0, boom(1.2), .45); put(t0, whoosh(.6), .25)
    elif tp == 'foto' and t0 > .1: put(t0, whoosh(.5), .2)
for tj in sc.get('tarjetas3d', []): put(tj['t'], silbato(.6), .35); put(tj['t'] + .8, boom(.8), .4)
for c in sc.get('capas', []):
    if c['tipo'] == 'ficha' and 'partido' in (c.get('texto', '')).lower(): put(c['desde'], silbato(1.1), .45)
mix = np.stack([L, R])[:, :int(dur * SR)]
fv = D / sc['audio'] if sc.get('audio') else None
if fv and fv.exists():  # voz al frente: el estadio y los efectos bajan cuando habla
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(fv), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    voz = np.frombuffer(raw, np.int16).astype(np.float32) / 32768; voz = np.pad(voz, (0, max(0, mix.shape[1] - len(voz))))[:mix.shape[1]]
    env = filt(np.abs(voz), 'low', 6); duck = 1 - .6 * np.clip(env / (np.percentile(env, 95) * .5 + 1e-9), 0, 1)
    mix = mix / (np.abs(mix).max() + 1e-9) * .5 * duck + voz[None, :] * 1.0
mix /= max(1e-9, np.abs(mix).max()) / .9
tmp = D / '.tmp'; tmp.mkdir(exist_ok=True)
with wave.open(str(tmp / 'estadio.wav'), 'w') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix.T * 32767).astype(np.int16).tobytes())
video = D / (sc['salida'] + '.mp4'); out = D / (sc['salida'] + ('-final.mp4' if fv and fv.exists() else '-con-sonido.mp4'))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(video), '-i', str(tmp / 'estadio.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', str(out)], check=True)
print('listo:', out)
