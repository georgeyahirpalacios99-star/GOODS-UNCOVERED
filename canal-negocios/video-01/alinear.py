"""Alinea las frases del guion (separadas por <break>) con los silencios de cada parte de voz. Salida: tiempos.json"""
import json, re, subprocess
from pathlib import Path
D = Path(__file__).resolve().parent
GAP = 0.7  # silencio entre partes
partes = re.findall(r'```\n(.*?)```', (D / 'GUION-ELEVENLABS.md').read_text(), re.S)
def silencios(f):
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(f), '-af', 'silencedetect=noise=-35dB:d=0.2', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', o)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', o)]
    return list(zip(st, en + [None] * (len(st) - len(en))))
def dur(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)], capture_output=True, text=True).stdout)
salida, t0 = [], 0.0
for n, txt in enumerate(partes, 1):
    f = D / 'voz' / f'parte-{n}.mp3'; T = dur(f); segs = [s.strip() for s in re.split(r'<break[^>]*/>', txt) if s.strip()]
    sil = [(a, b if b is not None else T) for a, b in silencios(f)]
    ini = sil[0][1] if sil and sil[0][0] < .05 else 0.0; fin = sil[-1][0] if sil and sil[-1][1] >= T - .05 else T
    cand = [(a, b) for a, b in sil if a > ini + .3 and b < fin - .3]
    K, ch = len(segs), [len(s) for s in segs]; frases = [max(0, len(re.findall(r'[.?!…]', s)) - 1) for s in segs]
    # velocidad: el habla total menos las K-1 pausas más largas
    pausas = sorted((b - a for a, b in cand), reverse=True)[:K - 1]; cps = sum(ch) / max(1, (fin - ini) - sum(pausas) - .3 * sum(frases))
    esp = [c / cps + .3 * fr for c, fr in zip(ch, frases)]
    S = len(cand); INF = 1e18
    # dp[i][j]: mejor costo poniendo el final del segmento i en el silencio j
    dp = [[INF] * S for _ in range(K)]; bk = [[-1] * S for _ in range(K)]
    for j in range(S): d = cand[j][0] - ini; dp[0][j] = (d - esp[0]) ** 2 - 2 * (cand[j][1] - cand[j][0])
    for i in range(1, K - 1):
        for j in range(S):
            for k in range(j):
                if dp[i - 1][k] >= INF: continue
                d = cand[j][0] - cand[k][1]; c = dp[i - 1][k] + (d - esp[i]) ** 2 - 2 * (cand[j][1] - cand[j][0])
                if c < dp[i][j]: dp[i][j], bk[i][j] = c, k
    best, bj = INF, -1
    for k in range(S):
        if dp[K - 2][k] < INF:
            c = dp[K - 2][k] + (fin - cand[k][1] - esp[K - 1]) ** 2
            if c < best: best, bj = c, k
    idx = [bj]
    for i in range(K - 2, 0, -1): idx.append(bk[i][idx[-1]])
    idx = idx[::-1]
    bordes = [ini] + [x for j in idx for x in cand[j]] + [fin]
    for i, s in enumerate(segs):
        a, b = bordes[2 * i], bordes[2 * i + 1]
        salida.append(dict(id=len(salida), parte=n, desde=round(t0 + a, 2), hasta=round(t0 + b, 2), texto=s))
    t0 += T + GAP
json.dump(dict(total=round(t0 - GAP, 2), frases=salida), open(D / 'tiempos.json', 'w'), ensure_ascii=False, indent=0)
# voz completa normalizada
lista = D / 'voz' / 'lista.txt'; lista.write_text(''.join(f"file 'parte-{n}.mp3'\nfile 'gap.wav'\n" for n in range(1, len(partes) + 1)))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=mono', '-t', str(GAP), '-c:a', 'libmp3lame', '-b:a', '128k', str(D / 'voz' / 'gap.mp3')], check=True)
lista.write_text(''.join(f"file 'parte-{n}.mp3'\n" + ("file 'gap.mp3'\n" if n < len(partes) else '') for n in range(1, len(partes) + 1)))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(lista), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', str(D / 'voz' / 'voz-completa.wav')], check=True)
for f in salida: print(f"{f['id']:>2} {f['desde']:7.2f}-{f['hasta']:7.2f} {f['texto'][:58]}")
print('total', round(t0 - GAP, 2))
