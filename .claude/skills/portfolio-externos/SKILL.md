---
name: portfolio-externos
description: Revisa periódicamente la carpeta Drive "reels dastudio/Externos" (reels hechos fuera del skill de video, p. ej. en Ootto), mantiene el registro de qué se publicó, cuántas veces y qué queda, renombra mp4/captions y prepara la programación con portfolio-schedule. Usar cuando se pida revisar Externos, el registro de externos, o en la tarea periódica.
---

# Portfolio externos

Carpeta: `/mnt/diegosteinberg_google_drive_1790645175/1-Trabajo/reels dastudio/Externos/<slug>/`
con `<slug>.mp4` + `caption.txt`. Registro: `Externos/registro.json` (se identifica cada reel por el
sha1 del mp4, así los renombres no lo rompen). Los reels externos entran al mismo cupo de 20 posts/mes
de Metricool que el resto (ver `portfolio-schedule`).

## Manejo de Drive (regla de Diego, 2026-11-06)
Claude se encarga de todo lo de Drive para los reels externos: crear la carpeta `Externos/<slug>/`,
bajar el mp4 desde Ootto (`media_url` de `workspace_render`/`reel_status`, firmada y con vencimiento: bajarla
apenas se entrega), nombrar mp4 y `caption.txt`, y mantener el registro. Diego ya no sube nada a mano
(el primer reel, `sistema-sin-internet`, lo subió él). Solo hace falta su OK para programar/publicar y
para borrar archivos.

## Cada corrida
1. `python3 -I .claude/skills/portfolio-externos/scan.py` (detecta reels nuevos, captions vacíos/ausentes,
   mp4 que desaparecieron; actualiza el registro).
2. **Reel nuevo** (`estado: nuevo`): sacar fotogramas con ffmpeg (`fps=1/3`, tile) y mirarlos; elegir un
   `slug` corto descriptivo; renombrar carpeta, mp4 (`<slug>.mp4`) y caption (`caption.txt`; si viene en
   .docx/.txt con otro nombre, renombrar o convertir). Nunca reescribir el contenido del caption.
   Si falta el caption, redactar una propuesta y dejarla en `notas` del registro, no en `caption.txt`.
3. **Revisar contra las reglas** del CLAUDE.md (marca neutra, sin dominios de clientes salvo las excepciones,
   sin mockups) y anotar en `notas`; estado `revisado`.
4. **Publicaciones**: con `getScheduledPosts` de Metricool, buscar posts cuyo texto coincida con el caption
   de cada reel; actualizar `publicaciones` (fecha, id) y `veces_publicado` (solo posts ya publicados;
   los agendados cuentan como `programado`). Estados: nuevo → revisado → aprobado → programado → publicado.
5. **Informe** breve a Diego: nuevos, problemas, por publicar, cupo libre del mes (20 − programados).

## Qué NO hace sola la tarea periódica
- No programa ni publica nada, ni sube archivos a GitHub: eso requiere el OK de Diego (regla de
  `portfolio-schedule`). Propone fecha/orden y espera.
- No borra nada de Drive. Solo renombra lo de `Externos/`.
- Diego aprueba un reel diciéndolo en el chat; recién ahí `estado: aprobado`.

## Datos verificados
- 2026-11-06: Diego confirmó que la publicación automática de Metricool funciona.
