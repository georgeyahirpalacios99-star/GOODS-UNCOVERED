# BLOQUES 0, 1, 5-10 — PAQUETE DE PRODUCCIÓN
**Video 001 · Goods Uncovered · "10 cargamentos que desaparecieron y qué pasó con cada uno"**

---

# BLOQUE 0 — FICHA TÉCNICA

| Campo | Valor |
|---|---|
| Título de trabajo | 10 cargamentos que desaparecieron y qué pasó con cada uno |
| Canal | Goods Uncovered |
| Nicho | Mercancía, logística y carga perdida · documental de investigación |
| Duración exacta | 12:00 (720 s) |
| Palabras narradas | 1.688 (conteo real) |
| Tomas | 144 |
| Formato | 16:9 · 4K · 24 fps |
| Voz | Narrador masculino, 35-45 años, tono bajo, registro grave, 155 ppm con pausas |
| Paleta | Azul acero `#0E2433` · Óxido `#C4581F` · Gris concreto `#8A8F94` · Blanco niebla `#E8E6E1` · Negro alquitrán `#0A0C0E` |
| Estilo visual | Documentary realism · 35mm · grano pesado · anamórfico en planos generales |
| Ángulo diferencial | Diez casos reales de carga perdida conectados por una sola causa: el documento que declara el contenido lo llena quien envía, y nadie lo verifica hasta que es tarde |
| Promesa central | Ver qué pasó, caso por caso, con mercancía que alguien fabricó, alguien pagó y nadie volvió a ver |
| Público | 25-45 años, hombres y mujeres, hispanohablantes, interés en logística, comercio, misterios reales y economía cotidiana. Motivación: entender un sistema que usan todos los días y nadie les explicó |
| Objetivo del video | Watch time + comentarios (el CTA pide un número, no una suscripción) |
| Declaración de IA | **SÍ** — marcar "contenido alterado o sintético" en YouTube Studio. Todas las tomas son recreación generada |

---

# BLOQUE 1 — ESTRUCTURA MACRO

| Beat | Timecode | Función narrativa | Re-gancho de entrada | Emoción objetivo | Retención estimada al salir |
|---|---|---|---|---|---|
| 0 | 0:00 - 0:08 | Inicio de gancho | Frase de impacto + silencio | Desconcierto | 88% |
| 1 | 0:08 - 0:50 | Desarrollo de gancho | Escalada + credibilidad + mapa parcial | Curiosidad comprometida | 76% |
| 2 | 0:50 - 1:53 | Caso 10 · precio vs material | Cifra sorpresa aislada | Reconocimiento ("yo compro eso") | 71% |
| 3 | 1:53 - 2:56 | Caso 9 · devoluciones | Interpelación directa ("devolviste algo") | Incomodidad personal | 67% |
| 4 | 2:56 - 3:59 | Caso 8 · equipaje perdido | Pregunta implícita | Empatía | 64% |
| 5 | 3:59 - 5:02 | Caso 7 · robo en tránsito | Contradicción (40 t → 31 t) | Intriga técnica | 61% |
| 6 | 5:02 - 6:05 | Caso 6 · destrucción judicial | Cambio brusco de ritmo visual | Desconcierto moral | 58% |
| 7 | 6:05 - 7:08 | Caso 5 · turno fantasma | Adelanto del clímax | Sorpresa | 56% |
| 8 | 7:08 - 8:11 | Caso 4 · subasta a ciegas | Cambio total de paleta y tempo | Tensión de apuesta | 54% |
| 9 | 8:11 - 9:14 | Caso 3 · naufragio en juicio | Silencio + ambiente submarino | Fascinación | 53% |
| 10 | 9:14 - 10:17 | Caso 2 · pérdida masiva | Cifra sorpresa + tormenta | Impacto físico | 52% |
| 11 | 10:17 - 11:20 | Caso 1 · Ancón, Perú | Cambio de locación total | Cercanía + indignación | 51% |
| 12 | 11:20 - 12:00 | Final de gancho | Pago del contrato + giro final + loop | Resolución con pregunta abierta | 48% |

