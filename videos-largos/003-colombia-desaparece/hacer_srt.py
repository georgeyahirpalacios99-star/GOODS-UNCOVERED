"""Subtítulos exactos (texto del guion + tiempos del alineador) para subir a YouTube.
    python3 videos-largos/003-colombia-desaparece/hacer_srt.py
"""
import re
from pathlib import Path
D = Path(__file__).resolve().parent
src = (D / 'construir.py').read_text(encoding='utf-8').split('cam, ev, caras, mirar')[0].replace('Path(__file__)', f'Path({str(D / "construir.py")!r})')
exec(src)
def hms(t): h, r = divmod(t, 3600); m, s = divmod(r, 60); return f'{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}'
def trozos(u, n=84):  # máximo 2 líneas de ~42 letras
    if len(u) <= n: return [u]
    pal, out, cur = u.split(), [], ''
    for p in pal:
        if len(cur) + len(p) + 1 > n and cur: out.append(cur); cur = p
        else: cur = (cur + ' ' + p).strip()
    return out + [cur]
def lineas(t):
    if len(t) <= 42: return t
    pal = t.split(); mejor = min(range(1, len(pal)), key=lambda i: abs(len(' '.join(pal[:i])) - len(' '.join(pal[i:])))); return ' '.join(pal[:mejor]) + '\n' + ' '.join(pal[mejor:])
subs = []
for b in B:
    for u, (a, c) in zip(b.us, b.tramos):
        ps = trozos(u); tot = sum(len(p) for p in ps); acc = 0
        for p in ps:
            t1 = b.t0 + b._en(a, c, acc / tot); acc += len(p); t2 = b.t0 + b._en(a, c, acc / tot); subs.append((t1, t2 + .15, p))
out = []
for i, (t1, t2, p) in enumerate(subs, 1):
    if i < len(subs): t2 = min(t2, subs[i][0] - .02)
    out.append(f'{i}\n{hms(t1)} --> {hms(t2)}\n{lineas(p)}\n')
(D / 'subtitulos.srt').write_text('\n'.join(out), encoding='utf-8')
print(len(subs), 'subtítulos →', D / 'subtitulos.srt')
