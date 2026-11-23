"""Video largo 007 · ¿Qué pasaría si desaparece Sinaloa? — estilo PRO (motor-mapa/ESTILO-PRO.md).
    python3 videos-largos/007-sinaloa-desaparece/construir.py
    node motor-mapa/render.cjs videos-largos/007-sinaloa-desaparece [--preview 5,60]
    python3 videos-largos/007-sinaloa-desaparece/sonido.py
"""
import json, shutil, subprocess, sys
from pathlib import Path
DIR = Path(__file__).resolve().parent; sys.path.insert(0, str(DIR))
from voz_alineada import preparar, palabras_de
BL, DUR = preparar(); B = {b.n: b for b in BL}
def T(cod, frase, k=1, d=0.0): return B['voz-' + cod].T(frase, k, d)
def INI(cod): return round(B['voz-' + cod].t0, 2)
def FIN(cod): return round(B['voz-' + cod].fin, 2)

CRED = {c['archivo']: f"Foto: {c['autor'].split('(')[0].strip()[:34]} · {c['licencia']}" for c in json.loads((DIR / 'fotos-reales' / 'creditos.json').read_text())}
CRED['mazatlan-vista-1.jpg'] = 'Foto: NASA · Dominio público'
R, IAF = 'fotos-reales/', 'clips/fotos-ia/'
IA = 'Imagen ilustrativa con IA'

cam, ev, CLIPS, ult = [], [], [], [None]
lugares = []
def lugar(t, txt): lugares.append(dict(t=round(t, 2), texto=txt))
def CAM(t, lon, lat, ancho, d=.8, corte=False, nombre=None):
    lugar(t, nombre or ('Norteamérica' if ancho >= 25 and lat > 27 else 'México' if ancho >= 20 else 'Noroeste de México' if ancho >= 13 else 'Mazatlán, Sinaloa' if abs(lon + 106.4) < 1 and abs(lat - 23.3) < 1 and ancho < 7 else 'Culiacán, Sinaloa' if ancho < 5 else 'Sinaloa, México'))
    if ult[0] and not corte: lo, la, an = ult[0]; cam.append(dict(t=round(t, 2), lon=lo, lat=la, ancho=an, suave=False))
    cam.append(dict(t=round(t + (0 if corte else d), 2), lon=lon, lat=lat, ancho=ancho)); ult[0] = (lon, lat, ancho)
def E(tipo, desde, hasta, **kw):
    e = dict(tipo=tipo, desde=round(desde, 2), hasta=round(hasta, 2), **kw); ev.append(e); return e
def clip(cod, a, b, **kw):  # clip de Flow a pantalla completa
    d = b - a; kw.setdefault('vel', round(min(1, 7.6 / max(.1, d)), 3)); kw.setdefault('etiqueta', 'IMAGEN ILUSTRATIVA CON IA'); CLIPS.append(dict(codigo=cod, desde=round(a, 2), hasta=round(b, 2), **kw))
def foto(img, a, b, z0=1.03, z1=1.12, ia=False, **kw):  # foto a pantalla completa con zoom lento
    f = (IAF if ia else R) + img; return E('foto', a, b, img=f, z0=z0, z1=z1, credito=IA if ia else CRED.get(img, ''), **kw)
def tarjeta(img, a, b, en=None, texto='', x=1400, y=420, w=500, ia=False, **kw):
    f = (IAF if ia else R) + img; return E('tarjetaFoto', a, b, img=f, en=en, x=x, y=y, w=w, texto=texto, credito=IA if ia else CRED.get(img, ''), **kw)
def tclip(cod, a, b, en=None, texto='', x=1400, y=420, w=520, **kw): return E('tarjetaClip', a, b, codigo=cod, en=en, x=x, y=y, w=w, texto=texto, **kw)
def barrido(t): E('barrido', t - .4, t + .4, dur=.8)
def ficha(a, b, kicker, texto, sub='', tam=60, **kw): return E('ficha', a, b, kicker=kicker, texto=texto, sub=sub, tam=tam, **kw)
def dato(a, b, kicker, num=None, texto=None, suf='', sub='', fuente='', **kw):
    e = E('dato', a, b, kicker=kicker, sub=sub, fuente=fuente, suf=suf, **kw)
    if num is not None: e['num'] = num
    else: e['texto'] = texto
    return e
def capitulo(n, texto, t): E('capitulo', t - .15, t + 2.1, n=n, texto=texto)

MZT, CUL, MOC, DGO, CHI = [-106.42, 23.22], [-107.39, 24.80], [-108.99, 25.79], [-104.66, 24.02], [-106.09, 28.63]
NOG, GDL, HOU, LA, CHG = [-110.94, 31.31], [-103.35, 20.67], [-95.37, 29.76], [-118.24, 34.05], [-87.63, 41.88]
OAX, GRO, CHS, TIJ, CDMX = [-96.72, 17.06], [-99.5, 17.55], [-93.1, 16.75], [-117.04, 32.51], [-99.13, 19.43]
ROS, GUA, BAL, BARR = [-105.86, 22.99], [-108.08, 25.46], [-105.78, 23.85], [-107.85, 27.45]
SIN = (-107.2, 24.6, 9); MEX = (-102.5, 23.8, 30); NOROESTE = (-106.5, 26.5, 15)