Separación real entre re-ganchos: **63 s**. El objetivo del sistema es 45-60 s; los 3 s de exceso se cubren con el contador visible en pantalla (10 → 1), que da sensación de progreso continuo, y con los 9 silencios estratégicos internos.

---

# BLOQUE 5 — BIBLIA DE CONSISTENCIA

## Paleta maestra (fija en los 144 prompts)

| Uso | Nombre | HEX |
|---|---|---|
| Base / sombras frías | Azul acero profundo | `#0E2433` |
| Acento / alerta | Óxido naranja | `#C4581F` |
| Neutro medio | Gris concreto | `#8A8F94` |
| Luz / papel | Blanco niebla | `#E8E6E1` |
| Negro absoluto | Negro alquitrán | `#0A0C0E` |

Los tres colores dominantes aparecen nombrados en cada prompt. No introduzcas un cuarto color dominante en ninguna toma.

## Grading
LUT de documental frío: sombras azuladas, medios desaturados un 15%, altas luces conservadas. Curva de contraste en S suave. Grano de película 35mm al 12%. Viñeteado 8%.

## Locaciones recurrentes y su seed

| Locación | Seed | Descripción fija (copiar palabra por palabra en todos sus prompts) |
|---|---|---|
| Playa de Ancón | `104417` | Pacific coast beach, wet dark sand, low dunes behind, small wooden fishing boats anchored offshore, overcast dawn haze |
| Puerto / patio de contenedores | `104417` | Industrial container yard, nine-high stacks, sodium floodlights on steel masts, oil-stained concrete, chain-link perimeter |
| Bodega de liquidación | `330912` | Vast warehouse interior, steel shelving six meters high, cold fluorescent strip lights, polished concrete floor, roof skylights |
| Fábrica / línea de producción | `773815` | Industrial factory hall, steel presses and conveyor belt, oil-streaked machinery, overhead work lamps, dust in the air |
| Bodega de equipaje | `448126` | Storage hall with numbered steel racks of suitcases, handwritten inventory cards, hard overhead industrial light |
| Fondo marino | `912664` | Dark seabed with fine sediment, sparse marine growth, deep blue falloff, visible water particulate |
| Buque en tormenta | `101338` | Container ship deck at night, lashing rods under tension, practical deck floodlights, driving rain, black sky |
| Oficina / archivo | `551703` | Dim administrative office, steel filing cabinets, desk lamp, perforated continuous paper, soft window light |

**Regla dura:** si una locación aparece en 12 tomas, su descripción fija se repite idéntica en las 12 y el seed no cambia. Cambiar el seed entre tomas de la misma locación es la causa número uno de que un video de IA se vea como clips sin relación.

## Personajes
Este video **no tiene personajes recurrentes identificables**, por decisión de producción. Todas las figuras humanas van en silueta, contraluz, o solo manos y antebrazos. Razón: evita el riesgo de parecido con personas reales, elimina el problema de consistencia facial entre tomas y elimina el artefacto más delator de la IA (rostros que cambian).

## Tipografía en pantalla

| Uso | Familia | Tamaño | Posición |
|---|---|---|---|
| Contador de casos (10 → 1) | Sans condensada bold, tracking 0 | 180 px | Centro, 2 s, fundido 0.2 s |
| Dato en pantalla | Sans medium, tracking +40 | 54 px | Tercio inferior, margen 120 px |
| Nombre de lugar | Sans regular mayúsculas, tracking +80 | 38 px | Inferior izquierda |

Una sola familia tipográfica en todo el video. Nada de sombras, bordes ni degradados en el texto.

---

# BLOQUE 6 — DISEÑO DE AUDIO

## Pista musical
Género: documental industrial / drone cinematográfico. Instrumentación: contrabajo, percusión metálica procesada, cuerdas graves, sub-bajo sintético. Sin melodía reconocible: el video es narrado y la melodía compite con la voz.

