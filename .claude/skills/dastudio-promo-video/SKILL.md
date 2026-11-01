---
name: dastudio-promo-video
description: Scaffold a 15s vertical (1080x1920) DAStudio promo/reel video with HyperFrames from real product screenshots in img/, reusing the proven panel/cursor/iris-click mechanics, brand fonts, music and SFX. Use when asked for a DAStudio Instagram video, reel, or promo clip, or a series of them.
---

# DAStudio promo video

Produces a 15-second vertical (1080×1920, 30fps) brand video: a cursor clicks through 3-4 real screenshots of a DAStudio product (each click causes an iris transition to the next), lands on a one-line claim, then the DAStudio mark performs itself and an Instagram follow CTA holds. Built once for `/home/diego/dastudio-instagram-video` (the "Panel a Panel" launch video) and reused as a template for a 3-video series (Flota / Presencia Online / Apps de Salud). This skill is that template, made reusable.

**Resource discipline is the point of this skill**: every number below (panel box, click coordinates, timing, cursor path, iris math) is already proven — do not re-derive it, do not re-run the iterative snapshot-and-adjust loop from scratch. Pick content, fill the config, generate, check once, snapshot once, render. Reuse the bundled fonts/SFX/music verbatim; only fetch a fresh HeyGen music track if the person explicitly asks for a different mood.

## When to use

The person asks for a DAStudio promo/reel/Instagram video (or a series), "parecido a los anteriores", or "otro video como el de Flota/Herramientas/etc." If they want a genuinely different storyline, format, duration or look, fall back to the full `/hyperframes` skill instead (three storylines, fresh SPEC.md) — this skill is for the established DAStudio look, not for inventing a new one.

## 1. Pick the content (the only real thinking step)

For each video: 4 **real** screenshots from `/home/diego/portfolio/img` (never a mockup — see Brand rules below), one theme tying them together, 4 short chip labels, and a two-line claim.

- **hook** (slot `hook`): the most immediately legible screen — big numbers, a clear headline. This is frame 0, so it must read instantly.
- **mid_a**, **mid_b** (slots `mid_a`/`mid_b`): two more real screens from the same theme.
- **payoff** (slot `payoff`): the most visually striking screen — this one gets a continuous slow push instead of a click, and exits via a dip-cut (darken) instead of an iris.
- **claim**: `{line1, line2_prefix, line2_accent}` — e.g. `"Cada movimiento," / "bajo" / "control."`. The accent word lands in sky blue. Keep both lines short (≤6 words); never "Introducing"/"unlock"/"seamless" (see the main `/hyperframes` `story.md` copy rules).
- **chip** per beat: `JETBRAINS MONO UPPERCASE · WITH A MIDDLE DOT`, naming what's on screen functionally (never a domain — see Brand rules).

