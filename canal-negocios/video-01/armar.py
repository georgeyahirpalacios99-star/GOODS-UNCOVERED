"""Video 1 de La Letra Chica: ¿Cómo gana dinero una tienda donde todo cuesta $1.25?
    python3 canal-negocios/video-01/alinear.py   # una vez: tiempos.json y voz completa
    python3 canal-negocios/video-01/armar.py && node motor-mapa/render.cjs canal-negocios/video-01
"""
import json, re, subprocess
from pathlib import Path
D = Path(__file__).resolve().parent
TJ = json.load(open(D / 'tiempos.json')); FR = TJ['frases']; FIN_VOZ = TJ['total']; DUR = round(FIN_VOZ + 12.5, 2)
S = lambda i: FR[i]['desde']; E = lambda i: FR[i]['hasta']
CLI = dict(id=1, ropa='#c23b4a', ropa2='#8f2533')
JEFE = dict(id=2, ropa='#2a3350', ropa2='#1c2238', corbata='#c8323a', sombrero='copa')
FUND = dict(id=3, ropa='#6b4a3a', ropa2='#4a3226', corbata='#2a2a2a')
tomas, ev = [], []
def toma(i, tipo, **k): tomas.append(dict(tipo=tipo, desde=0 if i == 0 else round(S(i) - .3, 2), **k))
def capa(tipo, i, d=0.0, **k): ev.append(dict(tipo=tipo, desde=round(S(i) + d, 2), **k))
def busto(i, quien, d=0.0, **k): capa('persona', i, d, **quien, x=k.pop('x', 960), y=k.pop('y', 600), tam=k.pop('tam', 1350), busto=True, claves=[dict(t=0)], **k)
def cifra(i, d, a, **k): capa('cifra', i, d, pantalla=True, encima=True, a=a, **k)
def golpe(i, d, txt, **k): capa('golpe', i, d, pantalla=True, encima=True, texto=txt, **k)
def cap(i, num, txt): toma(i, 'rayos', z0=1.1, z1=1, flash=True); capa('capitulo', i, -.2, pantalla=True, encima=True, num=num, texto=txt)

