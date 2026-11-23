"""Video largo 008 · Argentina vs Brasil: EL PARTIDO — motor 3D (estadio) + fotos reales + voz de ElevenLabs.
    python3 videos-largos/008-argentina-vs-brasil/construir.py
    (render en paralelo) node motor-3d/render3d.cjs videos-largos/008-argentina-vs-brasil --desde A --hasta B
"""
import json, sys
from pathlib import Path
DIR = Path(__file__).resolve().parent; sys.path.insert(0, str(DIR))
from voz_alineada import preparar
BL, DUR = preparar(); B = {b.n: b for b in BL}
def T(cod, frase, k=1, d=0.0): return B['voz-' + cod].T(frase, k, d)
def INI(cod): return round(B['voz-' + cod].t0, 2)
def FIN(cod): return round(B['voz-' + cod].fin, 2)
CR = {c['archivo']: f"Foto: {c['autor'].split('(')[0].split('/')[0].strip()[:28]} · {c['licencia']}" for c in json.loads((DIR / 'fotos-reales' / 'creditos.json').read_text())}
def F(n): return 'fotos-reales/' + n

ISO = {'BRA': 'br', 'ARG': 'ar', 'BOL': 'bo', 'PRY': 'py', 'URY': 'uy', 'PER': 'pe', 'COL': 'co', 'VEN': 've', 'GUY': 'gy', 'SUR': 'sr', 'ECU': 'ec', 'CHL': 'cl'}
RIO, BA, SP, MZA, BRS = [-43.21, -22.91], [-58.38, -34.6], [-46.63, -23.55], [-69.99, -32.65], [-47.88, -15.79]
PRE = {'cielo': (-58, -20, 430, 30), 'medio': (-58, -21, 480, 38), 'ancho': (-58, -21, 900, 52), 'arg': (-63, -32, 300, 42), 'bra': (-51, -13, 320, 42),
       'rio': (-45.5, -22.5, 210, 46), 'ba': (-60, -33, 210, 46), 'norte': (-58, -5, 560, 30), 'sp': (-48, -23, 230, 46), 'mza': (-68, -32, 230, 44)}
cam, capas, goles, pant, tarj, ult = [], [], [], [], [], [None]
def CAM(t, p, d=1.0):
    lon, lat, dist, inc = PRE[p]
    if ult[0]: cam.append(dict(t=round(t, 2), lon=ult[0][0], lat=ult[0][1], dist=ult[0][2], inclin=ult[0][3]))
    cam.append(dict(t=round(t + d, 2), lon=lon, lat=lat, dist=dist, inclin=inc)); ult[0] = (lon, lat, dist, inc)
def C(tipo, a, b, **kw): capas.append(dict(tipo=tipo, desde=round(a, 2), hasta=round(b, 2), **kw))
def ficha(a, b, kicker, texto, sub='', tam=80): C('ficha', a, b, kicker=kicker, texto=texto, sub=sub, y=800, tam=tam)
def foto(img, a, b, z0=1.03, z1=1.13, px=0, **kw): C('foto', a, b, img=F(img), z0=z0, z1=z1, px=px, credito=CR.get(img, ''), **kw)
def barrido(t): C('barrido', t - .35, t + .3)
def tarjeta(img, a, b, en, texto, x=1450, y=360, w=540, rot=0): C('tarjeta', a, b, img=F(img), lon=en[0], lat=en[1], x=x, y=y, w=w, texto=texto, credito=CR.get(img, ''), rot=rot)
def marcador(a, b, titulo, izq, der, gana=None, suf='', tam=110): C('marcador', a, b, titulo=titulo, isoIzq='ar', isoDer='br', nomIzq='Argentina', nomDer='Brasil', izq=izq, der=der, y=930, tam=tam, suf=suf, **({'gana': gana} if gana else {}))
def gol(frase_t, pais, texto, hinchas):  # el balón sale 1 s antes y entra justo cuando la voz dice "Gol de…"
    t = round(frase_t - 1.0, 2); goles.append(dict(t=t, pais=pais, lado=1 if pais == 'ARG' else -1, texto=texto)); CAM(t - .4, 'ancho', .5)
    pant.append(dict(desde=round(t + 1.0, 2), hasta=round(t + 4.6, 2), img=F(hinchas), texto=texto))

