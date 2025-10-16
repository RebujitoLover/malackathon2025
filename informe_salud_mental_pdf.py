from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
import os

base_path = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(base_path, "informe_salud_mental.pdf")

doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
styles = getSampleStyleSheet()
styleN = styles["Normal"]
styleH = styles["Heading1"]
styleH2 = styles["Heading2"]
styleH3 = styles["Heading3"]

story = []

story.append(Paragraph("Informe de Análisis de Datos de Salud Mental", styleH))
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("1. Análisis descriptivo inicial", styleH2))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Dimensiones y estructura:</b> El dataset contiene <b>21,210 filas</b> y <b>111 columnas</b>.", styleN))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>Tipos de variables:</b>", styleN))
var_types = [
    "Fechas: Fecha de nacimiento, Fecha de Ingreso, Fecha de Fin Contacto, etc.",
    "Carácter/Textos: Nombre, Diagnóstico Principal, Servicio, Centro Recodificado, etc.",
    "Categóricas: Comunidad Autónoma, Categoría, Procedimiento 9-20, POA Diagnóstico 1-20, etc.",
    "Numéricas: Sexo, Edad, Edad en Ingreso, Estancia Días, Reingreso, Coste APR, etc."
]
for vt in var_types:
    story.append(Paragraph(f"- {vt}", styleN))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>Valores nulos o desconocidos:</b> Algunas columnas presentan valores nulos en todos los registros (ejemplo: CCAA Residencia, Procedimiento Externo 6). Otras columnas clave no presentan nulos (ejemplo: Comunidad Autónoma, Nombre, Fecha de nacimiento, Sexo, Edad en Ingreso).", styleN))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>Estadísticos básicos:</b>", styleN))
data = [["Variable", "Media", "Mínimo", "Máximo", "Desviación estándar"],
        ["Edad en Ingreso", "43.7", "0", "96", "14.1"],
        ["Sexo", "1.45", "1", "9", "0.56"]]
table = Table(data, hAlign='LEFT')
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0,0), (-1,0), 8),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
]))
story.append(table)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Outliers:</b>", styleN))
outliers = [
    "Estancia Días: 1,229 posibles outliers",
    "Edad en Ingreso: 149 posibles outliers",
    "Otros: Coste APR, Riesgo Mortalidad APR, etc."
]
for o in outliers:
    story.append(Paragraph(f"- {o}", styleN))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Gráficas:</b>", styleN))
img1 = os.path.join(base_path, "hist_edad.png")
img2 = os.path.join(base_path, "hist_estancia.png")
if os.path.exists(img1):
    story.append(Image(img1, width=14*cm, height=8*cm))
    story.append(Paragraph("Distribución de Edad en Ingreso", styleN))
    story.append(Spacer(1, 0.3*cm))
if os.path.exists(img2):
    story.append(Image(img2, width=14*cm, height=8*cm))
    story.append(Paragraph("Distribución de Estancia Días", styleN))
    story.append(Spacer(1, 0.3*cm))

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("2. Ingeniería de características", styleH2))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Creación de nuevas variables:</b>", styleN))
new_vars = [
    "Edad agrupada: Agrupar Edad en Ingreso en rangos (ejemplo: 0-18, 19-30, 31-50, 51+)",
    "Año de ingreso: Extraer el año de la columna Fecha de Ingreso",
    "Duración estancia categorizada: Categorizar Estancia Días (ejemplo: corta, media, larga)"
]
for nv in new_vars:
    story.append(Paragraph(f"- {nv}", styleN))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>Transformaciones:</b>", styleN))
transforms = [
    "Normalización y centrado: Aplicar Z-score a Edad en Ingreso y Estancia Días",
    "Winsorización: Limitar valores extremos en variables continuas"
]
for t in transforms:
    story.append(Paragraph(f"- {t}", styleN))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>Codificación:</b>", styleN))
codes = [
    "Sexo binario: 1=Hombre, 2=Mujer → 0/1",
    "One-hot encoding: Para Comunidad Autónoma, Categoría, etc."
]
for c in codes:
    story.append(Paragraph(f"- {c}", styleN))
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("Este informe resume el análisis inicial y las propuestas de ingeniería de variables para el dataset de salud mental. Para detalles completos, consultar el archivo analisis_salud_mental.txt y los scripts de procesamiento.", styleN))

# Genera el PDF
if __name__ == "__main__":
    doc.build(story)
    print(f"PDF generado: {pdf_path}")
