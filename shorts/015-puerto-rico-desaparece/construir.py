"""Short 015 · ¿Y si PUERTO RICO desapareciera? — mapa de caricatura (fórmula del Short de Brasil) + clips de Flow + fotos reales de Wikimedia Commons.
    python3 shorts/015-puerto-rico-desaparece/construir.py
    node motor-mapa/render.cjs shorts/015-puerto-rico-desaparece
    python3 shorts/015-puerto-rico-desaparece/sonido.py
"""
import json, math, re, shutil, subprocess, sys
from pathlib import Path
DIR = Path(__file__).resolve().parent; sys.path.insert(0, str(DIR.parent / '007-brasil-shorts'))
from alinear import Bloque, BloqueEstimado, limpiar, palabras_de
TEXTO = re.search(r'```\n(.*?)```', (DIR / 'GUION-CAPCUT.md').read_text(encoding='utf-8'), re.S).group(1)
INICIO = .15
mp3 = sorted((DIR / 'voz').glob('*.mp3'))
if mp3: limpiar(mp3[0], DIR / 'voz' / 'limpia.wav'); b = Bloque(1, TEXTO, INICIO, DIR / 'voz' / 'limpia.wav'); CON_VOZ = True
else: b = BloqueEstimado(1, TEXTO, INICIO); CON_VOZ = False
T = b.T; DUR = round(b.fin + 1.2, 2)
cam, ev, CLIPS, sacud, DESAP, caras = [], [], [], [], [], {'*': [[0, 'normal']]}
ultimo = [None]
def CAM(t, lon, lat, ancho, d=.55):
    if ultimo[0]: lo, la, an = ultimo[0]; cam.append(dict(t=round(t, 2), lon=lo, lat=la, ancho=an, suave=False))
    cam.append(dict(t=round(t + d, 2), lon=lon, lat=lat, ancho=ancho)); ultimo[0] = (lon, lat, ancho)
def E(tipo, desde, dur=None, hasta=None, **kw):
    e = dict(tipo=tipo, desde=round(desde, 2), **kw)
    if hasta is not None: e['hasta'] = round(hasta, 2)
    elif dur is not None: e['hasta'] = round(desde + dur, 2)
    ev.append(e); return e
def cara(p, t, ex): caras.setdefault(p, []).append([round(t, 2), ex])
IA = 'IMAGEN ILUSTRATIVA CON IA'
def clip(cod, a0, a1, maxdur=7.6, **ex):
    d = a1 - a0; ex.setdefault('vel', round(min(1, (maxdur - ex.get('ofs', 0)) / max(.1, d)), 3)); ex.setdefault('etiqueta', IA); CLIPS.append(dict(codigo=cod, desde=round(a0, 2), hasta=round(a1, 2), **ex))
FOTOS = {}
def foto(cod, img, a0, a1, mov, credito):
    """Foto real con movimiento de cámara: mov = (zoom inicial, zoom final, foco x/y inicial, foco x/y final)."""
    FOTOS[cod] = dict(img=img, mov=mov, n=int(math.ceil((a1 - a0) * 30)) + 3); CLIPS.append(dict(codigo=cod, desde=round(a0, 2), hasta=round(a1, 2), etiqueta='FOTO: ' + credito, vel=1, z0=1, z1=1))
def desaparece(iso, t): DESAP.append(dict(iso=iso, t=round(t, 2))); sacud.append(dict(t=round(t, 2), dur=.9, fuerza=22))
NOM, CIF, CINTA = 330, 360, 1185
CARIBE = (-68.5, 18.6, 11)
VECINOS = ['DOM', 'HTI', 'CUB', 'JAM', 'VEN', 'COL', 'USA', 'MEX', 'BHS']

