# BLOQUE 4-B — PROMPTS DE IMAGEN (144)
**Video 001 · Goods Uncovered · flujo imagen primero, animación después**

---

## POR QUÉ ESTE FLUJO ES EL CORRECTO

Generar 144 imágenes y animar solo las que lo necesitan cuesta una fracción de generar 144 videos. Y una imagen fija de 4 s con un Ken Burns del 6% en el editor es indistinguible de un clip generado, siempre que la toma no tenga movimiento propio.

| Decisión | Tomas | Qué hacer |
|---|---|---|
| **ANIMAR** (image-to-video) | **85** | Tienen movimiento intrínseco: agua, fuego, maquinaria, caída, humo, polvo, figuras moviéndose |
| **Ken Burns** (imagen fija + zoom en editor) | **59** | Objetos estáticos: documentos, sellos, pantallas, objetos sobre mesa |

La columna `Decisión` de cada prompt es una propuesta, no una orden. Revísala al ver las imágenes: una imagen que salga mejor de lo esperado vale animarla aunque esté marcada Ken Burns.

**Ken Burns correcto:** zoom del 4-8% sobre la duración de la toma, más un desplazamiento de 2-3% en una sola dirección. Más que eso se ve como presentación de diapositivas. Y agrega grano de película al 10-12% encima: es lo que iguala la textura entre imagen fija y clip animado.

---

## REGLA DE ORO: PRIMER FOTOGRAMA

Cada prompt pide **el instante en que la acción empieza**, no el momento intermedio. Si generas la espuma ya cubriendo la lavadora, el image-to-video no tiene a dónde avanzar y el clip sale muerto. Si generas la espuma a punto de entrar en cuadro, el modelo tiene la trayectoria y el movimiento sale solo.

---

## PARÁMETROS POR GENERADOR

Cada prompt trae la línea de Midjourney y la genérica. Usa la que corresponda a tu herramienta.

| Generador | Línea de parámetros |
|---|---|
| Midjourney v7 | `--ar 16:9 --style raw --v 7 --seed <seed>` |
| Flux / Ideogram / Nano Banana / Seedream | `aspect 16:9 · 2560x1440 · guidance 3.5 · seed <seed>` |
| Higgsfield (generate_image) | `aspect 16:9 · quality high · seed <seed>` |

**Los seeds por locación son obligatorios.** Es lo único que mantiene la misma bodega, la misma playa y la misma fábrica a lo largo de doce tomas. Cambiar el seed entre tomas del mismo lugar es la razón número uno de que un video de IA se vea como clips sin relación.

**Para los Shorts verticales:** regenera con `--ar 9:16`. De las 144, las 61 macro y primer plano aguantan un recorte vertical; las aéreas y los grandes angulares hay que regenerarlas.

---

## HOJA DE DECISIÓN RÁPIDA