# ======================= GANCHO (voz-01a / 01b) =======================
t0 = INI('01a')
clip('S01', 0, T('01a', 'No hubo guerra'), z0=1.0, z1=1.08)
ficha(.4, T('01a', 'No hubo guerra') - .1, 'Goods Uncovered · México', '¿Y si Sinaloa desaparece?', 'Lo que el país perdería en 24 horas', tam=74)
CAM(0, *MEX, corte=True)
a = T('01a', 'No hubo guerra'); barrido(a)
E('fronteras', a, T('01b', 'Quédate') ); E('ambiente', 0, DUR);
E('resaltar', a, T('01a', 'aparece un hueco'), pais='MEX:SI', relleno='rgba(255,210,63,.14)')
E('simbolo', T('01a', 'No hubo guerra'), T('01a', 'No hubo terremoto'), forma='alerta', en=[-100.5, 26.5], texto='SIN GUERRA')
E('simbolo', T('01a', 'No hubo terremoto'), T('01a', 'Simplemente'), forma='olas', en=[-100.5, 26.5], texto='SIN TERREMOTO', ty=60)
CAM(T('01a', 'Simplemente', d=-.3), *SIN, d=1.4)
E('hueco', T('01a', 'aparece un hueco', d=-.6), FIN('01b'), pais='MEX:SI', t=T('01a', 'aparece un hueco'), dur=1.6)
E('rotulo2', T('01a', 'Tres millones'), T('01a', 'Y lo primero'), lon=-108.6, lat=25.9, dx=-150, dy=-110, texto='3,026,943 PERSONAS', sub='INEGI · CENSO 2020')
for i, (p, n, f) in enumerate([(CUL, 'CULIACÁN', 'Culiacán'), (MZT, 'MAZATLÁN', 'Mazatlán'), (MOC, 'LOS MOCHIS', 'Los Mochis')]):
    E('pinPro', T('01a', f), T('01a', 'Borrados') + .6, en=p, texto=n, color='#ff5a4a')
E('simbolo', T('01a', 'Es el precio'), T('01a', 'Esa misma mañana'), forma='precio', en={'x': 1500, 'y': 420}, tam=1.4, texto='EL PRECIO')
CAM(T('01a', 'Esa misma mañana', d=-.3), -104, 30, 34, d=1.2)
tclip('S02', T('01a', 'en un supermercado'), T('01a', 'En una tortillería'), en=HOU, texto='Supermercado en Texas', x=1420, y=360)
E('camino', T('01a', 'en un supermercado'), T('01a', 'En una tortillería'), puntos=[CUL, NOG, [-104, 31.5], HOU], vehiculo='camion', dur=2.6, color='#ff5a4a', tam=110)
tarjeta('S03.jpg', T('01a', 'En una tortillería'), T('01a', 'Y en un restaurante'), en=GDL, texto='Tortillería en Guadalajara', x=1400, y=560, ia=True, rot=2)
E('pinPro', T('01a', 'En una tortillería'), T('01a', 'Y en un restaurante'), en=GDL, texto='GUADALAJARA')
tarjeta('S04.jpg', T('01a', 'Y en un restaurante'), T('01a', 'Casi todo el mundo'), en=LA, texto='Restaurante en Los Ángeles', x=1380, y=420, ia=True, rot=-2)
E('pinPro', T('01a', 'Y en un restaurante'), T('01a', 'Casi todo el mundo'), en=LA, texto='LOS ÁNGELES')
a = T('01a', 'Casi todo el mundo'); clip('S05', a, T('01a', 'Pero hoy te voy'), z0=1.0, z1=1.1)
ficha(a + .3, T('01a', 'Pero hoy te voy') - .1, 'Lo que todos conocen', 'Las noticias', 'Pero Sinaloa es mucho más que eso')
a = T('01a', 'Pero hoy te voy'); barrido(a); CAM(a, *SIN, corte=True)
E('fila', T('01a', 'Pero hoy te voy') + .3, T('01a', 'Lo que está en tu mesa'), icono='tomate', en={'x': 1450, 'y': 520}, n=5, resalta=0, r=34, texto='LO QUE MÉXICO PERDERÍA DE VERDAD')
E('fila', T('01a', 'Lo que está en tu mesa'), T('01a', 'en tu música'), icono='maiz', en={'x': 1450, 'y': 520}, n=5, resalta=5, r=34, texto='TU MESA')
E('simbolo', T('01a', 'en tu música'), T('01a', 'y en tu alacena'), forma='notas', en=MZT, tam=1.3, texto='TU MÚSICA', ty=60)
E('fila', T('01a', 'y en tu alacena'), T('01a', 'Y al final'), icono='lata', en={'x': 1450, 'y': 520}, n=5, resalta=5, r=34, texto='TU ALACENA')
E('simbolo', T('01a', 'Y al final'), T('01a', 'Y no por lo que'), forma='reloj', en={'x': 1500, 'y': 420}, tam=1.4, texto='YA ESTÁ PASANDO', ty=80)
dato(T('01a', 'Y no por lo que'), T('01b', 'Así que hoy'), 'El dato del final', texto='?', sub='Y no es por lo que crees')
E('gente', T('01b', 'Así que hoy'), T('01b', 'Quédate'), modo='grupo', en={'x': 1450, 'y': 560}, n=6, columnas=6, tam=46, texto='EL EXPERIMENTO')
E('flechaPro', T('01b', 'pieza por pieza'), T('01b', 'Quédate'), de={'x': 1250, 'y': 300}, a=CUL, texto='PIEZA POR PIEZA', curva=.25)
ficha(T('01b', 'Quédate'), FIN('01b') + .3, 'No te lo pierdas', 'El capítulo 5 lo cambia todo', tam=58)

