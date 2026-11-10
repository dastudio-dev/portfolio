#!/usr/bin/env python3
"""Generador de reels de UN proyecto, sin voz y con texto cinetico (gen_kin.py parametrizado). Ver SKILL.md seccion 10.

Aprobado en borrador: tienda-online, landing-constructora, app-guardia, app-neonatal, monitor-simulacion,
planillas-a-sistema (19,5 s = hero 2,5 + 3 escenas de 4 + outro 5; el de conceptos 20 s con 5 escenas de 2,5).

Copialo al scratchpad (no lo ejecutes desde el skill), agrega una entrada a CFG y corre:  python3 -I build_all.py <slug>
Cada entrada de CFG:
  imgs      {nombre_destino: (archivo_en_img/, recorte_superior_px)}  o  (@archivo_de_sistema-a-medida/assets/screens, 0)
  hero_q    gancho en mayusculas ("*palabra" = celeste), hero_sub = bajada
  dur       segundos por escena (4 con 3 escenas; 2,5 con 5)
  scenes    lista de dict(tag, title (<=33 car.), shot=dict(img,w,S,crop,pan_to,hl), chips=[3], count=(valor, etiqueta) o ausente, mobile=True)
  caption   texto del post (nunca inventes cifras ni nombres de sistemas)
Crea proyectos/<slug>/ copiando sistema-a-medida (fuentes, marca, bgm.mp3) y escribe compositions/, index.html y renders/caption.txt.
Despues: npx --yes hyperframes@0.9.8 check, snapshot --at 4.5,8.5,12.5 y mirar la hoja de contacto, y render -o renders/<slug>_v1.mp4.
Con count ausente se oculta el contador (usalo si la captura no tiene una cifra real visible).
"""
import os, re, shutil, sys, json
from PIL import Image

REPO = "/home/diego/Soft/repos/portfolio"
PROY = REPO + "/proyectos"
BASE = PROY + "/sistema-a-medida"
IMG = REPO + "/img"
TPL = REPO + "/.claude/skills/portfolio-reel/templates/gen_kin.py"

src = open(TPL).read()
cut = src.index('hero()\nfeature2("k1"')
head_src = src[:cut]


def sub(s, old, new, count=1):
    assert old in s, f"no encontre: {old[:60]}"
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


def prep_img(P, name, src_file, crop_top=0):
    im = Image.open(f"{IMG}/{src_file}").convert("RGB")
    if crop_top:
        im = im.crop((0, crop_top, im.width, im.height))
    im.save(f"{P}/assets/screens/{name}")


def build(slug, cfg):
    P = scaffold(slug)
    for name, (srcf, ct) in cfg["imgs"].items():
        if srcf.startswith("@"):
            shutil.copy(f"{BASE}/assets/screens/{srcf[1:]}", f"{P}/assets/screens/{name}")
        else:
            prep_img(P, name, srcf, ct)
    os.environ["REEL_P"] = P
    ns = {"__name__": "gen", "HERO_Q": cfg["hero_q"], "HERO_SUB": cfg["hero_sub"], "NSEG": len(cfg["scenes"])}
    exec(head_src, ns)
    ns["hero"]()
    sc = []
    for i, s in enumerate(cfg["scenes"], 1):
        kw = dict(dur=cfg["dur"], count=s.get("count"))
        if s.get("mobile"):
            kw.update(band_top=455, band_h=820)
        ns["feature2"](f"k{i}", i, s["tag"], s["title"], [s["shot"]], s["chips"], **kw)
        sc.append((f"k{i}", 2.5 + (i - 1) * cfg["dur"], cfg["dur"]))
    ns["outro"]()
    total = 2.5 + len(cfg["scenes"]) * cfg["dur"] + 5
    sc = [("hero", 0, 2.5)] + sc + [("outro", total - 5, 5)]
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

