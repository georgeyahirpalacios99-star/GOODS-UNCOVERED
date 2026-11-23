"""Video 004 · ¿Qué pasaría si BRASIL desapareciera? — arma mapa.json atado a cada frase de la voz.
    python3 videos-largos/004-brasil-desaparece/limpiar_voz.py   # una vez, con voz/parte-1..6.mp3
    python3 videos-largos/004-brasil-desaparece/construir.py
    node motor-mapa/render.cjs videos-largos/004-brasil-desaparece
Sin voz todavía, reparte el tiempo por letras (vista previa).
"""
import json, re, subprocess, sys
from pathlib import Path
DIR = Path(__file__).resolve().parent
BLOQUES = re.findall(r'```\n(.*?)```', (DIR / 'GUION-ELEVENLABS.md').read_text(encoding='utf-8'), re.S)[:6]
INICIO, GAP = 0.7, 0.4

def unidades(b):
    """Corta el texto en frases (punto, ¿?, ¡!, …, dos puntos) y en cada <break>: cada corte suele ser una pausa real."""
    t = ' '.join(re.sub(r'<break time="[\d.]+s" />', ' ¶ ', b).split())
    return [u for u in (x.strip(' ¶') for x in re.split(r'(?<=[.?!…:])\s+|\s*¶\s*', t)) if u]
def silencios(audio):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(audio), '-af', 'silencedetect=noise=-38dB:d=0.15', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return list(zip([float(x) for x in re.findall(r'silence_start: ([\d.]+)', r)], [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r)]))
def duracion(a): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(a)], capture_output=True, text=True).stdout)

class Bloque:
    """Alinea cada frase con su tramo de voz: programación dinámica que asigna a cada corte de frase un silencio real,
    comparando el tiempo HABLADO de cada frase (sin contar pausas internas) con lo esperado por su número de letras."""
    def __init__(self, n, texto, t0):
        self.n, self.t0 = n, t0; self.us = unidades(texto); self.texto = ' '.join(self.us)
        self.audio = DIR / 'voz' / f'limpia-{n}.wav'; self.dur = L = duracion(self.audio)
        sil = [x for x in silencios(self.audio) if x[0] > .05 and x[1] < L - .05]; self.sil = sil
        U, k = len(self.us), len(sil); hab = L - sum(b - a for a, b in sil); cps = sum(len(u) for u in self.us) / hab
        bordes = [0.0] + [x for s_ in sil for x in s_] + [L]; voz = [bordes[2 * q + 1] - bordes[2 * q] for q in range(k + 1)]
        pre = [0.0]
        for v in voz: pre.append(pre[-1] + v)
        def hablado(a, b): return (b - a) - sum(max(0, min(b, y) - max(a, x)) for x, y in sil)
        def costo(i0, i1, j0, j1):  # frases i0..i1 entre el fin del silencio j0-1 y el inicio del silencio j1 (j1 = k: final)
            e = sum(len(u) for u in self.us[i0:i1 + 1]) / cps; h = pre[j1 + 1] - pre[j0]
            return ((h - e) / (.12 * e + .3)) ** 2 + 5.0 * (i1 - i0) - (2.0 * (sil[j1][1] - sil[j1][0]) if j1 < k else 0)
        INF = float('inf'); dp = [[INF] * (k + 1) for _ in range(U)]; ant = [[None] * (k + 1) for _ in range(U)]
        for i in range(U):  # dp[i][j]: frases 0..i colocadas y la frase i termina en el silencio j
            for j in range(k + 1):
                if (j == k) != (i == U - 1): continue
                for q in (1, 2):
                    i0 = i - q + 1
                    if i0 < 0: continue
                    if i0 == 0: c = costo(0, i, 0, j); (c < dp[i][j]) and (dp[i].__setitem__(j, c), ant[i].__setitem__(j, (-1, -1, q)))
                    else:
                        for j2 in range(j):
                            v = dp[i0 - 1][j2]
                            if v == INF: continue
                            v += costo(i0, i, j2 + 1, j)
                            if v < dp[i][j]: dp[i][j], ant[i][j] = v, (i0 - 1, j2, q)
        grupos, i, j = [], U - 1, k
        while i >= 0:
            pi, pj, q = ant[i][j]; grupos.append((i - q + 1, i, pj, j)); i, j = pi, pj
        self.tramos = [None] * U; self.sil = sil
        for i0, i1, j0, j1 in reversed(grupos):
            a = sil[j0][1] if j0 >= 0 else 0.0; b = sil[j1][0] if j1 < k else L
            if i0 == i1: self.tramos[i0] = (a, b); continue
            tot = sum(len(u) for u in self.us[i0:i1 + 1]); acc = 0; self._hab = hablado
            for q in range(i0, i1 + 1):
                ta = self._en(a, b, acc / tot); acc += len(self.us[q]) + 1; tb = self._en(a, b, min(1, acc / tot)); self.tramos[q] = (ta, tb)
        self.cps, self._hab = cps, hablado
    def _en(self, a, b, f):
        """Momento dentro del tramo (a, b) en que va la fracción f del tiempo hablado (salta las pausas internas)."""
        obj = f * self._hab(a, b); t = a
        for x, y in [s for s in self.sil if a < s[0] < b] + [(b, b)]:
            seg = x - t
            if obj <= seg: return t + obj
            obj -= seg; t = y
        return b
    def T(self, frase, k=1, d=0.0):
        idx = -1
        for _ in range(k):
            idx = self.texto.find(frase, idx + 1)
            if idx < 0: sys.exit(f'No encuentro «{frase}» en la parte {self.n}')
        acc = 0
        for u, (a, b) in zip(self.us, self.tramos):
            if idx <= acc + len(u): return round(self.t0 + self._en(a, b, (idx - acc) / max(1, len(u))) + d, 2)
            acc += len(u) + 1
        return round(self.t0 + self.dur + d, 2)
    def informe(self):
        for u, (a, b) in zip(self.us, self.tramos): print(f'    {a:6.2f}-{b:6.2f} {len(u) / max(.1, self._hab(a, b)):5.1f} l/s  {u[:64]}')
    @property
    def fin(self): return self.t0 + self.dur

class BloqueEstimado(Bloque):
    """Sin voz todavía: reparte el tiempo por número de letras (para la vista previa)."""
    def __init__(self, n, texto, t0, cps=21.0, pausa=.3):
        self.n, self.t0, self.us, self.sil = n, t0, unidades(texto), []; self.texto = ' '.join(self.us); t = 0.0; self.tramos = []
        for u in self.us: d = len(u) / cps; self.tramos.append((t, t + d)); t += d + pausa
        self.dur = t - pausa; self._hab = lambda a, b: b - a; self.cps = cps; self.audio = None

