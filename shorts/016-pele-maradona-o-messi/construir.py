"""Short 016 · ¿Pelé, Maradona o Messi? — tramo "VAR de leyendas" del video largo 008, en vertical 1080x1920.
    python3 shorts/016-pele-maradona-o-messi/construir.py
    node motor-3d/render3d.cjs shorts/016-pele-maradona-o-messi
    python3 motor-3d/sonido_estadio.py shorts/016-pele-maradona-o-messi
"""
import json, subprocess
from pathlib import Path
D = Path(__file__).resolve().parent; V = D.parent.parent / 'videos-largos' / '008-argentina-vs-brasil'
A, B = 222.25, 264.35   # "el VAR tiene que revisar…" → "…¿Pelé, Maradona o Messi?"
COLA = .8; DUR = round(B - A + COLA, 2)
s = json.loads((V / 'escena.json').read_text())
rel = lambda p: '../../videos-largos/008-argentina-vs-brasil/' + p
def corta(lst):
    out = []
    for c in lst:
        if c['hasta'] <= A or c['desde'] >= B + COLA: continue
        c = dict(c, desde=round(max(0, c['desde'] - A), 2), hasta=round(min(DUR, c['hasta'] - A), 2))
        if c.get('img'): c['img'] = rel(c['img'])
        out.append(c)
    return out
capas = corta(s['capas'])
for c in capas:
    if c['tipo'] == 'ficha': c['y'] = 1380                       # fichas abajo, sobre el tercio inferior vertical
    if c['tipo'] == 'var' and 'Messi' in c.get('texto', ''): c.update(hasta=DUR, veredicto='Comenta: ¿cuál?')
    if c['tipo'] == 'barrido': c['hasta'] = min(c['hasta'], DUR)
    if c['tipo'] == 'var': c['yEt'] = 200
    if c['tipo'] == 'foto' and 'pele-1' in c['img']: c['fy'] = 0
# gancho: titular grande los primeros segundos, encima del VAR
capas.insert(0, dict(tipo='titular', desde=0, hasta=round(228.15 - A, 2), texto='¿Quién es el mejor\nde la historia?', y=560, tam=118))
capas.append(dict(tipo='titular', desde=round(258.95 - A, 2), hasta=DUR, texto='Pelé · Maradona\no Messi', y=560, tam=112))
cam = [dict(c, t=round(c['t'] - A, 2)) for c in s['camara']]
corto = dict(s, salida='pele-maradona-o-messi', duracion=DUR, ancho=1080, alto=1920, calidad3d=.9, capas=capas,
             camara=[c for c in cam if -30 < c['t'] < DUR + 30] or cam[-1:], goles=[dict(g, t=round(g['t'] - A, 2)) for g in s['goles'] if g['t'] < A], tarjetas3d=[],
             pantalla=[], estadio=dict(s['estadio'], t=s['estadio']['t'] - A), audio='.tmp/voz.wav',
             reloj=dict(s['reloj'], desde=s['reloj']['desde'] - A, hasta=s['reloj']['hasta'] - A),
             elevar=[dict(e, desde=e['desde'] - A) for e in s['elevar']], atenuar=[dict(e, desde=e['desde'] - A) for e in s['atenuar']])
(D / 'escena.json').write_text(json.dumps(corto, ensure_ascii=False, indent=1))
(D / '.tmp').mkdir(exist_ok=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(A), '-t', str(DUR), '-i', str(V / '.tmp' / 'voz.wav'), '-af', f'afade=t=in:d=0.05,afade=t=out:st={DUR - .5:.2f}:d=0.5', str(D / '.tmp' / 'voz.wav')], check=True)
print('escena lista:', DUR, 's ·', len(capas), 'capas')
