---
name: portfolio-reel
description: Build an Instagram Reel (HyperFrames, vertical 1080x1920, ~25 s, with music) for a DAStudio portfolio project from real screenshots, following this repo's branding rules. Use when asked to make, generate, or resume a reel/video for a project in proyectos/.
---

# Portfolio reel (DAStudio / HyperFrames)

How this repo turns a project into a 1080x1920 HyperFrames video for Instagram, end to
end: intake, getting real screenshots (including from a panel behind login), scrubbing
them for privacy/brand, the house visual template that Diego approved, environment
quirks of this machine, and delivery of a render that is deliberately not committed.

Approved references (look at them before inventing anything): `proyectos/calidad-carrillo`
(v3) and `proyectos/flota-firebase` (v1). Diego liked both: "es dinámico y entretenido".
Read `/hyperframes` first for anything HyperFrames-specific this file doesn't cover.

## 0. The message (get this wrong and the reel is rejected)

The reel's focus is **what DAStudio can develop** (software a medida, of very different
kinds). It is NOT "this product has N modules / N types of software" — Diego rejected a
version that said "8 tipos de software" for that reason.

- **Present the project by its real systems**, named the way Diego names them. Ask for
  the names; don't invent them. Examples: calidad-carrillo = "Reporte de Eventos Adversos"
  + "Gestión de Calidad de Atención"; flota-firebase = "Gestión de Flota" + "Gestión de
  Proyectos de Obras Viales y de Arquitectura".
