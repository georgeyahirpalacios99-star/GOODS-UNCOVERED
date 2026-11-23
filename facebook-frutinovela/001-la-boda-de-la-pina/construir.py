"""Frutinovela 001 · La boda de la piña (Reel de Facebook). Los clips de Flow ya traen los diálogos: se montan en orden, con gancho, títulos, sonido y música bajita.
    python3 facebook-frutinovela/001-la-boda-de-la-pina/construir.py
    node motor-mapa/render.cjs facebook-frutinovela/001-la-boda-de-la-pina
    python3 facebook-frutinovela/001-la-boda-de-la-pina/sonido.py
"""
import json, subprocess
from pathlib import Path
DIR = Path(__file__).resolve().parent
GANCHO, LARGO = 1.9, 7.9          # avance mudo del pastelazo + duración de cada clip
ev, CLIPS, sacud, dest = [], [], [], []
def E(tipo, desde, hasta, **kw): ev.append(dict(tipo=tipo, desde=round(desde, 2), hasta=round(hasta, 2), **kw))
ETI = 'HECHO CON IA'
CLIPS.append(dict(codigo='F7', desde=0, hasta=GANCHO, ofs=.9, vel=1, entra=.01, sale=.01, z0=1.12, z1=1.2, etiqueta=ETI))
E('titulo', .05, GANCHO - .05, texto='LA BODA\n*SE ARRUINÓ*', tam=130, y=330, capa='C')
#          clip, rótulo de escena,        título de impacto (corto, arriba),  segundo en que entra el título, sacudida
ESC = [('F1', 'LA BODA DEL AÑO',        'TODO ERA *PERFECTO*',   .4, None),
       ('F2', 'EL NOVIO',               'ÉL ESCONDÍA *ALGO*',    .6, None),
       ('F3', 'DE PRONTO…',             'ALGUIEN *INTERRUMPE*',  1.2, 1.2),
       ('F4', 'LA PRUEBA',              '¡*POSITIVO*!',          3.2, 3.2),
       ('F5', 'LA NOVIA',               'NO PUEDE *CREERLO*',    1.0, 2.2),
       ('F6', 'EL NOVIO SUPLICA',       '¿LO *PERDONA*?',        2.0, None),
       ('F7', 'LA RESPUESTA',           '¡*PASTELAZO*!',         1.3, 1.3),
       ('F8', 'AFUERA DE LA IGLESIA',   'Y FALTABA *LO PEOR*…',  4.6, None)]
for i, (cod, rot, tit, tt, sac) in enumerate(ESC):
    t0 = GANCHO + i * LARGO; t1 = t0 + LARGO
    CLIPS.append(dict(codigo=cod, desde=round(t0, 2), hasta=round(t1, 2), vel=1, entra=.01, sale=.01, z0=1.0, z1=1.07, etiqueta=ETI))
    E('fecha', t0 + .15, t1 - .2, texto=rot)
    E('titulo', t0 + tt, min(t1 - .2, t0 + tt + 2.0), texto=tit, tam=96, y=300, capa='C')
    if sac is not None: sacud.append(dict(t=round(t0 + sac, 2), dur=.45, fuerza=12)); dest.append(round(t0 + sac, 2))
DUR = round(GANCHO + len(ESC) * LARGO, 2)
E('pregunta', DUR - 2.6, DUR, texto='¿QUIERES LA PARTE 2? COMENTA "PIÑA"', y=1500)
for c in {c['codigo'] for c in CLIPS}:
    dst = DIR / '.clips' / c
    if not dst.exists():
        dst.mkdir(parents=True); subprocess.run(['ffmpeg', '-v', 'error', '-i', str(DIR / 'clips' / f'{c}.mp4'), '-vf', 'scale=1080:1920:flags=lanczos,fps=30', '-q:v', '3', str(dst / '%04d.jpg')], check=True)
# audio: los diálogos de cada clip, nivelados uno por uno, después del gancho mudo
tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True); partes = []
for i, (cod, *_r) in enumerate(ESC):
    o = tmp / f'a{i}.wav'; partes.append(o)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(DIR / 'clips' / f'{cod}.mp4'), '-t', str(LARGO), '-af', f'loudnorm=I=-17:TP=-2:LRA=11,afade=t=in:d=0.03,afade=t=out:st={LARGO - .05:.2f}:d=0.05,apad=whole_dur={LARGO}', '-ar', '48000', '-ac', '1', str(o)], check=True)
lista = tmp / 'lista.txt'; lista.write_text(''.join(f"file '{p}'\n" for p in partes))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(lista), '-af', f'adelay={int(GANCHO * 1000)},apad=whole_dur={DUR}', '-ar', '48000', '-ac', '1', str(tmp / 'voz.wav')], check=True)
cam = [dict(t=0, lon=-78, lat=-1, ancho=40), dict(t=DUR, lon=-78, lat=-1, ancho=40)]
spec = dict(estilo='documental', formato='vertical', salida='la-boda-de-la-pina', duracion=DUR, camara=cam, sacudidas=sacud, eventos=sorted(ev, key=lambda e: e['desde']),
            clips=CLIPS, tipografia='cine', fundido_inicio=0, barra=True, destellos=dest, audio='.tmp/voz.wav')
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'Frutinovela 001 · {len(CLIPS)} clips · {DUR:.1f} s')
