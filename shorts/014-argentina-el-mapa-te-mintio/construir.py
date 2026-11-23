"""Short 014 · México quiere quitarle los barcos al Canal de Panamá con un tren — mapa satelital con países rayados, lista de claves, barras y clips de Flow.
    python3 shorts/014-argentina-el-mapa-te-mintio/construir.py
    node motor-mapa/render.cjs shorts/014-argentina-el-mapa-te-mintio
    python3 shorts/014-argentina-el-mapa-te-mintio/sonido.py
"""
import json, re, subprocess, sys
from pathlib import Path
DIR = Path(__file__).resolve().parent; sys.path.insert(0, str(DIR.parent / '007-brasil-shorts'))
from alinear import Bloque, BloqueEstimado, limpiar, palabras_de
TEXTO = re.search(r'```\n(.*?)```', (DIR / 'GUION-CAPCUT.md').read_text(encoding='utf-8'), re.S).group(1)
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
NOM, CIF, CINTA = 345, 360, 1185
AM, ROJO, BLANCO = '#ffd23f', '#ff4a4a', '#ffffff'
MUNDO = (-48, 12, 118)            # Groenlandia y Argentina en la misma pantalla
ARGV = (-64, -38, 34)             # Argentina entera
GRL0, ARG0 = (-41, 72), (-65, -37)
def rango(n, a, b): E('rango', a, n=n, hasta=b)
def polaroid(img, a, b, texto, x=820, y=880, rot=6, w=300): E('polaroid', a, img=f'obj/{img}.jpg', x=x, y=y, w=w, rot=rot, texto=texto, hasta=b)

