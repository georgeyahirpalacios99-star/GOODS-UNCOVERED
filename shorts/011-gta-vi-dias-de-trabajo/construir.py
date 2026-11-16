"""Short 011 · ¿Cuántos días tienes que trabajar para comprar GTA VI en tu país? — ranking sobre mapa satelital + clips de Flow + objetos recortados.
    python3 shorts/011-gta-vi-dias-de-trabajo/construir.py
    node motor-mapa/render.cjs shorts/011-gta-vi-dias-de-trabajo
    python3 shorts/011-gta-vi-dias-de-trabajo/sonido.py
"""
import json, re, subprocess, sys
from pathlib import Path
DIR = Path(__file__).resolve().parent; sys.path.insert(0, str(DIR.parent / '007-brasil-shorts'))
from alinear import Bloque, BloqueEstimado, limpiar, palabras_de
TEXTO = re.search(r'```\n(.*?)```', (DIR / 'GUION-ELEVENLABS.md').read_text(encoding='utf-8'), re.S).group(1)
INICIO = .15
mp3 = sorted((DIR / 'voz').glob('*.mp3'))
if mp3: limpiar(mp3[0], DIR / 'voz' / 'limpia.wav'); b = Bloque(1, TEXTO, INICIO, DIR / 'voz' / 'limpia.wav'); CON_VOZ = True
else: b = BloqueEstimado(1, TEXTO, INICIO); CON_VOZ = False
T = b.T; DUR = round(b.fin + 1.6, 2)
cam, ev, CLIPS, sacud = [], [], [], []
ultimo = [None]
def CAM(t, lon, lat, ancho, d=.55):
    if ultimo[0]: lo, la, an = ultimo[0]; cam.append(dict(t=round(t, 2), lon=lo, lat=la, ancho=an, suave=False))
    cam.append(dict(t=round(t + d, 2), lon=lon, lat=lat, ancho=ancho)); ultimo[0] = (lon, lat, ancho)
def E(tipo, desde, dur=None, hasta=None, **kw):
    e = dict(tipo=tipo, desde=round(desde, 2), **kw)
    if hasta is not None: e['hasta'] = round(hasta, 2)
    elif dur is not None: e['hasta'] = round(desde + dur, 2)
    ev.append(e); return e
def clip(cod, a0, a1, maxdur=7.6, **ex):
    d = a1 - a0; ex.setdefault('vel', round(min(1, (maxdur - ex.get('ofs', 0)) / max(.1, d)), 3)); CLIPS.append(dict(codigo=cod, desde=round(a0, 2), hasta=round(a1, 2), etiqueta='IMAGEN ILUSTRATIVA CON IA', **ex))
NOM, CIF, CINTA = 250, 470, 1185
LATAM = (-74, -14, 92)
VERDE, AMAR, NARA, ROJO = '#7dffa0', '#ffd23f', '#ff9a3a', '#ff5a4a'