B, t = [], INICIO
for i, txt in enumerate(BLOQUES, 1):
    b = Bloque(i, txt, t) if (DIR / 'voz' / f'limpia-{i}.wav').exists() else BloqueEstimado(i, txt, t); B.append(b); t = b.fin + GAP
CON_VOZ = all(b.audio for b in B)
b1, b2, b3, b4, b5, b6 = B; FIN_VOZ = b6.fin; DUR = round(FIN_VOZ + 14, 2)

cam, ev, caras, mirar = [], [], {'*': [[0, 'normal']]}, []
def C(t, lon, lat, ancho, **kw): cam.append(dict(t=round(t, 2), lon=lon, lat=lat, ancho=ancho, **kw))
def E(tipo, desde, dur=None, hasta=None, **kw):
    e = dict(tipo=tipo, desde=round(desde, 2), **kw)
    if hasta is not None: e['hasta'] = round(hasta, 2)
    elif dur is not None: e['hasta'] = round(desde + dur, 2)
    ev.append(e); return e
def cara(p, t, ex): caras.setdefault(p, []).append([round(t, 2), ex])
SA = ['ARG', 'BOL', 'CHL', 'COL', 'ECU', 'GUY', 'PRY', 'PER', 'SUR', 'URY', 'VEN']
VECINOS = ['ARG', 'BOL', 'COL', 'FRA', 'GUY', 'PRY', 'PER', 'SUR', 'URY', 'VEN']
SUDAM = (-62, -24, 135)                       # Sudamérica completa
# lugares
LETICIA, IQUITOS = (-69.94, -4.21), (-73.25, -3.75)
ITAIPU, YACY, IGUAZU, CURITIBA = (-54.59, -25.41), (-56.75, -27.48), (-54.44, -25.69), (-49.27, -25.43)
ROSARIO, ASUNCION, ARAXA, RIO = (-60.64, -32.95), (-57.58, -25.28), (-46.94, -19.59), (-43.21, -22.95)

# ================= 1 · EL GANCHO =================
C(0, -60, 10, 120); C(b1.T('Imagina que mañana', d=.2), -54, -13, 50, arco=.2)
cara('BRA', 0, 'feliz'); cara('BRA', b1.T('te despiertas'), 'normal')
T_DES = b1.T('y Brasil ya no está', d=.35)
DESAP = [dict(iso='BRA', t=T_DES)]; sacud = [dict(t=T_DES, dur=1.0, fuerza=18)]
for p in ['BOL', 'PRY', 'URY', 'ARG', 'PER', 'COL', 'VEN', 'GUY', 'SUR']: cara(p, T_DES + .5, 'shock')
E('nombre', T_DES + 1.0, texto='BRASIL', lon=-52, lat=-11, tam=52, fantasma=True, hasta=b1.T('Y no es un país'))
E('titulo', b1.T('Simplemente, donde estaba'), texto='SOLO… *MAR*', tam=110, y=230, hasta=b1.T('Y no es un país'))
C(b1.T('Y no es un país'), *SUDAM)
E('cifra', b1.T('Brasil ocupa casi la mitad'), texto='≈ 47 %', tam=170, sub='de Sudamérica era Brasil', fuente='8.5 de 17.8 millones de km²', y=250, hasta=b1.T('Así que, de un día'))
E('cinta', b1.T('amanece con un mordisco', d=.2), x=960, y=930, escala=1.5, texto='SUDAMÉRICA CON UN MORDISCO', icono='globo', color='#1f6aa8', hasta=b1.T('Y lo primero'))
for p in SA: cara(p, b1.T('amanece con un mordisco'), 'preocupado')
C(b1.T('Pasaría en Bolivia'), -63.5, -17, 20)
E('resaltar', b1.T('Pasaría en Bolivia'), pais='BOL', color='#ffd23f', hasta=b1.T('Antes de que termine'))
cara('BOL', b1.T('Pasaría en Bolivia'), 'sorpresa')
E('pin', b1.T('despertaría con playa', d=-.2), lon=-60.2, lat=-14.0, texto='¿PLAYA?', escala=1.6, hasta=b1.T('Antes de que termine'))
cara('BOL', b1.T('despertaría con playa'), 'risa')
E('cinta', b1.T('despertaría con playa', d=.4), x=960, y=930, escala=1.45, texto='BOLIVIA DESPIERTA CON PLAYA', icono='barco', color='#1f6aa8', hasta=b1.T('Antes de que termine'))
C(b1.T('Antes de que termine'), *SUDAM)
cara('BOL', b1.T('Antes de que termine'), 'normal')
E('iconos', b1.T('Antes de que termine'), y=470, paso=.0, gap=380, escala=1.45, items=[dict(icono='isla', texto='¿UNA ISLA?', color='#1f6aa8'), dict(icono='gota', texto='¿IGUAZÚ SECO?', color='#4ea3ff'), dict(icono='foco', texto='¿SIN LUZ?', color='#ffd23f')], hasta=b1.T('Y ese país es Paraguay'))
E('resaltar', b1.T('por qué Uruguay'), pais='URY', hasta=b1.T('por qué las cataratas'))
E('pin', b1.T('por qué las cataratas'), lon=IGUAZU[0], lat=IGUAZU[1], texto='IGUAZÚ', escala=1.5, hasta=b1.T('y por qué hay un país'))
C(b1.T('Y ese país es Paraguay'), -58.2, -23.4, 15, suave=False)
E('resaltar', b1.T('Y ese país es Paraguay'), pais='PRY', color='#ffd23f', hasta=b1.T('Ah, y como siempre'))
cara('PRY', b1.T('Y ese país es Paraguay'), 'grito')
E('apagon', b1.T('Y ese país es Paraguay', d=.8), dur=1.6, fuerza=.55)
C(b1.T('Ah, y como siempre'), -60, -18, 60)
cara('*', b1.T('Ah, y como siempre'), 'normal')
E('cinta', b1.T('nadie sufre'), x=960, y=900, escala=1.4, texto='TRANQUILO: NADIE SUFRE', icono='corazon', color='#2e9e5b', hasta=b1.T('Nosotros somos'))
E('globo', b1.T('se mudan a otro rincón'), pais='ARG', texto='¿Y a dónde se fueron?', lado=1, hasta=b1.T('Nosotros somos'))
for p in ['BOL', 'PRY', 'URY', 'ARG', 'PER']: cara(p, b1.T('Nosotros somos'), 'preocupado')
E('titulo', b1.T('Nosotros somos'), texto='¿QUÉ PASARÍA SI\n*BRASIL*\nDESAPARECIERA?', tam=92, y=330, hasta=b1.fin + .3)

