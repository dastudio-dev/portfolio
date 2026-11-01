#!/usr/bin/env python3
"""
Scaffolds a 15s vertical (1080x1920) DAStudio promo video as a HyperFrames
project, from a JSON config of 4 real screenshots + two lines of claim copy.
See ../SKILL.md for the full mechanics (panel geometry, the fixed iris/click
coordinate chain, timing map). This script only does template substitution +
asset copying — it never invents crops or copy, those come from the config.

Usage:
  python3 generate.py --config my-video.json [--out-dir /home/diego]

Config shape (one video):
{
  "dir": "dastudio-video-<slug>",        // output folder name
  "images_src_dir": "/home/diego/portfolio/img",  // where to copy real screenshots from
  "beats": [
    {"slot": "hook",     "image": "flota_1.png",        "object_position": "33% 40%", "chip": "GESTIÓN DE FLOTA · PANEL GENERAL"},
    {"slot": "mid_a",    "image": "flota_4.png",         "object_position": "28% 35%", "chip": "GESTIÓN DE FLOTA · MOVIMIENTOS"},
    {"slot": "mid_b",    "image": "flota_5.png",         "object_position": "25% 20%", "chip": "GESTIÓN DE FLOTA · INFORMES DE COSTOS"},
    {"slot": "payoff",   "image": "flota_3.png",         "object_position": "30% 30%", "chip": "GESTIÓN DE FLOTA · STOCK EN DEPÓSITO"}
  ],
  "claim": {"line1": "Cada movimiento,", "line2_prefix": "bajo", "line2_accent": "control."}
}

Pass a list of these objects (a JSON array) to build several videos in one run.
"""
import argparse
import json
import os
import re
import shutil

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL_DIR = os.path.join(SKILL_DIR, "templates")
ASSETS_DIR = os.path.join(SKILL_DIR, "assets")

SLOT_TEMPLATE_FILE = {
    "hook": "beat-hook.html",
    "mid_a": "beat-mid-a.html",
    "mid_b": "beat-mid-b.html",
    "payoff": "beat-payoff.html",
}
SLOT_PREFIX = {"hook": "s1", "mid_a": "s2", "mid_b": "s3", "payoff": "s4"}
SLOT_OUT_FILE = {"hook": "beat1.html", "mid_a": "beat2.html", "mid_b": "beat3.html", "payoff": "beat4.html"}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def set_img(content, new_src):
    return re.sub(r'src="\.\./assets/images/[^"]+"', f'src="../assets/images/{new_src}"', content, count=1)


def set_objpos(content, new_pos):
    return re.sub(r"object-position: [^;]+;", f"object-position: {new_pos};", content, count=1)


def set_chip(content, prefix, new_text):
    pattern = rf'(id="{prefix}-chip">)[^<]+(</div>)'
    return re.sub(pattern, lambda m: m.group(1) + new_text + m.group(2), content, count=1)


def build_beat(slot, image, object_position, chip_text):
    template = read(os.path.join(TPL_DIR, SLOT_TEMPLATE_FILE[slot]))
    prefix = SLOT_PREFIX[slot]
    c = set_img(template, image)
    c = set_objpos(c, object_position)
    c = set_chip(c, prefix, chip_text)
    return c


def build_claim(line1, line2_prefix, line2_accent):
    c = read(os.path.join(TPL_DIR, "claim.html"))
    c = re.sub(r'(id="s5-line1">)[^<]+(</div>)', lambda m: m.group(1) + line1 + m.group(2), c, count=1)
    c = re.sub(
        r'(id="s5-line2">)que <span class="s5-accent">[^<]+</span>(</div>)',
        lambda m: m.group(1) + f'{line2_prefix} <span class="s5-accent">{line2_accent}</span>' + m.group(2),
        c,
        count=1,
    )
    return c


def build_one(video, out_root):
    root = os.path.join(out_root, video["dir"])
    os.makedirs(os.path.join(root, "compositions"), exist_ok=True)
    os.makedirs(os.path.join(root, "assets", "fonts"), exist_ok=True)
    os.makedirs(os.path.join(root, "assets", "sfx"), exist_ok=True)
    os.makedirs(os.path.join(root, "assets", "bgm"), exist_ok=True)
    os.makedirs(os.path.join(root, "assets", "images"), exist_ok=True)

    # brand assets — reused verbatim, zero network calls
    shutil.copy(os.path.join(ASSETS_DIR, "fonts", "PlusJakartaSans-800.woff2"), os.path.join(root, "assets", "fonts"))
    for s in ["click.mp3", "whoosh-short.mp3", "whoosh.mp3", "pop.mp3", "riser.mp3", "CREDITS.md"]:
        shutil.copy(os.path.join(ASSETS_DIR, "sfx", s), os.path.join(root, "assets", "sfx"))
    bgm_name = video.get("bgm_file", "track-15s.mp3")
    bgm_src = video.get("bgm_src_path") or os.path.join(ASSETS_DIR, "bgm", "track-15s.mp3")
    shutil.copy(bgm_src, os.path.join(root, "assets", "bgm", "track-15s.mp3"))
    shutil.copy(os.path.join(ASSETS_DIR, "images", "logo-icon.png"), os.path.join(root, "assets", "images"))

    images_src_dir = video["images_src_dir"]
    for beat in video["beats"]:
        shutil.copy(os.path.join(images_src_dir, beat["image"]), os.path.join(root, "assets", "images", beat["image"]))

    name = video["dir"]
    with open(os.path.join(root, "meta.json"), "w", encoding="utf-8") as f:
        json.dump({"id": name, "name": name, "createdAt": "2026-01-01T00:00:00.000Z"}, f, indent=2)
    with open(os.path.join(root, "package.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "name": name,
                "private": True,
                "type": "module",
                "scripts": {
                    "dev": "npx --yes hyperframes@0.8.226 preview",
                    "check": "npx --yes hyperframes@0.8.226 check",
                    "render": "npx --yes hyperframes@0.8.226 render",
                    "publish": "npx --yes hyperframes@0.8.226 publish",
                },
            },
            f,
            indent=2,
        )
    with open(os.path.join(root, "hyperframes.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
                "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
                "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
                "media": {"autoProxy": True},
            },
            f,
            indent=2,
        )

    for beat in video["beats"]:
        content = build_beat(beat["slot"], beat["image"], beat["object_position"], beat["chip"])
        with open(os.path.join(root, "compositions", SLOT_OUT_FILE[beat["slot"]]), "w", encoding="utf-8") as f:
            f.write(content)

    claim = video["claim"]
    with open(os.path.join(root, "compositions", "claim.html"), "w", encoding="utf-8") as f:
        f.write(build_claim(claim["line1"], claim["line2_prefix"], claim["line2_accent"]))

    # end card — identical DAStudio branding every time, copied verbatim
    shutil.copy(os.path.join(TPL_DIR, "endcard.html"), os.path.join(root, "compositions", "endcard.html"))

    shutil.copy(os.path.join(TPL_DIR, "index.html"), os.path.join(root, "index.html"))

    print(f"built {root}")
    return root


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="JSON file: one video object, or an array of them")
    ap.add_argument("--out-dir", default=os.path.dirname(os.path.dirname(os.path.dirname(SKILL_DIR))))
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as f:
        cfg = json.load(f)
    videos = cfg if isinstance(cfg, list) else [cfg]

    built = [build_one(v, args.out_dir) for v in videos]
    print("\nNext, for each project:")
    for b in built:
        print(f"  cd {b} && npx hyperframes check --json && npx hyperframes render --json")


if __name__ == "__main__":
    main()
