"""Short 010 · ¿Por qué China rodeó un desierto entero con árboles? — mapa satelital realista + clips e imágenes de Flow + subtítulo por palabra.
    python3 shorts/010-muralla-verde-china/construir.py        (con voz/*.mp3 si existe; si no, tiempos estimados)
    node motor-mapa/render.cjs shorts/010-muralla-verde-china
    python3 shorts/010-muralla-verde-china/sonido.py
Toque del canal, "del satélite al suelo": los clips cenitales (T01, T02, T06, T09) entran con un zoom fuerte, como si el mapa siguiera bajando.
"""
import json, math, re, shutil, subprocess, sys
from pathlib import Path
DIR = Path(__file__).resolve().parent; sys.path.insert(0, str(DIR.parent / '007-brasil-shorts'))
from alinear import Bloque, BloqueEstimado, limpiar, palabras_de
TEXTO = re.search(r'```\n(.*?)```', (DIR / 'GUION-ELEVENLABS.md').read_text(encoding='utf-8'), re.S).group(1)
INICIO = .15
mp3 = sorted((DIR / 'voz').glob('*.mp3'))
if mp3: limpiar(mp3[0], DIR / 'voz' / 'limpia.wav'); b = Bloque(1, TEXTO, INICIO, DIR / 'voz' / 'limpia.wav'); CON_VOZ = True
else: b = BloqueEstimado(1, TEXTO, INICIO); CON_VOZ = False
T = b.T; DUR = round(b.fin + 1.4, 2)
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
ETI = 'IMAGEN ILUSTRATIVA CON IA'
def clip(cod, a0, a1, maxdur=7.6, **ex):
    """Clip de video de Flow: si la escena dura más que el clip, se reproduce más lento."""
    d = a1 - a0; ex.setdefault('vel', round(min(1, (maxdur - ex.get('ofs', 0)) / max(.1, d)), 3)); CLIPS.append(dict(codigo=cod, desde=round(a0, 2), hasta=round(a1, 2), etiqueta=ETI, **ex))
FOTOS = {}
def foto(cod, a0, a1, mov, img=None, **ex):
    """Imagen fija animada aquí: mov = (zoom inicial, zoom final, foco x/y inicial, foco x/y final), con el foco en fracción de la imagen."""
    FOTOS[cod] = dict(img=img or cod, mov=mov, n=int(math.ceil((a1 - a0) * 30)) + 3); CLIPS.append(dict(codigo=cod, desde=round(a0, 2), hasta=round(a1, 2), etiqueta=ETI, vel=1, z0=1, z1=1, **ex))