# ================= 2 · EL NUEVO MAPA Y LA GENTE =================
C(b2.t0, -58, -15, 62); cara('*', b2.t0, 'normal')
E('region', b2.t0, texto='EL NUEVO MAPA', hasta=b2.T('Ahora, piensa en la gente'))
for i, p in enumerate(VECINOS): E('resaltar', b2.T('Brasil tiene frontera con diez', d=.25 + i * .14), pais=p, color='#ffd23f', hasta=b2.T('menos Chile y Ecuador'))
E('cifra', b2.T('Brasil tiene frontera con diez'), texto='10 PAÍSES', tam=150, sub='tenían frontera con Brasil', y=250, hasta=b2.T('En total'))
for p in ['CHL', 'ECU']: E('resaltar', b2.T('menos Chile y Ecuador'), pais=p, color='#9aa5ae', hasta=b2.T('En total')); cara(p, b2.T('menos Chile y Ecuador'), 'confundido')
E('globo', b2.T('menos Chile y Ecuador', d=.3), pais='ECU', texto='¿Y nosotros qué?', lado=-1, hasta=b2.T('En total', d=.8))
E('cifra', b2.T('En total'), texto='16,885 km', tam=150, sub='de fronteras que desaparecen', fuente='Itamaraty', y=250, hasta=b2.T('Y todo eso'))
E('cinta', b2.T('La tercera frontera'), x=960, y=930, escala=1.35, texto='3.ª FRONTERA MÁS LARGA DEL PLANETA', icono='globo', color='#1f6aa8', hasta=b2.T('Y todo eso'))
E('titulo', b2.T('Y todo eso'), texto='TODO ESO… *ES COSTA*', tam=100, y=250, hasta=b2.T('El que más gana'))
C(b2.T('El que más gana'), -63, -15.5, 22)
E('nombre', b2.T('su frontera con Brasil medía'), texto='BOLIVIA +3,423 km DE COSTA', lon=-61, lat=-13.2, tam=34, hasta=b2.T('Paraguay, que nunca'))
cara('BOL', b2.T('El que más gana'), 'risa')
C(b2.T('En la Guerra del Pacífico'), -66, -20, 26)
E('pin', b2.T('En la Guerra del Pacífico', d=.3), lon=-70.4, lat=-23.6, texto='LITORAL · 1879', hasta=b2.T('Y lo mejor'))
E('cifra', b2.T('perdió unos cuatrocientos'), texto='400 km', tam=150, sub='de costa perdió Bolivia en 1879–1884', fuente='Guerra del Pacífico', y=250, hasta=b2.T('Ahora tendría ocho'))
cara('BOL', b2.T('perdió unos cuatrocientos'), 'triste'); cara('CHL', b2.T('perdió unos cuatrocientos'), 'duda')
E('cifra', b2.T('Ahora tendría ocho'), texto='× 8', tam=220, sub='más costa que la que perdió', y=280, hasta=b2.T('Y lo mejor'))
cara('BOL', b2.T('Ahora tendría ocho'), 'risa')
E('iconos', b2.T('Bolivia ya tiene Armada'), y=430, paso=0, escala=1.5, items=[dict(icono='barco', texto='ARMADA BOLIVIANA')], hasta=b2.T('Paraguay, que nunca'))
E('globo', b2.T('Por fin tendría un mar'), pais='BOL', texto='¡Zarpamos!', lado=1, hasta=b2.T('Paraguay, que nunca', d=.6))
C(b2.T('Paraguay, que nunca'), -57.5, -23.5, 16)
E('nombre', b2.T('ganaría mil trescientos'), texto='PARAGUAY +1,365 km DE PLAYA', lon=-56.0, lat=-21.6, tam=32, hasta=b2.T('Pero el caso más raro'))
cara('PRY', b2.T('Paraguay, que nunca'), 'sorpresa'); cara('PRY', b2.T('ganaría mil trescientos'), 'feliz')
C(b2.T('Pero el caso más raro'), -56.3, -33.0, 11)
E('resaltar', b2.T('Pero el caso más raro'), pais='URY', color='#ffd23f', hasta=b2.T('Y hay un país de Europa'))
E('nombre', b2.T('el río Uruguay y el Río de la Plata'), texto='RÍO URUGUAY', lon=-58.35, lat=-31.6, tam=24, hasta=b2.T('Y hay un país de Europa'))
E('nombre', b2.T('y el Río de la Plata'), texto='RÍO DE LA PLATA', lon=-57.0, lat=-34.75, tam=24, hasta=b2.T('Y hay un país de Europa'))
cara('URY', b2.T('Sin Brasil, Uruguay queda'), 'sorpresa')
E('iconos', b2.T('Técnicamente'), y=420, paso=0, escala=1.6, items=[dict(icono='isla', texto='')], hasta=b2.T('Y hay un país de Europa'))
E('cinta', b2.T('Uruguay se convierte en una isla'), x=960, y=930, escala=1.5, texto='URUGUAY ES UNA ISLA', icono='isla', color='#1f6aa8', hasta=b2.T('Y hay un país de Europa', d=.4))
cara('URY', b2.T('Uruguay se convierte en una isla'), 'risa')
C(b2.T('Y hay un país de Europa'), -54, 4, 14)
E('nombre', b2.T('Y hay un país de Europa', d=1.5), texto='GUAYANA FRANCESA', lon=-53.2, lat=3.9, tam=28, hasta=b2.T('Es con Brasil'))
C(b2.T('Porque la frontera más larga'), -25, 28, 120, arco=.25)
E('nombre', b2.T('Porque la frontera más larga', d=1.6), texto='FRANCIA', lon=2.5, lat=46.6, tam=30, hasta=b2.T('Y el río Amazonas'))
E('nombre', b2.T('Porque la frontera más larga', d=1.9), texto='GUAYANA FRANCESA', lon=-53.2, lat=3.9, tam=26, hasta=b2.T('Y el río Amazonas'))
E('resaltar', b2.T('Porque la frontera más larga'), pais='FRA', color='#ffd23f', hasta=b2.T('Y el río Amazonas'))
cara('FRA', b2.T('Porque la frontera más larga'), 'sorpresa')
E('cifra', b2.T('Es con Brasil'), texto='730 km', tam=150, sub='era la frontera más larga de Francia', fuente='Guayana Francesa – Brasil', y=250, hasta=b2.T('Y el río Amazonas'))
C(b2.T('Y el río Amazonas'), -70.8, -3.6, 14)
E('flujo', b2.T('Y el río Amazonas'), de=list(IQUITOS), a=list(LETICIA), icono='gota', n=5, hasta=b2.T('Ahora, piensa'))
E('pin', b2.T('Terminaría aquí'), lon=LETICIA[0], lat=LETICIA[1], texto='LETICIA: FIN DEL AMAZONAS', hasta=b2.T('Ahora, piensa'))
cara('COL', b2.T('Terminaría aquí'), 'sorpresa'); cara('PER', b2.T('Terminaría aquí'), 'feliz')
C(b2.T('Ahora, piensa en la gente'), -58, -18, 66)
E('region', b2.T('Ahora, piensa en la gente'), texto='LA GENTE', hasta=b2.fin)
E('cifra', b2.T('En Brasil viven'), texto='213 MILLONES', tam=150, sub='de personas vivían en Brasil', fuente='IBGE, julio de 2025', y=250, hasta=b2.T('Uno de cada tres'))
E('cifra', b2.T('Uno de cada tres'), texto='1 DE CADA 3', tam=150, sub='latinoamericanos era brasileño', y=250, hasta=b2.T('Y con ellos se va'))
E('cifra', b2.T('Y con ellos se va'), texto='4 DE CADA 5', tam=150, sub='personas que hablan portugués', y=250, hasta=b2.T('De pronto, Sudamérica'))
for i, p in enumerate(SA): E('resaltar', b2.T('De pronto, Sudamérica', d=i * .05), pais=p, color='#ffd23f', hasta=b2.T('Y ahora viene'))
E('titulo', b2.T('De pronto, Sudamérica'), texto='SUDAMÉRICA, CASI SOLO\nEN *ESPAÑOL*', tam=84, y=280, hasta=b2.T('Y ahora viene'))
E('titulo', b2.T('Empieza en tu desayuno'), texto='EMPIEZA EN TU *DESAYUNO*', tam=96, y=320, hasta=b3.t0 + 1.0)