# ===================== voz-01 · gancho =====================
foto('maradona-1.jpg', 0, T('01', 'Hoy los vamos'), z0=1.0, z1=1.12, sinFundido=True)
ficha(.3, T('01', 'Hoy los vamos') - .1, 'Lo Que el Mapa No Dice', 'Argentina vs Brasil', 'El clásico más grande de América', tam=96)
t = T('01', 'Hoy los vamos'); barrido(t); cam.append(dict(t=0, lon=-58, lat=-20, dist=430, inclin=30)); ult[0] = PRE['cielo']
ficha(t + .2, T('01', 'Diez rondas'), 'Hoy los enfrentamos', 'En todo', 'Fútbol, tamaño, dinero, ciencia, carreras, cine y comida')
C('marcador', T('01', 'Diez rondas'), T('01', 'Porque uno'), titulo='10 rondas · cada una vale un gol', isoIzq='ar', isoDer='br', nomIzq='Argentina', nomDer='Brasil', izq='?', der='?', y=930, tam=110)
CAM(T('01', 'Porque uno', d=-.3), 'bra'); tarjeta('pele-1970-1.jpg', T('01', 'tiene cinco Copas'), T('01', 'Y el otro'), BRS, 'Brasil · 5 Copas del Mundo')
CAM(T('01', 'Y el otro', d=-.3), 'rio'); tarjeta('maracana-1.jpg', T('01', 'Y el otro'), T('01', 'Una regla'), RIO, 'Maracaná · Río de Janeiro', rot=2)
CAM(T('01', 'Una regla', d=-.3), 'medio'); ficha(T('01', 'Una regla'), T('01', 'Y si hay polémica'), 'Regla del partido', 'Solo datos', 'Nada de opiniones')
C('var', T('01', 'Y si hay polémica'), T('01', 'Así que elige'), texto='Revisión')
C('adelanto', T('01', 'Así que elige'), T('01', 'Y si en algún'), minuto="45'", kicker='En el entretiempo', texto='El dato que nadie conoce', y=900)
ficha(T('01', 'Y si en algún'), FIN('01') - .1, 'Arriba, siempre', 'Marcador y reloj', 'Nunca se detienen')
TE = T('01', 'Rueda el balón'); C('ficha', TE + .6, TE + 2.6, kicker='Empieza', texto='El partido', sub='Argentina vs Brasil', y=800, tam=96); CAM(TE - .2, 'ancho', 1.4)