# ---------- geografía ----------
def anillo_taklamakan():
    """Contorno real del Taklamakán (Natural Earth), un poco hacia afuera y suavizado. Empieza en el sur para que el último tramo en cerrarse sea el del sur (Yutian)."""
    geo = json.loads((DIR.parents[1] / 'motor-mapa' / 'datos' / 'ne_10m_geography_regions_polys.geojson').read_text(encoding='utf-8'))
    g = next(f for f in geo['features'] if f['properties']['NAME'] == 'TAKLIMAKAN DESERT')['geometry']
    ring = max((p[0] for p in (g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']])), key=len)[:-1]
    cx, cy = sum(p[0] for p in ring) / len(ring), sum(p[1] for p in ring) / len(ring)
    ring = [[cx + (x - cx) * 1.05, cy + (y - cy) * 1.08] for x, y in ring]
    i0 = min(range(len(ring)), key=lambda i: abs(ring[i][0] - 81.4) + (0 if ring[i][1] < cy else 99)); ring = ring[i0:] + ring[:i0]
    if ring[1][0] > ring[0][0]: ring = [ring[0]] + ring[:0:-1]                     # que arranque hacia el oeste
    for _ in range(2): ring = [q for a, c in zip(ring, ring[1:] + ring[:1]) for q in ([.75 * a[0] + .25 * c[0], .75 * a[1] + .25 * c[1]], [.25 * a[0] + .75 * c[0], .25 * a[1] + .75 * c[1]])]
    return [[round(x, 3), round(y, 3)] for x, y in ring + ring[:1]]
ANILLO = anillo_taklamakan()
NORTE = [[76, 39.8], [81, 43.8], [87, 44.6], [93, 42.8], [99, 40.2], [104, 38.6], [108, 39.6], [112, 41.2], [116, 42.4], [120, 43.8], [124, 45.6], [127, 47.5]]   # franja de los "Tres Nortes" (trazado esquemático)
TAK, PEK, YUT, GOBI = (83.2, 39.0), (116.4, 39.9), (81.7, 36.6), (104, 42.5)
TIT, CIF, CINTA = 300, 330, 1185

# ---------- 1 · gancho ----------
clip('T01', 0, T('Mira el mapa', d=-.05), entra=.01, z0=1.0, z1=1.08)
E('titulo', .1, texto='CHINA RODEÓ\nUN *DESIERTO*', tam=100, y=TIT, capa='C', hasta=T('con una muralla', d=-.15))
E('titulo', T('con una muralla', d=-.1), texto='¿CON UNA MURALLA\nDE *ÁRBOLES*?', tam=92, y=TIT, hasta=T('Mira el mapa', d=-.1), capa='C')
CAM(0, 100, 36, 62, d=0)
# ---------- 2 · el desierto ----------
E('resaltar', T('Mira el mapa'), pais='CHN', color='#ffd23f', relleno='rgba(255,210,63,.10)', hasta=T('un mar de arena'))
CAM(T('Aquí está', d=-.1), TAK[0], TAK[1] - .6, 21, d=.9)
E('pin', T('Aquí está', d=.5), lon=TAK[0], lat=TAK[1] + .4, texto='TAKLAMAKÁN', escala=1.6, hasta=T('más grande que'))
E('cifra', T('un mar de arena'), texto='337,600 km²', num=[0, 337600], suf=' km²', dur=1.0, tam=150, sub='de arena', y=CIF, hasta=T('Su nombre'))
E('silueta', T('más grande que', d=.1), pais='ECU', lon=TAK[0], lat=TAK[1], lat0=-1.4, texto='ECUADOR · 283,561 km²', tam=40, dy=250, hasta=T('Su nombre'))
clip('T02', T('Su nombre', d=-.1), T('Y sus dunas', d=-.05))
E('titulo', T('entras', d=-.1), texto='"ENTRAS…\nY *NO SALES*"', tam=100, y=TIT, hasta=T('Y sus dunas', d=-.1), capa='C')
clip('T03', T('Y sus dunas', d=-.1), T('Al este', d=-.05), maxdur=4.4)
# ---------- 3 · el polvo llega a Pekín ----------
CAM(T('Al este', d=-.1), 108, 40.5, 30, d=.5)
E('pin', T('Al este', d=.15), lon=GOBI[0], lat=GOBI[1], texto='DESIERTO DE GOBI', escala=1.4, color='#e8a13a', hasta=T('en dos mil veintiuno'))
E('flujo', T('el polvo del Gobi'), de=list(GOBI), a=list(PEK), n=6, hasta=T('en dos mil veintiuno'))
E('pin', T('llega hasta', d=.2), lon=PEK[0], lat=PEK[1], texto='PEKÍN', escala=1.6, color='#e8463a', hasta=T('en dos mil veintiuno'))
clip('T04', T('en dos mil veintiuno', d=-.1), T('doscientas veces', d=.35), vel=1.6)
E('fecha', T('en dos mil veintiuno'), texto='PEKÍN · MARZO DE 2021', hasta=T('En mil novecientos'))
clip('T05', T('doscientas veces', d=.35), T('En mil novecientos', d=-.05), maxdur=5.5)
E('cifra', T('doscientas veces'), texto='×200', num=[0, 200], pre='×', dur=.9, tam=220, sub='el límite de polvo de la OMS', y=CIF, color='#ff8a3a', hasta=T('En mil novecientos'))
# ---------- 4 · el plan ----------
CAM(T('En mil novecientos', d=-.1), 101, 41, 58, d=.6)
E('fecha', T('En mil novecientos'), texto='AÑO 1978', hasta=T('Alrededor del desierto'))
E('titulo', T('un plan que'), texto='UN PLAN\n*"IMPOSIBLE"*', tam=100, y=TIT, hasta=T('una muralla verde', d=-.1), capa='C')
E('muralla', T('una muralla verde'), puntos=NORTE, dur=2.0, grosor=20, hasta=T('Alrededor del desierto'))
E('cifra', T('cuatro mil quinientos'), texto='4,500 km', num=[0, 4500], suf=' km', dur=1.0, tam=170, sub='de muralla verde (plan hasta 2050)', y=CIF, color='#7dffa0', hasta=T('Se calcula'))
E('cifra', T('Se calcula', d=.2), texto='66,000 MILLONES', num=[0, 66000], suf=' MILLONES', dur=1.6, tam=118, sub='de árboles plantados (estimado)', y=CIF, color='#7dffa0', hasta=T('Alrededor del desierto'))
# ---------- 5 · cómo lo hicieron ----------
foto('T06', T('Alrededor del desierto', d=-.1), T('con cuadrículas', d=.1), (1.0, 1.55, (.5, .5), (.5, .56)))
foto('T07', T('con cuadrículas', d=.1), T('y regaron', d=-.05), (1.22, 1.0, (.42, .45), (.5, .5)))
E('cinta', T('con cuadrículas', d=.2), x=960, y=CINTA, escala=1.25, texto='CUADRÍCULAS DE PAJA', icono='', color='#b9862f', hasta=T('y regaron', d=-.1))
foto('T08', T('y regaron', d=-.05), T('A finales', d=-.05), (1.0, 1.3, (.5, .35), (.5, .72)))
E('cinta', T('y regaron', d=.2), x=960, y=CINTA, escala=1.2, texto='RIEGO CON ENERGÍA SOLAR', icono='', color='#1f6aa8', hasta=T('A finales', d=-.1))
# ---------- 6 · cierran el anillo ----------
CAM(T('A finales', d=-.1), TAK[0], TAK[1] - .9, 19, d=.6)
E('muralla', T('A finales'), puntos=ANILLO, dur=2.0, hastaP=.906, fantasma=True, hasta=T('cerraron el anillo'))
E('cifra', T('A finales', d=.2), texto='2,761 km', num=[0, 2761], suf=' km', dur=1.6, tam=170, sub='a finales de 2023', y=CIF, color='#7dffa0', hasta=T('Y el veintiocho'))
E('pin', T('solo faltaba', d=.2), lon=YUT[0] + .6, lat=YUT[1] + .15, texto='FALTAN 285 km', escala=1.5, color='#e8463a', hasta=T('Y el veintiocho'))
foto('T09', T('Y el veintiocho', d=-.05), T('cerraron el anillo', d=-.1), (1.0, 1.5, (.5, .4), (.52, .5)))
E('fecha', T('Y el veintiocho'), texto='28 DE NOVIEMBRE DE 2024', hasta=T('Según China'))
CAM(T('cerraron el anillo', d=-.1), TAK[0], TAK[1] - .9, 17.5, d=1.6)
E('muralla', T('cerraron el anillo'), puntos=ANILLO, dur=.8, desdeP=.906, cerrada=True, hasta=T('Según China'))
E('cifra', T('tres mil cuarenta', d=-.1), texto='3,046 km', num=[2761, 3046], suf=' km', dur=.8, tam=180, sub='el anillo verde, completo', y=CIF, color='#7dffa0', hasta=T('Según China'))
# ---------- 7 · resultado ----------
foto('T10', T('Según China', d=-.1), T('Pero hay un problema', d=-.05), (1.18, 1.0, (.4, .6), (.5, .5)))
E('cifra', T('bajaron de', d=-.2), texto='179', num=[179, 128], dur=1.6, tam=220, sub='días de tormenta de arena al año', y=CIF, fuente='datos oficiales de China', hasta=T('Pero hay un problema', d=-.1))
# ---------- 8 · el giro ----------
foto('T11', T('Pero hay un problema', d=-.05), T('En el año dos mil', d=-.05), (1.0, 1.3, (.5, .45), (.5, .6)))
E('titulo', T('Pero hay un problema'), texto='PERO HAY\nUN *PROBLEMA*', tam=104, y=TIT, hasta=T('Un investigador', d=.6), capa='C')
E('arboles', T('de cada cien', d=-.3), y=585, celda=68, vivos=15, muere=T('solo quince', d=-.9), durMuere=1.5, hasta=T('En el año dos mil', d=-.1))
E('cifra', T('solo quince', d=-.1), texto='15 DE 100', tam=150, sub='sobrevivieron en zonas secas (estimación)', y=CIF, color='#ff6a5a', hasta=T('En el año dos mil', d=-.1))
foto('T11b', T('En el año dos mil', d=-.05), T('Y cada árbol', d=-.05), (1.5, 1.15, (.3, .75), (.6, .55)), img='T11')
E('fecha', T('En el año dos mil'), texto='AÑO 2000', hasta=T('Y cada árbol'))
E('cifra', T('mil millones de álamos', d=-.2), texto='1,000 MILLONES', num=[0, 1000], suf=' MILLONES', dur=.9, tam=120, sub='de álamos muertos por una sola plaga', y=CIF, color='#ff6a5a', hasta=T('Y cada árbol', d=-.1))
foto('T12', T('Y cada árbol', d=-.05), T('¿Es la muralla', d=-.05), (1.0, 1.4, (.5, .5), (.62, .52)))
# ---------- 9 · cierre: del suelo al satélite ----------
foto('T13', T('¿Es la muralla', d=-.05), T('o un oasis', d=-.1), (1.45, 1.0, (.5, .55), (.5, .5)))
CAM(T('o un oasis', d=-.2), TAK[0], TAK[1] - .9, 16, d=0); CAM(T('o un oasis', d=-.1), TAK[0], TAK[1] - 1.5, 27, d=3.2)
E('muralla', T('o un oasis', d=-.15), puntos=ANILLO, dur=.01, hasta=DUR)
E('pregunta', T('o un oasis'), texto='¿FRENA AL DESIERTO… O SE SECA?', y=CINTA, hasta=DUR)

# deriva lenta entre movimientos de cámara: el mapa nunca queda quieto
base = sorted(cam, key=lambda k: k['t']); extra = []
for k1, k2 in zip(base, base[1:]):
    if k1.get('suave') is False or k2.get('suave') is not False: continue
    if k2['t'] - k1['t'] > 1.2: extra.append(dict(t=round(k2['t'] - .05, 2), lon=k1['lon'], lat=k1['lat'], ancho=round(k1['ancho'] * .9, 3)))
cam += extra
for f, fu in [('cerraron el anillo', 12), ('Pero hay un problema', 10)]: sacud.append(dict(t=round(T(f) + (.8 if 'anillo' in f else 0), 2), dur=.5, fuerza=fu))
DESTELLOS = [round(T('cerraron el anillo') + .8, 2), round(T('Pero hay un problema'), 2)]

# ---------- cuadros de los clips y de las imágenes ----------
for c in CLIPS:
    cod, dst = c['codigo'], DIR / '.clips' / c['codigo']
    if cod in FOTOS:
        f = FOTOS[cod]; (z0, z1, (x0, y0), (x1, y1)), n = f['mov'], f['n']; shutil.rmtree(dst, ignore_errors=True); dst.mkdir(parents=True)
        u = f"(1-pow(1-on/{n - 1}\\,2))"                                              # avanza rápido y frena: se siente como la cámara que llega
        z = f"({z0}+({z1 - z0})*{u})"; fx = f"({x0}+({x1 - x0})*{u})"; fy = f"({y0}+({y1 - y0})*{u})"
        vf = f"scale=3240:5760:force_original_aspect_ratio=increase:flags=lanczos,crop=3240:5760,zoompan=z='{z}':x='{fx}*iw-iw/zoom/2':y='{fy}*ih-ih/zoom/2':d={n}:s=1080x1920:fps=30"
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(DIR / 'imagenes' / f"{f['img']}.jpg"), '-vf', vf, '-frames:v', str(n), '-q:v', '3', str(dst / '%04d.jpg')], check=True)
    elif not dst.exists():
        dst.mkdir(parents=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(DIR / 'clips' / f"{cod}.mp4"), '-vf', 'scale=1080:1920:flags=lanczos,fps=30', '-q:v', '3', str(dst / '%04d.jpg')], check=True)
