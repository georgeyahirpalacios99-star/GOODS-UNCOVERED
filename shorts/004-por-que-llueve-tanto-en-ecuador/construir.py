"""Short 004 · ¿Por qué llueve TANTO en Ecuador? — mapa fantástico 2D (estilo 'fantasia'), 9:16.
    python3 shorts/004-por-que-llueve-tanto-en-ecuador/construir.py        # con voz/voz.mp3 si existe; si no, tiempos estimados
    node motor-mapa/render.cjs shorts/004-por-que-llueve-tanto-en-ecuador
    python3 shorts/004-por-que-llueve-tanto-en-ecuador/sonido.py
"""
import json, re, subprocess, sys, wave
from pathlib import Path
import numpy as np
DIR = Path(__file__).resolve().parent
TEXTO = re.search(r'```\n(.*?)```', (DIR / 'GUION-ELEVENLABS.md').read_text(encoding='utf-8'), re.S).group(1)
INICIO = 0.75
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
    def __init__(self, n, texto, t0, cps=17.0, pausa=.38):
        self.n, self.t0, self.us, self.sil = n, t0, unidades(texto), []; self.texto = ' '.join(self.us); t = 0.0; self.tramos = []
        for u in self.us: d = len(u) / cps; self.tramos.append((t, t + d)); t += d + pausa
        self.dur = t - pausa; self._hab = lambda a, b: b - a; self.cps = cps

def limpiar(mp3, out, SR=44100):
    """Acorta solo los silencios largos (> 0.5 s) a 0.45 s. La voz no se toca."""
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(mp3), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32)
    fr = int(SR * .01); m = len(x) // fr; sil = 20 * np.log10(np.sqrt((x[:m * fr].reshape(m, fr) ** 2).mean(1)) / 32768 + 1e-9) < -40
    tramos, i = [], 0
    while i < m:
        if sil[i]:
            j = i
            while j < m and sil[j]: j += 1
            tramos.append((i, j)); i = j
        else: i += 1
    keep, last = [], 0
    for a, b in tramos:
        if a == 0: last = max(0, b - 5) * fr; continue
        if b == m: keep.append(x[last:min(len(x), (a + 15) * fr)]); last = len(x); break
        if (b - a) * .01 > .5: keep.append(x[last:(a + 20) * fr]); last = (b - 25) * fr
    keep.append(x[last:]); y = np.concatenate(keep)
    with wave.open(str(out), 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.astype(np.int16).tobytes())

mp3s = sorted((DIR / 'voz').glob('*.mp3'))
if mp3s: limpiar(mp3s[0], DIR / 'voz' / 'limpia-1.wav'); b = Bloque(1, TEXTO, INICIO); CON_VOZ = True
else: b = BloqueEstimado(1, TEXTO, INICIO); CON_VOZ = False
T = b.T; FIN_VOZ = b.fin; DUR = round(FIN_VOZ + 1.3, 2)

# ---------------- utilidades ----------------
cam, ev, sacud = [], [], []
TEXTOS = {'titulo', 'cifra', 'contador', 'chip', 'sello', 'pregunta', 'pin', 'caja'}
def E(tipo, desde, dur=None, hasta=None, **kw):
    e = dict(tipo=tipo, desde=round(desde, 2), **kw)
    if hasta is not None: e['hasta'] = round(hasta, 2)
    elif dur is not None: e['hasta'] = round(desde + dur, 2)
    if tipo in TEXTOS: e['arriba'] = True
    ev.append(e); return e
ultimo = [None]
def CAM(t, lon, lat, ancho, d=.45, arco=0):
    """Mueve la cámara a (lon, lat, ancho) en d segundos empezando en t (se queda quieta hasta t)."""
    if ultimo[0]: lo, la, an = ultimo[0]; cam.append(dict(t=round(t, 2), lon=lo, lat=la, ancho=an, suave=False))
    cam.append(dict(t=round(t + d, 2), lon=lon, lat=lat, ancho=ancho, **({'arco': arco} if arco else {}))); ultimo[0] = (lon, lat, ancho)
