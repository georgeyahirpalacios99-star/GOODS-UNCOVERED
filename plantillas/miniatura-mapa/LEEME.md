# Formato único de miniaturas · Lo Que el Mapa No Dice

Todas las miniaturas del canal usan este formato (1280x720). Nada de caricaturas planas, fondos de cine ni fotos a sangre.

| Elemento | Regla |
|---|---|
| Fondo | Mapa 3D del canal: país protagonista con bandera, relieve y **cara de susto**; mar azul marino con cuadrícula; países vecinos con cara de duda. Lado izquierdo oscurecido para el texto. |
| Texto | Arriba a la izquierda, **2 líneas**: la 1.ª blanca, la 2.ª **amarilla #FFD23F** y más grande. Fuente Anton, borde negro. Máximo 12 letras por línea; casi siempre una pregunta (`¿SIN COLOMBIA?`). No repetir el título. |
| Foto real | **1 tarjeta** abajo a la izquierda, marco blanco, giro de 4°, con **etiqueta amarilla** (lugar, plato o dato). Solo fotos con licencia libre (Commons, NASA/NOAA). |
| Acento rojo | **1 solo** elemento rojo sobre el protagonista: círculo, flecha o insignia VS en duelos. |
| Marca | Pin amarillo con ojo, arriba a la derecha. Abajo a la derecha queda libre (ahí va la duración). |

## Cómo hacer una nueva
1. Agrega el país en `FONDOS` de `fondo3d.py` (países, protagonistas, cámara) y corre `python3 plantillas/miniatura-mapa/fondo3d.py <clave>`.
2. Agrega la entrada en `MINIS` de `miniatura.py` (2 líneas, foto, etiqueta, marca) y corre `python3 plantillas/miniatura-mapa/miniatura.py <clave>`.
3. Revisa la miniatura en tamaño pequeño (400 px de ancho), como se ve en el inicio de YouTube.

Créditos de las fotos nuevas en `fotos/creditos.json`.
