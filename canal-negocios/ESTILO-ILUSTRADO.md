# Estilo ilustrado (palitos con cabeza redonda) · La Letra Chica

Es el estilo de tus capturas: cada escena es **una imagen de IA** con fondo detallado. Se anima con zoom lento, se cambia de imagen cada 4 a 6 s y lleva subtítulos. Ejemplo: "¿Qué hacían los primeros humanos por la noche?" (Zenn), con 8 M de vistas en 6 meses.

Lo mezclamos con lo que ya hace mi motor: etiquetas de precio, barras de "a dónde va tu dinero", contadores y la caja registradora encima de la imagen. Eso no lo tiene ningún canal de este estilo.

## 1. Bloque de estilo (va al inicio de TODOS los prompts, en inglés)
```
Hand-drawn cartoon storybook illustration, warm muted colors, clean black ink outlines, flat shading, detailed background, YouTube explainer style, 16:9. Characters are stickmen with a big perfectly round white head, small black oval eyes, expressive eyebrows and mouth, thin black stick arms and legs, simple clothes. No logos, no text unless specified.
```

## 2. Personaje fijo (para que siempre sea el mismo)
```
Main character "Beto": stickman with a big round white head, short messy black hair, simple blue t-shirt and gray pants.
```
El dueño de cada empresa siempre es el mismo personaje:
```
"El Jefe": stickman with a big round white head, small black top hat, dark blue suit and a red tie.
```

## 3. Prompts del demo (tienda de todo a $1.25), uno por frase
| # | Seg. | Prompt (después del bloque de estilo) |
|---|---|---|
| 1 | 0-4 | Interior of a cheap discount store, long shelves packed with colorful cheap products (mugs, rubber ducks, batteries, candy jars, cleaning bottles), a red sign hanging from the ceiling that says 'TODO A $1.25'. Beto in the center, surprised, holding a red mug with a yellow price tag. |
| 2 | 4-7 | Same store. Beto scratching his head, confused, question marks above him; behind the counter a smiling cashier stickman with a green apron next to a cash register. |
| 3 | 7-13 | Aerial view of a small American town drawn like a cartoon map, dozens of identical small discount stores with green signs on every street corner. |
| 4 | 13-17 | El Jefe standing proudly on top of a huge mountain of dollar bills and coins inside a giant warehouse full of boxes. |
| 5 | 17-20 | A factory with a conveyor belt making thousands of identical red mugs, stickman workers packing them into boxes. |
| 6 | 20-24 | A huge cargo ship full of colorful containers arriving at a port, and a truck loading boxes toward a discount store. |
| 7 | 24-27 | Small back office of the store: El Jefe at a wooden desk counting a small pile of coins, a calendar and bills pinned to the wall, slightly worried face. |
| 8 | 27-31 | El Jefe laughing while golden coins rain from the sky over the town full of discount stores. |
| 9 | 31-35 | Beto facing the viewer, smiling, holding the red mug, pointing at the viewer, discount store behind him. |

Las cifras (9,200 tiendas; $19,400 M; 80¢ / 45¢; $7,050 M) **no van en la imagen**: las pongo yo encima para que no salgan con errores de la IA.

## 4. Cuántas imágenes y cuánto cuesta
- Un video de 10 min lleva entre 100 y 120 imágenes (una cada 5 s).
- En Higgsfield (plan gratis) solo funciona el modelo barato `z_image`: 0.15 créditos por imagen. Con tus 10 créditos salen unas 60, así que no alcanza para un video.
- Más barato para producir en serie: Google (Gemini / Imagen) con una clave de API. Cuesta centavos por imagen y yo genero todas las imágenes de un tirón con `herramientas/generar_imagenes.py`.