def SAC(t, f=14, d=.5): sacud.append(dict(t=round(t, 2), dur=d, fuerza=f))
TODO = (-78.3, -2.75, 8.8)                       # Ecuador completo en vertical
PUYO, SALINAS = (-78.0, -1.49), (-80.95, -2.21)
REG_C = {'costa': (-80.05, -1.25), 'sierra': (-78.72, -1.05), 'amazonia': (-76.95, -1.75)}
U = lambda i: b.t0 + b.tramos[i][0]               # inicio de la frase i
iu = lambda frase: next(i for i, u in enumerate(b.us) if frase in u)

# ================= 0 · LA GOTA (0.0–1.3 s) =================
E('gota', 0, dur=1.6, cae=.55, abre=.85)
cam.append(dict(t=0, lon=-78.3, lat=-2.6, ancho=5.6)); cam.append(dict(t=.62, lon=-78.3, lat=-2.6, ancho=5.6, suave=False)); cam.append(dict(t=1.25, lon=TODO[0], lat=TODO[1], ancho=TODO[2])); ultimo[0] = TODO
E('tormenta', .45, lon=-77.55, lat=-1.75, r=1.75, sem=3, rayos=[T('donde llueve', d=.2), T('veinticinco', d=.3), T('que en otro', d=-.3)], hasta=T('La razón'))
E('seco', .45, lon=-80.72, lat=-2.25, r=.55, remolino=True, hasta=T('La razón'))

# ================= 1 · EL GANCHO =================
CAM(T('un lugar donde'), -77.95, -1.6, 3.6, d=.38)
E('chip', T('donde llueve'), lon=PUYO[0], lat=PUYO[1], dy=-78, texto='PUYO', flecha=True, tam=44, hasta=T('La razón'))
E('cifra', T('veinticinco veces'), texto='×25', sub='MÁS LLUVIA', tam=230, y=300, hasta=T('trescientos'))
SAC(T('veinticinco veces', d=.1), 12)
CAM(T('que en otro', d=-.15), -80.72, -2.3, 3.3, d=.38)
E('chip', T('que en otro', d=.1), lon=SALINAS[0], lat=SALINAS[1], dy=-78, texto='SALINAS', flecha=True, tam=44, color='#ff9a3c', hasta=T('La razón'))
CAM(T('Y están'), *TODO, d=.5)
E('trazo', T('a solo'), de=list(PUYO), a=list(SALINAS), dur=.9, hasta=T('Cada región'))
E('contador', T('trescientos'), de=0, a=340, suf=' km', dur=.9, sub='EN LÍNEA RECTA', tam=200, y=300, hasta=T('La razón', d=.1))
SAC(T('kilómetros'), 9)

# ================= 2 · CADA REGIÓN, SU LLUVIA =================
E('titulo', T('La razón'), texto='¿POR *QUÉ*?', tam=150, y=300, hasta=T('Cada región'))
E('regiones3', T('no tiene una sola'), paso=.25, foco=[[T('Cada región'), 'costa'], [T('llueve por'), 'sierra'], [T('motivo distinto'), 'amazonia']], hasta=U(iu('En la Amazonía')) + .25)
E('titulo', T('Cada región'), texto='CADA REGIÓN, *SU LLUVIA*', tam=72, y=300, hasta=U(iu('En la Amazonía')) - .35)
for k, frase in zip(['costa', 'sierra', 'amazonia'], ['Cada región', 'llueve por', 'motivo distinto']):
    E('chip', T(frase), lon=REG_C[k][0], lat=REG_C[k][1], texto={'costa': 'COSTA', 'sierra': 'SIERRA', 'amazonia': 'AMAZONÍA'}[k], tam=38, hasta=U(iu('En la Amazonía')) - .35)
