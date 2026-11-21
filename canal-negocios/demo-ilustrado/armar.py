"""Demo ilustrado de La Letra Chica: las 9 imágenes de PROMPTS-DEMO.md animadas con zoom, cifras y subtítulos.

    python3 canal-negocios/demo-ilustrado/armar.py            # arma mapa.json con img/01..09 (png, jpg o webp)
    node motor-mapa/render.cjs canal-negocios/demo-ilustrado   # renderiza
"""
import json, sys
from pathlib import Path
D = Path(__file__).resolve().parent
sys.path.insert(0, str(D.parent / 'demo'))
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
# (imagen, desde, duración, dirección del paneo)
ESC = [('01', 0, 3.7, (1, 0)), ('02', 3.7, 3.4, (-1, 0)), ('03', 7.1, 6.0, (0, 1)), ('04', 13.1, 4.0, (0, -1)),
       ('05', 17.1, 3.0, (1, 0)), ('06', 20.1, 4.0, (-1, 0)), ('07', 24.1, 3.6, (0, 1)), ('08', 27.7, 3.8, (1, -1)), ('09', 31.5, 4.0, (0, 0))]
def img(n):
    for ext in ('png', 'jpg', 'jpeg', 'webp'):
        if (D / 'img' / f'{n}.{ext}').exists(): return f'img/{n}.{ext}'
    print('falta la imagen', n); return None
escenas = [dict(desde=a, dur=d, img=img(n), pan=list(p), zoom=.07, fondo='papel') for n, a, d, p in ESC]
ev = [
    dict(tipo='titulo', desde=0.9, hasta=3.6, texto='¿CÓMO GANA DINERO\nUNA TIENDA DE *TODO A $1.25*?', y=820, tam=86),
    dict(tipo='tiendas', desde=9.6, hasta=13.0, filas=0, total=9200, prefijo='+', dur=2.4, sub='tiendas en EE. UU. y Canadá', yCifra=190),
    dict(tipo='cifra', desde=13.3, hasta=16.9, texto='$19,400 M', sub='en ventas en 2025', fuente='Dollar Tree, informe anual 2025', y=230, tam=170, color='#7dd67a'),
    dict(tipo='desglose', desde=20.2, hasta=27.5, x=420, y=130, w=1080, h=120, titulo='',
         partes=[dict(valor=80, cifra='≈ 80¢', texto='Comprar el producto y ponerlo en la tienda', color='#e8574a', desde=20.4),
                 dict(valor=45, cifra='≈ 45¢', texto='Le queda', color='#6dbb6a', desde=24.2)],
         fuente='margen bruto de 36.4 %, Dollar Tree, año fiscal 2025'),
    dict(tipo='cifra', desde=28.6, hasta=31.4, texto='$7,050 M', sub='ganancia bruta en 2025', fuente='Dollar Tree, informe anual 2025', y=210, tam=150, color='#7dd67a'),
    dict(tipo='pregunta', desde=31.9, hasta=35.4, texto='¿QUÉ NEGOCIO EXPLICAMOS DESPUÉS?', y=150),
]
spec = dict(estilo='escena', fps=30, duracion=35.4, salida='demo-ilustrado', subY=1010, subTam=48, escenas=escenas,
            narracion=[dict(desde=a, hasta=b, texto=x) for a, b, x in N], eventos=ev)
(D / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print('ok')
