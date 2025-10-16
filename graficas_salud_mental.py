import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar datos filtrados
base_path = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(base_path, "SaludMental_filtrado.xlsx")
df = pd.read_excel(excel_path)


# Graficar histograma de Edad en Ingreso
plt.figure(figsize=(8,5))
plt.hist(df['edad_en_ingreso'].dropna(), bins=20, color='#4F81BD', edgecolor='black', alpha=0.85)
plt.title('Distribución de Edad en Ingreso', fontsize=14)
plt.xlabel('Edad en Ingreso', fontsize=12)
plt.ylabel('Frecuencia', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(base_path, 'hist_edad.png'))
plt.close()


# Graficar histograma de Estancia Días
plt.figure(figsize=(8,5))
plt.hist(df['estancia_días'].dropna(), bins=20, color='#C0504D', edgecolor='black', alpha=0.85)
plt.title('Distribución de Estancia Días', fontsize=14)
plt.xlabel('Estancia Días', fontsize=12)
plt.ylabel('Frecuencia', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(base_path, 'hist_estancia.png'))
plt.close()

print('Gráficas generadas.')