# ===================== voz-02 · Ronda 1 y 2 =====================
ficha(INI('02'), T('02', 'Brasil tiene cinco'), 'Ronda 1', 'Copas del Mundo', 'La que todos quieren ver')
CAM(T('02', 'Brasil tiene cinco', d=-.3), 'bra'); tarjeta('pele-1970-2.jpg', T('02', 'Brasil tiene cinco'), T('02', 'Argentina tiene tres'), BRS, 'Brasil · 1958 · 62 · 70 · 94 · 2002')
CAM(T('02', 'Argentina tiene tres', d=-.3), 'arg'); tarjeta('maradona-1.jpg', T('02', 'Argentina tiene tres'), T('02', 'y dos mil veintidós'), BA, 'Argentina · 1978 · 1986 · 2022')
foto('messi-2022-2.jpg', T('02', 'y dos mil veintidós'), T('02', 'Y eso que Brasil'), px=1); ficha(T('02', 'y dos mil veintidós') + .2, T('02', 'Y eso que Brasil') - .1, 'Catar 2022', 'Messi, campeón del mundo')
barrido(T('02', 'Y eso que Brasil')); CAM(T('02', 'Y eso que Brasil', d=-.3), 'rio')
tarjeta('maracana-2.jpg', T('02', 'En mil novecientos cincuenta'), T('02', 'Y en dos mil catorce'), RIO, '1950 · Final perdida en el Maracaná')
foto('copa-mundial-trofeo-1.jpg', T('02', 'Y en dos mil catorce'), T('02', 'Pero los números')); ficha(T('02', 'Y en dos mil catorce') + .2, T('02', 'Pero los números') - .1, 'Brasil 2014 · Semifinal', '1 - 7 con Alemania', 'Alemania terminó campeona')
barrido(T('02', 'Pero los números')); CAM(T('02', 'Pero los números', d=-.2), 'medio')
marcador(T('02', 'Pero los números'), T('02', 'Ronda dos') - .1, 'Ronda 1 · Copas del Mundo', 3, 5)
gol(T('02', 'Gol de Brasil'), 'BRA', 'Brasil · 5 Mundiales', 'torcida-bra-1.jpg')
ficha(T('02', 'Ronda dos'), T('02', 'Y aquí el partido'), 'Ronda 2', 'Copa América', 'El torneo de selecciones más antiguo')
CAM(T('02', 'Y aquí el partido', d=-.3), 'medio'); marcador(T('02', 'Argentina tiene dieciséis'), T('02', 'Y hay una final'), 'Ronda 2 · Copa América', 16, 9)
CAM(T('02', 'Y hay una final', d=-.3), 'rio'); tarjeta('maracana-1.jpg', T('02', 'Y hay una final'), T('02', 'Gol de Di María'), RIO, '2021 · Final en el Maracaná')
foto('dimaria-1.jpg', T('02', 'Gol de Di María'), T('02', 'Era el primer'), px=1); ficha(T('02', 'Gol de Di María') + .2, T('02', 'Era el primer') - .1, 'Final Copa América 2021', 'Di María · 1 - 0')
foto('hinchas-arg-1.jpg', T('02', 'Era el primer'), T('02', 'Dieciséis contra nueve')); ficha(T('02', 'Era el primer') + .2, T('02', 'Dieciséis contra nueve') - .1, '2021', 'Primer título de Messi', 'En la casa del rival')
barrido(T('02', 'Dieciséis contra nueve')); CAM(T('02', 'Dieciséis contra nueve', d=-.2), 'medio')
gol(T('02', 'Gol de Argentina'), 'ARG', 'Argentina · 16 Copas América', 'argentina-2022-1.jpg')

# ===================== voz-03 · Ronda 3 =====================
ficha(INI('03'), T('03', 'Según la FIFA'), 'Ronda 3', 'Cara a cara', '¿Quién gana más cuando se enfrentan?')
CAM(INI('03'), 'medio'); marcador(T('03', 'Según la FIFA'), T('03', 'Un solo partido'), 'Ronda 3 · Historial (111 partidos)', 43, 42)
ficha(T('03', 'Un solo partido'), T('03', 'Porque esto empezó'), '26 empates', 'Un solo partido de diferencia')
foto('monumental-2.jpg', T('03', 'Porque esto empezó'), T('03', 'Hay fuentes')); ficha(T('03', 'Porque esto empezó') + .2, T('03', 'Hay fuentes') - .1, 'Desde 1914', 'Copa Roca', 'Un trofeo creado solo para este clásico')
barrido(T('03', 'Hay fuentes')); C('var', T('03', 'Así que esta va'), T('03', 'Gol de Argentina'), texto='Historial', veredicto='Confirmado: 43 - 42', ok=True)
gol(T('03', 'Gol de Argentina'), 'ARG', 'Argentina · 43 a 42', 'hinchas-arg-1.jpg')

