"""Demo animado de La Letra Chica: fondos de Flow (img/01..08) + palitos animados por código.
    python3 canal-negocios/demo-animado/armar.py && node motor-mapa/render.cjs canal-negocios/demo-animado
"""
import json
from pathlib import Path
D = Path(__file__).resolve().parent
K, OX = 1080 / 768, (1920 - 1376 * 1080 / 768) / 2          # imagen 1376x768 cubriendo 1920x1080
P = lambda x, y: [round(x * K + OX, 1), round(y * K, 1)]
poly = lambda *pts: [P(x, y) for x, y in pts]
N = [
    (0.5, 3.6, 'Todo en esta tienda cuesta un dólar con veinticinco.'),
    (3.7, 7.0, 'Entonces, ¿cómo gana millones vendiendo cosas tan baratas?'),
    (7.1, 9.3, 'Empecemos por el tamaño.'),
    (9.6, 13.0, 'Dollar Tree tiene más de 9,200 tiendas en Estados Unidos y Canadá.'),
    (13.1, 16.8, 'Y en 2025 vendió 19,400 millones de dólares.'),
    (17.1, 20.0, 'Pero el truco está en cuánto paga por cada cosa.'),
    (20.1, 24.0, 'De cada dólar con veinticinco, unos 80 centavos se van en comprar el producto y ponerlo en la tienda.'),
    (24.1, 27.4, 'Le quedan unos 45 centavos para sueldos, gastos… y ganancia.'),
    (27.7, 31.4, 'Parece poco. Pero en un año, eso sumó más de 7,000 millones de dólares.'),
    (31.5, 35.0, '¿Qué negocio quieres que expliquemos después?'),
]
BETO = dict(ropa='#4f8fc0', pantalon='#5d6470', pelo='#231a14', id=1)
JEFE = dict(ropa='#2c3e6b', pantalon='#2c3e6b', cuello=True, corbata='#c8323a', sombrero='copa', id=2)
esc = [
    dict(desde=0, dur=3.7, img='img/01.jpg'),
    dict(desde=3.7, dur=3.4, img='img/02.jpg', frente=[poly((668, 330), (1000, 372), (1000, 222), (1264, 222), (1264, 405), (1376, 412), (1376, 768), (690, 768), (690, 548), (668, 525))]),
    dict(desde=7.1, dur=6.0, img='img/03.jpg'),
    dict(desde=13.1, dur=4.0, img='img/04.jpg'),
    dict(desde=17.1, dur=3.0, img='img/05.jpg', frente=[poly((95, 348), (1285, 348), (1285, 425), (95, 425))]),
    dict(desde=20.1, dur=4.0, img='img/06.jpg'),
    dict(desde=24.1, dur=3.6, img='img/07.jpg', frente=[poly((443, 428), (980, 428), (980, 692), (443, 692)), poly((583, 330), (652, 330), (652, 430), (583, 430)),
                                                       poly((758, 358), (802, 358), (802, 430), (758, 430)), poly((803, 350), (920, 350), (920, 432), (803, 432))]),
    dict(desde=27.7, dur=3.8, img='img/08.jpg'),
    dict(desde=31.5, dur=4.0, img='img/01.jpg'),
]
for e in esc: e.update(margen=1, zoom=.05)
pines = [P(x, y) for x, y in [(175, 75), (330, 70), (450, 95), (590, 60), (760, 80), (930, 55), (1100, 75), (1260, 60), (120, 200), (285, 190), (520, 200), (880, 190),
                              (1040, 205), (1210, 190), (330, 300), (640, 300), (850, 330), (1000, 310), (1180, 300), (150, 380), (470, 380), (760, 400), (1120, 420), (1290, 380),
                              (240, 520), (430, 500), (620, 470), (960, 500), (1150, 520), (300, 640), (560, 650), (830, 620), (1100, 640), (1280, 600)]]
