"""Une las 8 partes de voz (ElevenLabs) recortando solo silencios largos y alinea cada frase. Lo usa construir.py."""
import re, sys, subprocess, wave
from pathlib import Path
import numpy as np
DIR = Path(__file__).resolve().parent; sys.path.insert(0, str(DIR.parents[1] / 'shorts' / '007-brasil-shorts'))
from alinear import Bloque, limpiar, palabras_de
INICIO = .4
def bloques_texto():
    src = (DIR / 'texto-voz.txt').read_text(encoding='utf-8')
    return [(b.split('|')[0].strip(), b.split('\n', 1)[1]) for b in re.split(r'^### ', src, flags=re.M)[1:]]
def preparar():
    tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True); bl, t0, wavs = [], INICIO, []
    for cod, txt in bloques_texto():
        w = tmp / f'{cod}.wav'
        if not w.exists(): limpiar(DIR / 'voz' / f'{cod}.mp3', w, largo=.7, deja=.5)
        b = Bloque(cod, txt, t0, w); bl.append(b); wavs.append((w, t0)); t0 = b.fin + .55
    dur = t0 + 1.2; SR = 48000; mix = np.zeros(int(dur * SR) + SR, np.float32)
    for w, a in wavs:
        x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(w), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32)
        i = int(a * SR); mix[i:i + len(x)] += x
    with wave.open(str(tmp / 'voz-cruda.wav'), 'w') as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(np.clip(mix, -32768, 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(tmp / 'voz-cruda.wav'), '-af', 'loudnorm=I=-16:TP=-2:LRA=11', '-ar', '48000', '-ac', '1', str(tmp / 'voz.wav')], check=True)
    return bl, round(dur, 2)
if __name__ == '__main__':
    bs, d = preparar()
    for b in bs: print(b.n, round(b.t0, 1), round(b.fin, 1)); b.informe()
    print('DURACIÓN', d)
