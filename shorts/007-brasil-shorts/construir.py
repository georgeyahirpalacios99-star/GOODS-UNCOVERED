"""Shorts 007 · "Si Brasil desapareciera" — 3 Shorts verticales con mapas animados + clips de Flow + subtítulo por palabra.
    python3 shorts/007-brasil-shorts/construir.py a        (a, b o c; con voz en <letra>/voz/*.mp3 si existe; si no, tiempos estimados)
    node motor-mapa/render.cjs shorts/007-brasil-shorts/a
    python3 shorts/007-brasil-shorts/sonido.py a
"""
import json, re, subprocess, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parent; sys.path.insert(0, str(RAIZ))
from alinear import Bloque, BloqueEstimado, limpiar, palabras_de
LETRA = sys.argv[1] if len(sys.argv) > 1 else 'a'; DIR = RAIZ / LETRA
CLIPSRC = RAIZ.parents[1] / 'videos-largos' / '004-brasil-desaparece' / 'clips'
TEXTO = re.findall(r'```\n(.*?)```', (RAIZ / 'GUION-ELEVENLABS.md').read_text(encoding='utf-8'), re.S)['abc'.index(LETRA)]
INICIO = .15
mp3 = sorted((DIR / 'voz').glob('*.mp3'))
if mp3: limpiar(mp3[0], DIR / 'voz' / 'limpia.wav'); b = Bloque(1, TEXTO, INICIO, DIR / 'voz' / 'limpia.wav'); CON_VOZ = True
else: b = BloqueEstimado(1, TEXTO, INICIO); CON_VOZ = False
T = b.T; DUR = round(b.fin + 1.0, 2)

cam, ev, caras, sacud, DESAP, CLIPS = [], [], {'*': [[0, 'normal']]}, [], [], []
ultimo = [None]
def CAM(t, lon, lat, ancho, d=.55, arco=0):
    """Mueve la cámara a (lon, lat, ancho) en d segundos empezando en t (se queda quieta hasta t)."""
    if ultimo[0]: lo, la, an = ultimo[0]; cam.append(dict(t=round(t, 2), lon=lo, lat=la, ancho=an, suave=False))
    cam.append(dict(t=round(t + d, 2), lon=lon, lat=lat, ancho=ancho, **({'arco': arco} if arco else {}))); ultimo[0] = (lon, lat, ancho)
def E(tipo, desde, dur=None, hasta=None, **kw):
    e = dict(tipo=tipo, desde=round(desde, 2), **kw)
    if hasta is not None: e['hasta'] = round(hasta, 2)
    elif dur is not None: e['hasta'] = round(desde + dur, 2)
    ev.append(e); return e
def cara(p, t, ex): caras.setdefault(p, []).append([round(t, 2), ex])
def clip(cod, a0, a1, **ex): CLIPS.append(dict(codigo=cod, desde=round(a0, 2), hasta=round(a1, 2), **ex))
def desaparece(iso, t): DESAP.append(dict(iso=iso, t=round(t, 2))); sacud.append(dict(t=round(t, 2), dur=.9, fuerza=22))
TIT, CIF, CINTA, ICO = 300, 330, 1185, 690           # alturas en el formato vertical (1080 × 1920)
SA = ['ARG', 'BOL', 'CHL', 'COL', 'ECU', 'GUY', 'PRY', 'PER', 'SUR', 'URY', 'VEN']
SUDAM = (-60, -22, 56)
ITAIPU, IGUAZU, CURITIBA, LETICIA, IQUITOS = (-54.59, -25.41), (-54.44, -25.69), (-49.27, -25.43), (-69.94, -4.21), (-73.25, -3.75)