| # | Timecode | Dur | Toma | Decisión |
|---|---|-----|------|----------|
| 1 | 0:00 | 2s | Lavadora blanca volcada en arena mojada, espuma entra en cuadr | **ANIMAR** |
| 2 | 0:02 | 2s | Playa al amanecer con cajas y electrodomésticos dispersos 400  | **Ken Burns** |
| 3 | 0:04 | 2s | Puerta de contenedor abierta a medias, oscuridad dentro | **ANIMAR** |
| 4 | 0:06 | 2s | Negro total, una sola palabra entrando | **ANIMAR** |
| 5 | 0:08 | 4s | Buque portacontenedores cargado navegando en mar gris | **ANIMAR** |
| 6 | 0:12 | 4s | Grúa de puerto bajando un contenedor sobre un camión | **ANIMAR** |
| 7 | 0:16 | 4s | Pasillo infinito de bodega con pallets envueltos en film | **Ken Burns** |
| 8 | 0:20 | 4s | Sello metálico de seguridad de contenedor con número grabado | **Ken Burns** |
| 9 | 0:24 | 5s | Buque inclinado en tormenta, torres de contenedores oscilando | **ANIMAR** |
| 10 | 0:29 | 4s | Contenedor girando lentamente mientras se hunde | **ANIMAR** |
| 11 | 0:33 | 4s | Manos llenando a mano un formulario de carga | **Ken Burns** |
| 12 | 0:37 | 4s | Contador digital en pantalla pasando de 10 a 1 | **Ken Burns** |
| 13 | 0:41 | 5s | Playa de Ancón al amanecer, vecinos recogiendo cajas a lo lejo | **ANIMAR** |
| 14 | 0:46 | 4s | Etiqueta de envío mojada e ilegible pegada a una caja | **ANIMAR** |
| 15 | 0:50 | 6s | Objeto plástico barato girando sobre fondo negro | **ANIMAR** |
| 16 | 0:56 | 5s | Etiqueta de precio de 1 dólar siendo pegada | **ANIMAR** |
| 17 | 1:01 | 5s | Molde de inyección cerrándose con presión | **ANIMAR** |
| 18 | 1:06 | 5s | Pellets de plástico cayendo en una tolva | **ANIMAR** |
| 19 | 1:11 | 5s | Cinta de empaque sellando cajas en serie | **ANIMAR** |
| 20 | 1:16 | 5s | Pallet envuelto en film girando en la máquina | **ANIMAR** |
| 21 | 1:21 | 5s | Contenedor cerrándose en el patio del puerto | **ANIMAR** |
| 22 | 1:26 | 5s | Buque saliendo de puerto visto desde arriba | **Ken Burns** |
| 23 | 1:31 | 5s | Sello de aduana golpeando un documento | **Ken Burns** |
| 24 | 1:36 | 5s | Góndola de tienda con el producto en primer plano | **Ken Burns** |
| 25 | 1:41 | 6s | El mismo producto hundiéndose solo en agua oscura | **ANIMAR** |
| 26 | 1:47 | 6s | Formulario de reclamo de seguro con cifra tachada | **Ken Burns** |
| 27 | 1:53 | 6s | Caja de devolución abierta con cinta desgarrada | **Ken Burns** |
| 28 | 1:59 | 5s | Montaña de cajas de devolución sin clasificar | **Ken Burns** |
| 29 | 2:04 | 5s | Trabajador apilando sin revisar el contenido | **ANIMAR** |
| 30 | 2:09 | 5s | Balanza industrial marcando el peso de un pallet | **Ken Burns** |
| 31 | 2:14 | 5s | Montacargas levantando un pallet de cajas mezcladas | **ANIMAR** |
| 32 | 2:19 | 5s | Nave de liquidación con pallets numerados en filas | **Ken Burns** |
| 33 | 2:24 | 5s | Número de lote escrito a mano en el film plástico | **Ken Burns** |
| 34 | 2:29 | 5s | Un televisor nuevo apareciendo entre cables cortados | **Ken Burns** |
| 35 | 2:34 | 5s | Misma caja con tres etiquetas de dueño distintas | **ANIMAR** |
| 36 | 2:39 | 5s | Bodega oscura con un solo pallet iluminado al fondo | **Ken Burns** |
| 37 | 2:44 | 6s | Negro total con partículas de polvo | **ANIMAR** |
| 38 | 2:50 | 6s | Portón de bodega cerrándose y dejando todo en negro | **ANIMAR** |
| 39 | 2:56 | 6s | Maleta cerrada con etiqueta de aerolínea arrancada | **Ken Burns** |
| 40 | 3:02 | 5s | Cinta de equipaje vacía girando sin maletas | **ANIMAR** |
| 41 | 3:07 | 5s | Una sola maleta dando vueltas sola en la cinta | **ANIMAR** |
| 42 | 3:12 | 5s | Bodega enorme con estanterías de maletas numeradas | **Ken Burns** |
| 43 | 3:17 | 5s | Tarjeta de inventario atada al asa de una maleta | **Ken Burns** |
| 44 | 3:22 | 5s | Mesa de clasificación con ropa separada por categoría | **Ken Burns** |
| 45 | 3:27 | 5s | Caja de electrónica recuperada, cables enredados | **Ken Burns** |
| 46 | 3:32 | 5s | Objeto personal evidente: una foto familiar impresa | **Ken Burns** |
| 47 | 3:37 | 5s | Nave de venta con maletas apiladas en lotes | **Ken Burns** |
| 48 | 3:42 | 5s | Teléfono fijo en una oficina vacía sonando | **ANIMAR** |
| 49 | 3:47 | 6s | Formulario de reclamo sin responder sobre un escritorio | **Ken Burns** |
| 50 | 3:53 | 6s | Pasillo de maletas perdiéndose en la oscuridad | **Ken Burns** |
| 51 | 3:59 | 6s | Camión de carga saliendo del portón de un puerto | **ANIMAR** |
| 52 | 4:05 | 5s | Báscula de camiones mostrando 40 toneladas | **ANIMAR** |
| 53 | 4:10 | 5s | Camión detenido en una bodega de paso de noche | **ANIMAR** |
| 54 | 4:15 | 5s | Sello de seguridad siendo cortado con alicate | **ANIMAR** |
| 55 | 4:20 | 5s | Sello nuevo idéntico siendo colocado en su lugar | **ANIMAR** |
| 56 | 4:25 | 5s | Dos pallets quedando atrás en la bodega oscura | **Ken Burns** |
| 57 | 4:30 | 5s | Conductor distinto subiendo a la cabina | **ANIMAR** |
| 58 | 4:35 | 5s | Escáner de código de barras leyendo una planilla | **Ken Burns** |
| 59 | 4:40 | 5s | Pantalla de inventario con una diferencia resaltada | **Ken Burns** |
| 60 | 4:45 | 5s | Camión llegando a destino, descarga ya iniciada | **ANIMAR** |
| 61 | 4:50 | 6s | Impresora de matriz escupiendo un reporte de faltante | **ANIMAR** |
| 62 | 4:56 | 6s | Carpeta archivada entre cientos de carpetas idénticas | **Ken Burns** |
| 63 | 5:02 | 6s | Pila de mercancía incautada en un patio cerrado | **Ken Burns** |
| 64 | 5:08 | 5s | Precinto de evidencia con código y fecha | **ANIMAR** |
| 65 | 5:13 | 5s | Zapatillas nuevas entrando a una trituradora industrial | **ANIMAR** |
| 66 | 5:18 | 5s | Salida de la trituradora con material irreconocible | **ANIMAR** |
| 67 | 5:23 | 5s | Horno industrial con la puerta abriéndose | **ANIMAR** |
| 68 | 5:28 | 5s | Relojes fundiéndose en un crisol | **ANIMAR** |
| 69 | 5:33 | 5s | Cosméticos sellados siendo arrojados a un contenedor | **Ken Burns** |
| 70 | 5:38 | 5s | Firma de un funcionario en el acta de destrucción | **Ken Burns** |
| 71 | 5:43 | 5s | Patio vacío después de la destrucción | **Ken Burns** |
| 72 | 5:48 | 5s | Pila mucho más grande pasando sin ser detectada | **ANIMAR** |
| 73 | 5:53 | 6s | Dos cajas idénticas: una sellada, una incautada | **Ken Burns** |
| 74 | 5:59 | 6s | Máquina industrial arrancando en una nave en penumbra | **ANIMAR** |
| 75 | 6:05 | 6s | Prensa industrial golpeando dos veces | **ANIMAR** |
| 76 | 6:11 | 5s | Línea de producción funcionando a plena luz de día | **ANIMAR** |
| 77 | 6:16 | 5s | Contador mecánico marcando cien mil unidades | **ANIMAR** |
| 78 | 6:21 | 5s | Contrato firmado sobre un escritorio de fábrica | **Ken Burns** |
| 79 | 6:26 | 5s | La misma línea, ahora de noche y sin uniformes | **ANIMAR** |
| 80 | 6:31 | 5s | El mismo molde produciendo la misma pieza | **ANIMAR** |
| 81 | 6:36 | 5s | Cajas sin etiqueta apilándose en un rincón | **Ken Burns** |
| 82 | 6:41 | 5s | Libro de producción con el turno nocturno en blanco | **Ken Burns** |
| 83 | 6:46 | 5s | Dos productos idénticos sobre una mesa de inspección | **Ken Burns** |
| 84 | 6:51 | 5s | Lupa sobre el acabado de un producto, sin defectos | **ANIMAR** |
| 85 | 6:56 | 6s | Impresora láser grabando un número de serie | **ANIMAR** |
| 86 | 7:02 | 6s | Dos cajas saliendo por puertas distintas de la fábrica | **Ken Burns** |
| 87 | 7:08 | 6s | Contenedor cerrado con candado, solo en un patio | **Ken Burns** |
| 88 | 7:14 | 5s | Candado oxidado siendo abierto con una llave | **ANIMAR** |
| 89 | 7:19 | 5s | Pantalla de subasta con pujas subiendo en tiempo real | **Ken Burns** |
| 90 | 7:24 | 5s | Ficha de lote: solo peso, origen y una foto de la puerta | **ANIMAR** |
| 91 | 7:29 | 5s | Martillo de subasta golpeando una mesa | **ANIMAR** |
| 92 | 7:34 | 5s | Puerta de contenedor abriéndose por primera vez | **Ken Burns** |
| 93 | 7:39 | 5s | Interior revelado: cajas apiladas hasta el techo | **Ken Burns** |
| 94 | 7:44 | 5s | Caja abierta mostrando contenido sin valor | **ANIMAR** |
| 95 | 7:49 | 5s | Segunda caja abierta: electrónica nueva en su empaque | **ANIMAR** |
| 96 | 7:54 | 5s | Diez contenedores numerados en fila, uno abierto | **Ken Burns** |
| 97 | 7:59 | 6s | Fichas apiladas cayendo: ocho, una, una | **ANIMAR** |
| 98 | 8:05 | 6s | Puerta de contenedor cerrándose con eco | **ANIMAR** |
| 99 | 8:11 | 6s | Casco de madera antiguo cubierto de sedimento | **ANIMAR** |
| 100 | 8:17 | 5s | Cofre de carga parcialmente enterrado en arena | **ANIMAR** |
| 101 | 8:22 | 5s | Pantalla de sonar marcando una anomalía en el fondo | **ANIMAR** |
| 102 | 8:27 | 5s | Barco de investigación solo en mar abierto | **ANIMAR** |
| 103 | 8:32 | 5s | Cuatro expedientes apilados con sellos distintos | **Ken Burns** |
| 104 | 8:37 | 5s | Sala de tribunal vacía con la luz entrando | **Ken Burns** |
| 105 | 8:42 | 5s | Mapa antiguo con una coordenada marcada a lápiz | **Ken Burns** |
| 106 | 8:47 | 5s | Fondo marino vacío donde algo fue removido | **ANIMAR** |
| 107 | 8:52 | 5s | Embarcación pequeña sin luces sobre el sitio | **ANIMAR** |
| 108 | 8:57 | 5s | Expediente con fecha de apertura de décadas atrás | **Ken Burns** |
| 109 | 9:02 | 6s | Carga intacta después de siglos, iluminada un instante | **ANIMAR** |
| 110 | 9:08 | 6s | Martillo de juez sobre el estrado, sin nadie | **Ken Burns** |
| 111 | 9:14 | 6s | Ola enorme rompiendo contra el casco del buque | **ANIMAR** |
| 112 | 9:20 | 5s | Torres de contenedores apiladas nueve de alto | **Ken Burns** |
| 113 | 9:25 | 5s | Barra de amarre de acero vibrando bajo tensión | **ANIMAR** |
| 114 | 9:30 | 5s | Buque escorando más allá del ángulo seguro | **ANIMAR** |
| 115 | 9:35 | 5s | Barra de amarre reventando en el punto de unión | **ANIMAR** |
| 116 | 9:40 | 5s | Bloque completo de contenedores cayendo al mar | **ANIMAR** |
| 117 | 9:45 | 5s | Decenas de contenedores hundiéndose en formación suelta | **ANIMAR** |
| 118 | 9:50 | 5s | Un contenedor flotando apenas bajo la superficie | **ANIMAR** |
| 119 | 9:55 | 5s | Pantalla de radar sin ninguna señal | **Ken Burns** |
| 120 | 10:00 | 5s | Contenedores a la deriva dispersos en el océano | **ANIMAR** |
| 121 | 10:05 | 6s | Otro buque pasando cerca de un contenedor a la deriva | **ANIMAR** |
| 122 | 10:11 | 6s | Contenedor llegando al fondo y levantando sedimento | **ANIMAR** |
| 123 | 10:17 | 6s | Playa al amanecer cubierta de cajas sin abrir | **ANIMAR** |
| 124 | 10:23 | 5s | Lavadora sellada con film plástico sobre la arena | **ANIMAR** |
| 125 | 10:28 | 5s | Cosméticos sellados dispersos en la línea de marea | **ANIMAR** |
| 126 | 10:33 | 5s | Pescadores a lo lejos cargando cajas al hombro | **ANIMAR** |
| 127 | 10:38 | 5s | Caja de cartón empapada abriéndose por el peso | **ANIMAR** |
| 128 | 10:43 | 5s | Buque portacontenedores lejano en el horizonte | **ANIMAR** |
| 129 | 10:48 | 5s | Contenedores volcados visibles en agua poco profunda | **ANIMAR** |
| 130 | 10:53 | 5s | Cuatro documentos distintos reclamando la misma carga | **Ken Burns** |
| 131 | 10:58 | 5s | Manos levantando una caja de la arena al amanecer | **ANIMAR** |
| 132 | 11:03 | 5s | Playa ya vacía al final del día, solo huellas | **Ken Burns** |
| 133 | 11:08 | 6s | Casilla de un formulario firmada por nadie | **Ken Burns** |
| 134 | 11:14 | 6s | Una sola ola borrando las huellas en la arena | **ANIMAR** |
| 135 | 11:20 | 4s | Grilla de diez imágenes, una por caso, apareciendo | **Ken Burns** |
| 136 | 11:24 | 4s | Contenedor en el fondo, inmóvil | **ANIMAR** |
| 137 | 11:28 | 4s | Material triturado cayendo en cámara lenta | **ANIMAR** |
| 138 | 11:32 | 4s | Martillo de subasta inmóvil sobre la mesa | **Ken Burns** |
| 139 | 11:36 | 4s | Expediente judicial cerrado con cinta | **Ken Burns** |
| 140 | 11:40 | 4s | Playa vacía con una sola caja restante | **ANIMAR** |
| 141 | 11:44 | 4s | Manifiesto de carga siendo llenado a mano | **ANIMAR** |
| 142 | 11:48 | 4s | Sello cayendo sobre el documento, sin revisión | **Ken Burns** |
| 143 | 11:52 | 4s | Camión con contenedor pasando por una carretera | **Ken Burns** |
| 144 | 11:56 | 4s | Pantalla negra con la pregunta final en texto | **ANIMAR** |