# ======================= CAPÍTULO 1 · EL HUECO (voz-02) =======================
a = INI('02a'); capitulo(1, 'El hueco', a); CAM(a, *NOROESTE, corte=True)
E('fronteras', a, FIN('02b')); E('resaltar', a + 2, T('02a', 'Ahora quitamos'), pais='MEX:SI', relleno='rgba(255,210,63,.12)')
dato(T('02a', 'Mide unos'), T('02a', 'Es más grande que'), 'Superficie', num=[0, 57365], suf='km²', sub='Una franja larga y delgada pegada al Pacífico', fuente='INEGI')
dato(T('02a', 'Es más grande que'), T('02a', 'Al norte'), 'Más grande que', texto='COSTA RICA', sub='Costa Rica: 51,100 km² · Sinaloa: 57,365 km²', tam=150)
for f, p, n, dx in [('Al norte', [-110.8, 29.3], 'SONORA', 120), ('Al este', [-106.2, 28.4], 'CHIHUAHUA', 120), ('y Durango', DGO, 'DURANGO', 130), ('Y al sur', [-104.9, 21.8], 'NAYARIT', 140)]:
    E('rotulo2', T('02a', f), T('02a', 'Ahora quitamos'), lon=p[0], lat=p[1], dx=dx, dy=-70, texto=n, tam=28)
E('tarjetaFoto', T('02a', 'detrás de una muralla'), T('02a', 'Y al sur'), img=R + 'barrancas-2.jpg', en=[-106.2, 26.0], x=1450, y=640, w=440, texto='Sierra Madre Occidental', credito=CRED['barrancas-2.jpg'])
a = T('02a', 'Ahora quitamos'); E('hueco', a - .3, FIN('02b'), pais='MEX:SI', t=a + .4, dur=1.4)
E('flechaPro', T('02a', 'Durango y Chihuahua pierden'), T('02a', 'La autopista'), de=DGO, a=MZT, texto='SIN SALIDA AL MAR', color='#ff5a4a', curva=-.25)
a = T('02a', 'La autopista'); barrido(a); foto('baluarte-1.jpg', a, T('02a', 'Esa autopista termina'), z0=1.02, z1=1.14)
ficha(a + .3, T('02a', 'Esa autopista termina') - .1, 'Frontera Durango–Sinaloa', 'Puente Baluarte', '402 m de altura · En 2012, el puente atirantado más alto del mundo (Guinness)')
a = T('02a', 'Esa autopista termina'); barrido(a); CAM(a, *NOROESTE, corte=True)
E('camino', a, T('02a', 'Y el famoso tren'), puntos=[DGO, BAL, MZT], vehiculo='camion', dur=2.2, color='#ffffff', tam=100)
E('circuloPro', a + 1, T('02a', 'Y el famoso tren'), en=MZT, r=36, texto='MAZATLÁN')
E('camino', T('02a', 'Y el famoso tren'), T('02a', 'Sin Sinaloa, el puente'), puntos=[CHI, [-107.6, 27.6], BARR, MOC], vehiculo='tren', dur=4.5, color='#ffd23f', tam=110, fin=True)
tarjeta('chepe-1.jpg', T('02a', 'el Chepe'), T('02a', 'termina en Los Mochis'), en=BARR, texto='El Chepe · Estación Creel', x=1450, y=380)
tarjeta('barrancas-2.jpg', T('02a', 'el que cruza las Barrancas'), T('02a', 'Sin Sinaloa, el puente'), en=BARR, texto='Barrancas del Cobre', x=1450, y=380, rot=2)
E('pinPro', T('02a', 'termina en Los Mochis'), T('02a', 'Y el tren al Pacífico'), en=MOC, texto='LOS MOCHIS')
E('simbolo', T('02a', 'Sin Sinaloa, el puente'), T('02a', 'Y el tren al Pacífico'), forma='alerta', en=BAL, texto='LLEVA A UN HUECO')
E('flechaPro', T('02a', 'Y el tren al Pacífico'), INI('02b'), de=CHI, a=[-109.6, 25.2], texto='¿AL PACÍFICO?', punteada=True, color='#ff5a4a')
E('simbolo', T('02b', 'Luego está el agua'), T('02b', 'Sinaloa los detuvo'), forma='gotas', en=[-106.6, 25.6], tam=1.6, texto='MÁS DE 10 RÍOS', ty=70)
dato(T('02b', 'Sinaloa los detuvo'), T('02b', 'Es uno de los sistemas'), 'Presas', num=[0, 11], sub='y una red de canales que riega más de 800,000 hectáreas', fuente='Gobierno de Sinaloa')
a = T('02b', 'Es uno de los sistemas'); clip('S10', a, T('02b', 'Sin Sinaloa, esa agua'))
ficha(a + .3, T('02b', 'Sin Sinaloa, esa agua') - .1, 'Uno de los más grandes de México', 'Distritos de riego', 'Más de 800,000 hectáreas regadas')
a = T('02b', 'Sin Sinaloa, esa agua'); barrido(a); CAM(a, *SIN, corte=True)
E('simbolo', a, T('02b', 'Y aquí empieza'), forma='gotas', en=[-107.3, 24.9], tam=1.5, texto='YA NO RIEGA NADA', ty=70)
E('fila', T('02b', 'Regaba la comida'), FIN('02b') + .5, icono='tomate', en={'x': 1450, 'y': 540}, n=5, resalta=5, r=34, texto='LA COMIDA DE MÉXICO')

