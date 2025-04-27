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
        if value > 0:
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

# 2.2 Estado Nutricional por PAB (con distinción de sexo)
plt.figure()
orden_pab = ['Bajo', 'Alto', 'Muy Alto']
ax = sns.countplot(data=df, x='Riesgo Cardiovascular', hue='Sexo', order=orden_pab)
total = len(df)
add_labels(ax, total)
plt.title('Estado Nutricional por PAB y Sexo')
plt.xticks(rotation=45)
guardar("2.2_estado_pab_sexo")

# 3. Actividad física
plt.figure()
orden_act = ['Bajo', 'Moderado', 'Alto']
ax = sns.countplot(data=df, x='Actividad Física', order=orden_act)
add_labels(ax, len(df))
plt.title('Nivel de Actividad Física')
guardar("3.1_nivel_actividad_fisica")

# 4. Estado Nutricional por IMC y Nivel de actividad física (con valores)
plt.figure()
ax = sns.countplot(data=df, x='Descripción IMC', hue='Actividad Física',
                   order=orden_imc, hue_order=orden_act)
plt.title('IMC vs Nivel de Actividad Física')
# Añadir etiquetas personalizadas
total = df.shape[0]
for container in ax.containers:
    ax.bar_label(container, labels=[f'{int(v)}\n({v/total:.1%})' for v in container.datavalues], label_type='center', color='white', fontsize=9)
guardar("4.1_imc_vs_actividad")

# 5. Estado Nutricional por PAB y nivel de actividad física (con valores)
plt.figure()
ax = sns.countplot(data=df, x='Riesgo Cardiovascular', hue='Actividad Física',
                   order=orden_pab, hue_order=orden_act)
plt.title('PAB vs Nivel de Actividad Física')
plt.xticks(rotation=45)
total = df.shape[0]
for container in ax.containers:
    ax.bar_label(container, labels=[f'{int(v)}\n({v/total:.1%})' for v in container.datavalues], label_type='center', color='white', fontsize=9)
guardar("5.1_pab_vs_actividad")

# 6. IMC, PAB y Actividad Física (Heatmap mejorado y barras apiladas con valores)
pivot = pd.crosstab(index=[df['Descripción IMC'], df['Riesgo Cardiovascular']],
                    columns=df['Actividad Física'])

plt.figure(figsize=(14, 8))
sns.heatmap(pivot, annot=True, fmt='d', cmap='YlGnBu')
plt.title('IMC y PAB vs Nivel de Actividad Física')
guardar("6.1_imc_pab_actividad_heatmap")

# Adicional: Barras apiladas
pivot_reset = pivot.reset_index()
pivot_reset.set_index(['Descripción IMC', 'Riesgo Cardiovascular'], inplace=True)

plt.figure(figsize=(12, 8))
pivot_reset.plot(kind='bar', stacked=True, colormap='tab20')
plt.title('Distribución de IMC, PAB y Nivel de Actividad Física')
plt.xlabel('Categorías Combinadas (IMC y PAB)')
plt.ylabel('Frecuencia')
plt.xticks(rotation=45)
plt.legend(title='Actividad Física')
guardar("6.2_barras_apiladas_3variables")
