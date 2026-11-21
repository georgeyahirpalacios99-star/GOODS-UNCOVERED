"""Demo de La Letra Chica con estilo visual cine (siluetas con contraluz, neón, primeros planos) y la voz de ElevenLabs."""
import json
from pathlib import Path
D = Path(__file__).resolve().parent
CLI = dict(id=1, ropa='#c23b4a', ropa2='#8f2533')
JEFE = dict(id=2, ropa='#2a3350', ropa2='#1c2238', corbata='#c8323a', sombrero='copa')
tomas = [dict(tipo='calle', desde=0, z0=1, z1=1.07, foco=[960, 620], hora=.04),
         dict(tipo='cara', desde=2.75, z0=1, z1=1.06, foco=[960, 420]),
         dict(tipo='ciudad', desde=6.55, z0=1.0, z1=1.12, foco=[960, 600], n=80, paso=.06, flash=True),
         dict(tipo='rayos', desde=12.5, z0=1.12, z1=1, flash=True),
         dict(tipo='producto', desde=17.15, z0=1, z1=1.1, foco=[960, 650]),
         dict(tipo='producto', desde=20.1, cx=1300, z0=1.08, z1=1, foco=[1300, 650]),
         dict(tipo='cara', desde=26.45, z0=1.05, z1=1, foco=[1450, 600], c0='#1b1830', c1='#3b2a4a', bok='150,170,255'),
         dict(tipo='dia', desde=30.3, z0=1, z1=1.05, foco=[960, 600], horaDe=.6, horaA=.98, flash=True),
         dict(tipo='cara', desde=35.0, z0=1, z1=1.05, foco=[960, 520], c0='#2a1630', c1='#5b2340', bok='255,110,150')]
ev = [
    dict(tipo='persona', toma=0, desde=0, hasta=2.75, **CLI, x=260, y=905, tam=430, claves=[dict(t=0, x=260), dict(t=2.4, x=760, dir=1)], cara='feliz'),
    dict(tipo='pregunta', toma=0, desde=0.5, hasta=2.7, texto='¿CÓMO GANA DINERO UNA TIENDA DE TODO A $1.25?', y=110),
    dict(tipo='persona', toma=1, desde=2.75, hasta=6.55, **CLI, x=960, y=580, tam=1450, busto=True, signos=3.7, claves=[dict(t=2.75)], cara='serio'),
    dict(tipo='cifra', toma=2, pantalla=True, encima=True, desde=8.7, hasta=12.5, a=9200, prefijo='+', dur=2.4, sub='tiendas en EE. UU. y Canadá', y=190, tam=140, color='#ff9db5'),
    dict(tipo='cifra', toma=3, pantalla=True, encima=True, desde=13.5, hasta=17.15, a=19400, prefijo='$', sufijo=' M', dur=1.4, sub='en ventas en 2025', fuente='Dollar Tree, informe anual 2025', y=470, tam=180, color='#7dea8f'),
    dict(tipo='precio', toma=4, desde=17.7, hasta=20.1, x=1200, y=520, tam=1.5),
    dict(tipo='precio', toma=5, desde=20.1, hasta=26.45, x=1540, y=520, tam=1.4),
    dict(tipo='barra', toma=5, pantalla=True, encima=True, desde=20.3, hasta=26.45, x=110, y=120, w=820,
         partes=[dict(valor=80, cifra='≈ 80¢', texto='producto y llevarlo a la tienda', color='#e8574a', desde=22.3), dict(valor=45, cifra='≈ 45¢', texto='le queda', color='#3fbf6a', desde=99)],
         fuente='margen bruto 36.4 %, Dollar Tree, año fiscal 2025'),
    dict(tipo='persona', toma=6, desde=26.45, hasta=30.3, **JEFE, x=1450, y=640, tam=1100, busto=True, claves=[dict(t=26.45)], cara='serio', caras=[[27.4, 'pillo']], rim='#9fb4ff'),
    dict(tipo='barra', toma=6, pantalla=True, encima=True, desde=26.45, hasta=30.3, x=110, y=120, w=820,
         partes=[dict(valor=80, cifra='≈ 80¢', texto='producto y llevarlo a la tienda', color='#e8574a', desde=25.0), dict(valor=45, cifra='≈ 45¢', texto='le queda', color='#3fbf6a', desde=26.9)],
         fuente='margen bruto 36.4 %, Dollar Tree, año fiscal 2025'),
    dict(tipo='multitud', toma=7, desde=30.3, hasta=35.0, n=22, paso=.21, dur=1.5),
    dict(tipo='pops', toma=7, pantalla=True, encima=True, desde=30.5, hasta=35.0, tiempos=[round(30.6 + i * .2, 2) for i in range(20)], x=1660, y=300),
    dict(tipo='cifra', toma=7, pantalla=True, encima=True, desde=32.5, hasta=35.0, a=7050, prefijo='$', sufijo=' M', dur=1.2, sub='ganancia bruta en 2025', fuente='Dollar Tree, informe anual 2025', y=420, tam=150, color='#7dea8f'),
    dict(tipo='persona', toma=8, desde=35.0, hasta=39.0, **CLI, x=960, y=640, tam=1250, busto=True, manos='arriba', claves=[dict(t=35.0)], cara='feliz', rim='#ff9db5'),
    dict(tipo='pregunta', toma=8, pantalla=True, encima=True, desde=35.3, hasta=39.0, texto='¿QUÉ NEGOCIO EXPLICAMOS DESPUÉS?', y=150),
]
N = [(0.0, 2.09, 'Todo en esta tienda cuesta un dólar con veinticinco.'), (3.01, 5.98, 'Entonces… ¿cómo gana millones vendiendo cosas tan baratas?'),
     (6.82, 8.05, 'Empecemos por el tamaño.'), (8.81, 12.04, 'Dollar Tree tiene más de 9,200 tiendas en Estados Unidos y Canadá.'),
     (12.75, 16.57, 'Y en 2025 vendió 19,400 millones de dólares.'), (17.45, 19.77, 'Pero el truco está en cuánto paga por cada cosa.'),
     (20.38, 21.80, 'De cada dólar con veinticinco,'), (22.29, 26.08, 'unos 80 centavos se van en comprar el producto y ponerlo en la tienda.'),
     (26.71, 29.76, 'Le quedan unos 45 centavos para sueldos, gastos… y ganancia.'), (30.61, 31.18, 'Parece poco.'),
     (31.86, 34.40, 'Pero en un año, eso sumó más de 7,000 millones de dólares.'), (35.33, 36.82, '¿Qué negocio quieres que expliquemos después?'),
     (37.46, 38.60, 'Déjalo en los comentarios.')]
spec = dict(motor='cine', estilo='cine', fps=30, duracion=38.95, salida='demo-cine', audio='voz-norm.wav', tomas=tomas, eventos=ev, narracion=[dict(desde=a, hasta=b, texto=x) for a, b, x in N])
(D / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8'); print('ok')