# ===================== voz-04 · Ronda 4 =====================
ficha(INI('04'), T('04', 'Argentina llegó'), 'Ronda 4', 'Mundial 2026', 'Estados Unidos, México y Canadá')
foto('espana-2026-2.jpg', T('04', 'Argentina llegó'), T('04', 'Brasil se quedó')); ficha(T('04', 'Argentina llegó') + .2, T('04', 'Brasil se quedó') - .1, '19 de julio de 2026', 'Subcampeona', 'Perdió 1 - 0 con España en el tiempo extra')
barrido(T('04', 'Brasil se quedó')); CAM(T('04', 'Brasil se quedó', d=-.2), 'bra')
tarjeta('haaland-2.jpg', T('04', 'Brasil se quedó'), T('04', 'Y Argentina llegaba'), BRS, 'Octavos · Noruega 2 - 1 Brasil')
foto('argentina-2022-2.jpg', T('04', 'Y Argentina llegaba'), T('04', 'Final contra octavos')); ficha(T('04', 'Y Argentina llegaba') + .2, T('04', 'Final contra octavos') - .1, 'Catar 2022', 'Campeona del mundo', 'Ganó la final a Francia en penales')
barrido(T('04', 'Final contra octavos')); CAM(T('04', 'Final contra octavos', d=-.2), 'medio')
marcador(T('04', 'Final contra octavos'), T('04', 'Y gol de Argentina') - .2, 'Ronda 4 · Mundial 2026', 'FINAL', 'OCTAVOS', gana='izq', tam=90)
tarj.append(dict(pais='BRA', t=round(T('04', 'Tarjeta roja'), 2), color='roja', hasta=round(T('04', 'Pero antes'), 2)))
gol(T('04', 'Y gol de Argentina', d=.4), 'ARG', 'Argentina · finalista 2026', 'argentina-2022-1.jpg')
CAM(T('04', 'Pero antes', d=-.2), 'medio'); C('var', T('04', 'Pero antes'), FIN('04') + .3, texto='El mejor de la historia')

# ===================== voz-05 · VAR de leyendas y entretiempo =====================
foto('pele-1.jpg', INI('05'), T('05', 'Argentina tiene a Maradona')); ficha(INI('05') + .2, T('05', 'Argentina tiene a Maradona') - .1, 'Brasil', 'Pelé · El Rey', '3 Copas del Mundo · más de mil goles')
foto('maradona-inglaterra-1.jpg', T('05', 'Argentina tiene a Maradona'), T('05', 'y el gol más bonito')); ficha(T('05', 'Argentina tiene a Maradona') + .2, T('05', 'y el gol más bonito') - .1, 'México 1986 · contra Inglaterra', 'Maradona', 'La mano de Dios')
foto('maradona-inglaterra-2.jpg', T('05', 'y el gol más bonito'), T('05', 'Y tiene a Messi'), z0=1.0, z1=1.08); ficha(T('05', 'y el gol más bonito') + .2, T('05', 'Y tiene a Messi') - .1, 'El mismo partido', 'El gol del siglo')
foto('messi-2026-2.jpg', T('05', 'Y tiene a Messi'), T('05', 'El VAR revisa'), px=1); ficha(T('05', 'Y tiene a Messi') + .2, T('05', 'El VAR revisa') - .1, 'Argentina', 'Messi', '8 Balones de Oro · mejor jugador de Catar 2022')
barrido(T('05', 'El VAR revisa')); CAM(T('05', 'El VAR revisa', d=-.2), 'medio')
C('var', T('05', 'El VAR revisa'), T('05', 'Minuto cuarenta'), texto='Pelé, Maradona o Messi', veredicto='Deciden los comentarios', ok=True)
ficha(T('05', 'Minuto cuarenta'), T('05', 'Y aquí viene'), "Minuto 45'", 'Entretiempo', 'Argentina 3 - 1 Brasil', tam=96)
C('adelanto', T('05', 'Y aquí viene'), T('05', 'Premios Nobel'), minuto="45'", kicker='Lo prometido', texto='El dato que nadie conoce', y=900)
CAM(T('05', 'Premios Nobel', d=-.4), 'norte')
nob = [('Carlos Saavedra', 'saavedra-lamas-1.jpg', 'Saavedra Lamas · Paz 1936'), ('Bernardo Houssay', 'houssay-2.jpg', 'Houssay · Medicina 1947'), ('Luis Federico', 'leloir-1.jpg', 'Leloir · Química 1970'), ('Adolfo Pérez', 'perez-esquivel-1.jpg', 'Pérez Esquivel · Paz 1980'), ('Y César Milstein', 'milstein-anticuerpo.jpg', 'Milstein · Medicina 1984 · anticuerpos monoclonales')]
for i, (fr, img, tx) in enumerate(nob):
    a = T('05', fr); b = T('05', nob[i + 1][0]) if i + 1 < len(nob) else T('05', 'Brasil, el país')
    pant.append(dict(desde=round(a, 2), hasta=round(b, 2), img=F(img), texto=tx))
