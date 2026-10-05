# GUION PARA ELEVENLABS — SOLO NARRACIÓN
**Video 001 · Goods Uncovered · 12:00**

Texto limpio: sin timecodes, sin indicaciones de cámara, sin SFX. Las cifras están escritas en palabras a propósito: un TTS lee "1.800" de forma inconsistente en español, "mil ochocientos" nunca falla.

---

## CONFIGURACIÓN EN ELEVENLABS

| Parámetro | Valor de arranque | Por qué |
|---|---|---|
| Modelo | Eleven Multilingual v2 | Mejor pronunciación de español latino. Usa v3 solo si vas a meter audio tags |
| Stability | 55-65 | Documental necesita consistencia entre bloques. Abajo de 50 la voz cambia de energía entre tomas y se nota al unir |
| Similarity | 70-80 | Suficiente para mantener el timbre sin arrastrar artefactos del sample |
| Style exaggeration | 0-15 | Alto suena a locutor de radio. Este guion es frío y seco |
| Speaker boost | Activado | Mejora la presencia en la voz grave |
| Speed | 1.0 | El ritmo ya está en la puntuación. No lo aceleres: el guion está calculado a 155 ppm |

**Voz:** masculina, 35-45 años, registro grave, acento latino neutro. Si usas una voz de biblioteca, busca etiquetas `narration` + `documentary` + `deep`. Evita las etiquetadas `energetic`, `upbeat` o `commercial`.

---

## CÓMO USAR LOS BLOQUES

Genera **un archivo de audio por bloque**, no todo de una vez. Tres razones:

1. Si un bloque sale mal, regeneras ese y no los doce.
2. Los silencios del guion (hay nueve) se insertan en la línea de tiempo del editor, no en el TTS. Un silencio pedido al TTS sale irregular; uno puesto en la edición es exacto.
3. Cada bloque coincide con un corte musical, así que el audio ya cae alineado al montaje.

**Los nueve silencios a insertar en edición:**

| Después de | Duración |
|---|---|
| "Nadie vino a reclamarlas." (fin bloque 1) | 2.0 s |
| "...sin que nadie sepa qué hay dentro." (caso 9) | 0.8 s |
| "...sigue esperando una llamada." (caso 8) | 0.8 s |
| "Es cuánto no se detecta." (caso 6) | 1.0 s |
| "...se puede imprimir." (caso 5) | 0.8 s |
| "...no valía el costo de reclamarla." (caso 4) | 0.8 s |
| "Lo que la está destruyendo es el juicio." (caso 3) | 0.8 s |
| "...en rutas donde pasan otros barcos." (caso 2) | 0.8 s |
| "...sin que nadie lo escriba." (caso 1) | 1.2 s |

---

## BLOQUE 1 — INTRO · GANCHO DE ENTRADA
`92 caracteres · 14 palabras`

```
Los pescadores de Ancón abrieron un contenedor lleno de lavadoras. Nadie vino a reclamarlas.
```

## BLOQUE 2 — INTRO · DESARROLLO DE GANCHO
`758 caracteres · 137 palabras`

```
Eso no fue un accidente aislado. Cada año, miles de contenedores se pierden en el mar, en puertos, en bodegas y en subastas donde nadie sabe qué está comprando. Mercancía que alguien fabricó, alguien pagó y nadie volvió a ver. En diciembre de 2020, un solo buque perdió cerca de mil ochocientos contenedores en una tormenta del Pacífico. En una noche. Y ese es apenas el número cuatro de esta lista. Vamos a bajar del diez al uno. Carga perdida, carga robada, carga destruida por orden judicial y carga que el mar devolvió a una playa. El número uno pasó en Perú y tiene testigos. Y antes de que lo pienses: no, casi nada de esto se recupera. Las aseguradoras pagan, los números se cierran y la mercancía simplemente deja de existir en el papel. Número diez.
```

## BLOQUE 3 — CASO 10 · "El dólar que no es un dólar"
`789 caracteres · 142 palabras`

```
Este producto cuesta un dólar en la tienda. El material con el que está hecho cuesta cuatro centavos. No es estafa. Es logística. Entre la fábrica y tu mano hay once pasos, y cada paso suma su parte. Molde, inyección de plástico, empaque, pallet, contenedor, flete marítimo, aduana, almacén, distribuidor, tienda, góndola. El objeto es lo más barato de toda la cadena. Lo que estás pagando es el viaje. Por eso cuando un contenedor se cae al mar, lo que se hunde no vale lo que dice la etiqueta. Vale lo que costó moverlo. Y eso sí es dinero real. Y hay una consecuencia que nadie menciona: para la aseguradora, un contenedor hundido se cierra más rápido que uno rescatado. Rescatarlo cuesta más que pagarlo. Lo que nos lleva al número nueve, y a un edificio que no aparece en ningún mapa.
```