cam.sort(key=lambda k: (k['t'], k.get('suave') is not False))
for i in range(1, len(cam)):
    if cam[i]['t'] <= cam[i - 1]['t']: cam[i]['t'] = round(cam[i - 1]['t'] + .02, 2)
spec = dict(estilo='documental', formato='vertical', salida='muralla-verde-china', duracion=DUR, camara=cam, sacudidas=sacud, eventos=sorted(ev, key=lambda e: e['desde']),
            clips=CLIPS, palabras=palabras_de(b), resaltar=['CHINA', 'DESIERTO', 'ÁRBOLES', 'TAKLAMAKÁN', 'ECUADOR', 'GOBI', 'PEKÍN', 'OMS', 'MURALLA', 'ANILLO', 'PROBLEMA', 'QUINCE', 'PLAGA', 'AGUA', 'SECAR', 'SALES'],
            capY=1420, capTam=104, fundido_inicio=0, barra=True, destellos=DESTELLOS)
if CON_VOZ:
    tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(DIR / 'voz' / 'limpia.wav'), '-af', f'adelay={int(INICIO * 1000)},apad=whole_dur={DUR},loudnorm=I=-16:TP=-2:LRA=11', '-ar', '48000', '-ac', '1', str(tmp / 'voz.wav')], check=True)
    spec['audio'] = '.tmp/voz.wav'
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
if CON_VOZ: b.informe()
print(f"Short 010 · {'CON VOZ' if CON_VOZ else 'SIN VOZ (tiempos estimados)'} · {len(ev)} capas · {len(CLIPS)} clips · {DUR:.1f} s")
for c in CLIPS: print(f"   {c['codigo']:5s} {c['desde']:6.2f} → {c['hasta']:6.2f}  ({c['hasta'] - c['desde']:.1f} s)")
