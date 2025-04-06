# Paso 1: Instalar librerías (una sola vez)
# Ejecuta en tu consola si no las tienes
# !pip install pandas matplotlib seaborn openpyxl

# Paso 2: Importar librerías
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Paso 3: Rutas
dataset_path = './dataset/Datos tesis.xlsx'
images_path = './images'
os.makedirs(images_path, exist_ok=True)

# Paso 4: Leer archivo
df = pd.read_excel(dataset_path, sheet_name='Datos')

# Paso 5: Configuración visual
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# FUNCIONES DE GUARDADO
def guardar(nombre):
    plt.savefig(f"{images_path}/{nombre}.png", bbox_inches='tight')
    plt.close()

# 1. Sociodemográficos (Sexo)
sns.countplot(data=df, x='Sexo')
plt.title('Distribución por Sexo')
guardar("1.1_distribucion_sexo")

# 2. Estado nutricional
sns.countplot(data=df, x='Descripción IMC', order=['Normal', 'Sobrepeso', 'Obesidad'])
plt.title('Estado Nutricional por IMC')
guardar("2.1_estado_imc")

sns.countplot(data=df, x='Riesgo Cardiovascular', order=['Bajo', 'Alto', 'Muy Alto'])
plt.title('Estado Nutricional por PAB')
plt.xticks(rotation=45)
guardar("2.2_estado_pab")

# 3. Actividad física
sns.countplot(data=df, x='Actividad Física', order=['Bajo', 'Moderado', 'Alto'])
plt.title('Nivel de Actividad Física')
guardar("3.1_nivel_actividad_fisica")

# 4. IMC vs Actividad Física
sns.countplot(data=df, x='Descripción IMC', hue='Actividad Física',
              order=['Normal', 'Sobrepeso', 'Obesidad'],
              hue_order=['Bajo', 'Moderado', 'Alto'])
plt.title('IMC vs Nivel de Actividad Física')
guardar("4.1_imc_vs_actividad")

# 5. PAB vs Actividad Física
sns.countplot(data=df, x='Riesgo Cardiovascular', hue='Actividad Física',
              order=['Bajo', 'Alto', 'Muy Alto'],
              hue_order=['Bajo', 'Moderado', 'Alto'])
plt.title('PAB vs Nivel de Actividad Física')
plt.xticks(rotation=45)
guardar("5.1_pab_vs_actividad")

# 6. IMC, PAB y Actividad Física (Heatmap)
pivot = pd.crosstab(
    index=df['Descripción IMC'],
    columns=[df['Riesgo Cardiovascular'], df['Actividad Física']]
)

sns.heatmap(pivot, annot=True, fmt='d', cmap='YlGnBu')
plt.title('IMC vs PAB vs Actividad Física')
guardar("6.1_imc_pab_actividad_heatmap")
