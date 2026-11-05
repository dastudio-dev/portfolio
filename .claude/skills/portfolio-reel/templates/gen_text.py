#!/usr/bin/env python3
"""Generador de reels de PROCESO / CONCEPTO, sin capturas de producto y sin voz (texto cinetico).

Estructura (19,5 s a 120 BPM): hero 2,5 + escena de lista (9 s: tarjetas que entran de a una, el cursor les hace
clic y quedan con tilde) + frase de remate 3 s + outro 5 s. Reusa hero()/outro()/words()/BASE_CSS de gen_kin.py.
Uso: python3 -I gen_text.py <slug>   (agrega una entrada a CFG; mismas reglas de marca: sin cifras ni procesos inventados).
"""
import os, re, shutil, sys

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


def ptext(ns, sid, tag, title, items, dur=9.0):
    C = ns["C"]
    BASE_CSS = ns["BASE_CSS"]
    words = ns["words"]
    n = len(items)
    top, gap = 540, 22
    area = 1320 - top
    h = int((area - gap * (n - 1)) / n)
    h = min(h, 250)
    fs = 46 if n <= 4 else 36
    delta = min(1.4, 6.0 / n)
    t0 = 1.0
    cards, js = "", ""
    for i, it in enumerate(items):
        y = top + i * (h + gap)
        cards += (f'<div id="{sid}-c{i}" class="card" style="top:{y}px;height:{h}px">'
                  f'<span class="num mono" id="{sid}-n{i}">{i + 1}</span>'
                  f'<span class="txt">{words(it, "tw")}</span></div>')
        te = t0 + i * delta
        ct = te + 0.7
        cy = y + h / 2
        js += (f'\n      tl.to("#{sid}-c{i}", {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.5)" }}, {te:.2f});'
               f'\n      tl.to("#{sid}-cur", {{ x: 150, y: {cy + 10:.0f}, duration: 0.25, ease: "power2.inOut" }}, {ct - 0.25:.2f});'
               f'\n      tl.to("#{sid}-cur", {{ scale: 0.82, duration: 0.07, yoyo: true, repeat: 1 }}, {ct:.2f});'
               f'\n      tl.set("#{sid}-c{i}", {{ className: "card on" }}, {ct + 0.05:.2f});'
               f'\n      tl.fromTo("#{sid}-c{i}", {{ scale: 0.97 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2.5)", overwrite: "auto" }}, {ct + 0.05:.2f});'
               f'\n      tl.set("#{sid}-n{i}", {{ textContent: "✓" }}, {ct + 0.05:.2f});')
    html = f"""<!-- compositions/{sid}.html -->
<template>
  <style>{BASE_CSS}
    .title {{ position:absolute; left:70px; right:70px; top:255px; font-size:92px; font-weight:800; line-height:1.04;
      letter-spacing:-0.025em; z-index:5; }}
    .title .hi {{ color:var(--brand,#38bdf8); }}
    .card {{ position:absolute; left:70px; right:70px; display:flex; align-items:center; gap:30px; padding:0 34px;
      border:2px solid var(--border,#30363d); border-radius:24px; background:var(--surface,#161b22); z-index:5; }}
    .card.on {{ border-color:var(--brand,#38bdf8); background:#10253a; }}
    .num {{ flex:none; width:68px; height:68px; border-radius:50%; border:2px solid #6e7681; display:flex; align-items:center;
      justify-content:center; font-size:32px; font-weight:700; color:#c9d1d9; }}
    .card.on .num {{ background:var(--brand,#38bdf8); border-color:var(--brand,#38bdf8); color:#0d1117; }}
    .txt {{ font-size:{fs}px; font-weight:700; line-height:1.15; letter-spacing:-0.01em; }}
    .prog {{ position:absolute; left:70px; right:70px; top:1390px; height:10px; border-radius:5px; background:var(--border,#30363d); overflow:hidden; z-index:5; }}
    .prog b {{ display:block; height:100%; width:100%; background:var(--brand,#38bdf8); transform-origin:0 50%; }}
    .cur {{ position:absolute; left:0; top:0; width:46px; height:46px; z-index:9; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div id="{sid}-clip" class="clip" data-start="0" data-duration="{dur}" data-track-index="0" style="position:absolute;inset:0">
      <div id="{sid}-tag" class="tag mono">{tag}</div>
      <h2 id="{sid}-title" class="title">{words(title, "tw")}</h2>
      {cards}
      <div class="prog" data-layout-ignore><b id="{sid}-pf"></b></div>
      <svg id="{sid}-cur" class="cur" data-layout-ignore viewBox="0 0 24 24"><path d="M4 2 L4 19 L8.6 14.6 L11.6 21.4 L14.4 20.2 L11.4 13.6 L18 13.4 Z" fill="#ffffff" stroke="#0d1117" stroke-width="1.4" stroke-linejoin="round"/></svg>
      <div id="{sid}-wipe" class="wipe" data-layout-ignore></div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      gsap.set("#{sid}-title .tw", {{ opacity: 0, filter: "blur(10px)", y: 40, scale: 0.8 }});
      gsap.set("#{sid}-tag", {{ opacity: 0, x: -40 }});
      gsap.set("#{sid}-pf", {{ scaleX: 0 }});
      gsap.set("#{sid}-cur", {{ x: 900, y: 1450, opacity: 0 }});
      gsap.set("#{sid} .card, #{sid}-clip .card", {{ opacity: 0, y: 40, scale: 0.92 }});
      tl.to("#{sid}-wipe", {{ x: 1180, duration: 0.42, ease: "power3.inOut" }}, 0);
      tl.to("#{sid}-tag", {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 0.3);
      tl.to("#{sid}-title .tw", {{ opacity: 1, filter: "blur(0px)", y: 0, scale: 1, duration: 0.35, ease: "back.out(1.6)", stagger: 0.09 }}, 0.3);
      tl.to("#{sid}-pf", {{ scaleX: 1, duration: {dur - 0.4}, ease: "none" }}, 0.2);
      tl.to("#{sid}-cur", {{ opacity: 1, duration: 0.15 }}, 1.0);
      tl.to("#{sid}-cur", {{ opacity: 0, duration: 0.2 }}, {dur - 0.3});{js}
      tl.seek(0);
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{C}/{sid}.html", "w").write(html)


def statement(ns, sid, lines, dur=3.0):
    C = ns["C"]
    BASE_CSS = ns["BASE_CSS"]
    words = ns["words"]
    body = "".join(f'<div class="ln" id="{sid}-l{i}" style="top:{470 + i * 150}px">{words(l, "sw")}</div>' for i, l in enumerate(lines))
    html = f"""<!-- compositions/{sid}.html -->
