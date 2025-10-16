# ============================
# 1. Importar librerías
# ============================
import pandas as pd
import numpy as np

# ============================
# 2. Cargar el archivo Excel
# ============================
# Cambia la ruta por la de tu archivo
ruta_archivo = "SaludMental.xls"  # Puede ser .xls o .xlsx
df = pd.read_excel(ruta_archivo)

# ============================
# 3. Vista general del dataset
# ============================
print("=== DIMENSIONES DEL DATAFRAME ===")
print(df.shape)

print("\n=== PRIMERAS FILAS ===")
print(df.head())

# ============================
# 4. Tipos de datos
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
# 5. Valores nulos
# ============================
print("\n=== VALORES NULOS POR COLUMNA ===")
print(df.isnull().sum())

# ============================
# 6. Estadísticos básicos
# ============================
print("\n=== ESTADÍSTICOS DESCRIPTIVOS NUMÉRICOS ===")
print(df.describe())

print("\n=== FRECUENCIAS PARA VARIABLES CATEGÓRICAS ===")
for col in df.select_dtypes(include=['object', 'category']):
    print(f"\nColumna: {col}")
    print(df[col].value_counts(dropna=False))

# ============================
# 7. Detección de Outliers (Método IQR)
# ============================
print("\n=== DETECCIÓN DE OUTLIERS (IQR) ===")
for col in df.select_dtypes(include=[np.number]):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
    print(f"\n{col}: {len(outliers)} posibles outliers")