if LETRA == 'a':   # ============ Bolivia tendría MAR ============
    RESALTAR = ['BRASIL', 'MAR', 'BOLIVIA', 'PLAYA', 'PARAGUAY', 'URUGUAY', 'ISLA', 'AMAZONAS', 'LETICIA', 'LUZ', 'DOS']
    clip('B01', 0, T('desapareciera mañana', d=.35), entra=.01, z0=1.0, z1=1.12)
    CAM(0, -53, -14, 48, d=0); CAM(.05, -53, -14, 42, d=1.8)
    E('titulo', .1, texto='¿Y SI *BRASIL*\nDESAPARECE?', tam=104, y=TIT, hasta=T('Casi la mitad'))
    T_DES = T('mañana', d=.45); desaparece('BRA', T_DES); cara('BRA', 0, 'feliz')
    for p in ['BOL', 'PRY', 'URY', 'ARG', 'PER', 'COL', 'VEN', 'GUY', 'SUR']: cara(p, T_DES + .45, 'shock')
    CAM(T('Casi la mitad'), *SUDAM)
    E('cifra', T('Casi la mitad'), texto='≈ 47 %', tam=170, sub='de Sudamérica… ¡desaparece!', y=CIF, hasta=T('se convierte en mar'))
    clip('B02', T('se convierte en mar', d=-.1), T('Y el primero', d=-.05))
    E('titulo', T('se convierte en mar'), texto='SOLO… *MAR*', tam=120, y=TIT, hasta=T('Y el primero'))
    CAM(T('Y el primero'), -63.5, -16.5, 15)
    E('resaltar', T('Y el primero'), pais='BOL', color='#ffd23f', hasta=T('y de pronto'))
    cara('BOL', T('Y el primero'), 'sorpresa'); E('globo', T('celebrarlo', d=.2), pais='BOL', texto='¿¡Yo, con playa!?', lado=1, hasta=T('Perdió su costa'))
    CAM(T('Perdió su costa'), -66.5, -20.5, 19)
    E('pin', T('Perdió su costa', d=.2), lon=-70.4, lat=-23.6, texto='LITORAL · 1879', escala=1.6, hasta=T('y de pronto'))
    E('cifra', T('Perdió su costa'), texto='1879', tam=190, sub='Bolivia pierde su mar', y=CIF, hasta=T('y de pronto')); cara('BOL', T('Perdió su costa'), 'triste')
    clip('B03', T('y de pronto', d=-.1), T('Paraguay, que nunca', d=-.05), z0=1.0, z1=1.1)
    E('cinta', T('más de tres mil'), x=960, y=CINTA, escala=1.25, texto='BOLIVIA: +3,423 km DE PLAYA', icono='barco', color='#1f6aa8', hasta=T('Paraguay, que nunca'))
    cara('BOL', T('y de pronto'), 'risa')
    CAM(T('Paraguay, que nunca', d=-.05), -58, -23.5, 12)
    E('resaltar', T('Paraguay, que nunca'), pais='PRY', color='#ffd23f', hasta=T('Pero el caso')); cara('PRY', T('Paraguay, que nunca'), 'feliz')
    E('nombre', T('también', d=-.3), texto='PARAGUAY +1,365 km', lon=-56.6, lat=-21.4, tam=40, hasta=T('Pero el caso'))
    CAM(T('Pero el caso más raro'), -56.2, -33, 8.5)
    E('resaltar', T('Pero el caso más raro'), pais='URY', color='#ffd23f', hasta=T('Y el río Amazonas')); cara('URY', T('Pero el caso más raro'), 'sorpresa')
    E('nombre', T('solo lo separa un río'), texto='RÍO URUGUAY', lon=-58.25, lat=-31.7, tam=34, hasta=T('Y el río Amazonas'))
    E('iconos', T('se convertiría en una isla'), y=ICO, paso=0, escala=2.0, items=[dict(icono='isla', texto='')], hasta=T('Y el río Amazonas'))
    E('cinta', T('se convertiría en una isla'), x=960, y=CINTA, escala=1.3, texto='URUGUAY ES UNA ISLA', icono='isla', color='#1f6aa8', hasta=T('Y el río Amazonas')); cara('URY', T('una isla'), 'risa')
    CAM(T('Y el río Amazonas'), -70.8, -3.9, 11)
    E('flujo', T('Y el río Amazonas'), de=list(IQUITOS), a=list(LETICIA), icono='gota', n=5, hasta=T('Lo peor'))
    E('pin', T('Terminaría en Leticia'), lon=LETICIA[0], lat=LETICIA[1], texto='LETICIA: FIN DEL AMAZONAS', escala=1.5, hasta=T('Lo peor')); cara('COL', T('Terminaría en Leticia'), 'sorpresa')
    CAM(T('Lo peor'), -58, -23.5, 12)
    E('apagon', T('la luz de Paraguay', d=.25), dur=2.0, fuerza=.72, foco=True); cara('PRY', T('la luz de Paraguay'), 'grito')
    E('titulo', T('pero eso te lo cuento'), texto='PARTE *2* →', tam=130, y=TIT, hasta=DUR)
    E('pregunta', T('en la parte dos'), texto='¿QUÉ LE PASA A PARAGUAY?', y=CINTA, hasta=DUR)