<template>
  <style>{BASE_CSS}
    .ln {{ position:absolute; left:70px; right:70px; font-size:116px; font-weight:800; letter-spacing:-0.035em; line-height:1.02; }}
    .ln .hi {{ color:var(--brand,#38bdf8); }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div id="{sid}-clip" class="clip" data-start="0" data-duration="{dur}" data-track-index="0" style="position:absolute;inset:0">
      <div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion id="{sid}-g" style="font-size:560px;bottom:-30px">&lt;/&gt;</div>
      {body}
      <div id="{sid}-wipe" class="wipe" data-layout-ignore></div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      gsap.set("#{sid}-clip .sw", {{ opacity: 0, filter: "blur(12px)", y: 40, scale: 0.85 }});
      gsap.set("#{sid}-g", {{ opacity: 0, scale: 0.92 }});
      tl.to("#{sid}-wipe", {{ x: 1180, duration: 0.42, ease: "power3.inOut" }}, 0);
      tl.to("#{sid}-g", {{ opacity: 1, scale: 1, duration: 0.8, ease: "expo.out" }}, 0.2);
      tl.to("#{sid}-clip .sw", {{ opacity: 1, filter: "blur(0px)", y: 0, scale: 1, duration: 0.35, ease: "back.out(1.5)", stagger: 0.12 }}, 0.35);
      tl.seek(0);
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{C}/{sid}.html", "w").write(html)


def build(slug, cfg):
    P = scaffold(slug)
    os.environ["REEL_P"] = P
    ns = {"__name__": "gen", "HERO_Q": cfg["hero_q"], "HERO_SUB": cfg["hero_sub"], "NSEG": 1}
    exec(head_src, ns)
    ns["hero"]()
    ptext(ns, "t1", cfg["tag"], cfg["title"], cfg["items"], dur=9.0)
    statement(ns, "t2", cfg["close"], dur=3.0)
    ns["outro"]()
    total = 19.5
    sc = [("hero", 0, 2.5), ("t1", 2.5, 9), ("t2", 11.5, 3), ("outro", 14.5, 5)]
    hosts = "".join(f"""
      <div id="{i}" data-composition-id="{i}" data-composition-src="compositions/{i}.html"
        data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics"
        data-width="1080" data-height="1920"></div>
""" for i, s, d in sc)
    idx = open(ns["SRC_INDEX"]).read()
    k = idx.index('id="hero"')
    head = idx[: idx.rindex("<div", 0, k)]
    tail = f"""{hosts}
      <audio id="bgm" class="clip" data-start="0" data-duration="{total}" data-media-start="15" data-volume="1"
        data-fade-in="0.2" data-fade-out="1.4" data-track-index="0" src="assets/bgm.wav"></audio>
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
    print(slug, "ok")


CTA = "\n\nDAStudio · Desarrollo Web & Software a Medida\n\n"
CFG = {}

CFG["senales-sistema"] = dict(
    hero_q="3 *señales *de que necesitás *un sistema", hero_sub="Mirá si te pasa alguna.",
    tag="SEÑALES", title="¿Te *pasa *esto?",
    items=["Cargás los mismos datos dos veces", "Nadie sabe cuál es la última versión", "La información depende de una sola persona"],
    close=["Tu proceso", "*se puede *ordenar."],
    caption="""3 señales de que necesitás un sistema a medida 🚦

1️⃣ Cargás los mismos datos dos veces.
2️⃣ Nadie sabe cuál es la última versión.
3️⃣ La información depende de una sola persona.

Si te pasa alguna, tu proceso se puede ordenar.

¿Qué proceso te gustaría ordenar? Contanos 👇""" + CTA + "#softwareamedida #desarrolloweb #sistemasdegestion #pymes #procesos #dastudio",
)

CFG["procesos-digitalizables"] = dict(
    hero_q="Procesos *que se *pueden *ordenar", hero_sub="Algunos ejemplos de lo que armamos.",
    tag="EJEMPLOS", title="Se puede *ordenar:",
    items=["Stock y costos", "Flota y mantenimiento", "Reportes e indicadores", "Formularios y actas", "Catálogo y pedidos", "Alertas y vencimientos"],
    close=["¿No está", "*en la lista?", "*Contanos igual."],
    caption="""¿Qué procesos se pueden ordenar con un sistema a medida? 🧩

📦 Stock y costos
🚛 Flota y mantenimiento
📊 Reportes e indicadores
📝 Formularios y actas
🛒 Catálogo y pedidos
🔔 Alertas y vencimientos

¿No está en la lista? Contanos igual cómo trabajás 👇""" + CTA + "#softwareamedida #desarrolloweb #sistemasdegestion #pymes #procesos #dastudio",
)

CFG["un-problema-primero"] = dict(
    hero_q="Empezá *por *un problema", hero_sub="No hace falta tener todo definido.",
    tag="CÓMO ARRANCAR", title="Así *se *empieza",
    items=["Elegí un proceso que te quite tiempo", "Contanos cómo lo resolvés hoy", "Vemos qué conviene ordenar primero"],
    close=["Un *proceso.", "Un *problema.", "Una *solución."],
    caption="""No hace falta tener todo definido para empezar 🌱

1️⃣ Elegí un proceso que te quite tiempo.
2️⃣ Contanos cómo lo resolvés hoy.
3️⃣ Vemos qué conviene ordenar primero.

Un proceso, un problema, una solución.

¿Cuál es el tuyo? Escribinos 👇""" + CTA + "#softwareamedida #desarrolloweb #pymes #procesos #transformaciondigital #dastudio",
)

CFG["una-idea-varios-formatos"] = dict(
    hero_q="Una idea, *varios *formatos", hero_sub="Elegimos el que le sirve a tu negocio.",
    tag="FORMATOS", title="Puede *ser:",
    items=["Un sistema de gestión web", "Una app instalable que anda sin internet", "Una tienda online con catálogo", "Un sitio o landing para tu empresa"],
    close=["Del *problema,", "a la *herramienta", "*indicada."],
    caption="""Una misma idea puede tomar distintos formatos 💡

🖥️ Un sistema de gestión web.
📱 Una app instalable que anda sin internet.
🛒 Una tienda online con catálogo.
🏢 Un sitio o landing para tu empresa.

Del problema a la herramienta indicada.

¿Qué idea tenés en mente? Escribinos 👇""" + CTA + "#softwareamedida #desarrolloweb #pwa #ecommerce #landingpage #dastudio",
)

if __name__ == "__main__":
    for slug in (sys.argv[1:] or list(CFG)):
        build(slug, CFG[slug])