---

# LOS 144 PROMPTS


---

## INTRO · GANCHO DE ENTRADA
`0:00 - 0:08` · seed de serie: **104417**

**IMAGEN 1** · `0:00` · 2 s · Macro · **ANIMAR**
```
Extreme macro of a brand-new white washing machine lying on its side half-buried in wet dark sand, sea foam sliding into frame over the control panel, dawn, tight static composition with the subject filling the frame, hard low side light from the east, deep steel blue and rust orange and fog white, 50mm f1.8, heavy 35mm grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 2** · `0:02` · 2 s · Plano general aéreo · **Ken Burns**
```
Wide aerial of an empty dawn beach scattered with sealed cardboard boxes and household appliances across 400 meters of sand, no people, high aerial vantage looking down, soft overcast dawn backlight, deep steel blue and concrete grey and fog white, 24mm f4, anamorphic flare, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 3** · `0:04` · 2 s · Plano medio · **ANIMAR**
```
Medium shot of a rust-streaked shipping container door half open on a beach, pitch black interior, dripping water from the top edge, static locked-off framing framing, hard rim light from the left, rust orange and tar black and fog white, 35mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 4** · `0:06` · 2 s · Plano negro + texto · **ANIMAR**
```
Pure black frame with faint volumetric dust particles drifting slowly, no subject, static locked-off framing, single weak top light catching only the dust, tar black and fog white, 85mm f2, heavy grain, abstract documentary insert, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```


---

## INTRO · DESARROLLO DE GANCHO
`0:08 - 0:50` · seed de serie: **104417**

**IMAGEN 5** · `0:08` · 4 s · Gran angular · **ANIMAR**
```
Wide shot of a fully loaded container ship steaming through grey choppy open sea seen from sea level, stacks of containers nine high, profile composition of the hull with lead room, flat overcast daylight, deep steel blue and concrete grey and rust orange, 70mm f4, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 6** · `0:12` · 4 s · Plano detalle · **ANIMAR**
```
Detail shot of a blue gantry crane lowering a corrugated steel container onto a waiting truck chassis, port at blue hour, high vantage angled down following the load, practical sodium floodlights as key, rust orange and deep steel blue and concrete grey, 50mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 7** · `0:16` · 4 s · Plano general · **Ken Burns**
```
Wide shot down an endless warehouse aisle, pallets shrink-wrapped in plastic film stacked six meters high on both sides, cold fluorescent strip lights overhead, symmetrical one-point perspective down the center, hard overhead fluorescent key, concrete grey and fog white and deep steel blue, 24mm f4, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 8** · `0:20` · 4 s · Macro · **Ken Burns**
```
Extreme macro of a metal container security seal stamped with an engraved serial number, scratched paint, condensation beads, slight twenty degree three-quarter angle, single hard key at 45 degrees, rust orange and tar black and fog white, 100mm macro f2.8, shallow depth of field, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 9** · `0:24` · 5 s · Plano general nocturno · **ANIMAR**
```
Wide night shot of a container ship listing heavily in a violent storm, container stacks swaying, sheets of rain crossing the frame, slightly off-level handheld framing from the deck, harsh practical deck floodlights against black sky, tar black and deep steel blue and fog white, 35mm f1.8, heavy grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 10** · `0:29` · 4 s · Plano subacuático · **ANIMAR**
```
Underwater shot of a single steel container slowly rotating as it sinks into deep blue darkness, bubble trail rising, vertical composition with the container mid-frame, shafts of surface light from above, deep steel blue and tar black and fog white, 28mm f2.8, water particulate, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 11** · `0:33` · 4 s · Primer plano · **Ken Burns**
```
Close-up of weathered hands filling a paper cargo manifest with a ballpoint pen on a metal clipboard, blurred port in background, static locked-off framing framing, subject centered, soft window light from the left, fog white and concrete grey and rust orange, 50mm f1.4, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 12** · `0:37` · 4 s · Plano medio · **Ken Burns**
```
Medium shot of a worn industrial LED counter display mounted on grey metal, digits flickering as they drop, dust on the glass cover, static locked-off framing, single practical glow from the display itself, rust orange and tar black and concrete grey, 85mm f2, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 13** · `0:41` · 5 s · Plano general · **ANIMAR**
```
Wide shot of a Pacific coast beach at sunrise, distant small figures of local residents carrying cardboard boxes across wet sand, fishing boats anchored offshore, high aerial vantage with the subject off-center, golden hour backlight with long shadows, rust orange and deep steel blue and fog white, 35mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 14** · `0:46` · 4 s · Macro · **ANIMAR**
```
Extreme macro of a soaked shipping label peeling off a waterlogged cardboard box, printed text blurred and illegible, sand grains stuck to the adhesive, tight static composition with the subject centered, soft overcast dawn light, fog white and concrete grey and rust orange, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```


---

## CASO 10 · El dólar que no es un dólar
`0:50 - 1:53` · seed de serie: **210530**

**IMAGEN 15** · `0:50` · 6 s · Macro · **ANIMAR**
```
Macro of a cheap injection-molded plastic household object rotating on a matte black turntable, visible mold seam and sprue mark, frontal three-quarter angle, single soft top key with hard rim from behind, fog white and tar black and rust orange, 85mm f2.8, film grain, product documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```

**IMAGEN 16** · `0:56` · 5 s · Primer plano · **ANIMAR**
```
Close-up of a one dollar price sticker being pressed onto plastic packaging by a thumb, slight wrinkle in the label, static locked-off framing, hard retail fluorescent key from above, fog white and rust orange and concrete grey, 100mm macro f4, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```