# ======================= CAPÍTULO 2 · LA MESA (voz-03) =======================
a = INI('03a'); capitulo(2, 'La mesa', a); CAM(a, *SIN, corte=True)
E('fronteras', a, FIN('03b')); E('resaltar', a + 2, FIN('03b'), pais='MEX:SI', relleno='rgba(120,200,90,.16)', color='#9be36b')
ficha(T('03a', 'A Sinaloa le dicen'), T('03a', 'En su mejor temporada'), 'Su apodo', 'El granero de México', 'Y no es un apodo bonito: es una cifra')
E('gente', T('03a', 'En su mejor temporada'), T('03a', 'Y en dos mil veinticuatro'), modo='cosechar', en=[-107.8, 25.3], n=5, columnas=5, tam=34, texto='COSECHA')
dato(T('03a', 'En su mejor temporada'), T('03a', 'Maíz blanco'), 'Maíz · temporada 2022-23', num=[0, 6.48], dec=2, suf='millones de t', sub='La mejor temporada reciente de Sinaloa', fuente='Imagen Agropecuaria')
tarjeta('tortillas-1.jpg', T('03a', 'Maíz blanco'), T('03a', 'Y en dos mil veinticuatro'), en=CUL, texto='Maíz blanco: el de la tortilla')
E('fila', T('03a', 'Y en dos mil veinticuatro'), T('03a', 'Si Sinaloa desaparece'), icono='maiz', en={'x': 1420, 'y': 520}, n=7, resalta=1, r=30, texto='CASI 1 DE CADA 7 TONELADAS (2024)')
CAM(T('03a', 'Si Sinaloa desaparece', d=-.3), -100, 27, 30, d=1.2)
E('flechaPro', T('03a', 'tiene que buscar ese maíz afuera'), T('03a', 'La tortilla, que'), de=[-93, 37], a=CDMX, texto='MAÍZ DE AFUERA', curva=.2)
E('simbolo', T('03a', 'la tortilla sube adentro'), T('03a', 'Pero el maíz'), forma='precio', en={'x': 1600, 'y': 330}, tam=1.3, texto='LA TORTILLA SUBE')
tarjeta('S03.jpg', T('03a', 'La tortilla, que'), T('03a', 'Pero el maíz'), en=CDMX, texto='La base de cada comida', x=1380, y=640, ia=True)
a = T('03a', 'Garbanzo'); CAM(a - .3, *SIN, d=.8)
dato(a, INI('03b'), 'Garbanzo', num=[0, 62], suf='%', sub='de todo el garbanzo de México sale de un solo estado', fuente='SIAP / SADER vía CODESIN')
tarjeta('garbanzo-1.jpg', a + .4, INI('03b'), en=CUL, texto='Garbanzo', x=1450, y=480)
a = INI('03b'); clip('S16', a, T('03b', 'Uno de cada cinco'))
dato(a + .2, T('03b', 'Uno de cada cinco'), 'Tomate', num=[0, 800000], suf='t', sub='en una sola temporada', fuente='CAADES')
a = T('03b', 'Uno de cada cinco'); barrido(a); CAM(a, -104, 30, 30, corte=True)
E('fila', a, T('03b', 'Así que si Sinaloa'), icono='tomate', en={'x': 1420, 'y': 800}, n=5, resalta=1, r=36, texto='1 DE CADA 5 TOMATES DE MÉXICO')
E('camino', T('03b', 'una gran parte cruza'), T('03b', 'Y también se van'), puntos=[CUL, NOG, [-100, 37], CHG], vehiculo='camion', dur=4, color='#ff5a4a', tam=110)
tarjeta('tomate-2.jpg', T('03b', 'Se nota en la hamburguesa'), T('03b', 'Y también se van'), en=CHG, texto='Una ensalada en Chicago', x=1350, y=640)
a = T('03b', 'Y también se van'); CAM(a - .3, *SIN, d=.8)
for i, (n, p) in enumerate([('PAPA', MOC), ('CHILE', [-107.9, 25.4]), ('MANGO', [-106.2, 23.6]), ('FRIJOL', [-108.3, 25.9])]):
    E('pinPro', a + i * .45, T('03b', 'Detrás de todo'), en=p, texto=n, color='#9be36b')
a = T('03b', 'Detrás de todo'); CAM(a, -100, 21.5, 26, d=1)
E('gente', T('03b', 'Cada temporada'), FIN('03b'), modo='caminar', de=OAX, a=CUL, dur=6, n=7, tam=34, en=[-97, 15.6], texto='JORNALEROS DEL SUR')
for p in (OAX, GRO, CHS): E('flechaPro', T('03b', 'desde Oaxaca'), FIN('03b'), de=p, a=[-107, 24.6], curva=.15, punteada=True, grosor=4)
E('rotulo2', T('03b', 'Familias enteras'), FIN('03b') + .4, lon=-99, lat=20.5, dx=150, dy=-90, texto='~2,000 KM', sub='DE SU CASA')