For `object_position` (CSS `object-position` on the screenshot inside its panel — this is the only per-image judgment call): look at the screenshot and estimate where the important content sits, as `X% Y%`. Desktop-wide screenshots (1360×641 or 1347×594) get height-constrained cropping — full height shows, only width crops — so X is what matters; a left-aligned hero or sidebar wants a low X (15-35%), a centered layout wants ~50%. A near-vertical screenshot (like NeoCalcu's 1080×2400) gets width-constrained cropping — only Y matters, and low Y (0-30%) keeps the top content (below any status/domain bar — see Brand rules) in frame. Don't over-think this: one reasonable guess, verified in the single snapshot pass in step 3.

## 2. Generate

```bash
python3 /home/diego/portfolio/.claude/skills/dastudio-promo-video/scripts/generate.py \
  --config my-video.json \
  --out-dir /home/diego
```

`--config` takes one video object or a JSON array of several (a series, built in one run). See the schema and a full worked example in `scripts/generate.py`'s docstring, or copy the shape below:

```json
{
  "dir": "dastudio-video-<slug>",
  "images_src_dir": "/home/diego/portfolio/img",
  "beats": [
    {"slot": "hook",   "image": "<file>.png", "object_position": "X% Y%", "chip": "LABEL · SUBLABEL"},
    {"slot": "mid_a",  "image": "<file>.png", "object_position": "X% Y%", "chip": "LABEL · SUBLABEL"},
    {"slot": "mid_b",  "image": "<file>.png", "object_position": "X% Y%", "chip": "LABEL · SUBLABEL"},
    {"slot": "payoff", "image": "<file>.png", "object_position": "X% Y%", "chip": "LABEL · SUBLABEL"}
  ],
  "claim": {"line1": "...", "line2_prefix": "...", "line2_accent": "..."}
}
```

Output into `--out-dir` as its own HyperFrames project (sibling of the portfolio repo, never inside it — these are rendered deliverables, not site code). The script copies the brand font, SFX and the already-trimmed 15s music bed verbatim (zero network calls), copies only the 4 named screenshots + the DAStudio mark, and writes `index.html` + `compositions/{beat1..4,claim,endcard}.html` from the templates in `templates/` with exactly three substitutions per beat file (image src, `object-position`, chip text) and two in the claim file. The end card (`endcard.html`) is copied **unchanged** every time — the DAStudio mark, tagline and "Seguinos @dastudioweb" CTA are identical across the whole series by design.

## 3. Verify once, then render

Do not repeat the full multi-round snapshot loop from the original build — it already proved the mechanics work. One pass is enough:

```bash
cd /home/diego/dastudio-video-<slug>
npx hyperframes check --json                     # must be 0 errors
npx hyperframes snapshot --at 0.5,2.8,5.0,7.5,9.9,12.9 --json   # one beat each + claim + end card
```

Look at the contact sheet. Fix only real problems (illegible crop, a domain leaking into frame, broken text) by editing the one `object-position` or `chip` line in the relevant `compositions/beat*.html` — don't polish further. Then:

```bash
npx hyperframes render --json
```

Sanity-check the output once: `ffprobe` for 1080×1920 @30fps, 15.0s, an AAC audio stream; `npx hyperframes audio <file> --json` for `loudness.lufsIntegrated` in **-16 to -14 LUFS** and `clipping.count: 0` (the bundled levels already target this — only re-check if you changed any `data-volume`).

## The mechanics (reference — already correct, don't redesign)

**Brand constants**: ground `#0d1117`, panel `#161b22` / border `#30363d` (3px, 16px radius), ink `#f0f6fc`, sky accent `#38bdf8` (rationed: click rings, iris flashes, the claim's accent word, the CTA glyph), display face Plus Jakarta Sans 800 (`assets/fonts/`, not bundled — `@font-face` required in any file using it), mono JetBrains Mono (bundled, used for every chip and the CTA line).

**Panel box** (identical in every beat, inside the Instagram-safe band y:168-1330): `left:56px; top:310px; width:968px; height:1150px`. Chip sits at `top:215px`, centered.

**The click/iris coordinate chain** (fixed — these are where the panels' own content made a click look natural, not arbitrary): hook's click/iris-close lands at `(656, 770)` → mid_a opens its entry iris there, clicks/closes at `(540, 943)` → mid_b opens there, clicks/closes at `(540, 1207)` → payoff opens there (no further click; it pushes 100%→104% continuously, then dip-cuts to black for 3 frames into the claim).

**Timing** (30fps, 450 frames = 15.000s exactly): hook 0-60 (2.0s) · mid_a 60-130 (2.333s) · mid_b 130-195 (2.167s) · payoff 195-270 (2.5s) · claim 270-330 (2.0s) · end card 330-450 (4.0s). Each product beat: chip pops in at local f6-14 (scale only, no fade — never fade+slide, it's on the BANNED list), cursor travels in and clicks at roughly 83-86% of the beat's length, iris-close/open takes 8 frames. Claim: two lines wipe in via `clip-path` (never opacity), accent word in sky. End card: mark fill rises bottom-to-top (`clip-path inset`), wordmark wipes in beside it, tagline wipes below, CTA pill pops with `back.out`, one small pulse, then static hold.

**Cursor**: hand-built inline SVG (not a registry component — the registry's `dart-cursor`/`agent-cursor` don't give frame-exact click timing), same path in every beat: `M5 3 L5 19 L9 15 L12 22 L15 20.5 L11.5 14 L18 14 Z`, 56px, ink fill + dark stroke. Click = sky ring scaling 1→5.83 with fading opacity (animate `scale`, never `width`/`height`/`margin` — those are layout properties and stutter under the seek-by-frame render; this was an actual lint error the first time).

**Audio**: one `<audio id="bgm">` at root (`data-volume="0.72"`, the whole 15s), one `<audio id="riser">` at root (`data-start="1.24" data-duration="10.03" data-volume="0.39"`, crests exactly as the end-card mark performs — `riser.mp3`'s own 10.03s build timed backward from the mark's reveal frame), and per-beat `<audio>` for `click.mp3` (on each click), `whoosh-short.mp3`/`whoosh.mp3` (on each cut/dip), `pop.mp3` (on the CTA landing) — all declared **inside** the sub-composition that owns the moment, with `data-hf-media-start-basis="local"` (silences an ambiguity lint warning; the timing really is local to that scene). Root-level `bgm`/`riser` need different `data-track-index` values or lint flags them as a same-track overlap even though the layering is intentional.

## Brand rules (from the portfolio's own CLAUDE.md — enforce every time)

- **Real screenshots only**, from `/home/diego/portfolio/img`. Never a drawn/invented UI.
- **No domain names in frame**, except `herramientaslibres.web.app` and `www.jlsrl.com.ar` (and even then, don't go out of your way to show the URL bar — functional labels in the chips, not domains). Watch for phone-frame screenshots that include a browser chrome bar with a URL in it (NeoCalcu's `neocalcu.pro` leaked into an early crop of this video — fixed by pushing `object-position`'s Y below the chrome bar). Check every new screenshot for this before finalizing its crop.
- **Neutral DAStudio branding** — the end card is the only place the brand performs, and it's the same every time (don't personalize per video).
- Functional chip labels (`🔒`-style descriptive tags), never the product's own domain, in the chips — consistent with how the live site hides domains on its project cards.

## Reusing vs. refreshing the music

The bundled `assets/bgm/track-15s.mp3` is already trimmed to this project's exact needs (124bpm, entered on a clean bar, faded in/out, levels tuned to -16 to -14 LUFS in the full mix) — reuse it by default; it's also a deliberate brand consistency device across a series. Only fetch a different track if the person asks for a different mood: `npx hyperframes auth status` (sign in once, free, via `! npx hyperframes auth login` typed by the person themselves — never type a login command on their behalf), then the `bgm` steps in the main `/media-use` skill's `audio/references/bgm.md`. Re-trim and re-tune levels the same way (enter on a strong bar, not the intro; check `npx hyperframes audio` for -16 to -14 LUFS, no clipping) before reusing it as the new `assets/bgm/track-15s.mp3` baseline.

## Files in this skill

- `templates/` — the 7 HyperFrames source files (`index.html`, 4 beat variants by slot, `claim.html`, `endcard.html`), each exactly as rendered in the original video minus the content that `generate.py` substitutes.
- `assets/` — brand font (woff2), 5 SFX files + credits (Pixabay license, no attribution required), the trimmed 15s music bed, the DAStudio mark PNG.
- `scripts/generate.py` — the templating script described above.
