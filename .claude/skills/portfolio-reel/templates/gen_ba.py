#!/usr/bin/env python3
"""Generador del reel ANTES / DESPUES, sin voz (texto cinetico + capturas reales). Ver SKILL.md seccion 12.

Cada par dura 4 s a 120 BPM: ANTES 1,5 s (frase grande con una palabra tachada, solo texto: nunca se dibuja una
planilla ni un chat falso) y DESPUES 2,5 s (la escena de gen_kin con la captura REAL, titulo, chips y contador).
Estructura: hero 2,5 + N pares de 4 s + outro 5 (N=4 -> 23,5 s). Reusa hero()/feature2()/outro() de gen_kin.py.
Copialo al scratchpad (no lo ejecutes desde el skill), agrega una entrada a CFG y corre:  python3 -I gen_ba.py <slug>
Cada par:  dict(antes="Planillas ~sueltas~", tag, title, shot=dict(img,w,S,crop,pan_to,hl), chips=[3], count=(valor,etiqueta))
  - antes: <=30 caracteres; solo UNA palabra con ~tilde~ (se tacha); lo "antes" es un malestar generico, nunca una afirmacion
    sobre un cliente real.
  - img: "@archivo" = captura ya depurada de sistema-a-medida/assets/screens, o un archivo de img/ (con recorte superior opcional).
Audio: la pista dura 35 s; con 23,5 s usa data-media-start="10".
"""
import os, re, shutil, sys
from PIL import Image

REPO = "/home/diego/Soft/repos/portfolio"
PROY = REPO + "/proyectos"
BASE = PROY + "/sistema-a-medida"
TPL = REPO + "/.claude/skills/portfolio-reel/templates/gen_kin.py"

src = open(TPL).read()
head_src = src[: src.index('hero()\nfeature2("k1"')]


def sub(s, old, new):
    assert old in s, old[:60]
    return s.replace(old, new)


head_src = re.sub(r'^P = ".*"$', 'P = os.environ["REEL_P"]', head_src, flags=re.M)
head_src = sub(head_src, "words('¿Para qué tener un sistema *a *medida?')", "words(HERO_Q)")
head_src = sub(head_src, "Tu operación, en una sola pantalla.", "{HERO_SUB}")
head_src = sub(head_src, "range(5)", "range(NSEG)")
head_src = sub(head_src, "{idx:02d} / 05", "{idx:02d} / {NSEG:02d}")
head_src = sub(head_src, '<div id="{sid}-cnt" class="cnt">',
               '<div id="{sid}-cnt" class="cnt" style="{\'display:none\' if not count else \'\'}">')


def scaffold(slug):
    P = f"{PROY}/{slug}"
    if os.path.exists(P):
        shutil.rmtree(P)
    shutil.copytree(BASE, P, ignore=shutil.ignore_patterns("compositions", "renders", "screens", "node_modules", ".hyperframes", ".media"))
    os.makedirs(P + "/assets/screens", exist_ok=True)
    os.makedirs(P + "/renders", exist_ok=True)
    for f in ("meta.json", "package.json"):
        t = open(f"{P}/{f}").read().replace("sistema-a-medida", slug)
        open(f"{P}/{f}", "w").write(t)
    return P


def antes(ns, sid, idx, n, phrase, dur=1.5):
    C, BASE_CSS, words = ns["C"], ns["BASE_CSS"], ns["words"]
    html = f"""<!-- compositions/{sid}.html -->
<template>
  <style>{BASE_CSS}
    .lab {{ position:absolute; left:70px; top:200px; font-size:30px; letter-spacing:0.14em; text-transform:uppercase; color:#8b949e; z-index:5; }}
    .lab b {{ color:var(--fg,#f8fafc); font-weight:700; }}
    .big {{ position:absolute; left:70px; right:70px; top:560px; font-size:128px; font-weight:800; line-height:1.02; letter-spacing:-0.035em; color:#c9d1d9; z-index:5; }}
    .big .st {{ color:#8b949e; }}
    .strike {{ position:absolute; left:-6px; right:-6px; top:54%; height:10px; background:var(--brand,#38bdf8); border-radius:5px; transform-origin:0 50%; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div id="{sid}-clip" class="clip" data-start="0" data-duration="{dur}" data-track-index="0" style="position:absolute;inset:0">
      <div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="font-size:560px;bottom:-30px;-webkit-text-stroke:3px rgba(139,148,158,0.14)">&lt;/&gt;</div>
      <div id="{sid}-lab" class="lab mono"><b>{idx:02d} / {n:02d}</b> &nbsp;·&nbsp; ANTES</div>
      <div id="{sid}-big" class="big">{words(phrase, "bw")}</div>
      <div id="{sid}-wipe" class="wipe" data-layout-ignore></div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      gsap.set("#{sid}-big .bw", {{ opacity: 0, filter: "blur(10px)", y: 40, scale: 0.85 }});
      gsap.set("#{sid}-big .strike", {{ scaleX: 0 }});
      gsap.set("#{sid}-lab", {{ opacity: 0, x: -40 }});
      tl.to("#{sid}-wipe", {{ x: 1180, duration: 0.42, ease: "power3.inOut" }}, 0);
      tl.to("#{sid}-lab", {{ opacity: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0.2);
      tl.to("#{sid}-big .bw", {{ opacity: 1, filter: "blur(0px)", y: 0, scale: 1, duration: 0.3, ease: "back.out(1.5)", stagger: 0.1 }}, 0.2);
      tl.to("#{sid}-big .strike", {{ scaleX: 1, duration: 0.25, ease: "power4.out" }}, 0.9);
      tl.seek(0);
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{C}/{sid}.html", "w").write(html)


def build(slug, cfg):
    P = scaffold(slug)
    for name, srcf in cfg["imgs"].items():
        if srcf.startswith("@"):
            shutil.copy(f"{BASE}/assets/screens/{srcf[1:]}", f"{P}/assets/screens/{name}")
        else:
            Image.open(f"{REPO}/img/{srcf}").convert("RGB").save(f"{P}/assets/screens/{name}")
    os.environ["REEL_P"] = P
    n = len(cfg["pairs"])
    ns = {"__name__": "gen", "HERO_Q": cfg["hero_q"], "HERO_SUB": cfg["hero_sub"], "NSEG": n}
    exec(head_src, ns)
    ns["hero"]()
    sc = [("hero", 0, 2.5)]
    for i, pr in enumerate(cfg["pairs"], 1):
        antes(ns, f"a{i}", i, n, pr["antes"])
        kw = dict(dur=2.5, count=pr.get("count"))
        if pr.get("mobile"):
            kw.update(band_top=455, band_h=820)
        ns["feature2"](f"d{i}", i, "Después · " + pr["tag"], pr["title"], [pr["shot"]], pr["chips"], **kw)
        t = 2.5 + (i - 1) * 4
        sc += [(f"a{i}", t, 1.5), (f"d{i}", t + 1.5, 2.5)]
    ns["outro"]()
    total = 2.5 + n * 4 + 5
    sc.append(("outro", total - 5, 5))
    hosts = "".join(f"""
      <div id="{i}" data-composition-id="{i}" data-composition-src="compositions/{i}.html"
        data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics"
        data-width="1080" data-height="1920"></div>
