import re, json, sys
src, dst = sys.argv[1], sys.argv[2]
voz = {}; b = None
for l in open(src):
    m = re.match(r'^## voz-0(\d)', l)
    if m: b = int(m.group(1)); voz[b] = []; continue
    if b and l.strip() and not l.startswith('```'):
        voz[b].append(re.sub(r'\s*<break[^>]*>\s*', '', l.strip()))

def I(img, buscar, **k): return dict(tipo='img', imagen=img, buscar=buscar, **k)
P = lambda bl, *esc: ('p', bl, list(esc))
T = lambda txt, d=3.2: ('t', txt, d)
V = lambda d, *esc: ('v', d, list(esc))
NASA = 'NASA / NOAA'
ECU = dict(lon=-80.4, lat=-1.6, nombre='Ecuador')
PAITA = dict(lon=-81.1, lat=-5.1, nombre='Paita')
GAL = dict(lon=-90.5, lat=-.7, nombre='Galápagos')

TL = [
  # BLOQUE 1 · GANCHO
  P(1, I('lluvia-charco', 'rain puddle night (Pexels)'), I('calle-inundada', 'flooded street car (Pexels)', vhs=True)),
  P(1, dict(tipo='cifra', items=[dict(desde=0, hasta=37, unidad=' mm', texto='en un solo día de septiembre')])),
  P(1, I('agua-puerta', 'flood water door (Pexels)'), I('relampago-ciudad', 'lightning city (Pexels)')),
  T('y eso… *no* es normal', 2.8),
  P(1, I('mapa-mar-caliente', 'El Niño sea level map (NASA)', credito='NASA / JPL · nivel del mar, 6 oct 1997', etiqueta='ASÍ ESTABA EL MAR EN 1997', zoom=.12),
       dict(tipo='cifra', items=[dict(valor='29 °C', texto='el mar frente a Ecuador'), dict(valor='+7 °C', rojo=True, texto='sobre lo normal')], peso=1.2)),
  P(1, I('archivo-1998-inundacion', 'flood 1998', bn=True, vhs=True, etiqueta='RECREACIÓN · ECUADOR 1998')),
  T('¿estamos a punto de vivir el niño *más* *fuerte* de la historia?', 4.2),
  V(3, dict(tipo='marca', sub='una investigación sobre El Niño 2026')),
  # BLOQUE 2 · QUÉ ES EL NIÑO
  P(2, I('grabado-puerto', 'fishing port engraving 19th century (PD)', bn=True), dict(tipo='costa', puntos=[PAITA, ECU], titulo='1892')),
  P(2, I('pesebre', 'nativity painting public domain', color=True)),
  P(2, dict(tipo='tablero', piezas=[dict(imagen='grabado-puerto', x=560, y=480, w=480, texto='Paita'), dict(texto='Camilo Carrillo · 1892', x=1180, y=380), dict(texto='corriente caliente después de Navidad', x=1300, y=720, rojo=True)], hilo=True)),
  P(2, dict(tipo='costa', titulo='la corriente de Humboldt', puntos=[ECU, PAITA], flechas=[dict(ruta=[[-77, -45], [-76, -35], [-73.5, -22], [-79, -10], [-83, -3], [-84.5, 0]], texto='agua fría', dy=60)])),
  P(2, I('mar-gris', 'grey ocean waves (Pexels)'), I('playa-seca', 'dry beach (Pexels)')),
  P(2, I('nubes-oceano', 'clouds over Pacific GOES satellite (NASA)', credito=NASA)),
  P(2, dict(tipo='esquema', pasos=[dict(texto='agua fría', azul=True), dict(texto='no se evapora'), dict(texto='no hay nubes')]),
       dict(tipo='esquema', pasos=[dict(texto='agua caliente', rojo=True), dict(texto='se evapora'), dict(texto='tormentas', rojo=True)])),
  P(2, I('mapa-anomalia-oct', 'sea level map', credito='NASA / JPL', zoom=.18)),
  P(2, dict(tipo='costa', puntos=[ECU], flechas=[dict(ruta=[[-100, 0], [-90, 0], [-82, -1]], rojo=True, texto='onda Kelvin', dy=-50), dict(ruta=[[-82, -1], [-80, 6], [-79, 9]], rojo=True), dict(ruta=[[-82, -1], [-80, -12], [-73, -25]], rojo=True)])),
  P(2, I('boyas-pacifico', 'TAO buoy array (NOAA)', credito=NASA), dict(tipo='cifra', items=[dict(valor='+3.9 °C', rojo=True, texto='región Niño 1+2 · frente a Ecuador')])),
  P(2, I('olas-rompiendo', 'big waves crashing (Pexels)')),
  # BLOQUE 3 · 2023
  T('en 2023 también nos lo dijeron…', 3),
  P(3, I('celular-lluvia', 'phone rain (Pexels)')),
  P(3, dict(tipo='esquema', titulo='2023', pasos=[dict(texto='pronóstico: fuerte', rojo=True), dict(texto='resultado: moderado')])),
  P(3, I('nubes-oceano', 'clouds', credito=NASA, zoom=.15)),
  P(3, dict(tipo='barras', titulo='lluvia en Guayaquil en septiembre', barras=[dict(etiqueta='septiembre 1997', valor=12.4, texto='12.4 mm'), dict(etiqueta='un solo día de septiembre 2026', valor=37, texto='37 mm', rojo=True)])),
  T('pero esta vez… el mar *dice* *otra* *cosa*', 3.2),
  P(3, I('mapa-anomalia-oct', 'El Niño sea level map 2023 (NASA)', credito='NASA / JPL · nivel del mar, mar 2023', etiqueta='EL NIÑO DE 2023'), dict(tipo='barras', titulo='anomalía de temperatura frente a la costa', barras=[dict(etiqueta='2023', valor=3, texto='~3 °C'), dict(etiqueta='2026', valor=7, texto='hasta 7 °C', rojo=True)])),
  P(3, I('mar-profundo', 'deep ocean underwater blue (Pexels)')),
  T('no hay agua fría ni a *100* *metros*', 3),
  P(3, dict(tipo='perfil', titulo='el mar frente a Ecuador · octubre 2026', marcas=[dict(f=0, prof='0 m', temp='29 °C'), dict(f=.5, prof='50 m', temp='24 °C'), dict(f=1, prof='100 m', temp='sin agua fría')])),
  P(3, dict(tipo='cifra', items=[dict(desde=0, hasta=83, unidad=' %', texto='probabilidad de un Niño fuerte o muy fuerte · NOAA')]),
       dict(tipo='cita', texto='se parece al de 1997… pero va en camino de ser más grande', autor='Josh Willis, NASA')),
  # BLOQUE 4 · 1997
  P(4, I('archivo-1998-canoa', 'canoe street', bn=True, vhs=True, etiqueta='RECREACIÓN · 1998')),
  P(4, dict(tipo='linea', titulo='El Niño 1997-1998', puntos=[dict(fecha='7 nov 1997', texto='Santa Rosa, El Oro'), dict(fecha='1998', texto='Chone, Portoviejo, Vinces, Quevedo, Machala'), dict(fecha='9 meses', texto='de lluvia en la Costa', rojo=True)])),
  T('9 meses de lluvia', 2.6),
  P(4, I('puente-caido', 'bridge', bn=True, etiqueta='RECREACIÓN')),
  P(4, dict(tipo='cifra', items=[dict(valor='286', rojo=True, texto='muertos'), dict(valor='30,000', texto='personas sin hogar'), dict(valor='USD 2,882 M', texto='≈ 15 % de la economía del país')])),
  P(4, dict(tipo='barras', titulo='daños de El Niño en Ecuador', barras=[dict(etiqueta='1982-1983', valor=640, texto='USD 640 M'), dict(etiqueta='1997-1998', valor=2882, texto='USD 2,882 M', rojo=True)])),
  P(4, I('banano-inundado', 'banana plantation (Pexels)'), I('cacao', 'cacao pods (Pexels)')),
  P(4, I('archivo-bn', 'archive', bn=True, vhs=True, color=True, etiqueta='RECREACIÓN')),
  T('hubo uno peor… y casi *nadie* lo recuerda', 3.2),
  # BLOQUE 5 · 1940 + IGUANAS
  P(5, I('guayaquil-1940', 'Guayaquil 1940', bn=True, vhs=True, etiqueta='RECREACIÓN · GUAYAQUIL 1940'), dict(tipo='cifra', items=[dict(valor='1939 - 1942'), dict(valor='~9,000 mm', texto='de lluvia en Guayaquil'), dict(valor='×1.5', rojo=True, texto='más que en 1997')])),
  P(5, I('periodicos-guerra', 'WWII newspaper headlines public domain', bn=True, color=True)),
  T('el niño que ecuador *olvidó*', 3),
  P(5, I('galapagos-satelite', 'Galapagos Islands satellite (NASA)', credito=NASA), I('iguana-marina', 'marine iguana Galapagos (CC0)')),
  P(5, I('algas-rocas', 'intertidal algae rocks Galapagos (PD)'), I('mar-profundo', 'underwater', zoom=.2)),
  P(5, dict(tipo='cifra', items=[dict(valor='−20 %', rojo=True, texto='de su tamaño'), dict(valor='hueso', texto='no grasa')]), I('iguana-marina', 'marine iguana', zoom=.25, dir=1)),
  T('para sobrevivir… se *encogen*', 3),
  P(5, I('iguana-marina', 'marine iguana', zoom=.15, dir=-1)),
  P(5, dict(tipo='tablero', piezas=[dict(imagen='iguana-marina', x=620, y=470, w=520, texto='Wikelski y Thom · Nature · 2000'), dict(texto='+100 se encogieron y volvieron a crecer', x=1300, y=520)])),
  # BLOQUE 6 · PARADOJA
  T('y eso no es lo más *extraño*…', 3),
  P(6, dict(tipo='esquema', titulo='El Niño 2026 en Ecuador', pasos=[dict(texto='Costa: lluvia', azul=True), dict(texto='Sierra'), dict(texto='Amazonía y Austro: sequía', rojo=True)])),
  P(6, I('represa', 'hydroelectric dam reservoir (PD)'), dict(tipo='cifra', items=[dict(valor='~4,000 MW', texto='en las cuencas del Oriente')])),
  P(6, dict(tipo='cifra', items=[dict(desde=0, hasta=5.43, dec=2, unidad=' m', rojo=True, texto='bajó el embalse de Mazar · ago-sep 2026')])),
  P(6, dict(tipo='barras', titulo='caudal del río Paute', barras=[dict(etiqueta='1997', valor=119.45, texto='119 m³/s'), dict(etiqueta='2026', valor=114.13, texto='114 m³/s', rojo=True)])),
  P(6, I('ciudad-apagon', 'city blackout', zoom=.14)),
  T('un país que se inunda… y se queda *sin* *agua*', 3.4),
  P(6, I('agua-estancada', 'stagnant water (Pexels)'), dict(tipo='cifra', items=[dict(valor='38,607', texto='casos de dengue en 2026'), dict(valor='42', rojo=True, texto='muertes')])),
  P(6, dict(tipo='tablero', piezas=[dict(texto='mar a 29 °C', x=420, y=300), dict(texto='sin agua fría a 100 m', x=900, y=260, rojo=True), dict(imagen='archivo-1998-inundacion', x=1450, y=330, w=380, texto='1998'), dict(imagen='iguana-marina', x=520, y=720, w=360, texto='Galápagos'), dict(texto='Mazar −5.4 m', x=1050, y=700, rojo=True), dict(texto='dengue: 38,607', x=1520, y=760)], hilo=True)),
  P(6, I('cientifico-datos', 'scientist data screen (Pexels)')),
  T('lo peor todavía *no* *llega*', 3),
  # BLOQUE 7 · QUÉ VIENE
  P(7, dict(tipo='calendario', titulo='mayor impacto esperado · Comité ERFEN', meses=['nov', 'dic', 'ene', 'feb', 'mar'])),
  P(7, dict(tipo='cifra', items=[dict(valor='33,486', texto='personas afectadas'), dict(valor='817', texto='eventos en 23 provincias'), dict(valor='52 → 107', rojo=True, texto='ríos desbordados · sep → oct')])),
  P(7, I('limpiar-desague', 'cleaning drain (Pexels)'), I('tanque-agua', 'water tank (Pexels)'), I('mochila', 'emergency backpack (Pexels)')),
  P(7, I('pescador', 'fisherman sunrise sea (Pexels)')),
  P(7, I('lluvia-charco', 'rain puddle night (Pexels)')),
  P(7, I('pescador', 'fisherman', zoom=.12, dir=1)),
  V(4, dict(tipo='marca', sub='¿cómo está lloviendo en tu ciudad? cuéntanos abajo')),
]

usados = {}; out = []
for it in TL:
    if it[0] == 't': out.append(dict(tarjeta=it[1], dur=it[2]))
    elif it[0] == 'v': out.append(dict(dur=it[1], escenas=it[2]))
    else:
        bl = it[1]; i = usados.get(bl, 0); usados[bl] = i + 1
        out.append(dict(bloque=bl, voz=voz[bl][i], escenas=it[2]))
for bl, ps in voz.items():
    assert usados.get(bl) == len(ps), f'bloque {bl}: {usados.get(bl)} escenas vs {len(ps)} párrafos'
json.dump(dict(salida='001-el-nino-2026', fps=30, volumen_musica=0.1, timeline=out), open(dst, 'w'), ensure_ascii=False, indent=1)
print('ok', len(out), 'items')