ficha(T('05', 'Premios Nobel'), T('05', 'Carlos Saavedra') - .1, 'Entretiempo', 'Premios Nobel')
CAM(T('05', 'Brasil, el país', d=-.3), 'medio'); marcador(T('05', 'Brasil, el país'), T('05', 'Gol de Argentina') - .2, 'Premios Nobel', 5, 0)
gol(T('05', 'Gol de Argentina'), 'ARG', 'Argentina · 5 Nobel', 'hinchas-arg-1.jpg')
ficha(T('05', 'Pero ojo'), FIN('05') + .3, 'Ojo', 'El segundo tiempo es de Brasil')

# ===================== voz-06 · tamaño, gente, dinero =====================
ficha(INI('06'), T('06', 'Brasil mide'), 'Segundo tiempo · Ronda 6', 'El tamaño'); CAM(INI('06'), 'medio')
marcador(T('06', 'Brasil mide'), T('06', 'Es el quinto'), 'Ronda 6 · Superficie (km²)', 2780400, 8515767)
ficha(T('06', 'Es el quinto'), T('06', 'Si pones Argentina'), 'Ranking mundial', 'Brasil 5.º · Argentina 8.º')
CAM(T('06', 'Si pones Argentina', d=-.3), 'bra'); ficha(T('06', 'Si pones Argentina'), T('06', 'Argentina tiene su propio'), 'Cabe 3 veces', 'Frontera con todos', 'Menos con Chile y Ecuador')
foto('aconcagua-2.jpg', T('06', 'Argentina tiene su propio'), T('06', 'Gol de Brasil')); ficha(T('06', 'Argentina tiene su propio') + .2, T('06', 'Gol de Brasil') - .1, 'Mendoza · 6,961 m', 'Aconcagua', 'La montaña más alta fuera de Asia')
barrido(T('06', 'Gol de Brasil', d=-1.4)); gol(T('06', 'Gol de Brasil'), 'BRA', 'Brasil · 3 veces más grande', 'torcida-bra-2.jpg')
ficha(T('06', 'Ronda siete'), T('06', 'Por cada argentino'), 'Ronda 7', 'La gente', 'Censos 2022'); CAM(T('06', 'Ronda siete'), 'medio')
marcador(T('06', 'Por cada argentino', d=-2.5), T('06', 'Solo la ciudad'), 'Ronda 7 · Habitantes (millones)', 46, 203)
foto('sao-paulo-1.jpg', T('06', 'Solo la ciudad'), T('06', 'Gol de Brasil', 2, -1.3)); ficha(T('06', 'Solo la ciudad') + .2, T('06', 'Gol de Brasil', 2, -1.4), 'Más de 11 millones', 'São Paulo', 'Casi un cuarto de Argentina en una ciudad')
barrido(T('06', 'Gol de Brasil', 2, -1.3)); gol(T('06', 'Gol de Brasil', 2), 'BRA', 'Brasil · 203 millones', 'torcida-bra-1.jpg')
ficha(T('06', 'Ronda ocho'), T('06', 'Es una de las diez'), 'Ronda 8', 'El dinero', 'Tamaño de la economía'); CAM(T('06', 'Ronda ocho'), 'medio')
marcador(T('06', 'La economía de Brasil'), T('06', 'Pero aquí hay'), 'Ronda 8 · Economía total', '1x', '3x', gana='der')
ficha(T('06', 'Pero aquí hay'), T('06', 'Y cada uno'), 'Pero por habitante', 'Gana Argentina', 'El argentino promedio queda por encima')
CAM(T('06', 'Y cada uno', d=-.3), 'sp'); tarjeta('cafe-brasil-2.jpg', T('06', 'Brasil es el mayor'), T('06', 'Argentina es famosa'), SP, 'Brasil · Café y soya')
CAM(T('06', 'Argentina es famosa', d=-.3), 'mza'); tarjeta('vinedo-2.jpg', T('06', 'Argentina es famosa'), T('06', 'El VAR mira'), MZA, 'Argentina · Carne y vino', rot=2)
CAM(T('06', 'El VAR mira', d=-.2), 'medio'); C('var', T('06', 'El VAR mira'), T('06', 'Gol de Brasil', 3, -1.2), texto='Economía', veredicto='Cuenta el total', ok=True)
gol(T('06', 'Gol de Brasil', 3), 'BRA', 'Brasil · economía 3 veces mayor', 'torcida-bra-2.jpg')
ficha(T('06', 'Empate'), FIN('06') + .4, 'Segundo tiempo', 'Cuatro a cuatro', 'Empate', tam=90)

