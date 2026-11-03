"""Efectos para la invitación (sintetizados): pops de letras, destellos, barridos."""
import numpy as np, wave
SR = 48000; DUR = 12.5; N = int(DUR * SR); out = np.zeros(N, np.float32); rng = np.random.default_rng(3)
T = lambda d: np.arange(int(d * SR)) / SR
def lp(x, a):
    y = np.empty_like(x); v = 0.0; a = np.broadcast_to(a, x.shape)
    for i in range(len(x)): v += a[i] * (x[i] - v); y[i] = v
    return y
def put(t0, s, g):
    i = int(t0 * SR); j = min(N, i + len(s)); out[i:j] += g * s[:j - i]
def norm(s): return (s / (np.abs(s).max() + 1e-9)).astype(np.float32)
def pop(f0=520): t = T(.1); return norm(np.sin(2 * np.pi * np.cumsum(f0 + f0 * 1.3 * t / t[-1]) / SR) * np.exp(-t * 40))
def ding(f=1568): t = T(.8); return norm(sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * k) for m, a, k in [(1, .6, 5), (1.5, .3, 8), (2, .15, 11)]))
def whoosh(d=.45): t = T(d); env = np.sin(np.pi * t / t[-1]) ** 2; return norm(lp(rng.standard_normal(len(t)), .02 + .2 * env) * env)
def brillo(): t = T(1.0); s = sum(np.sin(2 * np.pi * f * t) * np.exp(-((t - d) * 9) ** 2) for f, d in [(2093, .05), (2637, .15), (3136, .25), (4186, .35)]); return norm(s * np.exp(-t * 2))
for t0 in (0.0, .1): put(t0, whoosh(), .22)
for t0 in (.15, .3): put(t0 + .3, pop(300), .25)
for k, t0 in enumerate((.55, .7, .85, 1.0)): put(t0 + .25, pop(600 + k * 60), .3)
put(1.25, brillo(), .12); put(2.2, whoosh(.3), .15); put(2.5, pop(900), .25); put(2.75, pop(420), .3)
for i in range(12): put(2.6 + i * .06 + .2, pop(700 + i * 25), .12)
for i in range(8): put(3.4 + i * .11 + .5, pop(380 + i * 55), .32)
put(4.45, brillo(), .28); put(4.55, whoosh(.3), .15); put(4.7, pop(950), .2); put(5.1, pop(950), .2)
for t0 in (4.8, 5.1, 5.4): put(t0, whoosh(.5), .25)
for t0 in (5.3, 5.6, 5.9): put(t0, pop(650), .25)
put(6.4, whoosh(.8), .3); put(6.9, brillo(), .1); put(7.4, brillo(), .1); put(8.4, ding(), .2)
for t0 in (8.2, 10.6): put(t0 + .3, brillo(), .22)
out = np.clip(out, -1, 1)
with wave.open('sfx.wav', 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print('ok')