""" for i, s, d in sc)
    idx = open(ns["SRC_INDEX"]).read()
    k = idx.index('id="hero"')
    head = idx[: idx.rindex("<div", 0, k)]
    tail = f"""{hosts}
      <audio id="bgm" class="clip" data-start="0" data-duration="{total}" data-media-start="10" data-volume="1"
        data-fade-in="0.2" data-fade-out="1.4" data-track-index="0" src="assets/bgm.mp3"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    head = head.replace('data-duration="30"', f'data-duration="{total}"').replace('data-duration="25"', f'data-duration="{total}"')
    open(P + "/index.html", "w").write(head + tail.lstrip("\n"))
    open(P + "/renders/caption.txt", "w").write(cfg["caption"].strip() + "\n")
    print(slug, "ok", total, "s")


CTA = "\n\nDAStudio · Desarrollo Web & Software a Medida\n\n"
CFG = {}

CFG["antes-y-despues"] = dict(
    imgs={"a1.png": "@cc-indicadores.png", "a2.png": "@flota-unidades.png", "a3.png": "@flota-fases.png", "a4.png": "@tienda-1.png"},
    hero_q="Antes *y *después", hero_sub="Lo que cambia cuando el proceso se ordena.",
    pairs=[
        dict(antes="Planillas ~sueltas~", tag="Tablero", title="Un tablero *único",
             shot=dict(img="a1.png", w=1360, S=1.2, crop=(90, 141), pan_to=(330, 141), hl=(885, 515, 383, 252)),
             chips=["Indicadores", "Reportes", "Un solo lugar"], count=(12, "meses de historial")),
        dict(antes="Vencimientos ~olvidados~", tag="Alertas", title="Alertas *automáticas",
             shot=dict(img="a2.png", w=1368, S=1.2, crop=(0, 0), pan_to=(468, 20), hl=(36, 98, 1120, 240)),
             chips=["Unidades", "Obras", "Alertas"], count=(75, "unidades")),
        dict(antes="Costos ~dispersos~", tag="Costos", title="Costo *por fase",
             shot=dict(img="a3.png", w=1368, S=1.2, crop=(0, 30), pan_to=(110, 30), hl=(40, 215, 340, 340)),
             chips=["Fases", "Materiales", "Servicios"], count=(2, "fases con gasto")),
        dict(antes="Pedidos por ~chat~", tag="Catálogo", title="Catálogo *online",
             shot=dict(img="a4.png", w=1360, S=1.2, crop=(0, 0), pan_to=(260, 40), hl=(300, 325, 650, 300)),
             chips=["Catálogo", "Ofertas", "WhatsApp"], count=(4, "ofertas destacadas")),
    ],
    caption="""Antes y después de ordenar un proceso 🔄

📊 Planillas sueltas → un tablero único con indicadores.
🔔 Vencimientos olvidados → alertas automáticas.
🏗️ Costos dispersos → costo por fase, claro.
🛒 Pedidos por chat → catálogo online.

Hoy una planilla, mañana tu herramienta: sistemas de gestión, e-commerce, apps clínicas, sitios corporativos.

¿Cuál es tu "antes"? Contanos 👇""" + CTA + "#softwareamedida #desarrolloweb #antesydespues #sistemasdegestion #pymes #dastudio",
)

if __name__ == "__main__":
    for slug in (sys.argv[1:] or list(CFG)):
        build(slug, CFG[slug])