# 1 · gancho
toma(0, 'producto', z0=1, z1=1.08, foco=[960, 650], objetos=[[0, 'taza'], [S(0) + 2.6, 'pilas'], [S(0) + 3.6, 'pato'], [S(0) + 4.9, 'globo']])
capa('precio', 0, .6, x=1240, y=470, tam=1.5)
toma(1, 'calle', hora=.04, z0=1, z1=1.07, foco=[960, 600]); capa('multitud', 1, 0, n=26, paso=.26, dur=1.6); cifra(1, 2.2, 19400, prefijo='$', sufijo=' M', dur=1.6, sub='en ventas en un solo año (2025)', fuente='Dollar Tree, informe anual 2025', y=430, tam=160, color='#7dea8f')
toma(2, 'cara'); busto(2, CLI, signos=S(2) + .6, cara='serio')
toma(3, 'cara', c0='#1b1830', c1='#3b2a4a', bok='150,170,255'); busto(3, JEFE, x=1300, y=640, tam=1150, cara='pillo', rim='#9fb4ff'); golpe(3, 2.0, 'LO QUE NO VES', tam=110, y=300, color='#9fb4ff')
toma(4, 'rayos', z0=1.12, z1=1, flash=True); golpe(4, .3, '5 TRUCOS', tam=180, y=430, color='#ffd23f'); golpe(4, 3.4, '+ UN ERROR DE $8,000 M', tam=90, y=650, color='#ff4d7a')
# 2 · origen
toma(5, 'foco', z0=1.05, z1=1); golpe(5, .2, '¿CÓMO EMPEZÓ?', tam=110, y=480, color='#ffcf8a')
toma(6, 'calle', hora=.3, sepia=True, letrero='TIENDA DE VARIEDADES', neon=False, z0=1, z1=1.06, foco=[960, 560]); capa('rotulo', 6, .8, pantalla=True, encima=True, texto='1953', sub='Norfolk, Virginia')
toma(7, 'calle', hora=.3, sepia=True, letrero='K&K TOYS', neon=False, z0=1.06, z1=1, foco=[960, 560]); capa('multitud', 7, 0, n=20, paso=.4); cifra(7, 5.5, 130, prefijo='+', sufijo=' jugueterías', dur=1.6, y=300, tam=120, color='#ffcf8a')
toma(8, 'cara', sepia=True, c0='#3a2a20', c1='#6b4a30'); busto(8, FUND, cara='feliz', rim='#ffcf8a')
toma(9, 'foco', z0=1.1, z1=1); golpe(9, .3, '1986', tam=240, y=470, color='#ff9db5')
toma(10, 'calle', hora=.04, letrero='ONLY $1.00', z0=1, z1=1.07, foco=[960, 600]); cifra(10, 3.6, 5, sufijo=' tiendas', dur=.8, y=180, tam=110, color='#ff9db5')
toma(11, 'producto', objetos=[[S(11), 'taza'], [S(11) + 1.8, 'pilas'], [S(11) + 3.4, 'globo'], [S(11) + 5.2, 'pato']]); capa('precio', 11, .3, x=1240, y=470, tam=1.5, texto='$1.00')
cap(12, '1', 'El precio que no te deja pensar')
toma(13, 'cara', c0='#2b2040', c1='#5b3350'); busto(13, CLI, x=1250, y=650, tam=1150, cara='feliz'); capa('piensa', 13, 2.5, x=600, y=330, texto='$1', tam=110)
toma(14, 'calle', hora=.04, letrero='DOLLAR TREE', neonColor='#3fbf6a', neonClaro='#a8f5b8', z0=1, z1=1.07, foco=[960, 600]); capa('rotulo', 14, 4.0, pantalla=True, encima=True, texto='1993', sub='nace Dollar Tree')
toma(15, 'ruta', de='CALIFORNIA', a='NUEVA YORK')
toma(16, 'ciudad', n=110, paso=.03, z0=1, z1=1.12, foco=[960, 600])
toma(17, 'cara', c0='#1b1830', c1='#3b2a4a', bok='150,170,255'); busto(17, JEFE, cara='pillo', rim='#9fb4ff'); golpe(17, 3.0, 'FALTAN 4 TRUCOS', tam=90, y=170, color='#ffd23f')
# 3 · trucos 2 y 3
cap(18, '2', 'Comprar como un gigante')
toma(19, 'fabrica', z0=1, z1=1.06, foco=[960, 600])
toma(20, 'ruta', de='CHINA', a='EE. UU.'); cifra(20, 1.0, 40, sufijo=' %', dur=1.2, sub='de lo que vende lo importa directo', fuente='Dollar Tree, Form 10-K', y=180, tam=120, color='#ff9db5')
toma(21, 'puerto', hora=.66, barcos=1); cifra(21, 4.5, 18, dur=1, sub='centros de distribución', y=200, tam=120, color='#ffcf8a')
toma(22, 'producto', z0=1, z1=1.06); capa('lista', 22, 0, pantalla=True, encima=True, x=110, y=210, w=760, titulo='SI COMPRAS…',
     items=[[S(23), '1 taza → precio de tienda', '#e8574a'], [S(23) + 2.5, '100 tazas → descuento', '#ffd23f'], [S(24) + .5, '100,000 → directo de fábrica', '#3fbf6a']])