| Sección | Timecode | BPM | Qué hace la música |
|---|---|---|---|
| Intro | 0:00 - 0:08 | — | Una nota sostenida de contrabajo. Corte seco en 0:06. Silencio 0:06-0:08 |
| Build | 0:08 - 0:50 | 82 | Pulso de percusión, capa de cuerdas en 0:30, baja a -24 dB en 0:40 |
| Cuerpo A (casos 10-7) | 0:50 - 5:02 | 82 | Loop con variación por caso. Corte limpio en cada puente |
| Cuerpo B (casos 6-4) | 5:02 - 8:11 | 90 | Sube tempo. Distorsión leve en el caso 6. Percusión de subasta en el 4 |
| Cuerpo C (caso 3) | 8:11 - 9:14 | — | Sale la percusión. Solo ambiente submarino y una nota de cuerda |
| Clímax (caso 2) | 9:14 - 10:17 | 96 | Percusión completa, intensidad máxima del video |
| Resolución (caso 1) | 10:17 - 11:20 | 70 | Piano solo, entran cuerdas suaves. Corte total en 11:10 |
| Cierre | 11:20 - 12:00 | 82 | Reentra el tema principal completo. Corte seco en 12:00 |

Los 12 cortes musicales coinciden exactamente con los 12 puentes del guion. Eso es lo que hace que un cambio de caso se sienta como un capítulo y no como un salto.

## Niveles
| Elemento | Nivel |
|---|---|
| Narración | -3 dB (pico), -16 LUFS integrado |
| Música bajo voz | -18 dB |
| Música en pasajes sin voz | -9 dB |
| SFX | -12 dB |
| Ambiente de fondo | -26 dB, continuo, nunca silencio digital total |

## Silencios estratégicos (9 en total)
`0:06-0:08` · `2:47` · `3:50` · `5:42` · `6:51` · `8:06` · `9:05` · `10:12` · `11:10-11:20`

Cada uno dura entre 0.8 y 1.2 s salvo el final (10 s con ambiente). Un silencio digital absoluto suena a error de edición: deja siempre el ambiente a -26 dB.

## SFX obligatorios
Mínimo 1 cada 8 segundos. Librerías base: impactos sub-bajo, risers cortos, ticks metálicos, whooshes de transición, acero crujiendo, agua (olas, chapoteo, submarino), maquinaria industrial, papel y sellos, cinta de empaque, montacargas, teléfono lejano, bocina de barco.

## Fuentes sin copyright
Biblioteca de audio de YouTube (gratis, sin atribución para monetizar), Epidemic Sound, Artlist. **No uses música con licencia de atribución en un video monetizado sin cumplir la atribución exacta**: es la causa más común de reclamo en canales nuevos.

---

# BLOQUE 7 — MINIATURA Y TÍTULO

## 5 títulos

| # | Título | Caracteres | Nota |
|---|---|---|---|
| **1** | **10 cargamentos que desaparecieron y qué pasó con cada uno** | 57 | **Recomendado** |
| 2 | El mar devolvió 50 contenedores y nadie los reclamó | 51 | Mejor CTR, pero promete un solo caso: es el título del video individual del caso 1, no de la compilación |
| 3 | 10 cargamentos perdidos: qué había dentro de cada uno | 53 | Alternativa si el 1 no rinde en las primeras 48 h |
| 4 | La carga que nadie volvió a ver: 10 casos reales | 48 | Más corto, menos específico |
| 5 | Qué pasa con la mercancía que nunca llega | 42 | Buen SEO, gancho débil |

**Por qué el 1:** tiene cifra, promete exactamente lo que el gancho contrata en el segundo 30, y lo paga en el minuto 11:20. Cero riesgo de clickbait engañoso, que es un requisito de la auditoría de monetización. El título 2 tendría más CTR pero el video no lo paga: guárdalo para cuando hagas el caso 1 como video propio.

## 3 conceptos de miniatura

### Concepto A — "La lavadora en la arena" (recomendado)
- **Sujeto:** una lavadora blanca volcada en arena mojada, ocupando el 60% del cuadro a la derecha.
- **Contraste:** objeto doméstico blanco e impecable contra arena oscura y mar gris. El contraste es el concepto.
- **Texto en miniatura:** `¿DE QUIÉN ES?` (3 palabras)
- **Colores:** blanco niebla sobre azul acero, texto en óxido naranja.
- **Por qué funciona a 120×68 px:** una forma blanca grande y rectangular sobre fondo oscuro se lee como silueta a cualquier tamaño. No depende de leer el texto.