- Hook says "Software a medida" + "Este caso, para <tipo de cliente>:" + the two system
  cards. The outro carries the diversity idea: "Hoy, <el cliente>. Mañana, tu herramienta."
  + chips of what DAStudio builds (sistemas de gestión, e-commerce, apps clínicas, sitios
  corporativos — from `CLAUDE.md`'s project summary) + the brand.
- Brand stays neutral (`DAStudio / Desarrollo Web & Software a Medida`).

## 1. Intake — always ask before building

Ask (see `memory/feedback_hyperframes_intake.md`, which also governs this):

1. **Proyecto** (slug in `proyectos/`) and **la web** (URL deployed).
2. **El repositorio** (context; `gh api repos/<owner>/<repo>/contents/CLAUDE.md -H
   "Accept: application/vnd.github.raw"` reads private repos with the user's `gh`).
3. **Duración** — default offered: 25 s. Never assume.
4. **Audio** — "música dinámica" is the approved default.
5. **Foco / sistemas** — which 1–2 systems to present and their names (§0).
6. If it's behind a login: which browser is logged in (§2).

A **caption for the post is not optional** — always write `renders/caption.txt` and deliver
it with the video (§7).

## 2. Getting real screenshots

Per `CLAUDE.md`: **no invented mockups, ever** — only real screenshots of production.

- **Public site**: `npx hyperframes capture <url> --json` (scroll-stitched, clean).
- **Behind a login, Chrome logged in by Diego** (tools `mcp__claude-in-chrome__*`, deferred:
  load them in ONE `ToolSearch select:` call — `tabs_context_mcp`, `navigate`, `computer`,
  `javascript_tool`, `find`, `browser_batch`, `tabs_close_mcp`). The built-in browser pane
  is isolated and NOT logged in; use Chrome. Recipe that worked (flota-firebase):
  1. `list_connected_browsers`, then `tabs_context_mcp{createIfEmpty:true}` and
     `navigate` to the app. Wait ~3 s (SPA splash).
  2. Get the route list cheaply instead of clicking menus:
     `javascript_tool`: `[...document.querySelectorAll('a[href^="#/"]')].map(a=>a.textContent.trim()+' -> '+a.getAttribute('href'))`.
  3. Viewport is fixed (~1368x647) and `resize_window` doesn't change it. For crisp text set
     `document.body.style.zoom='1.3'`–`'1.45'` (zoom persists across hash navigation;
     re-apply after full loads) and capture 2–3 scroll positions per screen.
     **Scroll AFTER the zoom reflow**, and use real wheel scroll (`computer scroll`).
  4. Every screenshot is already saved as a full-size JPEG under
     `~/.claude/projects/<proj>/<session>/tool-results/mcp-claude-in-chrome-blob-*.jpg`
     (the path is printed under the image). Copy the good ones to the scratchpad `raw/`
     (NEVER into the repo: they contain real data until scrubbed, §3).
  5. Keep `browser_batch` calls to ≤5–6 actions: a long batch dropped the connection and
     lost its screenshots. Tools needing a `ref` can't be chained with the `find` that
     produces it; use coordinates or a JS `click()` (`find` text must be exact).
  6. When done: `document.body.style.zoom=''` and `tabs_close_mcp` the tab you opened.
- **No browser tool connected** (plain CLI over SSH): ask the person to take screenshots
  and send them (same machine → local path and `Read`; remote → Google Drive MCP
  `search_files` + `download_file_content`; big `content` results land in a `.txt` JSON,
  `base64 -d` it with a shell one-liner).

**Choose screens that don't need heavy redaction.** Production data has real people and
money. Prefer: dashboards with counters, machine/equipment lists (names like "Excavadora
320", not plates), alert lists (rows for machines in hours), obra detail tabs (Fases,
Materiales y Servicios, Resultados). Skip: operator lists, caja, facturación, registros
tables with operator names. Pick obras with non-personal names (e.g. "Ruta Provincial N°96").

## 3. Scrub before using as an asset

Originals stay in the scratchpad. Only scrubbed PNGs go to `proyectos/<slug>/assets/screens/`.
Template: `templates/scrub_template.py` (edit `JOBS`, run with `python3 -I`).

- **Crop browser chrome** (tabs, address bar) if present — keep only page content. Sample a
  pixel column with PIL to find where the app's own header starts; don't guess.
- **Personal identifiers on a flat background** (an email, a person's name): sample the
  adjacent bg color (`im.load()[x, y]`) and draw a filled rectangle of that color.
- **Numbers, plates, costs on busy backgrounds, and anything you can't paint over**:
  pixelate the box (`resize` down by ~14 with BILINEAR, then up with NEAREST) — it is
  unreadable and reads as an intentional privacy blur. Default policy for client
  production data: **pixelate money amounts (importes, costos, totales), license plates
  and personal names**; keep structure (labels, charts, percentages, counters). Diego
  confirmed "dejar pixelados". Don't reveal real amounts unless he says so.
- **Check every output by eye** (build a contact sheet with PIL and `Read` it). Boxes sized
  too large cut real names ("VOLVO (S…"); too small leave a plate legible. Re-run with
  adjusted boxes.
- No ImageMagick; Pillow is available.

## 4. House visual template (per `CLAUDE.md`)

- **Palette**: `--ground:#0d1117` `--surface:#161b22` `--border:#30363d`
  `--brand:#38bdf8` `--accent:#2563eb`. No neon, no radial glows, no AI-template clichés.
  Dim text on dark must stay ≥ ~#8b949e (contrast check fails below ~3:1).
- **Fonts**: *Plus Jakarta Sans* (copy `assets/fonts/*.ttf` + `assets/dastudio-mark.png`
  from an existing reel project; the `@font-face` block lives in that project's
  `index.html`) + *JetBrains Mono* (bundled, resolves by name).
- **No exposed domains, ever** (exceptions in `CLAUDE.md`). With full-width page-content
  captures there is no URL bar, so nothing to hide; don't screenshot the tab strip. The
  client's own logo inside the app header (e.g. JL) is fine.
- **Brand mark**: `assets/dastudio-mark.png` for the end card (don't redraw it).
- **Vertical safe zones** (`/hyperframes` `types/vertical.md`): nothing in the top 168 px;
  text and the product inside 168–1330 px. The approved template lets the chips sit just
  below the band (~1250–1310) and uses only decoration (ghost numeral) under that. Keep
  new text out of the bottom ~400 px.

## 5. Project structure and the approved mechanic

Scaffold: `npx --yes hyperframes@0.9.8 init <slug> --resolution portrait --tailwind
--skip-skills` inside `proyectos/`, then `mkdir -p assets/screens assets/fonts` and copy
`assets/fonts/*`, `assets/dastudio-mark.png` and the music from a previous reel project.

**Generate everything from one script**: `templates/gen_reel.py` (copy it to the scratchpad,
read its header docstring). It writes `compositions/*.html` and `index.html`, so a content
change is an edit + re-run, not hand-editing near-duplicate HTML.

Timeline (25 s at 120 BPM; every start/duration is a multiple of 0.5 s, i.e. on the beat):

| Block | Time | What |
| --- | --- | --- |
| hero | 0–2.5 | "Software *a medida*" + "Este caso, para …:" + two system cards that light up on beats (0.7 s and 1.3 s). Frame 0 is already fully visible (no blur/opacity-0 on text). Ghost `</>` fills the lower area. |
| feature × 5–6 | 2.5–19.5 | 2.5–3 s each. See below. |
| outro | 19.5–25 | Phrase "Hoy, X. / Mañana, tu herramienta." + chips of what DAStudio builds (0–2.2 s), blur-swap to DAStudio mark + tagline + CTA, hold ≥ 2.5 s. |

**Feature scene** (`feature(...)`): a dark ground; mono tag `SISTEMA 0N · <ÁREA>`; title in
≤2 lines (88 px/800, per-word blur-in, ≤ 6–8 words); a **full-width band** (0–1080 px,
720 px tall, white, brand top border) showing the real screenshot with a pan + zoom-settle
(starts at scale ×1.14, settles to scale 1.2 while panning from `crop` to `pan_to`); a
blue **highlight box** drawn on the key element (coordinates in screenshot px); 3 chips
below (spring pop, staggered); a big outlined **ghost numeral** = system number (01/02)
as decoration; a **wipe** panel (surface + brand edge) sweeping off at the start covers
the cut. Screenshots are 1368 px wide (browser zoom 1.3–1.45); pick windows over dense
content, never over blank white, and end the pan where the useful part is visible.

Beat grid, motion vocabulary and ease choices follow `/hyperframes` `motion.md`: exits
shorter than entrances, a landed title stays dead still, vary entrances (blur-in, wipe,
clip-path reveal, spring pop).

Recurring `check` findings and the fix:

- `content_overlap` between two text blocks → a line wrapped to 2 lines (long Spanish
  phrases do); move the next block down or shorten the text.
- `line_unread` → a line is on screen < 0.5 s + 0.3 s/word. Shorten titles, or put a tag
  that repeats across cards OUTSIDE the cards so it lives the whole block.
- `text_below_floor` → 28 px floor at 1080 width (the `.n` label of the system cards is 30).
- `text_occluded` / `canvas_overflow` on the ghost numeral → add
  `data-layout-allow-overflow data-layout-allow-occlusion` to the ghost; add
  `data-layout-allow-overflow` to the panned image and the highlight.
- `dead_stretch` → `data-hold="true"` on the deliberately still element (the band).
- Duplicated media nodes warning when the same PNG is used in several cards → use
  `background-image` on a div instead of repeated `<img>`.
- Contrast on dim "not yet lit" card text → brighter grey (#8b949e).
- `first_frame_empty` on the hero → text visible from frame 0.

After `check`: `npx --yes hyperframes@0.9.8 snapshot --at <t,...>` and read the contact
sheet; look at each scene's start, mid-pan and end, plus the outro.

## 6. Environment quirks (this machine)

Run every `hyperframes` command with `export PATH="$HOME/.local/bin:$PATH"`.

- **ffmpeg**: installed system-wide (`/usr/bin/ffmpeg`, apt, 2026-11-04) — no
  `HYPERFRAMES_FFMPEG_PATH` needed any more. If it is ever missing again: there is no `sudo`
  for the agent, so ask Diego to run `! sudo apt-get install -y ffmpeg` (or use the static build
  from johnvansickle.com in `~/.local/bin`, after asking). Writing to `~/.bashrc` is blocked.
- **HeyGen**: `heygen` in `~/.local/bin`, signed in as Diego via `heygen auth login --oauth`
  (plan **Free**, no credits; no cloned voices on the account; whether Free allows
  `heygen voice clone create` is untested). `npx hyperframes auth status` to confirm. If it is ever missing, ask him to run
  `! curl -fsSL https://static.heygen.ai/cli/install.sh | bash` and
  `! npx hyperframes auth login --device` himself (the auto-mode classifier blocks the agent).
- **Music**: `npx hyperframes media-use resolve --type bgm --intent "upbeat energetic modern
  tech corporate electronic, driving rhythm, 120-128 BPM, no vocals, short punchy"
  --project .` → copy `.media/audio/bgm/bgm_XXX.wav` to `assets/bgm.wav` (re-use the same
  track across reels unless asked otherwise; the cached one is 120 BPM). Find the cut with
  `npx hyperframes audio assets/bgm.wav --only sections,onsets,moments --json`; for this
  track `data-media-start="10"` lands on a strong bar. `<audio id="bgm" class="clip"
  data-start="0" data-duration="25" data-media-start="10" data-fade-in="0.2"
  data-fade-out="1.6" src="assets/bgm.wav">`. Cut every 0.5 s (a beat) / 0.25 s.
- Pin the CLI: `npx --yes hyperframes@0.9.8 …` (matches the project's `package.json`).
- Render: `npx --yes hyperframes@0.9.8 render -o renders/<slug>_vN.mp4` takes ~1.5 min for
  25 s (software GPU). Delete older versions in `renders/` once a new one is approved.

## 7. Delivery

`renders/` is gitignored (`proyectos/*/{node_modules,renders,.hyperframes,.media}/`): the
mp4 and `caption.txt` are local artifacts, posted manually by Diego.

- **Final destination: Google Drive.** Every approved video + caption goes to
  `/mnt/diegosteinberg_google_drive_1790645175/1-Trabajo/reels dastudio/<slug>/` (one folder
  per project, containing the mp4 and `caption.txt`). Copy with `cp`, verify with `cmp`.
  Keep only the approved version there.
- **In the Claude desktop app, send the video with `SendUserFile`** (display `render`) and
  mention where `caption.txt` is (paste its text in the reply if he asks). This is the
  default now; ask only if he wants another channel.
- Write `renders/caption.txt` every time: hook line, the two systems with one line each,
  "Hoy X, mañana tu herramienta", a CTA question, `DAStudio · Desarrollo Web & Software a
  Medida`, 6–7 hashtags (#softwareamedida #desarrolloweb … + topic ones).
- Fallbacks when the app can't attach files: Google Drive MCP `create_file` only takes
  inline base64 (fine for the caption, impossible for the video), so for the video publish
  an Artifact page with `capabilities: {assets: {}, downloads: true}`, upload the mp4 with
  `asset: true`, and wire a **button** (not a link) to `claude.use("downloads")` →
  `fetch(blobPath).then(r=>r.blob())` → `downloads.save({filename, data})`; handle a
  `null`/declined result. A plain `<a href>` does not let phones save the file.
- After approval: ask before committing (`proyectos/<slug>/` is untracked until then).

## 8. Variant: reel "mezcla" (varios proyectos en un solo video)

Approved: `proyectos/portfolio-mix` v1 (30 s, 5 proyectos). Same house style, but the message
is "N proyectos reales, N rubros" and each project is one scene. Generator:
`templates/gen_mix.py` (read its header docstring; it uses `feature2` with **2 shots per scene**).

- **Intake adds**: which projects, and the URLs. Say how many fit: ~4.5 s per project, so
  5 projects ≈ 30 s (hook 2.5 + 5×4.5 + outro 5).
- **Screens**: reuse scrubbed captures that already exist (other reels' `assets/screens/`)
  and the portfolio's own `img/*.png` (real, no URL bar) before capturing production again;
  copy them into the new project's `assets/screens/` with a prefix per project (`flota-`,
  `cc-`, `jl-`, `eg-`, `nc-`). Check each `img/` file first: crop status bars/URL bars (e.g.
  the first `neocalcu_*.png` shows the domain in the browser bar — don't use it).
- **Mobile apps** (1080-wide portrait PNGs): crop the Android status bar (~88 px), use S=1.0,
  a taller band (`band_top=455, band_h=820`) and a vertical pan that "scrolls" the app.
  Highlight coordinates are in the cropped image's px (previews are scaled: multiply by the
  factor the image viewer reports).
- **Two shots per scene**: the first pans for half the scene; a brand-edged wipe sweeps across
  the band (0.5 s, starts 0.25 s before the cut) and hides the swap; then the second shot pans.
- **Hook / outro**: hook lists the N rubros and lights them in sequence (0.3 s apart); outro
  "Cinco rubros. / Tu herramienta." (keep each outro line to one line: long phrases wrap and
  trigger `content_overlap`) + chips of what DAStudio builds + the brand.
- **Audio for 30 s**: `data-media-start="5"` of the 35 s track (start on a bar; the peak lands
  on the outro); fade-out 1.4.
- Render takes ~2 min (30 s). Caption lists each project in one line with an emoji.

## 9. Variant: reel sin voz, de texto cinético ("sistema a medida")

Approved: `proyectos/sistema-a-medida` v2 (20 s, música, **sin voz**). Origin: Diego asked for a
reel like the one made in Ootto (hook "¿Para qué tener un sistema a medida?") but with only the
house music and animated on-screen text, "dinámico y ágil". Generator: `templates/gen_kin.py`
(read its header docstring; it builds on `gen_mix.py`).

- **Why no voice**: the voice used in the Ootto reel was Diego's clone there (Ootto subscription
  cancelled; reels were downloaded). Local `hyperframes tts` (Kokoro) only offers `ef_dora` for
  Spanish — Spain-neutral accent, female, NOT rioplatense, so it is rejected. HeyGen Free has no
  cloned voice. Options if a voice is wanted later: Diego records the locución himself (best), or
  a voice clone from a 30–60 s sample.
- **Structure (20 s)**: hero 2.5 s (the question in caps, `a medida` in brand blue, one sub-line)
  + 5 scenes × 2.5 s + outro 5 s ("Escribinos y contanos tu proceso" → DAStudio mark). Every
  scene = ONE real screenshot (no repeats between scenes; reuse scrubbed ones from other projects'
  `assets/screens/` or the portfolio's `img/`) + a 2-line title (≤ 33 characters or the third
  line collides with the band).
- **Text motion**: words pop in one by one (blur + rise + `back.out`), 0.09 s stagger; `*palabra`
  marks brand-blue words and `~palabra~` greys a word and draws an animated strike-through
  (emit that tween only in scenes that have it, or `check` flags the CSS transform conflict).
- **Bottom zone (below the band) is animated, never static** (Diego: "es muy estática"): in place
  of the old ghost numeral, each scene has (1) 3 chips that the **cursor** clicks in turn — each
  one turns brand-bordered with a ✓ (click times start at 1.5 s, after the chips' own entrance,
  and use `overwrite: "auto"`); (2) a **count-up number** with a label, driven by a gsap proxy
  object + `onUpdate`; (3) a 5-segment **progress bar** (previous scenes full, current fills
  linearly). Counter values must be real figures visible in that screenshot (75 unidades,
  224 medicamentos, "Ofertas 4", 12 meses); never invent numbers, and never draw fake charts.
  Keep everything above y≈1500 except the bar (Instagram UI owns the bottom).
- **Audio**: same `assets/bgm.wav`; for 20 s use `data-media-start="15"`, fade-out 1.4.
- Render ~1.5 min. Deliver as §7 (Drive folder `reels dastudio/<slug>/`, keep only the approved
  version, caption.txt with hook, 4 emoji bullets, CTA, brand line and 7 hashtags).

## 10. Variant: reel de UN proyecto en lote, texto cinético sin voz

Approved as drafts (2026-11-04): `tienda-online`, `landing-constructora`, `app-guardia`, `app-neonatal`,
`monitor-simulacion` (3 escenas de 4 s, 19,5 s) y `planillas-a-sistema` (concepto, 5 escenas de 2,5 s, 20 s).
Generator: `templates/gen_proj.py` (read its header docstring; it wraps `gen_kin.py`, so a new reel is a
config entry in `CFG`, not new code). Use it when Diego asks for several reels at once and "automático".

- **Screens**: portfolio's `img/*.png` (real, no URL bar) or scrubbed ones from other reels
  (`@archivo`). Skip any capture showing a domain (e.g. `neocalcu_1.png`) and crop the mobile status
  bar (`crop_top≈110` at 1080 wide). Low-res files (`*_2.png` 247 px wide) are unusable.
- **One screenshot, three zones**: with a single capture, vary `crop`/`pan_to`/`S` (1.2 → 1.6 to zoom) and
  put the highlight on a different element each scene. State that in the delivery note.
- **Counters** only with a figure really visible in that zone (4 ofertas, 8 años, 10 kg, 2540 g, 224
  resultados). Simulated values get "simulado" in the label. No figure → omit `count`.
- **Facts**: take names and claims from the repo's own captions (`proyectos/*/renders/caption.txt`) and
  fix them if Diego corrects one (JL is a **landing page**, not a licitaciones site).
- **Check + look**: `check` then `snapshot --at 4.5,8.5,12.5` + the contact sheet, before rendering (~1,2 min each).
- **Delivery**: `renders/<slug>_v1.mp4` + `caption.txt` → Drive `reels dastudio/<slug>/`; scheduling is
  done with the `portfolio-schedule` skill after Diego approves.

## 11. Variant: reel de proceso / concepto (sin capturas de producto, sin voz)

Approved as drafts (2026-11-04), pensados para los domingos a la mañana: `senales-sistema`,
`procesos-digitalizables`, `un-problema-primero`, `una-idea-varios-formatos` (19,5 s). Generator:
`templates/gen_text.py` (read its header docstring; one `CFG` entry per reel). Use it when the topic is
"cómo trabajamos / qué se puede resolver", NOT a project.

- **Structure**: hero 2,5 s (gancho en mayúsculas) → lista 9 s (2–6 tarjetas que entran de a una; el cursor
  las tilda) → remate 3 s (frase grande, 1–3 líneas, `*palabra` en celeste) → outro 5 s.
- **Copy rules**: no cifras, plazos, precios ni pasos de trabajo inventados. Los ejemplos de procesos salen
  de lo que ya muestran los captions del portfolio (stock, costos, flota, reportes, formularios, catálogo,
  alertas) y el método de Diego ("vemos qué conviene ordenar primero", ver `como-empieza-el-trabajo`).
- **Hero**: las palabras de la pregunta no pueden superar ~9 letras por línea a 150 px (si no, se sale del
  cuadro); `check` lo marca. Remate: una línea que se parte en dos da `content_overlap`: cortala a mano.
- Cards: con ≤4 ítems 46 px, con 6 ítems 36 px. Barra de progreso inferior y cursor son la zona animada.

## 12. Variant: reel ANTES / DESPUÉS (sin voz)

Draft pending Diego's review (2026-11-04): `proyectos/antes-y-despues` (23,5 s, 4 pares). Generator:
`templates/gen_ba.py` (read its header docstring; one `CFG` entry per reel, `pairs` = lista de pares).

- **Par de 4 s**: ANTES 1,5 s (frase grande en gris con UNA palabra tachada, solo texto) → DESPUÉS 2,5 s
  (escena de `gen_kin`: título, captura REAL, chips tildados por el cursor, contador).
- **Regla de marca**: el "antes" nunca se dibuja (nada de planillas, chats o pantallas falsas, ver §2/CLAUDE.md)
  y es un malestar genérico, nunca una afirmación sobre un cliente. El "después" siempre es una captura real.
- Pares del ejemplo: Planillas ~sueltas~ → Un tablero único; Vencimientos ~olvidados~ → Alertas
  automáticas; Costos ~dispersos~ → Costo por fase; Pedidos por ~chat~ → Catálogo online.
- Estructura: hero 2,5 s ("Antes y después") + N×4 s + outro 5 s. Audio: `data-media-start="10"` (la pista dura 35 s).
- Tag del "después": `NN / 0N · DESPUÉS · <tema>`; `antes` ≤ 30 caracteres.
