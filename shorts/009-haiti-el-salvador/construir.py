"""Short 009 · ¿Qué está haciendo El Salvador en Haití? — mapa satelital realista (estilo documental) + clips de Flow + subtítulo por palabra.
    python3 shorts/009-haiti-el-salvador/construir.py        (con voz/*.mp3 si existe; si no, tiempos estimados)
    node motor-mapa/render.cjs shorts/009-haiti-el-salvador
    python3 shorts/009-haiti-el-salvador/sonido.py
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
T = b.T; DUR = round(b.fin + 1.2, 2)
cam, ev, CLIPS, sacud = [], [], [], []
ultimo = [None]
def CAM(t, lon, lat, ancho, d=.6):
    if ultimo[0]: lo, la, an = ultimo[0]; cam.append(dict(t=round(t, 2), lon=lo, lat=la, ancho=an, suave=False))
    cam.append(dict(t=round(t + d, 2), lon=lon, lat=lat, ancho=ancho)); ultimo[0] = (lon, lat, ancho)
def E(tipo, desde, dur=None, hasta=None, **kw):
    e = dict(tipo=tipo, desde=round(desde, 2), **kw)
    if hasta is not None: e['hasta'] = round(hasta, 2)
    elif dur is not None: e['hasta'] = round(desde + dur, 2)
    ev.append(e); return e
def clip(cod, a0, a1, maxdur=7.6, **ex):
    d = a1 - a0; ex.setdefault('vel', round(min(1, (maxdur - ex.get('ofs', 0)) / max(.1, d)), 3)); CLIPS.append(dict(codigo=cod, desde=round(a0, 2), hasta=round(a1, 2), etiqueta='IMAGEN ILUSTRATIVA CON IA', **ex))
TIT, CIF, CINTA = 300, 330, 1185
SSV, PAP, CDB = (-89.19, 13.69), (-72.34, 18.54), (-72.2, 18.58)     # San Salvador, Puerto Príncipe, Croix-des-Bouquets

clip('N03', 0, T('a un país que está', d=-.05), entra=.01, z0=1.0, z1=1.1)
E('cifra', .1, texto='+2,000', tam=200, sub='soldados de El Salvador', y=CIF, hasta=T('a un país que está'))
CAM(0, -80.5, 16, 26, d=0); CAM(T('a un país que está', d=-.05), -80.5, 16, 24, d=1.2)
E('ruta', T('a un país que está'), puntos=[list(SSV), list(PAP)], dur=1.4, color='#ffd23f', hasta=T('¿Por qué?'))
E('pin', T('a un país que está'), lon=SSV[0], lat=SSV[1], texto='SAN SALVADOR', escala=1.5, hasta=T('Haití.'))
E('pin', T('casi dos mil', d=.2), lon=PAP[0], lat=PAP[1], texto='PUERTO PRÍNCIPE', escala=1.5, hasta=T('¿Por qué?'))
E('cifra', T('casi dos mil'), texto='1,880 km', tam=170, sub='en línea recta', y=CIF, hasta=T('Haití.'))
CAM(T('Haití.', d=-.1), -72.7, 18.95, 4.6, d=.7)
E('resaltar', T('Haití.'), pais='HTI', color='#ff5a4a', hasta=T('En Puerto Príncipe'))
E('titulo', T('¿Por qué?'), texto='¿POR QUÉ?', tam=110, y=TIT, hasta=T('En Puerto Príncipe'))
clip('N01', T('En Puerto Príncipe', d=-.1), T('Y más de un millón', d=-.05))
E('cifra', T('las pandillas controlan'), texto='≈ 85 %', tam=180, sub='de la capital, en manos de pandillas (ONU)', y=CIF, hasta=T('Y más de un millón'))
clip('N06', T('Y más de un millón', d=-.1), T('El Salvador ya tenía', d=-.05))
E('cifra', T('Y más de un millón'), texto='1.4 MILLONES', tam=140, sub='de personas tuvieron que huir', y=CIF, hasta=T('El Salvador ya tenía'))
CAM(T('El Salvador ya tenía', d=-.15), -72.3, 18.6, 1.7, d=.6)
E('pin', T('El Salvador ya tenía'), lon=PAP[0], lat=PAP[1], texto='PUERTO PRÍNCIPE', escala=1.5, hasta=T('Bukele respondió'))
E('cinta', T('en la fuerza internacional'), x=960, y=CINTA, escala=1.2, texto='FUERZA DE LA ONU CONTRA PANDILLAS', icono='globo', color='#1f6aa8', hasta=T('Pero el dieciocho'))
clip('N05', T('Pero el dieciocho', d=-.1), T('Bukele respondió', d=-.05))
E('fecha', T('Pero el dieciocho'), texto='18 DE OCTUBRE', hasta=T('Bukele respondió'))
E('cinta', T('cuatro técnicos'), x=960, y=CINTA, escala=1.25, texto='4 TÉCNICOS DESAPARECIDOS', icono='', color='#d6453d', hasta=T('Bukele respondió'))
clip('N04', T('Bukele respondió', d=-.1), T('y el diez de noviembre', d=-.05), maxdur=4.8)
E('titulo', T('Bukele respondió'), texto='RESPUESTA\nEN GRANDE', tam=92, y=TIT, hasta=T('y el diez de noviembre'))
CAM(T('y el diez de noviembre', d=-.15), -72.15, 18.62, 1.1, d=.6)
E('fecha', T('y el diez de noviembre'), texto='10 DE NOVIEMBRE', hasta=T('El gobierno de Haití'))
E('pin', T('el ataque al cuartel'), lon=CDB[0], lat=CDB[1], texto='ZONA DE 400 MAWOZO', escala=1.5, color='#e8463a', hasta=T('El gobierno de Haití'))
CAM(T('El gobierno de Haití', d=-.1), -72.7, 18.95, 4.6, d=.6)
E('cinta', T('El gobierno de Haití'), x=960, y=CINTA, escala=1.25, texto='HAITÍ: "GRACIAS"', icono='corazon', color='#2e9e5b', hasta=T('La ONU, en cambio'))
E('cifra', T('La ONU, en cambio'), texto='≈ 200', tam=200, sub='de más de 2,000 están en la misión de la ONU', y=CIF, hasta=T('Y los cuatro'))
clip('N02', T('Y los cuatro', d=-.1), T('¿Es el principio', d=-.05))
E('titulo', T('siguen sin aparecer'), texto='SIGUEN SIN\nAPARECER', tam=100, y=TIT, hasta=T('¿Es el principio'))
CAM(T('¿Es el principio', d=-.1), -80.5, 16, 22, d=2.2)
E('pregunta', T('¿Es el principio'), texto='¿FIN DE LAS PANDILLAS O GUERRA SIN SALIDA?', y=CINTA, hasta=DUR)
E('resaltar', T('¿Es el principio'), pais='HTI', color='#ff5a4a', hasta=DUR)
E('resaltar', T('¿Es el principio', d=.3), pais='SLV', color='#4ea3ff', hasta=DUR)

for c in CLIPS:
    dst = DIR / '.clips' / c['codigo']
    if not dst.exists():
        dst.mkdir(parents=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(DIR / 'clips' / f"{c['codigo']}.mp4"), '-vf', 'scale=1080:1920:flags=lanczos,fps=30', '-q:v', '3', str(dst / '%04d.jpg')], check=True)
cam.sort(key=lambda k: k['t'])
for i in range(1, len(cam)):
    if cam[i]['t'] <= cam[i - 1]['t']: cam[i]['t'] = round(cam[i - 1]['t'] + .02, 2)
spec = dict(estilo='documental', formato='vertical', salida='el-salvador-en-haiti', duracion=DUR, camara=cam, sacudidas=sacud, eventos=sorted(ev, key=lambda e: e['desde']),
            clips=CLIPS, palabras=palabras_de(b), resaltar=['SALVADOR', 'HAITÍ', 'PANDILLAS', 'BUKELE', 'ONU', 'DESAPARECIDOS', 'MAWOZO', 'GUERRA', 'APARECER', 'HUIR'],
            capY=1420, capTam=104, fundido_inicio=0)
if CON_VOZ:
    tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(DIR / 'voz' / 'limpia.wav'), '-af', f'adelay={int(INICIO * 1000)},apad=whole_dur={DUR},loudnorm=I=-16:TP=-2:LRA=11', '-ar', '48000', '-ac', '1', str(tmp / 'voz.wav')], check=True)
    spec['audio'] = '.tmp/voz.wav'
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print(f"Short 009 · {'CON VOZ' if CON_VOZ else 'SIN VOZ (tiempos estimados)'} · {len(ev)} capas · {len(CLIPS)} clips · {DUR:.1f} s")
