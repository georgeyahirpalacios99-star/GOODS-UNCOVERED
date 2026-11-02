"""Prueba del estilo cine (20 s): 'Eres dueño de una tienda de todo a $1.25 por un día'."""
import json
from pathlib import Path
D = Path(__file__).resolve().parent
TU = dict(id=1, ropa='#c23b4a', ropa2='#8f2533')
tomas = [dict(tipo='calle', desde=0, z0=1, z1=1.08, foco=[960, 620], hora=.04),
         dict(tipo='cara', desde=4.2, z0=1, z1=1.06, foco=[960, 420]),
         dict(tipo='rayos', desde=7.0, z0=1.15, z1=1, flash=True),
         dict(tipo='dia', desde=8.6, z0=1, z1=1.05, foco=[960, 600], horaDe=.04, horaA=.97, flash=True),
         dict(tipo='foco', desde=16.0, z0=1.02, z1=1.12, foco=[960, 380])]
pops = [round(9.0 + i * .24, 2) for i in range(28)]
ev = [
    dict(tipo='persona', toma=0, desde=0, hasta=4.2, **TU, x=250, y=905, tam=430, claves=[dict(t=0.2, x=250), dict(t=3.2, x=820, pose='parado', dir=1)], caras=[[0, 'feliz']]),
    dict(tipo='persona', toma=1, desde=4.2, hasta=7.0, **TU, x=960, y=430, tam=1600, busto=True, manos='frotar', claves=[dict(t=4.2)], cara='feliz'),
    dict(tipo='golpe', toma=2, desde=7.05, hasta=8.6, texto='¡ABIERTO!', tam=170, y=540),
    dict(tipo='multitud', toma=3, desde=8.8, hasta=16.0, n=28, paso=.24, dur=1.5),
    dict(tipo='persona', toma=3, desde=8.6, hasta=16.0, **TU, x=1290, y=930, tam=440, claves=[dict(t=8.6, pose='parado'), dict(t=12.5, pose='celebrar')], cara='feliz'),
    dict(tipo='pops', pantalla=True, encima=True, desde=8.9, hasta=16.0, tiempos=pops, x=1660, y=330),
    dict(tipo='cifra', pantalla=True, encima=True, desde=13.6, hasta=16.0, a=5776, prefijo='$', dur=1.0, sub='lo que vende una tienda promedio en un día', fuente='Cálculo: ventas 2025 (Dollar Tree) ÷ 9,200 tiendas ÷ 365 días', y=420, tam=150, color='#7dea8f'),
    dict(tipo='persona', toma=4, desde=16.0, hasta=20.6, **TU, x=960, y=430, tam=1500, busto=True, manos='arriba', claves=[dict(t=16.0)], cara='oo', rim='#7ee0a0'),
    dict(tipo='hud', pantalla=True, encima=True, desde=0.6, hasta=20.6, horaDe=6, horaA=21.25, relojDesde=8.6, relojDur=7.2, dinDe=0, dinA=5776, dinDesde=8.9, dinDur=6.9),
]
N = [(0.4, 2.3, 'Son las seis de la mañana.'), (2.4, 4.1, 'Y hoy, la tienda es tuya.'), (4.3, 6.9, 'Todo adentro cuesta un dólar con veinticinco.'),
     (7.0, 8.5, 'Abres la puerta…'), (8.7, 11.8, '…y empieza a entrar gente. Una tras otra.'),
     (11.9, 15.9, 'Al cerrar, una tienda promedio de Dollar Tree vende unos 5,800 dólares.'), (16.1, 20.3, 'Pero de todo eso… ¿cuánto es tuyo de verdad?')]
spec = dict(motor='cine', estilo='cine', fps=30, duracion=20.6, salida='demo-cine', tomas=tomas, eventos=ev, narracion=[dict(desde=a, hasta=b, texto=x) for a, b, x in N])
(D / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8'); print('ok')
