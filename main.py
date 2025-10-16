# ============================
# 1. Importar librerías
# ============================
import pandas as pd
import numpy as np
import sys

# ============================
# 2. Configurar salida a archivo
# ============================
# Crear archivo de salida
output_file = r"C:\Users\gtorr\Desktop\Universidad\malakaton\malackathon2025\analisis_salud_mental.txt"
sys.stdout = open(output_file, 'w', encoding='utf-8')

# ============================
# 3. Cargar el archivo Excel
# ============================
# Cambia la ruta por la de tu archivo
ruta_archivo = r"C:\Users\gtorr\Desktop\Universidad\malakaton\malackathon2025\SaludMental.xls"
# Especificar el engine para archivos .xls
df = pd.read_excel(ruta_archivo, engine='xlrd')

# ============================
# 4. Vista general del dataset
# ============================
print("=== DIMENSIONES DEL DATAFRAME ===")
print(df.shape)

print("\n=== PRIMERAS FILAS ===")
print(df.head())

# ============================
# 5. Tipos de datos
# ============================
print("\n=== TIPOS DE DATOS ===")
print(df.dtypes)

# Clasificación personalizada
print("\n=== CLASIFICACIÓN DE VARIABLES ===")
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        tipo = "Numérica"
    elif pd.api.types.is_datetime64_any_dtype(df[col]):
        tipo = "Fecha"
    elif df[col].nunique() < 20:
        tipo = "Categórica"
    else:
        tipo = "Texto / Carácter"
    print(f"{col}: {tipo}")

# ============================
# 6. Valores nulos
# ============================
print("\n=== VALORES NULOS POR COLUMNA ===")
print(df.isnull().sum())

# ============================
# 7. Estadísticos básicos
# ============================
print("\n=== ESTADÍSTICOS DESCRIPTIVOS NUMÉRICOS ===")
print(df.describe())

print("\n=== FRECUENCIAS PARA VARIABLES CATEGÓRICAS ===")
for col in df.select_dtypes(include=['object', 'category']):
    print(f"\nColumna: {col}")
    print(df[col].value_counts(dropna=False))

# ============================
# 8. Detección de Outliers (Método IQR)
# ============================
print("\n=== DETECCIÓN DE OUTLIERS (IQR) ===")
for col in df.select_dtypes(include=[np.number]):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
    print(f"\n{col}: {len(outliers)} posibles outliers")

# ============================
# 9. Cerrar archivo de salida
# ============================
sys.stdout.close()
print("Análisis completado y guardado en: analisis_salud_mental.txt", file=sys.__stdout__)