```
Thumbnail photograph: a pristine white washing machine lying on its side half-buried
in wet dark sand on an empty beach at dawn, sea foam reaching it, dramatic low side
light from the right, deep steel blue sea and sky behind, high contrast, strong
negative space on the left third for text overlay, shot on 35mm, shallow depth of
field, documentary realism, 16:9.
Negative: no text, no watermarks, no logos, no people, no cartoon look, no oversaturation.
```

### Concepto B — "Las diez puertas"
- **Sujeto:** diez puertas de contenedor en fila, nueve cerradas y una entreabierta con luz saliendo.
- **Texto:** `1 DE 10`
- **Por qué funciona:** el patrón roto. El ojo va directo al único elemento distinto, sin leer nada.

```
Thumbnail photograph: ten shipping container doors in a straight row, nine of them
closed and rusted shut, one single door ajar with warm light spilling out of the gap,
overcast flat daylight, rust orange and deep steel blue and concrete grey, strong
symmetry, high contrast, negative space in the upper third, shot on 35mm, anamorphic,
documentary realism, 16:9.
Negative: no text, no watermarks, no logos, no people, no readable signage, no cartoon look.
```

### Concepto C — "El contenedor hundiéndose"
- **Sujeto:** contenedor girando mientras se hunde, visto desde abajo con la luz de la superficie detrás.
- **Texto:** `30 TONELADAS`
- **Por qué funciona:** imagen imposible de haber sido filmada. Genera la pregunta "¿cómo tomaron esto?", que es clic.

```
Thumbnail photograph: a single steel shipping container sinking and rotating in deep
blue ocean water seen from below, bubble trail rising, strong shafts of surface light
behind it creating a silhouette, deep steel blue and tar black and fog white, high
contrast, dramatic scale, negative space in the lower left, shot on 24mm, water
particulate, documentary realism, 16:9.
Negative: no text, no watermarks, no logos, no divers, no people, no cartoon look.
```

**Test de legibilidad:** los tres conceptos se entienden en 0.4 s a 120×68 px porque los tres dependen de **una forma grande y un contraste**, no de leer el texto. Si al reducir la miniatura al tamaño de una uña no distingues el sujeto, descarta y vuelve a empezar.

---

# BLOQUE 8 — PAQUETE DE PUBLICACIÓN

## Descripción

```
Diez cargamentos que desaparecieron y qué pasó con cada uno: carga perdida en el mar,
mercancía destruida por orden judicial, contenedores subastados a ciegas y el día que
el mar devolvió la carga en una playa de Perú.

En este video reconstruimos diez casos de mercancía que alguien fabricó, alguien pagó
y nadie volvió a ver. Cada caso tiene un dato verificable y una explicación de por qué
pasó: cómo se amarra la carga en un buque, por qué una devolución no vuelve a la
tienda, qué hace la aduana con un producto falsificado y por qué un naufragio con carga
puede quedar intacto durante siglos por un juicio.

Las imágenes de este video son recreaciones generadas por computadora. Ninguna es
material de archivo real. El contenido está declarado como sintético en YouTube Studio.

CAPÍTULOS
00:00 Los contenedores en la playa
00:50 10 · El dólar que no es un dólar
01:53 9 · El edificio de las devoluciones
02:56 8 · Las maletas que nadie reclamó
03:59 7 · Los nueve mil kilos que faltan
05:02 6 · Lo que se destruye por orden judicial
06:05 5 · El turno que no existe
07:08 4 · Comprar una caja cerrada
08:11 3 · La carga que nadie puede tocar
09:14 2 · Mil ochocientos en una noche
10:17 1 · El día que el mar lo devolvió
11:20 Lo que conecta los diez casos

Fuentes y aclaraciones en el comentario fijado.

#carga #logistica #contenedores
```

Los primeros 150 caracteres llevan la keyword principal ("cargamentos que desaparecieron", "carga perdida en el mar") porque es lo único visible sin expandir la descripción.

## 15 tags