CFG["tienda-online"] = dict(
    imgs={"tienda.png": ("herramientas_1.png", 0)},
    hero_q="Tu *tienda *online a medida", hero_sub="E-commerce con catálogo y carrito.", dur=4,
    scenes=[
        dict(tag="Catálogo", title="Tu catálogo *siempre abierto",
             shot=dict(img="tienda.png", w=1360, S=1.2, crop=(0, 0), pan_to=(330, 0), hl=(230, 170, 900, 62)),
             chips=["Catálogo", "Carrito", "WhatsApp"]),
        dict(tag="Ofertas", title="Ofertas y *liquidaciones",
             shot=dict(img="tienda.png", w=1360, S=1.6, crop=(60, 191), pan_to=(420, 191), hl=(60, 330, 270, 50)),
             chips=["Ofertas", "Destacados", "Nuevos"], count=(4, "ofertas activas")),
        dict(tag="Pedidos", title="Pedí directo por *WhatsApp",
             shot=dict(img="tienda.png", w=1360, S=1.6, crop=(400, 191), pan_to=(685, 191), hl=(1262, 405, 90, 90)),
             chips=["Envíos al país", "Venta directa", "WhatsApp"]),
    ],
    caption="""Tu tienda online a medida, con catálogo y carrito 🛒

Un e-commerce pensado para vender herramientas:
📦 Catálogo siempre abierto, con ofertas y liquidaciones.
🛠️ Productos destacados y nuevos ingresos.
💬 Pedidos directos por WhatsApp y envíos a todo el país.

Hoy una tienda, mañana tu herramienta: sistemas de gestión, e-commerce, apps clínicas, sitios corporativos.

¿Querés vender online? Escribinos 👇""" + CTA + "#softwareamedida #desarrolloweb #ecommerce #tiendaonline #catalogo #pymes #dastudio",
)

CFG["landing-constructora"] = dict(
    imgs={"jl1.png": ("constructora_1.png", 0), "jl2.png": ("constructora_2.png", 0), "jl3.png": ("constructora_3.png", 0)},
    hero_q="Tu *landing *page a medida", hero_sub="Presentación clara, lista para generar contactos.", dur=4,
    scenes=[
        dict(tag="Landing page", title="Tu empresa en *una *landing",
             shot=dict(img="jl1.png", w=1360, S=1.2, crop=(0, 0), pan_to=(330, 0), hl=(524, 184, 523, 151)),
             chips=["Marca", "Servicios", "Contacto"], count=(8, "años de trayectoria")),
        dict(tag="Servicios", title="Servicios *claros y visuales",
             shot=dict(img="jl2.png", w=1360, S=1.2, crop=(0, 0), pan_to=(330, 40), hl=(71, 328, 380, 312)),
             chips=["Servicios", "Imágenes", "Detalle"], count=(6, "líneas de negocio")),
        dict(tag="Equipamiento", title="Equipamiento *a la vista",
             shot=dict(img="jl3.png", w=1360, S=1.2, crop=(0, 0), pan_to=(330, 0), hl=(71, 303, 292, 290)),
             chips=["Maquinaria", "Flota propia", "Fichas"]),
    ],
    caption="""Una landing page que presenta tu empresa 🏗️

Este caso, para una empresa de transporte y construcción:
✅ Portada con identidad de marca y llamado a contactar.
✅ Servicios explicados con imágenes y detalle.
✅ Maquinaria y equipamiento a la vista.

Hoy una constructora, mañana tu herramienta: sistemas de gestión, e-commerce, apps clínicas, sitios corporativos.

¿Necesitás presentar tu empresa en la web? Escribinos 👇""" + CTA + "#softwareamedida #desarrolloweb #landingpage #construccion #sitioweb #dastudio",
)

