# Panel de prospección

Pantalla de trabajo diaria para la campaña de contacto en frío: las empresas
por contactar con su mensaje, el link de WhatsApp ya armado y un botón para
registrar cada envío. Se usa desde el celular.

- **Publicado como artefacto privado:** https://claude.ai/artifact/5DVnKJqPFxCR1x1x8hS72H
- **Fuente de verdad de los datos:** pestaña `Prospectos` de la planilla
  "Seguimiento DAStudio" (spreadsheetId `1gVPX4a6_JNTxjIddkV7At9c1guGz1kzZdMDa97Lt4-c`).
- **Dónde quedan los registros:** en la base de datos del propio artefacto,
  colección `registros`, un documento por fila de la planilla con id `f<fila>`.

## Por qué el panel no está en este repositorio con sus datos

Este repo se publica solo en dastudio.com.ar en cada push a `main`. El panel
lleva adentro la lista de prospectos, sus teléfonos y los mensajes de venta,
así que el HTML con datos no se versiona: acá vive la herramienta
(`plantilla.html` + `generar.py`) y el HTML final se arma cuando se necesita.
La carpeta `herramientas/` además tiene un `.htaccess` que la bloquea, por si
el deploy la copiara al servidor.

## Regenerar el panel

1. Leer la pestaña Prospectos **desde la fila 2**, rango `A2:T<última>`, con el
   conector de Google Sheets, y guardar la respuesta tal cual en un `.json`.
   El rango tiene que arrancar en A2: empezar más abajo deja empresas afuera
   sin avisar (ya pasó: se perdieron dos contactadas que estaban en las filas 2 y 3).
2. Generar el HTML:

   ```bash
   python3 generar.py prospectos.json /ruta/al/panel.html
   ```

   El script avisa si alguna empresa por contactar quedó sin mensaje en la
   columna O, sin versión en la columna T o sin ningún canal de contacto.
3. Publicar ese HTML como **nueva versión del mismo artefacto**, con la URL de
   arriba, para no perder los registros ya marcados ni cambiar el link.
   Las capacidades (`db` y `user`) se arrastran solas al republicar.

Hace falta regenerar cada vez que se cargan empresas nuevas en la planilla o
se reescriben los mensajes: la lista va embebida en el HTML. Los registros que
Diego haya marcado sobreviven, porque viven en la base y no en la página.

## Cómo se lee la planilla

`generar.py` toma de cada fila: empresa (A), ciudad (C), canal (E), el WhatsApp,
email e Instagram que saca de la columna F con expresiones regulares, la
personalización (H), la fecha del primer mensaje (I), el estado (L), la próxima
acción (M), el mensaje (O) y la versión del test A/B (T).

Reparte las filas por la columna L: `Por contactar` van a la lista de contacto,
`Contactado` a la de seguimientos (sin el mensaje, porque lo que les falta es el
segundo toque) y `Falta contacto` a la lista del final.

## Del panel a la planilla

El panel **no escribe en Google Sheets**. Lo que se marca ahí queda en la base
del artefacto; pasarlo a las columnas I, L y M de la planilla es un paso
manual que hace Claude leyendo la colección `registros` con la herramienta
ArtifactData.
