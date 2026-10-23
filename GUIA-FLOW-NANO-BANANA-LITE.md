# GUÍA GOOGLE FLOW + NANO BANANA 2 LITE
**Sistema de prompts para el canal de historia de empresas (ilustración 2D tinta + acuarela)**

> Datos de octubre de 2026. Casi todo viene de blogs que citan a Google; Google no publica una tabla completa de Flow. Lo marcado ⚠ confírmalo en la configuración de la caja de prompt de Flow.

---

## 1. LO QUE DEBES SABER DE FLOW

| Tema | Dato | Qué significa para ti |
|---|---|---|
| Créditos gratis | 50 al día, no se acumulan. El reloj de 24 h arranca con tu primera generación ⚠ | Planea las imágenes por bloques diarios |
| Costo de Lite | Reportan que es **el modelo por defecto sin costo** en Flow ⚠ | Por eso Lite es la base del canal |
| Costo de otros modelos | Nano Banana 2 y 2.1: ~10 créditos · Pro: ~20 créditos por imagen ⚠ | Pro solo para la miniatura |
| Video Veo 3.1 | Lite ~10 · Fast ~20 · Quality ~100 créditos por clip | 2-4 clips al día como máximo. Solo para tomas clave |
| Resolución de Lite | **Máximo 1K** (~1376×768 en 16:9, lo que Flow muestra como 768p) | Sirve para exportar en 1080p si el zoom en CapCut no pasa de 110% |
| Variantes | 4 imágenes por intento | Elige una. No regeneres más de 2 veces la misma escena |
| Frames to Video | Animas una imagen que ya generaste (inicio, final o ambos) | Para el puntito del mapa y transiciones |
| Ingredients to Video | Varias imágenes de referencia para personajes, objetos y estilo | Para video, no para tus imágenes fijas |
| Extend / Scenebuilder | Alarga un clip partiendo de su último segundo | No lo necesitas en este formato |
| Acceso | Por país; una VPN no lo desbloquea | Ya lo tienes funcionando |

---

## 2. LÍMITES DE NANO BANANA 2 LITE Y CÓMO VENCERLOS

| Límite de Lite | Regla para ti |
|---|---|
| No está optimizado para **varias imágenes de referencia** | Usa **máximo 1 referencia**: la imagen de estilo aprobada (el mapa) |
| No está optimizado para **editar en varios turnos** | No arregles con "Editar". **Regenera** con el prompt corregido |
| Sigue peor las instrucciones complejas que Pro | **1 sujeto + 1 acción + máximo 3 elementos de fondo** por imagen |
| Escribe mal el texto, sobre todo en español | **Cero texto en la imagen.** Las etiquetas ("MAPA", "BODEGA") se ponen en CapCut |
| Solo 1K | Encuadres amplios. Evita detalles diminutos que necesiten 4K |

**Reglas oficiales de Google para Nano Banana que aplican a Lite:**
1. **Párrafo narrativo, no lista de palabras.** Google dice que una descripción en párrafo casi siempre da mejor imagen que palabras sueltas.
2. **Redacción positiva.** Di lo que quieres ver ("las paredes de la tienda están en blanco"), no solo lo que no quieres.
3. **Términos de cámara:** plano general, vista aérea, primer plano, vista frontal.
4. **Describe el medio y el estilo con detalle** (tinta, acuarela, grosor de línea, colores) para que todas salgan consistentes.

---

## 3. BLOQUES FIJOS (copiar idénticos en CADA prompt)

> **Versión 2 (aprobada):** estilo y personaje validados con la calle latina. La última frase del estilo se cambió para quitar el margen blanco tipo tarjeta.

### Bloque de ESTILO
```
Drawn as a flat, front-facing hand-drawn ink illustration with a soft muted watercolor wash, in a storybook editorial style with fine detailed line work. The palette is slate grey, petrol blue, ochre and olive green with warm golden highlights. The watercolor painting extends almost to the edges of the image, edge to edge, with only a thin torn paper border showing a little white around it, no card, no drop shadow, no wide margin.
```

### Bloque de PERSONAJE (solo si hay personas)
```
Every person is a faceless character with a smooth round white head, two small black dot eyes and no other facial features, with simple rounded bodies.
```

### Bloque de SIN TEXTO (siempre al final)
```
Every sign, label, box and screen is blank, with no letters or numbers anywhere, and no logos.
```

---

## 4. PLANTILLA DE PROMPT

```
[TIPO DE PLANO] of [SUJETO haciendo UNA ACCIÓN] in [LUGAR], [HORA Y LUZ]. [1 a 3 detalles de fondo]. [BLOQUE PERSONAJE si aplica] [BLOQUE ESTILO] [BLOQUE SIN TEXTO]
```

**Tipos de plano que Lite entiende bien:** `A wide establishing view` · `A flat top-down view` · `A medium shot` · `A close-up` · `An aerial view` · `A side view`

**Luces que combinan con la paleta:** `at golden hour` · `at night under warm floodlights` · `on a grey overcast morning` · `lit by a single warm desk lamp`