CFG["app-guardia"] = dict(
    imgs={"eg1.png": ("egpediatria_1.png", 0), "eg2.png": ("egpediatria_2.png", 0)},
    hero_q="App médica *de *guardia", hero_sub="Dosis por peso, también sin conexión.", dur=4,
    scenes=[
        dict(tag="Guardia", title="Dosis por *peso, al instante",
             shot=dict(img="eg1.png", w=1360, S=1.2, crop=(160, 0), pan_to=(0, 0), hl=(42, 264, 196, 65)),
             chips=["Peso", "Edad", "Dosis"], count=(10, "kg · peso del paciente")),
        dict(tag="Preparación", title="Preparación *paso a paso",
             shot=dict(img="eg2.png", w=1360, S=1.2, crop=(230, 0), pan_to=(460, 0), hl=(370, 213, 430, 90)),
             chips=["Adrenalina", "Dopamina", "Diluciones"]),
        dict(tag="Infusión", title="Infusión *en bomba, calculada",
             shot=dict(img="eg2.png", w=1360, S=1.2, crop=(300, 0), pan_to=(460, 0), hl=(880, 300, 430, 150)),
             chips=["ml/h", "mcg/kg/min", "Rangos"], count=(20, "mcg/kg/min · máx.")),
    ],
    caption="""Una app médica de guardia, hecha a medida 🚑

Dosis de emergencia por peso del paciente, al instante:
⚖️ Ingresás el peso y la app calcula.
💉 Preparación estándar paso a paso (adrenalina, dopamina y más).
⏱️ Velocidad de infusión en bomba, calculada.
📶 Funciona también sin conexión.

Hoy una guardia, mañana tu herramienta: sistemas de gestión, e-commerce, apps clínicas, sitios corporativos.

¿Tenés una herramienta clínica en mente? Escribinos 👇""" + CTA + "#softwareamedida #desarrolloweb #saludDigital #appmedica #pwa #pediatria #dastudio",
)

CFG["app-neonatal"] = dict(
    imgs={"nc2.png": ("neocalcu_2.png", 110), "nc3.png": ("neocalcu_3.png", 110)},
    hero_q="App neonatal *en tu *celular", hero_sub="Dosificación en UCIN, instalable y offline.", dur=4,
    scenes=[
        dict(tag="UCIN", title="Dosis neonatales *por peso", mobile=True,
             shot=dict(img="nc2.png", w=1080, S=1.0, crop=(0, 0), pan_to=(0, 250), hl=(14, 215, 1052, 118)),
             chips=["Peso", "E.G.", "Días"], count=(2540, "g · peso del paciente")),
        dict(tag="Vademécum", title="*Medicamentos a mano", mobile=True,
             shot=dict(img="nc2.png", w=1080, S=1.0, crop=(0, 500), pan_to=(0, 900), hl=(14, 555, 1052, 105)),
             chips=["Buscador", "Favoritos", "Kit crítico"], count=(224, "resultados")),
        dict(tag="Dosificación", title="Dosis *calculada al instante", mobile=True,
             shot=dict(img="nc3.png", w=1080, S=1.0, crop=(0, 1100), pan_to=(0, 1250), hl=(60, 1352, 960, 250)),
             chips=["Dosis", "Intervalo", "Enfermería"], count=(15, "mg/kg/dosis")),
    ],
    caption="""Una app neonatal en el celular 👶

Dosificación en UCIN, instalable y que funciona offline:
⚖️ Cargás el peso, la edad gestacional y los días.
💊 Más de 200 medicamentos con buscador y favoritos.
🧮 Dosis calculada con la instrucción para enfermería.

Hoy una app clínica, mañana tu herramienta: sistemas de gestión, e-commerce, apps clínicas, sitios corporativos.

¿Necesitás una app a medida para tu equipo? Escribinos 👇""" + CTA + "#softwareamedida #desarrolloweb #saludDigital #neonatologia #pwa #appmovil #dastudio",
)

