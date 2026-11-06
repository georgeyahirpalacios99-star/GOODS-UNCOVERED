# Reel 001 · "Goliat no medía lo que crees" — capas para Google Flow
**Estilo:** collage cinematográfico realista (papel rasgado + recortes tipo sticker + profundidad), como el video de referencia de *Vive de lo tuyo*.
**Formato:** Facebook Reels 9:16 · ~45 s · subtítulos quemados (en Facebook casi todos ven sin sonido).

---

## 0. Cómo funciona (tú → yo)
1. En **Flow** genera cada capa de la lista (sección 2). Usa **Nano Banana** (o Imagen) y **2 versiones por prompt**; quédate con la mejor.
2. **Personajes y objetos:** sobre **fondo verde puro**. Yo quito el verde y los recorto con borde blanco tipo sticker.
   **Fondos:** sin personas, para poder poner los personajes encima.
3. **Mismo David y mismo Goliat en todas las tomas:** genera primero **P1 (Goliat)** y **P2 (David)**. Después, en cada prompt donde aparezcan, súbelos como **imagen de referencia ("ingrediente")**.
4. Mándame las imágenes con su nombre (F1, P1, O1…) por aquí o por Google Drive, más la voz de ElevenLabs (sección 4).
5. Yo armo la animación con código:
   - movimiento de cámara en profundidad;
   - papel que se rasga para pasar de escena;
   - recortes con borde blanco, cinta adhesiva, círculos y líneas punteadas;
   - polvo, destellos de luz y grano de película;
   - contadores (2,9 m · 57 kg) y subtítulos palabra por palabra, más sonido y música.

**Todo lo gráfico extra (papel rasgado, cinta, polvo, textos) lo hago yo en código: no lo generes.**

---

## 1. BLOQUE DE ESTILO (pégalo al final de CADA prompt)
```
Ultra-realistic cinematic photograph, ancient Israel around 1000 BC, the Valley of Elah, warm golden-hour sunlight with soft atmospheric haze, shot on 35mm film, shallow depth of field, rich earthy palette of ochre, olive green, bronze and deep blue sky, historically accurate Iron Age clothing and bronze armor, natural skin texture, dramatic but believable lighting. No text, no letters, no watermark, no logos, no modern objects, no extra fingers, no deformed hands or faces.
```

**Añade esto solo a los personajes y objetos (P y O):**
```
Isolated subject on a solid pure chroma green background (#00FF00), evenly lit, no shadow on the background, full subject visible and not cropped, sharp clean edges, generous margin around the subject.
```

**Añade esto solo a los fondos (F):**
```
Empty background plate with no people, wide composition, the lower third clear so characters can be placed on top, vertical 9:16.
```

---

## 2. CAPAS (18 imágenes · ⭐ = imprescindibles)

### Fondos (9:16)
| ID | Prompt |
|---|---|
| ⭐ F1 | `The Valley of Elah seen from a low angle: two rocky hills facing each other across a dry valley with a small stream, distant tents and banners of two ancient armies on each hilltop, dust in the air, dramatic sky.` |
| ⭐ F2 | `A clear shallow brook running over smooth round stones in a dry valley, close to the water, morning light reflecting on the water, reeds and dry grass.` |
| F3 | `The center of the battlefield after a fall: a cloud of golden dust rising from the ground, scattered bronze fragments and footprints, dramatic backlight.` |
| F4 | `Interior of an ancient scribe's room: wooden table, clay jars, oil lamp glowing, old parchment scrolls, warm dim light.` |
| ⭐ F5 | `Sunset over the Valley of Elah, a lone young shepherd seen from behind standing on a hill with a sling in his hand, epic golden sky, long shadows.` (este sí lleva persona) |

### Personajes (1:1, fondo verde)
| ID | Prompt |
|---|---|
| ⭐ P1 Goliat | `A towering Philistine warrior, about 2.9 meters tall, massive muscular build, full body, wearing a bronze helmet, a heavy coat of bronze scale armor, bronze greaves on his legs, a bronze javelin on his back and a huge spear in his hand, intimidating expression, seen from a slightly low angle.` |
| ⭐ P2 David | `A young Israelite shepherd boy of about 16, slim, curly dark hair, simple wool tunic with a leather belt and a shepherd's bag, sandals, holding a leather sling, full body, calm and confident expression.` |
| P3 | `The same young shepherd (use reference P2) kneeling by a stream, picking a smooth round stone from the water, full body, side view.` |
| P4 | `The same young shepherd (use reference P2) wearing oversized royal bronze armor and a helmet that is far too big for him, struggling to walk, awkward funny expression, full body.` |
| ⭐ P5 | `The same young shepherd (use reference P2) spinning a sling above his head at full speed, dynamic action pose, dust kicking up, full body, three-quarter view.` |
| ⭐ P6 | `The giant warrior (use reference P1) falling forward face down, mid-fall, helmet slipping, spear dropping from his hand, dramatic action, full body.` |
| P7 | `A group of five ancient Benjamite slingers, left-handed, in Iron Age tunics, all aiming slings in the same direction, full bodies, disciplined army look.` |