### Cómo usar la referencia de estilo en Flow
1. Sube o selecciona la **imagen del mapa aprobada** como referencia.
2. Empieza el prompt con: `Match the illustration style, line work and color palette of the reference image.`
3. Luego pega el prompt completo con los 3 bloques.

---

## 5. GANCHO DE AMAZON: 8 PROMPTS LISTOS (versión Latinoamérica)

Narración: *"Ves un puntito en el mapa de tu app. Sale de una bodega que nunca vas a pisar, sube a un avión que nunca vas a abordar y entra a tu calle antes de que termines de preguntarte dónde está. Detrás de ese puntito…"*

**IMAGEN 1 · El puntito** (ya aprobada: el mapa)

**IMAGEN 2 · Bodega cerrada**
```
Match the illustration style, line work and color palette of the reference image. A wide establishing view of a giant windowless warehouse behind a tall chained metal gate with a padlock, at dusk under warm floodlights. Rows of loading docks and parked trailers stretch into the distance. Drawn as a flat, front-facing hand-drawn ink illustration with a soft muted watercolor wash, in a storybook editorial style with fine detailed line work. The palette is slate grey, petrol blue, ochre and olive green with warm golden highlights. The watercolor painting extends almost to the edges of the image, edge to edge, with only a thin torn paper border showing a little white around it, no card, no drop shadow, no wide margin. Every sign, label, box and screen is blank, with no letters or numbers anywhere, and no logos.
```

**IMAGEN 3 · Avión de carga**
```
Match the illustration style, line work and color palette of the reference image. A side view of a white cargo plane on a wet runway at night under warm floodlights, with its front cargo door open and small workers loading a large wooden crate. A crescent moon and distant runway lights. Every person is a faceless character with a smooth round white head, two small black dot eyes and no other facial features, with simple rounded bodies. Drawn as a flat, front-facing hand-drawn ink illustration with a soft muted watercolor wash, in a storybook editorial style with fine detailed line work. The palette is slate grey, petrol blue, ochre and olive green with warm golden highlights. The watercolor painting extends almost to the edges of the image, edge to edge, with only a thin torn paper border showing a little white around it, no card, no drop shadow, no wide margin. Every sign, label, box and screen is blank, with no letters or numbers anywhere, and no logos.
```

**IMAGEN 4 · Camioneta cargando**
```
Match the illustration style, line work and color palette of the reference image. A medium shot of a delivery worker in an orange vest loading cardboard boxes into the back of a blue delivery van beside a brick warehouse at sunrise. Stacked boxes on the wet pavement. Every person is a faceless character with a smooth round white head, two small black dot eyes and no other facial features, with simple rounded bodies. Drawn as a flat, front-facing hand-drawn ink illustration with a soft muted watercolor wash, in a storybook editorial style with fine detailed line work. The palette is slate grey, petrol blue, ochre and olive green with warm golden highlights. The watercolor painting extends almost to the edges of the image, edge to edge, with only a thin torn paper border showing a little white around it, no card, no drop shadow, no wide margin. Every sign, label, box and screen is blank, with no letters or numbers anywhere, and no logos.
```

**IMAGEN 5 · Calle latina**
```
Match the illustration style, line work and color palette of the reference image. A wide view of a blue delivery van turning into a quiet Latin American neighborhood street at golden hour. Low houses with flat roofs and metal gates, tangled power lines overhead, and a small corner store with a striped awning. Every person is a faceless character with a smooth round white head, two small black dot eyes and no other facial features, with simple rounded bodies. Drawn as a flat, front-facing hand-drawn ink illustration with a soft muted watercolor wash, in a storybook editorial style with fine detailed line work. The palette is slate grey, petrol blue, ochre and olive green with warm golden highlights. The watercolor painting extends almost to the edges of the image, edge to edge, with only a thin torn paper border showing a little white around it, no card, no drop shadow, no wide margin. Every sign, label, box and screen is blank, with no letters or numbers anywhere, and no logos.
```

**IMAGEN 6 · Persona mirando el celular**
```
Match the illustration style, line work and color palette of the reference image. A medium shot of a person sitting in a worn floral armchair in a cozy living room, looking at a phone with a small question mark floating above their head. Through the window behind them, a blue delivery van is parked on the street. A bookshelf and a potted plant. Every person is a faceless character with a smooth round white head, two small black dot eyes and no other facial features, with simple rounded bodies. Drawn as a flat, front-facing hand-drawn ink illustration with a soft muted watercolor wash, in a storybook editorial style with fine detailed line work. The palette is slate grey, petrol blue, ochre and olive green with warm golden highlights. The watercolor painting extends almost to the edges of the image, edge to edge, with only a thin torn paper border showing a little white around it, no card, no drop shadow, no wide margin. Every sign, label, box and screen is blank, with no letters or numbers anywhere, and no logos.
```

