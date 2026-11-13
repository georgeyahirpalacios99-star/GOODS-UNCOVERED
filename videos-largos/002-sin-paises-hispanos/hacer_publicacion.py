"""Escribe 05-PUBLICACION.md con los capítulos según los tiempos reales de mapa.json."""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent
spec = json.loads((D / 'mapa.json').read_text(encoding='utf-8'))
reg = [e for e in spec['eventos'] if e['tipo'] == 'region']
mm = lambda s: f"{int(s // 60)}:{int(s % 60):02d}"
caps = [(0, 'Borramos 21 territorios')]
nombres = {'NORTEAMÉRICA': 'Estados Unidos, Canadá y Belice', 'EL CARIBE': 'El Caribe y el Canal de Panamá', 'SUDAMÉRICA': 'Brasil se queda solo', 'EL MUNDO': 'Lo que el mundo deja de recibir', 'EUROPA': 'Europa, África y el idioma', 'EL VEREDICTO': 'Quién llora y quién ni se entera'}
for e in reg:
    if e['texto'] in nombres and nombres[e['texto']] not in [c[1] for c in caps]: caps.append((max(0, e['desde'] - 1), nombres[e['texto']]))
cap_txt = '\n'.join(f'{mm(t)} {n}' for t, n in caps)
(D / '05-PUBLICACION.md').write_text(f"""# PUBLICACIÓN · Video 002
**Duración: {mm(spec['duracion'])} · Miniatura recomendada: `miniaturas/miniatura-D.jpg`**

## Título
```
¿Qué pasaría si desaparecieran TODOS los países que hablan español?
```

## Descripción
```
21 territorios borrados del mapa en un segundo: México, Centroamérica, casi toda Sudamérica, Cuba, República Dominicana, Puerto Rico, España y Guinea Ecuatorial. ¿Qué le pasaría al resto del mundo?

Brasil se queda con solo tres vecinos, Portugal se convierte en una isla, el Atlántico y el Pacífico se juntan sin el Canal de Panamá… y el país con más hablantes de español pasaría a ser Estados Unidos.

Escenario hipotético, contado con datos reales.

⏱️ CAPÍTULOS
{cap_txt}

📚 FUENTES
Instituto Cervantes, El español en el mundo 2025
Oficina del Censo de EE. UU. (estimaciones 2024 y ACS 2024)
Departamento de Agricultura de EE. UU. (USDA ERS): importaciones de aguacate
Asocolflores: exportaciones de flores de Colombia
FAO: Banana Statistical Compendium
Banco Central del Ecuador: exportaciones de camarón
USGS, Mineral Commodity Summaries 2026 (cobre y litio)
The Silver Institute, World Silver Survey 2026
Ministerio de Agricultura de España (aceite de oliva)
INE / Frontur 2025 (turismo en España)

Mapas: Natural Earth (dominio público). Banderas: flag-icons (licencia MIT).

#QuéPasaríaSi #Geografía #Mapas #Español #Latinoamérica #España #Curiosidades
```

## Etiquetas
```
qué pasaría si, qué pasaría si desaparecieran los países que hablan español, países que hablan español, países hispanohablantes, mapa del mundo, geografía, curiosidades del mundo, latinoamérica, españa, méxico, brasil, idioma español, mapas animados, countryballs, qué pasaría si méxico desapareciera
```

## Configuración
| Campo | Qué elegir |
|---|---|
| Miniatura | `miniaturas/miniatura-D.jpg` |
| Lista de reproducción | Nueva: **¿Qué pasaría si…?** |
| Público | No es para niños |
| Contenido alterado o sintético | **Sí** (voz generada con IA) |
| Idioma del video | Español |
| Categoría | Educación |
| Capítulos automáticos | Activados (ya van en la descripción) |
| Pantalla final | Últimos 20 s: 1 video + Suscribirse |
| Hora | 19:00 hora de Ecuador |

## Comentario fijado
```
¿Qué crees que extrañaría más el mundo de TU país? 👇 El país con más votos es el próximo que borramos.
```

## Shorts del mismo video (cortar en vertical)
1. Belice se convierte en una isla.
2. Brasil pasa de 10 vecinos a 3.
3. Portugal ahora es una isla.
4. El país con más hablantes de español sería… Estados Unidos.
""", encoding='utf-8')
print('ok', cap_txt)