ev = [
    # 1 · la tienda
    dict(tipo='palito', desde=0, hasta=3.75, **BETO, x=-150, y=1000, tam=560, lleva='taza',
         claves=[dict(t=0, x=-150), dict(t=1.7, x=700, pose='parado', dir=0), dict(t=2.1, pose='señalarArriba', dir=0)], caras=[[1.8, 'sorpresa']]),
    dict(tipo='titulo', desde=0.9, hasta=3.6, texto='¿CÓMO GANA DINERO\nUNA TIENDA DE *TODO A $1.25*?', y=372, tam=70),
    # 2 · la caja
    dict(tipo='palito', desde=3.7, hasta=7.15, capa='detras', ropa='#efe6d2', delantal='#3f7d4e', pelo='#6b4527', id=3, x=P(840, 0)[0], y=P(0, 560)[1], tam=560, dir=-1,
         claves=[dict(t=3.7, pose='saludar'), dict(t=5.0, pose='parado')], cara='feliz'),
    dict(tipo='palito', desde=3.7, hasta=7.15, **BETO, x=P(300, 0)[0], y=P(0, 718)[1], tam=640, lleva='taza', dir=1,
         claves=[dict(t=3.7, pose='parado'), dict(t=4.3, pose='rascar', lleva='nada')], caras=[[3.7, 'confundido']]),
    dict(tipo='signos', desde=4.5, hasta=7.1, quien=1, texto='???'),
    # 3 · miles de tiendas
    dict(tipo='pines', desde=9.4, hasta=13.1, puntos=pines, paso=.065, tam=1.05),
    dict(tipo='tiendas', desde=9.5, hasta=13.0, filas=0, total=9200, prefijo='+', dur=2.4, sub='tiendas en EE. UU. y Canadá', yCifra=500),
    # 4 · la montaña de dinero
    dict(tipo='montana', desde=13.2, hasta=17.15, x=960, y=975, w=820, h=420, dur=2.2),
    dict(tipo='palito', desde=15.0, hasta=17.15, **JEFE, x=960, y=565, tam=330, dir=0, claves=[dict(t=15.0, pose='celebrar')], cara='risa'),
    dict(tipo='cifra', desde=13.4, hasta=16.9, texto='$19,400 M', sub='en ventas en 2025', fuente='Dollar Tree, informe anual 2025', x=430, y=300, tam=118, color='#7dd67a'),
    # 5 · la fábrica
    dict(tipo='cinta', desde=17.1, hasta=20.15, x0=P(105, 0)[0], x1=P(1275, 0)[0], y=P(0, 368)[1], n=11, vel=230, tam=56),
    dict(tipo='palito', desde=17.1, hasta=20.15, capa='detras', ropa='#6a8fb3', sombrero='gorra', id=4, x=P(400, 0)[0], y=P(0, 520)[1], tam=430, dir=1, claves=[dict(t=17.1, pose='contar')], cara='normal'),
    dict(tipo='palito', desde=17.1, hasta=20.15, capa='detras', ropa='#6a8fb3', sombrero='gorra', id=5, fase=.4, x=P(960, 0)[0], y=P(0, 520)[1], tam=430, dir=-1, claves=[dict(t=17.1, pose='contar')], cara='feliz'),
    dict(tipo='palito', desde=17.1, hasta=20.15, **JEFE, x=-120, y=1050, tam=560, claves=[dict(t=17.1, x=-120), dict(t=18.2, x=300, pose='señalar', dir=1)], cara='feliz'),
    # 6 · el puerto
    dict(tipo='camion', desde=20.1, hasta=24.15, x0=-500, x1=2400, y=P(0, 690)[1], dur=4.0, tam=150, lineal=True),
    dict(tipo='palito', desde=20.1, hasta=24.15, ropa='#e8873a', pantalon='#4a4f57', sombrero='casco', id=6, x=1650, y=1000, tam=470, dir=-1, claves=[dict(t=20.1, pose='saludar')], cara='feliz'),
    dict(tipo='desglose', global_=True, desde=20.2, hasta=27.6, x=420, y=110, w=1080, h=120, titulo='',
         partes=[dict(valor=80, cifra='≈ 80¢', texto='Comprar el producto y ponerlo en la tienda', color='#e8574a', desde=20.4),
                 dict(valor=45, cifra='≈ 45¢', texto='Le queda', color='#6dbb6a', desde=24.3)],
         fuente='margen bruto de 36.4 %, Dollar Tree, año fiscal 2025'),
    # 7 · la oficina
    dict(tipo='palito', desde=24.1, hasta=27.75, capa='detras', **JEFE, x=P(700, 0)[0], y=P(0, 640)[1], tam=560, dir=0, claves=[dict(t=24.1, pose='contar')], caras=[[24.1, 'preocupado'], [26.2, 'normal']]),
    dict(tipo='pila', desde=24.3, hasta=27.75, x=P(700, 0)[0], y=P(0, 452)[1], r=19, de=1, a=9, dur=2.6),
    # 8 · lluvia de monedas
    dict(tipo='palito', desde=27.7, hasta=31.55, **JEFE, x=2100, y=P(0, 655)[1], tam=520, claves=[dict(t=27.7, x=2100), dict(t=29.0, x=960, pose='risa', dir=0)], cara='feliz', caras=[[29.0, 'risa']]),
    dict(tipo='monedas', capa='detras', desde=28.5, hasta=31.55, x=960, y=930, n=30, paso=.09, ancho=1900, r=30, vuelo=1.1),
    dict(tipo='cifra', desde=29.2, hasta=31.4, texto='$7,050 M', sub='ganancia bruta en 2025', fuente='Dollar Tree, informe anual 2025', y=200, tam=130, color='#7dd67a'),
    # 9 · pregunta final
    dict(tipo='palito', desde=31.5, hasta=35.4, **BETO, x=960, y=1070, tam=700, dir=0, claves=[dict(t=31.5, pose='parado'), dict(t=32.0, pose='saludar')], cara='feliz'),
    dict(tipo='pregunta', desde=31.9, hasta=35.4, texto='¿QUÉ NEGOCIO EXPLICAMOS DESPUÉS?', y=120),
]
spec = dict(estilo='escena', fps=30, duracion=35.4, salida='demo-animado', subY=1018, subTam=46, escenas=esc,
            narracion=[dict(desde=a, hasta=b, texto=x) for a, b, x in N], eventos=ev)
INI = [e['desde'] for e in esc]
for e in ev:
    if e.pop('global_', False): e['global'] = True
    if any(abs(e.get('hasta', 0) - (i + .05)) < .06 for i in INI): e['hasta'] = round(e['hasta'] + .55, 2)
(D / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print('ok')