E('tormenta', T('Cada región'), lon=-79.9, lat=-1.5, r=.75, sem=11, fi=.2, fo=.3, oscura=False, hasta=T('llueve por', d=.2))
E('seco', T('Cada región', d=.5), lon=-80.0, lat=-1.6, r=.7, hasta=T('llueve por', d=.3))
E('tormenta', T('llueve por'), lon=-78.65, lat=-1.1, r=.6, sem=12, fi=.2, fo=.3, rayos=[T('llueve por', d=.25)], hasta=T('motivo distinto', d=.1))
E('tormenta', T('motivo distinto'), lon=-77.0, lat=-1.7, r=1.15, sem=13, fi=.2, hasta=U(iu('En la Amazonía')) + .3)
E('girar', T('motivo distinto'), dur=1.2, vueltas=2)
CAM(T('Cada región'), -78.4, -2.5, 8.0, d=1.6)

# ================= 3 · CORTE DE LOS ANDES =================
t5 = U(iu('En la Amazonía'))
E('nubesPaso', t5 - .45, dur=1.0)
CAM(t5 - .45, -77.6, -1.6, 2.2, d=.5)
d0 = t5 + .05
E('corte', d0, tAire=T('el aire húmedo') - d0, tFrio=T('se enfría') - d0 - .2, tNube=T('sube,') - d0, tLluvia=T('se descarga') - d0, tZoom=T('En Puyo') - d0,
  rayos=[T('se descarga') - d0 + .3, T('cuatro mil') - d0 + .2, T('al año.') - d0], hasta=U(iu('En la Costa')) + .25)
E('chip', T('el aire húmedo'), x=880, y=980, texto='AIRE HÚMEDO', tam=36, color='#3fd0c4', hasta=T('se descarga'))
E('chip', T('contra los Andes'), x=660, y=690, texto='LOS ANDES', tam=40, hasta=T('En Puyo'))
E('chip', T('En la Amazonía'), x=890, y=1110, texto='AMAZONÍA', tam=34, color='#5fb35a', hasta=U(iu('En la Costa')))
E('chip', T('se enfría'), x=450, y=640, texto='SE ENFRÍA', tam=40, color='#bfe9ff', hasta=T('se descarga', d=.4))
E('chip', T('En Puyo'), x=860, y=1065, texto='PUYO', tam=38, flecha=True, hasta=U(iu('En la Costa')))
E('contador', T('cuatro mil'), de=0, a=4000, suf=' mm', dur=1.0, sub='DE LLUVIA AL AÑO', tam=170, y=330, hasta=U(iu('En la Costa')) + .1)
SAC(T('cuatro mil', d=1.0), 8)

# ================= 4 · LA COSTA, AL REVÉS =================
t7 = U(iu('En la Costa'))
cam.append(dict(t=round(t7 + .05, 2), lon=-80.25, lat=-2.45, ancho=5.6, suave=False)); ultimo[0] = (-80.25, -2.45, 5.6)
E('titulo', T('pasa lo contrario'), texto='LA COSTA: *AL REVÉS*', tam=92, y=300, hasta=T('la corriente fría'))
HUMB = [[-81.0, -8.5], [-81.4, -5.6], [-81.6, -3.6], [-81.75, -2.4], [-82.3, -1.2], [-83.6, -.2]]
E('corriente', T('la corriente fría'), mar=True, ruta=HUMB, color='#5d55d8', brillo='#dfe8ff', ancho=.3, frio=True, dur=1.2, hasta=T('casi todos'))
E('chip', T('de Humboldt'), lon=-81.55, lat=-3.05, texto='CORRIENTE DE HUMBOLDT', tam=34, color='#9d97ff', hasta=T('Salinas recibe'))
E('chip', T('la corriente fría', d=.6), lon=-81.7, lat=-3.6, texto='FRÍA', tam=30, color='#bfe9ff', hasta=T('Salinas recibe'))
E('nubesBajas', T('no deja crecer'), puntos=[[-80.15, -.9], [-80.35, -1.95], [-80.0, -.05]], llovizna=True, hasta=T('casi todos', d=.3))
CAM(T('Salinas recibe'), -80.7, -2.35, 3.4, d=.45)
E('seco', T('Salinas recibe'), lon=-80.72, lat=-2.25, r=.5, remolino=True, hasta=T('casi todos', d=.4))
E('contador', T('ciento veinte'), de=0, a=120, suf=' mm', dur=.8, sub='AL AÑO EN SALINAS', tam=170, y=330, hasta=T('Y en la Sierra'))
SAC(T('ciento veinte', d=.8), 8)
CAM(T('casi todos'), -80.0, -2.0, 5.2, d=.6)
CALIDA = [[-79.6, 3.6], [-80.3, 2.0], [-80.6, .7], [-81.0, -.6], [-81.2, -1.8]]
E('corriente', T('casi todos'), mar=True, ruta=CALIDA, color='#ff8a3d', brillo='#fff1c9', ancho=.4, dur=1.0, hasta=T('Y en la Sierra', d=.3))
E('tormenta', T('entre enero', d=.2), lon=-80.0, lat=-1.6, r=.9, sem=21, oscura=False, crece=.8, hasta=T('Y en la Sierra', d=.4))
E('chip', T('entre enero'), lon=SALINAS[0], lat=SALINAS[1], dy=-80, texto='ENERO → ABRIL', tam=36, color='#ff9a3c', flecha=True, hasta=T('Y en la Sierra'))

