"""Arma mapa.json del video 002 a partir del guion y (si existen) de los audios voz/voz-01..07.mp3.

Cada capa se ata a una frase del guion: aparece cuando la voz dice esa frase.
Sin audios usa tiempos estimados; con audios mide cada bloque y ancla las pausas reales.

    python3 videos-largos/002-sin-paises-hispanos/construir.py
    node motor-mapa/render.cjs videos-largos/002-sin-paises-hispanos
"""
import json, re, subprocess, sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
GUION = (DIR / '02-GUION-ELEVENLABS.md').read_text(encoding='utf-8')
BLOQUES = re.findall(r'```\n(.*?)```', GUION, re.S)
assert len(BLOQUES) == 7
INICIO, GAP, CPS = 0.6, 0.45, 14.5     # silencio inicial, pausa entre bloques, caracteres por segundo estimados


def segmentos(b):
    """[(texto, pausa_despues)] del bloque."""
    partes = re.split(r'<break time="([\d.]+)s" />', b)
    out = []
    for i in range(0, len(partes), 2):
        txt = ' '.join(partes[i].split())
        pausa = float(partes[i + 1]) if i + 1 < len(partes) else 0
        out.append((txt, pausa))
    return out


def silencios(audio):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(audio), '-af', 'silencedetect=noise=-35dB:d=0.3', '-f', 'null', '-'], capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r)]
    fin = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r)]
    return list(zip(ini, fin))


def duracion(audio):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(audio)], capture_output=True, text=True).stdout)


class Bloque:
    def __init__(self, n, texto, t0):
        self.n, self.segs = n, segmentos(texto)
        self.texto = ' '.join(s for s, _ in self.segs)
        audio = DIR / 'voz' / f'voz-{n:02d}.mp3'
        est = [len(s) / CPS for s, _ in self.segs]
        if audio.exists():
            self.audio, self.dur = audio, duracion(audio)
            sil = silencios(audio)
            # ancla: final de cada segmento hablado = inicio del silencio que mejor encaja con lo esperado
            total_est = sum(est) + sum(p for _, p in self.segs)
            esc = self.dur / total_est
            # DP: elegir un silencio por cada pausa del guion para que cada tramo dure lo esperado según su texto
            m, n = len(self.segs) - 1, len(sil)
            PS = 0.6   # pausa típica entre oraciones dentro de un tramo
            internas = [len(re.findall(r'[.?!…:](?=\s)', s_)) for s_, _ in self.segs]
            habla = self.dur - sum(p_ for _, p_ in self.segs) - PS * sum(internas)
            cps = sum(len(s_) for s_, _ in self.segs) / max(1, habla)
            exp = [len(s_) / cps + PS * k for (s_, _), k in zip(self.segs, internas)]
            def costo(i, a, b, kb=None):
                d = b - a; e = exp[i]
                return ((d - e) / (0.12 * e + 0.6)) ** 2 - (1.5 * (sil[kb][1] - sil[kb][0]) if kb is not None else 0)
            INF = float('inf'); anclas = []
            if m and n >= m:
                dp = [[INF] * n for _ in range(m)]; ant = [[-1] * n for _ in range(m)]
                for k in range(n): dp[0][k] = costo(0, 0, sil[k][0], k)
                for i in range(1, m):
                    for k in range(i, n):
                        for k2 in range(i - 1, k):
                            v = dp[i - 1][k2] + costo(i, sil[k2][1], sil[k][0], k)
                            if v < dp[i][k]: dp[i][k], ant[i][k] = v, k2
                k = min(range(n), key=lambda k: dp[m - 1][k] + costo(m, sil[k][1], self.dur)); idx = []
                for i in range(m - 1, -1, -1): idx.append(k); k = ant[i][k]
                anclas = [sil[k] for k in reversed(idx)]
            elif m:
                t_ = 0
                for e_, (_, p_) in zip(exp, self.segs): t_ += e_; anclas.append((t_, t_ + p_)); t_ += p_
            self.tramos, t = [], 0.0
            for i, (s, _) in enumerate(self.segs):
                fin = anclas[i][0] if i < len(anclas) else self.dur
                self.tramos.append((t, max(t + .1, fin)))
                t = anclas[i][1] if i < len(anclas) else self.dur
        else:
            self.audio = None
            self.tramos, t = [], 0.0
            for (s, p), e in zip(self.segs, est):
                self.tramos.append((t, t + e)); t += e + p
            self.dur = t + .2
        self.t0 = t0

    def T(self, frase, k=1, d=0.0):
        """Tiempo absoluto en que la voz dice `frase` (k-ésima aparición) más d segundos."""
        idx = -1
        for _ in range(k):
            idx = self.texto.find(frase, idx + 1)
            if idx < 0: sys.exit(f'No encuentro «{frase}» en el bloque {self.n}')
        acc = 0
        for (s, _), (a, b) in zip(self.segs, self.tramos):
            if idx <= acc + len(s):
                return round(self.t0 + a + (b - a) * (idx - acc) / max(1, len(s)) + d, 2)
            acc += len(s) + 1
        return round(self.t0 + self.dur + d, 2)

    @property
    def fin(self): return self.t0 + self.dur


B, t = [], INICIO
for i, txt in enumerate(BLOQUES, 1):
    b = Bloque(i, txt, t); B.append(b); t = b.fin + GAP
