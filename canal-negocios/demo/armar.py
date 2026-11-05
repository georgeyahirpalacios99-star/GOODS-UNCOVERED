"""Demo de La Letra Chica: ¿Cómo gana dinero una tienda de todo a $1.25? (35 s, sin audio)."""
import json
from pathlib import Path
N = [  # narración: (desde, hasta, texto)
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
ev = [
    # escena 1: la tienda
    dict(tipo='muneco', desde=0.3, hasta=9.4, x=-120, y=900, tam=330, ropa='#4f8fc0', camisa='#fff', pelo='castano', dir=1,
         hacia=dict(desde=0.4, dur=1.6, x=620, y=900), caras=[[2.2, 'sorpresa'], [4.4, 'normal'], [6.2, 'feliz']], habla=[[3.7, 7.0]]),
    dict(tipo='titulo', desde=1.0, hasta=4.2, texto='¿CÓMO GANA DINERO\nUNA TIENDA DE *TODO A $1.25*?', y=470, tam=92),
    dict(tipo='producto', desde=4.4, hasta=9.4, cual='taza', x=960, y=668, tam=105, precio='$1.25', precioDesde=4.8, tamPrecio=.72),
    dict(tipo='producto', desde=4.7, hasta=9.4, cual='pato', x=1220, y=668, tam=100, precio='$1.25', precioDesde=5.1, tamPrecio=.72),
    dict(tipo='producto', desde=5.0, hasta=9.4, cual='pilas', x=1470, y=668, tam=100, precio='$1.25', precioDesde=5.4, tamPrecio=.72),
    dict(tipo='muneco', desde=5.6, hasta=9.4, x=1700, y=900, tam=300, ropa='#6dbb6a', delantal='#2e6b4c', pelo='negro', dir=-1, cara='feliz'),
    # escena 2: el tamaño
    dict(tipo='tiendas', desde=9.8, hasta=13.3, cols=10, filas=4, gx=165, gy=135, y=500, total=9200, prefijo='+', dur=2.6, sub='tiendas en EE. UU. y Canadá', yCifra=200, paso=.035, tam=1.15),
    dict(tipo='cifra', desde=13.4, hasta=16.9, texto='$19,400 M', sub='en ventas en 2025', fuente='Dollar Tree, informe anual 2025', y=500, tam=210, color='#7dd67a'),
    # escena 3: el desglose
    dict(tipo='producto', desde=17.3, hasta=27.5, cual='taza', x=330, y=760, tam=230, precio='$1.25', precioDesde=17.7, tamPrecio=1.5),
    dict(tipo='desglose', desde=19.6, hasta=27.5, x=700, y=420, w=1080, h=130, titulo='¿A DÓNDE VA TU $1.25?',
         partes=[dict(valor=80, cifra='≈ 80¢', texto='Comprar el producto y ponerlo en la tienda', color='#e8574a', desde=20.3),
                 dict(valor=45, cifra='≈ 45¢', texto='Le queda', color='#6dbb6a', desde=24.1)],
         fuente='margen bruto de 36.4 %, Dollar Tree, año fiscal 2025'),
    dict(tipo='muneco', desde=24.6, hasta=27.5, x=1740, y=990, tam=210, ropa='#2f3f6e', camisa='#fff', corbata='#d6453d', sombrero='copa', cara='feliz', dir=-1),
    # escena 4: miles de millones de veces
    dict(tipo='caja', desde=27.9, hasta=35, x=1200, y=835, tam=135, monto=[0, 7050, 28.3, 3.4], sufijo=' M', abre=[29.0, 30.4]),
    dict(tipo='cifra', desde=29.6, hasta=31.4, texto='$7,050 M', sub='ganancia bruta en 2025', fuente='Dollar Tree, informe anual 2025', x=1200, y=330, tam=92, color='#7dd67a'),
    dict(tipo='monedas', desde=28.2, hasta=35, x=1200, y=640, n=22, paso=.15, ancho=1100, r=32),
    dict(tipo='muneco', desde=27.9, hasta=35, x=560, y=900, tam=340, ropa='#2f3f6e', camisa='#fff', corbata='#d6453d', sombrero='copa', caras=[[27.9, 'sorpresa'], [29.2, 'feliz']]),
    dict(tipo='pregunta', desde=31.6, hasta=35, texto='¿QUÉ NEGOCIO EXPLICAMOS DESPUÉS?', y=250),
]
spec = dict(estilo='escena', fps=30, duracion=35.4, salida='demo-la-letra-chica', subY=1018, subTam=46,
            escenas=[dict(desde=0, fondo='tienda', letrero='TODO A $1.25', mostrador=[1300, 620], dur=9),
                     dict(desde=9.5, fondo='papel', color='#86bfae', dur=7.5),
                     dict(desde=17.0, fondo='papel', dur=10.5),
                     dict(desde=27.6, fondo='tienda', letrero='TODO A $1.25', estantes=[[40, 640, 3], [1320, 1880, 4]], dur=8)],
            narracion=[dict(desde=a, hasta=b, texto=x) for a, b, x in N], eventos=ev)
Path(__file__).with_name('mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print('ok')
