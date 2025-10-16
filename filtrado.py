import pandas as pd
import numpy as np

# ============================
# 1. Cargar datos
# ============================
ruta_archivo = r"C:\Users\gtorr\Desktop\Universidad\malakaton\malackathon2025\SaludMental.xls"
df = pd.read_excel(ruta_archivo, engine='xlrd')

# ============================
# 2. Normalizar nombres de columnas
# ============================
df.columns = df.columns.str.lower().str.strip().str.replace(r'\s+', '_', regex=True)

# ============================
# 3. Filtrado de columnas
# ============================
# Ejemplo: solo columnas de interés
columnas_interes = [
	'comunidad_autónoma',
	'sexo',
	'edad_en_ingreso',
	'fecha_de_ingreso',
	'diagnóstico_principal',
	'categoría',
	'estancia_días',
	'reingreso',
]

# Validación: comprobar que existen las columnas seleccionadas
faltantes = [c for c in columnas_interes if c not in df.columns]
if faltantes:
	raise KeyError(
		"No se encontraron en el dataset las siguientes columnas normalizadas: "
		+ ", ".join(faltantes)
		+ "\nDisponibles: "
		+ ", ".join(df.columns)
	)

df = df[columnas_interes]

# ============================
# 4. Filtrado de filas
# ============================
# Ejemplos de filtros:
# a) Edad entre 18 y 65 (usando Edad en Ingreso)
df = df[(df['edad_en_ingreso'] >= 18) & (df['edad_en_ingreso'] <= 65)]

# b) Sexo conocido (no nulo)
df = df[df['sexo'].notnull()]

# c) (Eliminado) No existe 'puntaje_test' en el XLS — omitir este filtro

# d) Filtrado por fecha de ingreso (ajustado al rango real del dataset)
df['fecha_de_ingreso'] = pd.to_datetime(df['fecha_de_ingreso'], errors='coerce')
# Mantener datos desde 2016-01-01 (según análisis: 2016-2018)
mask_fecha = df['fecha_de_ingreso'] >= '2016-01-01'
df_filtrado_fecha = df[mask_fecha]
# Fallback: si no hay filas tras el filtro, mantener todas las filas con fecha válida
if df_filtrado_fecha.empty:
	df = df[df['fecha_de_ingreso'].notna()]
else:
	df = df_filtrado_fecha

# ============================
# 5. Eliminación de duplicados (opcional)
# ============================
df = df.drop_duplicates()

# ============================
# 6. Tratamiento de outliers (winsorización IQR)
# ============================
# Selección de columnas numéricas continuas a tratar (excluyendo códigos/categóricas numéricas)
cols_para_outliers = [c for c in ['edad_en_ingreso', 'estancia_días'] if c in df.columns]

def winsorizar_iqr(serie: pd.Series, factor: float = 1.5) -> pd.Series:
	q1 = serie.quantile(0.25)
	q3 = serie.quantile(0.75)
	iqr = q3 - q1
	limite_inf = q1 - factor * iqr
	limite_sup = q3 + factor * iqr
	return serie.clip(lower=limite_inf, upper=limite_sup)

for col in cols_para_outliers:
	df[col] = winsorizar_iqr(df[col])

# ============================
# 7. Normalización y centrado (Z-score)
# ============================
# Creamos una copia para dejar los valores originales en df
df_norm = df.copy()

cols_para_escalar = cols_para_outliers  # reutilizamos las mismas columnas continuas
for col in cols_para_escalar:
	media = df_norm[col].mean()
	std = df_norm[col].std(ddof=0)  # std poblacional (alineado con scikit-learn)
	if std and std > 0:
		df_norm[col] = (df_norm[col] - media) / std
	else:
		# Si la desviación es 0, todos iguales: poner 0s
		df_norm[col] = 0.0

# ============================
# 8. Guardar datasets (filtrado y normalizado)
# ============================
ruta_base = "C:\\Users\\gtorr\\Desktop\\Universidad\\malakaton\\malackathon2025\\"
df.to_excel(ruta_base + "SaludMental_filtrado.xlsx", index=False)
df_norm.to_excel(ruta_base + "SaludMental_filtrado_normalizado.xlsx", index=False)
df_norm.to_csv(ruta_base + "SaludMental_filtrado_normalizado.csv", index=False, encoding='utf-8')

print("Filtrado y normalización completados. Archivos guardados:")
print(" - SaludMental_filtrado.xlsx")
print(" - SaludMental_filtrado_normalizado.xlsx")
print(" - SaludMental_filtrado_normalizado.csv")
print(f"Dimensiones finales: {df.shape}")
