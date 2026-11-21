# Zona Encuestada

## Descripción

Este módulo forma parte del proyecto **Laboratorio Interdisciplinario: Diagnóstico Ambiental** y analiza la percepción de los habitantes sobre las inundaciones en una zona delimitada del partido de San Miguel, provincia de Buenos Aires.

La información proviene de encuestas realizadas a vecinos de la zona y se procesa con Python y Pandas para identificar cuántas personas consideran que viven en un área inundable.

## Objetivos

- Analizar las respuestas de los habitantes sobre el riesgo de inundaciones.
- Delimitar las encuestas correspondientes a la zona estudiada.
- Clasificar las respuestas según la percepción de los encuestados.
- Representar los resultados mediante gráficos.
- Relacionar la percepción de inundación con el diagnóstico ambiental del área.

## Datos

Los datos utilizados se encuentran en el archivo:

- `encuestas_para_qgis.xlsx`

Este conjunto de datos contiene las respuestas de las encuestas junto con campos geográficos y de dirección, entre los que se utilizan:

- `calle_norm`
- `esquina_norm`
- `calle_original`
- `esquina_original`
- `p16`

La variable `p16` corresponde a la respuesta sobre si el encuestado considera que vive en un área inundable.

## Metodología

El análisis implementado en `zonaEncuestada.py` sigue los siguientes pasos:

1. Carga el archivo Excel mediante Pandas.
2. Construye una descripción textual de cada dirección.
3. Excluye las encuestas ubicadas en calles externas a la zona delimitada.
4. Selecciona las encuestas ubicadas en las calles centrales.
5. Cuenta las respuestas de la pregunta P16.
6. Calcula el total de personas encuestadas.
7. Genera un gráfico de torta con cantidades y porcentajes.
8. Guarda la visualización como una imagen en alta resolución.

## Resultados

El programa genera una imagen con los resultados del análisis.

El gráfico muestra:

- La cantidad de personas que consideran que viven en un área inundable.
- La cantidad de personas que consideran que no viven en un área inundable.
- El porcentaje correspondiente a cada respuesta.
- El número total de encuestas incluidas en la zona estudiada.

## Conclusión

El análisis permite observar la percepción de los habitantes respecto del riesgo de inundación en el sector estudiado.

Los resultados pueden complementarse con análisis de precipitaciones, impermeabilización del suelo y crecimiento poblacional para obtener un diagnóstico ambiental más completo.

## Ejecución

1. Clonar el repositorio:

```bash
git clone https://github.com/menegol-t/Laboratorio_Interdisciplinario-Diagnostico_Ambiental.git
```

2. Ingresar a la carpeta del módulo:

```bash
cd "Laboratorio_Interdisciplinario-Diagnostico_Ambiental/Zona Encuestada"
```

3. Instalar las dependencias necesarias:

```bash
pip install pandas matplotlib openpyxl
```

4. Ejecutar el programa:

```bash
python zonaEncuestada.py
```

El archivo Excel debe encontrarse en la misma carpeta que el script.

## Requisitos

- Python 3
- Pandas
- Matplotlib
- OpenPyXL
- Microsoft Excel o una aplicación compatible para modificar archivos `.xlsx`

## Aplicación ambiental

La percepción de los habitantes puede utilizarse para:

- Identificar sectores donde el riesgo de inundación es reconocido por la población.
- Comparar la información social con datos meteorológicos e hidrológicos.
- Detectar zonas que requieren mayor prevención y planificación urbana.
- Incorporar la perspectiva comunitaria en el diagnóstico ambiental.

## Archivos del módulo

- `zonaEncuestada.py`: procesa las encuestas y genera el gráfico.
- `encuestas_para_qgis.xlsx`: base de datos geoespacial de las encuestas.
- `diccionario_preguntas.xlsx`: contiene el significado de las preguntas y respuestas.
- `Encuestados.png`: imagen generada con los resultados.

## Autoría

Tomás Menegol - Lucia Salomón - Soledad Sánchez - Lucia Sequeira - Luca Velazquez.