# ===================== voz-07 · Fórmula 1 y cine =====================
ficha(INI('07'), T('07', 'Argentina tiene a Juan'), 'Ronda 9', 'Fórmula 1', 'La velocidad')
foto('fangio-1.jpg', T('07', 'Argentina tiene a Juan'), T('07', 'Pero Brasil tiene'), z0=1.0, z1=1.08); ficha(T('07', 'Argentina tiene a Juan') + .2, T('07', 'Pero Brasil tiene') - .1, 'Argentina · años 50', 'Fangio', '5 campeonatos del mundo')
foto('fittipaldi-2.jpg', T('07', 'Emerson Fittipaldi'), T('07', 'Nelson Piquet')); ficha(T('07', 'Emerson Fittipaldi') + .2, T('07', 'Nelson Piquet') - .1, 'Brasil · 2 títulos', 'Emerson Fittipaldi')
foto('piquet-2.jpg', T('07', 'Nelson Piquet'), T('07', 'Y Ayrton Senna'), px=1); ficha(T('07', 'Nelson Piquet') + .2, T('07', 'Y Ayrton Senna') - .1, 'Brasil · 3 títulos', 'Nelson Piquet')
foto('senna-mclaren-2.jpg', T('07', 'Y Ayrton Senna'), T('07', 'Senna, además'), px=-1); ficha(T('07', 'Y Ayrton Senna') + .2, T('07', 'Senna, además') - .1, 'Brasil · 3 títulos', 'Ayrton Senna')
foto('senna-1.jpg', T('07', 'Senna, además'), T('07', 'Y el récord')); ficha(T('07', 'Senna, además') + .2, T('07', 'Y el récord') - .1, '1960 - 1994', 'Una leyenda', 'Más allá del deporte')
foto('fangio-2.jpg', T('07', 'Y el récord'), T('07', 'Ocho contra cinco')); ficha(T('07', 'Y el récord') + .2, T('07', 'Ocho contra cinco') - .1, 'Fangio', 'Su récord duró casi medio siglo')
barrido(T('07', 'Ocho contra cinco')); CAM(T('07', 'Ocho contra cinco', d=-.2), 'medio'); marcador(T('07', 'Ocho contra cinco'), T('07', 'Gol de Brasil') - .2, 'Ronda 9 · Títulos de F1', 5, 8)
gol(T('07', 'Gol de Brasil'), 'BRA', 'Brasil · 8 títulos de F1', 'torcida-bra-1.jpg')
ficha(T('07', 'Ronda diez'), T('07', 'Brasil ganó el primero'), 'Ronda 10 · la última', 'El cine', 'Óscar a mejor película internacional')
foto('fernanda-torres-2.jpg', T('07', 'Brasil ganó el primero'), T('07', 'Argentina tiene dos')); ficha(T('07', 'Brasil ganó el primero') + .2, T('07', 'Argentina tiene dos') - .1, 'Brasil · 2025', 'Ainda Estou Aqui', 'Fernanda Torres · dirige Walter Salles')
foto('campanella-1.jpg', T('07', 'Argentina tiene dos'), T('07', 'Dos películas')); ficha(T('07', 'Argentina tiene dos') + .2, T('07', 'Dos películas') - .1, 'Argentina · 1986 y 2010', 'La historia oficial', 'El secreto de sus ojos · Juan José Campanella')
barrido(T('07', 'Dos películas')); CAM(T('07', 'Dos películas', d=-.2), 'medio'); marcador(T('07', 'Dos películas'), T('07', 'Gol de Argentina') - .2, 'Ronda 10 · Óscar', 2, 1)
gol(T('07', 'Gol de Argentina'), 'ARG', 'Argentina · 2 Óscar', 'argentina-2022-1.jpg')