# ================= 5 · LA SIERRA, DOS VECES =================
CAM(T('Y en la Sierra'), -78.6, -1.45, 4.3, d=.45)
E('titulo', T('dos temporadas'), texto='SIERRA: *2* TEMPORADAS', tam=92, y=300, hasta=U(iu('Pero cada pocos')))
E('tormenta', T('dos temporadas'), lon=-78.55, lat=-.95, r=.55, sem=31, fi=.2, fo=.25, rayos=[T('dos temporadas', d=.3)], hasta=T('dos temporadas', d=.85))
E('tormenta', T('de lluvia al año'), lon=-78.75, lat=-2.2, r=.55, sem=32, fi=.2, fo=.25, rayos=[T('de lluvia al año', d=.25)], hasta=U(iu('Pero cada pocos')) + .2)
E('chip', T('dos temporadas'), lon=-78.55, lat=-.95, dy=-90, texto='1', tam=40, hasta=U(iu('Pero cada pocos')))
E('chip', T('de lluvia al año'), lon=-78.75, lat=-2.2, dy=-90, texto='2', tam=40, hasta=U(iu('Pero cada pocos')))

# ================= 6 · EL NIÑO =================
t10 = U(iu('Pero cada pocos'))
CAM(t10, -80.4, -2.6, 11.0, d=1.0, arco=.15)
E('titulo', T('el mar cambia'), texto='EL MAR *CAMBIA*\nLAS REGLAS', tam=92, y=300, hasta=U(iu('Los pescadores')))
SAC(T('cambia las reglas'), 10)
t11 = U(iu('Los pescadores'))
E('noche', t11 - .1, lon=-81.0, lat=-2.75, estrella=[790, 640], hasta=U(iu('El agua se calienta')) + .4)
CAM(t11, -80.6, -2.7, 6.2, d=.8)
E('caja', T('El Niño'), x=540, y=330, texto='EL NIÑO', tam=130, hasta=U(iu('El agua se calienta')))
SAC(T('El Niño', d=.05), 12)
E('chip', T('cerca de Navidad'), x=540, y=500, texto='LLEGABA EN NAVIDAD', tam=40, hasta=U(iu('El agua se calienta')) + .2)
t12 = U(iu('El agua se calienta'))
CAM(t12, -79.9, -2.55, 9.2, d=.8)
E('calor', T('se calienta'), mar=True, dur=1.6, hasta=U(iu('En tu ciudad')) + .6)
E('titulo', T('se calienta'), texto='EL AGUA SE *CALIENTA*', tam=88, y=300, hasta=T('fabricar nubes', d=.2))
E('tormenta', T('fabricar nubes'), lon=-80.0, lat=-1.75, r=1.35, sem=41, desdeMar=True, crece=1.2, rayos=[T('fabricar nubes', d=1.2), T('veintinueve', d=.6)], hasta=U(iu('En tu ciudad')) + .5)
E('chip', T('fabricar nubes', d=.2), x=540, y=330, texto='¡FABRICA NUBES!', tam=52, hasta=T('Hoy el mar'))
E('inundacion', T('fabricar nubes', d=.8), lon=-79.65, lat=-1.75, r=.85, dur=2.4, hasta=U(iu('En tu ciudad')) + .6)
E('tinte', T('fabricar nubes', d=.5), region='amazonia', color='#d9a441', alfa=.5, hasta=U(iu('En tu ciudad')) + .6)
CAM(T('Hoy el mar'), -80.3, -2.5, 8.0, d=.7)
E('contador', T('veintinueve'), de=24, a=29, suf=' °C', dur=.9, sub='MÁS QUE EN 1997', tam=200, y=300, hasta=U(iu('En tu ciudad')))
SAC(T('veintinueve', d=.9), 16, .6)

