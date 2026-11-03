#!/usr/bin/env python3
"""Plantilla del reel MEZCLA (varios proyectos), aprobado: proyectos/portfolio-mix v1 (30 s, 5 proyectos).

Ver SKILL.md §8. Copiala al scratchpad (no la ejecutes desde el skill) y editá:
  - P (carpeta nueva del reel) y SRC_INDEX (index.html de otro reel, de donde sale la cabecera con las fuentes).
  - hero(): las filas de la lista (un rubro por proyecto) y "N proyectos reales, N rubros:".
  - Las llamadas feature2(...) del final: una por proyecto, con 2 tomas (shots) cada una.
      shots[i] = dict(img, w=ancho natural del PNG, S=zoom, crop=(x,y) arranque, pan_to=(x,y) fin, hl=(x,y,w,h) recuadro)
      Escritorio: S=1.2, banda 720 px. Móvil (PNG de ~1080 de ancho): S=1.0, band_top=455, band_h=820 y el paneo es vertical.
  - outro(): frase de remate. scenes: hero 2.5 s + N escenas de 4.5 s + outro 5 s (todo múltiplo de 0.5 a 120 BPM).
  - El audio: data-media-start="5" para 30 s (la pista dura 35 s; 5 s es compás exacto y el pico cae en el cierre).
"""
import os

P = "/home/diego/Soft/repos/portfolio/proyectos/portfolio-mix"
SRC_INDEX = "/home/diego/Soft/repos/portfolio/proyectos/calidad-carrillo/index.html"
C = P + "/compositions"
os.makedirs(C, exist_ok=True)
for f in os.listdir(C):
    os.remove(os.path.join(C, f))

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