## BLOQUE 4 — CASO 9 · "El edificio de las devoluciones"
`821 caracteres · 146 palabras`

```
Devolviste algo que compraste por internet. Lo que no te dijeron es que nunca volvió a la tienda. Revisar una devolución, probarla, reempacarla y volverla a poner en inventario cuesta más que el producto en una buena parte de los casos. Entonces no se revisa. Se apila. Se mete en una caja con otras cuarenta cosas y esa caja se vende por peso a un liquidador. El liquidador la revende sin abrirla. Hay una industria completa construida sobre eso: pallets de devoluciones que se compran a ciegas. Pagas por el peso, no por el contenido. Puede venir un televisor. Pueden venir cuarenta cables cortados. Y una parte de esos pallets nunca se abre. Se revende dos, tres veces, entre liquidadores. La misma caja cambia de dueño sin que nadie sepa qué hay dentro. Número ocho. Y aquí el contenido sí se conoce. Por eso es peor.
```

## BLOQUE 5 — CASO 8 · "Las maletas que nadie reclamó"
`761 caracteres · 137 palabras`

```
Existe un lugar donde se vende el equipaje que las aerolíneas perdieron. Con todo adentro. Cuando una maleta se pierde, la aerolínea la busca por un plazo. Si nadie la reclama en ese plazo, deja de ser tuya y pasa a ser mercancía. Se clasifica, se agrupa y se vende. La ropa por bulto. La electrónica por lote. Los objetos personales, a veces, tal cual quedaron. Y lo que convierte esto en negocio es el volumen. No son maletas sueltas. Son bodegas enteras de equipaje acumulado durante meses, organizado por categoría como si fuera inventario de fábrica. Lo incómodo no es que se venda. Es que la maleta que compras venía con la vida de alguien dentro. Y ese alguien sigue esperando una llamada. Número siete. Carga que sí llegó al puerto, pero no a la tienda.
```

## BLOQUE 6 — CASO 7 · "Los nueve mil kilos que faltan"
`800 caracteres · 143 palabras`

```
El camión salió del puerto con cuarenta toneladas. Llegó con treinta y uno. No fue un asalto. No hubo armas, ni persecución, ni reporte policial. La carga se fue desapareciendo en paradas: una bodega de paso, un cambio de conductor, un pallet que se queda, un sello que se reemplaza por otro idéntico. Para cuando el camión llega a destino, el papel y el contenido ya no coinciden. El robo de carga en tránsito es el tipo de pérdida más difícil de detectar porque no hay un momento del delito. Hay una diferencia en una planilla, semanas después. Y el detalle que lo vuelve casi perfecto: nadie denuncia una carga que el seguro ya pagó. La pérdida se vuelve un costo operativo. Una línea en un presupuesto del año siguiente. Número seis. Mercancía que sí se encontró, y que fue destruida a propósito.
```

## BLOQUE 7 — CASO 6 · "Lo que se destruye por orden judicial"
`682 caracteres · 120 palabras`

```
Esta pila de mercancía vale millones. Mañana va a ser destruida, y es legal. Cuando la aduana incauta producto falsificado, ese producto no se puede donar, no se puede vender y no se puede devolver. Si entra al mercado, aunque sea gratis, sigue siendo una falsificación circulando. Entonces la orden es destruirlo. Se trituran zapatillas nuevas, se funden relojes, se queman cosméticos sellados. Y la cifra que importa no es cuánto se destruye. Es cuánto no se detecta. Lo incautado es la parte que falló. Todo lo demás llegó a su destino y ya se vendió. Y hay un caso que incomoda a todos: cuando la fábrica que hizo la falsificación es la misma que hace el original. Número cinco.
```

## BLOQUE 8 — CASO 5 · "El turno que no existe"
`748 caracteres · 134 palabras`

```
La misma máquina hace el original y la copia. Con doce horas de diferencia. Una fábrica tiene un contrato para producir cien mil unidades. Tiene el molde, el material y la especificación exacta. Produce las cien mil, las entrega y cumple. Y después, con el mismo molde, corre un turno que no está en ningún contrato. Mismo material, mismo proceso, misma calidad. Solo que esas unidades no existen en los libros de nadie. Y por eso estas copias son las más difíciles de detectar. No tienen defecto. No tienen material barato. No tienen error de ortografía en la caja. Son idénticas porque son las mismas. Lo único que las delata es el número de serie. Y el número de serie se puede imprimir. Número cuatro. Y aquí el comprador sabe que no sabe nada.
```

## BLOQUE 9 — CASO 4 · "Comprar una caja cerrada"
`759 caracteres · 140 palabras`