# ================= 7 · CIERRE =================
t14 = U(iu('En tu ciudad'))
CAM(t14, *TODO, d=.8)
E('titulo', t14, texto='¿Y EN *TU CIUDAD*?', tam=110, y=300, hasta=DUR)
E('chip', T('Escríbelo'), x=540, y=470, texto='COMENTA Y LA PONEMOS EN EL MAPA', tam=36, hasta=DUR)
for i, (lo, la) in enumerate([(-78.47, -.18), (-79.9, -2.19), (-79.0, -2.9), (-80.72, -.95), (-79.7, .97), (-78.62, -1.24), (-79.2, -4.0), (-77.81, -.99)]):
    E('pin', T('lo ponemos en el mapa', d=i * .12), lon=lo, lat=la, escala=1.6, color='#ffd23f', hasta=DUR)

# ================= salida =================
cam.sort(key=lambda k: k['t'])
for i in range(1, len(cam)):
    if cam[i]['t'] <= cam[i - 1]['t']: cam[i]['t'] = round(cam[i - 1]['t'] + .02, 2)
narr = [dict(desde=round(b.t0 + a, 2), hasta=round(b.t0 + c + .12, 2), texto=u) for u, (a, c) in zip(b.us, b.tramos)]
for i in range(len(narr) - 1): narr[i]['hasta'] = min(narr[i]['hasta'], narr[i + 1]['desde'])
ORDEN = {'tormenta': 1, 'seco': 1, 'trazo': 2, 'regiones3': 0, 'inundacion': 1, 'tinte': 0, 'nubesBajas': 2, 'noche': 4, 'corte': 5, 'nubesPaso': 6, 'gota': 9}
ev.sort(key=lambda e: (ORDEN.get(e['tipo'], 8 if e.get('arriba') else 3), e['desde']))
spec = dict(estilo='fantasia', formato='vertical', salida='por-que-llueve-tanto-en-ecuador', duracion=DUR, camara=cam, sacudidas=sacud, ocultar=['barra', 'marcador', 'lista', 'region'],
            narracion=narr, subY=1335, subTam=64, subColor='#ffffff', eventos=ev, fundido_inicio=0)
if CON_VOZ:
    tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(DIR / 'voz' / 'limpia-1.wav'), '-af', f'adelay={int(INICIO * 1000)},apad=whole_dur={DUR},loudnorm=I=-16:TP=-2:LRA=11', '-ar', '48000', '-ac', '1', str(tmp / 'voz.wav')], check=True)
    spec['audio'] = '.tmp/voz.wav'
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print(f"{'CON VOZ' if CON_VOZ else 'SIN VOZ (tiempos estimados)'} · {len(ev)} capas · {len(cam)} claves de cámara · {DUR:.1f} s")