# ================= 3 · EL DESAYUNO Y LA CARNE =================
C(b3.t0, -64, -2, 56); E('region', b3.t0, texto='EL DESAYUNO', hasta=b3.T('Pero el golpe más grande'))
E('resaltar', b3.t0 + .3, pais='COL', color='#ffd23f', hasta=b3.T('Brasil produce cerca'))
cara('COL', b3.T('Hoy pasa al revés'), 'risa')
E('globo', b3.T('Hoy pasa al revés'), pais='COL', texto='¡Ahora me toca a mí!', lado=1, hasta=b3.T('Brasil produce cerca', d=.6))
C(b3.T('Brasil produce cerca'), -20, 15, 235)
E('cifra', b3.T('Brasil produce cerca'), texto='≈ 40 %', tam=170, sub='del café del mundo', fuente='USDA FAS', y=250, hasta=b3.T('Sin Brasil, el café'))
for a in [[-95, 38], [10, 50], [138, 37]]: E('flujo', b3.T('Brasil produce cerca', d=.4), de=[-48, -18], a=a, icono='cafe', n=5, hasta=b3.T('Sin Brasil, el café'))
for a in [[-95, 38], [10, 50], [138, 37]]: E('flujo', b3.T('Sin Brasil, el café'), de=[-48, -18], a=a, icono='cafe', n=4, roto=True, hasta=b3.T('Ahora mira el jugo'))
E('cinta', b3.T('el café sube de precio'), x=960, y=880, escala=1.4, texto='EL CAFÉ SUBE DE PRECIO', icono='dolar', color='#d6453d', hasta=b3.T('y los grandes ganadores'))
for p in ['VNM', 'COL']: E('resaltar', b3.T('Vietnam y Colombia'), pais=p, color='#ffd23f', hasta=b3.T('Ahora mira el jugo')); cara(p, b3.T('Vietnam y Colombia'), 'risa')
E('iconos', b3.T('Ahora mira el jugo'), y=430, paso=0, escala=1.6, items=[dict(icono='naranja', texto='JUGO DE NARANJA')], hasta=b3.T('De cada cuatro vasos'))
E('cifra', b3.T('De cada cuatro vasos'), texto='3 DE CADA 4', tam=150, sub='vasos de jugo de naranja exportado', fuente='CitrusBR / USDA', y=250, hasta=b3.T('Y el azúcar'))
E('cifra', b3.T('Y el azúcar'), texto='≈ 50 %', tam=170, sub='del azúcar que se exporta en el mundo', fuente='Cepea / JOB', y=250, hasta=b3.T('O sea: café'))
E('iconos', b3.T('O sea: café'), y=440, paso=.35, gap=360, escala=1.45, items=[dict(icono='cafe', texto='CAFÉ'), dict(icono='naranja', texto='JUGO'), dict(icono='azucar', texto='AZÚCAR')], hasta=b3.T('Pero el golpe más grande'))
E('titulo', b3.T('Tu desayuno entero'), texto='TU DESAYUNO…\n*DE UN SOLO PAÍS*', tam=88, y=250, hasta=b3.T('Pero el golpe más grande'))
C(b3.T('Llegaría a China'), 112, 32, 60)
E('resaltar', b3.T('Llegaría a China'), pais='CHN', color='#ffd23f', hasta=b3.T('Brasil vende cerca del cincuenta'))
cara('CHN', b3.T('Llegaría a China'), 'shock')
C(b3.T('Brasil vende cerca del cincuenta'), 30, 5, 260)
E('flujo', b3.T('Brasil vende cerca del cincuenta', d=.3), de=[-50, -15], a=[112, 32], icono='soja', n=7, hasta=b3.T('Para alimentar'))
E('cifra', b3.T('Brasil vende cerca del cincuenta'), texto='58 %', tam=170, sub='de la soja exportada del planeta', fuente='USDA WASDE 2024/25', y=250, hasta=b3.T('Y de cada cuatro granos'))
E('cifra', b3.T('Y de cada cuatro granos'), texto='3 DE CADA 4', tam=150, sub='granos de soja que importa China', fuente='Aduana de China / Hedgepoint, 2025', y=250, hasta=b3.T('Para alimentar'))
C(b3.T('Para alimentar'), 108, 33, 48)
E('iconos', b3.T('Para alimentar'), y=430, paso=.25, gap=200, escala=1.4, items=[dict(icono='cerdo') for _ in range(4)], hasta=b3.T('China tiene casi'))
cara('CHN', b3.T('Para alimentar'), 'preocupado')
E('cifra', b3.T('China tiene casi'), texto='≈ 1 DE CADA 2', tam=140, sub='cerdos del mundo vive en China', fuente='FAO', y=250, hasta=b3.T('Y como Brasil también'))
E('flujo', b3.T('y sin Brasil, se quedaría'), de=[-50, -15], a=[112, 32], icono='soja', n=5, roto=True, hasta=b3.T('Y como Brasil también'))
cara('CHN', b3.T('y sin Brasil, se quedaría'), 'llora')
C(b3.T('Y como Brasil también'), 15, 15, 250)
E('iconos', b3.T('Y como Brasil también'), y=430, paso=.35, gap=420, escala=1.5, items=[dict(icono='pollo', texto='POLLO · N.º 1'), dict(icono='carne', texto='RES · N.º 1')], hasta=b3.T('Y aquí es donde'))
E('cinta', b3.T('la carne subiría'), x=960, y=880, escala=1.4, texto='LA CARNE SUBE EN MEDIO PLANETA', icono='dolar', color='#d6453d', hasta=b3.T('Y aquí es donde'))
C(b3.T('Y aquí es donde'), -60, -10, 42)
E('titulo', b3.T('Exporta… lluvia'), texto='EXPORTA… *LLUVIA*', tam=120, y=260, hasta=b4.t0 + 1.0)
E('flujo', b3.T('Exporta… lluvia'), de=[-58, -4], a=[-61, -26], icono='nube', n=5, hasta=b4.t0 + 1.0)

