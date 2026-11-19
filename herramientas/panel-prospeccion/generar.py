#!/usr/bin/env python3
"""Genera el panel de prospección a partir de la pestaña Prospectos.

Uso:
    python3 generar.py prospectos.json [salida.html]

`prospectos.json` es la respuesta del conector de Google Sheets al leer el
rango A2:T<ultima> de la pestaña Prospectos, tal cual la devuelve:

    {"range": "Prospectos!A2:T60", "values": [["Empresa", "Rubro", ...], ...]}

El rango TIENE que empezar en la fila 2 (la 1 son los encabezados). Empezar
más abajo deja empresas afuera sin avisar.

La salida es el HTML del panel, listo para publicar como artefacto. Los datos
quedan dentro del HTML: no se guardan en el repositorio.
"""

import json
import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).parent
PLANTILLA = AQUI / "plantilla.html"

# Columnas de la pestaña Prospectos, por posición (A = 0).
EMPRESA, RUBRO, CIUDAD, CONTACTO, CANAL, DATO = 0, 1, 2, 3, 4, 5
COMO, VI, PRIMER, SEG1, SEG2, ESTADO, ACCION, NOTA, MSG = 6, 7, 8, 9, 10, 11, 12, 13, 14
VERSION = 19  # columna T


def celda(fila, i):
    return fila[i].strip() if len(fila) > i and fila[i] else ""


def telefono(dato):
    """Saca el WhatsApp de la columna F y lo deja en dígitos para wa.me."""
    m = re.search(r"WhatsApp:\s*\+?([\d\s\-\(\)]{8,})", dato)
    if not m:
        return ""
    return re.sub(r"\D", "", m.group(1))


def email(dato):
    m = re.search(r"Email:\s*([^\s|,]+@[^\s|,]+)", dato)
    return m.group(1) if m else ""


def instagram(dato):
    m = re.search(r"Instagram:\s*@?([A-Za-z0-9._]+)", dato)
    return m.group(1) if m else ""


def primera_fila(rango):
    """De 'Prospectos!A2:T60' saca el 2."""
    m = re.search(r"![A-Z]+(\d+)", rango or "")
    return int(m.group(1)) if m else 2


def armar(crudo):
    valores = crudo.get("values", [])
    base = primera_fila(crudo.get("range"))
    if base == 1:  # incluyó los encabezados
        valores = valores[1:]
        base = 2

    empresas = []
    for i, fila in enumerate(valores):
        nombre = celda(fila, EMPRESA)
        if not nombre:
            continue
        dato = celda(fila, DATO)
        empresas.append({
            "row": base + i,
            "empresa": nombre,
            "ciudad": celda(fila, CIUDAD),
            "canal": celda(fila, CANAL),
            "wa": telefono(dato),
            "email": email(dato),
            "ig": instagram(dato),
            "vi": celda(fila, VI),
            "primer": celda(fila, PRIMER),
            "estado": celda(fila, ESTADO),
            "accion": celda(fila, ACCION),
            "msg": celda(fila, MSG),
            "ver": celda(fila, VERSION),
        })

    pendientes = [e for e in empresas if e["estado"] == "Por contactar"]
    contactadas = [e for e in empresas if e["estado"] == "Contactado"]
    sin_contacto = [e for e in empresas if e["estado"] == "Falta contacto"]

    return {
        "pendientes": pendientes,
        # Las contactadas no llevan el mensaje: lo que les falta es el seguimiento.
        "contactadas": [{k: v for k, v in c.items() if k != "msg"} for c in contactadas],
        "sinContacto": [
            {"empresa": s["empresa"], "ciudad": s["ciudad"], "accion": s["accion"]}
            for s in sin_contacto
        ],
    }, empresas


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    entrada = pathlib.Path(sys.argv[1])
    salida = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else AQUI / "panel.html"

    crudo = json.loads(entrada.read_text())
    datos, empresas = armar(crudo)

    faltan_msg = [p["empresa"] for p in datos["pendientes"] if not p["msg"]]
    faltan_ver = [p["empresa"] for p in datos["pendientes"] if not p["ver"]]
    sin_canal = [
        p["empresa"] for p in datos["pendientes"]
        if not (p["wa"] or p["email"] or p["ig"])
    ]

    plantilla = PLANTILLA.read_text()
    if "__DATOS__" not in plantilla:
        print("ERROR: la plantilla no tiene el marcador __DATOS__", file=sys.stderr)
        return 1

    # Se escapa "<" para que ningún texto de la planilla pueda cerrar el <script>.
    json_datos = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    salida.write_text(plantilla.replace("__DATOS__", json_datos))

    print(f"{salida}  ({salida.stat().st_size} bytes)")
    print(f"  {len(empresas)} empresas leídas desde la fila {datos['pendientes'][0]['row'] if datos['pendientes'] else '?'}")
    print(f"  {len(datos['pendientes'])} por contactar")
    print(f"  {len(datos['contactadas'])} contactadas")
    print(f"  {len(datos['sinContacto'])} sin forma de contacto")
    for etiqueta, lista in (
        ("sin mensaje en la columna O", faltan_msg),
        ("sin versión en la columna T", faltan_ver),
        ("sin ningún canal de contacto", sin_canal),
    ):
        if lista:
            print(f"  REVISAR, {etiqueta}: {', '.join(lista)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