toma(25, 'cara', c0='#1b1830', c1='#3b2a4a', bok='150,170,255'); busto(25, JEFE, cara='pillo', rim='#9fb4ff'); capa('pops', 25, .5, pantalla=True, encima=True, tiempos=[round(S(25) + .6 + k * .3, 2) for k in range(18)], textos=['+1¢'], x=420, y=330)
cap(26, '3', 'El precio manda sobre el producto')
toma(27, 'producto', z0=1, z1=1.05); capa('precio', 27, 2.0, x=1240, y=470, tam=1.5)
toma(28, 'producto', objetoDesde=S(28) + 2.6, z0=1.05, z1=1); capa('precio', 28, .3, x=1240, y=470, tam=1.7)
toma(29, 'producto', encoger=S(29) + 3.0, z0=1, z1=1.05); capa('precio', 29, .2, x=1240, y=470, tam=1.5); golpe(29, 3.2, '¿MÁS PEQUEÑO?', tam=100, y=200, color='#ffd23f')
toma(30, 'cara'); busto(30, CLI, cara='feliz'); golpe(30, 1.5, 'FÍJATE EN EL TAMAÑO', tam=96, y=150, color='#7dea8f')
toma(31, 'cara', c0='#1b1830', c1='#3b2a4a', bok='150,170,255'); busto(31, JEFE, cara='serio', rim='#9fb4ff', signos=S(31) + .5)
toma(32, 'interior', z0=1, z1=1.06); capa('versus', 32, 3.0, pantalla=True, encima=True, izq=['Comida y limpieza', 'menos margen'], der=['Variedad y temporada', 'más margen'], derDesde=S(32) + 5.2)
# 4 · trucos 4 y 5
cap(34, '4', 'Tiendas pequeñas… pero muchísimas')
toma(35, 'plano'); cifra(35, 4.5, 930, prefijo='750 – ', sufijo=' m²', dur=.01, y=170, tam=90, color='#ff9db5')
toma(36, 'calle', hora=.04, z0=1.05, z1=1, foco=[960, 600]); capa('lista', 36, .3, pantalla=True, encima=True, x=120, y=230, w=600, items=[[S(36) + .5, 'Menos renta'], [S(36) + 1.5, 'Menos luz'], [S(36) + 2.6, 'Menos personal']])
toma(37, 'ciudad', n=120, paso=.03, z0=1, z1=1.12, foco=[960, 600]); cifra(37, 2.0, 9200, prefijo='+', dur=2.2, sub='tiendas en EE. UU. y Canadá', y=190, tam=140, color='#ff9db5')
toma(38, 'dia', horaDe=.05, horaA=.97, z0=1, z1=1.05, foco=[960, 600]); capa('multitud', 38, 0, n=26, paso=.26, dur=1.5); capa('hud', 38, 0, pantalla=True, encima=True, horaDe=8, horaA=21, relojDesde=S(38), relojDur=E(39) - S(38), dinDe=0, dinA=5776, dinDesde=S(38), dinDur=E(39) - S(38))
cifra(38, 3.0, 5800, prefijo='≈ $', dur=1.5, sub='al día, por tienda', fuente='Cálculo: ventas 2025 ÷ 9,200 tiendas ÷ 365 días', y=420, tam=140, color='#7dea8f')
toma(40, 'interior', z0=1, z1=1.08); capa('pops', 40, .5, pantalla=True, encima=True, tiempos=[round(S(40) + .5 + k * .22, 2) for k in range(int((E(43) - S(40)) / .22) - 3)], textos=['+ taza', '+ pilas', '+ globo', '+ dulces', '+ cargador'], x=1600, y=300)
cifra(41, 2.0, 4600, prefijo='≈ ', sufijo=' cosas', dur=1.8, sub='vendidas al día en una sola tienda', y=430, tam=140, color='#ffd23f')
cifra(42, 1.2, 6, sufijo=' por minuto', dur=1.0, sub='si abre 13 horas', y=430, tam=150, color='#ff9db5')
cap(44, '5', 'La cacería del tesoro')
toma(45, 'interior', z0=1, z1=1.06); capa('persona', 45, 0, **CLI, x=-150, y=1000, tam=520, claves=[dict(t=S(45) - .3, x=-150), dict(t=S(45) + 2.8, x=760, dir=1)], cara='feliz')
capa('pops', 46, .3, pantalla=True, encima=True, tiempos=[round(S(46) + .4 + k * 1.3, 2) for k in range(6)], textos=['+ globos', '+ cargador', '+ dulces', '+ taza', '+ pilas', '+ pato'], x=1560, y=280); cifra(46, 7.0, 6, prefijo='', sufijo=' cosas', dur=.6, sub='y entraste por una', y=520, tam=150, color='#ffd23f')
toma(47, 'producto', objeto='caja', z0=1, z1=1.06); cifra(48, .5, 10, prefijo='< ', sufijo=' %', dur=1, sub='de sus compras son ofertas de oportunidad', fuente='Dollar Tree, Form 10-K', y=180, tam=120, color='#ff9db5')
toma(49, 'rayos', z0=1.12, z1=1, flash=True); golpe(49, 1.2, 'COMPRA POR IMPULSO', tam=130, y=500, color='#ff4d7a')
toma(51, 'calle', hora=.62, apagar=S(52) + 1.8, z0=1, z1=1.08, foco=[960, 560])
# 5 · la crisis
toma(53, 'foco', z0=1.1, z1=1); golpe(53, .2, '2021', tam=240, y=470, color='#e8463a')
toma(54, 'puerto', hora=.68, barcos=7, camion=False, z0=1, z1=1.05)
toma(55, 'ruta', de='ASIA', a='EE. UU.'); cifra(55, .8, 40, prefijo='≈ ', sufijo=' %', dur=1, sub='llega en contenedores', y=180, tam=120, color='#ff9db5')
toma(56, 'producto'); capa('precio', 56, .2, x=1240, y=470, tam=1.5, texto='$1.00'); capa('barra', 56, 1.0, pantalla=True, encima=True, x=110, y=120, w=820, partes=[dict(valor=92, cifra='casi $1', texto='traerlo hasta la tienda', color='#e8574a', desde=S(56) + 2.0), dict(valor=8, cifra='', texto='', color='#3fbf6a', desde=99)], fuente='ejemplo')
toma(57, 'puerto', hora=.7, barcos=4); cifra(57, 3.0, 200, prefijo='+$', sufijo=' M', dur=1.2, sub='extra en fletes en 2021', fuente='Dollar Tree / AP', y=200, tam=130, color='#e8463a')
toma(58, 'producto', z0=1, z1=1.08); capa('cambio', 58, 0, x=1180, y=380, de='$1.00', a='$1.25', tachar=S(59) + .3); golpe(59, 3.0, 'PERMANENTE', tam=100, y=170, color='#ff4d7a')
toma(60, 'producto', objeto='globo'); capa('precios', 60, 0, items=[[S(60) + .4, '$1.25', 1260, 440, 1.4], [S(61) + .3, '$3', 520, 380, 1.4], [S(61) + 1.6, '$5', 620, 620, 1.4]])
cifra(62, 1.0, 5300, prefijo='≈ ', dur=1.4, sub='tiendas con varios precios', fuente='Dollar Tree, año fiscal 2025', y=180, tam=120, color='#ff9db5')
toma(63, 'calle', hora=.04, z0=1, z1=1.07, foco=[960, 600]); capa('multitud', 63, 0, n=28, paso=.3, dur=1.6)
# 6 · Family Dollar
toma(65, 'foco', z0=1.1, z1=1); golpe(65, .2, 'EL ERROR', tam=220, y=470, color='#e8463a')
toma(66, 'calle', hora=.04, letrero='FAMILY DOLLAR', neonColor='#ff8a2b', neonClaro='#ffd0a0', z0=1, z1=1.07, foco=[960, 600]); cifra(66, 3.5, 8000, prefijo='+$', sufijo=' M', dur=1.4, sub='lo que pagó en 2015', y=430, tam=150, color='#ffcf8a')
toma(67, 'foco'); capa('comparar', 67, 0, pantalla=True, encima=True, barras=[dict(valor=8000, texto='+$8,000 M', sub='compra 2015', color='#ffb36b', desde=S(67)), dict(valor=1000, texto='~$1,000 M', sub='venta 2025', color='#e8463a', desde=S(67) + 3.5)])
toma(68, 'cara', c0='#1e1a2a', c1='#2c2335', bok='160,170,200'); busto(68, CLI, x=1300, y=640, tam=1150, cara='serio', rim='#c8d0ff')
capa('lista', 69, 3.0, pantalla=True, encima=True, x=110, y=260, w=700, titulo='¿QUÉ SALIÓ MAL?', items=[[S(69) + 3.4, 'Inflación', '#e8463a'], [S(69) + 6.0, 'Robos en tiendas', '#e8463a'], [S(69) + 8.4, 'Fin de las ayudas', '#e8463a']])
toma(70, 'calle', hora=.9, letrero='FAMILY DOLLAR', neonColor='#ff8a2b', neonClaro='#ffd0a0', apagar=S(70) + 1.5, z0=1, z1=1.06, foco=[960, 560]); golpe(70, 2.2, 'CERRADO', tam=150, y=560, color='#e8463a')
toma(71, 'rayos', z0=1.1, z1=1, flash=True); cifra(71, .4, 7000, prefijo='-$', sufijo=' M', dur=1.4, sub='de valor perdido', y=470, tam=180, color='#e8463a')
toma(72, 'cara', c0='#1b1830', c1='#3b2a4a', bok='150,170,255'); busto(72, JEFE, cara='serio', rim='#9fb4ff')
# 7 · los números y el cierre
toma(73, 'cara'); busto(73, CLI, cara='oo', rim='#7ee0a0')
toma(74, 'producto', z0=1, z1=1.06); capa('precio', 74, .2, x=1240, y=470, tam=1.5); capa('barra', 74, .3, pantalla=True, encima=True, x=110, y=120, w=820, hasta=E(75) + .3,
     partes=[dict(valor=80, cifra='≈ 80¢', texto='producto y llevarlo a la tienda', color='#e8574a', desde=S(74) + 2.2), dict(valor=45, cifra='≈ 45¢', texto='le queda', color='#3fbf6a', desde=S(75) + .8)], fuente='margen bruto 36.4 %, Dollar Tree, año fiscal 2025')