# ======================= CAPÍTULO 3 · EL MAR (voz-04) =======================
a = INI('04a'); capitulo(3, 'El mar', a); CAM(a, -107.4, 23.6, 9, corte=True)
E('fronteras', a, FIN('04b')); E('simbolo', T('04a', 'Ahora mira la costa'), T('04a', 'En dos mil veintitrés'), forma='olas', en=[-108.4, 23.2], tam=1.4)
E('circuloPro', T('04a', 'Ahora mira la costa'), T('04a', 'En dos mil veintitrés'), en=[-107.2, 24.2], r=120, texto='LA COSTA DE SINALOA')
a = T('04a', 'En dos mil veintitrés'); clip('S22', a, T('04a', 'El camarón del aguachile'))
dato(a + .2, T('04a', 'El camarón del aguachile'), 'Camarón · 2023', num=[0, 115132], suf='t', sub='45 % del valor de todo el camarón de México', fuente='CONAPESCA')
a = T('04a', 'El camarón del aguachile'); barrido(a); foto('aguachile-1.jpg', a, T('04a', 'Y luego está Mazatlán'), z0=1.04, z1=1.14)
ficha(a + .3, T('04a', 'El de los tacos'), 'Hecho con camarón de Sinaloa', 'Aguachile')
ficha(T('04a', 'El de los tacos'), T('04a', 'Y luego está Mazatlán') - .1, 'También nacieron en Sinaloa', 'Tacos gobernador')
a = T('04a', 'Y luego está Mazatlán'); barrido(a); CAM(a, -106.5, 23.3, 4.5, corte=True)
E('circuloPro', a, T('04a', 'Sin Sinaloa, el atún'), en=MZT, r=40, texto='MAZATLÁN')
tarjeta('mazatlan-vista-1.jpg', a + .3, T('04a', 'Según datos'), en=MZT, texto='Mazatlán desde la Estación Espacial')
E('fila', T('04a', 'Según datos'), T('04a', 'Esa lata'), icono='lata', en={'x': 1420, 'y': 520}, n=10, resalta=7, r=26, texto='70 DE CADA 100 KILOS DE ATÚN (2015)')
tarjeta('faro-1.jpg', T('04a', 'Esa lata'), T('04a', 'Sin Sinaloa, el atún'), en=MZT, texto='Puerto de Mazatlán', rot=2)
E('simbolo', T('04a', 'Sin Sinaloa, el atún'), T('04a', 'y miles de pescadores'), forma='precio', en={'x': 1500, 'y': 360}, tam=1.3, texto='ATÚN Y CAMARÓN')
E('camino', T('04a', 'y miles de pescadores'), FIN('04a') + .3, puntos=[MZT, [-106.9, 22.7], [-107.8, 22.5]], vehiculo='barco', dur=3.5, color='#7fd6ff', tam=150, curva=.25)
a = INI('04b'); barrido(a); foto('S22b.jpg', a, T('04b', 'Con familias'), ia=True)
ficha(a + .3, T('04b', 'Con familias'), 'Cada año, al terminar la veda', 'La despedida de los barcos')
a = T('04b', 'Con familias'); foto('malecon-2.jpg', a, FIN('04b') + .3)
E('simbolo', T('04b', 'y con música de banda'), FIN('04b') + .3, forma='notas', en={'x': 960, 'y': 600}, tam=1.6)

