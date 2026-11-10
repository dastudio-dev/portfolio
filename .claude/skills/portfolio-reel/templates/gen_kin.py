#!/usr/bin/env python3
"""Plantilla del reel SIN VOZ de texto cinético, aprobado: proyectos/sistema-a-medida v2 (20 s, música).

Ver SKILL.md §9. Copiala al scratchpad (no la ejecutes desde el skill) y editá:
  - P (carpeta nueva del reel) y SRC_INDEX (index.html de otro reel: de ahí sale la cabecera con las fuentes).
  - words(): marcadores en los títulos: "*palabra" = celeste, "~palabra~" = gris con tachado animado.
  - hero(): la pregunta de gancho y la bajada.
  - Las llamadas feature2(...) del final: UNA toma por escena (2,5 s), con
      shots[0] = dict(img, w, S, crop, pan_to, hl)   (igual que gen_mix.py)
      chips    = 3 palabras cortas (el cursor les hace clic de a uno y cada una queda con tilde)
      count    = (valor, etiqueta): contador que sube con una cifra REAL visible en esa captura (nunca inventada)
      Móvil: band_top=455, band_h=820.
    La zona de abajo (chips + contador + barra de progreso de 5 segmentos) reemplaza al número fantasma:
    se calcula sola desde band_top/band_h. Dejá la barra de progreso en 5 segmentos = 5 escenas.
  - outro(): frase de remate y CTA. scenes: hero 2,5 s + N escenas de 2,5 s + outro 5 s (múltiplos de 0,5 a 120 BPM).
  - Audio: data-media-start="15" para 20 s (la pista dura 35 s; 15 s cae en compás y el pico llega al cierre).
"""
import os

P = "/home/diego/Soft/repos/portfolio/proyectos/sistema-a-medida"
SRC_INDEX = "/home/diego/Soft/repos/portfolio/proyectos/portfolio-mix/index.html"
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
    out = []
    for w in text.split():
        if w.startswith("*"):
            out.append(f'<span class="{cls} hi" style="display:inline-block">{w.strip("*")}</span>')
        elif w.startswith("~"):
            core, _, tail = w[1:].partition("~")
            out.append(f'<span class="{cls} st" style="display:inline-block;position:relative">{core}<i class="strike" data-layout-ignore></i>{tail}</span>')
        else:
            out.append(f'<span class="{cls}" style="display:inline-block">{w}</span>')
    return " ".join(out)