elif LETRA == 'b':   # ============ Iguazú se SECA ============
    RESALTAR = ['BRASIL', 'IGUAZÚ', 'CATARATAS', 'HILO', 'SECA', 'ITAIPÚ', 'LUZ', 'PARAGUAY', 'OSCURAS', 'ARGENTINA', 'LLUVIA']
    clip('B14', 0, T('esto le pasaría', d=.05), entra=.01)
    E('titulo', .1, texto='SI *BRASIL*\nDESAPARECE…', tam=110, y=TIT, hasta=T('esto le pasaría'))
    clip('B15', T('esto le pasaría', d=.05), T('Hoy el agua', d=-.05), z0=1.05, z1=1.15)
    E('titulo', T('esto le pasaría', d=.05), texto='¿IGUAZÚ… *SECO*?', tam=110, y=TIT, hasta=T('Hoy el agua'))
    clip('B14', T('Hoy el agua', d=-.05), T('Pero el río Iguazú', d=-.05), ofs=2.5)
    E('cifra', T('doscientos setenta'), texto='275 SALTOS', tam=150, sub='de agua, hoy', y=CIF, hasta=T('Pero el río Iguazú'))
    CAM(0, -52.5, -25.4, 10, d=0); CAM(T('Pero el río Iguazú', d=-.1), -52, -25.5, 9.5, d=.01)
    E('pin', T('Pero el río Iguazú'), lon=IGUAZU[0], lat=IGUAZU[1], texto='CATARATAS', escala=1.5, hasta=T('Sin Brasil'))
    E('nombre', T('cerca de Curitiba'), texto='CURITIBA', lon=CURITIBA[0], lat=CURITIBA[1], tam=36, hasta=T('Sin Brasil'))
    E('flujo', T('nace en Brasil'), de=list(CURITIBA), a=list(IGUAZU), icono='gota', n=7, hasta=T('Sin Brasil'))
    E('cifra', T('recorre más de mil'), texto='+1,000 km', tam=150, sub='de río dentro de Brasil', y=CIF, hasta=T('Sin Brasil'))
    T_DES = T('Sin Brasil', d=.2); desaparece('BRA', T_DES)
    E('flujo', T_DES, de=list(CURITIBA), a=list(IGUAZU), icono='gota', n=3, roto=True, hasta=T('apenas un hilo'))
    cara('ARG', T_DES + .4, 'shock'); cara('PRY', T_DES + .4, 'shock')
    clip('B15', T('apenas un hilo', d=-.35), T('Y no sería', d=-.05), ofs=1.0, z0=1.0, z1=1.12)
    E('cinta', T('apenas un hilo'), x=960, y=CINTA, escala=1.25, texto='APENAS UN HILO DE AGUA', icono='gota', color='#d6453d', hasta=T('Y no sería'))
    E('sello', T('hilo de agua', d=.25), x=960, y=CIF, texto='CASI SECA', tam=1.6, hasta=T('Y no sería'))
    CAM(T('Y no sería', d=-.1), -55.8, -25.2, 9)
    E('titulo', T('Y no sería'), texto='Y NO ES LO *PEOR*…', tam=104, y=TIT, hasta=T('Itaipú, la represa')); cara('PRY', T('Y no sería'), 'preocupado')
    clip('B12', T('Itaipú, la represa', d=-.1), T('también depende', d=-.05))
    E('cifra', T('casi el ochenta'), texto='87.6 %', tam=160, sub='de la luz de Paraguay sale de aquí', y=CIF, hasta=T('también depende'))
    E('pin', T('también depende'), lon=ITAIPU[0], lat=ITAIPU[1], texto='ITAIPÚ', escala=1.6, hasta=T('Sin río'))
    E('flujo', T('también depende'), de=[-51.5, -21.5], a=list(ITAIPU), icono='gota', n=4, roto=True, hasta=T('Sin río'))
    clip('B13', T('Sin río', d=-.1), T('Paraguay se quedaría', d=-.05), ofs=1.0)
    E('titulo', T('Sin río'), texto='SIN RÍO,\nNO HAY *LUZ*', tam=110, y=TIT, hasta=T('Paraguay se quedaría'))
    CAM(T('Paraguay se quedaría', d=-.1), -58, -23.5, 12)
    E('apagon', T('casi a oscuras', d=-.1), dur=2.0, fuerza=.75, foco=True); cara('PRY', T('Paraguay se quedaría'), 'grito')
    CAM(T('¿Y Argentina?', d=-.05), -62, -31, 24)
    cara('ARG', T('¿Y Argentina?'), 'preocupado'); E('resaltar', T('¿Y Argentina?'), pais='ARG', color='#4ea3ff', hasta=DUR)
    E('flujo', T('Se quedaría sin la lluvia'), de=[-62, -14], a=[-62, -32], icono='nube', n=4, roto=True, hasta=T('Pero esa es'))
    E('titulo', T('Pero esa es otra'), texto='ESA ES OTRA\n*HISTORIA*…', tam=104, y=TIT, hasta=DUR)
    E('pregunta', T('otra historia'), texto='PARTE 3 EN EL CANAL →', y=CINTA, hasta=DUR)