# ======================= CAPÍTULO 4 · EL SONIDO DE MÉXICO (voz-05) =======================
a = INI('05a'); capitulo(4, 'El sonido de México', a); CAM(a, -106.8, 24.3, 6, corte=True)
E('fronteras', a, FIN('05b'))
E('pinPro', T('05a', 'en Mazatlán'), T('05a', 'Creció en Guamúchil'), en=MZT, texto='MAZATLÁN · 18-NOV-1917')
tarjeta('pedro-infante-1.jpg', T('05a', 'nació un niño'), T('05a', 'Creció en Guamúchil'), en=MZT, texto='Pedro Infante (archivo, 1948)', w=420, x=1450, y=440)
E('pinPro', T('05a', 'Creció en Guamúchil'), T('05a', 'Murió en mil'), en=GUA, texto='GUAMÚCHIL')
tarjeta('pedro-estatua-1.jpg', T('05a', 'y se convirtió'), T('05a', 'Murió en mil'), en=MZT, texto='Monumento a Pedro Infante, Mazatlán', rot=-2)
dato(T('05a', 'Murió en mil'), T('05a', 'Si Sinaloa desaparece'), 'Cada 15 de abril', texto='1957', sub='Miles de personas lo siguen recordando')
E('hueco', T('05a', 'Si Sinaloa desaparece'), T('05a', 'Y no está solo'), pais='MEX:SI', t=T('05a', 'Si Sinaloa desaparece') + .3, dur=1.2)
E('pinPro', T('05a', 'En El Rosario'), T('05a', 'Y en Guamúchil'), en=ROS, texto='EL ROSARIO')
tarjeta('lola-beltran-1.jpg', T('05a', 'nació Lola Beltrán'), T('05a', 'Y en Guamúchil'), en=ROS, texto='Museo Lola Beltrán, El Rosario')
E('pinPro', T('05a', 'Y en Guamúchil'), INI('05b') - .1, en=GUA, texto='GUAMÚCHIL')
tarjeta('ana-gabriel-1.jpg', T('05a', 'Y en Guamúchil'), T('05a', 'En mil novecientos treinta'), en=GUA, texto='Ana Gabriel', w=360, x=1480, y=420)
tarjeta('recodo-1.jpg', T('05a', 'En mil novecientos treinta'), T('05a', 'Fue la primera banda'), en=MZT, texto='Cruz Lizárraga · Banda El Recodo, 1938')
tarjeta('recodo-2.jpg', T('05a', 'Fue la primera banda'), INI('05b') - .1, en=MZT, texto='Banda El Recodo en concierto', rot=2)
E('simbolo', T('05a', 'En mil novecientos treinta'), INI('05b') - .1, forma='notas', en=MZT, tam=1.2)
a = INI('05b'); clip('S31', a, T('05b', 'La historia más contada'))
ficha(a + .3, T('05b', 'La historia más contada') - .1, 'Tambora, clarinetes y trompetas', 'La banda sinaloense')
a = T('05b', 'La historia más contada'); foto('tambora-2.jpg', a, T('05b', 'Sin Sinaloa no hay'), z0=1.02, z1=1.1)
ficha(a + .3, T('05b', 'Sin Sinaloa no hay') - .1, 'Siglo XIX', 'Las bandas de viento', 'Llegaron al puerto de Mazatlán')
a = T('05b', 'Sin Sinaloa no hay'); barrido(a); foto('tambora-3.jpg', a, T('05b', 'Desde Tijuana'))
a = T('05b', 'Desde Tijuana'); barrido(a); CAM(a, -110, 29, 22, corte=True)
for p in (TIJ, LA, [-112, 33.4], [-106.5, 31.7]): E('flechaPro', a + .2, T('05b', 'Y tampoco habría'), de=[-107.4, 24.8], a=p, curva=.15, grosor=4)
E('simbolo', a + .6, T('05b', 'Y tampoco habría'), forma='notas', en=LA, tam=1.2, texto='FIESTAS EN SILENCIO', ty=60)
a = T('05b', 'Y tampoco habría'); clip('S35', a, T('05b', 'Más de ciento veinte'))
dato(a + .3, T('05b', 'Más de ciento veinte'), 'Carnaval de Mazatlán', texto='1898', sub='La tradición de carnaval moderno más antigua de México', fuente='Carnaval Internacional de Mazatlán')
a = T('05b', 'Más de ciento veinte'); foto('carnaval-3.jpg', a, T('05b', 'Ahora, seguro'))
a = T('05b', 'Ahora, seguro'); barrido(a); CAM(a, *SIN, corte=True)
E('simbolo', a + .3, FIN('05b') + .5, forma='alerta', en=CUL, texto='¿Y LAS NOTICIAS?', ty=70)

# ======================= CAPÍTULO 5 · LA PARTE INCÓMODA (voz-06) =======================
a = INI('06a'); capitulo(5, 'La parte incómoda', a); CAM(a, -107.4, 24.8, 3.5, corte=True)
E('fronteras', a, FIN('06b'))
tarjeta('catedral-culiacan-3.jpg', T('06a', 'Y no es un invento'), T('06a', 'En los primeros'), en=CUL, texto='Culiacán', w=400)
ficha(T('06a', 'Desde el nueve'), T('06a', 'En los primeros'), 'Desde el 9 de septiembre de 2024', 'Guerra entre facciones', 'Culiacán, Sinaloa')
dato(T('06a', 'En los primeros'), T('06a', 'Escuelas que'), 'Primeros 12 meses', num=[0, 1632], suf='homicidios', sub='al menos, según la Fiscalía de Sinaloa', fuente='Fiscalía de Sinaloa vía La Opinión', tam=170)
E('gente', T('06a', 'Escuelas que'), T('06a', 'Entonces la pregunta'), modo='fila', en={'x': 1450, 'y': 520}, n=6, columnas=6, tam=44, resalta=0, color='rgba(255,255,255,.45)', texto='ESCUELAS · NEGOCIOS · FAMILIAS')
E('simbolo', T('06a', 'Negocios que'), T('06a', 'Entonces la pregunta'), forma='reloj', en={'x': 1450, 'y': 300}, tam=1.1, texto='DE NOCHE, NADIE SALE', ty=70)
a = T('06a', 'Entonces la pregunta'); CAM(a - .3, *SIN, d=1)
E('hueco', a, T('06a', 'El crimen organizado'), pais='MEX:SI', t=T('06a', 'si Sinaloa desaparece') + .3, dur=1.2)
dato(T('06a', 'No.'), T('06a', 'El crimen organizado'), 'La respuesta', texto='NO', sub='El problema no desaparece', tam=220)
a = T('06a', 'Es una red'); CAM(a - 2, -100, 26, 34, d=1.2)
for p in (CDMX, [-99.2, 29.5], [-117, 32.5], [-90, 21], HOU, [-75, 5]): E('flechaPro', a, T('06b', 'Los que sí'), de=CUL, a=p, curva=.12, punteada=True, grosor=3, color='#ff5a4a')
E('simbolo', T('06a', 'Si borras el mapa'), INI('06b'), forma='alerta', en=CUL, texto='LA RED SE MUEVE', ty=70)
a = INI('06b'); CAM(a, *SIN, corte=True)
E('gente', a, T('06b', 'Los agricultores'), modo='grupo', en={'x': 1430, 'y': 470}, n=18, columnas=6, tam=40, paso=.06, texto='3 MILLONES DE PERSONAS')
E('gente', T('06b', 'Los agricultores'), T('06b', 'Esa es la verdad'), modo='fila', en={'x': 1430, 'y': 520}, n=5, columnas=5, tam=50, resalta=5)
for i, n in enumerate(['AGRICULTORES', 'PESCADORES', 'MAESTROS', 'MÉDICOS', 'MÚSICOS']):
    E('rotulo2', T('06b', ['Los agricultores', 'Los pescadores', 'Los maestros', 'Los médicos', 'Los músicos'][i]), T('06b', 'Esa es la verdad'), lon=-109.4, lat=27.2 - i * .75, dx=-60, dy=0, largo=60, texto=n, tam=24)