def feature2(sid, idx, tag, title, shots, chips, dur=4.5, band_top=480, band_h=720, count=None):
    """shots: lista de dict(img, w, S, crop, pan_to, hl). Se reparten la duración; entre tomas hay un corte con cortina."""
    n = len(shots)
    t_start = 0.18
    t_end = dur - 0.1
    seg = (t_end - t_start) / n
    chip_html = "".join(f'<span class="chip mono" id="{sid}-c{i}">{c}</span>' for i, c in enumerate(chips))
    chips_top = band_top + band_h + 30
    cnt_top = chips_top + 95
    prog_top = cnt_top + 170
    cx_list, x = [], 70
    for c in chips:
        w = 18 * len(c) + 72
        cx_list.append(x + w * 0.45)
        x += w + 14
    cy = chips_top + 34
    cnt_val, cnt_label = count if count else (0, "")
    seg_html = "".join(f'<i class="seg"><b id="{sid}-f{k}"></b></i>' for k in range(5))
    seg_js = ""
    for k in range(5):
        if k < idx - 1:
            seg_js += f'\n      gsap.set("#{sid}-f{k}", {{ scaleX: 1 }});'
        elif k == idx - 1:
            seg_js += (f'\n      gsap.set("#{sid}-f{k}", {{ scaleX: 0 }});'
                       f'\n      tl.to("#{sid}-f{k}", {{ scaleX: 1, duration: {dur - 0.2:.2f}, ease: "none" }}, 0.1);')
        else:
            seg_js += f'\n      gsap.set("#{sid}-f{k}", {{ scaleX: 0 }});'
    click_js, t = "", 1.5
    for i, cxx in enumerate(cx_list):
        click_js += (f'\n      tl.to("#{sid}-cur", {{ x: {cxx:.0f}, y: {cy + 18:.0f}, duration: 0.22, ease: "power2.inOut" }}, {t - 0.22:.2f});'
                     f'\n      tl.to("#{sid}-cur", {{ scale: 0.82, duration: 0.07, yoyo: true, repeat: 1 }}, {t:.2f});'
                     f'\n      tl.set("#{sid}-c{i}", {{ className: "chip mono on" }}, {t + 0.05:.2f});'
                     f'\n      tl.fromTo("#{sid}-c{i}", {{ scale: 0.93 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2.5)", overwrite: "auto" }}, {t + 0.05:.2f});')
        t += 0.3
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
    strike_js = ""
    if "~" in title:
        strike_js = f"""
      gsap.set("#{sid}-title .strike", {{ scaleX: 0 }});
      tl.to("#{sid}-title .strike", {{ scaleX: 1, duration: 0.3, ease: "power4.out" }}, 1.0);"""
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
    .title .hi {{ color:var(--brand,#38bdf8); }}
    .title .st {{ color:#8b949e; }}
    .strike {{ position:absolute; left:-6px; right:-6px; top:54%; height:9px; background:var(--brand,#38bdf8); border-radius:5px; transform-origin:0 50%; }}
    .cnt {{ position:absolute; left:70px; right:70px; top:{cnt_top}px; display:flex; align-items:baseline; gap:22px; z-index:5; }}
    .cnt b {{ font-size:140px; font-weight:800; letter-spacing:-0.04em; line-height:1; color:var(--brand,#38bdf8); font-variant-numeric:tabular-nums; }}
    .cnt span {{ font-size:36px; letter-spacing:0.08em; text-transform:uppercase; color:#c9d1d9; }}
    .prog {{ position:absolute; left:70px; right:70px; top:{prog_top}px; display:flex; gap:12px; z-index:5; }}
    .seg {{ flex:1; height:10px; border-radius:5px; background:var(--border,#30363d); overflow:hidden; display:block; }}
    .seg b {{ display:block; height:100%; width:100%; background:var(--brand,#38bdf8); transform-origin:0 50%; }}
    .cur {{ position:absolute; left:0; top:0; width:46px; height:46px; z-index:9; }}
    .chip.on {{ border-color:var(--brand,#38bdf8); background:#10253a; }}
    .chip.on::before {{ content:"✓"; width:auto; height:auto; background:none; border-radius:0; color:var(--brand,#38bdf8); font-size:26px; line-height:1; }}
    .chips {{ position:absolute; left:70px; right:70px; top:{band_top+band_h+30}px; display:flex; flex-wrap:wrap; gap:14px; z-index:5; }}
    .chip {{ font-size:30px; font-weight:600; padding:12px 22px; border:2px solid var(--border,#30363d); border-radius:999px;
      background:var(--surface,#161b22); color:var(--fg,#f8fafc); }}
    .chip::before {{ content:""; display:inline-block; width:12px; height:12px; border-radius:50%; background:#6e7681; margin-right:12px; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div id="{sid}-clip" class="clip" data-start="0" data-duration="{dur}" data-track-index="0" style="position:absolute;inset:0">
      <div id="{sid}-tag" class="tag mono"><b>{idx:02d} / 05</b> &nbsp;·&nbsp; {tag}</div>
      <h2 id="{sid}-title" class="title">{words(title)}</h2>
      <div id="{sid}-band" class="band" data-hold="true">{shot_html}
        <div id="{sid}-bw" class="bw" data-layout-ignore></div>
      </div>
      <div id="{sid}-chips" class="chips">{chip_html}</div>
      <div id="{sid}-cnt" class="cnt"><b id="{sid}-n" class="mono">0</b><span class="mono">{cnt_label}</span></div>
      <div id="{sid}-prog" class="prog" data-layout-ignore>{seg_html}</div>
      <svg id="{sid}-cur" class="cur" data-layout-ignore viewBox="0 0 24 24"><path d="M4 2 L4 19 L8.6 14.6 L11.6 21.4 L14.4 20.2 L11.4 13.6 L18 13.4 Z" fill="#ffffff" stroke="#0d1117" stroke-width="1.4" stroke-linejoin="round"/></svg>
      <div id="{sid}-wipe" class="wipe" data-layout-ignore></div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      gsap.set("#{sid}-bw", {{ x: -1100 }});
      gsap.set("#{sid}-band", {{ clipPath: "inset(50% 0% 50% 0%)" }});
      gsap.set("#{sid}-title .w", {{ opacity: 0, filter: "blur(10px)", y: 40, scale: 0.8 }});
      gsap.set("#{sid}-tag", {{ opacity: 0, x: -40 }});
      gsap.set("#{sid}-cnt", {{ opacity: 0, y: 30 }});
      gsap.set("#{sid}-cur", {{ x: 900, y: {cy + 140:.0f}, opacity: 0 }});
      var cnt = {{ v: 0 }};
      var nEl = document.getElementById("{sid}-n");
      tl.to("#{sid}-cnt", {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, 0.45);
      tl.to(cnt, {{ v: {cnt_val}, duration: 1.4, ease: "power2.out", onUpdate: function () {{ nEl.textContent = Math.round(cnt.v); }} }}, 0.5);
      tl.to("#{sid}-cur", {{ opacity: 1, duration: 0.15 }}, 0.85);
      tl.to("#{sid}-cur", {{ opacity: 0, duration: 0.2 }}, {dur - 0.25:.2f});{click_js}{seg_js}
      gsap.set("#{sid}-chips .chip", {{ opacity: 0, y: 40, scale: 0.9 }});
      tl.to("#{sid}-wipe", {{ x: 1180, duration: 0.42, ease: "power3.inOut" }}, 0);
      tl.to("#{sid}-band", {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "expo.out" }}, 0.18);{js}
      tl.to("#{sid}-tag", {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 0.3);
      tl.to("#{sid}-title .w", {{ opacity: 1, filter: "blur(0px)", y: 0, scale: 1, duration: 0.35, ease: "back.out(1.6)", stagger: 0.09 }}, 0.3);
{strike_js}
      tl.to("#{sid}-chips .chip", {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.5)", stagger: 0.09 }}, 0.95);
      tl.seek(0);
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{C}/{sid}.html", "w").write(html)


def hero():
    html = f"""<!-- compositions/hero.html -->
<template>
  <style>{BASE_CSS}
    .kick {{ position:absolute; left:70px; top:215px; font-size:30px; letter-spacing:0.14em; text-transform:uppercase; color:var(--brand,#38bdf8); }}
    .q {{ position:absolute; left:70px; right:50px; top:420px; font-size:150px; font-weight:800; line-height:1.0; letter-spacing:-0.04em; text-transform:uppercase; }}
    .q .hi {{ color:var(--brand,#38bdf8); }}
    .sub {{ position:absolute; left:70px; right:70px; top:1130px; font-size:50px; font-weight:600; color:#c9d1d9; }}
  </style>
  <div id="root" data-composition-id="hero" data-width="1080" data-height="1920">
    <div id="hero-clip" class="clip" data-start="0" data-duration="2.5" data-track-index="0" style="position:absolute;inset:0">
      <div class="ghost" data-layout-allow-overflow data-layout-allow-occlusion style="font-size:600px;left:30px;bottom:-40px">&lt;/&gt;</div>
      <div class="kick mono" id="hero-kick">DAStudio · Desarrollo a medida</div>
      <div class="q" id="hero-q">{words('¿Para qué tener un sistema *a *medida?')}</div>
      <div class="sub" id="hero-sub">Tu operación, en una sola pantalla.</div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      gsap.set("#hero-q .w", {{ y: 36 }});
      gsap.set("#hero-sub", {{ opacity: 0, y: 30 }});
      tl.to("#hero-q .w", {{ y: 0, duration: 0.45, ease: "expo.out", stagger: 0.05 }}, 0);
      tl.to("#hero-sub", {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, 0.15);
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
      <div class="l1" id="o-l1">{words('Escribinos y')}</div>
      <div class="l2" id="o-l2">{words('contanos *tu *proceso')}</div>
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
feature2("k1", 1, "Operación", "Tu operación en *una *sola *pantalla", [
    dict(img="flota-unidades.png", w=1368, S=1.2, crop=(0, 0), pan_to=(468, 20), hl=(36, 98, 1120, 240)),
], ["Unidades", "Obras", "Alertas"], dur=2.5, count=(75, "unidades"))
feature2("k2", 2, "Control", "Stock, costos, flota y *operadores", [
    dict(img="flota-fases.png", w=1368, S=1.2, crop=(0, 30), pan_to=(110, 30), hl=(40, 215, 340, 340)),
], ["Costos por fase", "Stock", "Flota"], dur=2.5, count=(2, "fases con gasto"))
feature2("k3", 3, "Gestión", "Menos ~planillas~, más *control", [
    dict(img="cc-indicadores.png", w=1360, S=1.2, crop=(90, 141), pan_to=(330, 141), hl=(885, 515, 383, 252)),
], ["Indicadores", "Reportes", "Un solo lugar"], dur=2.5, count=(12, "meses de historial"))
feature2("k4", 4, "E-commerce", "Tienda online y *catálogo", [
    dict(img="tienda-1.png", w=1360, S=1.2, crop=(0, 0), pan_to=(260, 40), hl=(300, 325, 650, 300)),
], ["Catálogo", "Ofertas", "WhatsApp"], dur=2.5, count=(4, "ofertas destacadas"))
feature2("k5", 5, "Apps", "Apps que andan *sin *internet", [
    dict(img="nc-dosis.png", w=1080, S=1.0, crop=(0, 880), pan_to=(0, 1240), hl=(82, 1382, 916, 258)),
], ["Móvil", "Offline", "A medida"], dur=2.5, band_top=455, band_h=820, count=(224, "medicamentos"))
outro()

scenes = [("hero", 0, 2.5), ("k1", 2.5, 2.5), ("k2", 5, 2.5), ("k3", 7.5, 2.5),
          ("k4", 10, 2.5), ("k5", 12.5, 2.5), ("outro", 15, 5)]
hosts = "".join(f"""
      <div id="{i}" data-composition-id="{i}" data-composition-src="compositions/{i}.html"
        data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics"
        data-width="1080" data-height="1920"></div>
""" for i, s, d in scenes)
idx = open(SRC_INDEX).read()
k = idx.index('id="hero"')
head = idx[: idx.rindex("<div", 0, k)]
tail = f"""{hosts}
      <audio id="bgm" class="clip" data-start="0" data-duration="20" data-media-start="15" data-volume="1"
        data-fade-in="0.2" data-fade-out="1.4" data-track-index="0" src="assets/bgm.mp3"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
head = head.replace('data-duration="30"', 'data-duration="20"').replace('data-duration="25"', 'data-duration="20"')
open(P + "/index.html", "w").write(head + tail.lstrip("\n"))
print("ok")