**IMAGEN 17** · `1:01` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of a steel injection mold clamping shut under hydraulic pressure, steam venting from the seam, oil streaks on the plates, tight static composition on the closing line, hard industrial key with orange practical warning lamp, rust orange and concrete grey and tar black, 50mm f2.8, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```

**IMAGEN 18** · `1:06` · 5 s · Plano detalle · **ANIMAR**
```
Detail shot of translucent plastic pellets pouring into a steel hopper in slow motion, individual pellets bouncing, dust haze, static locked-off framing, hard top key through dust, fog white and concrete grey and deep steel blue, 100mm f4, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```

**IMAGEN 19** · `1:11` · 5 s · Plano general · **ANIMAR**
```
Wide shot of an automated packaging line sealing identical cardboard boxes with tape in rapid succession, blurred motion of the belt, profile composition along the line, cold fluorescent key, concrete grey and fog white and rust orange, 35mm f4, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```

**IMAGEN 20** · `1:16` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of a stacked pallet rotating on a stretch-wrap machine as plastic film spirals around it, film glinting, ninety degree profile angle, hard warehouse key from the right, fog white and concrete grey and deep steel blue, 50mm f2.8, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```

**IMAGEN 21** · `1:21` · 5 s · Plano general · **ANIMAR**
```
Wide shot of a container door swinging shut in a port yard at dusk, worker silhouette pulling the locking bar, stacks of containers behind, static locked-off framing framing from ten meters, sodium floodlight key against blue dusk sky, rust orange and deep steel blue and tar black, 35mm f2.8, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```

**IMAGEN 22** · `1:26` · 5 s · Plano aéreo · **Ken Burns**
```
Top-down aerial of a container ship leaving a port channel, wake spreading behind, tugboat alongside, top-down aerial vantage, flat midday overcast light, deep steel blue and concrete grey and fog white, 24mm f5.6, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```

**IMAGEN 23** · `1:31` · 5 s · Primer plano · **Ken Burns**
```
Close-up of a rubber customs stamp striking a paper declaration form, ink spreading into the fibers, hand blurred by the motion, static locked-off framing, hard desk lamp key at 45 degrees, rust orange and fog white and tar black, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```

**IMAGEN 24** · `1:36` · 5 s · Plano medio · **Ken Burns**
```
Medium shot of a retail shelf with rows of the same cheap plastic product, wide static composition showing the entire aisle, harsh overhead retail fluorescents, fog white and rust orange and concrete grey, 35mm f4, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```

**IMAGEN 25** · `1:41` · 6 s · Plano subacuático · **ANIMAR**
```
Underwater shot of that same cheap plastic product sinking alone through dark blue water, tiny bubbles trailing, vertical composition with the subject mid-frame, single weak shaft of surface light, deep steel blue and tar black and fog white, 50mm f2.8, water particulate, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```

**IMAGEN 26** · `1:47` · 6 s · Macro · **Ken Burns**
```
Extreme macro of an insurance claim form with a printed amount crossed out in blue ink and a lower figure handwritten beside it, paper fibers visible, tight static composition centered on the number, soft desk window light, fog white and deep steel blue and rust orange, 100mm macro f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 210530
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 210530)
```


---

## CASO 9 · El edificio de las devoluciones
`1:53 - 2:56` · seed de serie: **330912**

**IMAGEN 27** · `1:53` · 6 s · Plano medio · **Ken Burns**
```
Medium shot of a returned cardboard box with torn packing tape sitting alone on a concrete floor, contents hidden, a printed return label on top, static locked-off framing with tight static composition with the subject centered, cold overhead fluorescent key, concrete grey and fog white and rust orange, 50mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```

**IMAGEN 28** · `1:59` · 5 s · Plano general · **Ken Burns**
```
Wide shot of an unsorted mountain of returned cardboard boxes piled four meters high inside a vast warehouse, no people, low vantage looking up at the full height, hard industrial top light, concrete grey and fog white and tar black, 24mm f4, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```

**IMAGEN 29** · `2:04` · 5 s · Primer plano · **ANIMAR**
```
Close-up over the shoulder of a warehouse worker in a grey uniform tossing an unopened returned box onto a pallet without inspecting it, slightly off-level handheld framing, hard fluorescent key with cold fill, concrete grey and fog white and deep steel blue, 35mm f2, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```

**IMAGEN 30** · `2:09` · 5 s · Plano detalle · **Ken Burns**
```
Detail shot of an industrial floor scale digital readout showing a pallet weight, scuffed metal plate, cable running off frame, static locked-off framing, single practical glow from the display, rust orange and concrete grey and tar black, 85mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```

**IMAGEN 31** · `2:14` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of a forklift lifting a pallet of mismatched returned boxes, forks sliding under the load, profile composition of the forklift with lead room, hard warehouse key with amber beacon practical, rust orange and concrete grey and fog white, 35mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```

**IMAGEN 32** · `2:19` · 5 s · Plano general · **Ken Burns**
```
Wide shot of a liquidation warehouse floor with numbered pallets in long rows under a steel roof, hand-painted lot numbers on the wrap, slow symmetrical one-point perspective down the central aisle, shafts of daylight from roof skylights, concrete grey and fog white and rust orange, 24mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```

**IMAGEN 33** · `2:24` · 5 s · Macro · **Ken Burns**
```
Extreme macro of a lot number written by hand in thick black marker on stretched plastic wrap, the ink bleeding slightly into the film, tight static composition with the subject centered, soft side light raking across the plastic, fog white and tar black and concrete grey, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```

**IMAGEN 34** · `2:29` · 5 s · Plano medio · **Ken Burns**
```
Medium shot of a brand-new flat screen television partially buried under a tangle of cut power cables inside an open pallet box, static locked-off framing framing with a hand entering frame, hard work-lamp key from the right, fog white and tar black and rust orange, 50mm f2, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```

**IMAGEN 35** · `2:34` · 5 s · Plano detalle · **ANIMAR**
```
Detail shot of a single sealed pallet box carrying three different owner labels stacked over each other, corners worn from handling, thirty degree three-quarter angle, hard single key at 45 degrees, fog white and rust orange and concrete grey, 85mm macro f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```

**IMAGEN 36** · `2:39` · 5 s · Plano general · **Ken Burns**
```
Wide shot of a dark cavernous warehouse with a single pallet lit by one hanging work lamp far at the end, everything else in shadow, symmetrical one-point perspective receding into the frame, single practical hanging lamp as the only key, tar black and rust orange and concrete grey, 35mm f1.8, heavy grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```

**IMAGEN 37** · `2:44` · 6 s · Plano negro · **ANIMAR**
```
Pure black frame with slow drifting dust motes catching a single thin light beam, no subject, static locked-off framing, single hard narrow key, tar black and fog white, 85mm f2, heavy grain, abstract documentary insert, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```

**IMAGEN 38** · `2:50` · 6 s · Plano medio · **ANIMAR**
```
Medium shot of a corrugated steel warehouse roller door descending and closing out the last strip of daylight, static locked-off framing, hard backlight from outside shrinking to nothing, tar black and fog white and concrete grey, 35mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 330912
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 330912)
```


---

## CASO 8 · Las maletas que nadie reclamó
`2:56 - 3:59` · seed de serie: **448126**

**IMAGEN 39** · `2:56` · 6 s · Primer plano · **Ken Burns**
```
Close-up of a closed hard-shell suitcase with a torn airline baggage tag still looped on the handle, scuff marks on the shell, tight static composition centered on the torn tag, soft overhead hangar light, concrete grey and fog white and rust orange, 85mm f2, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```

**IMAGEN 40** · `3:02` · 5 s · Plano general · **ANIMAR**
```
Wide shot of an empty airport baggage carousel turning with no luggage on it, worn rubber slats, terminal lights reflected on the metal, profile composition along the belt, cold practical terminal lighting, concrete grey and deep steel blue and fog white, 35mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```

**IMAGEN 41** · `3:07` · 5 s · Plano detalle · **ANIMAR**
```
Detail shot of one lone suitcase circling an otherwise empty baggage carousel, slight wobble as it turns a corner, static locked-off framing, cold overhead terminal light with reflection on the floor, deep steel blue and fog white and concrete grey, 50mm f2, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```

**IMAGEN 42** · `3:12` · 5 s · Plano general · **Ken Burns**
```
Wide shot of a vast storage hall with steel shelving racks filled with numbered suitcases from floor to ceiling, symmetrical one-point perspective down the aisle, hard overhead industrial light, concrete grey and fog white and rust orange, 24mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```

**IMAGEN 43** · `3:17` · 5 s · Macro · **Ken Burns**
```
Extreme macro of a handwritten inventory card tied with string to a suitcase handle, the number partially smudged, worn cardboard texture, slight twenty degree three-quarter angle from the left, single hard key at 45 degrees, fog white and rust orange and concrete grey, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```

**IMAGEN 44** · `3:22` · 5 s · Plano medio · **Ken Burns**
```
Medium shot of a long sorting table with clothing separated into labeled piles by category, hands out of frame, high overhead vantage angled down over the table, soft diffused overhead light, fog white and concrete grey and rust orange, 35mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```

**IMAGEN 45** · `3:27` · 5 s · Plano detalle · **Ken Burns**
```
Detail shot of a plastic bin filled with recovered electronics, chargers and tangled cables, a cracked phone screen on top, static locked-off framing with tight static composition with the subject centered, hard work-lamp key from above, tar black and concrete grey and fog white, 85mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```

**IMAGEN 46** · `3:32` · 5 s · Primer plano · **Ken Burns**
```
Close-up of a printed family photograph lying face up among unsorted luggage contents, the faces turned away from camera and out of focus, very tight static composition with the subject centered, soft side window light, fog white and rust orange and concrete grey, 100mm f2, shallow depth of field, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```

**IMAGEN 47** · `3:37` · 5 s · Plano general · **Ken Burns**
```
Wide shot of a resale hall with suitcases stacked in numbered lots on wooden pallets, price placards on each lot, profile composition with lead room on both sides, flat daylight through high windows, concrete grey and fog white and rust orange, 28mm f4, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```

**IMAGEN 48** · `3:42` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of an old desk telephone ringing in an empty office, dust on the receiver, a stack of unread forms beside it, static locked-off framing, single desk lamp key with deep shadow, rust orange and tar black and fog white, 50mm f1.8, heavy grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```