ficha(T('06b', 'Esa es la verdad'), T('06b', 'Pero ahora viene'), 'La verdad que casi nunca se dice', 'La primera víctima', 'Sinaloa sufre aquello por lo que la conocen')
E('simbolo', T('06b', 'Pero ahora viene'), FIN('06b') + .5, forma='reloj', en={'x': 1450, 'y': 400}, tam=1.4, texto='YA ESTÁ PASANDO', ty=80)

# ======================= CAPÍTULO 6 · YA ESTÁ PASANDO (voz-07a) =======================
a = INI('07a'); capitulo(6, 'Ya está desapareciendo', a); CAM(a, *SIN, corte=True)
a = T('07a', 'La sequía'); clip('S41', a, T('07a', 'En dos mil veinticinco'))
ficha(a + .3, T('07a', 'Y sin agua') , 'Sequía', 'Presas en niveles muy bajos')
ficha(T('07a', 'Y sin agua'), T('07a', 'En dos mil veinticinco') - .1, 'Sequía', 'Sin agua no hay siembra')
a = T('07a', 'En dos mil veinticinco'); barrido(a); CAM(a, *SIN, corte=True); E('fronteras', a, FIN('07a'))
E('simbolo', a, T('07a', 'El granero'), forma='sol', en={'x': 1560, 'y': 260}, tam=1.2)
dato(a, T('07a', 'El granero'), 'Maíz de Sinaloa · 2025', num=[0, 75], pre='-', suf='%', sub='menos que su máximo histórico: 1.5 a 1.6 millones de t', fuente='Imagen Agropecuaria')
a = T('07a', 'El granero'); foto('S41b.jpg', a, T('07a', 'Y no es solo'), ia=True)
ficha(a + .2, T('07a', 'Y no es solo') - .1, 'El granero de México', 'Medio vacío')
a = T('07a', 'Y no es solo'); barrido(a); CAM(a, -103, 28, 26, corte=True)
E('flechaPro', T('07a', 'En julio'), T('07a', 'Súmale'), de=[-97, 36], a=[-106, 26], texto='ARANCEL 17 %', color='#ff5a4a', curva=-.2)
dato(T('07a', 'En julio'), T('07a', 'Súmale'), 'Desde julio de 2025', texto='17 %', sub='de arancel de EE. UU. al tomate mexicano', fuente='Departamento de Comercio de EE. UU.')
E('simbolo', T('07a', 'Súmale'), T('07a', 'para la temporada'), forma='sol', en={'x': 1500, 'y': 300}, tam=1.0, texto='SEQUÍA', ty=90)
E('simbolo', T('07a', 'y la inseguridad'), T('07a', 'para la temporada'), forma='alerta', en={'x': 1700, 'y': 520}, texto='INSEGURIDAD')
dato(T('07a', 'para la temporada'), T('07a', 'Menos campo'), 'Tomate · temporada 2025-26', num=[0, 30], pre='-', suf='%', sub='de superficie: unas 8,000 hectáreas', fuente='CAADES')
a = T('07a', 'Menos campo'); foto('S16b.jpg', a, T('07a', 'No es un hueco'), ia=True)
for f, n in [('Menos campo', 'Menos campo'), ('Menos trabajo', 'Menos trabajo'), ('Menos comida', 'Menos comida')]:
    ficha(T('07a', f), (T('07a', {'Menos campo': 'Menos trabajo', 'Menos trabajo': 'Menos comida', 'Menos comida': 'No es un hueco'}[f])) - .05, 'Sinaloa hoy', n)
a = T('07a', 'No es un hueco'); barrido(a); CAM(a, -107.2, 24.6, 12, corte=True); CAM(a + .5, -107.2, 24.6, 8, d=5)
E('fronteras', a, FIN('07a') + .4); E('hueco', a, FIN('07a') + .4, pais='MEX:SI', t=T('07a', 'Es un hueco que se abre'), dur=4.5)