# ================= 4 · LOS RÍOS QUE VUELAN =================
C(b4.t0, -62, -13, 44); E('region', b4.t0, texto='LOS RÍOS QUE VUELAN', hasta=b4.T('Y hay un país que perdería'))
E('nombre', b4.T('Sobre la Amazonía', d=1.0), texto='AMAZONÍA', lon=-60, lat=-6, tam=40, fantasma=True, hasta=b4.T('Los científicos'))
E('titulo', b4.T('Los científicos los llaman'), texto='RÍOS *VOLADORES*', tam=110, y=250, hasta=b4.T('Cada día'))
E('flujo', b4.T('Los científicos los llaman'), de=[-55, -3], a=[-67, -12], icono='nube', n=5, hasta=b4.T('sin Brasil, esos ríos'))
E('flujo', b4.T('Los científicos los llaman', d=.8), de=[-67, -12], a=[-60, -27], icono='nube', n=5, hasta=b4.T('sin Brasil, esos ríos'))
E('cifra', b4.T('Cada día'), texto='20,000 MILLONES', tam=120, sub='de toneladas de agua suben al aire cada día', fuente='A. D. Nobre, INPE', y=250, hasta=b4.T('Eso es más agua'))
E('iconos', b4.T('Eso es más agua'), y=440, paso=.5, gap=520, escala=1.4, items=[dict(icono='nube', texto='AL CIELO: 20,000 M t'), dict(icono='gota', texto='AL MAR: 18,000 M t')], hasta=b4.T('El viento se lleva'))
for p in ['BOL', 'PRY', 'ARG']: E('resaltar', b4.T('baja convertida en lluvia'), pais=p, color='#4ea3ff', hasta=b4.T('Y como cerca')); cara(p, b4.T('baja convertida en lluvia'), 'feliz')
E('cifra', b4.T('Y como cerca del sesenta'), texto='≈ 60 %', tam=170, sub='de la Amazonía estaba en Brasil', y=250, hasta=b4.T('sin Brasil, esos ríos'))
E('flujo', b4.T('sin Brasil, esos ríos'), de=[-55, -3], a=[-67, -12], icono='nube', n=4, roto=True, hasta=b4.T('Ahora, seguro'))
E('flujo', b4.T('sin Brasil, esos ríos'), de=[-67, -12], a=[-60, -27], icono='nube', n=4, roto=True, hasta=b4.T('Ahora, seguro'))
for p in ['BOL', 'PRY', 'ARG']: cara(p, b4.T('sin Brasil, esos ríos'), 'preocupado')
C(b4.T('Ahora, seguro escuchaste'), -40, 0, 150)
E('cifra', b4.T('Ahora, seguro escuchaste'), texto='¿20 % DEL OXÍGENO?', tam=120, sub='lo que siempre nos dijeron', y=250, hasta=b4.T('Los árboles producen'))
E('sello', b4.T('eso es un mito', d=.1), x=960, y=560, texto='MITO', tam=2.2, hasta=b4.T('Los árboles producen'))
E('iconos', b4.T('Los árboles producen'), y=440, paso=.8, gap=440, escala=1.5, items=[dict(icono='o2', texto='+ LO PRODUCE'), dict(icono='o2', texto='− SE LO CONSUME', color='#9aa5ae')], hasta=b4.T('Según un científico'))
E('cifra', b4.T('Según un científico'), texto='≈ 0', tam=220, sub='aporte neto de oxígeno de la Amazonía', fuente='Y. Malhi, Universidad de Oxford', y=280, hasta=b4.T('Así que no'))
E('cinta', b4.T('Así que no'), x=960, y=900, escala=1.4, texto='EL AIRE: TRANQUILO', icono='corazon', color='#2e9e5b', hasta=b4.T('El problema real'))
E('cinta', b4.T('El problema real'), x=960, y=900, escala=1.4, texto='EL PROBLEMA: LA LLUVIA', icono='gota', color='#d6453d', hasta=b4.T('Argentina es uno'))
C(b4.T('Argentina es uno'), -63, -33, 30)
E('resaltar', b4.T('Argentina es uno'), pais='ARG', color='#ffd23f', hasta=b4.T('Y hay un país que perdería'))
E('iconos', b4.T('Argentina es uno'), y=330, paso=.3, gap=300, escala=1.35, items=[dict(icono='soja', texto='SOJA'), dict(icono='maiz', texto='MAÍZ'), dict(icono='trigo', texto='TRIGO')], hasta=b4.T('Y parte de la lluvia'))
E('flujo', b4.T('Y parte de la lluvia'), de=[-60, -8], a=[-62, -32], icono='nube', n=4, hasta=b4.T('Y hay un país que perdería'))
cara('ARG', b4.T('Y parte de la lluvia'), 'preocupado')
C(b4.T('Y hay un país que perdería'), -57, -25, 18)
E('titulo', b4.T('Perdería sus ríos'), texto='PERDERÍA SUS *RÍOS*', tam=110, y=260, hasta=b5.t0 + 1.0)

