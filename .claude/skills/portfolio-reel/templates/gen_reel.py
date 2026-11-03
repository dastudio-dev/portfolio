#!/usr/bin/env python3
"""Plantilla del generador de reels DAStudio (estilo aprobado: calidad-carrillo v3 y flota-firebase v1).

Cómo usarla (ver SKILL.md §5):
  1. Copiala a un lugar temporal (scratchpad), NO la ejecutes desde el skill.
  2. Cambiá P (carpeta del proyecto) y, si hace falta, SRC_INDEX (index.html de un reel ya hecho:
     de ahí se reusa la cabecera con @font-face y variables; el script sólo regenera los <div> de escenas).
  3. Editá hero(): textos de las dos tarjetas "Sistema 01/02" y el subtítulo "Este caso, para ...".
  4. Editá las llamadas a feature(...) al final: una por captura (ver parámetros abajo).
  5. Editá outro() (frase de remate) y la lista `scenes` (id, inicio, duración; todo múltiplo de 0.5 a 120 BPM).
  6. python3 gen.py  ->  npx hyperframes check  ->  snapshot  ->  render.

feature(sid, num_sistema, total, tag, titulo, imagen, crop=(x,y), scale, pan_to=(x,y), hl=(x,y,w,h), chips, dur)
  - imagen: PNG de 1368 px de ancho en assets/screens/ (ya limpia; ver scrub_template.py)
  - crop: esquina sup-izq (px de la captura) donde ARRANCA la ventana; pan_to: esquina donde TERMINA.
    Con scale=1.2 la ventana es 900 px de ancho y 600 de alto de captura; elegí ventanas sobre contenido denso.
  - hl: recuadro de resalte en px de la captura (se dibuja con el paneo).
  - montage() es opcional (tarjetas de 1.25 s con una tira de UI real); para usarlo, llamalo y agregalo a `scenes`.
"""
"""Genera las composiciones del reel calidad-carrillo v2 (25 s, 1080x1920)."""
import os, json

P = "/home/diego/Soft/repos/portfolio/proyectos/flota-firebase"
SRC_INDEX = "/home/diego/Soft/repos/portfolio/proyectos/calidad-carrillo/index.html"
C = P + "/compositions"

# limpiar escenas del reel anterior (siguen en git)
os.makedirs(C, exist_ok=True)

BASE_CSS = """
    #root { position:absolute; inset:0; overflow:hidden; background:var(--ground,#0d1117);
      font-family:var(--font-display,"Plus Jakarta Sans",sans-serif); color:var(--fg,#f8fafc); }
    .wipe { position:absolute; top:0; bottom:0; left:0; width:1100px; background:var(--surface,#161b22); z-index:50; }
    .wipe::after { content:""; position:absolute; top:0; bottom:0; right:0; width:14px; background:var(--brand,#38bdf8); }
    .mono { font-family:var(--font-mono,"JetBrains Mono",monospace); }
    .ghost { position:absolute; left:40px; bottom:-60px; font-size:760px; font-weight:800; line-height:1; letter-spacing:-0.04em;
      color:transparent; -webkit-text-stroke:3px rgba(56,189,248,0.16); z-index:1; }
    .tag { position:absolute; left:70px; top:200px; font-size:30px; letter-spacing:0.14em; text-transform:uppercase;
      color:var(--brand,#38bdf8); z-index:5; }
    .tag b { color:var(--fg,#f8fafc); font-weight:700; }
"""

def words(text, cls="w"):
    return " ".join(f'<span class="{cls}" style="display:inline-block">{w}</span>' for w in text.split())

