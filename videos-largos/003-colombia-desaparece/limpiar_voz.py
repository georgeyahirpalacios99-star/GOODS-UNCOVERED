"""Acorta solo los silencios largos (> 0.5 s) a 0.45 s. La voz no se toca: ni velocidad, ni tono, ni ecualización."""
import numpy as np, subprocess, wave
from pathlib import Path
D = Path(__file__).resolve().parent; SR = 44100
def leer(f): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32)
for n in range(1, 7):
    x = leer(D / 'voz' / f'parte-{n}.mp3'); fr = int(SR * .01); m = len(x) // fr
    rms = np.sqrt((x[:m * fr].reshape(m, fr) ** 2).mean(1)) / 32768; sil = 20 * np.log10(rms + 1e-9) < -40
    # tramos de silencio
    tramos, i = [], 0
    while i < m:
        if sil[i]:
            j = i
            while j < m and sil[j]: j += 1
            tramos.append((i, j)); i = j
        else: i += 1
    keep, last, quitado = [], 0, 0.0
    for a, b in tramos:
        dur = (b - a) * .01
        if a == 0: keep.append(x[0:0]); last = max(0, b - 5) * fr; quitado += (b - 5) * .01 if b > 5 else 0; continue
        if b == m: keep.append(x[last:min(len(x), (a + 15) * fr)]); last = len(x); quitado += max(0, dur - .15); break
        if dur > .5: keep.append(x[last:(a + 20) * fr]); last = (b - 25) * fr; quitado += dur - .45
    keep.append(x[last:]); y = np.concatenate(keep)
    with wave.open(str(D / 'voz' / f'limpia-{n}.wav'), 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.astype(np.int16).tobytes())
    print(f'parte {n}: {len(x) / SR:6.1f} s → {len(y) / SR:6.1f} s (silencio recortado {quitado:.1f} s)')