DUR = round(B[-1].fin + 3.0, 2)
b1, b2, b3, b4, b5, b6, b7 = B

# ---------------------------------------------------------------- datos fijos
HISP = ['MEX', 'GTM', 'SLV', 'HND', 'NIC', 'CRI', 'PAN', 'CUB', 'DOM', 'PRI', 'COL', 'VEN', 'ECU', 'PER', 'BOL', 'CHL', 'ARG', 'PRY', 'URY', 'ESP', 'GNQ']
CA, SA, CAR = ['GTM', 'SLV', 'HND', 'NIC', 'CRI', 'PAN'], ['COL', 'VEN', 'ECU', 'PER', 'BOL', 'CHL', 'ARG', 'PRY', 'URY'], ['CUB', 'DOM', 'PRI']
cam, ev, caras, mirar = [], [], {'*': [[0, 'normal']]}, []


def C(t, lon, lat, ancho, **kw): cam.append(dict(t=round(t, 2), lon=lon, lat=lat, ancho=ancho, **kw))
def E(tipo, desde, dur=None, hasta=None, **kw):
    e = dict(tipo=tipo, desde=round(desde, 2), **kw)
    if hasta is not None: e['hasta'] = round(hasta, 2)
    elif dur is not None: e['hasta'] = round(desde + dur, 2)
    ev.append(e); return e
def cara(pais, t, ex): caras.setdefault(pais, []).append([round(t, 2), ex])
def lista(iso, nombre, estado, t): E('lista', t, iso=iso, nombre=nombre, estado=estado)


# ---------------------------------------------------------------- 1 · gancho
C(0, -45, 18, 235)
C(b1.T('Mira este mapa', d=1.2), -48, 18, 225, suave=False)
C(b1.T('borra a México'), -101, 23, 44)
E('marcar', b1.T('borra a México'), paises=['MEX'], hasta=b1.T('Uno.', d=.1))
C(b1.T('Borra a Centroamérica'), -86, 14, 30)
E('marcar', b1.T('Borra a Centroamérica'), paises=CA, hasta=b1.T('Uno.', d=.1))
C(b1.T('Borra casi toda Sudamérica'), -62, -20, 72)
E('marcar', b1.T('Borra casi toda Sudamérica'), paises=SA, hasta=b1.T('Uno.', d=.1))
C(b1.T('Borra a Cuba'), -73, 19.5, 24)
E('marcar', b1.T('Borra a Cuba'), paises=CAR, hasta=b1.T('Uno.', d=.1))
C(b1.T('borra a España'), -4, 40, 26, arco=.8)
E('marcar', b1.T('borra a España'), paises=['ESP'], hasta=b1.T('Uno.', d=.1))
C(b1.T('y a un pequeño país'), 10, 2.5, 26, arco=.4)
E('marcar', b1.T('y a un pequeño país'), paises=['GNQ'], hasta=b1.T('Uno.', d=.1))
E('nombre', b1.T('casi nadie recuerda'), texto='GUINEA ECUATORIAL', lon=10.4, lat=4.2, dur=2.4)
for grupo, frase in [(['MEX'], 'borra a México'), (CA, 'Borra a Centroamérica'), (SA, 'Borra casi toda Sudamérica'), (CAR, 'Borra a Cuba'), (['ESP'], 'borra a España'), (['GNQ'], 'y a un pequeño país')]:
    for p in grupo: cara(p, b1.T(frase, d=.3), 'shock')
C(b1.T('Son veintiún territorios'), -40, 14, 265, arco=.3)
E('cifra', b1.T('Son veintiún territorios'), texto='21', sub='TERRITORIOS', hasta=b1.T('Unos doce millones'))
E('cifra', b1.T('Unos doce millones'), texto='12 MILLONES DE km²', tam=104, sub='más que Canadá entero', hasta=b1.T('Y cerca de cuatrocientos'))
E('resaltar', b1.T('más que Canadá'), pais='CAN', hasta=b1.T('Y cerca de cuatrocientos', d=.5))
E('cifra', b1.T('Y cerca de cuatrocientos'), texto='460 MILLONES', tam=118, sub='de hablantes nativos de español', fuente='Instituto Cervantes, 2025', hasta=b1.T('Hoy vamos'))
C(b1.T('Hoy vamos'), -42, 14, 250, suave=False)
E('titulo', b1.T('Hoy vamos'), texto='¿QUÉ PASARÍA SI DESAPARECIERAN\nTODOS LOS PAÍSES QUE\nHABLAN *ESPAÑOL*?', tam=84, y=300, hasta=b1.T('Las reglas son simples'))
E('reglas', b1.T('Las reglas son simples'), titulo='LAS REGLAS', y=250, paso=2.2,
  lineas=['Los 21 territorios desaparecen', 'El mar ocupa su lugar', 'La gente que vive fuera se queda', 'Todo lo demás: datos reales'], hasta=b1.T('Te adelanto algo'))