# ---------- gancho: la isla se pierde entre las nubes ----------
clip('R01', 0, T('Una isla que', d=-.05), entra=.01, z0=1.0, z1=1.06)
E('titulo', .1, texto='¿Y SI *PUERTO RICO*\nDESAPARECE?', tam=96, y=NOM, capa='C', hasta=T('Una isla que', d=-.1))
CAM(0, *CARIBE, d=0); cara('PRI', 0, 'feliz')
E('resaltar', T('Una isla que'), pais='PRI', color='#ffd23f', hasta=T('y sin embargo'))
E('cifra', T('Una isla que', d=.2), texto='9,100 km²', num=[0, 9100], suf=' km²', dur=.8, tam=160, sub='menos de la mitad de El Salvador', y=CIF, hasta=T('y sin embargo'))
T_DES = T('el mundo entero', d=-.1); desaparece('PRI', T_DES)
for p in VECINOS: cara(p, T_DES + .45, 'shock')
E('titulo', T('lo notaría', d=-.1), texto='EL MUNDO\n*LO NOTARÍA*', tam=100, y=NOM, capa='C', hasta=T('Primero', d=-.1))
# ---------- 1 · la música ----------
clip('R04', T('Primero', d=-.05), T('Bad Bunny.', d=-.05), maxdur=7.6)
E('titulo', T('se apagaría', d=-.1), texto='SE APAGA\nLA *MÚSICA*', tam=110, y=NOM, capa='C', hasta=T('Bad Bunny.', d=-.1))
foto('F1', 'bad-bunny-retrato.jpg', T('Bad Bunny.', d=-.05), T('En febrero', d=-.05), (1.05, 1.22, (.5, .33), (.5, .3)), 'GLENN FRANCIS · CC BY-SA 4.0')
E('titulo', T('Bad Bunny.'), texto='*BAD BUNNY*', tam=130, y=NOM, capa='C', hasta=T('El artista', d=-.1))
E('cifra', T('El artista', d=.1), texto='#1', tam=230, sub='más escuchado del mundo en Spotify · 4.ª vez', y=CIF, hasta=T('En febrero', d=-.1))
foto('F2', 'bad-bunny-residencia.webp', T('En febrero', d=-.05), T('Y una semana', d=-.05), (1.0, 1.25, (.5, .5), (.42, .45)), 'AJ83400 · CC BY-SA 4.0')
E('titulo', T('En febrero'), texto='GRAMMY AL\n*ÁLBUM DEL AÑO*', tam=96, y=NOM, capa='C', hasta=T('el primero en español', d=-.1))
E('titulo', T('el primero en español', d=-.1), texto='EL PRIMERO\n*EN ESPAÑOL*', tam=110, y=NOM, capa='C', hasta=T('Y una semana', d=-.1))
foto('F3', 'bad-bunny-concierto.jpg', T('Y una semana', d=-.05), T('Su residencia', d=-.05), (1.0, 1.3, (.5, .5), (.42, .35)), 'COMECOQUITO · CC0')
E('titulo', T('Y una semana'), texto='*SUPER BOWL*', tam=130, y=NOM, capa='C', hasta=T('frente a más', d=-.1))
E('cifra', T('ciento veinte millones', d=-.15), texto='+120 MILLONES', num=[0, 120], pre='+', suf=' MILLONES', dur=.9, tam=130, sub='lo vieron solo en Estados Unidos', y=CIF, hasta=T('Su residencia', d=-.1))
clip('R04', T('Su residencia', d=-.05), T('Sin Puerto Rico', d=-.05), maxdur=7.6, ofs=3.5)
E('cifra', T('cerca de doscientos', d=-.15), texto='$200 MILLONES', num=[0, 200], pre='$', suf=' MILLONES', dur=.9, tam=130, sub='dejó su residencia en la isla (2025)', y=CIF, color='#7dffa0', hasta=T('Sin Puerto Rico', d=-.1))
foto('F4', 'daddy-yankee.jpg', T('Sin Puerto Rico', d=-.05), T('Pero no solo', d=-.05), (1.0, 1.25, (.5, .4), (.5, .32)), 'APOXYOMENUS · CC BY-SA 4.0')
E('titulo', T('Daddy Yankee', d=-.1), texto='*DADDY YANKEE*', tam=120, y=NOM, capa='C', hasta=T('Ni "Despacito"', d=-.1))
E('cinta', T('"Gasolina"', d=-.1), x=960, y=CINTA, escala=1.2, texto='"GASOLINA"', icono='', color='#c0392b', hasta=T('Pero no solo', d=-.1))
E('titulo', T('Ni "Despacito"', d=-.1), texto='Y *"DESPACITO"*', tam=120, y=NOM, capa='C', hasta=T('Pero no solo', d=-.1))
# ---------- 2 · medicinas ----------
clip('R03', T('Pero no solo', d=-.05), T('Y lo más raro', d=-.05), maxdur=7.6)
E('cifra', T('casi una de cada cinco', d=-.15), texto='1 DE CADA 5', tam=170, sub='medicinas que EE. UU. le vende al mundo', y=CIF, color='#4ea3ff', hasta=T('Y lo más raro', d=-.1))
# ---------- 3 · la diáspora ----------
CAM(T('Y lo más raro', d=-.15), -78, 30, 44, d=.8)
E('flujo', T('más puertorriqueños', d=-.2), de=[-66.4, 18.2], a=[-74, 40.7], n=7, hasta=T('Una isla pequeña'))
E('flujo', T('viviendo en Estados Unidos', d=-.2), de=[-66.4, 18.2], a=[-81.4, 28.5], n=5, hasta=T('Una isla pequeña'))
E('barras', T('Casi seis millones', d=-.1), titulo='PUERTORRIQUEÑOS', y=1100, ancho=300, alto=420, dec=1, suf=' M', items=[dict(valor=5.9, texto='EN EE. UU.', color='#4ea3ff', desde=round(T('Casi seis millones', d=-.1), 2)), dict(valor=3.2, texto='EN LA ISLA', color='#ffd23f', desde=round(T('contra unos tres', d=-.1), 2))], hasta=T('Una isla pequeña', d=-.1))
# ---------- cierre ----------
clip('R02', T('Una isla pequeña', d=-.05), T('¿Cuál es', d=-.05), maxdur=7.6)
E('titulo', T('Una isla pequeña'), texto='UNA ISLA *PEQUEÑA*…', tam=100, y=NOM, capa='C', hasta=T('que mueve', d=-.1))
E('titulo', T('que mueve', d=-.1), texto='QUE MUEVE\nAL *MUNDO*', tam=120, y=NOM, capa='C', hasta=T('¿Cuál es', d=-.1))
CAM(T('¿Cuál es', d=-.15), *CARIBE, d=0)
E('pregunta', T('¿Cuál es'), texto='¿TU CANCIÓN BORICUA FAVORITA? 👇', y=CINTA, hasta=DUR)
tits = sorted([e for e in ev if e['tipo'] == 'titulo'], key=lambda e: e['desde'])
for e1, e2 in zip(tits, tits[1:]):
    if e1.get('hasta', 1e9) > e2['desde'] - .05: e1['hasta'] = round(e2['desde'] - .05, 2)
