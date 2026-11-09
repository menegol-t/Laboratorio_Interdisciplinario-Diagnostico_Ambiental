# Precipitación anual desde Excel

Script en Python que lee un Excel con precipitación diaria de una estación meteorológica y dibuja un gráfico de barras con el total de cada año. En particular, se utilizo  el excel [smn_datos_meteorologicos_1991_2020](https://ssl.smn.gob.ar/dpd/observaciones/smn_datos_meteorologicos_1991_2020.rar) obtenido del [Servicio Meteorologico Nacional Argentino > Descarga de datos historicos > Registro de datos diarios 1991-2020](https://www.smn.gob.ar/descarga-de-datos). De esta fuente, se filtro solo la estación de San Miguel y se genero con sus datos el nuevo excel "Estación de San Miguel", adjunto en este repositorio.

## Uso rápido

Instalar librerias
```
python -m pip install pandas openpyxl matplotlib
```

Posterior
```
python precip_anual.py estacion_san_miguel.xlsx
```

# Requisitos

- Python 3.9 o superior


### Formato del Excel

El archivo debe tener una hoja con dos columnas, con estos nombres exactos en la primera fila:

| FECHA      | PRECIP |
|------------|--------|
| 01/01/1991 | 6      |
| 02/01/1991 |        |
| 08/01/1991 | 34     |

- `FECHA`: formato día/mes/año. Puede estar guardada como texto o como fecha de Excel.
- `PRECIP`: precipitación diaria en mm.
- Una fila por día y **una sola estación**. Si el archivo tiene varias estaciones apiladas, o filas repetidas, los totales salen inflados: filtrá o limpiá los datos antes.

### Otras opciones

```
python precip_anual.py estacion_san_miguel.xlsx
python precip_anual.py estacion_san_miguel.xlsx --hoja "Hoja1"
python precip_anual.py archivo.xlsx --hoja "Hoja1" --salida grafico.png
```

| Argumento  | Descripción                                              | Por defecto                |
|------------|----------------------------------------------------------|----------------------------|
| `archivo`  | Ruta al Excel (.xlsx)                                    | (obligatorio)              |
| `--hoja`   | Nombre o índice de la hoja con los datos                 | primera hoja               |
| `--salida` | Nombre de la imagen de salida                            | `precipitacion_anual.png`  |

El nombre de la hoja tiene que coincidir exactamente con el de la pestaña, y va entre comillas si tiene espacios.

## Qué hace

1. Lee las columnas `FECHA` y `PRECIP`.
2. Convierte las fechas (día primero) y los valores a número.
3. Suma la precipitación por año.
4. Imprime en consola los totales anuales y la cantidad de días con registro por año.
5. Dibuja el gráfico de barras, con el valor sobre cada barra y una línea con el promedio, lo guarda como PNG y lo muestra en pantalla.

## Datos faltantes

- Las celdas vacías y los valores no numéricos (por ejemplo `S/D`) se ignoran en la suma, es decir que no aportan nada al total.
- Si en tu estación vacío significa "no llovió", los totales son correctos.
- Si vacío o `S/D` significa "sin dato", los años con muchos faltantes quedan subestimados. Revisá la tabla de **días con registro por año** que imprime el script: un año con muy pocos días probablemente esté incompleto.

## Problemas frecuentes

- **`ModuleNotFoundError: No module named 'matplotlib'`**: las librerías están instaladas en otro Python. Instalalas con `python -m pip install ...`.
- **Error de columnas `FECHA` / `PRECIP` no encontradas**: probablemente se está leyendo otra hoja. Indicá la correcta con `--hoja`.
- **Totales anuales absurdamente altos** (decenas de miles de mm): hay filas duplicadas o varias estaciones en la misma hoja.
