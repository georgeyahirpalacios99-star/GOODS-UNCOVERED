# Estilo PRO de Goods Uncovered (configuración fija desde nov-2026)

George lo pidió así: **realista y de diseñador, nada infantil**. Esta es la configuración por defecto de **todos** los videos, largos y Shorts.

## Reglas
1. **Estilo `documental`** en el motor: mapa satelital con relieve, fronteras finas y tipografía Anton + Barlow.
   - **Prohibido:** caritas, ojos, bocas, banderas con cara, el estilo `caricatura` y los objetos con fondo verde.
2. **Siempre hay algo en pantalla.** Cada frase de la voz tiene su anotación visual, y ningún cuadro queda quieto más de 2.5 s.
   - Si no hay clip ni foto, el mapa lleva una flecha, un círculo, un camino, figuritas o una cifra.
3. **Anotaciones en cada escena de mapa:** flechas, círculos, pines, caminos con vehículo y figuritas tipo señalética, que actúan lo que dice la voz (caminar, cosechar, fila de proporción).
4. **Fotos reales primero** (Wikimedia Commons, NASA o dominio público), con el crédito en pantalla. Flow/Veo se usa solo para lo que no existe y lleva la etiqueta "IMAGEN ILUSTRATIVA CON IA".
5. **El mapa nunca va solo.** En toda escena de mapa hay, al mismo tiempo:
   - `hud`: el lugar y las coordenadas en vivo, más la barra de escala;
   - `ambiente`: partículas suaves;
   - **al menos un acompañante** que cambia cada 3–4 s: `tarjetaFoto` (foto real flotando, unida al lugar), `simbolo` animado (notas, gotas, sol, precio, olas, reloj, alerta), `fila`, `dato` o `gente`.
   - Cada cambio de escena lleva transición: `barrido`, o la entrada circular de un clip.
6. **Muestras antes de producir:** con cada tema nuevo, primero se mandan 15–25 s de muestra y se espera el visto bueno de George.
7. **Clips: PRINCIPAL o RECUADRO.** Lo impactante va a pantalla completa 3–5 s; el resto va en `tarjetaClip` o `tarjetaFoto` sobre el mapa, 2–4 s.
8. **Prompts de Flow en formato agente.** Como en `videos-largos/007-sinaloa-desaparece/04-PROMPTS-FLOW.md`, para que Claude los genere desde la extensión de Chrome de George:
   - un bloque `ESTILO` fijo y un bloque `MOVIMIENTO` fijo;
   - una tabla por capítulo: ID, uso, frase de la voz, imagen y movimiento;
   - un checklist de calidad;
   - descarga con el nombre del ID.
9. **Música muy baja**, solo de fondo, sintetizada y sin derechos. Nunca audios virales con copyright.

## Capas del estilo pro (`mapa.json`, estilo `documental`)
Las posiciones aceptan `[lon, lat]` o `{ "x": px, "y": px }`.

| Capa | Para qué | Campos clave |
|---|---|---|
| `fronteras` | Bordes de los estados (México; necesita `"estadosDe": ["MEX"]`) | — |
| `resaltar` | Marcar un país o estado | `pais` (`MEX:SI`…), `relleno`, `color` |
| `hueco` | El territorio se hunde y queda el hueco | `pais`, `t` (momento), `dur` |
| `rotulo2` | Rótulo con línea guía | `lon`, `lat`, `dx`, `dy`, `texto`, `sub` |
| `pinPro` | Pin que cae sobre un lugar | `en`, `texto`, `tdx`, `tdy` |
| `circuloPro` | Círculo trazado a mano | `en`, `r`, `texto`, `color` |
| `flechaPro` | Flecha curva que se dibuja sola | `de`, `a`, `curva`, `punteada`, `texto` |
| `camino` | Ruta con un vehículo en la punta | `puntos`, `vehiculo` (`camion`, `tren`, `barco`, `avion`, `persona`), `dur`, `color` |
| `gente` | Figuritas de persona | `modo` (`grupo`, `caminar`, `cosechar`, `fila`), `n`, `resalta`, `en` / `de` + `a` |
| `fila` | Proporción con íconos ("1 de cada 5") | `icono` (`tomate`, `maiz`, `camaron`, `lata`), `n`, `resalta` |
| `ficha` | Rótulo inferior (título + subtítulo) | `kicker`, `texto`, `sub` |
| `dato` | Cifra grande con contador y fuente | `kicker`, `num`, `suf`, `sub`, `fuente` |
| `capitulo` | Tarjeta de capítulo | `n`, `texto` |
| `hud` | Lugar y coordenadas en vivo, y escala | `lugares: [{t, texto}]` |
| `ambiente` | Partículas que flotan | `n`, `color` |
| `tarjetaFoto` | Foto real flotando sobre el mapa, unida a un punto | `img`, `en`, `x`, `y`, `w`, `texto`, `credito`, `rot` |
| `tarjetaClip` | Clip de Flow/Veo recortado en un recuadro sobre el mapa (cuadros en `.clips/<codigo>/`) | `codigo`, `en`, `x`, `y`, `w`, `texto` (crédito por defecto: "Imagen ilustrativa con IA") |
| `simbolo` | Motion graphic sobre el mapa | `forma` (`notas`, `gotas`, `sol`, `precio`, `olas`, `reloj`, `alerta`), `en`, `tam`, `texto` |
| `barrido` | Transición: panel diagonal con filo amarillo | `desde`, `dur` |
| `foto` | Foto real a pantalla completa con zoom lento | `img`, `z0`, `z1`, `credito` |

Ejemplos que funcionan: `videos-largos/007-sinaloa-desaparece/muestras/` y `muestras-2/`.