```
Pagó por un contenedor de doce metros sin saber qué había dentro. Nadie se lo dijo. Nadie se lo iba a decir. Existen plataformas donde se subasta carga abandonada: mercancía que llegó a puerto y nadie fue a buscar, lotes que una empresa quebrada dejó en una bodega, carga que el consignatario rechazó. Se publica el peso, el origen, a veces una foto de la puerta cerrada. Y se puja. El negocio no está en acertar. Está en el promedio. Compras diez lotes sabiendo que ocho van a ser basura, uno va a empatar y uno va a pagar los diez. Es estadística, no suerte. Y la pregunta que nadie hace en voz alta: ¿por qué nadie fue a buscar esa carga? Porque alguien, en algún punto, decidió que no valía el costo de reclamarla. Número tres. Trescientos años esperando.
```

## BLOQUE 10 — CASO 3 · "La carga que nadie puede tocar"
`747 caracteres · 133 palabras`

```
Está en el fondo del mar desde hace tres siglos. Se sabe dónde. Y nadie puede tocarla. Cuando se encuentra un naufragio con carga de valor, empieza un problema que no es técnico. Es legal. El país donde se hundió reclama soberanía. El país de la bandera reclama propiedad. La empresa que lo encontró reclama el hallazgo. Y los descendientes de quienes la pagaron reclaman herencia. Mientras eso se discute, la carga se queda donde está. Y el tiempo juega contra todos. Cada año que el pleito sigue abierto, el sitio es más conocido, menos vigilado y más fácil de saquear por quien no piensa reclamar nada. Hay una ironía en esto: la carga sobrevivió trescientos años en el agua. Lo que la está destruyendo es el juicio. Número dos. Una sola noche.
```

## BLOQUE 11 — CASO 2 · "Mil ochocientos en una noche"
`727 caracteres · 128 palabras`

```
Un solo buque. Una sola tormenta. Cerca de mil ochocientos contenedores al agua. Los contenedores no van atornillados al barco. Van trabados entre ellos y amarrados en torres. Cuando un buque se balancea más allá de cierto ángulo, esas torres trabajan como un péndulo. Y cuando una cede, arrastra a las de al lado. No se caen de uno en uno. Se caen por bloques. Y los que caen no se hunden de inmediato. Un contenedor sellado flota. Puede quedar días a la deriva, apenas bajo la superficie, pesando treinta toneladas y sin aparecer en ningún radar. Por eso el verdadero problema no es la pérdida. Es que esos contenedores siguen navegando sin nadie a bordo, en rutas donde pasan otros barcos. Número uno. Y este tiene testigos.
```

## BLOQUE 12 — CASO 1 · "El día que el mar lo devolvió"
`714 caracteres · 128 palabras`

```
Amaneció y la playa estaba cubierta de cajas. Lavadoras. Cosméticos. Electrodomésticos sellados. Frente a la costa de Callao, en Perú, cerca de cincuenta contenedores de un buque cayeron al mar. Días después, la carga empezó a aparecer en las playas de Ancón. No llegó rota. Llegó empacada. Los pescadores y los vecinos del distrito la recogieron de la arena, caja por caja. Y ahí quedó la pregunta que nadie respondió rápido: ¿de quién era eso? De la naviera que la perdió. Del importador que la pagó. De la aseguradora que iba a indemnizarla. O de quien la levantó de la arena a las seis de la mañana. Y esto es lo que conecta los diez casos: la mercancía no desaparece. Cambia de dueño sin que nadie lo escriba.
```

## BLOQUE 13 — FINAL DE GANCHO
`661 caracteres · 127 palabras`

```
Al principio te dije que ibas a ver diez cargamentos que desaparecieron y qué pasó con cada uno. Ahí están. Uno se hundió. Uno se trituró. Uno se subastó a ciegas. Uno lleva tres siglos en un juicio. Y uno terminó en manos de los pescadores de Ancón. Pero hay un dato que dejé para el final. En casi todos estos casos existe un documento que dice exactamente qué había dentro. El problema es que ese documento lo llena quien envía la carga. Nadie lo verifica hasta que ya es tarde. Así que la próxima vez que veas un contenedor pasar en un camión, la pregunta no es qué lleva. Es quién dice que lo lleva. ¿Cuál de los diez te costó más creer? Escribe el número.
```

---

## TOTALES

| Dato | Valor |
|---|---|
| Bloques de audio | 13 |
| Caracteres totales | 9059 |
| Palabras narradas | 1.688 |
| Duración de voz esperada | ~10:54 |
| Silencios en edición | 9 (suman ~9 s) |
| Duración final del video | 12:00 |

La voz no dura 12 minutos: dura cerca de once. Los 66 segundos restantes son los nueve silencios y los pasajes sin narración del gancho y el cierre. Eso es intencional, no un faltante.

**Consumo de créditos:** 9059 caracteres. En ElevenLabs un crédito equivale aproximadamente a un carácter, así que considera ~9.059 créditos por generación completa del video. Si regeneras bloques, suma solo los de ese bloque.
