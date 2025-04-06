import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Rutas
dataset_path = './dataset/Datos tesis.xlsx'
images_path = './images'
os.makedirs(images_path, exist_ok=True)

# Leer archivo
df = pd.read_excel(dataset_path, sheet_name='Datos')

# Configuración visual
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Función para guardar gráficos
def guardar(nombre):
    plt.savefig(f"{images_path}/{nombre}.png", bbox_inches='tight')
    plt.close()

# Función auxiliar para añadir etiquetas a las barras
def add_labels(ax, total):
    for p in ax.patches:
        value = int(p.get_height())
        percentage = 100 * value / total
        ax.text(p.get_x() + p.get_width() / 2, p.get_height() / 2,
                f'{value}\n({percentage:.1f}%)', 
                ha='center', va='center', color='white', fontsize=11, fontweight='bold')

# 1. Sociodemográficos (Sexo)
plt.figure()
ax = sns.countplot(data=df, x='Sexo')
add_labels(ax, len(df))
plt.title('Distribución por Sexo')
guardar("1.1_distribucion_sexo")

# 2.1 Estado Nutricional por IMC
plt.figure()
orden_imc = ['Normal', 'Sobrepeso', 'Obesidad']
ax = sns.countplot(data=df, x='Descripción IMC', order=orden_imc)
add_labels(ax, len(df))
plt.title('Estado Nutricional por IMC')
guardar("2.1_estado_imc")

# 2.2 Estado Nutricional por PAB
plt.figure()
orden_pab = ['Bajo', 'Alto', 'Muy Alto']
ax = sns.countplot(data=df, x='Riesgo Cardiovascular', order=orden_pab)
add_labels(ax, len(df))
plt.title('Estado Nutricional por PAB')
plt.xticks(rotation=45)
guardar("2.2_estado_pab")

# 3. Actividad física
plt.figure()
orden_act = ['Bajo', 'Moderado', 'Alto']
ax = sns.countplot(data=df, x='Actividad Física', order=orden_act)
add_labels(ax, len(df))
plt.title('Nivel de Actividad Física')
guardar("3.1_nivel_actividad_fisica")

# 4. IMC vs Actividad Física
plt.figure()
ax = sns.countplot(data=df, x='Descripción IMC', hue='Actividad Física',
                   order=orden_imc, hue_order=orden_act)
plt.title('IMC vs Nivel de Actividad Física')
guardar("4.1_imc_vs_actividad")

# 5. PAB vs Actividad Física
plt.figure()
ax = sns.countplot(data=df, x='Riesgo Cardiovascular', hue='Actividad Física',
                   order=orden_pab, hue_order=orden_act)
plt.title('PAB vs Nivel de Actividad Física')
plt.xticks(rotation=45)
guardar("5.1_pab_vs_actividad")

# 6. IMC, PAB y Actividad Física (Heatmap)
plt.figure(figsize=(14, 8))
pivot = pd.crosstab(index=df['Descripción IMC'],
                    columns=[df['Riesgo Cardiovascular'], df['Actividad Física']])
sns.heatmap(pivot, annot=True, fmt='d', cmap='YlGnBu')
plt.title('IMC vs PAB vs Actividad Física')
guardar("6.1_imc_pab_actividad_heatmap")
