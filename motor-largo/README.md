# MOTOR DE VIDEOS LARGOS · estilo ensayo de investigación
Convierte `video.json` + voces + imágenes en un video 16:9 (1920×1080, 30 fps) con el estilo de `FORMATO-VIDEO-LARGO-ENSAYO.md`.

## Carpeta del video
```
videos-largos/001-nombre/
  video.json          ← línea de tiempo (la escribe Claude)
  voz/voz-01.mp3 …    ← un MP3 por bloque de ElevenLabs, con pausa entre párrafos
  imagenes/           ← fotos y capturas con el nombre que pide video.json (jpg, png, webp)
  musica.mp3          ← opcional, al 10 %
```
Si falta una imagen sale un recuadro gris con lo que hay que buscar. Si falta la voz, los tiempos se calculan a 2.5 palabras por segundo.

## Piezas que hace el editor (0 créditos)
`tarjeta` (texto palabra por palabra) · `cifra` (número fijo o que sube) · `barras` · `cita` · `esquema` (pasos con flechas) · `linea` (línea de tiempo) · `tablero` (corcho con fotos, notas e hilo rojo) · `calendario` · `perfil` (capas del mar) · `costa` (mapa de la costa oeste de Sudamérica con flechas) · `marca`.
Las imágenes (`img`) llevan zoom lento y opciones `bn` (blanco y negro), `vhs`, `color` (desfase rojo/azul), `etiqueta`, `lugar` y `credito`.

## Motion graphics (capas sobre cualquier escena)
Cada capa aparece cuando la voz dice su `clave` (o a los `en` segundos de la escena) y se pega a la escena que está en pantalla:
`palabra` (palabra clave que salta en caja amarilla o roja) · `dato` (punto que late + línea + etiqueta sobre la imagen, con `u`,`v` de 0 a 1) · `circulo` (círculo rojo a mano) · `sello` (cae con golpe y sacude la pantalla) · `fuente` (cita de la fuente arriba a la izquierda) · `suscribete` (botón animado).
Además: rótulo de capítulo y barra de progreso por capítulos (`capitulos` en video.json), `glitch` en tarjetas de giro, sacudida en las cifras.

## Efectos de sonido
Se sintetizan solos (sin derechos): whoosh en tarjetas y capítulos, golpe en sellos y cifras, pop en palabras y gráficas, tic en fuentes, glitch. Volumen con `volumen_efectos` (0.45 por defecto) y se apagan con `"efectos": false`.

## Comandos
```
node motor-largo/render.cjs videos-largos/001-el-nino-2026                 # video completo (~30 min de render)
node motor-largo/render.cjs videos-largos/001-el-nino-2026 --hasta 110     # muestra de los primeros 110 s
node motor-largo/render.cjs videos-largos/001-el-nino-2026 --preview 5,60  # fotos de esos segundos
node motor-largo/render.cjs videos-largos/001-el-nino-2026 --lista         # tiempos de cada escena
```
