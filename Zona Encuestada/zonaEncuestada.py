import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar la base de datos de encuestas
df = pd.read_excel('encuestas_para_qgis.xlsx')

# 2. Filtrar las encuestas dentro de la zona delimitada
def filtrar_zona(row):
    texto = f"{str(row['calle_norm'])} {str(row['esquina_norm'])} {str(row['calle_original'])} {str(row['esquina_original'])}".lower()
    
    # Excluir calles externas
    fuera = ['darragueira', 'mosconi', 'dante', 'alighieri', 'gascón', 'gascon', 'rivadavia', 'villa de mayo', 'medrano', 'moreno', 'godoy cruz', 'verdi', 'artigas', 'peregrino', 'cayetano', 'amenábar', 'romain rolland']
    for f in fuera:
        if f in str(row['calle_norm']).lower() or f in str(row['esquina_norm']).lower():
            return False
            
    # Incluir solo calles de la zona central
    dentro = ['velázquez', 'velazquez', 'mozart', 'gutiérrez', 'gutierrez', 'el greco', 'carlos pellegrini', 'alejandro sirio']
    return any(d in texto for d in dentro)

df_zona = df[df.apply(filtrar_zona, axis=1)].copy()

# 3. Analizar la pregunta P16 (¿Considera que vive en un área inundable?)
conteo_p16 = df_zona['p16'].value_counts()
total_encuestas = len(df_zona)

print(f"Total de personas encuestadas en la zona: {total_encuestas}")
print(conteo_p16)

# 4. Generar el Gráfico de Torta con cantidades y porcentajes
plt.figure(figsize=(8, 8))
colores = ['#ff9999', '#66b3ff']

# Función para mostrar cantidad absoluta y porcentaje en cada porción
def funcion_formato(pct):
    total = sum(conteo_p16)
    val = int(round(pct * total / 100.0))
    return f"{val} pers.\n({pct:.1f}%)"

wedges, texts, autotexts = plt.pie(
    conteo_p16, 
    labels=conteo_p16.index, 
    autopct=funcion_formato, 
    startangle=90, 
    colors=colores,
    wedgeprops={'edgecolor': 'black', 'linewidth': 1}
)

# Mejorar estilo de texto dentro del gráfico
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')

plt.title(f'Percepción de Inundaciones en la Zona Delimitada\n(Total encuestados: {total_encuestas} personas)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()

# Guardar y mostrar el gráfico
plt.savefig('grafico_inundaciones_con_cantidades.png', dpi=300)
plt.show()