else:   # ============ Tu desayuno depende de UN país ============
    RESALTAR = ['DESAYUNO', 'BRASIL', 'CAFÉ', 'NARANJA', 'AZÚCAR', 'LLUVIA', 'AMAZONÍA', 'AMAZONAS', 'ARGENTINA', 'NUNCA']
    clip('B07', 0, T('Cuatro de cada diez', d=-.05), entra=.01)
    E('titulo', .1, texto='TU DESAYUNO\nDEPENDE DE *1 PAÍS*', tam=96, y=TIT, hasta=T('Cuatro de cada diez'))
    CAM(0, -40, 8, 130, d=0); CAM(T('Cuatro de cada diez', d=-.1), -42, 8, 118, d=1.2)
    E('resaltar', T('Cuatro de cada diez'), pais='BRA', color='#ffd23f', hasta=T('Si Brasil desapareciera')); cara('BRA', T('Cuatro de cada diez'), 'feliz')
    for a in [[-95, 38], [10, 50], [138, 37]]: E('flujo', T('Cuatro de cada diez', d=.2), de=[-48, -15], a=a, icono='cafe', n=5, hasta=T('Si Brasil desapareciera'))
    E('cifra', T('Cuatro de cada diez'), texto='4 DE CADA 10', tam=140, sub='granos de café del mundo', y=CIF, hasta=T('Tres de cada cuatro'))
    E('iconos', T('Tres de cada cuatro'), y=ICO, paso=0, escala=1.8, items=[dict(icono='naranja', texto='')], hasta=T('Y la mitad'))
    E('cifra', T('Tres de cada cuatro'), texto='3 DE CADA 4', tam=140, sub='vasos de jugo de naranja', y=CIF, hasta=T('Y la mitad'))
    E('iconos', T('Y la mitad'), y=ICO, paso=0, escala=1.8, items=[dict(icono='azucar', texto='')], hasta=T('Si Brasil desapareciera'))
    E('cifra', T('Y la mitad'), texto='≈ 50 %', tam=160, sub='del azúcar que se exporta', y=CIF, hasta=T('Si Brasil desapareciera'))
    CAM(T('Si Brasil desapareciera', d=-.1), -53, -14, 44, d=.5)
    E('resaltar', T('Si Brasil desapareciera'), pais='BRA', color='#ff3b30', hasta=T('tu desayuno costaría')); cara('BRA', T('Si Brasil desapareciera'), 'shock'); sacud.append(dict(t=round(T('desapareciera mañana'), 2), dur=.6, fuerza=14))
    clip('B07', T('tu desayuno costaría', d=-.1), T('Pero lo más raro', d=-.05), ofs=3.6)
    E('cinta', T('costaría mucho más'), x=960, y=CINTA, escala=1.3, texto='TODO SUBE DE PRECIO', icono='dolar', color='#d6453d', hasta=T('Pero lo más raro'))
    CAM(T('Pero lo más raro', d=-.1), -60, -6, 34)
    E('titulo', T('Pero lo más raro'), texto='LO MÁS *RARO*…', tam=110, y=TIT, hasta=T('Brasil también exporta')); cara('BRA', T('Pero lo más raro'), 'normal')
    clip('B10', T('Brasil también exporta', d=-.1), T('Más de lo que', d=-.05), vel=.8)
    E('titulo', T('Brasil también exporta'), texto='BRASIL EXPORTA…\n*LLUVIA*', tam=110, y=TIT, hasta=T('Los árboles'))
    E('cifra', T('veinte mil millones'), texto='20,000 MILLONES', tam=118, sub='de toneladas de agua al aire, cada día', y=CIF, hasta=T('Más de lo que'))
    E('flujo', T('Más de lo que'), de=[-69, -4], a=[-50, -.5], icono='gota', n=6, hasta=T('Ese vapor'))
    E('iconos', T('Más de lo que'), y=ICO, paso=.4, gap=380, escala=1.5, items=[dict(icono='nube', texto='AL CIELO'), dict(icono='gota', texto='AL MAR')], hasta=T('Ese vapor'))
    CAM(T('Ese vapor', d=-.1), *SUDAM)
    E('flujo', T('Ese vapor'), de=[-58, -4], a=[-67, -14], icono='nube', n=5, hasta=T('Sin Brasil'))
    E('flujo', T('Ese vapor', d=.6), de=[-67, -14], a=[-61, -30], icono='nube', n=5, hasta=T('Sin Brasil'))
    for p in ['BOL', 'PRY', 'ARG']: E('resaltar', T('cae como lluvia'), pais=p, color='#4ea3ff', hasta=T('Sin Brasil')); cara(p, T('cae como lluvia'), 'feliz')
    T_DES = T('Sin Brasil', d=.1); desaparece('BRA', T_DES)
    E('flujo', T_DES + .3, de=[-67, -14], a=[-61, -30], icono='nube', n=4, roto=True, hasta=T('se quedaría esperando'))
    for p in ['BOL', 'PRY', 'ARG']: cara(p, T_DES + .4, 'shock')
    clip('B11', T('se quedaría esperando', d=-.2), DUR, z0=1.0, z1=1.12)
    E('titulo', T('se quedaría esperando'), texto='UNA LLUVIA QUE\n*NUNCA LLEGA*', tam=96, y=TIT, hasta=DUR)