**Cola larga exacta (3):** `cargamentos que desaparecieron` · `contenedores perdidos en el mar` · `mercancía abandonada en puerto`

**Nicho (7):** `carga perdida` · `subasta de contenedores` · `devoluciones de internet` · `equipaje no reclamado` · `robo de carga` · `naufragio con carga` · `aduana mercancía falsificada`

**Amplios (5):** `logística` · `comercio internacional` · `misterios reales` · `documental español` · `casos reales`

## Hashtags
`#carga` `#logistica` `#contenedores` — tres, nunca más. Los hashtags de más diluyen la clasificación.

## Comentario fijado

```
Aclaración importante: las imágenes son recreaciones generadas, no material de archivo.
Lo declaré como contenido sintético en Studio.

Y una pregunta real: de los diez casos, ¿cuál te pareció más difícil de creer?
Yo tengo el número 5 — que la misma máquina haga el original y la copia me costó
aceptarlo hasta que leí cómo funcionan los contratos de producción.

Escribe tu número.
```

Un comentario fijado que abre debate con una opinión propia genera más respuestas que uno que solo pide suscripción.

## Hora de publicación
**Martes o jueves, 19:00 hora de Ciudad de México (UTC-6).** Razón: cubre la franja de 18:00-22:00 en México, Colombia, Perú y Ecuador simultáneamente, que es donde está el volumen de audiencia hispanohablante para contenido de 12 minutos consumido en casa. Evita el fin de semana, donde un canal nuevo compite contra el pico de subidas.

## Declaración de contenido sintético
**Marcar SÍ** en la casilla de "contenido alterado o sintético" al subir. El video entero es recreación generada de hechos reales. Omitir esa declaración en contenido realista generado con IA es una violación de política, y es la primera cosa que revisan cuando reportan un canal nuevo.

---

# BLOQUE 9 — AUDITORÍA DE MONETIZACIÓN

| # | Control | Estado | Nota |
|---|---|---|---|
| 1 | Valor original añadido | ✔ | Diez casos investigados, reconstruidos y conectados por una tesis propia (el manifiesto lo llena quien envía). No es recopilación de clips ni plantilla |
| 2 | No es contenido producido en masa | ✔ | Guion original de 1.688 palabras, estructura narrativa propia, 144 tomas diseñadas una por una |
| 3 | Apto para anunciantes | ✔ | Sin violencia gráfica, sin lenguaje fuerte, sin contenido sexual, sin sustancias. Los primeros 30 s son limpios |
| 4 | Sin material de terceros | ✔ | 100% generado. Música de biblioteca libre. **Acción requerida:** confirmar licencia de la pista antes de subir |
| 5 | Sin afirmaciones médicas, financieras ni legales | ✔ | No se da consejo legal ni financiero. Los casos se narran como hechos, no como asesoría |
| 6 | Título y miniatura coinciden con el contenido | ✔ | El título promete 10 casos y el video entrega 10. La miniatura muestra el caso 1, que está en el video |
| 7 | Marcado de contenido sintético | ⚠ | **Acción requerida al subir:** marcar la casilla. Hasta que no se marque, este control está abierto |
| 8 | Apto para público general | ✔ | No es contenido para niños. Marcar "no está hecho para niños" |
| 9 | Datos verificados | ✖ | **11 marcas `[VERIFICAR]` en el guion.** Ver abajo |

## Los 11 datos a verificar antes de locutar

| Timecode | Dato | Qué confirmar |
|---|---|---|
| 0:18 | ≈1.800 contenedores perdidos en una tormenta, dic. 2020 | Nombre del buque, cifra oficial, fuente de prensa |
| 1:21 | Valor promedio declarado por contenedor | Fuente de aseguradora o cámara de comercio |
| 2:24 | Precio promedio de un pallet de devoluciones | Fuente de liquidador o reporte de industria |
| 3:02 | Plazos de reclamo de equipaje | Varían por aerolínea y por país: confirma el de tu mercado |
| 4:30 | Cifras de robo de carga en tránsito | Reporte de aseguradora por región |
| 5:08 | Procedimiento de destrucción de falsificaciones | Normativa del país que vayas a citar |
| 6:11 | Casos documentados de turno no autorizado | Necesita al menos una fuente periodística |
| 7:14 | Plataformas de subasta de carga abandonada | Nombres reales y condiciones de venta publicadas |
| 8:17 | Naufragios con carga en disputa legal | Caso concreto y jurisdicciones que reclaman |
| 9:20 | Mecánica de caída por bloques + caso dic. 2020 | Fuente técnica de amarre y la nota de prensa del caso |
| 10:23 | Caso Callao / Ancón: año, buque, número de contenedores | **El más importante: es el caso 1 del video** |