# ===================== voz-08 · penales y cierre =====================
C('marcador', INI('08'), T('08', 'Repasemos'), titulo='Final · 90 minutos', isoIzq='ar', isoDer='br', nomIzq='Argentina', nomDer='Brasil', izq=5, der=5, y=930, tam=130)
ficha(T('08', 'Repasemos'), T('08', 'Argentina ganó'), 'Brasil ganó en', 'Mundiales · tamaño · gente · economía · F1', tam=60)
ficha(T('08', 'Argentina ganó'), T('08', 'Así que esto'), 'Argentina ganó en', 'Copa América · historial · 2026 · Nobel · Óscar', tam=60)
ficha(T('08', 'Así que esto'), T('08', 'Primer penal'), 'Empate', 'Penales', 'Los patean ustedes', tam=96)
CAM(T('08', 'Primer penal', d=-.3), 'arg'); tarjeta('asado-1.jpg', T('08', 'Primer penal'), T('08', 'o el churrasco'), BA, 'Penal 1 · El asado argentino')
CAM(T('08', 'o el churrasco', d=-.3), 'bra'); tarjeta('picanha-1.jpg', T('08', 'o el churrasco'), T('08', 'Segundo penal'), BRS, 'Penal 1 · El churrasco brasileño', rot=2)
foto('tango-baile-1.jpg', T('08', 'Segundo penal'), T('08', 'O la samba')); ficha(T('08', 'Segundo penal') + .2, T('08', 'O la samba') - .1, 'Penal 2 · la música', 'El tango', 'Patrimonio de la humanidad (UNESCO)')
foto('samba-rio-1.jpg', T('08', 'O la samba'), T('08', 'Tercer penal')); ficha(T('08', 'O la samba') + .2, T('08', 'Tercer penal') - .1, 'Penal 2 · la música', 'La samba', 'También patrimonio de la UNESCO')
foto('argentina-2022-1.jpg', T('08', 'Tercer penal'), T('08', 'o el carnaval')); ficha(T('08', 'Tercer penal') + .2, T('08', 'o el carnaval') - .1, 'Penal 3 · la fiesta', 'La hinchada argentina')
foto('carnaval-rio-2.jpg', T('08', 'o el carnaval'), T('08', 'Cuarto penal')); ficha(T('08', 'o el carnaval') + .2, T('08', 'Cuarto penal') - .1, 'Penal 3 · la fiesta', 'El carnaval de Río')
foto('pele-1970-1.jpg', T('08', 'Cuarto penal'), T('08', 'Y el quinto')); ficha(T('08', 'Cuarto penal') + .2, T('08', 'Y el quinto') - .1, 'Penal 4 · la leyenda', '¿Pelé, Maradona o Messi?')
barrido(T('08', 'Y el quinto')); CAM(T('08', 'Y el quinto', d=-.2), 'ancho', 1.4)
C('marcador', T('08', 'Y el quinto'), T('08', 'Y si quieres'), titulo='Penal 5 · ¿Quién gana para ti?', isoIzq='ar', isoDer='br', nomIzq='Argentina', nomDer='Brasil', izq='?', der='?', y=930, tam=130)
pant.append(dict(desde=round(T('08', 'Escríbelo'), 2), hasta=round(T('08', 'Y si quieres'), 2), img=F('hinchas-arg-1.jpg'), texto='Comenta: ARGENTINA o BRASIL'))
C('adelanto', T('08', 'Escríbelo'), T('08', 'Y si quieres'), minuto='VOTA', kicker='Los penales los patean ustedes', texto='Comenta: ARGENTINA o BRASIL', y=650)
CAM(T('08', 'Y si quieres', d=-.2), 'medio', 1.6); ficha(T('08', 'Y si quieres'), DUR, 'Próximo clásico', 'México vs Colombia', '¿O Perú vs Chile? Suscríbete y comenta', tam=90)