# ---------- clips verticales: fondo difuminado + el clip 16:9 a lo ancho (sin perder calidad) ----------
for c in CLIPS:
    dst = DIR / '.clips' / c['codigo']
    if not dst.exists():
        dst.mkdir(parents=True)
        f = ('[0]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:3,eq=brightness=-0.12:saturation=1.15[bg];'
             '[0]scale=1188:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-160,fps=30')
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(CLIPSRC / f"{c['codigo']}.mp4"), '-filter_complex', f, '-q:v', '3', str(dst / '%04d.jpg')], check=True)
cam.sort(key=lambda k: k['t'])
for i in range(1, len(cam)):
    if cam[i]['t'] <= cam[i - 1]['t']: cam[i]['t'] = round(cam[i - 1]['t'] + .02, 2)
for k in caras.values(): k.sort()
spec = dict(estilo='caricatura', formato='vertical', salida=f'si-brasil-desapareciera-{LETRA}', duracion=DUR, camara=cam, desaparece=DESAP, sacudidas=sacud,
            tam={'URY': 1.5, 'PRY': 1.4, 'BOL': 1.3, 'ECU': 1.3, 'GUY': 1.4, 'SUR': 1.5, 'CHL': 1.1, 'ARG': 1.1}, caras=caras, eventos=sorted(ev, key=lambda e: e['desde']),
            clips=CLIPS, palabras=palabras_de(b), resaltar=RESALTAR, capY=1420, capTam=112, fundido_inicio=0)
if CON_VOZ:
    tmp = DIR / '.tmp'; tmp.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(DIR / 'voz' / 'limpia.wav'), '-af', f'adelay={int(INICIO * 1000)},apad=whole_dur={DUR},loudnorm=I=-16:TP=-2:LRA=11', '-ar', '48000', '-ac', '1', str(tmp / 'voz.wav')], check=True)
    spec['audio'] = '.tmp/voz.wav'
(DIR / 'mapa.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
print(f"Short {LETRA.upper()} · {'CON VOZ' if CON_VOZ else 'SIN VOZ (tiempos estimados)'} · {len(ev)} capas · {len(CLIPS)} clips · {DUR:.1f} s")
