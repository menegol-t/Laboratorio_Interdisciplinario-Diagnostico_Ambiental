#!/usr/bin/env python3
"""
Calcula el % de terreno impermeabilizado (asfalto, techos, cemento) vs. filtrable
(vegetación verde, vegetación seca/marrón, suelo desnudo) en imágenes satelitales.

Uso:
    pip install pillow numpy
    python impermeabilizacion.py 2004.png 2026.png --perfiles seca normal

Genera, por cada imagen, un *_mascara.png (verde = filtrable, rojo = impermeable)
para que verifiques a ojo si la clasificación tiene sentido. Si no, ajustá los
perfiles (PERFILES, más abajo) y repetí.
"""
import argparse
import os
import numpy as np
from PIL import Image, ImageFilter

# Parámetros por perfil. Todo en HSV (H en grados 0-360, S y V entre 0 y 1).
#  green_s    : saturación mínima para considerar "verde" (tono 60-170)
#  exg        : umbral de Exceso de Verde (2g - r - b, sobre colores normalizados)
#  brown_h0   : tono mínimo para considerar "marrón/seco" (hasta 60)
#  brown_s0   : saturación mínima de lo marrón (el asfalto/cemento tienen S baja)
PERFILES = {
    "normal": dict(green_s=0.10, exg=0.03, brown_h0=20, brown_s0=0.20),
    # Imagen con vegetación pardusca (ej. 2004): más permisivo con marrones y verdes apagados
    "seca":   dict(green_s=0.08, exg=0.015, brown_h0=15, brown_s0=0.14),
}


def clasificar(path, p, mediana=5):
    img = Image.open(path)
    alpha = None
    if img.mode == "RGBA":
        alpha = np.asarray(img.split()[-1]) > 0
    img = img.convert("RGB")

    rgb = np.asarray(img).astype(np.float32) / 255.0
    hsv = np.asarray(img.convert("HSV")).astype(np.float32)
    h = hsv[..., 0] * 360.0 / 255.0
    s = hsv[..., 1] / 255.0
    v = hsv[..., 2] / 255.0

    # Exceso de verde sobre coordenadas cromáticas normalizadas
    suma = rgb.sum(axis=-1) + 1e-6
    r, g, b = rgb[..., 0] / suma, rgb[..., 1] / suma, rgb[..., 2] / suma
    exg = 2 * g - r - b

    valido = v > 0.03                      # descarta negro puro (sin datos / bordes)
    if alpha is not None:
        valido &= alpha
    agua = (h >= 180) & (h <= 260) & (s > 0.25) & valido   # se excluye del cálculo

    verde = ((h >= 60) & (h <= 170) & (s >= p["green_s"])) | (exg > p["exg"])
    marron = (h >= p["brown_h0"]) & (h < 60) & (s >= p["brown_s0"]) & (s <= 0.75) \
             & (v >= 0.15) & (v <= 0.80)

    filtrable = (verde | marron) & valido & ~agua

    # Limpieza de ruido "sal y pimienta" (filtro de mediana sobre la máscara)
    if mediana and mediana > 1:
        m = Image.fromarray((filtrable * 255).astype(np.uint8))
        m = m.filter(ImageFilter.MedianFilter(size=mediana if mediana % 2 else mediana + 1))
        filtrable = (np.asarray(m) > 127) & valido & ~agua

    area = valido & ~agua
    total = int(area.sum())
    n_filtrable = int((filtrable & area).sum())
    pct_filtrable = 100.0 * n_filtrable / total
    pct_imperm = 100.0 - pct_filtrable

    # Imagen de control: verde = filtrable, rojo = impermeable
    overlay = rgb.copy()
    color = np.zeros_like(rgb)
    color[filtrable] = (0.0, 0.8, 0.0)
    color[~filtrable & area] = (0.9, 0.1, 0.1)
    sel = area
    overlay[sel] = 0.55 * rgb[sel] + 0.45 * color[sel]
    base, _ = os.path.splitext(path)
    Image.fromarray((overlay * 255).astype(np.uint8)).save(base + "_mascara.png")

    return pct_imperm, pct_filtrable, total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("imagenes", nargs="+", help="imágenes a analizar (en orden cronológico)")
    ap.add_argument("--perfiles", nargs="+", default=None,
                    help=f"perfil por imagen ({', '.join(PERFILES)}); default: normal")
    ap.add_argument("--mediana", type=int, default=5, help="tamaño del filtro de limpieza (0 = sin filtro)")
    a = ap.parse_args()

    perfiles = a.perfiles or ["normal"] * len(a.imagenes)
    if len(perfiles) == 1:
        perfiles = perfiles * len(a.imagenes)
    if len(perfiles) != len(a.imagenes):
        ap.error("--perfiles debe tener 1 valor o uno por imagen")

    resultados = []
    for path, perfil in zip(a.imagenes, perfiles):
        imp, fil, tot = clasificar(path, PERFILES[perfil], a.mediana)
        resultados.append((path, imp))
        print(f"{path}  [{perfil}]")
        print(f"   impermeabilizado: {imp:6.2f} %")
        print(f"   filtrable:        {fil:6.2f} %   (píxeles analizados: {tot})")

    if len(resultados) >= 2:
        d = resultados[-1][1] - resultados[0][1]
        print(f"\nVariación {resultados[0][0]} -> {resultados[-1][0]}: {d:+.2f} puntos porcentuales de superficie impermeable")


if __name__ == "__main__":
    main()