**IMAGEN 49** · `3:47` · 6 s · Plano detalle · **Ken Burns**
```
Detail shot of an unanswered lost-baggage claim form on a desk with an empty signature box, pen lying diagonally across it, tight static composition centered on the blank box, soft window light from the left, fog white and concrete grey and deep steel blue, 100mm macro f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```

**IMAGEN 50** · `3:53` · 6 s · Plano general · **Ken Burns**
```
Wide shot down an aisle of shelved suitcases receding into darkness, the far end unlit, symmetrical perspective receding into darkness, single overhead lamp near camera as the only key, tar black and concrete grey and fog white, 35mm f2, heavy grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 448126
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 448126)
```


---

## CASO 7 · Los nueve mil kilos que faltan
`3:59 - 5:02` · seed de serie: **551703**

**IMAGEN 51** · `3:59` · 6 s · Plano general · **ANIMAR**
```
Wide shot of a loaded semi truck pulling out through a port gate at dawn, barrier arm rising, container stacks behind the fence, static locked-off framing framing from twenty meters, low golden hour backlight with long shadows, rust orange and deep steel blue and concrete grey, 35mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```

**IMAGEN 52** · `4:05` · 5 s · Plano detalle · **ANIMAR**
```
Detail shot of a truck weighbridge display board reading a forty tonne figure, weather-stained housing, rain drops on the glass, static locked-off framing, flat overcast light with practical display glow, concrete grey and rust orange and fog white, 85mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```

**IMAGEN 53** · `4:10` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of a semi truck parked inside a dim transit warehouse at night, engine idling with exhaust haze, roller door half open behind it, slightly off-level handheld framing from the shadows, single sodium work lamp as key, rust orange and tar black and concrete grey, 35mm f1.8, heavy grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```

**IMAGEN 54** · `4:15` · 5 s · Macro · **ANIMAR**
```
Extreme macro of a bolt-type security seal being cut by heavy pliers, metal shearing with a burr, gloved fingers in frame, static locked-off framing, hard single key from the left, rust orange and tar black and concrete grey, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```

**IMAGEN 55** · `4:20` · 5 s · Plano detalle · **ANIMAR**
```
Extreme macro of a brand-new identical security seal being pushed into the same latch hole, the number nearly matching the old one, tight static composition with the subject centered, hard single key from the left matching the previous shot, rust orange and tar black and fog white, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```

**IMAGEN 56** · `4:25` · 5 s · Plano general · **Ken Burns**
```
Wide shot of two wrapped pallets left behind alone on a dark warehouse floor as the camera dollies out, tire marks on the concrete, wide static composition with the subject small in frame, single distant work lamp key, tar black and concrete grey and rust orange, 28mm f2, heavy grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```

**IMAGEN 57** · `4:30` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of a different driver climbing into the truck cab, body backlit so the face is not visible, door swinging, static locked-off framing, hard backlight from the warehouse opening, tar black and fog white and rust orange, 50mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```

**IMAGEN 58** · `4:35` · 5 s · Plano detalle · **Ken Burns**
```
Detail shot of a handheld barcode scanner reading a printed manifest sheet, red scan line across the barcode, thumb on the trigger, static locked-off framing, hard desk lamp key, rust orange and fog white and tar black, 85mm macro f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```

**IMAGEN 59** · `4:40` · 5 s · Primer plano · **Ken Burns**
```
Close-up of a warehouse inventory monitor showing a spreadsheet row highlighted with a quantity discrepancy, screen glare and dust, tight static composition centered on the highlighted row, single practical monitor glow as key, deep steel blue and fog white and tar black, 85mm f2, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```

**IMAGEN 60** · `4:45` · 5 s · Plano general · **ANIMAR**
```
Wide shot of the semi truck backed into a receiving dock with unloading already underway, pallets on the ramp, high overhead vantage over the loading platform, flat midday overcast light, concrete grey and fog white and rust orange, 28mm f4, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```

**IMAGEN 61** · `4:50` · 6 s · Plano detalle · **ANIMAR**
```
Detail shot of a dot matrix printer feeding out a shortage report on perforated continuous paper, the paper curling over the desk edge, static locked-off framing, hard overhead office light, fog white and concrete grey and rust orange, 85mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```

**IMAGEN 62** · `4:56` · 6 s · Plano medio · **Ken Burns**
```
Medium shot of a single file folder being slid into place among hundreds of identical folders in a steel filing cabinet, wide static composition showing the full archive wall, cold fluorescent key, concrete grey and fog white and deep steel blue, 35mm f4, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 551703
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 551703)
```


---

## CASO 6 · Lo que se destruye por orden judicial
`5:02 - 6:05` · seed de serie: **667240**

**IMAGEN 63** · `5:02` · 6 s · Plano general · **Ken Burns**
```
Wide shot of a fenced yard stacked with seized merchandise in clear evidence bags and open crates, sneakers and boxed goods visible, low vantage looking up at the full volume, flat harsh midday light, rust orange and concrete grey and fog white, 24mm f5.6, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```

**IMAGEN 64** · `5:08` · 5 s · Plano detalle · **ANIMAR**
```
Extreme macro of an evidence seal sticker with a printed case code and date stretched across a cardboard box flap, slight air bubbles under the tape, tight static composition with the subject centered, hard single key at 45 degrees, fog white and rust orange and tar black, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```