# --------------------------------------------------------------------------------------
# Escena de feature: pantalla real ancha a sangre + titular + chips + numeral fantasma
# --------------------------------------------------------------------------------------
def feature(sid, num, total, tag, title, img, crop, scale, pan_to, hl, chips, dur=3.0, band_top=480, band_h=720):
    cx, cy = crop
    ex, ey = pan_to
    hlx, hly, hlw, hlh = hl
    chip_html = "".join(f'<span class="chip mono">{c}</span>' for c in chips)
    html = f"""<!-- compositions/{sid}.html -->
<template>
  <style>{BASE_CSS}
    .title {{ position:absolute; left:70px; right:70px; top:255px; font-size:88px; font-weight:800; line-height:1.04;
      letter-spacing:-0.025em; z-index:5; }}
    .band {{ position:absolute; left:0; right:0; top:{band_top}px; height:{band_h}px; overflow:hidden; background:#ffffff;
      border-top:3px solid var(--brand,#38bdf8); border-bottom:3px solid var(--border,#30363d); z-index:4; }}
    .pan {{ position:absolute; left:0; top:0; width:1368px; transform-origin:0 0; }}
    .pan img {{ display:block; width:1368px; height:auto; }}
    .hl {{ position:absolute; left:{hlx}px; top:{hly}px; width:{hlw}px; height:{hlh}px; border:5px solid var(--accent,#2563eb);
      border-radius:14px; box-shadow:0 0 0 6px rgba(37,99,235,0.18); transform-origin:0 50%; }}
    .chips {{ position:absolute; left:70px; right:70px; top:{band_top+band_h+34}px; display:flex; flex-wrap:wrap; gap:14px; z-index:5; }}
    .chip {{ font-size:30px; font-weight:600; padding:12px 22px; border:2px solid var(--border,#30363d); border-radius:999px;
      background:var(--surface,#161b22); color:var(--fg,#f8fafc); }}
    .chip::before {{ content:""; display:inline-block; width:12px; height:12px; border-radius:50%; background:var(--brand,#38bdf8); margin-right:12px; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div id="{sid}-clip" class="clip" data-start="0" data-duration="{dur}" data-track-index="0" style="position:absolute;inset:0">
      <div id="{sid}-ghost" class="ghost" data-layout-allow-overflow data-layout-allow-occlusion>{num:02d}</div>
      <div id="{sid}-tag" class="tag mono"><b>SISTEMA {num:02d}</b> &nbsp;·&nbsp; {tag}</div>
      <h2 id="{sid}-title" class="title">{words(title)}</h2>
      <div id="{sid}-band" class="band" data-hold="true">
        <div id="{sid}-pan" class="pan" data-layout-allow-overflow>
          <img src="assets/screens/{img}" alt="{tag}" />
          <div id="{sid}-hl" class="hl" data-layout-allow-overflow></div>
        </div>
      </div>
      <div id="{sid}-chips" class="chips">{chip_html}</div>
      <div id="{sid}-wipe" class="wipe" data-layout-ignore></div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      var $ = function (s) {{ return document.querySelector(s); }};
      var S = {scale};
      gsap.set("#{sid}-pan", {{ scale: S * 1.14, x: -({cx} * S * 1.14) , y: -({cy} * S * 1.14) }});
      gsap.set("#{sid}-band", {{ clipPath: "inset(50% 0% 50% 0%)" }});
      gsap.set("#{sid}-title .w", {{ opacity: 0, filter: "blur(10px)", y: 18 }});
      gsap.set("#{sid}-tag", {{ opacity: 0, x: -40 }});
      gsap.set("#{sid}-ghost", {{ opacity: 0, y: 120 }});
      gsap.set("#{sid}-hl", {{ opacity: 0, scaleX: 0.2 }});
      gsap.set("#{sid}-chips .chip", {{ opacity: 0, y: 40, scale: 0.9 }});

      // cortina que descubre la escena (cubre el corte)
      tl.to("#{sid}-wipe", {{ x: 1180, duration: 0.42, ease: "power3.inOut" }}, 0);
      tl.to("#{sid}-band", {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "expo.out" }}, 0.18);
      // paneo + zoom que se asienta sobre la captura real
      tl.to("#{sid}-pan", {{ scale: S, x: -({ex} * S), y: -({ey} * S), duration: {dur - 0.2}, ease: "power2.out" }}, 0.18);
      tl.to("#{sid}-tag", {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 0.3);
      tl.to("#{sid}-title .w", {{ opacity: 1, filter: "blur(0px)", y: 0, duration: 0.35, ease: "power3.out", stagger: 0.07 }}, 0.35);
      tl.to("#{sid}-ghost", {{ opacity: 1, y: 0, duration: 0.7, ease: "expo.out" }}, 0.3);
      tl.to("#{sid}-hl", {{ opacity: 1, scaleX: 1, duration: 0.4, ease: "power4.out" }}, 1.05);
      tl.to("#{sid}-chips .chip", {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.5)", stagger: 0.09 }}, 0.95);

      tl.seek(0);
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{C}/{sid}.html", "w").write(html)


# --------------------------------------------------------------------------------------
# Hook: "8 tipos de software" con 8 chips que se encienden al ritmo
# --------------------------------------------------------------------------------------
def hero():
    html = f"""<!-- compositions/hero.html -->
