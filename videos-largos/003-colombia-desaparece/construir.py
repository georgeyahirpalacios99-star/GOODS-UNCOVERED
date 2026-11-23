"""Video 003 · ¿Qué pasaría si COLOMBIA desapareciera? — arma mapa.json atado a cada frase de la voz.
    python3 videos-largos/003-colombia-desaparece/limpiar_voz.py   # una vez
    python3 videos-largos/003-colombia-desaparece/construir.py
    node motor-mapa/render.cjs videos-largos/003-colombia-desaparece
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

B, t = [], INICIO
for i, txt in enumerate(BLOQUES, 1): b = Bloque(i, txt, t); B.append(b); t = b.fin + GAP
b1, b2, b3, b4, b5, b6 = B; FIN_VOZ = b6.fin; DUR = round(FIN_VOZ + 14, 2)

cam, ev, caras, mirar = [], [], {'*': [[0, 'normal']]}, []
def C(t, lon, lat, ancho, **kw): cam.append(dict(t=round(t, 2), lon=lon, lat=lat, ancho=ancho, **kw))
def E(tipo, desde, dur=None, hasta=None, **kw):
    e = dict(tipo=tipo, desde=round(desde, 2), **kw)
    if hasta is not None: e['hasta'] = round(hasta, 2)
    elif dur is not None: e['hasta'] = round(desde + dur, 2)
    ev.append(e); return e
def cara(p, t, ex): caras.setdefault(p, []).append([round(t, 2), ex])
SA = ['VEN', 'ECU', 'PER', 'BRA', 'BOL', 'CHL', 'ARG', 'PRY', 'URY', 'GUY', 'SUR']

# ================= 1 · EL GANCHO =================
E('despertar', 0, dur=2.8)
C(0, -60, 10, 120); C(b1.T('Imagina que mañana', d=.2), -73.5, 4.5, 26, arco=.2)
cara('COL', 0, 'feliz'); cara('COL', b1.T('te despiertas'), 'normal')
T_DES = b1.T('y Colombia ya no está', d=.35)
DESAP = [dict(iso='COL', t=T_DES)]; sacud = [dict(t=T_DES, dur=1.0, fuerza=18)]
for p in ['VEN', 'ECU', 'PER', 'BRA', 'PAN']: cara(p, T_DES + .5, 'shock')
E('nombre', T_DES + 1.0, texto='COLOMBIA', lon=-73.5, lat=4.5, tam=46, fantasma=True, hasta=b1.T('Y lo primero'))
E('titulo', b1.T('Simplemente, donde estaba'), texto='SOLO… *MAR*', tam=110, y=230, hasta=b1.T('Y lo primero'))
C(b1.T('Pasaría aquí'), -77.8, 8.2, 9)
E('pin', b1.T('Pasaría aquí', d=.2), lon=-77.4, lat=7.9, texto='AQUÍ', escala=1.8, hasta=b1.T('Sin ella'))
cara('PAN', b1.T('Pasaría aquí'), 'preocupado')
C(b1.T('Sin ella, Sudamérica'), -64, -16, 78, arco=.3)
for i, p in enumerate(SA): E('resaltar', b1.T('se convierte en una isla', d=i * .06), pais=p, color='#ffd23f', hasta=b1.T('Y eso es solo'))
E('cinta', b1.T('se convierte en una isla', d=.3), x=960, y=930, escala=1.55, texto='SUDAMÉRICA ES UNA ISLA', icono='globo', color='#1f6aa8', hasta=b1.T('Una isla gigante', d=1.6))
E('cifra', b1.T('separada del norte'), texto='3 MILLONES DE AÑOS', tam=104, sub='desde la última vez que estuvo sola', fuente='Istmo de Panamá · O’Dea et al., 2016', y=260, hasta=b1.T('Y eso es solo'))
C(b1.T('Y eso es solo'), -70, 8, 110)
E('iconos', b1.T('Antes de que termine'), y=470, paso=.0, gap=380, escala=1.45, items=[dict(icono='flor', texto='¿ROSAS?', color='#e8463a'), dict(icono='cafe', texto='¿TU CAFÉ?', color='#a0683a'), dict(icono='foco', texto='¿LA LUZ?', color='#ffd23f')], hasta=b1.T('Y ese país es Ecuador'))
E('resaltar', b1.T('por qué Estados Unidos'), pais='USA', hasta=b1.T('por qué tu café'))
C(b1.T('Y ese país es Ecuador'), -78.5, -1.3, 13, suave=False)
E('resaltar', b1.T('Y ese país es Ecuador'), pais='ECU', color='#ffd23f', hasta=b1.T('Ah, y antes'))
cara('ECU', b1.T('Y ese país es Ecuador'), 'grito')
E('apagon', b1.T('perdería la luz, literalmente', d=.6), dur=1.6, fuerza=.55)
C(b1.T('Ah, y antes'), -70, 5, 60)
cara('*', b1.T('Ah, y antes'), 'normal'); cara('ECU', b1.T('Ah, y antes'), 'normal')
E('cinta', b1.T('no, nadie sufre'), x=960, y=900, escala=1.4, texto='TRANQUILO: NADIE SUFRE', icono='corazon', color='#2e9e5b', hasta=b1.T('Nosotros somos'))
E('globo', b1.T('se mudan a otro rincón'), pais='VEN', texto='¿Y a dónde se fueron?', lado=1, hasta=b1.T('Nosotros somos'))
for p in ['VEN', 'ECU', 'PER', 'BRA', 'PAN']: cara(p, b1.T('Nosotros somos'), 'preocupado')
E('titulo', b1.T('Nosotros somos'), texto='¿QUÉ PASARÍA SI\n*COLOMBIA*\nDESAPARECIERA?', tam=92, y=330, hasta=b1.fin + .3)

# ================= 2 · EL NUEVO MAPA Y LA GENTE =================
C(b2.t0, -72, 4, 34); cara('*', b2.t0, 'normal')
E('region', b2.t0, texto='EL NUEVO MAPA', hasta=b2.T('Ahora, piensa en la gente'))
E('flujo', b2.T('Y ahora esos dos mares'), de=[-79, 12], a=[-80, 2], icono='gota', n=5, hasta=b2.T('De un momento'))
E('cifra', b2.T('De un momento a otro'), texto='6,342 km', tam=150, sub='de fronteras que desaparecen', fuente='Cancillería de Colombia', y=250, hasta=b2.T('Venezuela pierde'))
for txt, lon, lat, frase in [('VENEZUELA −2,219 km', -66, 7.2, 'Venezuela pierde'), ('BRASIL −1,645 km', -62.5, -3.5, 'Brasil pierde'), ('PERÚ −1,626 km', -74.5, -6.5, 'Perú, mil'), ('ECUADOR −586 km', -78.7, -1.8, 'Y Ecuador, quinientos')]:
    E('nombre', b2.T(frase), texto=txt, lon=lon, lat=lat, tam=34, hasta=b2.T('Pero el caso más raro'))
cara('VEN', b2.T('Venezuela pierde'), 'triste'); cara('BRA', b2.T('Brasil pierde'), 'triste'); cara('PER', b2.T('Perú, mil'), 'triste'); cara('ECU', b2.T('Y Ecuador, quinientos'), 'triste')
C(b2.T('Pero el caso más raro'), -79.5, 8.8, 11)
E('pin', b2.T('Panamá pasa a ser'), lon=-77.6, lat=8.0, texto='FIN DE NORTEAMÉRICA', hasta=b2.T('Y esto no es solo'))
cara('PAN', b2.T('Panamá pasa a ser'), 'sorpresa')
C(b2.T('Cuando los dos continentes'), -80, 8, 58, arco=.2)
E('flujo', b2.T('Los armadillos'), de=[-76, 2], a=[-90, 18], icono='flecha', n=3, roto=True, hasta=b2.T('Y no solo para'))
E('flujo', b2.T('Los pumas'), de=[-95, 20], a=[-70, -5], icono='flecha', n=3, roto=True, hasta=b2.T('Y no solo para'))
E('sello', b2.T('Ese puente natural', d=.8), x=960, y=520, texto='CORTADO', hasta=b2.T('Y no solo para'))
C(b2.T('Por la selva del Darién'), -77.6, 8.3, 8)
E('cifra', b2.T('cruzaron a pie'), texto='+520,000', tam=140, sub='personas cruzaron el Darién en 2023', fuente='Migración de Panamá', y=260, hasta=b2.T('Y en el Caribe'))
C(b2.T('Y en el Caribe'), -81.7, 12.6, 6)
E('nombre', b2.T('San Andrés y Providencia', d=.2), texto='SAN ANDRÉS', lon=-81.7, lat=12.55, fantasma=True, hasta=b2.T('Ahora, piensa'))
E('nombre', b2.T('San Andrés y Providencia', d=.6), texto='PROVIDENCIA', lon=-81.37, lat=13.35, fantasma=True, hasta=b2.T('Ahora, piensa'))
C(b2.T('Ahora, piensa en la gente'), -72, 2, 40)
E('region', b2.T('Ahora, piensa en la gente'), texto='LA GENTE', hasta=b2.fin)
E('cifra', b2.T('En Colombia viven'), texto='53 MILLONES', tam=150, sub='más que toda España', fuente='DANE, 2025', y=260, hasta=b2.T('Y no solo colombianos'))
E('cifra', b2.T('Colombia es el país que más venezolanos'), texto='2.8 MILLONES', tam=140, sub='de venezolanos vivían en Colombia', fuente='Migración Colombia, 2025', y=260, hasta=b2.T('O sea, en un solo día'))
cara('VEN', b2.T('Colombia es el país que más venezolanos'), 'llora')
for p in ['URY', 'PRY', 'PAN']: E('resaltar', b2.T('Uruguay, Paraguay y Panamá'), pais=p, color='#ffd23f', hasta=b2.T('Y ahora viene'))
C(b2.T('Uruguay, Paraguay y Panamá'), -68, -10, 80)
E('titulo', b2.T('Empieza en tu taza'), texto='EMPIEZA EN TU *TAZA*', tam=100, y=320, hasta=b3.t0 + 1.0)

# ================= 3 · CAFÉ Y FLORES =================
C(b3.t0, -45, 22, 210); E('region', b3.t0, texto='EL CAFÉ', hasta=b3.T('Pero el golpe más bonito'))
E('cifra', b3.T('Colombia produjo'), texto='13.67 MILLONES', tam=128, sub='de sacos de café en 2025', fuente='Federación Nacional de Cafeteros', y=250, hasta=b3.T('Cada saco pesa'))
for de, a in [([-74, 4.5], [-95, 38]), ([-74, 4.5], [10, 50]), ([-74, 4.5], [138, 37])]: E('flujo', b3.T('Cada saco pesa'), de=de, a=a, icono='cafe', n=5, hasta=b3.T('Sin Colombia, el mundo'))
E('cifra', b3.T('Si cada taza lleva'), texto='80,000 MILLONES', tam=118, sub='de tazas de café al año', fuente='cálculo: 10 g por taza', y=250, hasta=b3.T('Sin Colombia, el mundo'))
for de, a in [([-74, 4.5], [-95, 38]), ([-74, 4.5], [10, 50]), ([-74, 4.5], [138, 37])]: E('flujo', b3.T('Sin Colombia, el mundo'), de=de, a=a, icono='cafe', n=4, roto=True, hasta=b3.T('Y quien más'))
E('cinta', b3.T('el precio sube'), x=960, y=880, escala=1.4, texto='EL CAFÉ SUBE DE PRECIO', icono='dolar', color='#d6453d', hasta=b3.T('y ahora reinaría solo'))
C(b3.T('Y quien más lo aprovecharía'), -55, -12, 50); cara('BRA', b3.T('Y quien más lo aprovecharía'), 'risa')
E('globo', b3.T('y ahora reinaría solo'), pais='BRA', texto='¡Más café para mí!', hasta=b3.T('Ah, y hay otra pelea', d=.6))
C(b3.T('Ah, y hay otra pelea'), -66, 7, 16)
E('globo', b3.T('Venezuela gana por abandono'), pais='VEN', texto='¡La arepa es mía!', hasta=b3.T('Pero el golpe más bonito', d=1.0))
cara('VEN', b3.T('Venezuela gana por abandono'), 'risa')
C(b3.T('Pero el golpe más bonito'), -88, 35, 78, arco=.2); E('region', b3.T('Pero el golpe más bonito'), texto='LAS FLORES', hasta=b3.T('Y aquí es donde'))
E('flujo', b3.T('Para San Valentín'), de=[-74, 4.5], a=[-82, 33], icono='flor', n=6, hasta=b3.T('Así que imagina'))
E('cifra', b3.T('Para San Valentín'), texto='900 MILLONES', tam=140, sub='de flores para San Valentín 2025', fuente='MinAgricultura / ICA', y=250, hasta=b3.T('Más de sesenta'))
E('cifra', b3.T('Más de sesenta y cinco mil'), texto='65,000 TONELADAS', tam=120, sub='de flores a EE. UU. en unas semanas', y=250, hasta=b3.T('Así que imagina'))
E('flujo', b3.T('Así que imagina'), de=[-74, 4.5], a=[-82, 33], icono='flor', n=4, roto=True, hasta=b3.T('Y aquí es donde'))
cara('USA', b3.T('Así que imagina'), 'llora')
E('globo', b3.T('costando lo que cuesta una cena'), pais='USA', texto='¿¡80 dólares un ramo!?', lado=-1, hasta=b3.T('Y aquí es donde', d=.8))
C(b3.T('Y aquí es donde la historia'), -78.5, -1.3, 16)
E('apagon', b3.T('Perdería la luz.', d=.1), hasta=b4.t0 + 1.2, foco=True)
cara('ECU', b3.T('Perdería la luz.'), 'shock')

# ================= 4 · ECUADOR =================
C(b4.t0, -78.2, -1.6, 13); E('region', b4.t0, texto='ECUADOR', hasta=b4.fin)
E('flujo', b4.T('Ecuador y Colombia están conectados'), de=[-76.5, 3.5], a=[-78.5, -0.3], icono='rayo', n=5, hasta=b4.T('Ahora imagina'))
E('cifra', b4.T('Una línea eléctrica'), texto='460 MW', tam=150, sub='de Colombia a Ecuador', fuente='Cenace / Primicias', y=250, hasta=b4.T('Eso es cerca'))
E('cifra', b4.T('Eso es cerca del once'), texto='11 %', tam=170, sub='de la demanda máxima de Ecuador', y=250, hasta=b4.T('Y en dos mil veinticuatro'))
E('cinta', b4.T('Y en dos mil veinticuatro'), x=960, y=930, escala=1.35, texto='2024 · CRISIS ELÉCTRICA', icono='rayo', color='#d6453d', hasta=b4.T('Ahora imagina'))
E('apagon', b4.T('con apagones de horas'), dur=1.4, fuerza=.5)
cara('ECU', b4.T('con apagones de horas'), 'llora')
E('cifra', b4.T('Entre enero y noviembre'), texto='$268 MILLONES', tam=130, sub='pagó Ecuador por luz colombiana', fuente='Primicias, enero–noviembre 2024', y=250, hasta=b4.T('Ahora imagina'))
E('flujo', b4.T('Ahora imagina esos mismos'), de=[-76.5, 3.5], a=[-78.5, -0.3], icono='rayo', n=4, roto=True, hasta=b4.T('Y no es lo único'))
E('apagon', b4.T('sin nadie al otro lado', d=.2), dur=2.0, fuerza=.7, foco=True)
cara('ECU', b4.T('sin nadie al otro lado'), 'grito')
C(b4.T('El puente de Rumichaca'), -78.0, 0.2, 9)
E('pin', b4.T('El puente de Rumichaca', d=.3), lon=-77.65, lat=0.82, texto='RUMICHACA', hasta=b4.T('Pero ojo'))
cara('ECU', b4.T('Y con playa nueva'), 'risa')
E('cinta', b4.T('Y con playa nueva'), x=960, y=930, escala=1.35, texto='ECUADOR: PLAYA NUEVA AL NORTE', icono='casa', color='#1f6aa8', hasta=b4.T('Pero ojo', d=1.3))
C(b4.T('Pero ojo, porque Ecuador'), -85, 18, 70, arco=.2)
E('flujo', b4.T('Ecuador ya es uno de los mayores'), de=[-78.5, -1.5], a=[-82, 33], icono='flor', n=6, hasta=b4.fin)
cara('ECU', b4.T('Ecuador ya es uno de los mayores'), 'feliz'); cara('USA', b4.T('dependería muchísimo más'), 'amor')
E('titulo', b4.T('Ecuador perdería la luz'), texto='ECUADOR PIERDE LA LUZ…\n…PERO GANA *SAN VALENTÍN*', tam=80, y=300, hasta=b4.fin + .3)

# ================= 5 · EL AGUA =================
C(b5.t0, -71, 4, 30); E('region', b5.t0, texto='EL AGUA', hasta=b5.fin)
cara('*', b5.t0, 'normal')
E('cifra', b5.T('Colombia tiene cerca de la mitad'), texto='≈ 50 %', tam=170, sub='de los páramos del mundo', fuente='PNUD / Gobierno de Colombia', y=250, hasta=b5.T('Son esas montañas'))
E('pin', b5.T('Solo el páramo de Chingaza'), lon=-73.75, lat=4.6, texto='CHINGAZA · 80 % DEL AGUA DE BOGOTÁ', hasta=b5.T('Pero esa agua'))
E('flujo', b5.T('El río Meta y el Guaviare'), de=[-72.5, 4], a=[-63, 7.8], icono='gota', n=6, hasta=b5.T('O sea: sin Colombia'))
E('nombre', b5.T('al Orinoco'), texto='ORINOCO', lon=-64.5, lat=7.6, tam=26, hasta=b5.fin)
E('flujo', b5.T('Y el Caquetá y el Putumayo'), de=[-75, 1], a=[-62, -3.3], icono='gota', n=6, hasta=b5.T('O sea: sin Colombia'))
E('nombre', b5.T('hasta llegar al Amazonas'), texto='AMAZONAS', lon=-61, lat=-3.6, tam=26, hasta=b5.fin)
E('flujo', b5.T('O sea: sin Colombia'), de=[-72.5, 4], a=[-63, 7.8], icono='gota', n=4, roto=True, hasta=b5.fin)
E('flujo', b5.T('O sea: sin Colombia'), de=[-75, 1], a=[-62, -3.3], icono='gota', n=4, roto=True, hasta=b5.fin)
cara('VEN', b5.T('O sea: sin Colombia'), 'preocupado'); cara('BRA', b5.T('O sea: sin Colombia'), 'preocupado')
E('titulo', b5.T('Ríos que llevan miles'), texto='RÍOS QUE EMPIEZAN… *EN EL MAR*', tam=86, y=250, hasta=b5.T('Y hay algo'))

# ================= 6 · LO QUE NO SE REEMPLAZA Y EL CIERRE =================
C(b6.t0, -72, 3, 36); E('region', b6.t0, texto='LO QUE NO TIENE PRECIO', hasta=b6.T('Te acuerdas'))
E('iconos', b6.T('Colombia es el país con más especies'), y=430, paso=.15, gap=150, items=[dict(icono='ave', color=c) for c in ['#e8463a', '#ffd23f', '#3d6fb4', '#2e9e5b', '#e8873a']], hasta=b6.T('En su territorio'))
E('cifra', b6.T('En su territorio viven'), texto='1,954 ESPECIES', tam=128, sub='de aves · casi 1 de cada 5 del mundo', fuente='SiB Colombia · Global Big Day', y=250, hasta=b6.T('Y unas ochenta'))
E('cifra', b6.T('Y unas ochenta y dos'), texto='82', tam=220, sub='solo existen en Colombia', y=280, hasta=b6.T('Y bajo la tierra'))
E('sello', b6.T('Esas se pierden para siempre'), x=960, y=560, texto='PARA SIEMPRE', hasta=b6.T('Y bajo la tierra', d=.9))
E('cifra', b6.T('Colombia produce más o menos la mitad'), texto='≈ 55 %', tam=170, sub='de las esmeraldas del mundo', fuente='Fedesmeraldas', y=250, hasta=b6.T('Sin Colombia, las joyerías'))
C(b6.T('Sin Colombia, las joyerías'), 0, 20, 300)
for a in [[-74, 40.7], [55.3, 25.2], [139.7, 35.7]]: E('flujo', b6.T('Sin Colombia, las joyerías'), de=[-74, 5.5], a=a, icono='gema', n=3, roto=True, hasta=b6.T('En el fútbol'))
C(b6.T('En el fútbol'), -62, -15, 75)
E('iconos', b6.T('En el fútbol'), y=430, paso=.5, gap=560, escala=1.2, items=[dict(icono='futbol', texto='FINAL COPA AMÉRICA'), dict(icono='futbol', texto='BOTA DE ORO 2014')], hasta=b6.T('También se iría'))
E('iconos', b6.T('También se iría la música'), y=430, paso=.35, gap=250, items=[dict(icono='nota', texto=n) for n in ['SHAKIRA', 'KAROL G', 'J BALVIN', 'CARLOS VIVES']], hasta=b6.T('Y se iría Macondo'))
E('iconos', b6.T('Y se iría Macondo'), y=430, paso=0, items=[dict(icono='libro', texto='NOBEL 1982')], hasta=b6.T('Te acuerdas'))
E('titulo', b6.T('Y se iría Macondo', d=.2), texto='*MACONDO*', tam=120, y=250, hasta=b6.T('Los libros'))
C(b6.T('Te acuerdas'), -70, 8, 110)
E('iconos', b6.T('Te acuerdas'), y=460, paso=.4, gap=370, escala=1.35, items=[dict(icono='flor', texto='ROSAS ✓', color='#e8463a'), dict(icono='cafe', texto='CAFÉ ✓', color='#a0683a'), dict(icono='foco', texto='LUZ ✓', color='#ffd23f')], hasta=b6.T('Entonces'))
E('tarjeta', b6.T('Brasil gana el café'), iso='br', nombre='Brasil', estado='CELEBRA', dato='GANA', texto='Se queda con el café.', hasta=b6.T('Ecuador gana las rosas'))
E('tarjeta', b6.T('Ecuador gana las rosas'), iso='ec', nombre='Ecuador', estado='LE AFECTA', dato='PIERDE Y GANA', texto='Sin luz… pero con las rosas.', hasta=b6.T('Panamá se queda'))
E('tarjeta', b6.T('Panamá se queda'), iso='pa', nombre='Panamá', estado='NI LO NOTA', dato='FIN DEL CAMINO', texto='Última parada del continente.', hasta=b6.T('Y Sudamérica se convierte'))
for i, p in enumerate(SA): E('resaltar', b6.T('Y Sudamérica se convierte', d=i * .05), pais=p, color='#ffd23f', hasta=b6.T('Pero la verdad'))
C(b6.T('Y Sudamérica se convierte'), -64, -16, 80)
C(b6.T('Pero la verdad'), -45, 15, 240)
cara('*', b6.T('Porque hay países que se extrañan'), 'triste')
E('titulo', b6.T('Porque hay países que se extrañan'), texto='HAY PAÍSES QUE SE EXTRAÑAN\nPOR LO QUE *SON*', tam=78, y=300, hasta=b6.T('Qué país hacemos'))
cara('*', b6.T('Qué país hacemos'), 'feliz')
E('pregunta', b6.T('Qué país hacemos'), texto='¿QUÉ PAÍS DESAPARECEMOS DESPUÉS?', y=470, hasta=DUR)
E('cinta', b6.T('el más votado'), x=960, y=640, texto='EL MÁS VOTADO ES EL SIGUIENTE', icono='globo', color='#2e9e5b', hasta=DUR)
C(DUR, -45, 15, 235, suave=False)

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
for i, b in enumerate(B): partes += [silencio(b.t0 - t, f's{i}.wav'), b.audio]; t = b.fin
partes.append(silencio(DUR - t, 'sfin.wav'))
(tmp / 'lista.txt').write_text(''.join(f"file '{p}'\n" for p in partes))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(tmp / 'lista.txt'), '-af', 'loudnorm=I=-16:TP=-2:LRA=11', '-ar', '48000', str(tmp / 'voz.wav')], check=True)
spec = dict(estilo='caricatura', salida='que-pasaria-si-colombia-desapareciera', duracion=DUR, camara=cam, desaparece=DESAP, sacudidas=sacud,
            tam={'USA': 1.2, 'BRA': 1.2, 'PAN': 1.4, 'ECU': 1.25, 'URY': 1.2}, mirar=mirar, caras=caras, eventos=sorted(ev, key=lambda e: e['desde']), audio='.tmp/voz.wav')
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print(f"{len(ev)} capas · {len(cam)} posiciones de cámara · {DUR / 60:.2f} min")
for b in B: print(f'  parte {b.n}: {b.t0:6.1f} s · dura {b.dur:5.1f} s')
