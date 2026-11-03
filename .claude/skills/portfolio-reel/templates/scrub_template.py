# Plantilla de limpieza de capturas (ver SKILL.md §3). Copiala al scratchpad y editá RAW/OUT/JOBS.
# RAW: capturas originales SIN limpiar (fuera del repo). OUT: assets/screens/ del proyecto.
# JOBS: {nombre: [cajas (x0,y0,x1,y1) en px de la captura a pixelar]}. Revisá SIEMPRE el resultado a ojo:
# una caja de más tapa nombres de unidades; una de menos deja una patente legible.
from PIL import Image
RAW="/tmp/claude-1000/-home-diego--claude-spares-spare-m98Q3R/98e29902-77c6-46c0-8d9e-ccc9237f6314/scratchpad/raw/"
OUT="/home/diego/Soft/repos/portfolio/proyectos/flota-firebase/assets/screens/"
def pix(im, box, k=14):
    x0,y0,x1,y1 = box
    r = im.crop(box); w,h = r.size
    r = r.resize((max(1,w//k), max(1,h//k)), Image.BILINEAR).resize((w,h), Image.NEAREST)
    im.paste(r, box)
JOBS = {
 "resultados": [(770,150,995,545),(1095,150,1325,195),(1095,500,1325,540)],      # importes reales y facturados
 "fases":      [(790,335,1312,482)],                                              # importes por fase
 "materiales": [(1160,125,1330,647)],                                             # costos
 "alertas":    [(188,133,312,168),(84,60,198,94),(282,503,378,540),(52,540,116,570),(52,0,190,30)],  # patentes
 "unidades":   [], "inicio": [], "obra-header": [],
}
for name, boxes in JOBS.items():
    im = Image.open(RAW+name+".jpg").convert("RGB")
    for b in boxes: pix(im, b)
    im.save(OUT+name+".png")
    print(name, im.size)
