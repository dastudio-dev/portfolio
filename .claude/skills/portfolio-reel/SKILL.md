---
name: portfolio-reel
description: Build an Instagram Reel/Story (HyperFrames, vertical 1080x1920) for a DAStudio portfolio project from real screenshots, following this repo's branding rules. Use when asked to make, generate, or resume a reel/video for a project in proyectos/.
---

# Portfolio reel (DAStudio / HyperFrames)

How this repo turns a project into a 1080x1920 HyperFrames video for Instagram, end to
end: intake, getting real screenshots (including from a panel behind login, over a
remote/no-browser CLI session), scrubbing them for privacy/brand before they become
assets, the house visual template, environment quirks specific to this machine, and
how to deliver a render that is deliberately not committed to git.

Read `/hyperframes` first for anything HyperFrames-specific this file doesn't cover
(contract, work loop, `check`/`snapshot`/`render`). This file is the DAStudio-specific
layer on top of it.

## 1. Intake — always ask before building

Before scaffolding or writing any composition, ask for (see
`memory/feedback_hyperframes_intake.md` in the user's auto-memory, which also governs
this):

1. **La web** — URL of the deployed site.
2. **El repositorio** — the project's own repo (context, not just the public URL).
3. **Duración** — never assume 15s/30s.
4. **Audio** — music/voice/mute, and what kind.
5. **Foco** — any specific feature/screen the person wants emphasized, or "recorrido
   general" (a plain tour of the main screens).

A **caption for the post is not optional** — always write one and deliver it
alongside the video, whether or not the person asked for it (§7).

## 2. Getting real screenshots

Per `CLAUDE.md`: **no invented mockups, ever** — only real screenshots of the
production site.

- **Public site**: `npx hyperframes capture <url> --json` (see `/hyperframes`
  "From a website" guidance). Prefer this; it's a clean, scroll-stitched capture.
- **Behind a login, and no browser-automation tool is connected in this session**
  (true for a plain CLI/tmux session over SSH — check with `ToolSearch` for
  `claude-in-chrome` / `Claude_Browser` tools before assuming): you cannot log in
  and capture yourself. Ask the person to log in from their own browser, take
  screenshots of the key screens, and get them to you:
  - If they're on the **same machine** this session runs on: ask for the local
    file path and `Read` it directly.
  - If they're on a **different machine** (e.g. a Chromebook attached to a remote
    tmux session on a desktop): don't suggest `scp`/terminal transfer first — it's
    real friction for a non-technical path. Suggest **Google Drive**: ChromeOS
    saves/uploads to Drive natively, and the Google Drive MCP connector
    (`mcp__claude_ai_Google_Drive__*`) can search and download from the same session.
    Ask for the folder link, `search_files` with `parentId = '<folder id from the
    URL>'`, then `download_file_content` per file. Each file's `content` often
    exceeds the single tool-result size limit — when it does, the result is saved
    to a local `.txt` (JSON with a `content` field); extract and `base64 -d` it
    with a shell one-liner instead of reading the saved file inline.

## 3. Scrub before using as an asset

Real screenshots taken by a person routinely leak things the final brand voice (§4)
must not show. Before copying anything into `proyectos/<slug>/assets/`:

- **Crop the browser's own chrome** (tabs, address bar, bookmarks bar) if present —
  keep only the actual page content. Sample a vertical pixel column with PIL to find
  the exact row the real app's own header starts at; don't guess.
- **Redact personal identifiers** — a logged-in user's email/name shown in the app's
  own header, a browser link-hover tooltip revealing the real domain
  (`https://thedomain.app/...`) at the bottom of the frame, etc. Technique: sample
  the exact background color next to the text with PIL (`im.load()[x, y]`), then
  draw a filled rectangle of that color over the region (`ImageDraw.rectangle`) —
  it blends seamlessly. Do this for every screenshot that needs it; check each one.
- No ImageMagick is installed on this machine; Pillow (`python3 -c "import PIL"`)
  is available — use it directly, no install needed.

## 4. House visual template (per `CLAUDE.md`)