E('iconos', b1.T('se quedarían sin café'), y=420, paso=.55, items=[dict(icono='cafe', texto='CAFÉ'), dict(icono='cobre', texto='COBRE'), dict(icono='aguacate', texto='AGUACATES'), dict(icono='casa', texto='VECINOS')], hasta=b1.T('Y al final'))
E('titulo', b1.T('Y al final'), texto='¿EL NUEVO HOGAR\nDEL *ESPAÑOL*?', tam=88, y=360, hasta=b1.T('Tres.'))
C(b1.T('Tres.'), -40, 12, 255, suave=False)
for i, n in enumerate(['3', '2', '1']):
    frase = ['Tres.', 'Dos.', 'Uno.'][i]
    E('cifra', b1.T(frase), texto=n, tam=230, color='#ffffff', hasta=b1.T(frase, d=.85 if n != '1' else .7))
T_UNO = b1.T('Uno.', d=.35)
DESAP = [dict(iso=p, t=round(T_UNO + i * .06, 2)) for i, p in enumerate(HISP)]
sacud = [dict(t=round(T_UNO, 2), dur=.9, fuerza=16)]
cara('*', T_UNO + .4, 'shock')
cara('*', b2.t0 + 2.5, 'normal')
mirar.append(dict(t=0, lon=-70, lat=5))

# ---------------------------------------------------------------- 2 · Norteamérica
C(b2.t0, -97, 33, 58)
C(b2.T('Hay mar'), -103, 27, 36)
E('region', b2.t0, texto='NORTEAMÉRICA', hasta=b2.fin)
E('barra', b2.T('El primer golpe'), hasta=DUR)
E('marcador', b2.T('El primer golpe'), texto='EL MUNDO', hasta=DUR)
cara('USA', b2.t0 + .3, 'shock')
E('nombre', b2.T('Hay mar'), texto='AQUÍ ESTABA LA FRONTERA', lon=-103, lat=29.5, fantasma=True, dur=4)
E('pin', b2.T('San Diego'), lon=-117.16, lat=32.72, texto='SAN DIEGO', dur=4.5)
C(b2.T('El primer golpe'), -97, 33, 52)
E('flujo', b2.T('El primer golpe'), de=[-102, 22], a=[-98, 35.5], icono='aguacate', roto=True, n=5, hasta=b2.T('Después, las flores'))
E('globo', b2.T('casi nueve de cada diez'), pais='USA', texto='¿Y mi guacamole?', dur=3.6)
E('tarjeta', b2.T('casi nueve de cada diez'), iso='us', nombre='Estados Unidos', estado='LLORA', dato='CASI 9 DE CADA 10', texto='aguacates que importa Estados Unidos vienen de México.', fuente='Departamento de Agricultura de EE. UU.', hasta=b2.T('Después, las flores'))
lista('us', 'Estados Unidos', 'LLORA', b2.T('casi nueve de cada diez', d=1))
cara('USA', b2.T('Adiós al guacamole'), 'llora')
C(b2.T('Después, las flores'), -88, 20, 75)
E('flujo', b2.T('Después, las flores'), de=[-74, 4.5], a=[-90, 34], icono='flor', roto=True, n=5, hasta=b2.T('Y el camarón'))
E('tarjeta', b2.T('Alrededor de dos de cada tres'), iso='us', nombre='Estados Unidos', estado='LLORA', dato='2 DE CADA 3', texto='flores que importa Estados Unidos vienen de Colombia.', fuente='Asocolflores', hasta=b2.T('Y el camarón'))
E('cinta', b2.T('el catorce de febrero'), pais='USA', texto='SAN VALENTÍN EN PELIGRO', icono='flor', dur=3.2)
E('flujo', b2.T('Y el camarón'), de=[-79.5, -1.5], a=[-92, 33], icono='camaron', roto=True, n=4, hasta=b2.T('Pero el golpe más fuerte'))
E('cinta', b2.T('Ecuador es hoy'), pais='USA', texto='ADIÓS AL CAMARÓN', icono='camaron', hasta=b2.T('Pero el golpe más fuerte'))
C(b2.T('Pero el golpe más fuerte'), -97, 38, 48)
E('cifra', b2.T('unos sesenta y ocho millones'), texto='68 MILLONES', tam=120, sub='de hispanos en EE. UU. · 1 de cada 5', fuente='Oficina del Censo de EE. UU., 2024', y=300, hasta=b2.T('Ellos no desaparecen'))
cara('USA', b2.T('Ellos no desaparecen'), 'triste')
E('iconos', b2.T('el país de sus padres'), y=330, paso=.9, items=[dict(icono='casa', texto='SUS PADRES'), dict(icono='corazon', texto='LOS DOMINGOS'), dict(icono='avion', texto='VOLVER')], hasta=b2.T('Canadá también'))
cara('USA', b2.T('el lugar al que pensaban volver'), 'llora')
C(b2.T('Canadá también'), -98, 54, 80)
cara('CAN', b2.T('Canadá también'), 'duda')
E('globo', b2.T('El tratado de comercio'), pais='CAN', texto='¿El T-MEC… sin la M?', dur=4)
E('cinta', b2.T('se queda con dos socios'), pais='CAN', texto='EL T-MEC SE QUEDA COJO', icono='alerta', color='#e0672a', hasta=b2.T('Y aparece algo'))
lista('ca', 'Canadá', 'LE AFECTA', b2.T('se queda con dos socios'))
C(b2.T('Y aparece algo'), -88.7, 17.3, 9)
E('resaltar', b2.T('Belice'), pais='BLZ', hasta=b2.fin)
cara('BLZ', b2.T('de pronto es una isla'), 'shock')
E('cinta', b2.T('de pronto es una isla'), pais='BLZ', texto='BELICE AHORA ES UNA ISLA', icono='alerta', dy=40, hasta=b2.fin)
E('globo', b2.T('Un país entero'), pais='BLZ', texto='¿Qué acaba de pasar?', hasta=b2.fin)
lista('bz', 'Belice', 'LE AFECTA', b2.T('de pronto es una isla', d=.8))
mirar.append(dict(t=b2.t0, lon=-102, lat=22))

