"""Alineador de frases con la voz (sin reconocimiento de voz: usa los silencios reales) y utilidades comunes de los Shorts 007."""
import re, subprocess, sys, wave
import numpy as np
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
    def __init__(self, n, texto, t0, audio=None):
        self.n, self.t0 = n, t0; self.us = unidades(texto); self.texto = ' '.join(self.us)
        self.audio = audio; self.dur = L = duracion(self.audio)
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


def limpiar(mp3, out, SR=44100, largo=.5, deja=.42):
    """Acorta solo los silencios largos (> largo s) a 'deja' s. La voz no se toca: ni velocidad, ni tono, ni ecualización."""
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(mp3), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32)
    fr = int(SR * .01); m = len(x) // fr; sil = 20 * np.log10(np.sqrt((x[:m * fr].reshape(m, fr) ** 2).mean(1)) / 32768 + 1e-9) < -40
    tramos, i = [], 0
    while i < m:
        if sil[i]:
            j = i
            while j < m and sil[j]: j += 1
            tramos.append((i, j)); i = j
        else: i += 1
    keep, last = [], 0; mitad = int(deja * 50)
    for a, b in tramos:
        if a == 0: last = max(0, b - 5) * fr; continue
        if b == m: keep.append(x[last:min(len(x), (a + 15) * fr)]); last = len(x); break
        if (b - a) * .01 > largo: keep.append(x[last:(a + mitad) * fr]); last = (b - mitad) * fr
    keep.append(x[last:]); y = np.concatenate(keep)
    with wave.open(str(out), 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.astype(np.int16).tobytes())

def palabras_de(b):
    """Tiempos de cada palabra (repartidos por letras dentro de su frase) para el subtítulo de una palabra."""
    out = []
    for u, (a, c) in zip(b.us, b.tramos):
        ws = u.split(); tot = sum(len(w) + 1 for w in ws); acc = 0
        for w in ws:
            t0 = b.t0 + b._en(a, c, acc / tot); acc += len(w) + 1; t1 = b.t0 + b._en(a, c, min(1, acc / tot)); limpio = w.strip('…,.:;').strip()
            if limpio: out.append(dict(t0=round(t0, 3), t1=round(t1, 3), w=limpio))
    for i in range(len(out) - 1): out[i]['t1'] = max(out[i]['t1'], out[i + 1]['t0'])
    return out