CFG["monitor-simulacion"] = dict(
    imgs={"nm.png": ("neomonitor_1.png", 0)},
    hero_q="Un monitor *de *simulación", hero_sub="Signos vitales en pantalla, hecho a medida.", dur=4,
    scenes=[
        dict(tag="Simulación", title="Frecuencia *cardíaca en vivo",
             shot=dict(img="nm.png", w=1360, S=1.2, crop=(0, 0), pan_to=(460, 40), hl=(1120, 145, 215, 120)),
             chips=["ECG", "FC", "Tiempo real"], count=(123, "lpm · simulado")),
        dict(tag="Signos vitales", title="SpO₂ y *temperatura",
             shot=dict(img="nm.png", w=1360, S=1.2, crop=(460, 168), pan_to=(460, 100), hl=(1160, 410, 190, 125)),
             chips=["SpO₂", "Temperatura", "Pleth"], count=(91, "% · SpO₂ simulado")),
        dict(tag="Controles", title="Controles *a la mano",
             shot=dict(img="nm.png", w=1360, S=1.2, crop=(0, 168), pan_to=(300, 168), hl=(10, 700, 780, 52)),
             chips=["Silenciar", "Menú", "Vincular"]),
    ],
    caption="""Un monitor de simulación hecho a medida 📈

Signos vitales en pantalla para capacitar:
💚 Frecuencia cardíaca y trazado de ECG.
🫁 Saturación (SpO₂) y curva de pletismografía.
🌡️ Temperatura y controles de simulación.

Hoy una simulación, mañana tu herramienta: sistemas de gestión, e-commerce, apps clínicas, sitios corporativos.

¿Tenés una idea para una herramienta a medida? Escribinos 👇""" + CTA + "#softwareamedida #desarrolloweb #simulacion #saludDigital #pwa #dastudio",
)

CFG["planillas-a-sistema"] = dict(
    imgs={"a1.png": ("@cc-indicadores.png", 0), "a2.png": ("@flota-unidades.png", 0), "a3.png": ("@flota-fases.png", 0),
          "a4.png": ("@tienda-1.png", 0), "a5.png": ("@nc-dosis.png", 0)},
    hero_q="¿Todavía con *planillas y *WhatsApp?", hero_sub="Pasá a un sistema hecho a tu medida.", dur=2.5,
    scenes=[
        dict(tag="Tablero", title="Del ~Excel~ al *tablero",
             shot=dict(img="a1.png", w=1360, S=1.2, crop=(90, 141), pan_to=(330, 141), hl=(885, 515, 383, 252)),
             chips=["Indicadores", "Reportes", "Un solo lugar"], count=(12, "meses de historial")),
        dict(tag="Alertas", title="Alertas que *avisan antes",
             shot=dict(img="a2.png", w=1368, S=1.2, crop=(0, 0), pan_to=(468, 20), hl=(36, 98, 1120, 240)),
             chips=["Unidades", "Obras", "Alertas"], count=(75, "unidades")),
        dict(tag="Costos", title="Cada obra, *costo por fase",
             shot=dict(img="a3.png", w=1368, S=1.2, crop=(0, 30), pan_to=(110, 30), hl=(40, 215, 340, 340)),
             chips=["Fases", "Materiales", "Servicios"], count=(2, "fases con gasto")),
        dict(tag="Ventas", title="Ventas sin ~chats~ eternos",
             shot=dict(img="a4.png", w=1360, S=1.2, crop=(0, 0), pan_to=(260, 40), hl=(300, 325, 650, 300)),
             chips=["Catálogo", "Ofertas", "WhatsApp"], count=(4, "ofertas destacadas")),
        dict(tag="Móvil", title="En el celu, *sin internet", mobile=True,
             shot=dict(img="a5.png", w=1080, S=1.0, crop=(0, 880), pan_to=(0, 1240), hl=(82, 1382, 916, 258)),
             chips=["Móvil", "Offline", "A medida"], count=(224, "medicamentos")),
    ],
    caption="""¿Todavía resolvés todo con planillas y WhatsApp? 📊

Pasá a un sistema hecho a tu medida:
📈 Del Excel al tablero con indicadores.
🔔 Alertas que te avisan antes del problema.
🏗️ Costos por obra y por fase, claros.
🛒 Ventas con catálogo en vez de chats eternos.
📱 Apps que funcionan hasta sin internet.

¿Contanos cómo trabajás hoy? Escribinos 👇""" + CTA + "#softwareamedida #desarrolloweb #sistemasdegestion #pymes #automatizacion #pwa #dastudio",
)

if __name__ == "__main__":
    only = sys.argv[1:] or list(CFG)
    for slug in only:
        build(slug, CFG[slug])
