# Cálculo de Superficie Impermeable en Imágenes Satelitales

Este script analiza imágenes satelitales o fotos aéreas para medir el impacto de la urbanización en una zona determinada. Su objetivo principal es calcular qué porcentaje del terreno corresponde a superficie impermeable (asfalto, concreto, techos) y cuánto permanece como suelo filtrable (vegetación, tierra o zonas secas), permitiendo comparar la evolución del suelo a lo largo del tiempo.

## Requisitos

Requiere Python 3 y las librerías `pillow` y `numpy`. Se instalan ejecutando:

```
pip install pillow numpy
```

## Cómo se ejecuta

### Analizar y comparar dos fechas

Para analizar una secuencia de imágenes (por ejemplo, dos capturas de distintas épocas):

```
python impermeabilizacion.py 2004.jpg 2026.jpg
```

### Ajuste por estacionalidad (`--perfiles`)

La vegetación cambia de color según la época del año. Si una de las imágenes fue tomada en invierno o durante un periodo de sequía (donde predominan los tonos amarillentos o marrones), se puede especificar el perfil correspondiente:

```
python impermeabilizacion.py 2004.png 2026.png --perfiles seca normal
```

* `normal`: Pensado para imágenes de primavera o verano, donde la vegetación se observa verde.
* `seca`: Diseñado para tomas de invierno o zonas áridas, siendo más permisivo con los tonos pardos y amarillos.

---

## Para qué sirve

El programa ayuda a cuantificar la pérdida de suelo natural frente al avance urbano o industrial. Es útil para:

* Estudiar la evolución del uso del suelo entre distintas fechas (por ejemplo, comparar una toma de 2004 con una de 2026).
* Evaluar el riesgo de inundaciones o capacidad de absorción en una cuenca urbana.
* Generar reportes rápidos sobre expansión de la huella construida.

## Cómo funciona la clasificación

El algoritmo trabaja analizando el color y la saturación de cada píxel de la imagen:

1. **Suelo filtrable:** Identifica coberturas vegetales (tanto verdes intensas como vegetación seca o pardusca) y superficies de tierra desnuda.
2. **Suelo impermeable:** Clasifica como impermeable todo aquello que no presente firma espectral/cromática vegetal o de tierra (principalmente materiales de construcción, asfalto y cemento).
3. **Exclusiones:** Descarta automáticamente cuerpos de agua y áreas sin datos (bordes transparentes o negros).

Al finalizar cada análisis, el programa genera una imagen de control (`*_mascara.png`) donde pinta de **verde** las áreas filtrables y de **rojo** las impermeables. Esto permite verificar visualmente si la clasificación refleja la realidad del terreno.

## Ejemplo de resultado

Al procesar las imágenes, la herramienta devuelve un resumen por terminal con el balance de superficies y la variación neta entre el primer y el último período:

```
2004.png  [seca]
   impermeabilizado:  34.12 %
   filtrable:         65.88 %   (píxeles analizados: 1048576)

2026.png  [normal]
   impermeabilizado:  52.40 %
   filtrable:         47.60 %   (píxeles analizados: 1048576)

Variación 2004.png -> 2026.png: +18.28 puntos porcentuales de superficie impermeable
```