# ===================== ensamblado =====================
fichas = sorted([c for c in capas if c['tipo'] == 'ficha'], key=lambda c: c['desde'])
for a, b in zip(fichas, fichas[1:]):
    if a['hasta'] > b['desde'] - .05: a['hasta'] = round(b['desde'] - .05, 2)
cam.sort(key=lambda k: k['t'])
for i in range(1, len(cam)):
    if cam[i]['t'] <= cam[i - 1]['t']: cam[i]['t'] = round(cam[i - 1]['t'] + .03, 2)
orden = {'foto': 0, 'barrido': 9}
spec = dict(salida='argentina-vs-brasil', duracion=DUR, ancho=1920, alto=1080, centro=[-58, -20], mar='#0d2a4f', cielo='#061630', entorno='mundo', contexto=[-130, -60, 25, 40],
            calidad3d=.85, sombra=1536,
            paises=[dict(adm=k, iso=v, alto=3.4 if k in ('BRA', 'ARG') else 2.2) for k, v in ISO.items()],
            estadio=dict(t=round(TE, 2), dur=1.6), camara=cam,
            caras={'*': [[0, 'normal']], 'ARG': [[0, 'normal']] + [[g['t'] + 1, 'feliz'] for g in goles if g['pais'] == 'ARG'] + [[g['t'] + 1, 'duda'] for g in goles if g['pais'] == 'BRA'],
                   'BRA': [[0, 'normal']] + [[g['t'] + 1, 'feliz'] for g in goles if g['pais'] == 'BRA'] + [[g['t'] + 1, 'duda'] for g in goles if g['pais'] == 'ARG']},
            atenuar=[dict(desde=3.5, hasta=9999, paises=['ARG', 'BRA'])], elevar=[dict(pais='ARG', desde=4.0, altura=6), dict(pais='BRA', desde=4.2, altura=6)],
            goles=goles, tarjetas3d=tarj, pantalla=pant, reloj=dict(desde=round(TE + .4, 2), hasta=FIN('07'), isoIzq='ar', isoDer='br'),
            capas=sorted(capas, key=lambda c: (c['desde'], orden.get(c['tipo'], 5))), audio='.tmp/voz.wav')
for k in ('ARG', 'BRA'): spec['caras'][k].sort(key=lambda x: x[0])
(DIR / 'escena.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'Video 008 · {DUR:.1f} s · {len(capas)} capas · {len(goles)} goles · {len(cam)} claves de cámara')