# ---------------------------------------------------------------- 3 · Caribe y canal
E('region', b3.t0, texto='EL CARIBE', hasta=b3.T('Ahora mira Centroamérica'))
C(b3.t0, -73, 19.5, 16)
mirar.append(dict(t=b3.t0, lon=-70.5, lat=19))
E('nombre', b3.T('Cuba desaparece'), texto='CUBA', lon=-79, lat=21.8, fantasma=True, dur=3.5)
E('nombre', b3.T('República Dominicana desaparece'), texto='REP. DOMINICANA', lon=-70.3, lat=19.4, fantasma=True, dur=3.5)
E('resaltar', b3.T('Haití'), pais='HTI', hasta=b3.T('Puerto Rico'))
cara('HTI', b3.T('Haití'), 'shock')
E('cinta', b3.T('ahora tiene mar'), pais='HTI', texto='MEDIA ISLA, CERO VECINOS', icono='alerta', dy=30, hasta=b3.T('Puerto Rico'))
lista('ht', 'Haití', 'LE AFECTA', b3.T('ahora tiene mar'))
C(b3.T('Puerto Rico'), -67.5, 18.5, 12)
E('nombre', b3.T('Puerto Rico'), texto='PUERTO RICO', lon=-66.5, lat=18.2, fantasma=True, hasta=b3.T('Ahora mira Centroamérica'))
E('iconos', b3.T('millones de turistas'), y=330, items=[dict(icono='avion', texto='TURISTAS', tachado=True)], hasta=b3.T('Ahora mira Centroamérica'))
E('region', b3.T('Ahora mira Centroamérica'), texto='CENTROAMÉRICA', hasta=b3.T('El Caribe que sobrevive'))
C(b3.T('Ahora mira Centroamérica'), -85, 12.5, 26)
for i, (n, lo, la) in enumerate([('GUATEMALA', -90.3, 15.6), ('HONDURAS', -86.6, 14.8), ('EL SALVADOR', -88.9, 13.7), ('NICARAGUA', -85.2, 12.8), ('COSTA RICA', -84.1, 9.9), ('PANAMÁ', -80.1, 8.6)]):
    E('nombre', b3.T(n.title() if n != 'EL SALVADOR' else 'El Salvador', d=0) if n not in ('PANAMÁ',) else b3.T('Panamá', 1), texto=n, lon=lo, lat=la, fantasma=True, tam=24, hasta=b3.T('¿Te das cuenta'))
E('cinta', b3.T('Todo es agua'), x=960, y=200, texto='TODO ES AGUA', icono='alerta', hasta=b3.T('¿Te das cuenta', d=.5))
C(b3.T('¿Te das cuenta'), -80, 12, 40)
E('titulo', b3.T('el océano Atlántico'), texto='*ATLÁNTICO* + *PACÍFICO*', tam=80, y=210, hasta=b3.T('El Canal de Panamá'))
E('pin', b3.T('El Canal de Panamá'), lon=-79.7, lat=9.1, texto='AQUÍ ESTABA EL CANAL', hasta=b3.T('Suena a una buena noticia'))
E('sello', b3.T('ya no hace falta'), x=1350, y=320, texto='YA NO HACE FALTA', hasta=b3.T('Suena a una buena noticia'))
E('flujo', b3.T('Cualquier barco'), de=[-70, 15], a=[-92, 10], icono='barco', n=4, hasta=b3.T('no tienen dónde parar', d=1.5))
E('cinta', b3.T('los puertos de ese lado'), x=960, y=860, texto='PERO NO HAY PUERTOS', icono='barco', color='#e0672a', hasta=b3.T('El Caribe que sobrevive'))
C(b3.T('El Caribe que sobrevive'), -70, 17, 34)
E('region', b3.T('El Caribe que sobrevive'), texto='EL CARIBE QUE QUEDA', hasta=b3.T('Y el mapa de América'))
for n, lo, la, adm in [('JAMAICA', -77.3, 18.1, 'JAM'), ('BAHAMAS', -77.4, 24.3, 'BHS'), ('TRINIDAD Y TOBAGO', -61.3, 10.6, 'TTO'), ('ARUBA', -70, 12.5, 'ABW'), ('CURAZAO', -69, 12.2, 'CUW')]:
    E('nombre', b3.T(n.title() if n != 'TRINIDAD Y TOBAGO' else 'Trinidad y Tobago'), texto=n, lon=lo, lat=la + 1.1, tam=22, hasta=b3.T('Y el mapa de América'))
    cara(adm, b3.T('se quedan sin la mitad'), 'shock')
C(b3.T('Y el mapa de América'), -78, 8, 150)
mirar.append(dict(t=b3.T('Y el mapa de América'), lon=-70, lat=0))
E('titulo', b3.T('un hueco gigante'), texto='UN *HUECO* GIGANTE', tam=86, y=200, hasta=b3.fin)