# ================= 5 · PARAGUAY Y LOS RÍOS DEL SUR =================
C(b5.t0, -57, -27, 24); E('region', b5.t0, texto='LOS RÍOS DEL SUR', hasta=b5.fin)
E('flujo', b5.T('Es el Paraná'), de=list(ITAIPU), a=list(ROSARIO), icono='gota', n=6, hasta=b5.T('Sin Brasil, esos ríos'))
E('nombre', b5.T('Es el Paraná'), texto='RÍO PARANÁ', lon=-58.6, lat=-28.4, tam=28, hasta=b5.T('Y aquí es donde'))
E('flujo', b5.T('Y nace… en Brasil'), de=[-50, -20], a=list(ITAIPU), icono='gota', n=4, hasta=b5.T('Sin Brasil, esos ríos'))
E('nombre', b5.T('Y nace… en Brasil', d=.4), texto='NACE AQUÍ', lon=-50.5, lat=-20.5, tam=26, fantasma=True, hasta=b5.T('Y aquí es donde'))
E('flujo', b5.T('El río Paraguay también'), de=[-56.5, -15.5], a=list(ASUNCION), icono='gota', n=4, hasta=b5.T('Sin Brasil, esos ríos'))
E('flujo', b5.T('Y el río Uruguay, igual'), de=[-51.5, -27.6], a=[-58.2, -33.5], icono='gota', n=4, hasta=b5.T('Sin Brasil, esos ríos'))
E('cifra', b5.T('O sea: los tres grandes'), texto='3 RÍOS', tam=170, sub='del sur del continente nacen en Brasil', y=250, hasta=b5.T('Sin Brasil, esos ríos'))
for de, a in [([-50, -20], list(ITAIPU)), ([-56.5, -15.5], list(ASUNCION)), ([-51.5, -27.6], [-58.2, -33.5])]: E('flujo', b5.T('Sin Brasil, esos ríos'), de=de, a=a, icono='gota', n=3, roto=True, hasta=b5.T('Y aquí es donde'))
E('titulo', b5.T('Sin Brasil, esos ríos'), texto='RÍOS QUE NACEN… *EN EL MAR*', tam=86, y=250, hasta=b5.T('Y aquí es donde'))
C(b5.T('Y aquí es donde Paraguay'), -56.2, -25.2, 10)
cara('PRY', b5.T('Y aquí es donde Paraguay'), 'preocupado')
E('pin', b5.T('la represa de Itaipú'), lon=ITAIPU[0], lat=ITAIPU[1], texto='ITAIPÚ', escala=1.4, hasta=b5.T('Y no solo Paraguay'))
E('flujo', b5.T('En dos mil veinticinco, Itaipú'), de=list(ITAIPU), a=list(ASUNCION), icono='rayo', n=5, hasta=b5.T('Sin Brasil, Itaipú'))
E('cifra', b5.T('En dos mil veinticinco, Itaipú'), texto='87.6 %', tam=160, sub='de la electricidad de Paraguay (2025)', fuente='Itaipú, informe anual 2025', y=250, hasta=b5.T('Pero la mitad de la represa'))
E('cinta', b5.T('Pero la mitad de la represa'), x=960, y=930, escala=1.35, texto='MITAD BRASIL · MITAD PARAGUAY', icono='rayo', color='#1f6aa8', hasta=b5.T('Sin Brasil, Itaipú'))
E('flujo', b5.T('Sin Brasil, Itaipú'), de=list(ITAIPU), a=list(ASUNCION), icono='rayo', n=4, roto=True, hasta=b5.T('Y no solo Paraguay'))
E('apagon', b5.T('y sin río', d=.2), dur=1.4, fuerza=.5)
cara('PRY', b5.T('y sin río'), 'llora')
E('apagon', b5.T('a quedarse casi a oscuras', d=.2), dur=2.2, fuerza=.72, foco=True)
cara('PRY', b5.T('a quedarse casi a oscuras'), 'grito')
C(b5.T('Río abajo'), -56.6, -27.3, 9)
E('pin', b5.T('la represa de Yacyretá'), lon=YACY[0], lat=YACY[1], texto='YACYRETÁ', escala=1.3, hasta=b5.T('Ahora mira hacia el este'))
cara('ARG', b5.T('la represa de Yacyretá'), 'preocupado'); cara('PRY', b5.T('Río abajo'), 'triste')
C(b5.T('Ahora mira hacia el este'), -54.6, -25.7, 6)
E('pin', b5.T('Las cataratas del Iguazú'), lon=IGUAZU[0], lat=IGUAZU[1], texto='CATARATAS DEL IGUAZÚ', escala=1.3, hasta=b5.T('Y Argentina también'))
E('cifra', b5.T('doscientos setenta y cinco'), texto='275 SALTOS', tam=150, sub='de agua en la frontera con Argentina', y=250, hasta=b5.T('Pero el río Iguazú'))
C(b5.T('Pero el río Iguazú'), -52, -25.6, 10)
E('flujo', b5.T('Pero el río Iguazú'), de=list(CURITIBA), a=list(IGUAZU), icono='gota', n=6, hasta=b5.T('Sin Brasil, a las cataratas'))
E('nombre', b5.T('cerca de Curitiba'), texto='CURITIBA', lon=CURITIBA[0], lat=CURITIBA[1], tam=26, fantasma=True, hasta=b5.T('Una de las siete'))
E('flujo', b5.T('Sin Brasil, a las cataratas'), de=list(CURITIBA), a=list(IGUAZU), icono='gota', n=3, roto=True, hasta=b5.T('Y Argentina también'))
E('cinta', b5.T('apenas un hilo de agua'), x=960, y=930, escala=1.4, texto='IGUAZÚ: APENAS UN HILO DE AGUA', icono='gota', color='#d6453d', hasta=b5.T('Una de las siete'))
E('sello', b5.T('casi seca', d=.1), x=960, y=540, texto='CASI SECA', tam=1.8, hasta=b5.T('Y Argentina también'))
cara('ARG', b5.T('Sin Brasil, a las cataratas'), 'llora')
C(b5.T('Y Argentina también'), -60.5, -32.5, 12)
E('pin', b5.T('Por los puertos del Gran Rosario'), lon=ROSARIO[0], lat=ROSARIO[1], texto='GRAN ROSARIO', escala=1.3, hasta=b5.T('Y hay algo más'))
E('cifra', b5.T('sale cerca del setenta y cinco'), texto='75 %', tam=170, sub='de lo que Argentina exporta del campo', fuente='Bolsa de Comercio de Rosario, 2025', y=250, hasta=b5.T('Con un río más bajo'))
E('flujo', b5.T('Con un río más bajo'), de=list(ROSARIO), a=[-53, -36.5], icono='barco', n=3, hasta=b5.T('Y hay algo más'))
C(b5.T('Y hay algo más'), -57, -27, 34)
E('flujo', b5.T('dos de cada tres autos'), de=[-60, -33], a=[-48, -20], icono='auto', n=5, roto=True, hasta=b5.T('Pero ojo'))
E('cifra', b5.T('dos de cada tres autos'), texto='2 DE CADA 3', tam=150, sub='autos que exporta Argentina iban a Brasil', fuente='ADEFA, 2025 (67.2 %)', y=250, hasta=b5.T('Sin Brasil, las fábricas'))
cara('ARG', b5.T('Sin Brasil, las fábricas'), 'llora')
E('globo', b5.T('Sin Brasil, las fábricas'), pais='ARG', texto='¿Y ahora a quién le vendo?', lado=1, hasta=b5.T('Pero ojo', d=.6))
C(b5.T('Pero ojo'), -57.5, -23.5, 18)
cara('PRY', b5.T('Ganaría mar'), 'risa')
E('iconos', b5.T('Ganaría mar'), y=430, paso=.4, gap=440, escala=1.4, items=[dict(icono='barco', texto='PUERTOS PROPIOS'), dict(icono='soja', texto='SOJA AL MUNDO')], hasta=b5.T('Paraguay perdería la luz'))
E('titulo', b5.T('Paraguay perdería la luz'), texto='PARAGUAY PIERDE LA LUZ…\n…PERO GANA *EL OCÉANO*', tam=80, y=300, hasta=b5.fin + .3)