# ---------- 1 · gancho: la mano encierra Groenlandia en el mapa ----------
clip('A01', 0, T('Pero el mapa', d=-.05), maxdur=7.6, entra=.01, z0=1.0, z1=1.12)
E('titulo', .1, texto='GROENLANDIA\n¿*8 VECES* ARGENTINA?', tam=86, y=NOM, capa='C', hasta=T('Pero el mapa', d=-.1))
CAM(0, *MUNDO, d=0)
E('capa', T('Pero el mapa', d=-.1), img='obj/nubes.jpg', alpha=.22, vx=14, hasta=DUR)
E('resaltar', T('Pero el mapa'), pais='GRL', color=BLANCO, rayas=True, relleno='rgba(255,255,255,.12)', hasta=T('Argentina...', d=.2))
E('resaltar', T('Pero el mapa', d=.25), pais='ARG', color=AM, rayas=True, relleno='rgba(255,210,63,.14)', hasta=T('Número cinco'))
E('titulo', T('Pero el mapa'), texto='EL MAPA TE *MINTIÓ*', tam=110, y=NOM, capa='C', hasta=T('Argentina...', d=-.1))
# ---------- 2 · la prueba: Groenlandia baja hasta Argentina y se encoge ----------
E('silueta', T('Argentina...', d=-.05), pais='GRL', desdeLon=GRL0[0], desdeLat=GRL0[1], lon=ARG0[0] + 1, lat=ARG0[1] + 3, lat0=72, espera=.15, viaje=2.6, color=BLANCO, relleno='rgba(255,255,255,.35)', hasta=T('Número cinco', d=-.1))
E('titulo', T('es más grande', d=-.1), texto='ARGENTINA ES *MÁS GRANDE*', tam=92, y=NOM, capa='C', hasta=T('Y eso no es', d=-.1))
E('titulo', T('Y eso no es'), texto='5 COSAS QUE\n*CABEN EN ARGENTINA*', tam=84, y=NOM, capa='C', hasta=T('Número cinco', d=-.1))
# ---------- #5 Italia en una provincia ----------
clip('A03', T('Número cinco', d=-.05), T('Una sola provincia', d=.4), maxdur=7.6)
rango(5, T('Número cinco'), T('Número cuatro', d=-.1))
CAM(T('Una sola provincia', d=.2), -63.5, -35, 26, d=.7)
E('resaltar', T('Una sola provincia', d=.3), pais='ARG', color=AM, rayas=True, relleno='rgba(255,210,63,.08)', hasta=T('Número cuatro', d=-.1))
E('silueta', T('Buenos Aires', d=-.1), pais='ITA', lon=-60.2, lat=-36.6, lat0=42, texto='ITALIA · 302,073 km²', tam=30, dy=-200, color=AM, hasta=T('Número cuatro', d=-.1))
E('titulo', T('Buenos Aires', d=.2), texto='UNA PROVINCIA *> ITALIA*', tam=88, y=NOM, capa='C', hasta=T('Número cuatro', d=-.1))
polaroid('P01', T('toda Italia', d=-.4), T('Número cuatro', d=-.1), 'ITALIA', x=830, y=1000)
# ---------- #4 de norte a sur > Madrid–Moscú ----------
clip('A04', T('Número cuatro', d=-.05), T('De norte a sur', d=.3), maxdur=7.6)
rango(4, T('Número cuatro'), T('Número tres', d=-.1))
CAM(T('De norte a sur', d=.1), *ARGV, d=.7)
E('muralla', T('Argentina mide', d=-.2), puntos=[[-65.6, -22.1], [-66.2, -30], [-67.5, -40], [-68.3, -54.8]], dur=1.4, grosor=12, color=AM, hasta=T('Número tres', d=-.1))
E('cifra', T('Argentina mide', d=.4), texto='3,643 km', num=[0, 3643], suf=' km', dur=1.0, tam=170, sub='de La Quiaca a Ushuaia', y=CIF, color=AM, hasta=T('Número tres', d=-.1))
polaroid('P02', T('de Madrid', d=-.2), T('Número tres', d=-.1), 'MADRID → MOSCÚ: 3,440 km', x=800, y=1010, rot=-5)
# ---------- #3 cinco países de Europa ----------
rango(3, T('Número tres'), T('Número dos', d=-.1))
E('barras', T('Juntos', d=-.1), titulo='SUPERFICIE (km²)', y=1080, ancho=300, alto=440, dec=2, suf=' M', items=[dict(valor=1.96, texto='5 PAÍSES', color='#4ea3ff', desde=round(T('Juntos', d=-.1), 2)), dict(valor=2.78, texto='ARGENTINA', color=AM, desde=round(T('Caben todos'), 2))], hasta=T('Número dos', d=-.1))
E('titulo', T('Número tres', d=.1), texto='ESPAÑA · FRANCIA · ALEMANIA\nITALIA · REINO UNIDO', tam=58, y=NOM, capa='C', hasta=T('y todavía sobra', d=-.1))
E('titulo', T('y todavía sobra', d=-.1), texto='Y *SOBRA ESPACIO*', tam=100, y=NOM, capa='C', hasta=T('Número dos', d=-.1))
# ---------- #2 México + Chile ----------
rango(2, T('Número dos'), T('Y número uno', d=-.1))
CAM(T('Número dos', d=-.1), -78, -12, 72, d=.8)
E('silueta', T('México entero', d=-.2), pais='MEX', desdeLon=-102, desdeLat=23.5, lon=-63.5, lat=-30, lat0=23.5, espera=.1, viaje=1.6, color='#3ddc7a', relleno='rgba(61,220,122,.35)', hasta=T('Y número uno', d=-.1))
E('resaltar', T('Número dos', d=.1), pais='ARG', color=AM, rayas=True, relleno='rgba(255,210,63,.08)', hasta=T('Y número uno', d=-.1))
polaroid('P03', T('México entero', d=.2), T('entra todo Chile', d=-.2), 'MÉXICO', x=820, y=980, rot=6)
polaroid('P04', T('entra todo Chile', d=.2), T('Y número uno', d=-.1), 'CHILE', x=820, y=1000, rot=-6)
E('cifra', T('entra todo Chile', d=.3), texto='2.72 < 2.78', tam=140, sub='millones de km²', y=CIF, color=AM, hasta=T('Y número uno', d=-.1))
# ---------- #1 Groenlandia ----------
clip('A02', T('Y número uno', d=-.05), T('cabe dentro', d=-.1), maxdur=7.6)
rango(1, T('Y número uno'), T('¿Por qué', d=-.1))
E('titulo', T('Y número uno', d=.2), texto='*GROENLANDIA*', tam=120, y=NOM, capa='C', hasta=T('cabe dentro', d=-.1))
CAM(T('cabe dentro', d=-.15), *MUNDO, d=0)
E('silueta', T('cabe dentro', d=-.1), pais='GRL', desdeLon=GRL0[0], desdeLat=GRL0[1], lon=ARG0[0] + 1, lat=ARG0[1] + 3, lat0=72, espera=0, viaje=1.4, color=BLANCO, relleno='rgba(255,255,255,.35)', hasta=T('¿Por qué', d=-.1))
E('resaltar', T('cabe dentro', d=-.1), pais='ARG', color=AM, rayas=True, relleno='rgba(255,210,63,.14)', hasta=T('¿Por qué', d=-.1))
polaroid('P05', T('otra Francia', d=-.3), T('¿Por qué', d=-.1), 'Y SOBRA… ¡OTRA FRANCIA!', x=780, y=1040, rot=5, w=340)
# ---------- por qué + cierre ----------
clip('A05', T('¿Por qué', d=-.05), T('¿Tu país', d=-.05), maxdur=7.6)
E('titulo', T('Porque estira', d=-.1), texto='EL MAPA ESTIRA\n*LOS POLOS*', tam=96, y=NOM, capa='C', hasta=T('¿Tu país', d=-.1))
CAM(T('¿Tu país', d=-.15), *MUNDO, d=0)
E('resaltar', T('¿Tu país'), pais='ARG', color=AM, rayas=True, relleno='rgba(255,210,63,.14)', hasta=DUR)
E('pregunta', T('¿Tu país'), texto='¿TU PAÍS TAMBIÉN? COMENTA 👇', y=CINTA, hasta=DUR)
sacud.append(dict(t=round(T('Argentina...') + 2.7, 2), dur=.5, fuerza=12))
# títulos que no se pisan: cada uno termina justo antes de que empiece el siguiente
tits = sorted([e for e in ev if e['tipo'] == 'titulo'], key=lambda e: e['desde'])
for e1, e2 in zip(tits, tits[1:]):
    if e1.get('hasta', 1e9) > e2['desde'] - .05: e1['hasta'] = round(e2['desde'] - .05, 2)