- **Palette**: `--ground:#0d1117` `--surface:#161b22` `--border:#30363d`
  `--brand:#38bdf8` (sky) `--accent:#2563eb` (blue). No neon, no blurred radial
  glows, no AI-template clichés (see HyperFrames' own `story.md` §8 banned list —
  it agrees with this repo's rules).
- **Fonts**: *Plus Jakarta Sans* (display/body) + *JetBrains Mono* (badges/mono).
  JetBrains Mono is bundled by HyperFrames and resolves by name. Plus Jakarta Sans is
  **not** bundled — download the weights you need as `@font-face` files:
  ```bash
  curl -s "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" -o /tmp/pjs.css
  # then curl -sL each fonts.gstatic.com .ttf URL from that CSS into assets/fonts/
  ```
- **No exposed domains, ever** (except the two explicit exceptions listed in
  `CLAUDE.md`). Build a browser-chrome frame (toolbar, 3 dots, centered pill) with a
  **functional label** instead of the real URL — e.g. `🔒 Panel Interno`, matching
  the style of `CLAUDE.md`'s own examples (`🔒 Panel de Gestión de Flota`,
  `🛒 Tienda Online & Catálogo`). This repo's first reel (`calidad-carrillo`) hand-built
  a fixed-pixel version of this frame rather than the HyperFrames registry's
  `browser-device-stage` component, because the registry component's responsive
  `cqmin` sizing is tuned for an arbitrary reusable mount box, not a known
  1080x1920 layout — simpler to size it directly per scene. `catalog --query` it
  again before repeating this choice in case a better-fit block exists by then.
