# Goods Uncovered — convenciones de producción

Canal de YouTube de George Palacios. Responder en español latino, directo, con datos concretos; si pide una decisión, dar una sola recomendación.

## Presentador
- **Jonas**: personaje IA (pelo castaño ondulado, ojos verdes, barba corta, camisa de lino verde olivo). Serio, calmado, varonil. Ver `analisis/PERSONAJE-BIBLIA.md` y `videos/002-arca-de-noe/04-JONAS-SET.md`.

## Entregables por parte de guion
Cuando George envía el texto de una parte, entregar:
1. Mapa de cortes (un cambio visual cada 2-4 s) con efecto de sonido sugerido.
2. Prompts de imagen realistas + prompt de animación para Flow (copiar y pegar).
3. Motion graphics renderizados con ffmpeg (fondo #0f0d0a con viñeta, ámbar #E8A33D, rojo #D7263D solo para tachado/clasificado, títulos en Liberation Serif Bold).
4. Material real con licencia libre (Ken Burns, etiqueta de fuente) y su crédito.
6. Todo en un solo zip `PARTE-XX-COMPLETA.zip` con la guía PDF (sin pre-montaje: a George no le sirvió). Máximo ~6 imágenes IA por parte; los prompts también van en el chat, listos para copiar.
5. **Todo texto en pantalla también como PNG transparente 1920x1080** (títulos, citas bíblicas, cifras, etiquetas) para ponerlo como capa en CapCut. Usar `tools/png_title.sh` para títulos con cita y `tools/png_label.sh` para cifras y etiquetas.

## Reglas
- Marcar "AI RECREATION" en tomas IA de hechos históricos; nunca presentar Durupınar como "el arca encontrada".
- Sin sangre ni violencia gráfica (apto para anunciantes).
- Binarios (mp4, mov, jpg) no van al repo; se entregan con SendUserFile.