# ---------------------------------------------------------------- 4 · Sudamérica
E('region', b4.t0, texto='SUDAMÉRICA', hasta=b4.fin)
C(b4.t0, -56, -10, 62)
mirar.append(dict(t=b4.t0, lon=-65, lat=-15))
cara('BRA', b4.t0 + .5, 'shock')
E('cifra', b4.T('Hoy Brasil'), texto='10 VECINOS', tam=110, sub='7 hablan español', y=260, hasta=b4.T('Al día siguiente'))
E('cifra', b4.T('Al día siguiente'), texto='3 VECINOS', tam=110, color='#ff6b5e', y=260, hasta=b4.T('Y Brasil gana algo'))
C(b4.T('Al día siguiente'), -55, -2, 45)
for adm, frase, n, lo, la in [('GUY', 'Guyana', 'GUYANA', -58.9, 5.2), ('SUR', 'Surinam', 'SURINAM', -55.9, 4.3), ('FRA', 'Francia', 'GUAYANA FRANCESA', -53.1, 3.6)]:
    E('resaltar', b4.T(frase), pais=adm, hasta=b4.T('Y Brasil gana algo'))
    E('nombre', b4.T(frase), texto=n, lon=lo, lat=la + 1.6, tam=22, hasta=b4.T('Y Brasil gana algo'))
    cara(adm, b4.T(frase), 'shock')
E('globo', b4.T('un país europeo'), pais='BRA', texto='¿Bonjour…?', dy=-20, hasta=b4.T('Y Brasil gana algo', d=.5))
C(b4.T('Y Brasil gana algo'), -62, -12, 55)
cara('BRA', b4.T('costa en el océano Pacífico'), 'feliz')
E('cinta', b4.T('costa en el océano Pacífico'), pais='BRA', texto='¡AHORA TENGO PACÍFICO!', icono='barco', color='#2e9e5b', dx=-120, hasta=b4.T('La selva amazónica'))
E('nombre', b4.T('Donde antes estaban'), texto='AQUÍ ESTABAN PERÚ Y BOLIVIA', lon=-72, lat=-13, fantasma=True, hasta=b4.T('La selva amazónica'))
cara('BRA', b4.T('La selva amazónica'), 'triste')
C(b4.T('Y los Andes'), -62, -22, 72)
E('nombre', b4.T('Y los Andes'), texto='AQUÍ ESTABAN LOS ANDES', lon=-71, lat=-25, fantasma=True, hasta=b4.T('Sería el Denali'))
E('cifra', b4.T('ya no sería el Aconcagua'), texto='6.961 m', tam=120, sub='Aconcagua: ya no existe', y=280, hasta=b4.T('Sería el Denali'))
C(b4.T('Sería el Denali'), -150, 62, 40, arco=1.2)
E('pin', b4.T('Sería el Denali', d=1.2), lon=-151.0, lat=63.07, texto='DENALI · 6.190 m', hasta=b4.T('Desaparecen las islas Galápagos'))
E('cinta', b4.T('Sería el Denali', d=1.8), x=960, y=230, texto='NUEVO TECHO DE AMÉRICA', icono='alerta', color='#2e9e5b', hasta=b4.T('Desaparecen las islas Galápagos'))
C(b4.T('Desaparecen las islas Galápagos'), -80, -15, 60, arco=1.0)
E('nombre', b4.T('Desaparecen las islas Galápagos', d=1), texto='GALÁPAGOS', lon=-90.5, lat=-0.6, fantasma=True, hasta=b4.T('Y las islas Malvinas'))
E('nombre', b4.T('el desierto de Atacama'), texto='ATACAMA', lon=-69.5, lat=-24, fantasma=True, hasta=b4.T('Y las islas Malvinas'))
E('nombre', b4.T('la Patagonia'), texto='PATAGONIA', lon=-69, lat=-45, fantasma=True, hasta=b4.T('Y las islas Malvinas'))
C(b4.T('Y las islas Malvinas'), -59.5, -51.7, 14)
E('resaltar', b4.T('Y las islas Malvinas'), pais='FLK', hasta=b4.T('El fútbol también'))
cara('FLK', b4.T('Y las islas Malvinas'), 'shock')
E('cinta', b4.T('se quedan flotando'), pais='FLK', texto='SOLAS EN EL ATLÁNTICO', icono='alerta', hasta=b4.T('El fútbol también'))
C(b4.T('El fútbol también'), -45, -15, 120)
E('iconos', b4.T('El fútbol también'), y=330, items=[dict(icono='futbol', texto='ARGENTINA ×3'), dict(icono='futbol', texto='URUGUAY ×2'), dict(icono='futbol', texto='ESPAÑA ×1')], gap=300, hasta=b4.T('Y con ellos'))
E('cifra', b4.T('al menos seis Copas'), texto='6 COPAS DEL MUNDO', tam=96, sub='desaparecen de golpe', fuente='FIFA', y=640, hasta=b4.T('Brasil mira'))
C(b4.T('Brasil mira'), -54, -11, 58)
cara('BRA', b4.T('Brasil mira'), 'llora')
E('globo', b4.T('Tiene más de doscientos'), pais='BRA', texto='¿Alguien quiere jugar?', hasta=b4.fin)
lista('br', 'Brasil', 'LLORA', b4.T('Brasil mira'))

