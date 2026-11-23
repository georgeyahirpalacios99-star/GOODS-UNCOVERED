# Biblioteca de plantillas Goods Uncovered (generadas en Flow, lotes 1 y 2)

El motor 3D (`motor-3d/render3d.cjs`) carga solas las texturas T01–T06 en todos los videos. Para no usarlas en una escena, pon `"texturas": false`.

| ID | Uso | Notas |
|---|---|---|
| T01-mar | Mar del mapa 3D y del entorno "mundo vivo" | se repite en mosaico |
| T02-pasto | Pasto de la cancha | girado para que las franjas queden a lo ancho |
| T03-gradas | Anillo del estadio | se repite 6 veces |
| T04-tierra | Países sin bandera (contexto) | oscurecida un 25 % |
| T05-mesa | Mesa de madera (escenas de mapa de papel) | — |
| T06-nubes | Nubes que pasan sobre el mapa | el negro se vuelve transparente; bordes con fundido |
| V01-tinta | Transición de tinta (fondo blanco) | mezclar en modo "multiply" |
| V02-papel-quemado | Transición de papel que se quema | — |
| V03-destello | Destello para cortes rápidos | mezclar en modo "screen" |
| V04 / V04b-polvo | Capa de polvo dorado | casi iguales; mezclar en "screen" |
| V05 / V05b-papelitos | Papelitos en goles | recortar la lámpara de arriba; mezclar en "screen" |
| V06-humo | Humo de bengala (blanco) | se tiñe con el color del país; mezclar en "screen" |
| V07-tierra-espacio | Gancho: zoom desde el espacio a América | — |
| V08-mapa-antiguo | Gancho: mapa antiguo con lámpara | — |
| V09-ciudad-noche | Recurso: ciudad de noche desde el avión | — |
| V10-gente | Recurso: multitud en la calle | se lee "FARMACIA" en una esquina: usar recortado |
| V11-billetes | Recurso: economía | — |
| V12-puerto | Recurso: comercio | — |
| V13-cosecha | Recurso: campo | — |
| V14-aula | Recurso: educación y temas serios | — |
| V15-atardecer | Cierre | — |
