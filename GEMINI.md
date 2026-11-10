# GEMINI.md

Este archivo contiene las directrices de comportamiento y reglas técnicas para **Gemini AI Assistant** al trabajar en el proyecto **Portfolio**.

---

## 🌐 Información del Proyecto

- **Nombre del Proyecto**: DAStudio Portfolio
- **Propósito**: Portafolio profesional de soluciones web, sistemas B2B, e-commerce y aplicaciones médicas.
- **Repositorio GitHub**: [https://github.com/dastudio-dev/portfolio](https://github.com/dastudio-dev/portfolio)
- **Producción (Hostinger)**: [https://dastudio.com.ar](https://dastudio.com.ar) — deploy automático desde `main` en cada push (dominio sin `www`; el `www` redirige).

---

## 📜 Reglas de Comportamiento & Idioma

### 1. Idioma de Comunicación
- **Preferencia**: Responder y comunicarse **siempre en español** en todas las explicaciones, comentarios de código e interacciones.

### 2. Estética & Diseño
- **Diseño Sobrio y Profesional**: Mantener una línea visual limpia (estilo GitHub/Vercel) libre de efectos neón, luces borrosas artificiales o cliqués de IA.
- **Marca Neutra**: Utilizar la marca `DAStudio` sin incluir nombres de personas individuales.

### 3. Capturas Reales & Galerías
- **Usar Capturas Reales**: Usar únicamente imágenes de capturas de pantalla de aplicaciones reales en producción localizadas en `img/`.
- **Galerías Interactivas**: Mantener las capturas presentadas en carruseles deslizantes con contador de imágenes.

### 4. Ocultamiento de Dominios
- **Sin URLs Expuestas**: No incluir nombres de dominio ni URLs explícitas en los encabezados de las tarjetas o maquetas. Usar nombres funcionales.

---

## 🛠️ Comandos Frecuentes

```bash
# Previsualización local
python3 -m http.server 8080

# Guardar y publicar cambios en GitHub
git add .
git commit -m "Actualización del proyecto"
git push origin main
```
