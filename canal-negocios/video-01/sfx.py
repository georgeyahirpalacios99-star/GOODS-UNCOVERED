"""Efectos de sonido sincronizados con la animación (sintetizados, sin licencias): lee mapa.json y escribe voz/sfx.wav
Cortes = whoosh · rayos/flash = impacto · textos grandes = golpe · cifras = tic-tic + caja registradora
+$1.25 = campanita · etiquetas y listas = pop · capítulos = tecleo · barras = barrido · neón apagado = zumbido
"""
import json, numpy as np, wave
from pathlib import Path
D = Path(__file__).resolve().parent
SP = json.load(open(D / 'mapa.json')); SR = 48000; N = int(SP['duracion'] * SR) + SR
out = np.zeros(N, np.float32); rng = np.random.default_rng(7)
T = lambda d: np.arange(int(d * SR)) / SR
def lp(x, a):  # filtro paso bajo de un polo con coeficiente (variable) a
    y = np.empty_like(x); v = 0.0; a = np.broadcast_to(a, x.shape)
    for i in range(len(x)): v += a[i] * (x[i] - v); y[i] = v
    return y
def put(t0, s, g=1.0):
    i = int(t0 * SR)
    if i < 0: s = s[-i:]; i = 0
    j = min(N, i + len(s)); out[i:j] += g * s[:j - i]
CACHE = {}
def sonido(nombre):
    if nombre in CACHE: return CACHE[nombre]
    if nombre == 'whoosh':
        t = T(.5); env = np.sin(np.pi * t / t[-1]) ** 2; a = .02 + .25 * env; s = lp(rng.standard_normal(len(t)), a) * env * 1.6
    elif nombre == 'impacto':
        t = T(.9); f = 40 + 50 * np.exp(-t * 7); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5) * .9
        s += lp(rng.standard_normal(len(t)), .3) * np.exp(-t * 30) * .9
    elif nombre == 'golpe':
        t = T(.35); s = np.sin(2 * np.pi * np.cumsum(90 + 120 * np.exp(-t * 18)) / SR) * np.exp(-t * 11) * .7 + lp(rng.standard_normal(len(t)), .5) * np.exp(-t * 45) * .5
    elif nombre in ('pop', 'pop2'):
        t = T(.09); f0 = 500 if nombre == 'pop' else 900; s = np.sin(2 * np.pi * np.cumsum(f0 + (f0 * 1.2) * t / t[-1]) / SR) * np.exp(-t * 45) * .55
    elif nombre == 'ding':
        t = T(.6); s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in [(1568, .5, 7), (2349, .3, 10), (3136, .15, 14)])
    elif nombre == 'caja':
        t = T(.9); s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in [(2093, .45, 5), (3136, .25, 7)])
        s2 = np.zeros_like(s); s2[int(.07 * SR):] = s[:len(s) - int(.07 * SR)] * .9; n = rng.standard_normal(len(t)); n = n - lp(n, .35)
        s = s + s2 + n * np.exp(-t * 25) * .35
    elif nombre == 'tic':
        t = T(.012); s = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 400) * .5
    elif nombre == 'subida':
        t = T(.7); s = np.sin(2 * np.pi * np.cumsum(250 + 900 * (t / t[-1]) ** 1.5) / SR) * np.sin(np.pi * t / t[-1]) * .35 + lp(rng.standard_normal(len(t)), .15) * np.sin(np.pi * t / t[-1]) * .3
    elif nombre == 'bajada':
        t = T(.8); s = np.sin(2 * np.pi * np.cumsum(700 - 520 * (t / t[-1])) / SR) * np.sin(np.pi * t / t[-1]) * .4
    elif nombre == 'zumbido':
        t = T(.45); s = np.sign(np.sin(2 * np.pi * 120 * t)) * .25 * (rng.random(len(t)) > .3) * np.exp(-t * 4) + lp(rng.standard_normal(len(t)), .6) * .15 * np.exp(-t * 8)
    elif nombre == 'raya':
        t = T(.25); n = rng.standard_normal(len(t)); s = (n - lp(n, .2)) * np.sin(np.pi * t / t[-1]) * .5
    m = np.abs(s).max(); s = (s / m * .9 if m > 0 else s).astype(np.float32); CACHE[nombre] = s; return s

tomas = SP['tomas']
for i, tm in enumerate(tomas):
    if i == 0: continue
    if tm['tipo'] == 'rayos' or tm.get('flash'): put(tm['desde'], sonido('impacto'), .55)
    else: put(tm['desde'] - .25, sonido('whoosh'), .22)
    if tm.get('apagar'): put(tm['apagar'], sonido('zumbido'), .35)
    if tm['tipo'] == 'ciudad':
        for k in range(min(40, tm.get('n', 70))): put(tm['desde'] + .5 + k * tm.get('paso', .055) * (tm.get('n', 70) / 40), sonido('tic'), .25)
for e in SP['eventos']:
    t0, tp = e['desde'], e['tipo']
    if tp == 'golpe': put(t0, sonido('golpe'), .45)
    elif tp == 'cifra':
        put(t0, sonido('pop'), .35); d = e.get('dur', 2)
        if d > .3:
            for k in np.arange(t0 + .1, t0 + .1 + d, .075): put(k, sonido('tic'), .22)
        put(t0 + .1 + d, sonido('caja' if '$' in (e.get('prefijo', '') + e.get('sufijo', '')) else 'ding'), .3)
    elif tp == 'pops':
        ts = e.get('tiempos', []); g = .16 if len(ts) < 2 or ts[1] - ts[0] > .5 else .09
        for k in ts: put(k, sonido('ding'), g)
    elif tp in ('precio', 'piensa', 'rotulo', 'pregunta'): put(t0, sonido('pop'), .4)
    elif tp == 'precios':
        for it in e['items']: put(it[0], sonido('pop'), .4)
    elif tp == 'lista':
        for it in e['items']: put(it[0], sonido('pop2'), .3)
    elif tp == 'capitulo':
        for k in np.arange(t0 + .35, t0 + 1.05, .055): put(k + rng.random() * .02, sonido('tic'), .4)
    elif tp == 'cambio': put(e['tachar'], sonido('raya'), .4); put(e['tachar'] + .5, sonido('caja'), .35)
    elif tp == 'barra':
        for q in e['partes']:
            if q['desde'] < 90 and q['desde'] >= t0: put(q['desde'], sonido('subida'), .3)
    elif tp == 'comparar':
        for j, b in enumerate(e['barras']): put(b['desde'], sonido('subida' if j == 0 else 'bajada'), .32)
    elif tp == 'versus': put(t0, sonido('pop'), .4); put(e.get('derDesde', t0 + 1.5), sonido('pop'), .4)
    elif tp == 'persona' and e.get('signos'):
        for k in range(3): put(e['signos'] + k * .2, sonido('pop2'), .3)
pico = np.abs(out).max(); out = np.clip(out, -1, 1)
with wave.open(str(D / 'voz' / 'sfx.wav'), 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print('sfx listo · pico', round(float(pico), 2))