DESTELLOS = [round(T('Argentina...') + 2.7, 2), round(T('cabe dentro') + 1.4, 2)]
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
spec = dict(estilo='documental', formato='vertical', salida='argentina-el-mapa-te-mintio', duracion=DUR, camara=cam, sacudidas=sacud, eventos=sorted(ev, key=lambda e: e['desde']),
            clips=CLIPS, palabras=palabras_de(b), resaltar=['GROENLANDIA', 'ARGENTINA', 'MINTIÓ', 'ITALIA', 'EUROPA', 'MOSCÚ', 'MÉXICO', 'CHILE', 'FRANCIA', 'POLOS', 'OCHO', 'CINCO', 'CUATRO', 'TRES', 'DOS', 'UNO', 'ESPACIO', 'PAÍS'],
            capY=1500, capTam=74, capEstilo='caja', tipografia='cine', tituloClave='texto', capColor='#ffd23f', capTextoClave='#0b0f14', fundido_inicio=0, barra=True, destellos=DESTELLOS)
if CON_VOZ:
    tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(DIR / 'voz' / 'limpia.wav'), '-af', f'adelay={int(INICIO * 1000)},apad=whole_dur={DUR},loudnorm=I=-16:TP=-2:LRA=11', '-ar', '48000', '-ac', '1', str(tmp / 'voz.wav')], check=True)
    spec['audio'] = '.tmp/voz.wav'
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
if CON_VOZ: b.informe()
print(f"Short 014 · {'CON VOZ' if CON_VOZ else 'SIN VOZ'} · {len(ev)} capas · {len(CLIPS)} clips · {DUR:.1f} s")