def feature2(sid, idx, tag, title, shots, chips, dur=4.5, band_top=480, band_h=720):
    """shots: lista de dict(img, w, S, crop, pan_to, hl). Se reparten la duración; entre tomas hay un corte con cortina."""
    n = len(shots)
    t_start = 0.18
    t_end = dur - 0.1
    seg = (t_end - t_start) / n
    chip_html = "".join(f'<span class="chip mono">{c}</span>' for c in chips)
    shot_html, js = "", ""
    for i, s in enumerate(shots):
        t0 = t_start + i * seg
        t1 = t0 + seg
        cx, cy = s["crop"]
        ex, ey = s["pan_to"]
        S = s["S"]
        hl = s.get("hl")
        hl_html = ""
        if hl:
            hl_html = (f'<div id="{sid}-h{i}" class="hl" data-layout-allow-overflow '
                       f'style="left:{hl[0]}px;top:{hl[1]}px;width:{hl[2]}px;height:{hl[3]}px"></div>')
        shot_html += f"""
        <div id="{sid}-s{i}" class="shot">
          <div id="{sid}-p{i}" class="pan" data-layout-allow-overflow style="width:{s['w']}px">
            <img src="assets/screens/{s['img']}" alt="{tag}" style="width:{s['w']}px" />
            {hl_html}
          </div>
        </div>"""
        js += f"""
      gsap.set("#{sid}-p{i}", {{ scale: {S*1.12:.4f}, x: {-cx*S*1.12:.1f}, y: {-cy*S*1.12:.1f} }});"""
        if i > 0:
            js += f"""
      gsap.set("#{sid}-s{i}", {{ opacity: 0 }});
      tl.set("#{sid}-s{i-1}", {{ opacity: 0 }}, {t0:.3f});
      tl.set("#{sid}-s{i}", {{ opacity: 1 }}, {t0:.3f});
      tl.fromTo("#{sid}-bw", {{ x: -1100 }}, {{ x: 1100, duration: 0.5, ease: "power3.inOut" }}, {t0 - 0.25:.3f});"""
        js += f"""
      tl.to("#{sid}-p{i}", {{ scale: {S}, x: {-ex*S:.1f}, y: {-ey*S:.1f}, duration: {seg - 0.05:.3f}, ease: "power2.out" }}, {t0:.3f});"""
        if hl:
            js += f"""
      gsap.set("#{sid}-h{i}", {{ opacity: 0, scaleX: 0.2 }});
      tl.to("#{sid}-h{i}", {{ opacity: 1, scaleX: 1, duration: 0.4, ease: "power4.out" }}, {t0 + 0.7:.3f});"""
    html = f"""<!-- compositions/{sid}.html -->
<template>
  <style>{BASE_CSS}
    .title {{ position:absolute; left:70px; right:70px; top:255px; font-size:88px; font-weight:800; line-height:1.04;
      letter-spacing:-0.025em; z-index:5; }}
    .band {{ position:absolute; left:0; right:0; top:{band_top}px; height:{band_h}px; overflow:hidden; background:#ffffff;
      border-top:3px solid var(--brand,#38bdf8); border-bottom:3px solid var(--border,#30363d); z-index:4; }}
    .shot {{ position:absolute; inset:0; overflow:hidden; }}
    .pan {{ position:absolute; left:0; top:0; transform-origin:0 0; }}
    .pan img {{ display:block; height:auto; }}
    .hl {{ position:absolute; border:5px solid var(--accent,#2563eb); border-radius:14px; box-shadow:0 0 0 6px rgba(37,99,235,0.18); transform-origin:0 50%; }}
    .bw {{ position:absolute; top:0; bottom:0; left:0; width:1100px; background:var(--surface,#161b22); z-index:10; transform:none; }}
    .bw::after {{ content:""; position:absolute; top:0; bottom:0; right:0; width:14px; background:var(--brand,#38bdf8); }}
    .chips {{ position:absolute; left:70px; right:70px; top:{band_top+band_h+30}px; display:flex; flex-wrap:wrap; gap:14px; z-index:5; }}
    .chip {{ font-size:30px; font-weight:600; padding:12px 22px; border:2px solid var(--border,#30363d); border-radius:999px;
      background:var(--surface,#161b22); color:var(--fg,#f8fafc); }}
    .chip::before {{ content:""; display:inline-block; width:12px; height:12px; border-radius:50%; background:var(--brand,#38bdf8); margin-right:12px; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div id="{sid}-clip" class="clip" data-start="0" data-duration="{dur}" data-track-index="0" style="position:absolute;inset:0">
      <div id="{sid}-ghost" class="ghost" data-layout-allow-overflow data-layout-allow-occlusion>{idx:02d}</div>
      <div id="{sid}-tag" class="tag mono"><b>{idx:02d} / 05</b> &nbsp;·&nbsp; {tag}</div>
      <h2 id="{sid}-title" class="title">{words(title)}</h2>
      <div id="{sid}-band" class="band" data-hold="true">{shot_html}
        <div id="{sid}-bw" class="bw" data-layout-ignore></div>
      </div>
      <div id="{sid}-chips" class="chips">{chip_html}</div>
      <div id="{sid}-wipe" class="wipe" data-layout-ignore></div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      gsap.set("#{sid}-bw", {{ x: -1100 }});
      gsap.set("#{sid}-band", {{ clipPath: "inset(50% 0% 50% 0%)" }});
      gsap.set("#{sid}-title .w", {{ opacity: 0, filter: "blur(10px)", y: 18 }});
      gsap.set("#{sid}-tag", {{ opacity: 0, x: -40 }});
      gsap.set("#{sid}-ghost", {{ opacity: 0, y: 120 }});
      gsap.set("#{sid}-chips .chip", {{ opacity: 0, y: 40, scale: 0.9 }});
      tl.to("#{sid}-wipe", {{ x: 1180, duration: 0.42, ease: "power3.inOut" }}, 0);
      tl.to("#{sid}-band", {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "expo.out" }}, 0.18);{js}
      tl.to("#{sid}-tag", {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 0.3);
      tl.to("#{sid}-title .w", {{ opacity: 1, filter: "blur(0px)", y: 0, duration: 0.35, ease: "power3.out", stagger: 0.07 }}, 0.35);
      tl.to("#{sid}-ghost", {{ opacity: 1, y: 0, duration: 0.7, ease: "expo.out" }}, 0.3);
      tl.to("#{sid}-chips .chip", {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.5)", stagger: 0.09 }}, 0.95);
      tl.seek(0);
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{C}/{sid}.html", "w").write(html)


def hero():
    rows = ["Gestión de flota y obras", "Gestión hospitalaria", "Sitio corporativo",
            "App médica de guardia", "App móvil neonatal"]
    cells = "".join(f'<div class="row" id="hero-r{i}"><i class="mono">{i+1:02d}</i>{r}</div>' for i, r in enumerate(rows))
    html = f"""<!-- compositions/hero.html -->