**IMAGEN 65** · `5:13` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of brand-new sneakers tumbling into the intake of an industrial shredder, teeth rotating below, dust puffing up, static locked-off framing, hard industrial key with orange warning lamp practical, rust orange and tar black and concrete grey, 50mm f2.8, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```

**IMAGEN 66** · `5:18` · 5 s · Plano detalle · **ANIMAR**
```
Detail shot of the shredder output chute spilling unrecognizable shredded material into a bin in slow motion, dust haze in the light, static locked-off framing, hard side key through the dust, concrete grey and rust orange and tar black, 85mm f2.8, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```

**IMAGEN 67** · `5:23` · 5 s · Plano general · **ANIMAR**
```
Wide shot of a large industrial furnace door sliding open to reveal glowing interior, heat distortion in the air, tight static composition with the subject centered toward the furnace mouth, the furnace glow itself as the key light, rust orange and tar black and fog white, 35mm f2.8, heat haze, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```

**IMAGEN 68** · `5:28` · 5 s · Plano detalle · **ANIMAR**
```
Detail shot of wristwatches collapsing and melting inside a steel crucible, metal glowing orange, slag forming on the surface, static locked-off framing, the molten metal as the only light source, rust orange and tar black and fog white, 100mm f4, heat haze, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```

**IMAGEN 69** · `5:33` · 5 s · Plano medio · **Ken Burns**
```
Medium shot of sealed cosmetics boxes being thrown into a large waste skip by gloved hands, boxes bouncing on impact, slightly off-level handheld framing, flat overcast daylight, fog white and rust orange and concrete grey, 35mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```

**IMAGEN 70** · `5:38` · 5 s · Primer plano · **Ken Burns**
```
Close-up of an official signing a destruction certificate with a fountain pen, only the hand and cuff visible, rubber stamps beside the page, tight static composition centered on the signature, soft window light from the right, fog white and deep steel blue and rust orange, 100mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```

**IMAGEN 71** · `5:43` · 5 s · Plano general · **Ken Burns**
```
Wide shot of the same fenced yard now completely empty, only tire tracks and scattered debris on the concrete, chain-link fence casting shadows, static locked-off framing, low late afternoon side light, concrete grey and rust orange and fog white, 28mm f5.6, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```

**IMAGEN 72** · `5:48` · 5 s · Plano detalle · **ANIMAR**
```
Detail shot tracking fast past an immense stack of identical unmarked cardboard boxes moving on a conveyor, no inspection point visible, profile composition with strong motion blur across the frame, hard overhead fluorescent key with motion blur, concrete grey and fog white and rust orange, 35mm f4, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```

**IMAGEN 73** · `5:53` · 6 s · Plano medio · **Ken Burns**
```
Medium shot of two visually identical cardboard boxes side by side on a steel table, one with an evidence seal and one without, forty-five degree three-quarter angle, hard single key at 45 degrees with deep shadow, fog white and rust orange and tar black, 50mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```

**IMAGEN 74** · `5:59` · 6 s · Plano general · **ANIMAR**
```
Wide shot of a large industrial press starting up in a dim factory hall, belts beginning to turn, dust rising in the light shafts, tight static composition with the subject centered, single hard work lamp plus roof skylight shafts, concrete grey and rust orange and tar black, 28mm f2.8, heavy grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 667240
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 667240)
```


---

## CASO 5 · El turno que no existe
`6:05 - 7:08` · seed de serie: **773815**

**IMAGEN 75** · `6:05` · 6 s · Plano detalle · **ANIMAR**
```
Extreme detail of an industrial press head striking a steel die twice in succession, sparks and oil mist on impact, static locked-off framing, hard single industrial key from the right, rust orange and tar black and concrete grey, 100mm f4, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```

**IMAGEN 76** · `6:11` · 5 s · Plano general · **ANIMAR**
```
Wide shot of a fully staffed production line running in daylight with workers in uniform at their stations, product moving on the belt, profile composition along the line, bright diffused daylight through factory windows, fog white and concrete grey and deep steel blue, 28mm f4, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```

**IMAGEN 77** · `6:16` · 5 s · Plano detalle · **ANIMAR**
```
Extreme macro of a mechanical counter wheel display reading a one hundred thousand figure on a greasy machine panel, worn digits, tight static composition with the subject centered, single practical panel lamp as key, rust orange and tar black and fog white, 100mm macro f3.5, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```

**IMAGEN 78** · `6:21` · 5 s · Plano medio · **Ken Burns**
```
Medium shot of a signed production contract lying on a metal factory desk beside a hard hat and a mug, fluorescent reflection on the plastic sleeve, static locked-off framing, cold overhead fluorescent key, fog white and concrete grey and rust orange, 50mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```

**IMAGEN 79** · `6:26` · 5 s · Plano general · **ANIMAR**
```
Wide shot of the exact same production line running at night with unidentifiable workers in plain clothes, most ceiling lights off, profile composition matched to the daylight shot, single row of work lamps as key, tar black and rust orange and concrete grey, 28mm f2, heavy grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```

**IMAGEN 80** · `6:31` · 5 s · Plano detalle · **ANIMAR**
```
Extreme detail of the identical steel mold ejecting the identical part, same oil streaks and same wear marks as before, static locked-off framing framing, matched to the earlier shot, single hard key from the right, rust orange and concrete grey and tar black, 100mm f4, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```

**IMAGEN 81** · `6:36` · 5 s · Plano medio · **Ken Burns**
```
Medium shot of unlabeled cardboard boxes stacking up in a dark factory corner away from the main line, no markings at all, tight static composition with the subject centered, single distant work lamp key leaving the stack half in shadow, tar black and concrete grey and fog white, 50mm f2, heavy grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```

**IMAGEN 82** · `6:41` · 5 s · Plano detalle · **Ken Burns**
```
Extreme macro of a production logbook page where the night shift row is completely blank while every other row is filled in pen, tight static composition centered on the empty row, soft desk lamp light, fog white and concrete grey and rust orange, 100mm macro f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```

**IMAGEN 83** · `6:46` · 5 s · Plano medio · **Ken Burns**
```
Medium shot of two identical finished products placed side by side on a white inspection table under measurement tools, no visible difference between them, frontal symmetrical angle on both subjects, even soft box lighting from above, fog white and concrete grey and deep steel blue, 50mm f4, film grain, product documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```

**IMAGEN 84** · `6:51` · 5 s · Macro · **ANIMAR**
```
Extreme macro through a magnifying lens examining a product surface finish with no defects, flawless molding texture, tight static composition with the subject centered through the lens, hard single inspection lamp, fog white and concrete grey and rust orange, 100mm macro f4, film grain, product documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```

**IMAGEN 85** · `6:56` · 6 s · Plano detalle · **ANIMAR**
```
Extreme detail of a laser marking head engraving a serial number onto a product housing, faint smoke and a bright beam point tracking across the surface, static locked-off framing, the laser point as the dominant light source, rust orange and tar black and fog white, 100mm f4, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```

**IMAGEN 86** · `7:02` · 6 s · Plano general · **Ken Burns**
```
Wide symmetrical shot of two identical boxes exiting the factory through two different loading doors at once, one door lit and one dark, static locked-off framing, split lighting with hard key on the left door only, rust orange and tar black and concrete grey, 28mm f4, anamorphic, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 773815
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 773815)
```


---

## CASO 4 · Comprar una caja cerrada
`7:08 - 8:11` · seed de serie: **889402**

**IMAGEN 87** · `7:08` · 6 s · Plano general · **Ken Burns**
```
Wide shot of a single closed shipping container with a heavy padlock standing alone in an empty gravel yard, weeds at the base, tight static composition with the subject centered toward the door, flat overcast daylight, rust orange and concrete grey and fog white, 35mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```

**IMAGEN 88** · `7:14` · 5 s · Macro · **ANIMAR**
```
Extreme macro of a rusted padlock being opened with a key, flakes of rust falling, gloved fingertips in frame, static locked-off framing, hard single key from the left, rust orange and tar black and concrete grey, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```

**IMAGEN 89** · `7:19` · 5 s · Primer plano · **Ken Burns**
```
Close-up of an online auction screen with bid amounts incrementing in real time, a countdown timer in red, cursor hovering, tight static composition centered on the figure, single monitor glow as key in a dark room, deep steel blue and rust orange and tar black, 85mm f2, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```

**IMAGEN 90** · `7:24` · 5 s · Plano detalle · **ANIMAR**
```
Detail shot of a printed auction lot sheet listing only weight and origin with one small photograph of a closed container door, no contents described, static locked-off framing, soft desk window light, fog white and concrete grey and rust orange, 85mm macro f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```

**IMAGEN 91** · `7:29` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of a wooden auction gavel striking a worn table surface, dust jumping on impact, blurred hand, static locked-off framing, hard single overhead key, rust orange and tar black and fog white, 50mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```

**IMAGEN 92** · `7:34` · 5 s · Plano general · **Ken Burns**
```
Wide shot of container doors swinging fully open for the first time, dust and stale air rolling out, the interior still dark, frontal composition at the threshold looking in, hard daylight raking in from behind camera, rust orange and tar black and fog white, 28mm f2.8, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```

**IMAGEN 93** · `7:39` · 5 s · Plano medio · **Ken Burns**
```
Medium shot of the revealed container interior packed to the ceiling with unmarked cardboard boxes, a narrow gap down the middle, frontal static composition with depth ahead of the subject along that gap, single hard light source from the open door behind camera, concrete grey and rust orange and tar black, 35mm f2.8, heavy grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```

**IMAGEN 94** · `7:44` · 5 s · Plano detalle · **ANIMAR**
```
Detail shot of an opened box revealing worthless contents, loose packing foam and broken plastic fittings, nothing salvageable, static locked-off framing, hard single work lamp from above, fog white and concrete grey and tar black, 85mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```