# ======================= CIERRE (voz-07b) =======================
a = INI('07b'); CAM(a, *SIN, corte=True); E('fronteras', a, T('07b', 'Sinaloa es lo que'))
E('hueco', a, T('07b', 'Sinaloa es lo que'), pais='MEX:SI', t=a + .2, dur=.6)
for f, img, txt, rot in [('su tortilla', 'tortillas-1.jpg', 'Tortilla', -3), ('Casi la mitad de su camarón', 'aguachile-1.jpg', 'Camarón', 2), ('Más de la mitad de su garbanzo', 'garbanzo-1.jpg', 'Garbanzo', -2), ('Su carnaval', 'carnaval-2.jpg', 'Carnaval de Mazatlán', 3), ('Y la tierra de Pedro', 'pedro-estatua-1.jpg', 'Pedro Infante', -2)]:
    tarjeta(img, T('07b', f), T('07b', 'Y el problema'), texto=txt, x=520 + 220 * ['su tortilla', 'Casi la mitad de su camarón', 'Más de la mitad de su garbanzo', 'Su carnaval', 'Y la tierra de Pedro'].index(f), y=440, w=380, rot=rot)
E('simbolo', T('07b', 'Y el problema'), T('07b', 'Sinaloa no es lo que'), forma='alerta', en=CUL, texto='SEGUIRÍA AHÍ', ty=70)
ficha(T('07b', 'Sinaloa no es lo que'), T('07b', 'Sinaloa es lo que'), '', 'No es lo que sale en las noticias', tam=58)
a = T('07b', 'Sinaloa es lo que'); clip('S45', a, T('07b', 'Ahora dime'))
ficha(a + .3, T('07b', 'Ahora dime') - .1, 'Sinaloa', 'Es lo que está en tu mesa', tam=70)
a = T('07b', 'Ahora dime'); foto('S46.jpg', a, DUR, ia=True, z0=1.0, z1=1.12)
E('pregunta', T('07b', '¿qué extrañarías'), T('07b', 'Si quieres que'), texto='¿QUÉ EXTRAÑARÍAS PRIMERO? 👇', y=300)
for i, n in enumerate(['AGUACHILE', 'BANDA', 'CARNAVAL']):
    ficha(T('07b', '¿El aguachile') + i * .55, T('07b', 'Y si eres de Sinaloa'), '', n, tam=50, x=150 + i * 560, y=520)
ficha(T('07b', 'Si quieres que'), DUR, 'Suscríbete', '¿Qué estado sigue?', 'Escríbelo en los comentarios', tam=70)

# ======================= HUD y ensamblado =======================
E('hud', 0, DUR, lugares=sorted(lugares, key=lambda q: q['t']))
fichas = sorted([e for e in ev if e['tipo'] in ('ficha',) and 'x' not in e], key=lambda e: e['desde'])
for e1, e2 in zip(fichas, fichas[1:]):
    if e1['hasta'] > e2['desde'] - .05: e1['hasta'] = round(e2['desde'] - .05, 2)
datos_ = sorted([e for e in ev if e['tipo'] == 'dato'], key=lambda e: e['desde'])
for e1, e2 in zip(datos_, datos_[1:]):
    if e1['hasta'] > e2['desde'] - .05: e1['hasta'] = round(e2['desde'] - .05, 2)
# los acompañantes del mapa duran hasta que entra el siguiente (nunca queda el mapa solo)
ACOMP = ('simbolo', 'fila', 'gente', 'tarjetaFoto', 'tarjetaClip', 'dato')
acs = sorted([e for e in ev if e['tipo'] in ACOMP], key=lambda e: e['desde'])
for e1, e2 in zip(acs, acs[1:]):
    if e1['hasta'] < e2['desde'] - .05: e1['hasta'] = round(max(e1['hasta'], min(e2['desde'] - .05, e1['hasta'] + 3)), 2)
# cuadros de los clips (pantalla completa y recuadros) a 30 fps
for cod in sorted({c['codigo'] for c in CLIPS} | {e['codigo'] for e in ev if e['tipo'] == 'tarjetaClip'}):
    dst = DIR / '.clips' / cod
    if not dst.exists():
        dst.mkdir(parents=True); subprocess.run(['ffmpeg', '-v', 'error', '-i', str(DIR / 'clips' / f'{cod}.mp4'), '-vf', 'fps=30', '-q:v', '3', str(dst / '%04d.jpg')], check=True)
cam.sort(key=lambda k: (k['t'], k.get('suave') is not False))
for i in range(1, len(cam)):
    if cam[i]['t'] <= cam[i - 1]['t']: cam[i]['t'] = round(cam[i - 1]['t'] + .02, 2)
pal = [w for b in BL for w in palabras_de(b)]
spec = dict(estilo='documental', estadosDe=['MEX'], salida='que-pasaria-si-desaparece-sinaloa', duracion=DUR, camara=cam, eventos=sorted(ev, key=lambda e: e['desde']), clips=sorted(CLIPS, key=lambda c: c['desde']),
            palabras=pal, resaltar=['SINALOA', 'MÉXICO', 'MAÍZ', 'TORTILLA', 'TOMATE', 'GARBANZO', 'CAMARÓN', 'MAZATLÁN', 'CULIACÁN', 'PEDRO', 'INFANTE', 'BANDA', 'CARNAVAL', 'HUECO', 'SEQUÍA', 'NO', 'MILLONES'],
            capY=1000, capTam=46, capEstilo='caja', tipografia='cine', capColor='#ffd23f', capTextoClave='#0b0f14', fundido_inicio=0, barra=True, audio='.tmp/voz.wav')
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'Video 007 · {len(ev)} capas · {len(CLIPS)} clips · {DUR:.1f} s · {len(pal)} palabras')
