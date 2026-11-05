---
name: guion-youtube
description: Prepara un video completo de Goods Uncovered a partir de un tema: investigación con fuentes, guion con gancho, voz para ElevenLabs en bloques, prompts de imágenes para Google Flow, línea de tiempo para el editor y datos de publicación. Úsalo cuando George diga "/guion-youtube", "hazme un video de…", "siguiente Short", "siguiente video largo" o dé un tema nuevo.
---

# /guion-youtube "tema" [short | largo] [duración]

Canal: **Goods Uncovered**. Las historias ocultas detrás de los objetos que usas, los lugares que conoces y los misterios que nadie te explicó. **Español neutro, para todo el público hispano** (Latinoamérica, España, hispanos en EE. UU.). Si no dice formato: **largo** = 13 min; **short** = ~30 s.

Escribe siempre en español latino, directo, con datos concretos y sin lenguaje de anuncio. Si hay que elegir algo, da **una sola recomendación**.

## 1. Investigar (antes de escribir una sola línea)
- Usa WebSearch (extended si el tema es reciente). Busca la cifra más sorprendente, una contradicción, un dato histórico olvidado y un dato científico raro.
- **Cada dato con fuente.** Si las fuentes no coinciden, usa la cifra más conservadora y dilo. Nada inventado.
- Proponer **3 ideas con gancho** y recomendar una. Guardar en `videos-largos/NNN-tema/00-INVESTIGACION-E-IDEAS.md` (o `shorts/NNN-tema/`).

## 2. Estructura
**Largo (ensayo de investigación, ver `FORMATO-VIDEO-LARGO-ENSAYO.md`):**
- 0:00 gancho con cifra imposible → 0:50 **pregunta central** en tarjeta → 6 capítulos.
- Cada 2-3 min una tarjeta que **niega o corrige** lo anterior ("pero…", "esa no es la razón").
- Cierre: respuesta honesta + qué hacer + vuelve a la imagen del inicio + suscribirse.
- ~1,750 palabras para 13 min (la voz de ElevenLabs va a ~150 ppm).
- **Meta visual: un cambio cada 3-4 s** (imagen, clip o gráfico). Para 13 min: ~60-90 imágenes + clips + gráficos del editor.

**Short (fórmula de récords que funcionó: 1,105 vistas en 4 h):**
- 8 récords + cierre. Frase: "El/La ___ más ___ del mundo es ___". El más polémico primero. Cierre que pide comentar ("¿qué le faltó a tu país?").

## 3. Archivos que entregas (copiar el formato de los videos anteriores)
| Archivo | Plantilla a seguir |
|---|---|
| `01-GUION.md` (cada escena con su origen: `[MOTOR]` `[NASA]` `[PD]` `[PEXELS]` `[IA]`) | `videos-largos/001-el-nino-2026/01-GUION.md` |
| `02-GUION-ELEVENLABS.md` en **7 bloques** (`voz-01`…), `<break time="0.6s" />` entre párrafos, números escritos en palabras cuando se leen raro | `videos-largos/001-el-nino-2026/02-GUION-ELEVENLABS.md` |
| `04-PROMPTS.md`: prompts 16:9 (9:16 en Shorts) + **un solo bloque para el agente de Flow** con estilos A/B/C/D y la lista numerada | `videos-largos/001-el-nino-2026/04-PROMPTS.md` |
| `video.json` (largo) o `short.json` (short), con motion graphics atados a palabras clave (`palabra`, `dato`, `circulo`, `sello`, `fuente`) y capítulos | `motor-largo/guion_a_json_el_nino.py`, `shorts/001-records-mercancia/short.json` |
| `05-PUBLICACION.md`: título, descripción con capítulos y fuentes, etiquetas, configuración, comentario fijado, Short de promoción | `videos-largos/001-el-nino-2026/05-PUBLICACION.md` |

## 4. Producción
- Imágenes: priorizar **0 créditos**: gráficos del editor, NASA/NOAA (dominio público), Pexels (si hay `PEXELS_API_KEY`). IA solo para lo que no exista. Las imágenes de IA de hechos históricos llevan etiqueta **"RECREACIÓN"**. Nunca rótulos de lugar sobre imágenes de IA.
- Voz: si hay `ELEVENLABS_API_KEY`, generarla por API con tiempos por palabra; si no, George la genera con `02-GUION-ELEVENLABS.md`.
- Render: `node motor-largo/render.cjs videos-largos/NNN-tema` (o `motor-shorts/render.cjs`). Revisar cuadros con `--preview` antes del render final. Normalizar el audio a ~-16 LUFS con picos bajo -1 dB.
- Miniaturas: `node motor-largo/miniaturas.cjs videos-largos/NNN-tema` + prompts de fondo sin texto. Máximo 4 palabras, una pregunta, un solo protagonista. Nada que el video no cumpla.
- Entregar el MP4 por el chat y, si pesa más de 100 MB, también en partes en `entregas-partes/` subidas al repo.

## 5. Reglas de monetización (revisar siempre)
- "Contenido alterado o sintético: **Sí**" cuando hay recreaciones o voz de IA.
- Música solo de la **Biblioteca de audio de YouTube** (la de CapCut da reclamos).
- Nada de metraje de otros canales ni documentales.
- Cada video con tema nuevo, datos reales y guion propio (YouTube no paga contenido repetitivo hecho en masa).
- ElevenLabs: el plan gratis **no permite uso comercial**; para monetizar hace falta un plan de pago.
