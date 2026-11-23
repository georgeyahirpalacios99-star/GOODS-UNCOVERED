"""Fondo 3D para miniaturas del formato del canal: países con bandera y cara, mar azul marino, mundo alrededor.
    python3 plantillas/miniatura-mapa/fondo3d.py <clave>   (claves en FONDOS)
Deja plantillas/miniatura-mapa/fondos/<clave>.jpg (1920x1080).
"""
import json, subprocess, sys, shutil
from pathlib import Path
R = Path(__file__).resolve().parents[2]; D = Path(__file__).resolve().parent
HISP = ['MEX', 'GTM', 'HND', 'SLV', 'NIC', 'CRI', 'PAN', 'CUB', 'DOM', 'COL', 'VEN', 'ECU', 'PER', 'BOL', 'CHL', 'ARG', 'URY', 'PRY']
ISO = {'MEX': 'mx', 'GTM': 'gt', 'HND': 'hn', 'SLV': 'sv', 'NIC': 'ni', 'CRI': 'cr', 'PAN': 'pa', 'CUB': 'cu', 'DOM': 'do', 'COL': 'co', 'VEN': 've', 'ECU': 'ec',
       'PER': 'pe', 'BOL': 'bo', 'CHL': 'cl', 'ARG': 'ar', 'URY': 'uy', 'PRY': 'py', 'BRA': 'br', 'GUY': 'gy', 'SUR': 'sr', 'USA': 'us', 'BLZ': 'bz', 'HTI': 'ht', 'JAM': 'jm'}
# clave: países (protagonistas primero), caras, cámara (lon, lat, dist, inclin), elevar
FONDOS = {
    'colombia':  dict(paises=['COL', 'VEN', 'ECU', 'PER', 'BRA', 'PAN'], prota=['COL'], cam=(-80, 1.5, 135, 42), caras={'COL': 'shock', '*': 'duda'}),
    'sinaloa':   dict(paises=['MEX', 'GTM', 'BLZ'], prota=['MEX'], cam=(-112, 21, 150, 44), caras={'MEX': 'shock', '*': 'duda'}),
    'hispanos':  dict(paises=HISP + ['BRA', 'GUY', 'SUR', 'BLZ', 'HTI', 'JAM'], prota=HISP, cam=(-80, -14, 440, 30), caras={'BRA': 'feliz', '*': 'shock'}),
    'el-nino':   dict(paises=['ECU', 'PER', 'COL', 'BRA', 'BOL', 'CHL'], prota=['ECU', 'PER'], cam=(-86, -3, 150, 44), caras={'ECU': 'shock', 'PER': 'shock', '*': 'duda'}),
    'arg-bra':   dict(paises=['ARG', 'BRA', 'BOL', 'PRY', 'URY', 'CHL', 'PER', 'COL', 'VEN', 'ECU', 'GUY', 'SUR'], prota=['ARG', 'BRA'], cam=(-66, -21, 330, 38), caras={'ARG': 'shock', 'BRA': 'shock', '*': 'duda'}),
}
def hacer(clave):
    f = FONDOS[clave]; lon, lat, dist, inc = f['cam']; tmp = D / '.esc' / clave; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
    sc = dict(salida=clave, duracion=2, ancho=1920, alto=1080, centro=[lon, lat], mar='#0d2a4f', cielo='#061630', entorno='mundo',
              contexto=[lon - 70, lat - 45, lon + 70, lat + 40], calidad3d=1, sombra=2048,
              paises=[dict(adm=a, iso=ISO[a], alto=3.6 if a in f['prota'] else 2.0) for a in f['paises']],
              caras={k: [[0, v]] for k, v in f['caras'].items()}, camara=[dict(t=0, lon=lon, lat=lat, dist=dist, inclin=inc)],
              atenuar=[dict(desde=-10, hasta=9999, paises=f['prota'])], elevar=[dict(pais=a, desde=-10, altura=5) for a in f['prota']], capas=[])
    (tmp / 'escena.json').write_text(json.dumps(sc))
    subprocess.run(['node', str(R / 'motor-3d/render3d.cjs'), str(tmp), '--preview', '1'], check=True, capture_output=True)
    (D / 'fondos').mkdir(exist_ok=True); shutil.copy(tmp / 'preview' / 't1.jpg', D / 'fondos' / f'{clave}.jpg'); print('fondo', clave)
for c in (sys.argv[1:] or FONDOS): hacer(c)