# ---------------------------------------------------------------- 5 · lo que el mundo pierde
E('region', b5.t0, texto='EL MUNDO', hasta=b5.fin)
C(b5.t0, -20, 15, 330)
mirar.append(dict(t=b5.t0, lon=-65, lat=-5))
E('titulo', b5.t0 + .2, texto='LO QUE EL MUNDO\n*DEJA DE RECIBIR*', tam=86, y=220, hasta=b5.T('Empecemos por algo'))
E('iconos', b5.T('Tu teléfono tiene cobre'), y=300, items=[dict(icono='cobre', texto='COBRE')], hasta=b5.T('Chile y Perú juntos'))
E('flujo', b5.T('Chile y Perú juntos'), de=[-70, -25], a=[104, 34], icono='cobre', roto=True, n=5, hasta=b5.T('Hablando de autos'))
E('tarjeta', b5.T('Chile y Perú juntos'), iso='cl', nombre='Chile + Perú', estado='YA NO EXISTE', dato='MÁS DE 1 DE CADA 3', texto='toneladas de cobre que se extraen en el planeta.', fuente='USGS, Mineral Commodity Summaries 2026', hasta=b5.T('Hablando de autos'))
E('nombre', b5.T('Hablando de autos'), texto='TRIÁNGULO DEL LITIO', lon=-66, lat=-23, fantasma=True, hasta=b5.T('México es el primer'))
E('iconos', b5.T('el llamado triángulo'), y=300, items=[dict(icono='bateria', texto='LITIO')], hasta=b5.T('México es el primer'))
E('tarjeta', b5.T('Ahí está más de la mitad'), iso='ar', nombre='Argentina, Bolivia y Chile', estado='YA NO EXISTE', dato='MÁS DEL 50 %', texto='de los recursos de litio conocidos del mundo.', fuente='USGS', hasta=b5.T('México es el primer'))
E('tarjeta', b5.T('México es el primer'), iso='mx', nombre='México', estado='YA NO EXISTE', dato='1 DE CADA 5', texto='onzas de plata que se sacan de la tierra.', fuente='World Silver Survey 2026', hasta=b5.T('Y la comida'))
E('iconos', b5.T('México es el primer'), y=300, items=[dict(icono='plata', texto='PLATA')], hasta=b5.T('Y la comida'))
C(b5.T('Y la comida'), -30, 20, 230)
E('flujo', b5.T('Ecuador vende'), de=[-79, -1.5], a=[10, 50], icono='platano', roto=True, n=5, hasta=b5.T('¿Quién lo siente más?'))
E('tarjeta', b5.T('Ecuador vende'), iso='ec', nombre='Ecuador', estado='YA NO EXISTE', dato='CERCA DE 1 DE CADA 3', texto='bananos que se exportan en el mundo.', fuente='FAO', hasta=b5.T('Colombia, Honduras'))
E('iconos', b5.T('Colombia, Honduras'), y=300, paso=.3, items=[dict(icono='cafe', texto='COLOMBIA'), dict(icono='cafe', texto='HONDURAS'), dict(icono='cafe', texto='PERÚ'), dict(icono='cafe', texto='GUATEMALA')], hasta=b5.T('Y España produce'))
E('tarjeta', b5.T('Y España produce'), iso='es', nombre='España', estado='YA NO EXISTE', dato='45 %', texto='de todo el aceite de oliva del planeta.', fuente='Ministerio de Agricultura de España', hasta=b5.T('¿Quién lo siente más?'))
E('iconos', b5.T('Y España produce'), y=300, items=[dict(icono='aceite', texto='ACEITE DE OLIVA')], hasta=b5.T('¿Quién lo siente más?'))
C(b5.T('¿Quién lo siente más?'), 104, 35, 70, arco=.9)
cara('CHN', b5.T('China, el mayor'), 'shock')
E('globo', b5.T('China, el mayor'), pais='CHN', texto='¿Y mi cobre?', hasta=b5.T('Europa se queda'))
lista('cn', 'China', 'LLORA', b5.T('China, el mayor', d=1))
cara('CHN', b5.T('se le cierra'), 'llora')
C(b5.T('Europa se queda'), 10, 48, 45, arco=.6)
for p in ['DEU', 'FRA', 'ITA', 'GBR', 'POL', 'NLD', 'BEL']: cara(p, b5.T('Europa se queda'), 'triste')
E('cinta', b5.T('Europa se queda'), x=960, y=230, texto='SIN BANANO EN EL DESAYUNO', icono='platano', color='#e0672a', hasta=b5.T('Ningún país'))
E('iconos', b5.T('los cafés de medio planeta'), y=560, items=[dict(icono='cafe', texto='MENÚ NUEVO', tachado=True)], hasta=b5.T('Ningún país'))
C(b5.T('Ningún país'), -20, 15, 320)
E('titulo', b5.T('todo cuesta más'), texto='TODO *CUESTA MÁS*', tam=96, y=300, hasta=b5.fin)

# ---------------------------------------------------------------- 6 · Europa, África e idioma
E('region', b6.t0, texto='EUROPA', hasta=b6.T('En África'))
C(b6.t0, -5, 40, 24)
mirar.append(dict(t=b6.t0, lon=-4, lat=40))
for n, lo, la in [('CANARIAS', -15.6, 28.3), ('BALEARES', 2.9, 39.6), ('CEUTA', -5.3, 35.9), ('MELILLA', -2.9, 35.3)]:
    E('nombre', b6.T(n.title() if n != 'CANARIAS' else 'islas Canarias'), texto=n, lon=lo, lat=la + (.9 if n in ('CEUTA',) else 0), fantasma=True, tam=22, hasta=b6.T('Portugal, que solo'))