toma(76, 'dia', horaDe=.6, horaA=.98, flash=True); capa('multitud', 76, 0, n=20, paso=.3); cifra(76, 2.0, 7050, prefijo='$', sufijo=' M', dur=1.4, sub='ganancia bruta en 2025', fuente='Dollar Tree, informe anual 2025', y=420, tam=150, color='#7dea8f')
toma(77, 'rayos', z0=1.12, z1=1, flash=True); golpe(77, .2, 'NO ES LO QUE VENDEN', tam=96, y=400, color='#fff'); golpe(77, 1.9, 'ES CUÁNTAS VECES', tam=120, y=580, color='#7dea8f')
toma(78, 'cara', c0='#2b2040', c1='#5b3350'); busto(78, CLI, x=1400, y=660, tam=1050, cara='feliz')
capa('lista', 79, -.3, pantalla=True, encima=True, x=110, y=230, w=760, titulo='LOS 5 TRUCOS', tam=38, lh=86,
     items=[[S(79), '1 · El precio único'], [S(79) + 2.4, '2 · Comprar gigante'], [S(79) + 5.0, '3 · El precio manda'], [S(79) + 7.6, '4 · Tiendas pequeñas'], [S(79) + 10.4, '5 · La cacería del tesoro']], hasta=E(79) + .2)
