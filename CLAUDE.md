# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Summary

**DAStudio Portfolio** es un sitio web de portafolio para un desarrollador web enfocado en software a medida, sistemas B2B, plataformas de e-commerce, aplicaciones de utilidad médica y sitios corporativos.

- **Repositorio GitHub**: [https://github.com/dastudio-dev/portfolio](https://github.com/dastudio-dev/portfolio)
- **Producción (Hostinger)**: [https://dastudio.com.ar](https://dastudio.com.ar) — deploy automático desde `main` en cada push (dominio sin `www`; el `www` redirige).

---

## Commands

### Servidor Local de Previsualización
```bash
python3 -m http.server 8080 --directory /home/diego/Soft/repos/portfolio
```

### Git & Deploy
El remoto `origin` debe ser `https://github.com/dastudio-dev/portfolio.git` (el nombre viejo `diegoastein/portfolio` solo redirige). Verificar con `git remote -v` antes de pushear.
```bash
git add .
git commit -m "Descripción del cambio"
git push origin main
```

---

## Reglas de Diseño & Guías del Proyecto

### 1. Estética Dinámica & Humana (Sin Neón)
- **Dinamismo con criterio** (rediseño 2026-11): el sitio debe sentirse moderno y ágil: tipografía grande, aparición al hacer scroll, carril de capturas en movimiento y pasos del proceso que se activan al scrollear. Todo con CSS/JS propio, respetando `prefers-reduced-motion`.
- **Estructura** (v2): hero tipográfico con carril de capturas reales; **"Cómo trabajamos" va antes que los proyectos** y prevalece sobre ellos; los trabajos se muestran como lista + panel en la misma página. No mostrar cantidad de proyectos ni cifras de relleno; no usar modales para los casos.
- **Cero Efectos Neón / IA**: No utilizar fondos fluorescentes, luces radiales borrosas, gradientes en texto, grillas decorativas ni patrones sobrecargados estilo plantilla genérica de IA.
- **Paleta de Colores**: Fondo neutro Slate-950 (`#0d1117`), tarjetas (`#161b22`), bordes definidos (`#30363d`) y acentos sólidos en azul cielo (`#38bdf8`) y azul primario (`#2563eb`).
- **Tipografía**: *Plus Jakarta Sans* para títulos y cuerpo; *JetBrains Mono* para badges y código.

### 2. Capturas Reales (Cero Mockups Ficticios)
- **Imágenes Reales**: Se deben utilizar únicamente capturas de pantalla reales de las webs en producción guardadas en la carpeta `img/`.
- **Prohibición de Mockups**: No utilizar maquetados gráficos dibujaos o ilustrados.

### 3. Ocultamiento de Dominios
- **Cero URLs Expuestas por Defecto**: No mostrar nombres de dominio (`.web.app`, `.com.ar`, `.pro`) en las barras superiores de los marcos de escritorio o celulares, salvo las excepciones explícitas listadas abajo.
- **Titulares Descriptivos**: Utilizar etiquetas funcionales limpias (ej. `🔒 Panel de Gestión de Flota`, `🛒 Tienda Online & Catálogo`, `📱 App Clínica Offline`, `📈 Monitor de Simulación`).
- **Excepciones permitidas** (proyectos de acceso público donde el cliente autorizó mostrar el dominio):
  - `herramientaslibres.web.app` — E-Commerce & Venta de Herramientas (acceso libre).
  - `www.jlsrl.com.ar` — Landing Page JL Constructora SRL.

### 4. Marca Neutra
- Mantener la marca neutra `DAStudio / Desarrollo Web & Software a Medida`. No personalizar con nombres propios individuales.

### 5. Galerías Interactivas
- Cada proyecto se muestra en el panel de "Proyectos" (`#workPanel`): captura principal, miniaturas para cambiar de captura y problema/solución visibles sin abrir nada.
- Al hacer clic en la captura principal se amplía en el lightbox (solo imagen). No hay modal de caso de estudio.
- Los datos de cada proyecto viven en `script.js` (objeto `projects`).

---

## 6. Herramientas Internas (no se publican)

La carpeta `herramientas/` guarda utilidades de trabajo que **no son parte del sitio**. Lleva un `.htaccess` que bloquea su acceso, porque el deploy copia el repositorio completo: todo lo que entra a `main` queda publicado en dastudio.com.ar. Nunca versionar ahí datos de clientes ni de prospectos.

- `herramientas/panel-prospeccion/`: generador del panel de la campaña de contacto en frío. `plantilla.html` es la página sin datos y `generar.py` la completa leyendo la pestaña `Prospectos` de la planilla de seguimiento. El HTML con datos no se versiona: se publica como artefacto privado. Instrucciones y enlaces en su `README.md`.

---

## Qué vive fuera de este repositorio

La captación de clientes no está en el código; no buscarla acá:

- **Prospectos y su estado**: la planilla "Seguimiento DAStudio" en Drive, pestaña `Prospectos`. Es la fuente de verdad del estado de cada empresa (contactada, respondió, sin forma de contacto) y de los mensajes que se le mandan a cada una.
- **Agenda diaria de contactos**: una routine en la nube, "DAStudio - Prospección diaria", que corre a las 9:05 de lunes a viernes: completa los mensajes y los links de contacto en la planilla y le manda a Diego el lote del día por mail. No contacta a nadie: el envío lo hace Diego.
- **Reels y su programación**: los skills `portfolio-reel`, `portfolio-externos` y `portfolio-schedule`.