C(b6.T('islas Canarias'), -8, 36, 34)
C(b6.T('Portugal, que solo'), -6, 40.5, 16)
E('resaltar', b6.T('Portugal, que solo'), pais='PRT', hasta=b6.T('Andorra'))
cara('PRT', b6.T('se convierte en una isla'), 'shock')
E('cinta', b6.T('se convierte en una isla'), pais='PRT', texto='PORTUGAL AHORA ES UNA ISLA', icono='alerta', dx=60, hasta=b6.T('Andorra', d=.5))
lista('pt', 'Portugal', 'LLORA', b6.T('se convierte en una isla', d=1))
C(b6.T('Andorra'), 1.5, 42.6, 8)
E('resaltar', b6.T('Andorra'), pais='AND', hasta=b6.T('Francia gana'))
E('nombre', b6.T('de pronto tiene playa'), texto='ANDORRA: ¡PLAYA!', lon=1.55, lat=42.15, tam=26, hasta=b6.T('Y Gibraltar'))
cara('AND', b6.T('de pronto tiene playa'), 'feliz')
cara('FRA', b6.T('Francia gana'), 'feliz')
lista('fr', 'Francia', 'LE AFECTA', b6.T('Francia gana'))
C(b6.T('Y Gibraltar'), -5.35, 36.6, 6)
E('pin', b6.T('Y Gibraltar'), lon=-5.35, lat=36.14, texto='GIBRALTAR', hasta=b6.T('El turismo mundial'))
C(b6.T('El turismo mundial'), 8, 41, 40)
E('cifra', b6.T('España recibió'), texto='97 MILLONES', tam=120, sub='de turistas extranjeros en 2025', fuente='INE · Frontur', y=270, hasta=b6.T('En África'))
E('flujo', b6.T('Toda esa gente'), de=[-4, 40], a=[12.5, 42], icono='avion', n=3, hasta=b6.T('En África'))
E('flujo', b6.T('a Grecia'), de=[-4, 40], a=[22, 39], icono='avion', n=3, hasta=b6.T('En África'))
cara('ITA', b6.T('Toda esa gente'), 'feliz'); cara('GRC', b6.T('Toda esa gente'), 'feliz')
E('region', b6.T('En África'), texto='ÁFRICA', hasta=b6.T('Y se apagan'))
C(b6.T('En África'), 11, 2, 16, arco=.6)
E('nombre', b6.T('Guinea Ecuatorial'), texto='AQUÍ ESTABA GUINEA ECUATORIAL', lon=10.3, lat=1.6, fantasma=True, tam=22, hasta=b6.T('Y se apagan'))
E('resaltar', b6.T('Gabón y Camerún'), pais='GAB', hasta=b6.T('Y se apagan'))
E('resaltar', b6.T('Gabón y Camerún'), pais='CMR', hasta=b6.T('Y se apagan'))
cara('GAB', b6.T('Gabón y Camerún'), 'duda'); cara('CMR', b6.T('Gabón y Camerún'), 'duda')
lista('ga', 'Gabón', 'NI LO NOTA', b6.T('ni siquiera sabía ubicar'))
C(b6.T('Y se apagan'), -40, 15, 250)
E('iconos', b6.T('Y se apagan'), y=360, paso=.45, items=[dict(icono='nota', texto='TANGO'), dict(icono='nota', texto='FLAMENCO'), dict(icono='nota', texto='CUMBIA'), dict(icono='nota', texto='SON'), dict(icono='nota', texto='MARIACHI')], gap=250, hasta=b6.T('Y ahora, el giro'))
E('titulo', b6.T('Y ahora, el giro'), texto='EL GIRO:\n¿Y EL *IDIOMA*?', tam=100, y=320, hasta=b6.T('Según el Instituto'))
E('cifra', b6.T('Según el Instituto'), texto='520 MILLONES', tam=120, sub='de hablantes nativos de español', fuente='Instituto Cervantes, 2025', y=300, hasta=b6.T('En un segundo'))
E('cifra', b6.T('En un segundo'), texto='9 DE CADA 10', tam=130, color='#ff6b5e', sub='desaparecen con sus países', y=300, hasta=b6.T('Pero no muere'))
C(b6.T('Pero no muere'), -96, 37, 60, arco=.5)
mirar.append(dict(t=b6.T('Pero no muere'), lon=-97, lat=38))
E('cifra', b6.T('casi cuarenta y cinco millones'), texto='45 MILLONES', tam=120, sub='hablan español en casa en EE. UU.', fuente='Oficina del Censo, 2024', y=260, hasta=b6.T('Miami, Los Ángeles'))
cara('USA', b6.T('sería… Estados Unidos'), 'amor')
E('cinta', b6.T('sería… Estados Unidos'), pais='USA', texto='EL NUEVO HOGAR DEL ESPAÑOL', icono='libro', color='#2e9e5b', hasta=b6.fin)
for frase, n, lo, la in [('Miami', 'MIAMI', -80.19, 25.76), ('Los Ángeles', 'LOS ÁNGELES', -118.24, 34.05), ('Houston', 'HOUSTON', -95.37, 29.76), ('Nueva York', 'NUEVA YORK', -74.0, 40.71)]:
    E('pin', b6.T(frase), lon=lo, lat=la, texto=n, color='#ffd23f', hasta=b6.fin)

