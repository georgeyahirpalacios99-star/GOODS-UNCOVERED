# Instrucción para Claude en tu Chrome (cópiala completa)

```
Usa la skill "director-flow" y sigue todas sus reglas (fórmula de prompts, revisión de calidad, arreglos rápidos y reporte final).

Eres mi asistente de producción para el canal de YouTube "Goods Uncovered". Tienes control de mi navegador Chrome. Tu trabajo es generar en Google Flow (labs.google/flow) las imágenes y los videos de mi próximo video largo: "¿Qué pasaría si desaparece Sinaloa?". Es un documental realista y profesional, nada infantil.

OBJETIVO
Generar las 46 tomas de la lista de abajo, revisar su calidad y descargarlas con su nombre exacto. No publiques nada, no compres créditos y no cambies la configuración de mi cuenta. Si Flow pide pagar, se acaban los créditos o aparece un captcha, detente y avísame.

PASOS EN FLOW
1. Abre Flow y crea un proyecto nuevo llamado: GU-007 Sinaloa.
2. Para cada toma, en el orden de la lista:
   a. IMAGEN: elige el modelo Nano Banana Pro y la relación 16:9. Escribe el BLOQUE ESTILO + un espacio + el texto de IMAGEN de esa toma. Genera 2 variantes.
   b. REVISA las 2 con el CHECKLIST y quédate con la mejor. Si ninguna pasa, genera 2 más una sola vez; si siguen sin pasar, anota el ID como "fallido" y sigue con la siguiente.
   c. VIDEO (solo si la toma tiene línea VIDEO): sobre la imagen elegida usa imagen a video con Veo 3.1 Fast, 8 segundos y el audio apagado. Escribe el texto de VIDEO + un espacio + el BLOQUE MOVIMIENTO. Revisa el resultado con el CHECKLIST; si falla, regenera una sola vez.
   d. DESCARGA: el video como ID.mp4 (por ejemplo S01.mp4). Si la toma no tiene VIDEO, descarga la imagen como ID.jpg. Guárdalo todo en una carpeta llamada GU-007-clips.
3. Si los créditos no alcanzan para todo, haz primero las tomas marcadas con ⭐ y después las demás en orden.
4. Al terminar, dame un reporte con: las tomas listas, las fallidas y por qué, y los créditos que quedan.

CHECKLIST (todo tiene que cumplirse)
- No hay texto, letras, letreros, logos, marcas ni banderas.
- No hay caras reconocibles: la gente sale de espaldas, lejos o desenfocada.
- No hay manos, cuerpos ni objetos deformes.
- No hay armas, sangre, policías ni militares.
- Se ve como una foto real de documental, no como dibujo ni como 3D de videojuego.
- En el video, la cámara se mueve suave y nada se deforma, cambia de forma ni aparece de la nada.

BLOQUE ESTILO (va antes de cada prompt de imagen)
Ultra-realistic documentary photograph, shot on a full-frame cinema camera, 35mm lens, natural light, subtle film grain, muted teal-and-amber color grade, high dynamic range, sharp details. Northwestern Mexico, Pacific coast state of Sinaloa. 16:9. No text, no signs, no logos, no flags, no watermark. People only from behind, far away or out of focus, no recognizable faces. No weapons, no police, no military, no blood.

BLOQUE MOVIMIENTO (va después de cada prompt de video)
Smooth, slow, realistic camera movement. Keep every object exactly as in the image, no morphing, no new objects appearing, no text, no audio.

USO DE CADA TOMA (solo para que entiendas; no lo escribas en el prompt)
PRINCIPAL = irá a pantalla completa: tiene que ser espectacular.
RECUADRO = irá pequeño, en una tarjeta sobre un mapa: el sujeto tiene que verse claro en el centro.
FOTO-IA = imagen fija, sin video.

LISTA DE TOMAS
S01 ⭐ [PRINCIPAL] IMAGEN: Aerial view at dawn of a Pacific coastal city with a long seafront boulevard, green hills and a rocky island with a lighthouse, soft morning haze.
    VIDEO: Slow drone push-in toward the city, then a thick white sea fog rolls in and swallows the whole city.
S02 ⭐ [RECUADRO] IMAGEN: Supermarket produce aisle in the United States, crates of red tomatoes, one crate almost empty, cold fluorescent light, shallow depth of field.
    VIDEO: Slow dolly along the aisle toward the nearly empty crate.
S03 ⭐ [RECUADRO] IMAGEN: Small Mexican tortilla shop before sunrise, steel tortilla machine with fresh tortillas coming out on the conveyor, steam rising, warm light.
    VIDEO: Static close shot, tortillas move along the conveyor, steam drifts.
S04 ⭐ [RECUADRO] IMAGEN: Restaurant kitchen pass with an empty white plate under a heat lamp, a lime wedge beside it, blurred cooks in the background.
    VIDEO: Slow push-in on the empty plate, background cooks move out of focus.
S05 ⭐ [PRINCIPAL] IMAGEN: A paper map of Mexico on a wooden table; on the northwest Pacific coast there is a burnt hole in the paper with glowing ember edges and thin smoke.
    VIDEO: Top-down, the ember edges glow and the hole slowly widens, smoke curls up.
S06 [PRINCIPAL] IMAGEN: Endless rugged mountain range with deep canyons and low clouds filling the valleys, golden late light.
    VIDEO: Slow aerial glide over the ridges, clouds flow through the canyons.
S07 [RECUADRO] IMAGEN: Extremely tall cable-stayed bridge spanning a deep forested canyon, empty highway, clouds below the deck.
    VIDEO: Slow orbit around the main tower.
S08 [RECUADRO] IMAGEN: Orange and green passenger train crossing a high steel bridge over a reddish rock canyon.
    VIDEO: Train moves slowly across the bridge, the camera tracks it sideways.
S09 [RECUADRO] IMAGEN: Large concrete dam wall with a blue reservoir between dry hills, spillway closed.
    VIDEO: Slow drone rise over the dam wall revealing the reservoir.
S10 ⭐ [PRINCIPAL] IMAGEN: Straight top-down view of perfectly straight irrigation canals crossing a vast patchwork of green and gold fields, water shining in the sun.
    VIDEO: Starts straight top-down and rises higher and higher, revealing more identical fields to the horizon.
S11 ⭐ [PRINCIPAL] IMAGEN: Huge cornfield ready for harvest, a combine harvester cutting the rows, golden dust in the low sun.
    VIDEO: Slow drone pass alongside the combine, dust drifting.
S12 [RECUADRO] IMAGEN: Close-up of white corn kernels pouring from a metal chute into a pile, macro detail.
    VIDEO: Slow-motion kernels falling and bouncing.
S13 [FOTO-IA] IMAGEN: Grain silos at sunset next to a rural road in northwestern Mexico, trucks parked, no logos.
S14 [RECUADRO] IMAGEN: Hands from behind placing a stack of corn tortillas wrapped in a cloth on a kitchen table, warm morning light.
    VIDEO: Slow push-in, light steam from the tortillas.
S15 [RECUADRO] IMAGEN: Chickpea field with green plants and pods, a straw hat resting on a bucket in the foreground.
    VIDEO: Gentle breeze moves the plants, slow lateral slide.
S16 ⭐ [PRINCIPAL] IMAGEN: Rows of white greenhouses for tomatoes stretching to the horizon, workers far away from behind with caps.
    VIDEO: Slow drone flight along the greenhouse rows.
S17 [RECUADRO] IMAGEN: Red tomatoes rolling on a packing conveyor into plain unbranded cardboard boxes.
    VIDEO: Tomatoes roll steadily, slight camera push.
S18 [RECUADRO] IMAGEN: Refrigerated truck without logos driving north on a desert highway at sunset.
    VIDEO: Camera tracks the truck from the side, then it drives away.
S19 [RECUADRO] IMAGEN: Diner counter with a burger and fresh tomato slice on a plate, blurred city lights through the window, no brands.
    VIDEO: Slow push-in on the tomato slice.
S20 [RECUADRO] IMAGEN: Line of farm workers from behind walking between furrows at sunrise carrying buckets, long shadows.
    VIDEO: They walk away from the camera slowly, dust in the backlight.
S21 [FOTO-IA] IMAGEN: Bus station at night in southern Mexico, families from behind with bags waiting for a long-distance bus.
S22 ⭐ [PRINCIPAL] IMAGEN: Fleet of shrimp trawlers leaving a harbor at dawn with their nets raised like wings, calm water.
    VIDEO: Slow drone flight following the boats out to sea.
S23 [RECUADRO] IMAGEN: Deck of a shrimp boat, the net opens and hundreds of shiny shrimp spill onto the deck.
    VIDEO: Slow-motion shrimp spilling and sliding.
S24 [RECUADRO] IMAGEN: Plate of green aguachile with shrimp, red onion and cucumber on a wooden table, lime drops falling.
    VIDEO: Slow push-in, lime drops in slow motion.
S25 [RECUADRO] IMAGEN: Golden crispy shrimp tacos with melted cheese coming off a hot griddle.
    VIDEO: Cheese stretches as a taco is lifted slowly.
S26 [RECUADRO] IMAGEN: Large tuna fishing vessel docked at an industrial port at sunset, cranes and seagulls.
    VIDEO: Slow lateral slide along the hull, gulls flying.
S27 [RECUADRO] IMAGEN: Unlabeled tuna cans moving in a line on a factory conveyor, clean industrial light.
    VIDEO: Cans move steadily, slight focus pull.
S28 [RECUADRO] IMAGEN: Pier crowded with families seen from behind waving at boats leaving, confetti in the air, sunset.
    VIDEO: Boats move away, confetti drifts, slow push.
S29 ⭐ [PRINCIPAL] IMAGEN: Empty vintage movie theater in black and white, projector beam with floating dust, red velvet seats turned grey.
    VIDEO: Slow push through the projector beam toward the screen.
S30 [FOTO-IA] IMAGEN: Vintage radio and vinyl records on a wooden table in a 1950s Mexican living room, warm lamp light.
S31 ⭐ [PRINCIPAL] IMAGEN: Sinaloan brass band playing at an outdoor night party: tuba, trumpets, clarinets and a big bass drum, musicians from behind and out of focus, string lights.
    VIDEO: Slow orbit behind the band toward the dancing crowd.
S32 [RECUADRO] IMAGEN: Close-up of a big bass drum being hit, the skin vibrating, warm light.
    VIDEO: Slow-motion hit and vibration.
S33 [RECUADRO] IMAGEN: Wedding dance floor at night, couples from behind, a white dress spinning, band in the background.
    VIDEO: The dress spins in slow motion, lights bokeh.
S34 [RECUADRO] IMAGEN: Packed stadium at night seen from the upper seats, a stage with lights far away, crowd silhouettes.
    VIDEO: Slow push, lights sweep the crowd.
S35 ⭐ [PRINCIPAL] IMAGEN: Night carnival parade on a seafront boulevard with huge glowing floats and fireworks over the ocean.
    VIDEO: Slow drone glide along the parade, fireworks bursting.
S36 ⭐ [PRINCIPAL] IMAGEN: Empty street of a northern Mexican city at night, closed metal shop shutters, a traffic light blinking amber, wet asphalt.
    VIDEO: Slow dolly down the empty street, the light blinks.
S37 [RECUADRO] IMAGEN: Empty classroom with chairs on the desks, morning light through the windows.
    VIDEO: Slow push between the desks.
S38 [RECUADRO] IMAGEN: Small family shop with its metal shutter half closed at dusk, warm light inside.
    VIDEO: The shutter slowly closes to the ground.
S39 [RECUADRO] IMAGEN: Night view from very high of many connected city lights across a continent, glowing lines that shift.
    VIDEO: Slow drift, light lines pulse and move.
S40 [RECUADRO] IMAGEN: Teacher from behind in front of a chalkboard with children from behind, simple bright classroom.
    VIDEO: Slow lateral slide.
S41 ⭐ [PRINCIPAL] IMAGEN: Almost empty reservoir with cracked dry earth at the bottom and a pale line marking where the water used to reach.
    VIDEO: Slow drone rise revealing how empty it is.
S42 [RECUADRO] IMAGEN: Cracked dry soil with a withered corn sprout, wind lifting dust.
    VIDEO: Dust blows across, slow push-in.
S43 [RECUADRO] IMAGEN: Abandoned tomato greenhouses with torn plastic flapping in the wind.
    VIDEO: Plastic flaps, slow lateral slide.
S44 [RECUADRO] IMAGEN: A tractor stopped in an empty field at sunset, dust floating.
    VIDEO: Slow orbit around the still tractor.
S45 ⭐ [PRINCIPAL] IMAGEN: Mexican table with tortillas, tomato salsa, beans and shrimp; the dishes disappear one by one until the table is empty.
    VIDEO: The camera pulls back slowly as the dishes vanish one by one.
S46 ⭐ [PRINCIPAL] IMAGEN: The same coastal city as S01 at golden sunset, lighthouse on the island.
    VIDEO: Drone rises high to reveal the Pacific coast in golden light.
```
