"""
Lee un Excel con precipitación diaria (columnas FECHA y PRECIP)
y dibuja un gráfico de barras con la precipitación total por año.

Uso:
    python precip_anual.py datos.xlsx
    python precip_anual.py datos.xlsx --hoja "Hoja1" --salida grafico.png

Requisitos:
    pip install pandas openpyxl matplotlib
"""

import argparse

import matplotlib.pyplot as plt
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archivo", help="Ruta al archivo Excel (.xlsx)")
    parser.add_argument("--hoja", default=0, help="Nombre o índice de la hoja (por defecto la primera)")
    parser.add_argument("--salida", default="precipitacion_anual.png", help="Imagen de salida")
    args = parser.parse_args()

    # --- Leer Excel ---
    df = pd.read_excel(args.archivo, sheet_name=args.hoja, usecols=["FECHA", "PRECIP"])

    # Fechas en formato día/mes/año (funciona tanto si Excel las guarda
    # como texto "13/01/1991" como si son fechas reales)
    df["FECHA"] = pd.to_datetime(df["FECHA"], dayfirst=True, errors="coerce")
    df["PRECIP"] = pd.to_numeric(df["PRECIP"], errors="coerce")

    # Descartar filas con fecha inválida
    df = df.dropna(subset=["FECHA"])

    # --- Totales anuales ---
    # Las celdas vacías (NaN) se ignoran en la suma, o sea cuentan como 0 mm
    df["ANIO"] = df["FECHA"].dt.year
    anual = df.groupby("ANIO")["PRECIP"].sum()

    # Días con dato por año (para detectar años incompletos)
    dias_con_dato = df.groupby("ANIO")["PRECIP"].count()
    print("Precipitación anual (mm):")
    print(anual.round(1).to_string())
    print("\nDías con registro por año:")
    print(dias_con_dato.to_string())

    # --- Gráfico ---
    fig, ax = plt.subplots(figsize=(12, 6))
    barras = ax.bar(anual.index.astype(str), anual.values, color="steelblue", edgecolor="black")
    ax.bar_label(barras, fmt="%.0f", padding=3, fontsize=8)

    ax.axhline(anual.mean(), color="red", linestyle="--", label=f"Promedio: {anual.mean():.0f} mm")

    ax.set_title("Precipitación total anual")
    ax.set_xlabel("Año")
    ax.set_ylabel("Precipitación (mm)")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(args.salida, dpi=150)
    print(f"\nGráfico guardado en: {args.salida}")
    plt.show()


if __name__ == "__main__":
    main()