**IMAGEN 95** · `7:49` · 5 s · Plano detalle · **ANIMAR**
```
Detail shot of a second opened box revealing brand-new boxed electronics in pristine packaging, protective film still on the surfaces, static locked-off framing, hard single work lamp from above matching the previous shot, fog white and deep steel blue and rust orange, 85mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```

**IMAGEN 96** · `7:54` · 5 s · Plano general · **Ken Burns**
```
Wide aerial of ten numbered containers in a row on a gravel yard with only one of them open, long shadows between them, high aerial vantage looking down, low golden hour side light, rust orange and concrete grey and deep steel blue, 24mm f5.6, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```

**IMAGEN 97** · `7:59` · 6 s · Plano detalle · **ANIMAR**
```
Extreme detail of stacked betting chips collapsing in slow motion on a dark surface, separating into an uneven group and two single chips, static locked-off framing, hard single top key with deep shadow, rust orange and tar black and fog white, 100mm f2.8, film grain, abstract documentary insert, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```

**IMAGEN 98** · `8:05` · 6 s · Plano medio · **ANIMAR**
```
Medium shot of the container door swinging shut and sealing out all light, the last strip of daylight narrowing to nothing, static locked-off framing, hard backlight shrinking to black, tar black and rust orange and fog white, 35mm f2.8, heavy grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 889402
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 889402)
```


---

## CASO 3 · La carga que nadie puede tocar
`8:11 - 9:14` · seed de serie: **912664**

**IMAGEN 99** · `8:11` · 6 s · Plano subacuático · **ANIMAR**
```
Underwater wide shot of an ancient wooden ship hull encrusted with sediment and marine growth resting on a dark seabed, three-quarter angle on the hull, single cold diving light from the left with deep blue falloff, deep steel blue and tar black and concrete grey, 24mm f2.8, water particulate, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```

**IMAGEN 100** · `8:17` · 5 s · Plano detalle subacuático · **ANIMAR**
```
Underwater detail of a partially sand-buried cargo chest with corroded iron bands, small fish passing through frame, tight static composition with the subject centered, single cold diving light raking across the lid, deep steel blue and rust orange and tar black, 50mm f2.8, water particulate, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```

**IMAGEN 101** · `8:22` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of a vessel sonar display showing a rectangular anomaly on the seabed scan, green sweep line crossing it, instrument panel in darkness, static locked-off framing, single display glow as the only key, deep steel blue and fog white and tar black, 85mm f2, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```

**IMAGEN 102** · `8:27` · 5 s · Plano general · **ANIMAR**
```
Wide aerial of a small research vessel alone on flat open sea with survey equipment on the aft deck, high three-quarter aerial vantage, flat high overcast light, deep steel blue and fog white and concrete grey, 24mm f5.6, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```

**IMAGEN 103** · `8:32` · 5 s · Plano detalle · **Ken Burns**
```
Detail shot of four thick legal case files stacked on a dark wooden desk, each bearing a different official seal and ribbon, high overhead vantage angled down over the stack, soft window light from the right, fog white and rust orange and deep steel blue, 85mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```

**IMAGEN 104** · `8:37` · 5 s · Plano medio · **Ken Burns**
```
Medium shot of an empty courtroom with dust suspended in shafts of window light, benches in rows, symmetrical one-point perspective down the central aisle, hard window side light with strong shafts, fog white and concrete grey and rust orange, 35mm f2.8, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```

**IMAGEN 105** · `8:42` · 5 s · Plano detalle · **Ken Burns**
```
Extreme macro of an antique nautical chart with a single coordinate marked in pencil, paper creases and foxing stains, tight static composition centered on the pencil mark, soft raking side light across the paper texture, fog white and rust orange and concrete grey, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```

**IMAGEN 106** · `8:47` · 5 s · Plano subacuático · **ANIMAR**
```
Underwater wide shot of a disturbed seabed depression where an object was clearly removed, drag marks in the sediment, profile composition with lead room on both sides, single cold diving light with deep blue falloff, deep steel blue and tar black and concrete grey, 28mm f2.8, water particulate, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```

**IMAGEN 107** · `8:52` · 5 s · Plano general nocturno · **ANIMAR**
```
Wide night shot of a small unlit boat holding position on dark water, only a single dim lamp on deck, no other vessels in sight, static locked-off framing framing from a distance, that single deck lamp as the only key against black sea and sky, tar black and rust orange and deep steel blue, 85mm f1.8, heavy grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```

**IMAGEN 108** · `8:57` · 5 s · Plano detalle · **Ken Burns**
```
Detail shot of a legal file cover showing a case opening date decades in the past, the cardboard sun-faded and the ink browned, static locked-off framing, flat soft overhead light, fog white and rust orange and concrete grey, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```

**IMAGEN 109** · `9:02` · 6 s · Plano subacuático · **ANIMAR**
```
Underwater detail of intact cargo surviving centuries under sediment, briefly lit as a diving lamp sweeps across it then falling back into darkness, tight static composition with the subject centered, single moving diving light as the only key, deep steel blue and rust orange and tar black, 50mm f2.8, water particulate, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```

**IMAGEN 110** · `9:08` · 6 s · Plano medio · **Ken Burns**
```
Medium shot of a judge's gavel resting alone on an empty bench in a dim courtroom, dust settled on the wood, static locked-off framing, single hard shaft of window light hitting only the gavel, tar black and fog white and rust orange, 85mm f2, heavy grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 912664
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 912664)
```


---

## CASO 2 · Mil ochocientos en una noche
`9:14 - 10:17` · seed de serie: **101338**

**IMAGEN 111** · `9:14` · 6 s · Plano general nocturno · **ANIMAR**
```
Wide night shot of a massive wave exploding against the steel hull of a container ship, spray crossing the entire frame, slightly off-level handheld framing from the upper deck, harsh practical deck floodlights cutting through rain, tar black and fog white and deep steel blue, 35mm f1.8, heavy grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```

**IMAGEN 112** · `9:20` · 5 s · Plano general · **Ken Burns**
```
Wide shot of container stacks nine high lashed together on deck seen from below, steel lashing rods under tension, low vantage looking up the face of the stacks, overcast flat daylight, rust orange and deep steel blue and concrete grey, 24mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```

**IMAGEN 113** · `9:25` · 5 s · Macro · **ANIMAR**
```
Extreme macro of a steel lashing rod vibrating under extreme tension, paint cracking around the turnbuckle, salt crust on the metal, static locked-off framing, hard single key from the right, rust orange and tar black and concrete grey, 100mm f4, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```

**IMAGEN 114** · `9:30` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of a container ship listing far past safe angle in heavy seas, the horizon line steeply tilted in frame, dutch angle with a steeply tilted horizon, flat storm daylight, deep steel blue and concrete grey and fog white, 35mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```

**IMAGEN 115** · `9:35` · 5 s · Plano detalle · **ANIMAR**
```
Extreme detail of a lashing rod snapping at the turnbuckle in slow motion, metal fragments and paint flakes flying, static locked-off framing, hard single key with spray in the air, rust orange and tar black and fog white, 100mm f4, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```

**IMAGEN 116** · `9:40` · 5 s · Plano general · **ANIMAR**
```
Wide shot of an entire block of containers toppling off the deck into the sea at once, massive white impact plume, static locked-off framing framing from the bow, harsh storm daylight, deep steel blue and fog white and rust orange, 24mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```

**IMAGEN 117** · `9:45` · 5 s · Plano subacuático · **ANIMAR**
```
Underwater wide shot of dozens of containers sinking in a loose scattered formation through blue water, bubble columns rising between them, vertical composition with the group mid-frame, surface light shafts from above, deep steel blue and tar black and rust orange, 24mm f2.8, water particulate, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```