**IMAGEN 7 · La caja en la puerta**
```
Match the illustration style, line work and color palette of the reference image. A close-up of a cardboard box sitting on a doormat in front of a green metal door, in soft morning light. A potted plant and a few fallen leaves. Drawn as a flat, front-facing hand-drawn ink illustration with a soft muted watercolor wash, in a storybook editorial style with fine detailed line work. The palette is slate grey, petrol blue, ochre and olive green with warm golden highlights. The watercolor painting extends almost to the edges of the image, edge to edge, with only a thin torn paper border showing a little white around it, no card, no drop shadow, no wide margin. Every sign, label, box and screen is blank, with no letters or numbers anywhere, and no logos.
```

**IMAGEN 8 · El garaje de 1994 (transición a la historia)**
```
Match the illustration style, line work and color palette of the reference image. A medium shot of a man typing on a bulky beige 1990s computer in a cramped garage office at night, lit by a single warm desk lamp. Cardboard boxes, a door laid flat as a desk, and stacks of books. Every person is a faceless character with a smooth round white head, two small black dot eyes and no other facial features, with simple rounded bodies. Drawn as a flat, front-facing hand-drawn ink illustration with a soft muted watercolor wash, in a storybook editorial style with fine detailed line work. The palette is slate grey, petrol blue, ochre and olive green with warm golden highlights. The watercolor painting extends almost to the edges of the image, edge to edge, with only a thin torn paper border showing a little white around it, no card, no drop shadow, no wide margin. Every sign, label, box and screen is blank, with no letters or numbers anywhere, and no logos.
```

> Las personas reales (Bezos, fundadores) siempre van como personaje sin cara. Así evitas parecidos con gente real y mantienes el estilo.

---

## 6. ANIMAR CON VEO (solo 2-3 tomas por video)

En Flow → **Frames to Video** → elige la imagen → modelo **Veo 3.1 Lite** (el más barato).

**Puntito del mapa:**
```
Keep the exact same illustration, style and composition. The orange dot pulses softly and its three ripple rings expand slowly outward. Very slow camera push in. Nothing else moves, no new objects, no text.
```

**Plantilla general:**
```
Keep the exact same illustration, style and composition. [UN SOLO MOVIMIENTO SUAVE: the van drives slowly forward / the plane door closes / steam rises from the cup]. Very slow camera push in. Nothing else changes, no new objects, no text.
```

El resto de las imágenes no se anima en Flow: en CapCut les pones zoom lento de 100% a 108% en 5-7 segundos.

---

## 7. SI ALGO SALE MAL

| Problema | Arreglo (agrégalo al prompt y regenera) |
|---|---|
| Sale como foto de un papel inclinado | `flat scan, viewed straight on, not a photograph, no perspective` |
| Personajes con cara o nariz | `smooth featureless round white head, only two small black dot eyes` |
| Aparecen letras | `all surfaces are blank and plain` y quita del prompt palabras como "sign", "store name" o "newspaper" |
| Colores muy vivos | `muted, desaturated watercolor, soft faded colors` |
| Tarjeta con sombra y mucho blanco | Ya corregido en el bloque de estilo (v2). Si persiste, agrega `full-bleed composition` |
| Estilo distinto al de la referencia | Revisa que adjuntaste la referencia y que el bloque de estilo está completo, sin cambios |
| Demasiados elementos | Quita detalles: 1 sujeto, 1 acción, máximo 3 cosas de fondo |

---

## 8. CUÁNDO NO USAR LITE

| Caso | Modelo |
|---|---|
| **Miniatura** (necesita más resolución y nitidez) | Nano Banana Pro, 2K. Cuesta más créditos, vale la pena 1 por video |
| Imágenes del video | **Siempre Lite.** No mezcles modelos dentro de un video |
| Video | Veo 3.1 Lite, solo tomas clave |

---

## FUENTES
- [Google Cloud – Ultimate prompting guide for Nano Banana](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- [Google AI for Developers – Image generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Google – Nano Banana 2 Lite](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/)
- [Google – Introducing Flow](https://blog.google/innovation-and-ai/products/google-flow-veo-ai-filmmaking-tool/)
- [Google – 5 tips for using Flow](https://blog.google/innovation-and-ai/products/flow-video-tips/)
- [Google – Veo 3.1 updates in Flow](https://blog.google/innovation-and-ai/products/veo-updates-flow/)
- [eesel – Nano Banana 2 Lite](https://www.eesel.ai/blog/nano-banana-2-lite)
- [eesel – Lite pricing](https://www.eesel.ai/blog/nano-banana-2-lite-pricing)
- [CometAPI – Nano Banana 2 Lite](https://www.cometapi.com/zh-TW/models/google/gemini-3-1-flash-lite-image/)
- [nanobanana21.app – 2.1 en Flow](https://nanobanana21.app/blog/nano-banana-2-1-arrives-in-google-flow)
- [Atlas Cloud – Veo 3.1 gratis o pago](https://www.atlascloud.ai/blog/tips/veo-3.1-ai-video-generator-free-or-paid)
- [SolidAITech – Flow gratis](https://www.solidaitech.com/2026/09/unlimited-free-ai-image-generator-google-flow.html)