# ---------- 1 · gancho ----------
clip('G01', 0, T('En tu país', d=-.05), entra=.01, z0=1.0, z1=1.1)
E('titulo', .1, texto='ESTADOS UNIDOS', tam=84, y=NOM, capa='C', hasta=T('En tu país', d=-.1))
E('cifra', T('un día y medio', d=-.1), texto='1.5 DÍAS', num=[0, 1.5], dec=1, suf=' DÍAS', dur=.7, tam=190, sub='de trabajo para comprarlo', y=CIF, color=VERDE, hasta=T('En tu país', d=-.1))
E('objeto', .5, img='obj/control.png', x=540, y=830, w=330, rot=-8, hasta=T('En tu país', d=-.1))
CAM(0, *LATAM, d=0)
E('capa', T('En tu país', d=-.1), img='obj/nubes.jpg', alpha=.32, vx=16, hasta=DUR)
E('titulo', T('En tu país'), texto='¿Y EN *TU PAÍS*?', tam=104, y=NOM, capa='C', hasta=T('puede costar', d=-.05))
E('titulo', T('puede costar', d=-.05), texto='PUEDE COSTAR\n*AÑOS*', tam=120, y=NOM + 60, capa='C', hasta=T('El juego vale', d=-.1))
# ---------- 2 · la regla ----------
clip('G03', T('El juego vale', d=-.1), T('Y esto es lo que', d=-.05), maxdur=6.2)
E('cifra', T('ochenta dólares', d=-.15), texto='$79.99', tam=210, sub='precio oficial en dólares', y=CIF - 120, color=AMAR, hasta=T('Y esto es lo que', d=-.1))
clip('G04', T('Y esto es lo que', d=-.05), T('Costa Rica', d=-.1), maxdur=7.4)
E('titulo', T('alguien que gana', d=-.2), texto='CON EL\n*SALARIO MÍNIMO*', tam=100, y=NOM + 40, capa='C', hasta=T('Costa Rica', d=-.15))
# ---------- 3 · ranking ----------
#        frase ancla,        fin,              nombre en pantalla,          cifra, color, países,                cámara (lon, lat, ancho),  etiquetas en el mapa
RANK = [('Costa Rica',       'Uruguay, Panamá', 'COSTA RICA',               (3, 0),  VERDE, ['CRI'],               (-84.2, 9.0, 13),   [(-84.2, 9.9, 'CRI', '3')]),
        ('Uruguay, Panamá',  'México',          'URUGUAY · PANAMÁ · CHILE', (4, 0),  VERDE, ['URY', 'PAN', 'CHL'], (-70, -15, 78),     [(-56, -33, 'URY', '4'), (-80, 8.5, 'PAN', '4'), (-71, -31, 'CHL', '4')]),
        ('México',           'Ecuador',         'MÉXICO',                   (4.5, 1), AMAR, ['MEX'],               (-102, 21.5, 36),   [(-102, 23.5, 'MEX', '4.5')]),
        ('Ecuador',          'Colombia y',      'ECUADOR',                  (5, 0),  AMAR,  ['ECU'],               (-78.4, -2.6, 12),  [(-78.4, -1.6, 'ECU', '5')]),
        ('Colombia y',       'Bolivia y',       'COLOMBIA · PARAGUAY',      (6, 0),  AMAR,  ['COL', 'PRY'],        (-66, -11, 50),     [(-73, 4, 'COL', '5.4'), (-58, -23, 'PRY', '5.6')]),
        ('Bolivia y',        'Brasil',          'BOLIVIA · PERÚ',           (7, 0),  NARA,  ['BOL', 'PER'],        (-70, -14.5, 30),   [(-64.5, -16.7, 'BOL', '7'), (-75, -9.5, 'PER', '7')]),
        ('Brasil',           'Argentina',       'BRASIL',                   (8, 0),  NARA,  ['BRA'],               (-53, -14, 50),     [(-52, -11, 'BRA', '8')]),
        ('Argentina',        '¿Y Venezuela?',   'ARGENTINA',                (10, 0), ROJO,  ['ARG'],               (-64, -41, 44),     [(-65, -36, 'ARG', '10')])]
NUM = {'Costa Rica': 'tres días', 'Uruguay, Panamá': 'cuatro.', 'México': 'cuatro y medio', 'Ecuador': 'cinco.', 'Colombia y': 'casi seis', 'Bolivia y': 'siete.', 'Brasil': 'ocho.', 'Argentina': 'diez días'}
for i, (fr, fin, nom, (n, dec), col, paises, (lo, la, an), etis) in enumerate(RANK):
    t0, t1 = T(fr, d=-.08), T(fin, d=-.1)
    CAM(t0 - .1, lo, la, an)
    E('titulo', t0, texto='*' + nom + '*' if len(nom) < 14 else nom, tam=96 if len(nom) < 14 else 62, y=NOM, capa='C', hasta=t1)
    tc = T(NUM[fr], d=-.08)
    E('cifra', tc, texto=f'{n} DÍAS', num=[0, n], dec=dec, suf=' DÍAS', dur=.45, tam=200 if not nom.startswith('COLOMBIA') else 150, y=CIF, color=col, pre='CASI ' if nom.startswith('COLOMBIA') else '', hasta=t1)
    E('objeto', tc + .1, img='obj/billetes.png', x=880, y=CIF + 250, w=120 + n * 16, rot=6, hasta=t1)
    for p in paises: E('resaltar', t0, pais=p, color=col, relleno='rgba(255,255,255,.14)', hasta=t1)
    for (elo, ela, cod, val) in etis: E('nombre', t1 - .05, lon=elo, lat=ela, texto=f'{cod} {val}', tam=30, hasta=DUR)