<template>
  <style>{BASE_CSS}
    .kick {{ position:absolute; left:70px; top:215px; font-size:30px; letter-spacing:0.14em; text-transform:uppercase; color:var(--brand,#38bdf8); }}
    .big {{ position:absolute; left:70px; right:50px; top:275px; font-size:140px; font-weight:800; line-height:0.98; letter-spacing:-0.04em; }}
    .big em {{ font-style:normal; color:var(--brand,#38bdf8); }}
    .case {{ position:absolute; left:70px; top:590px; font-size:50px; font-weight:600; color:#c9d1d9; }}
    .sys {{ position:absolute; left:70px; right:70px; height:290px; border:2px solid var(--border,#30363d); border-radius:24px;
      background:var(--surface,#161b22); padding:34px 40px; overflow:hidden; }}
    .sys .n {{ font-size:30px; letter-spacing:0.14em; text-transform:uppercase; color:#7d8590; }}
    .sys .t {{ margin-top:14px; font-size:68px; font-weight:800; line-height:1.04; letter-spacing:-0.025em; color:#8b949e; }}
    .sys .bar {{ position:absolute; left:0; top:0; bottom:0; width:14px; background:var(--border,#30363d); }}
    .sys.on {{ border-color:var(--brand,#38bdf8); background:#10253a; }}
    .sys.on .n {{ color:var(--brand,#38bdf8); }}
    .sys.on .t {{ color:var(--fg,#f8fafc); }}
    .sys.on .bar {{ background:var(--brand,#38bdf8); }}
  </style>
  <div id="root" data-composition-id="hero" data-width="1080" data-height="1920">
    <div id="hero-clip" class="clip" data-start="0" data-duration="2.5" data-track-index="0" style="position:absolute;inset:0">
      <div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="font-size:600px;left:30px;bottom:-40px">&lt;/&gt;</div>
      <div class="kick mono" id="hero-kick">DAStudio · Desarrollo a medida</div>
      <div class="big" id="hero-big">Software <em>a medida</em></div>
      <div class="case" id="hero-case">Este caso, para una constructora:</div>
      <div class="sys mono" id="hero-s1" style="top:690px;height:250px"><div class="bar"></div><div class="n">Sistema 01</div><div class="t" style="font-family:var(--font-display)">Gestión de Flota</div></div>
      <div class="sys mono" id="hero-s2" style="top:970px;height:360px"><div class="bar"></div><div class="n">Sistema 02</div><div class="t" style="font-family:var(--font-display);font-size:60px">Gestión de Proyectos de Obras Viales y de Arquitectura</div></div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      gsap.set("#hero-big", {{ scale: 1.12, transformOrigin: "0 50%" }});
      gsap.set("#hero-case", {{ x: 50 }});
      tl.to("#hero-big", {{ scale: 1, duration: 0.5, ease: "expo.out" }}, 0);
      tl.to("#hero-case", {{ x: 0, duration: 0.4, ease: "power3.out" }}, 0.12);
      tl.set("#hero-s1", {{ className: "sys mono on" }}, 0.7);
      tl.fromTo("#hero-s1", {{ scale: 0.96 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, 0.7);
      tl.set("#hero-s2", {{ className: "sys mono on" }}, 1.3);
      tl.fromTo("#hero-s2", {{ scale: 0.96 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, 1.3);
      tl.seek(0);
      window.__timelines["hero"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{C}/hero.html", "w").write(html)


# --------------------------------------------------------------------------------------
# Montaje: 4 tipos más, 1.25 s cada uno, tira de UI real con resalte
# --------------------------------------------------------------------------------------
def montage():
    cards = [
        dict(n=5, tag="REUNIONES", word="Reuniones", desc="Agenda, actas y compromisos del comité",
             items=["Agenda", "Actas", "Compromisos"],
             img="inicio.png", crop=(0, 56, 540), hl=(424, 62, 102, 62), strip_h=150),
        dict(n=6, tag="FORMULARIOS", word="Formularios", desc="Encuestas y QR propios, con export CSV",
             items=["Respuestas", "QR propio", "Export CSV"],
             img="clean-protocolos.png", crop=(80, 176, 540), hl=(93, 190, 168, 48), strip_h=150),
        dict(n=7, tag="SERVICIOS", word="Servicios", desc="Catálogo de servicios y responsables",
             items=["Responsables", "Correo", "WhatsApp"],
             img="clean-protocolos.png", crop=(80, 176, 540), hl=(266, 190, 108, 48), strip_h=150),
        dict(n=8, tag="RESPALDO", word="Backups", desc="Copia de todas las colecciones, solo admins",
             items=["Excel", "CSV", "JSON"],
             img="clean-protocolos.png", crop=(300, 176, 540), hl=(618, 190, 196, 48), strip_h=150),
    ]
    dur = 1.25
    HH = {'inicio.png':634, 'clean-protocolos.png':767}
    blocks, js = "", ""
    for i, c in enumerate(cards):
        s = 1080 / c["crop"][2]
        cx, cy, cw = c["crop"]
        hx, hy, hw, hh = c["hl"]
        items = "".join(f'<div class="it" id="m{i}-it{j}"><span></span>{t}</div>' for j, t in enumerate(c["items"]))
        blocks += f"""
      <div class="card" id="m{i}">
        <div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion id="m{i}-g">02</div>
        <div class="word" id="m{i}-w">{c['word']}</div>
        <div class="strip" id="m{i}-s" style="height:{c['strip_h']}px">
          <div class="spin" id="m{i}-p" role="img" aria-label="{c['tag']}" style="height:{HH[c['img']]}px;background:url(assets/screens/{c['img']}) 0 0/1360px auto no-repeat;transform:translate({-cx*s}px,{-cy*s}px) scale({s})">
            <div class="shl" id="m{i}-h" style="left:{hx}px;top:{hy}px;width:{hw}px;height:{hh}px"></div>
          </div>
        </div>
        <div class="list">{items}</div>
      </div>"""
        t0 = i * dur
        js += f"""
      tl.set("#m{i}", {{ opacity: 1 }}, {t0});
      tl.set("#m{i}", {{ opacity: 0 }}, {t0 + dur - 0.001});
      tl.fromTo("#m{i}-wipe", {{ x: 0 }}, {{ x: 1180, duration: 0.3, ease: "power3.inOut" }}, {t0});
      tl.fromTo("#m{i}-w", {{ x: -80, opacity: 0, filter: "blur(10px)" }}, {{ x: 0, opacity: 1, filter: "blur(0px)", duration: 0.32, ease: "expo.out" }}, {t0 + 0.1});
      tl.fromTo("#m{i}-s", {{ opacity: 0, scaleX: 0.7 }}, {{ opacity: 1, scaleX: 1, duration: 0.35, ease: "expo.out" }}, {t0 + 0.12});
      tl.fromTo("#m{i}-h", {{ opacity: 0, scaleX: 0.2 }}, {{ opacity: 1, scaleX: 1, duration: 0.3, ease: "power4.out" }}, {t0 + 0.4});
      tl.fromTo("#m{i}-g", {{ opacity: 0, y: 100 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {t0 + 0.1});
      tl.fromTo("#m{i} .it", {{ opacity: 0, x: -50 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out", stagger: 0.07 }}, {t0 + 0.3});"""
        blocks = blocks.replace(f'<div class="card" id="m{i}">', f'<div class="card" id="m{i}"><div class="wipe" id="m{i}-wipe" data-layout-ignore></div>')
    html = f"""<!-- compositions/montage.html -->
<template>
  <style>{BASE_CSS}
    .card {{ position:absolute; inset:0; opacity:0; }}
    .word {{ position:absolute; left:70px; right:40px; top:270px; font-size:150px; font-weight:800; letter-spacing:-0.035em; line-height:1; z-index:5; }}
    .desc {{ position:absolute; left:70px; right:80px; top:450px; font-size:50px; font-weight:600; color:#c9d1d9; line-height:1.15; z-index:5; }}
    .strip {{ position:absolute; left:0; right:0; top:490px; overflow:hidden; background:#f5f7f9; border-top:3px solid var(--brand,#38bdf8);
      border-bottom:3px solid var(--border,#30363d); z-index:4; transform-origin:0 50%; }}
    .spin {{ position:absolute; left:0; top:0; width:1360px; transform-origin:0 0; }}
        .shl {{ position:absolute; border:4px solid var(--accent,#2563eb); border-radius:12px; box-shadow:0 0 0 5px rgba(37,99,235,0.2); transform-origin:0 50%; }}
    .list {{ position:absolute; left:70px; right:70px; top:700px; z-index:5; }}
    .it {{ font-size:84px; font-weight:700; letter-spacing:-0.02em; padding:30px 0; border-bottom:2px solid var(--border,#30363d); display:flex; align-items:center; }}
    .it span {{ width:24px; height:24px; border-radius:6px; background:var(--brand,#38bdf8); margin-right:28px; flex:0 0 auto; }}
  </style>
  <div id="root" data-composition-id="montage" data-width="1080" data-height="1920">
    <div id="montage-clip" class="clip" data-start="0" data-duration="{dur*4}" data-track-index="0" style="position:absolute;inset:0">{blocks}
      <div class="tag mono" style="z-index:60"><b>SISTEMA 02</b> &nbsp;·&nbsp; CALIDAD DE ATENCIÓN</div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});{js}
      tl.seek(0);
      window.__timelines["montage"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{C}/montage.html", "w").write(html)


# --------------------------------------------------------------------------------------
# Cierre: frase de remate + marca DAStudio
# --------------------------------------------------------------------------------------
def outro():
    html = f"""<!-- compositions/outro.html -->
<template>
  <style>{BASE_CSS}
    .l1 {{ position:absolute; left:70px; right:70px; top:330px; font-size:112px; font-weight:800; letter-spacing:-0.03em; line-height:1.02; }}
    .l2 {{ position:absolute; left:70px; right:70px; top:620px; font-size:112px; font-weight:800; letter-spacing:-0.03em; line-height:1.02; color:var(--brand,#38bdf8); }}
    .brand {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; padding-bottom:120px; }}
    .brand img {{ width:180px; height:auto; display:block; }}
    .word {{ margin-top:34px; font-size:96px; font-weight:800; letter-spacing:-0.02em; }}
    .word span {{ color:var(--brand,#38bdf8); }}
    .tagl {{ margin-top:22px; font-size:40px; font-weight:500; color:#9aa4b2; text-align:center; padding:0 70px; }}
    .cta {{ margin-top:52px; font-size:30px; letter-spacing:0.1em; text-transform:uppercase; color:var(--brand,#38bdf8);
      border:2px solid var(--border,#30363d); border-radius:999px; padding:18px 36px; }}
    .kinds {{ position:absolute; left:70px; right:70px; top:900px; display:flex; flex-wrap:wrap; gap:16px; }}
    .k {{ font-size:34px; font-weight:600; padding:16px 28px; border:2px solid var(--brand,#38bdf8); border-radius:999px; background:#10253a; }}
    .rule {{ position:absolute; left:0; right:0; bottom:0; height:4px; background:linear-gradient(90deg,transparent,var(--brand,#38bdf8),transparent); }}
  </style>
  <div id="root" data-composition-id="outro" data-width="1080" data-height="1920">
    <div id="outro-clip" class="clip" data-start="0" data-duration="5.5" data-track-index="0" style="position:absolute;inset:0">
      <div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion id="o-ghost" style="font-size:560px;bottom:-30px">∞</div>
      <div class="l1" id="o-l1">{words('Hoy, una constructora.')}</div>
      <div class="l2" id="o-l2">{words('Mañana, tu herramienta.')}</div>
      <div class="kinds" id="o-kinds">
        <span class="k mono">Sistemas de gestión</span><span class="k mono">E-commerce</span>
        <span class="k mono">Apps clínicas</span><span class="k mono">Sitios corporativos</span>
      </div>
      <div class="brand" id="o-brand">
        <img id="o-mark" src="assets/dastudio-mark.png" alt="DAStudio" />
        <div class="word" id="o-word">DA<span>Studio</span></div>
        <div class="tagl" id="o-tag">Desarrollo Web &amp; Software a Medida</div>
        <div class="cta mono" id="o-cta" data-hold="true">Más proyectos en el portfolio</div>
      </div>
      <div class="rule" data-layout-ignore></div>
      <div class="wipe" id="o-wipe" data-layout-ignore></div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      gsap.set("#o-brand", {{ opacity: 0 }});
      gsap.set("#o-l1 .w, #o-l2 .w", {{ opacity: 0, filter: "blur(12px)", y: 24 }});
      gsap.set("#o-ghost", {{ opacity: 0, scale: 0.9 }});
      gsap.set("#o-kinds .k", {{ opacity: 0, y: 30 }});
      tl.to("#o-wipe", {{ x: 1180, duration: 0.4, ease: "power3.inOut" }}, 0);
      tl.to("#o-ghost", {{ opacity: 1, scale: 1, duration: 0.8, ease: "expo.out" }}, 0.3);
      tl.to("#o-l1 .w", {{ opacity: 1, filter: "blur(0px)", y: 0, duration: 0.35, ease: "power3.out", stagger: 0.09 }}, 0.35);
      tl.to("#o-l2 .w", {{ opacity: 1, filter: "blur(0px)", y: 0, duration: 0.35, ease: "power3.out", stagger: 0.09 }}, 0.75);
      tl.to("#o-kinds .k", {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.4)", stagger: 0.12 }}, 1.0);
      // salida de la frase y entrada de la marca
      tl.to(["#o-l1", "#o-l2", "#o-ghost", "#o-kinds"], {{ opacity: 0, filter: "blur(10px)", duration: 0.2, ease: "power2.in" }}, 2.15);
      tl.fromTo("#o-brand", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, 2.35);
      tl.fromTo("#o-mark", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, 2.35);
      tl.fromTo("#o-word", {{ opacity: 0, y: 20, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }}, 2.55);
      tl.fromTo("#o-tag", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, 2.8);
      tl.fromTo("#o-cta", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, 3.05);
      tl.seek(0);
      window.__timelines["outro"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{C}/outro.html", "w").write(html)


hero()
feature("f-inicio", 1, 2, "Gestión de flota", "Toda la flota en un solo panel",
        "inicio.png", crop=(0, 0), scale=1.2, pan_to=(468, 0), hl=(352, 125, 313, 327),
        chips=["75 unidades", "43 operadores", "Alertas al día"], dur=2.5)
feature("f-unidades", 1, 2, "Gestión de flota", "75 unidades, cada una con su ficha",
        "unidades.png", crop=(0, 0), scale=1.2, pan_to=(468, 20), hl=(36, 98, 1120, 240),
        chips=["47 vehículos", "28 máquinas", "Por tipo"], dur=2.5)
feature("f-alertas", 1, 2, "Gestión de flota", "Alertas por fecha, horas o kilómetros",
        "alertas.png", crop=(0, 0), scale=1.2, pan_to=(468, 0), hl=(448, 196, 330, 150),
        chips=["VTV", "Service por hs", "Service por km"], dur=3.0)
feature("f-fases", 2, 2, "Proyectos de obras", "Gasto de cada obra, repartido por fases",
        "fases.png", crop=(0, 30), scale=1.2, pan_to=(110, 30), hl=(40, 215, 340, 340),
        chips=["Obras viales", "Arquitectura", "Por fase"], dur=3.0)
feature("f-materiales", 2, 2, "Proyectos de obras", "Materiales y servicios de cada obra",
        "materiales.png", crop=(0, 0), scale=1.2, pan_to=(468, 0), hl=(730, 62, 100, 580),
        chips=["Productos", "Servicios", "Costo por ítem"], dur=3.0)
feature("f-resultados", 2, 2, "Proyectos de obras", "Presupuestado vs. real, en cada obra",
        "resultados.png", crop=(0, 0), scale=1.2, pan_to=(120, 0), hl=(18, 148, 1316, 92),
        chips=["Rentabilidad", "Facturado", "Con o sin IVA"], dur=3.0)
outro()

# --------------------------------------------------------------------------------------
# Raíz
# --------------------------------------------------------------------------------------
scenes = [("hero", 0, 2.5), ("f-inicio", 2.5, 2.5), ("f-unidades", 5, 2.5), ("f-alertas", 7.5, 3),
          ("f-fases", 10.5, 3), ("f-materiales", 13.5, 3), ("f-resultados", 16.5, 3), ("outro", 19.5, 5.5)]
hosts = "".join(f"""
      <div id="{i}" data-composition-id="{i}" data-composition-src="compositions/{i}.html"
        data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics"
        data-width="1080" data-height="1920"></div>
""" for i, s, d in scenes)
idx = open(SRC_INDEX).read()
k = idx.index('id="hero"')
head = idx[: idx.rindex("<div", 0, k)]
tail = f"""{hosts}
      <audio id="bgm" class="clip" data-start="0" data-duration="25" data-media-start="10" data-volume="1"
        data-fade-in="0.2" data-fade-out="1.6" data-track-index="0" src="assets/bgm.wav"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
head = head.replace('data-duration="30"', 'data-duration="25"')
open(P + "/index.html", "w").write(head + tail.lstrip("\n"))
print("ok")