**IMAGEN 118** · `9:50` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of a single sealed container floating just below the water surface with only a corner breaking through, waves washing over it, profile composition at water level, hard low sun glare off the water, deep steel blue and fog white and rust orange, 50mm f4, anamorphic flare, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```

**IMAGEN 119** · `9:55` · 5 s · Plano detalle · **Ken Burns**
```
Detail shot of a ship radar display with a clean sweep and no contacts at all, green phosphor trace, scratches on the screen cover, static locked-off framing, single display glow as the only key on a dark bridge, deep steel blue and tar black and fog white, 85mm f2, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```

**IMAGEN 120** · `10:00` · 5 s · Plano aéreo · **ANIMAR**
```
Top-down aerial of scattered drifting containers spread across open ocean, wakes and foam trails behind each one, very high aerial vantage showing the full spread, flat high overcast light, deep steel blue and fog white and rust orange, 24mm f5.6, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```

**IMAGEN 121** · `10:05` · 6 s · Plano general · **ANIMAR**
```
Wide shot at water level of another container ship passing close to a half-submerged drifting container, scale contrast extreme, static locked-off framing, flat overcast daylight with haze, deep steel blue and concrete grey and fog white, 70mm f5.6, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```

**IMAGEN 122** · `10:11` · 6 s · Plano subacuático · **ANIMAR**
```
Underwater shot of a container reaching the seabed and raising a slow billowing cloud of sediment on impact, vertical composition looking down at the impact point, single cold light from above with deep blue falloff, deep steel blue and tar black and concrete grey, 28mm f2.8, water particulate, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 101338
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 101338)
```


---

## CASO 1 · El día que el mar lo devolvió
`10:17 - 11:20` · seed de serie: **104417**

**IMAGEN 123** · `10:17` · 6 s · Plano general · **ANIMAR**
```
Wide aerial of a Pacific beach at sunrise completely strewn with unopened cardboard boxes along the tideline, wet sand reflecting the sky, no people yet, high aerial vantage looking down, low golden hour backlight with long shadows, rust orange and deep steel blue and fog white, 24mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 124** · `10:23` · 5 s · Macro · **ANIMAR**
```
Macro of a sealed washing machine still wrapped in factory plastic film lying on wet sand, film torn at one corner with sand inside, thirty degree three-quarter angle, low golden hour side light, fog white and rust orange and concrete grey, 85mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 125** · `10:28` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of sealed cosmetics boxes and bottles scattered along the tideline, foam washing around them, labels still intact, high overhead vantage angled down over the sand, soft dawn light, fog white and rust orange and deep steel blue, 50mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 126** · `10:33` · 5 s · Plano general · **ANIMAR**
```
Wide shot of distant fishermen in silhouette carrying cardboard boxes on their shoulders across wet sand toward small boats, faces not visible, profile composition with lead room on both sides, low golden hour backlight, rust orange and deep steel blue and tar black, 70mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 127** · `10:38` · 5 s · Plano detalle · **ANIMAR**
```
Detail shot of a waterlogged cardboard box splitting open under the weight of its own contents, soaked fibers sagging, sand stuck to the seams, static locked-off framing, soft overcast dawn light, fog white and concrete grey and rust orange, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 128** · `10:43` · 5 s · Plano general · **ANIMAR**
```
Wide telephoto shot of a container ship far out on the horizon at dawn, heat shimmer compressing the image, calm sea in the foreground, static locked-off framing, low sun backlight through haze, deep steel blue and rust orange and fog white, 200mm f5.6, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 129** · `10:48` · 5 s · Plano aéreo · **ANIMAR**
```
Top-down aerial of overturned containers visible through shallow clear coastal water, sand clouds around them, low aerial vantage close to the water surface, high sun with strong water caustics, deep steel blue and rust orange and fog white, 24mm f5.6, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 130** · `10:53` · 5 s · Plano detalle · **Ken Burns**
```
Detail shot of four different official documents laid side by side on a dark table, each with a different letterhead and seal claiming the same cargo, high overhead vantage angled down over all four, soft diffused overhead light, fog white and deep steel blue and rust orange, 50mm f4, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 131** · `10:58` · 5 s · Plano medio · **ANIMAR**
```
Medium shot of weathered hands lifting a wet cardboard box out of the sand at dawn, only hands and forearms in frame, water draining from the bottom of the box, static locked-off framing, low golden hour side light, rust orange and fog white and concrete grey, 50mm f2, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 132** · `11:03` · 5 s · Plano general · **Ken Burns**
```
Wide aerial of the same beach empty at the end of the day, only footprints and drag marks left in the sand, long shadows, high aerial vantage looking down, low late afternoon side light, concrete grey and rust orange and deep steel blue, 24mm f5.6, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 133** · `11:08` · 6 s · Plano detalle · **Ken Burns**
```
Extreme macro of an official cargo form with the ownership box left entirely blank, pen resting across the page, paper fibers and a faint coffee ring, tight static composition centered on the empty box, soft window light from the left, fog white and concrete grey and deep steel blue, 100mm macro f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 134** · `11:14` · 6 s · Plano general · **ANIMAR**
```
Wide shot of a single wave washing over footprints in wet sand and erasing them completely, foam receding, static locked-off framing framing on the sand, low golden hour backlight, rust orange and deep steel blue and fog white, 35mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```


---

## FINAL DE GANCHO
`11:20 - 12:00` · seed de serie: **104417**

**IMAGEN 135** · `11:20` · 4 s · Plano general · **Ken Burns**
```
Wide shot of a dark wall of ten framed photographs arranged in a grid, each showing a different cargo scene, lighting up one by one, static locked-off framing, single hard key per frame as it lights, tar black and rust orange and fog white, 35mm f4, film grain, abstract documentary insert, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 136** · `11:24` · 4 s · Plano subacuático · **ANIMAR**
```
Underwater wide shot of a container resting motionless on the seabed half covered in sediment, no movement at all, static locked-off framing, single cold light from above with deep blue falloff, deep steel blue and tar black and concrete grey, 28mm f2.8, water particulate, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 137** · `11:28` · 4 s · Plano detalle · **ANIMAR**
```
Detail shot of shredded material falling in slow motion through a shaft of dusty light, individual fragments tumbling, static locked-off framing, hard single side key through the dust, concrete grey and rust orange and tar black, 85mm f2.8, film grain, industrial documentary, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 138** · `11:32` · 4 s · Plano medio · **Ken Burns**
```
Medium shot of an auction gavel lying still on a worn table in an empty room, dust settled around it, static locked-off framing, single hard overhead key with deep shadow, rust orange and tar black and fog white, 50mm f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 139** · `11:36` · 4 s · Plano detalle · **Ken Burns**
```
Detail shot of a closed legal case file bound with faded ribbon on a dark desk, the cardboard sun-bleached, static locked-off framing, soft raking window light, fog white and rust orange and concrete grey, 85mm macro f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 140** · `11:40` · 4 s · Plano general · **ANIMAR**
```
Wide shot of an empty beach at dusk with one single cardboard box remaining at the tideline, foam reaching it, static locked-off framing, low dusk backlight, deep steel blue and rust orange and fog white, 35mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 141** · `11:44` · 4 s · Macro · **ANIMAR**
```
Extreme macro of a cargo manifest being filled in by hand, the pen forming a quantity figure, paper grain visible under raking light, tight static composition centered on the writing, soft desk window light, fog white and concrete grey and rust orange, 100mm macro f2.8, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 142** · `11:48` · 4 s · Primer plano · **Ken Burns**
```
Close-up of a rubber stamp striking a cargo manifest with no inspection taking place around it, ink spreading into the paper, static locked-off framing, hard desk lamp key at 45 degrees, rust orange and fog white and tar black, 100mm macro f3.5, film grain, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 143** · `11:52` · 4 s · Plano general · **Ken Burns**
```
Wide shot of a semi truck hauling a shipping container along an open highway at dusk, dust trailing behind, profile composition of the truck with lead room, low dusk backlight with long shadows, rust orange and deep steel blue and concrete grey, 50mm f4, anamorphic, documentary realism, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```

**IMAGEN 144** · `11:56` · 4 s · Plano medio · **ANIMAR**
```
Medium shot of a pure black frame with slow drifting dust motes and a single thin beam of light crossing the lower third, no subject, static locked-off framing, single hard narrow key, tar black and fog white, 85mm f2, heavy grain, abstract documentary insert, first frame of the shot, captured at the instant the action begins. Negative: no on-screen text, no watermarks, no logos, no brand names, no readable signage, no distorted hands, no deformed faces, no recognizable real people, no cartoon look, no oversaturation, no lens dirt overlay.
--ar 16:9 --style raw --v 7 --seed 104417
(genérico: aspect 16:9 · 2560x1440 · guidance 3.5 · seed 104417)
```


---

## RESUMEN

| Dato | Valor |
|---|---|
| Prompts de imagen | 144 |
| A animar (image-to-video) | 85 |
| A resolver con Ken Burns | 59 |
| Seeds de locación | 8 |
| Segundos cubiertos | 720 / 720 |