ev[:] = [({k: v for k, v in e.items() if v is not None}) for e in ev]
# ---------- 4 · Venezuela ----------
tv = T('¿Y Venezuela?', d=-.08)
CAM(tv - .1, -66.5, 6.0, 17)
E('titulo', tv, texto='¿Y *VENEZUELA*?', tam=104, y=NOM, capa='C', hasta=T('Y eso es solo', d=-.1))
E('resaltar', tv, pais='VEN', color=ROJO, relleno='rgba(255,90,74,.22)', hasta=T('Y eso es solo', d=-.1))
E('cinta', T('Con el salario mínimo oficial'), x=960, y=CINTA, escala=1.15, texto='SALARIO OFICIAL · SIN BONOS', icono='', color='#8a3a34', hasta=T('Y eso es solo', d=-.1))
ta = T('dieciséis años', d=-.05)
E('cifra', ta, texto='16 AÑOS', num=[0, 16], suf=' AÑOS', dur=.9, tam=230, y=CIF + 10, color=ROJO, hasta=T('Y eso es solo', d=-.1))
E('objeto', ta + .2, img='obj/calendario.png', x=870, y=CIF + 330, w=300, rot=8, hasta=T('Y eso es solo', d=-.1))
sacud.append(dict(t=round(ta + .95, 2), dur=.6, fuerza=14))
# ---------- 5 · la consola ----------
clip('G05', T('Y eso es solo', d=-.1), T('¿Cuántos días', d=-.05))
E('titulo', T('Y eso es solo'), texto='Y ESO ES\n*SOLO EL JUEGO*', tam=96, y=NOM + 30, capa='C', hasta=T('Si no tienes', d=-.1))
E('cifra', T('seiscientos dólares', d=-.15), texto='+$600', tam=230, sub='si no tienes la consola (precio en EE. UU.)', y=CIF - 60, color=ROJO, hasta=T('¿Cuántos días', d=-.1))
E('objeto', T('Si no tienes', d=.1), img='obj/consola.png', x=540, y=880, w=420, rot=-4, hasta=T('¿Cuántos días', d=-.1))
# ---------- 6 · cierre ----------
clip('G02', T('¿Cuántos días', d=-.05), T('Escribe tu país', d=-.1))
E('titulo', T('¿Cuántos días'), texto='¿CUÁNTOS DÍAS\nTE CUESTA *A TI*?', tam=96, y=NOM + 30, capa='C', hasta=T('Escribe tu país', d=-.15))
CAM(T('Escribe tu país', d=-.3), -66.5, 6.0, 17, d=0); CAM(T('Escribe tu país', d=-.1), *LATAM, d=1.2)
E('pregunta', T('Escribe tu país'), texto='ESCRIBE TU PAÍS EN LOS COMENTARIOS', y=CINTA, hasta=DUR)
E('nombre', T('Escribe tu país'), lon=-66.5, lat=7.5, texto='VEN 16 años', tam=30, hasta=DUR)

DESTELLOS = [round(ta + .95, 2)]
for c in CLIPS:
    dst = DIR / '.clips' / c['codigo']
    if not dst.exists():
        dst.mkdir(parents=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(DIR / 'clips' / f"{c['codigo']}.mp4"), '-vf', 'scale=1080:1920:flags=lanczos,fps=30', '-q:v', '3', str(dst / '%04d.jpg')], check=True)
# deriva lenta: el mapa nunca queda quieto
base = sorted(cam, key=lambda k: k['t']); extra = []
for k1, k2 in zip(base, base[1:]):
    if k1.get('suave') is False or k2.get('suave') is not False: continue
    if k2['t'] - k1['t'] > 1.0: extra.append(dict(t=round(k2['t'] - .05, 2), lon=k1['lon'], lat=k1['lat'], ancho=round(k1['ancho'] * .92, 3)))
cam += extra; cam.sort(key=lambda k: (k['t'], k.get('suave') is not False))
for i in range(1, len(cam)):
    if cam[i]['t'] <= cam[i - 1]['t']: cam[i]['t'] = round(cam[i - 1]['t'] + .02, 2)
spec = dict(estilo='documental', formato='vertical', salida='gta-vi-dias-de-trabajo', duracion=DUR, camara=cam, sacudidas=sacud, eventos=sorted(ev, key=lambda e: e['desde']),
            clips=CLIPS, palabras=palabras_de(b), resaltar=['GTA', 'SEIS', 'AÑOS', 'DÍAS', 'OCHENTA', 'DÓLARES', 'VENEZUELA', 'DIECISÉIS', 'CONSOLA', 'SEISCIENTOS', 'PAÍS', 'TRES', 'CUATRO', 'CINCO', 'SIETE', 'OCHO', 'DIEZ'],
            capY=1420, capTam=104, fundido_inicio=0, barra=True, destellos=DESTELLOS)
if CON_VOZ:
    tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(DIR / 'voz' / 'limpia.wav'), '-af', f'adelay={int(INICIO * 1000)},apad=whole_dur={DUR},loudnorm=I=-16:TP=-2:LRA=11', '-ar', '48000', '-ac', '1', str(tmp / 'voz.wav')], check=True)
    spec['audio'] = '.tmp/voz.wav'
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
if CON_VOZ: b.informe()
print(f"Short 011 · {'CON VOZ' if CON_VOZ else 'SIN VOZ'} · {len(ev)} capas · {len(CLIPS)} clips · {DUR:.1f} s")
