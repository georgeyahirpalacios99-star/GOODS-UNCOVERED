# MOTOR DE SHORTS · edición automática

Convierte **voz + imágenes + guion** en un Short terminado (1080×1920, 30 fps), sin CapCut.

## Qué hace solo
- Corta el video en cada pausa de la voz: una imagen por línea del guion
- Zoom lento y movimiento sobre cada imagen, golpe de zoom y destello blanco en cada corte
- Contador `#1`, `#2`…, título del récord arriba y la respuesta en caja naranja cuando la voz la dice
- Subtítulos de 3 palabras con la palabra activa resaltada
- Barra de progreso, grano de película, cierre con "GOODS UNCOVERED"
- Música de fondo al 12 % (se ajusta con `volumen_musica`)

## Carpeta de cada Short
```
shorts/002-nombre/
  short.json     ← guion (lo escribe Claude)
  voz.mp3        ← ElevenLabs, una pausa entre cada línea
  musica.mp3     ← opcional
  01.png … 09.png
```
Si falta una imagen, sale un recuadro gris que dice "IMAGEN 0N", para ver el ritmo antes de tenerlas todas.
Si falta la voz, los tiempos se calculan a 2.6 palabras por segundo y el video sale sin audio.

## Comandos
```
node motor-shorts/render.cjs shorts/001-records-mercancia                       # video completo
node motor-shorts/render.cjs shorts/001-records-mercancia --preview 1,5,12       # fotos de esos segundos
```
Un Short de 33 s tarda ~1 minuto en renderizar.

## Error "La voz tiene X bloques y el guion Y líneas"
ElevenLabs juntó dos líneas. Agrega `<break time="0.7s" />` al final de cada línea y vuelve a generar la voz.
