"""Crea Shorts verticales (1080x1920) a partir del video 002, con la misma voz, subtítulos y cabecera fija.

    python3 videos-largos/002-sin-paises-hispanos/shorts.py          # arma y renderiza todos
    python3 videos-largos/002-sin-paises-hispanos/shorts.py --solo 2 # solo el short 2
"""
import contextlib, copy, importlib.util, io, json, re, subprocess, sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
RAIZ = DIR.parent.parent
spec_mod = importlib.util.spec_from_file_location('construir', DIR / 'construir.py')
c = importlib.util.module_from_spec(spec_mod)
with contextlib.redirect_stdout(io.StringIO()):
    spec_mod.loader.exec_module(c)
b1, b2, b3, b4, b5, b6, b7 = c.B
base = json.loads((DIR / 'mapa.json').read_text(encoding='utf-8'))

# subtítulos: cada tramo hablado se parte en oraciones con tiempos proporcionales al texto
narr = []
for b in c.B:
    for (txt, _), (a, z) in zip(b.segs, b.tramos):
        oraciones = re.findall(r'[^.?!…]+[.?!…]*', txt)
        tot = sum(len(o) for o in oraciones) or 1; t = b.t0 + a
        for o in oraciones:
            d = (z - a) * len(o) / tot
            if o.strip(): narr.append(dict(desde=round(t, 2), hasta=round(t + d, 2), texto=o.strip()))
            t += d

SHORTS = [
    dict(n=1, nombre='21 paises borrados', ini=b1.t0, fin=b1.T('Hoy vamos', d=1.2),
         cabecera='¿Y SI DESAPARECEN TODOS\nLOS PAÍSES QUE HABLAN *ESPAÑOL*?',
         titulo='Borramos 21 países del mapa en un segundo 😳 #geografia #mapas #shorts'),
    dict(n=2, nombre='adios canal de panama', ini=b3.T('Ahora mira Centroamérica', d=-.3), fin=b3.T('El Caribe que sobrevive', d=-.2),
         cabecera='SI CENTROAMÉRICA DESAPARECE…\n¿Y EL *CANAL DE PANAMÁ*?',
         titulo='Si Centroamérica desapareciera, el Canal de Panamá ya no haría falta 🌊 #geografia #shorts'),
    dict(n=3, nombre='brasil se queda solo', ini=b4.t0 - .2, fin=b4.T('La selva amazónica', d=-.2),
         cabecera='SIN PAÍSES HISPANOS,\n*BRASIL* SE QUEDA SOLO',
         titulo='Brasil pasaría de 10 vecinos a solo 3 😢 #geografia #brasil #shorts'),
    dict(n=4, nombre='portugal se vuelve isla', ini=b6.t0 - .2, fin=b6.T('El turismo mundial', d=-.2),
         cabecera='SI ESPAÑA DESAPARECE…\n*PORTUGAL* SE VUELVE ISLA',
         titulo='Si España desapareciera, Portugal sería una isla 🏝️ #geografia #españa #shorts'),
    dict(n=5, nombre='el nuevo hogar del espanol', ini=b6.T('Y ahora, el giro', d=-.3), fin=b6.fin + .4,
         cabecera='SIN PAÍSES HISPANOS…\n¿DÓNDE QUEDA EL *ESPAÑOL*?',
         titulo='El país con más hablantes de español sería… Estados Unidos 🇺🇸 #geografia #español #shorts'),
]

solo = int(sys.argv[sys.argv.index('--solo') + 1]) if '--solo' in sys.argv else None
SALIDA = RAIZ / 'entregas-partes'
for s in SHORTS:
    if solo and s['n'] != solo: continue
    ini, fin = round(s['ini'], 2), round(s['fin'] + 1.6, 2)
    d = DIR / 'shorts' / f"{s['n']:02d}"; d.mkdir(parents=True, exist_ok=True)
    sp = copy.deepcopy(base)
    sp.update(formato='vertical', salida='short', duracion=fin, ocultar=['barra', 'marcador', 'lista', 'region'], escalaCaras=1.55,
              offsetY=330, subY=1450, subTam=62, subColor='#ffd23f', margenInf=560, narracion=[n for n in narr if n['hasta'] > ini and n['desde'] < fin])
    sp.pop('audio', None)
    sp['eventos'] = sp['eventos'] + [
        dict(tipo='cabecera', desde=ini, hasta=fin, texto=s['cabecera'], y=140, tam=66),
        dict(tipo='pregunta', desde=round(fin - 3.4, 2), hasta=fin, texto='VIDEO COMPLETO EN EL CANAL', y=930),
    ]
    (d / 'mapa.json').write_text(json.dumps(sp, ensure_ascii=False), encoding='utf-8')
    print(f"Short {s['n']}: {ini:.1f} → {fin:.1f} s ({fin - ini:.1f} s)", flush=True)
    if '--armar' in sys.argv: continue
    subprocess.run(['node', str(RAIZ / 'motor-mapa' / 'render.cjs'), str(d), '--desde', str(ini), '--hasta', str(fin)], check=True, stdout=subprocess.DEVNULL)
    video = next(d.glob('short-tramo-*.mp4'))
    out = SALIDA / f"Short {s['n']} - {s['nombre']}.mp4"
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(video), '-ss', str(ini), '-t', str(fin - ini), '-i', str(DIR / '.tmp' / 'voz.wav'),
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', f'loudnorm=I=-14:TP=-2:LRA=11,afade=t=in:d=.15,afade=t=out:st={fin - ini - .4:.2f}:d=.4',
                    '-ar', '48000', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', str(out)], check=True)
    video.unlink()
    (d / 'titulo.txt').write_text(s['titulo'] + '\n', encoding='utf-8')
    print('   listo:', out.name, flush=True)