DESTELLOS = [round(T_DES, 2), round(T('En febrero'), 2), round(T('Y una semana'), 2)]
for c in CLIPS:
    cod, dst = c['codigo'], DIR / '.clips' / c['codigo']
    if cod in FOTOS:
        f = FOTOS[cod]; (z0, z1, (x0, y0), (x1, y1)), n = f['mov'], f['n']; shutil.rmtree(dst, ignore_errors=True); dst.mkdir(parents=True)
        u = f"(1-pow(1-on/{n - 1}\\,2))"; z = f"({z0}+({z1 - z0})*{u})"; fx = f"({x0}+({x1 - x0})*{u})"; fy = f"({y0}+({y1 - y0})*{u})"
        vf = f"scale=3240:5760:force_original_aspect_ratio=increase:flags=lanczos,crop=3240:5760,zoompan=z='{z}':x='{fx}*iw-iw/zoom/2':y='{fy}*ih-ih/zoom/2':d={n}:s=1080x1920:fps=30"
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(DIR / 'fotos-reales' / f['img']), '-vf', vf, '-frames:v', str(n), '-q:v', '3', str(dst / '%04d.jpg')], check=True)
    elif not dst.exists():
        dst.mkdir(parents=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(DIR / 'clips' / f'{cod}.mp4'), '-vf', 'scale=1080:1920:flags=lanczos,fps=30', '-q:v', '3', str(dst / '%04d.jpg')], check=True)
cam.sort(key=lambda k: (k['t'], k.get('suave') is not False))
for i in range(1, len(cam)):
    if cam[i]['t'] <= cam[i - 1]['t']: cam[i]['t'] = round(cam[i - 1]['t'] + .02, 2)
spec = dict(estilo='caricatura', formato='vertical', salida='si-puerto-rico-desapareciera', duracion=DUR, camara=cam, desaparece=DESAP, sacudidas=sacud, caras=caras, eventos=sorted(ev, key=lambda e: e['desde']),
            clips=CLIPS, palabras=palabras_de(b), resaltar=['PUERTO', 'RICO', 'MÚSICA', 'BAD', 'BUNNY', 'GRAMMY', 'ESPAÑOL', 'SUPER', 'BOWL', 'MILLONES', 'DADDY', 'YANKEE', 'GASOLINA', 'DESPACITO', 'MEDICINAS', 'MUNDO', 'BORICUA', 'SPOTIFY'],
            capY=1500, capTam=74, capEstilo='caja', tipografia='cine', tituloClave='texto', capColor='#ffd23f', capTextoClave='#0b0f14', fundido_inicio=0, barra=True, destellos=DESTELLOS)
if CON_VOZ:
    tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(DIR / 'voz' / 'limpia.wav'), '-af', f'adelay={int(INICIO * 1000)},apad=whole_dur={DUR},loudnorm=I=-16:TP=-2:LRA=11', '-ar', '48000', '-ac', '1', str(tmp / 'voz.wav')], check=True)
    spec['audio'] = '.tmp/voz.wav'
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
if CON_VOZ: b.informe()
print(f"Short 015 · {'CON VOZ' if CON_VOZ else 'SIN VOZ'} · {len(ev)} capas · {len(CLIPS)} clips · {DUR:.1f} s")
