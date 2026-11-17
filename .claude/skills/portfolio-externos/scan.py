#!/usr/bin/env python3
"""Escanea Drive/reels dastudio/Externos y sincroniza registro.json (sin tocar nombres).
Uso: python3 scan.py [--json]   -> imprime un informe; actualiza el registro.
Un reel = una subcarpeta con un .mp4 y un caption (.txt). Se identifica por el sha1 del mp4,
así sobrevive a renombres."""
import hashlib, json, os, sys, datetime as dt

ROOT = "/mnt/diegosteinberg_google_drive_1790645175/1-Trabajo/reels dastudio/Externos"
REG = os.path.join(ROOT, "registro.json")

def sha1(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def load():
    try:
        with open(REG, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"version": 1, "reels": {}}

def main():
    reg = load()
    reels = reg["reels"]
    seen, problems = set(), []
    for d in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        files = os.listdir(p)
        mp4s = [f for f in files if f.lower().endswith(".mp4")]
        caps = [f for f in files if f.lower().endswith((".txt", ".docx", ".md"))]
        if len(mp4s) != 1:
            problems.append(f"{d}: {len(mp4s)} mp4 (se esperaba 1)")
            continue
        mp4 = os.path.join(p, mp4s[0])
        h = sha1(mp4)
        seen.add(h)
        r = reels.setdefault(h, {
            "slug": None, "estado": "nuevo", "veces_publicado": 0, "publicaciones": [],
            "primera_vez": dt.date.today().isoformat(), "notas": []})
        r["carpeta"] = d
        r["mp4"] = mp4s[0]
        r["bytes"] = os.path.getsize(mp4)
        r["caption"] = None
        for c in caps:
            if os.path.getsize(os.path.join(p, c)) > 0:
                r["caption"] = c
        if not r["caption"]:
            problems.append(f"{d}: sin caption utilizable (vacío o ausente)")
    for h, r in reels.items():
        if h not in seen and r["estado"] != "retirado":
            problems.append(f"{r.get('carpeta')}: mp4 ya no está en la carpeta (hash {h[:8]})")
    reg["actualizado"] = dt.datetime.now().isoformat(timespec="minutes")
    with open(REG, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
    pend = [r for r in reels.values() if r["estado"] in ("nuevo", "revisado", "aprobado")]
    print(f"Reels: {len(reels)} | por publicar: {len(pend)} | publicados al menos 1 vez: "
          f"{sum(1 for r in reels.values() if r['veces_publicado'])}")
    for h, r in reels.items():
        print(f"- [{r['estado']}] {r.get('slug') or '(sin slug)'} · carpeta={r.get('carpeta')} · "
              f"publicado x{r['veces_publicado']} · hash={h[:8]}")
    for pr in problems:
        print("PROBLEMA:", pr)

main()