**Veredicto:** `RIESGO DE DESMONETIZACIÓN: BAJO` — con una condición. El riesgo de política es bajo porque hay investigación, guion original y tesis propia. El riesgo real de este video no es la desmonetización: es la **credibilidad**. Son once cifras sin verificar en un video cuyo valor entero es que los casos son reales. Si subes esto sin verificar, el primer comentario que desmienta una cifra contamina los otros nueve casos.

No locutes ninguna línea marcada `[VERIFICAR]` sin fuente.

---

# BLOQUE 10 — DERIVADOS Y DISTRIBUCIÓN

## 3 Shorts verticales

### Short 1 — "La playa de las lavadoras" (del caso 1)
- **Origen:** 10:17 - 10:48
- **Duración:** 42 s
- **Gancho reescrito (0-3 s):** "Amaneció y la playa estaba llena de lavadoras nuevas."
- **Texto en pantalla:** `ANCÓN, PERÚ` en el segundo 2 · `¿DE QUIÉN SON?` en el segundo 8
- **CTA:** "La historia completa está en el canal."
- **Tomas que sobreviven al 9:16:** las macro (lavadora en arena, caja empapada, manos levantando la caja). Las aéreas hay que regenerar en vertical.

### Short 2 — "Por qué los contenedores caen por bloques" (del caso 2)
- **Origen:** 9:20 - 9:45
- **Duración:** 38 s
- **Gancho reescrito:** "Los contenedores no van atornillados al barco."
- **Texto en pantalla:** `NO DE UNO EN UNO` en el segundo 5 · `POR BLOQUES` en el segundo 12
- **CTA:** "Caso completo en el canal."
- **Tomas que sobreviven:** la macro de la barra de amarre y la rotura. El plano general del bloque cayendo hay que regenerarlo vertical.

### Short 3 — "El producto de 1 dólar" (del caso 10)
- **Origen:** 0:50 - 1:21
- **Duración:** 45 s
- **Gancho reescrito:** "Esto cuesta un dólar. El plástico cuesta cuatro centavos."
- **Texto en pantalla:** los once pasos de la cadena, apareciendo acumulados
- **CTA:** "Nueve casos más en el canal."
- **Tomas que sobreviven:** todas las macro de fábrica. El pasillo de góndola hay que regenerarlo vertical.

## Reencuadre a 9:16
De las 144 tomas, **sobreviven al corte vertical las 61 macro y primer plano** (el sujeto está centrado y hay aire arriba y abajo). Las **38 tomas aéreas y de gran angular hay que regenerarlas** con `aspect 9:16`: recortar un plano general a vertical destruye la composición y se nota.

## Video secuela
**"Qué pasa cuando un contenedor llega al fondo del mar"** — el caso 3 y el caso 2 dejan abierta la pregunta de qué ocurre después. Video de 10 min sobre el contenedor como objeto en el fondo marino: presión, corrosión, qué sobrevive, qué se libera al agua y por qué casi ninguno se recupera. Conecta directo con el loop de salida de este video.

## Secuencia de publicación
1. Video largo, martes 19:00 México.
2. Short 3 (el de 1 dólar, el más accesible) 24 h después.
3. Short 1 (Ancón, el más fuerte) 72 h después, cuando el video largo ya tiene datos de retención.
4. Short 2 a los 7 días.

Razón del orden: el Short más fuerte va segundo, no primero. Si el primero revienta, el canal recibe tráfico antes de tener retención medida en el video largo y el algoritmo lo clasifica mal.
