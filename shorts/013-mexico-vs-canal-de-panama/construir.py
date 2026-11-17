"""Short 013 · México quiere quitarle los barcos al Canal de Panamá con un tren — mapa satelital con países rayados, lista de claves, barras y clips de Flow.
    python3 shorts/013-mexico-vs-canal-de-panama/construir.py
    node motor-mapa/render.cjs shorts/013-mexico-vs-canal-de-panama
    python3 shorts/013-mexico-vs-canal-de-panama/sonido.py
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
NOM, CIF, CINTA = 250, 330, 1185
VERDE, AMAR, NARA, ROJO = '#3ddc7a', '#ffd23f', '#ff9a3a', '#ff4a4a'
PAN, GAT, SCZ, COA = (-79.75, 9.05), (-79.87, 9.2), (-95.2, 16.17), (-94.42, 18.15)
VIA = [[-95.2, 16.17], [-95.1, 16.56], [-95.03, 16.88], [-95.04, 17.4], [-94.95, 17.67], [-94.42, 18.15]]
AMBOS = (-87.5, 14.0, 34)
def claves(t0, t1, activa=None):
    it = [dict(texto=x, desde=round(t0 + (i * .45 if activa is None else 0), 2)) for i, x in enumerate(['EL LAGO', 'EL TREN', 'EL PROBLEMA'])]
    if activa is not None: it[activa]['activa'] = round(t0, 2)
    E('claves', t0, items=it, y=600, tam=54, alto=112, hasta=t1)

# ---------- 1 · gancho ----------
clip('M01', 0, T('Y México quiere', d=-.05), maxdur=3.9, entra=.01, z0=1.0, z1=1.08)
E('titulo', .1, texto='EL CANAL DE PANAMÁ\n*SE QUEDA SIN AGUA*', tam=86, y=NOM, capa='C', hasta=T('Y México quiere', d=-.1))
CAM(0, *AMBOS, d=0)
E('capa', T('Y México quiere', d=-.1), img='obj/nubes.jpg', alpha=.26, vx=16, hasta=DUR)
E('resaltar', T('Y México quiere'), pais='MEX', color=VERDE, rayas=True, relleno='rgba(61,220,122,.10)', hasta=T('El lago.'))
E('resaltar', T('Y México quiere', d=.2), pais='PAN', color=ROJO, rayas=True, relleno='rgba(255,74,74,.12)', hasta=T('El lago.'))
E('flujo', T('quedarse con sus barcos'), de=list(PAN), a=[-94.8, 17.1], n=5, hasta=T('Para entenderlo'))
E('titulo', T('usando un tren', d=-.1), texto='¿CON UN *TREN*?', tam=120, y=NOM, capa='C', hasta=T('Para entenderlo', d=-.1))
claves(T('un lago', d=-.1), T('El lago.', d=-.1))
# ---------- 2 · el lago ----------
CAM(T('El lago.', d=-.1), -79.8, 8.95, 3.4, d=.7)
claves(T('El lago.'), T('Los barcos no cruzan', d=-.1), 0)
E('muralla', T('El lago.', d=.3), puntos=[[-79.92, 9.36], [-79.9, 9.2], [-79.72, 9.1], [-79.6, 9.0], [-79.55, 8.93]], dur=1.0, grosor=12, color='#4ea3ff', hasta=T('Este año'))
E('pin', T('El lago.', d=.4), lon=GAT[0], lat=GAT[1], texto='LAGO GATÚN', escala=1.5, color='#4ea3ff', hasta=T('En la sequía'))
clip('M02', T('Los barcos no cruzan', d=-.05), T('Y cuando no llueve', d=-.05), maxdur=3.9, circulo=True)
E('cinta', T('con agua dulce', d=-.2), x=960, y=CINTA, escala=1.2, texto='SUBEN CON AGUA DULCE', icono='', color='#1f6aa8', hasta=T('Y cuando no llueve', d=-.1))
clip('M03', T('Y cuando no llueve', d=-.05), T('En la sequía', d=-.05), maxdur=3.9, circulo=True)
E('titulo', T('el lago baja', d=-.1), texto='EL LAGO *BAJA*', tam=110, y=NOM, capa='C', hasta=T('En la sequía', d=-.1))
E('fecha', T('En la sequía'), texto='SEQUÍA DE 2023', hasta=T('Este año'))
E('barras', T('En la sequía', d=.2), titulo='BARCOS POR DÍA', y=1080, ancho=270, alto=430, items=[dict(valor=36, texto='NORMAL', color='#4ea3ff', desde=round(T('treinta y seis', d=-.1), 2)), dict(valor=22, texto='SEQUÍA', color=ROJO, desde=round(T('a unos veintidós', d=-.1), 2))], hasta=T('Este año', d=-.1))
clip('M04', T('Este año', d=-.05), T('El tren.', d=-.05), maxdur=3.9, circulo=True)
E('cinta', T('Este año', d=.2), x=960, y=CINTA, escala=1.15, texto='2026 · EL NIÑO: NUEVOS RECORTES', icono='', color='#8a3a34', hasta=T('El tren.', d=-.1))
# ---------- 3 · el tren ----------
CAM(T('El tren.', d=-.1), -94.8, 16.6, 8.5, d=.8)
claves(T('El tren.'), T('Aquí, en el punto', d=.6), 1)
E('resaltar', T('El tren.'), pais='MEX', color=VERDE, rayas=True, relleno='rgba(61,220,122,.08)', hasta=T('Pero hay un problema'))
E('muralla', T('solo hay unos', d=-.2), puntos=VIA, dur=1.4, grosor=14, color=NARA, hasta=T('Pero hay un problema'))
E('cifra', T('solo hay unos', d=.1), texto='≈ 300 km', num=[0, 300], pre='≈ ', suf=' km', dur=.9, tam=190, sub='entre el Pacífico y el Atlántico', y=CIF, color=NARA, hasta=T('La idea'))
E('pin', T('en Salina Cruz', d=-.1), lon=SCZ[0], lat=SCZ[1], texto='SALINA CRUZ', escala=1.4, hasta=T('Pero hay un problema'))
E('pin', T('en Coatzacoalcos', d=-.1), lon=COA[0], lat=COA[1], texto='COATZACOALCOS', escala=1.4, hasta=T('Pero hay un problema'))
E('titulo', T('La idea'), texto='BARCO → *TREN* → BARCO', tam=84, y=NOM, capa='C', hasta=T('Pero hay un problema', d=-.1))
E('ruta', T('el barco descarga'), puntos=[[-99.5, 13.2], list(SCZ)], dur=.9, color='#ffffff', hasta=T('Pero hay un problema'))
E('ruta', T('y otro barco', d=-.1), puntos=[list(COA), [-90.5, 21.8]], dur=.9, color='#ffffff', hasta=T('Pero hay un problema'))
# ---------- 4 · el problema ----------
clip('M07', T('Pero hay un problema', d=-.05), T('Para moverlos', d=-.05), maxdur=3.9)
claves(T('Pero hay un problema'), T('Un solo barco', d=-.1), 2)
E('cifra', T('catorce mil', d=-.15), texto='14,000', num=[0, 14000], dur=.9, tam=230, sub='contenedores en un solo barco', y=CIF, color=ROJO, hasta=T('Para moverlos', d=-.1))
clip('M08', T('Para moverlos', d=-.05), T('Por eso México', d=-.05), maxdur=3.9, circulo=True)
E('titulo', T('decenas de trenes', d=-.1), texto='DECENAS DE *TRENES*', tam=96, y=NOM, capa='C', hasta=T('Por eso México', d=-.1))
# ---------- 5 · cierre ----------
CAM(T('Por eso México', d=-.2), -94.8, 16.6, 8.5, d=0); CAM(T('Por eso México', d=-.1), *AMBOS, d=1.4)
E('titulo', T('Por eso México'), texto='NO PUEDE\n*REEMPLAZAR* AL CANAL', tam=84, y=NOM, capa='C', hasta=T('Pero cada vez', d=-.1))
E('resaltar', T('Por eso México'), pais='MEX', color=VERDE, rayas=True, relleno='rgba(61,220,122,.10)', hasta=DUR)
E('resaltar', T('Pero cada vez'), pais='PAN', color=ROJO, rayas=True, relleno='rgba(255,74,74,.14)', hasta=DUR)
E('muralla', T('Por eso México'), puntos=VIA, dur=.01, grosor=10, color=NARA, hasta=DUR)
E('pregunta', T('el tren gana', d=-.1), texto='CUANDO PANAMÁ SE SECA, EL TREN GANA', y=CINTA, hasta=DUR)
sacud.append(dict(t=round(T('Pero hay un problema'), 2), dur=.5, fuerza=10))
DESTELLOS = [round(T('Pero hay un problema'), 2)]
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
spec = dict(estilo='documental', formato='vertical', salida='mexico-vs-canal-de-panama', duracion=DUR, camara=cam, sacudidas=sacud, eventos=sorted(ev, key=lambda e: e['desde']),
            clips=CLIPS, palabras=palabras_de(b), resaltar=['PANAMÁ', 'AGUA', 'MÉXICO', 'TREN', 'BARCOS', 'LAGO', 'PROBLEMA', 'GATÚN', 'SEQUÍA', 'VEINTIDÓS', 'TRESCIENTOS', 'CATORCE', 'TRENES', 'CANAL', 'CLIENTES', 'OCÉANOS'],
            capY=1500, capTam=66, capEstilo='caja', fundido_inicio=0, barra=True, destellos=DESTELLOS)
if CON_VOZ:
    tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(DIR / 'voz' / 'limpia.wav'), '-af', f'adelay={int(INICIO * 1000)},apad=whole_dur={DUR},loudnorm=I=-16:TP=-2:LRA=11', '-ar', '48000', '-ac', '1', str(tmp / 'voz.wav')], check=True)
    spec['audio'] = '.tmp/voz.wav'
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
if CON_VOZ: b.informe()
print(f"Short 013 · {'CON VOZ' if CON_VOZ else 'SIN VOZ'} · {len(ev)} capas · {len(CLIPS)} clips · {DUR:.1f} s")