# ================= 6 · LO QUE NO SE REEMPLAZA Y EL CIERRE =================
C(b6.t0, -50, -18, 46); E('region', b6.t0, texto='LO QUE NO TIENE PRECIO', hasta=b6.T('Te acuerdas'))
E('iconos', b6.T('Hay un metal llamado niobio'), y=430, paso=0, escala=2.0, items=[dict(icono='niobio', texto='NIOBIO')], hasta=b6.T('Seguramente nunca'))
E('iconos', b6.T('va en el acero'), y=430, paso=.3, gap=300, escala=1.35, items=[dict(icono='auto', texto='AUTOS'), dict(icono='casa', texto='PUENTES', color='#8fa3b8'), dict(icono='rayo', texto='GASODUCTOS', color='#8fa3b8'), dict(icono='avion', texto='AVIONES')], hasta=b6.T('Y Brasil produce cerca del noventa'))
E('cifra', b6.T('Y Brasil produce cerca del noventa'), texto='93 %', tam=170, sub='del niobio del mundo', fuente='USGS, 2026', y=250, hasta=b6.T('Casi todo sale'))
C(b6.T('Casi todo sale'), -47, -19.5, 16)
E('pin', b6.T('Casi todo sale', d=.6), lon=ARAXA[0], lat=ARAXA[1], texto='ARAXÁ · MINAS GERAIS', escala=1.5, hasta=b6.T('Sin Brasil, las fábricas de acero'))
E('iconos', b6.T('Casi todo sale', d=.9), y=330, paso=0, escala=1.6, items=[dict(icono='niobio', texto='')], hasta=b6.T('Sin Brasil, las fábricas de acero'))
C(b6.T('Sin Brasil, las fábricas de acero'), -85, 38, 120, arco=.2)
E('resaltar', b6.T('tendrían que depender de Canadá'), pais='CAN', color='#ffd23f', hasta=b6.T('En el fútbol'))
cara('CAN', b6.T('tendrían que depender de Canadá'), 'shock')
E('cifra', b6.T('que produce apenas'), texto='5 %', tam=170, sub='Canadá, el segundo productor', fuente='USGS, 2026', y=250, hasta=b6.T('En el fútbol'))
C(b6.T('En el fútbol'), -50, -15, 60)
E('cifra', b6.T('Brasil es el único país'), texto='23 DE 23', tam=150, sub='Mundiales jugados: todos', y=250, hasta=b6.T('Y el que más ha ganado'))
E('iconos', b6.T('Y el que más ha ganado'), y=430, paso=.18, gap=170, escala=1.3, items=[dict(icono='trofeo') for _ in range(5)], hasta=b6.T('Sin Brasil, la cima'))
C(b6.T('Sin Brasil, la cima'), 10, 47, 34)
for p in ['DEU', 'ITA']: E('resaltar', b6.T('Alemania e Italia'), pais=p, color='#ffd23f', hasta=b6.T('Y Argentina se quedaría')); cara(p, b6.T('Alemania e Italia'), 'risa')
E('iconos', b6.T('con cuatro cada una'), y=430, paso=.3, gap=420, escala=1.3, items=[dict(icono='trofeo', texto='ALEMANIA · 4'), dict(icono='trofeo', texto='ITALIA · 4')], hasta=b6.T('Y Argentina se quedaría'))
C(b6.T('Y Argentina se quedaría'), -64, -34, 30)
cara('ARG', b6.T('Y Argentina se quedaría'), 'confundido')
E('globo', b6.T('Y Argentina se quedaría', d=.4), pais='ARG', texto='¿Y ahora contra quién?', lado=1, hasta=b6.T('También se irían'))
C(b6.T('También se irían'), -50, -18, 46)
E('iconos', b6.T('También se irían'), y=430, paso=.35, gap=300, items=[dict(icono='futbol', texto='PELÉ'), dict(icono='futbol', texto='RONALDINHO'), dict(icono='futbol', texto='NEYMAR'), dict(icono='nota', texto='CARNAVAL')], hasta=b6.T('Y el Cristo Redentor'))
E('pin', b6.T('Y el Cristo Redentor'), lon=RIO[0], lat=RIO[1], texto='RÍO DE JANEIRO', escala=1.4, hasta=b6.T('Te acuerdas'))
E('iconos', b6.T('Y el Cristo Redentor'), y=380, paso=0, escala=1.9, items=[dict(icono='cristo', texto='CRISTO REDENTOR')], hasta=b6.T('Y la bossa nova'))
E('iconos', b6.T('Y la bossa nova'), y=380, paso=0, escala=1.7, items=[dict(icono='nota', texto='LA CHICA DE IPANEMA')], hasta=b6.T('Te acuerdas'))
C(b6.T('Te acuerdas'), *SUDAM)
E('iconos', b6.T('Te acuerdas'), y=460, paso=.4, gap=330, escala=1.3, items=[dict(icono='barco', texto='PLAYA ✓'), dict(icono='isla', texto='ISLA ✓'), dict(icono='gota', texto='IGUAZÚ ✓'), dict(icono='foco', texto='LUZ ✓', color='#ffd23f')], hasta=b6.T('Entonces'))
E('tarjeta', b6.T('Bolivia gana el mar'), iso='bo', nombre='Bolivia', estado='CELEBRA', dato='GANA EL MAR', texto='Por fin, playa propia.', hasta=b6.T('Colombia y Vietnam'))
E('tarjeta', b6.T('Colombia y Vietnam'), iso='co', nombre='Colombia', estado='CELEBRA', dato='GANA EL CAFÉ', texto='Junto con Vietnam.', hasta=b6.T('Paraguay gana el océano'))
E('tarjeta', b6.T('Paraguay gana el océano'), iso='py', nombre='Paraguay', estado='LE AFECTA', dato='GANA Y PIERDE', texto='Con océano… pero sin luz.', hasta=b6.T('Y Argentina se queda sin lluvia'))
E('tarjeta', b6.T('Y Argentina se queda sin lluvia'), iso='ar', nombre='Argentina', estado='LLORA', dato='PIERDE', texto='Sin lluvia, sin cliente y sin rival.', hasta=b6.T('Y Sudamérica se convierte'))
for i, p in enumerate(SA): E('resaltar', b6.T('Y Sudamérica se convierte', d=i * .05), pais=p, color='#ffd23f', hasta=b6.T('Porque Brasil no es solo'))
E('titulo', b6.T('Y Sudamérica se convierte'), texto='UNA *MEDIA LUNA*\nALREDEDOR DE UN MAR NUEVO', tam=78, y=280, hasta=b6.T('Porque Brasil no es solo'))
C(b6.T('Porque Brasil no es solo'), -45, 5, 150)
cara('*', b6.T('Es el que le da agua'), 'triste')
E('titulo', b6.T('Es el que le da agua'), texto='LE DABA *AGUA, COMIDA Y LLUVIA*\nA MEDIO CONTINENTE', tam=72, y=300, hasta=b6.T('Qué país hacemos'))
cara('*', b6.T('Qué país hacemos'), 'feliz')
E('pregunta', b6.T('Qué país hacemos'), texto='¿QUÉ PAÍS DESAPARECEMOS DESPUÉS?', y=470, hasta=DUR)
E('cinta', b6.T('el más votado'), x=960, y=640, texto='EL MÁS VOTADO ES EL SIGUIENTE', icono='globo', color='#2e9e5b', hasta=DUR)
C(DUR, -45, 5, 145, suave=False)