# ---------------------------------------------------------------- 7 · veredicto
E('region', b7.t0, texto='EL VEREDICTO', hasta=b7.fin)
C(b7.t0, -30, 18, 320)
mirar.append(dict(t=b7.t0, lon=-65, lat=0))
E('titulo', b7.t0 + .2, texto='¿QUIÉN LLORA Y\nQUIÉN *NI SE ENTERA*?', tam=88, y=240, hasta=b7.T('Lloran Estados Unidos'))
for p in ['USA', 'BRA', 'CHN', 'PRT']: cara(p, b7.T('Lloran Estados Unidos'), 'llora')
E('nombre', b7.T('Lloran Estados Unidos'), texto='LLORAN', lon=-98, lat=50, fondo='#4ea3ff', borde='#ffffff', tam=34, hasta=b7.T('Les afecta'))
for p in ['CAN', 'FRA']: cara(p, b7.T('Les afecta'), 'triste')
E('nombre', b7.T('Les afecta'), texto='LES AFECTA', lon=2, lat=55, fondo='#e0a400', borde='#ffffff', tam=34, hasta=b7.T('Y ni lo notan'))
C(b7.T('Y ni lo notan'), 85, 42, 85, arco=.6)
for p, frase in [('MNG', 'Mongolia'), ('NPL', 'Nepal'), ('KAZ', 'Kazajistán')]:
    cara(p, b7.T(frase), 'feliz')
lista('mn', 'Mongolia', 'NI LO NOTA', b7.T('Mongolia')); lista('np', 'Nepal', 'NI LO NOTA', b7.T('Nepal')); lista('kz', 'Kazajistán', 'NI LO NOTA', b7.T('Kazajistán'))
E('globo', b7.T('que siguen su vida'), pais='MNG', texto='¿Pasó algo?', hasta=b7.T('Volvamos al mapa'))
C(b7.T('Volvamos al mapa'), -45, 15, 240)
mirar.append(dict(t=b7.T('Volvamos al mapa'), lon=-70, lat=0))
E('iconos', b7.T('Es comida'), y=420, paso=.4, gap=220, items=[dict(icono='platano', texto='COMIDA'), dict(icono='cobre', texto='METALES'), dict(icono='nota', texto='MÚSICA'), dict(icono='futbol', texto='FÚTBOL'), dict(icono='libro', texto='IDIOMA')], hasta=b7.T('Ahora te toca'))
E('pregunta', b7.T('Ahora te toca'), texto='¿QUÉ EXTRAÑARÍA EL MUNDO DE TU PAÍS?', y=470, hasta=DUR)
E('cinta', b7.T('suscríbete'), x=960, y=640, texto='EL PRÓXIMO PAÍS LO ELIGES TÚ', icono='globo', color='#2e9e5b', hasta=DUR)
C(DUR, -48, 15, 225, suave=False)

# ---------------------------------------------------------------- salida
cam.sort(key=lambda k: k['t'])
for i in range(1, len(cam)):
    if cam[i]['t'] <= cam[i - 1]['t']: cam[i]['t'] = round(cam[i - 1]['t'] + .05, 2)
for k in caras.values(): k.sort()
spec = dict(estilo='caricatura', salida='que-pasaria-sin-paises-hispanos', duracion=DUR, camara=cam, desaparece=DESAP, sacudidas=sacud,
            tam={'USA': 1.2, 'BRA': 1.2, 'BLZ': 1.4, 'HTI': 1.3, 'PRT': 1.3, 'CHN': 1.1, 'FLK': 1.3, 'AND': 1.6}, mirar=mirar, caras=caras, eventos=sorted(ev, key=lambda e: e['desde']))
if any(b.audio for b in B):
    tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True)
    partes = []
    def silencio(seg, nombre):
        f = tmp / nombre; subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', f'{seg:.3f}', '-c:a', 'pcm_s16le', str(f)], check=True); return f
    t = 0.0
    for i, b in enumerate(B):
        partes.append(silencio(b.t0 - t, f's{i}.wav'))
        if b.audio:
            f = tmp / f'v{i}.wav'; subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(b.audio), '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le', str(f)], check=True)
        else:
            f = silencio(b.dur, f'v{i}.wav')
        partes.append(f)
        t = b.t0 + duracion(f)
    partes.append(silencio(DUR - t, 'sfin.wav'))
    (tmp / 'lista.txt').write_text(''.join(f"file '{p}'\n" for p in partes))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(tmp / 'lista.txt'), '-c:a', 'pcm_s16le', str(tmp / 'voz.wav')], check=True)
    spec['audio'] = '.tmp/voz.wav'
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print('bloques con voz:', [b.n for b in B if b.audio])
print(f"{len(ev)} capas · {len(cam)} posiciones de cámara · {DUR / 60:.1f} min · voz: {'sí' if spec.get('audio') else 'no (tiempos estimados)'}")
for b in B: print(f'  bloque {b.n}: {b.t0:7.1f} s  dura {b.dur:5.1f} s')