- **Brand mark**: reuse `img/logo-icon.png` from the repo root for the end card
  (don't redraw it).
- **Vertical safe zones** (`/hyperframes` `types/vertical.md`): nothing in the top
  168px, keep all text/product inside the 168–1330px band, texture-only below 1330px.

## 5. Project structure

One `hero.html` (title card: project's functional label, e.g.
`🏥 Gestión de Calidad y Seguridad Hospitalaria`) → one scene per screen (device-chrome
frame + real screenshot + big caption + step counter `N / total`) → `outro.html`
(DAStudio mark + "Desarrollo Web & Software a Medida" + CTA). Generate the repeated
per-screen scenes from one Python template (a `dict` per screen: id, image, caption,
step) rather than hand-writing near-duplicate HTML files — faster and keeps them
consistent. Size each screen's image container to that image's own aspect ratio
(`container_width * img_h / img_w`) so `object-fit: cover` never crops real content
off the edges — don't just pick one fixed height for every screen; screenshots taken
by hand are rarely a consistent size.

The settle-then-hold treatment (device fades/rises in, sits still, fades out) is a
sober baseline, not a ceiling — it's what the first reel (`calidad-carrillo`) used
everywhere. Later reels can carry more motion per screen (a slow push-in on the
device, the screenshot panning inside its frame, a sharper punch-in on one stat) —
see `/hyperframes` `motion.md` for the vocabulary. Default to the plain settle+hold
(it's correct and on-brand), but it's fine to offer more movement, and do it when the
person asks for something livelier.

Recurring `check` findings on this template, and the fix:

- `dead_stretch` on a screen's readable hold → add `data-hold="true"` on the element
  that's deliberately still (the device frame), not a shorter hold.
- `text_below_floor` → floor is 28px at 1080 width; bump the pill/caption font, don't
  shrink the box.
- `clipped_text` on the chrome pill → shorten the label text and/or widen the pill's
  `max-width`, in that order.
- `first_frame_empty` on the hero → don't fade the headline up from `opacity:0` at
  t=0; set it visible from frame 0 and animate something else (a light blur-in is
  fine, full invisibility is not — per `/hyperframes` "the hook": frame 0 is the
  thumbnail).

## 6. Environment quirks (this machine)

- **No `sudo`**: can't `apt-get install ffmpeg`. A static ffmpeg build lives at
  `/tmp/ffmpeg-static/ffmpeg-*-amd64-static/{ffmpeg,ffprobe}` (from
  johnvansickle.com) — re-download it if a fresh session doesn't have it (`/tmp` is
  not persistent across restarts). Point every `hyperframes` invocation at it with
  env vars on **every single command** (not persisted — writing to `~/.bashrc` is
  blocked by the auto-mode classifier as unauthorized persistence):
  ```bash
  export HYPERFRAMES_FFMPEG_PATH="/tmp/ffmpeg-static/ffmpeg-7.0.2-amd64-static/ffmpeg"
  export HYPERFRAMES_FFPROBE_PATH="/tmp/ffmpeg-static/ffmpeg-7.0.2-amd64-static/ffprobe"
  ```
- **Music/voice/images via HeyGen catalog** (`media-use resolve`) needs the `heygen`
  CLI, which isn't installed by default. Installing it means piping/running a
  downloaded shell script, which the auto-mode classifier blocks for the agent
  itself ("Code from External") even after you've read and verified the script is
  legitimate. Ask the person to run it themselves with the `!` prefix:
  ```
  ! curl -fsSL https://static.heygen.ai/cli/install.sh | bash
  ```
  then `! npx hyperframes auth login --device` (not plain `auth login` — this is a
  headless/remote terminal, so the browser-callback flow fails; `--device` gives a
  code + URL the person opens on any device).
- Installed `heygen` lands in `~/.local/bin`, not on `PATH` by default — add
  `export PATH="$HOME/.local/bin:$PATH"` alongside the ffmpeg exports above.
- Pick the music cut point deliberately: `npx hyperframes audio <file> --only
  sections,onsets,moments --json` segments the track — if section A (the start) is a
  slow build, start the bed from section B/C instead (`data-media-start`), per
  `/hyperframes` `sound.md`.

## 7. Delivery — the render is not committed, and delivery method is not assumed

This repo's `.gitignore` excludes `proyectos/*/{node_modules,renders,.hyperframes,.media}/`
— the rendered `.mp4` is a local artifact only, downloaded and posted manually (see
`memory/project_hyperframes_reels_setup.md`). So after `npx hyperframes render`,
**don't assume the person can just grab the file from the repo or via `scp`** —
that's exactly the friction that led to using Drive for screenshot intake (§2).

**Ask, don't assume, how to deliver it** — once the render exists, ask where the
person wants it (e.g. the same Drive folder the screenshots came from, if it'll fit;
or propose the Artifact download page below) rather than defaulting silently to one
path. Whatever the channel, **always write and deliver a caption** for the post
alongside the video (§1) — generate it even if the person only asked for the video.

- `mcp__claude_ai_Google_Drive__create_file` only takes **inline** `base64Content` —
  there is no server-side fetch/upload-by-path option. A rendered reel (several MB)
  is 3-4M+ base64 characters, which is far past what fits in a single tool call —
  don't attempt it; it will blow the turn's output budget before finishing. Drive
  works fine for the **caption** (plain text, trivial size) — `create_file` with
  `parentId` set to the same folder the screenshots came from.
- For the **video**, propose an Artifact download page instead. The plain
  `<a href="...">` / long-press-to-save pattern does **not** reliably let a phone
  browser save the file (confirmed: the person could play it but not download it) —
  build it with the `downloads` capability instead:
  1. Publish a small HTML page (`Artifact`, no `url` yet) with a `<video controls>`
     preview and a "Descargar" `<button>` (not a link).
  2. Republish the same `file_path` with `capabilities: {assets: {}, downloads: true}`
     declared (the asset upload is refused until `assets` is declared on the live
     version).
  3. Upload the rendered `.mp4`: `Artifact` with that `url`, `asset: true`,
     `file_path` pointing at the render (15MB/binary ceiling, comfortably fits a
     ~30s 1080x1920 render). It returns a same-origin path like
     `/_blob/<id>` — put that in the `<video src>` and keep it for the button's
     fetch below.
  4. Wire the button's `onclick` to: `claude.use("downloads")` → on click,
     `fetch(blobPath).then(r => r.blob())` → `downloads.save({filename, data: blob})`
     (mp4 is in the save allowlist). Handle `downloads` resolving `null` (fall back
     to `window.open(blobPath)`) and a rejected `save` (e.g. `declined`) by
     re-enabling the button with a hint to long-press the video as a last resort.
     This is the part that actually lets a phone save the file — the earlier
     plain-`<a>` version did not.
  5. Share the resulting `claude.ai/artifact/...` link. It's private to the
     publishing account by default (view it with `action: "open"` to sanity-check
     it yourself before handing it over).