# ================= escenas reales (clips de Flow/Veo) entre los mapas =================
# (código, desde, hasta, extras). Encima van los textos de pantalla; lo atado al mapa se oculta mientras dura el clip.
CL = [
    ('B01', 0.0, b1.T('y Brasil ya no está', d=.15), dict(entra=.01)),
    ('B02', b1.T('Simplemente, donde estaba', d=-.15), b1.T('Y no es un país', d=-.05), {}),
    ('B03', b1.T('despertaría con playa', d=-.35), b1.T('Antes de que termine', d=-.05), dict(z0=1.0, z1=1.1)),
    ('B07', b2.T('Empieza en tu desayuno', d=-.25), b3.t0 + 1.0, {}),
    ('B07', b3.T('O sea: café'), b3.T('Pero el golpe más grande', d=-.05), dict(ofs=3.6)),
    ('B10', b3.T('Exporta… lluvia', d=-.25), b4.T('Cada día', d=-.05), dict(vel=.85)),
    ('B11', b4.T('El problema real'), b4.T('Argentina es uno', d=-.05), {}),
    ('B12', b5.T('Paraguay comparte con Brasil', d=-.1), b5.T('En dos mil veinticinco, Itaipú', d=-.05), {}),
    ('B13', b5.T('Sin Brasil, Itaipú', d=-.1), b5.T('Paraguay pasaría de tener', d=-.05), dict(ofs=.5)),
    ('B14', b5.T('Las cataratas del Iguazú', d=-.1), b5.T('Pero el río Iguazú', d=-.05), {}),
    ('B15', b5.T('Sin Brasil, a las cataratas', d=-.1), b5.T('Y Argentina también', d=-.05), dict(z0=1.0, z1=1.12)),
]
CLIPS = []
for cod, a0, a1, ex in CL:
    src, dst = DIR / 'clips' / f'{cod}.mp4', DIR / '.clips' / cod
    if not src.exists(): print('  falta el clip', cod); continue
    if not dst.exists():
        dst.mkdir(parents=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(src), '-vf', 'fps=30,scale=1920:1080:flags=lanczos', '-q:v', '3', str(dst / '%04d.jpg')], check=True)
    CLIPS.append(dict(codigo=cod, desde=round(a0, 2), hasta=round(a1, 2), **ex))

# ================= salida =================
cam.sort(key=lambda k: k['t']); quieta = [cam[0]]
for k in cam[1:]:
    prev = quieta[-1]
    if k.get('suave') is False: quieta.append(k); continue
    mov = 2.2 if k.get('arco') else 1.5
    if k['t'] - prev['t'] > mov + .3: quieta.append(dict(t=k['t'], lon=prev['lon'], lat=prev['lat'], ancho=prev['ancho'], suave=False)); k = dict(k, t=round(k['t'] + mov, 2))
    quieta.append(k)
cam = sorted(quieta, key=lambda k: k['t'])
for i in range(1, len(cam)):
    if cam[i]['t'] <= cam[i - 1]['t']: cam[i]['t'] = round(cam[i - 1]['t'] + .05, 2)
for k in caras.values(): k.sort()
# voz completa: silencio inicial + partes + pausas, normalizada
tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True); partes = []
def silencio(seg, nombre):
    f = tmp / nombre; subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', f'{max(.01, seg):.3f}', '-c:a', 'pcm_s16le', str(f)], check=True); return f
t = 0.0
if CON_VOZ:
    for i, b in enumerate(B): partes += [silencio(b.t0 - t, f's{i}.wav'), b.audio]; t = b.fin
    partes.append(silencio(DUR - t, 'sfin.wav'))
    (tmp / 'lista.txt').write_text(''.join(f"file '{p}'\n" for p in partes))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(tmp / 'lista.txt'), '-af', 'loudnorm=I=-16:TP=-2:LRA=11', '-ar', '48000', str(tmp / 'voz.wav')], check=True)
spec = dict(estilo='caricatura', salida='que-pasaria-si-brasil-desapareciera', duracion=DUR, camara=cam, desaparece=DESAP, sacudidas=sacud,
            tam={'URY': 1.35, 'PRY': 1.25, 'BOL': 1.1, 'ECU': 1.3, 'GUY': 1.3, 'SUR': 1.4, 'CHL': 1.1, 'VNM': 1.4, 'ITA': 1.3, 'DEU': 1.2}, mirar=mirar, caras=caras, eventos=sorted(ev, key=lambda e: e['desde']), clips=CLIPS, fundido_inicio=.5, **({'audio': '.tmp/voz.wav'} if CON_VOZ else {}))
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print(('CON VOZ' if CON_VOZ else 'SIN VOZ (tiempos estimados)') + f" · {len(ev)} capas · {len(cam)} posiciones de cámara · {DUR / 60:.2f} min")
for b in B: print(f'  parte {b.n}: {b.t0:6.1f} s · dura {b.dur:5.1f} s')