### Objetos (1:1, fondo verde)
| ID | Prompt |
|---|---|
| ⭐ O1 | `A fragment of an ancient Dead Sea Scroll, torn brown parchment with faded Hebrew handwriting, close-up, museum lighting.` (aquí sí se permiten letras hebreas antiguas) |
| ⭐ O2 | `A heavy ancient bronze scale armor coat displayed upright, hundreds of overlapping bronze scales, worn and polished, studio product shot.` |
| O3 | `A massive ancient spear head made of dark iron, rough forged texture, attached to a thick wooden shaft, close-up product shot.` |
| ⭐ O4 | `Five smooth round river stones held in the open palm of a young hand, wet, close-up.` |
| O5 | `An ancient leather sling with braided cords and a stone pouch, laid flat, studio product shot.` |
| ⭐ O6 | `A single smooth river stone flying through the air with a slight motion blur, sharp center, close-up.` |
| O7 | `A bronze helmet of a giant warrior lying in the dust, dented, close-up product shot.` |

---

## 3. Toma por toma (cómo las voy a animar)
| Tiempo | Capas | Animación |
|---|---|---|
| 0–3 s | F1 + P1 + P2 | **Gancho:** cámara que sube por Goliat hasta su casco; David diminuto delante; contador **2,9 m** con golpe grave |
| 3–9 s | F4 → O1 | El papel se rasga y aparece el rollo antiguo; tarjetas "**6 codos y un palmo = 2,9 m**" contra "**4 codos y un palmo = 2,0 m**" |
| 9–15 s | O2, O3 | Armadura y lanza en recortes tipo sticker; contadores **57 kg** y **6,8 kg** |
| 15–19 s | P4 | David con la armadura gigante, sacudida cómica |
| 19–24 s | F2 + P3 + O4 | Zoom al arroyo; las 5 piedras aparecen una por una (1 · 2 · 3 · 4 · 5) |
| 24–31 s | P7 | Rasgado de papel; "**700 zurdos que no fallaban**" (Jueces 20:16) |
| 31–37 s | P5 → O6 | La honda gira con estela; la piedra vuela en cámara lenta con línea punteada hacia Goliat |
| 37–41 s | P6 + F3 + O7 | Impacto: destello, polvo, el casco rodando |
| 41–45 s | F5 | Atardecer + pregunta final |

---

## 4. VOZ (ElevenLabs · tono de narrador cálido · Speed 1.0)
```
Goliat medía casi tres metros… <break time="0.3s" /> o eso dice tu Biblia. <break time="0.3s" /> Porque los manuscritos más antiguos dicen otra cosa. <break time="0.5s" />
El texto que usamos hoy dice seis codos y un palmo: <break time="0.2s" /> unos dos metros noventa. <break time="0.3s" /> Pero los Rollos del Mar Muerto y la traducción griega dicen cuatro codos y un palmo: <break time="0.2s" /> unos dos metros. <break time="0.5s" />
Igual era un gigante. <break time="0.2s" /> Su armadura pesaba cinco mil siclos de bronce: <break time="0.2s" /> unos cincuenta y siete kilos. <break time="0.3s" /> Y solo la punta de su lanza, <break time="0.15s" /> casi siete kilos de hierro. <break time="0.5s" />
A David le pusieron la armadura del rey… <break time="0.2s" /> y no podía ni caminar. <break time="0.4s" />
Así que bajó al arroyo y eligió cinco piedras lisas. <break time="0.5s" />
Y esto casi nadie lo cuenta: <break time="0.2s" /> la honda no era un juguete. <break time="0.2s" /> La Biblia habla de setecientos zurdos que lanzaban una piedra a un cabello… <break time="0.2s" /> y no fallaban. <break time="0.5s" />
Goliat tenía casco de bronce. <break time="0.2s" /> Pero la piedra entró justo en su frente. <break time="0.4s" />
Una sola piedra. <break time="0.5s" />
¿Qué historia de la Biblia quieres que contemos después?
```

## 5. Datos y fuentes (para la descripción)
- Altura: 1 Samuel 17:4 → "seis codos y un palmo" (texto masorético, unos 2,9 m). Los Rollos del Mar Muerto (4QSamᵃ), Flavio Josefo y la Septuaginta dicen "cuatro codos y un palmo" (unos 2 m). Codo ≈ 45 cm, palmo ≈ 22 cm.
- Armadura: 1 Samuel 17:5 → 5.000 siclos de bronce (siclo ≈ 11,4 g → unos 57 kg).
- Lanza: 1 Samuel 17:7 → punta de 600 siclos de hierro (unos 6,8 kg).
- La armadura de Saúl: 1 Samuel 17:38-39. Las cinco piedras: 1 Samuel 17:40. La piedra en la frente: 1 Samuel 17:49.
- Los 700 honderos zurdos de Benjamín: Jueces 20:16.

## 6. Reglas de Facebook que cuidan el alcance
- **No pidas "escribe Amén" ni "comparte si crees".** Facebook le baja el alcance a eso porque lo cuenta como "cebo de interacción". Cierra con una pregunta real, como en el guion.
- Si alguna imagen parece una foto real de un hecho histórico, márcala con la etiqueta de IA de Facebook ("Información de IA").
- Pon los versículos en la descripción: dan confianza y evitan discusiones en los comentarios.
