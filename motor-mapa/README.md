# Motor de mapas

`node motor-mapa/render.cjs <carpeta> [--preview 2,8.5] [--hasta 10] [--hilos 3]`

La carpeta lleva un `mapa.json` (y las fotos que use). Ejemplos: `demos-mapa/A-documental`, `demos-mapa/B-caricatura`.

## Estilos
- **documental**: relieve satelital dibujado por código, plataforma continental brillante, montañas y desiertos de Natural Earth.
  Capas: `fecha`, `titulo`, `pin`, `bandera`, `ruta` (con barco), `polaroid`, `documento`, `versus`, `ecuador`, `medida`, `sello`, `etiqueta`. Subtítulos en `narracion`.
- **caricatura**: países con su bandera, ojos y boca que reaccionan (`normal`, `shock`, `triste`, `llora`, `feliz`, `duda`, `enojado`, `amor`).
  Capas: `titulo` (palabras entre `*` salen amarillas), `region`, `barra`, `marcador`, `lista`, `tarjeta`, `globo`, `cinta`, `flujo`, `pregunta`. También `desaparece`, `caras`, `mirar`, `tam`, `sacudidas`.

## Cámara
`camara`: lista de `{t, lon, lat, ancho}` (ancho = grados de longitud visibles). `"suave": false` = movimiento lineal (deriva), `"arco": 1` = se aleja a mitad del viaje.

## Datos (libres de derechos)
- Mapas: Natural Earth (dominio público), en `datos/`.
- Banderas: flag-icons (licencia MIT), en `datos/banderas/`.
- Tipografías: Fredoka y Montserrat (licencia OFL), en `datos/fuentes/`.