capa('lista', 80, 0, pantalla=True, encima=True, x=110, y=300, w=760, titulo='LA PRÓXIMA VEZ', items=[[S(80) + .2, 'Lleva tu lista'], [S(80) + 1.6, 'Fíjate en el tamaño'], [S(80) + 3.2, 'Decide tú, no la tienda']])
toma(81, 'cara', c0='#2a1630', c1='#5b2340', bok='255,110,150'); busto(81, CLI, y=660, tam=1150, manos='arriba', cara='feliz', rim='#ff9db5'); capa('pregunta', 81, .2, pantalla=True, encima=True, texto='¿QUÉ NEGOCIO EXPLICAMOS DESPUÉS?', y=150)
golpe(82, 1.5, 'SUSCRÍBETE', tam=120, y=950, color='#ff4d7a')
tomas.append(dict(tipo='fin', desde=round(FIN_VOZ + .5, 2), z0=1, z1=1.02))

# fin de cada capa: el siguiente corte (salvo que diga otra cosa); toma a la que pertenece
cortes = sorted(x['desde'] for x in tomas)
for e in ev:
    k = max(j for j, x in enumerate(tomas) if x['desde'] <= e['desde'] + 1e-6)
    sig = tomas[k + 1]['desde'] if k + 1 < len(tomas) else DUR
    e.setdefault('hasta', sig); e['toma'] = k
    if e['tipo'] == 'persona' and not e.get('busto'): pass
# subtítulos: trozos de máximo 52 caracteres, con tiempo proporcional
narr = []
for f in FR:
    pal, trozos, cur = f['texto'].split(), [], ''
    for w in pal:
        if len(cur) + len(w) + 1 > 52 and cur: trozos.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    trozos.append(cur); tot = sum(len(x) for x in trozos); t = f['desde']
    for x in trozos: d = (f['hasta'] - f['desde']) * len(x) / tot; narr.append(dict(desde=round(t, 2), hasta=round(t + d, 2), texto=x)); t += d
audio = D / 'voz' / 'voz-final.wav'
if not audio.exists(): subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(D / 'voz' / 'voz-completa.wav'), '-af', f'apad=whole_dur={DUR}', str(audio)], check=True)
spec = dict(motor='cine', estilo='cine', fps=30, duracion=DUR, salida='video-01', audio='voz/voz-final.wav', tomas=tomas, eventos=ev, narracion=narr)
(D / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False), encoding='utf-8')
print(len(tomas), 'tomas,', len(ev), 'capas, duración', DUR)