<template>
  <style>{BASE_CSS}
    .kick {{ position:absolute; left:70px; top:215px; font-size:30px; letter-spacing:0.14em; text-transform:uppercase; color:var(--brand,#38bdf8); }}
    .big {{ position:absolute; left:70px; right:50px; top:275px; font-size:140px; font-weight:800; line-height:0.98; letter-spacing:-0.04em; }}
    .big em {{ font-style:normal; color:var(--brand,#38bdf8); }}
    .case {{ position:absolute; left:70px; top:590px; font-size:50px; font-weight:600; color:#c9d1d9; }}
    .list {{ position:absolute; left:70px; right:70px; top:690px; display:flex; flex-direction:column; gap:14px; }}
    .row {{ font-size:50px; font-weight:700; letter-spacing:-0.02em; padding:24px 30px; border:2px solid var(--border,#30363d); border-radius:18px;
      background:var(--surface,#161b22); color:#8b949e; display:flex; align-items:center; }}
    .row i {{ font-style:normal; font-size:30px; color:#7d8590; margin-right:26px; width:52px; }}
    .row.on {{ border-color:var(--brand,#38bdf8); background:#10253a; color:var(--fg,#f8fafc); }}
    .row.on i {{ color:var(--brand,#38bdf8); }}
  </style>
  <div id="root" data-composition-id="hero" data-width="1080" data-height="1920">
    <div id="hero-clip" class="clip" data-start="0" data-duration="2.5" data-track-index="0" style="position:absolute;inset:0">
      <div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="font-size:600px;left:30px;bottom:-40px">&lt;/&gt;</div>
      <div class="kick mono" id="hero-kick">DAStudio · Desarrollo a medida</div>
      <div class="big" id="hero-big">Software <em>a medida</em></div>
      <div class="case" id="hero-case">5 proyectos reales, 5 rubros:</div>
      <div class="list" id="hero-list">{cells}</div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      gsap.set("#hero-big", {{ scale: 1.12, transformOrigin: "0 50%" }});
      gsap.set("#hero-case", {{ x: 50 }});
      tl.to("#hero-big", {{ scale: 1, duration: 0.5, ease: "expo.out" }}, 0);
      tl.to("#hero-case", {{ x: 0, duration: 0.4, ease: "power3.out" }}, 0.12);
      for (var i = 0; i < 5; i++) {{
        tl.set("#hero-r" + i, {{ className: "row on" }}, 0.5 + i * 0.3);
        tl.fromTo("#hero-r" + i, {{ scale: 0.96 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, 0.5 + i * 0.3);
      }}
      tl.seek(0);
      window.__timelines["hero"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{C}/hero.html", "w").write(html)


def outro():
    html = f"""<!-- compositions/outro.html -->
<template>
  <style>{BASE_CSS}
    .l1 {{ position:absolute; left:70px; right:70px; top:330px; font-size:112px; font-weight:800; letter-spacing:-0.03em; line-height:1.02; }}
    .l2 {{ position:absolute; left:70px; right:70px; top:470px; font-size:112px; font-weight:800; letter-spacing:-0.03em; line-height:1.02; color:var(--brand,#38bdf8); }}
    .kinds {{ position:absolute; left:70px; right:70px; top:900px; display:flex; flex-wrap:wrap; gap:16px; }}
    .k {{ font-size:34px; font-weight:600; padding:16px 28px; border:2px solid var(--brand,#38bdf8); border-radius:999px; background:#10253a; }}
    .brand {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; padding-bottom:120px; }}
    .brand img {{ width:180px; height:auto; display:block; }}
    .word {{ margin-top:34px; font-size:96px; font-weight:800; letter-spacing:-0.02em; }}
    .word span {{ color:var(--brand,#38bdf8); }}
    .tagl {{ margin-top:22px; font-size:40px; font-weight:500; color:#9aa4b2; text-align:center; padding:0 70px; }}
    .cta {{ margin-top:52px; font-size:30px; letter-spacing:0.1em; text-transform:uppercase; color:var(--brand,#38bdf8);
      border:2px solid var(--border,#30363d); border-radius:999px; padding:18px 36px; }}
    .rule {{ position:absolute; left:0; right:0; bottom:0; height:4px; background:linear-gradient(90deg,transparent,var(--brand,#38bdf8),transparent); }}
  </style>
  <div id="root" data-composition-id="outro" data-width="1080" data-height="1920">
    <div id="outro-clip" class="clip" data-start="0" data-duration="5" data-track-index="0" style="position:absolute;inset:0">
      <div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion id="o-ghost" style="font-size:560px;bottom:-30px">∞</div>
      <div class="l1" id="o-l1">{words('Cinco rubros.')}</div>
      <div class="l2" id="o-l2">{words('Tu herramienta.')}</div>
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
      tl.to("#o-l2 .w", {{ opacity: 1, filter: "blur(0px)", y: 0, duration: 0.35, ease: "power3.out", stagger: 0.09 }}, 0.7);
      tl.to("#o-kinds .k", {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.4)", stagger: 0.12 }}, 1.0);
      tl.to(["#o-l1", "#o-l2", "#o-ghost", "#o-kinds"], {{ opacity: 0, filter: "blur(10px)", duration: 0.2, ease: "power2.in" }}, 1.95);
      tl.fromTo("#o-brand", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, 2.1);
      tl.fromTo("#o-mark", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, 2.1);
      tl.fromTo("#o-word", {{ opacity: 0, y: 20, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }}, 2.3);
      tl.fromTo("#o-tag", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, 2.55);
      tl.fromTo("#o-cta", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, 2.8);
      tl.seek(0);
      window.__timelines["outro"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{C}/outro.html", "w").write(html)


hero()
# 1 Flota y obras
feature2("p-flota", 1, "Gestión empresarial", "Flota y obras en tiempo real", [
    dict(img="flota-unidades.png", w=1368, S=1.2, crop=(0, 0), pan_to=(468, 20), hl=(36, 98, 1120, 240)),
    dict(img="flota-fases.png", w=1368, S=1.2, crop=(0, 30), pan_to=(110, 30), hl=(40, 215, 340, 340)),
], ["75 unidades", "Alertas de service", "Obras por fase"])
# 2 Calidad Carrillo
feature2("p-calidad", 2, "Gestión hospitalaria", "Eventos adversos con QR e indicadores", [
    dict(img="cc-qr.png", w=1360, S=1.2, crop=(320, 210), pan_to=(330, 290), hl=(473, 362, 414, 405)),
    dict(img="cc-indicadores.png", w=1360, S=1.2, crop=(90, 141), pan_to=(330, 141), hl=(885, 515, 383, 252)),
], ["Reportes anónimos", "Tablero Kanban", "Indicadores"])
# 3 Landing JL
feature2("p-landing", 3, "Sitio corporativo", "Web institucional para licitaciones", [
    dict(img="jl-1.png", w=1360, S=1.2, crop=(0, 0), pan_to=(300, 0), hl=(312, 507, 172, 59)),
    dict(img="jl-2.png", w=1360, S=1.2, crop=(0, 60), pan_to=(400, 60), hl=(72, 327, 377, 211)),
], ["Mobile first", "SEO B2B", "Carga rápida"])
# 4 EGPediatría
feature2("p-egp", 4, "App médica · PWA", "Dosis de emergencia en segundos", [
    dict(img="eg-1.png", w=1360, S=1.2, crop=(0, 0), pan_to=(300, 0), hl=(350, 318, 311, 110)),
    dict(img="eg-2.png", w=1360, S=1.2, crop=(300, 0), pan_to=(380, 0), hl=(370, 515, 440, 125)),
], ["Por peso del paciente", "SAP / PALS", "Funciona offline"])
# 5 NeoCalcu (móvil)
feature2("p-neo", 5, "App móvil · PWA", "Dosis neonatales por peso", [
    dict(img="nc-lista.png", w=1080, S=1.0, crop=(0, 0), pan_to=(0, 300), hl=(0, 246, 1080, 110)),
    dict(img="nc-dosis.png", w=1080, S=1.0, crop=(0, 880), pan_to=(0, 1240), hl=(82, 1382, 916, 258)),
], ["224 medicamentos", "Cálculo por peso", "Funciona offline"], band_top=455, band_h=820)
outro()

scenes = [("hero", 0, 2.5), ("p-flota", 2.5, 4.5), ("p-calidad", 7, 4.5), ("p-landing", 11.5, 4.5),
          ("p-egp", 16, 4.5), ("p-neo", 20.5, 4.5), ("outro", 25, 5)]
hosts = "".join(f"""
      <div id="{i}" data-composition-id="{i}" data-composition-src="compositions/{i}.html"
        data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics"
        data-width="1080" data-height="1920"></div>
""" for i, s, d in scenes)
idx = open(SRC_INDEX).read()
k = idx.index('id="hero"')
head = idx[: idx.rindex("<div", 0, k)]
tail = f"""{hosts}
      <audio id="bgm" class="clip" data-start="0" data-duration="30" data-media-start="5" data-volume="1"
        data-fade-in="0.2" data-fade-out="1.4" data-track-index="0" src="assets/bgm.wav"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
head = head.replace('data-duration="25"', 'data-duration="30"')
open(P + "/index.html", "w").write(head + tail.lstrip("\n"))
print("ok")
