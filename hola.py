from fpdf import FPDF

# Crear clase PDF personalizada
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Reporte de Escaneo - ZAP por Checkmarx", ln=True, align="C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(2)

    def chapter_body(self, body):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_section(self, title, body):
        self.chapter_title(title)
        self.chapter_body(body)

# Instanciar PDF
pdf = PDF()
pdf.add_page()

# Secciones del reporte traducidas
pdf.add_section("Acerca del Reporte", 
"""Reporte generado con ZAP por Checkmarx el lunes 14 de abril de 2025, a las 23:53:08
Versión de ZAP: 2.16.0

Parámetros del reporte:
- Contextos: no se seleccionaron, se incluyeron todos por defecto.
- Sitios incluidos: http://pruebas4.factury.mx
- Niveles de riesgo incluidos: Alto, Medio, Bajo, Informativo
- Niveles de confianza incluidos: Confirmado por el usuario, Alta, Media, Baja""")

pdf.add_section("Resumen de Alertas por Riesgo y Confianza", 
"""Nivel de Riesgo | Confirmado | Alta | Media | Baja | Total
Medio            |     0      |  2   |  1    |  1   |   4
Bajo             |     0      |  0   |  1    |  0   |   1
Informativo      |     0      |  0   |  2    |  2   |   4
Total: 9 alertas""")

pdf.add_section("Resumen de Alertas por Sitio y Riesgo", 
"""Sitio: http://pruebas4.factury.mx
- Riesgo Medio: 4
- Riesgo Bajo: 1
- Informativo: 4""")

pdf.add_section("Resumen de Alertas por Tipo", 
"""- Falta de tokens Anti-CSRF: Medio (2)
- Encabezado CSP no establecido: Medio (1)
- Archivo oculto encontrado: Medio (1)
- Falta encabezado Anti-clickjacking: Medio (1)
- Falta encabezado X-Content-Type-Options: Bajo (1)
- Solicitud de autenticación detectada: Informativo (1)
- Divulgación de información sensible en URL: Informativo (1)
- Comentarios sospechosos: Informativo (2)
- Aplicación web moderna: Informativo (2)""")

pdf.add_section("Alertas Detalladas", 
"""Medio, Alta (2):
- Encabezado CSP no establecido: GET /Facturación_files/WebResource(2).axd
- Archivo oculto encontrado: GET /i.php

Medio, Media (1):
- Falta encabezado Anti-clickjacking: GET /

Medio, Baja (1):
- Falta de token Anti-CSRF: GET /index.php?session=false

Bajo, Media (1):
- Falta encabezado X-Content-Type-Options: GET /resources/images/logos/ra4.png

Informativo, Media (2):
- Información sensible en URL: GET /index.php?session=false
- Aplicación web moderna: GET /

Informativo, Baja (2):
- Solicitud de autenticación: POST /sesion.php
- Comentarios sospechosos: GET /resources/js/jquery/jquery.min.js""")

pdf.add_section("Apéndice - Tipos de Alerta", 
"""- Falta de tokens Anti-CSRF: CWE 352, WASC 9
- CSP no establecido: CWE 693, WASC 15
- Archivo oculto: CWE 538, WASC 13
- Falta encabezado Anti-clickjacking: CWE 1021, WASC 15
- Falta encabezado X-Content-Type-Options: CWE 693, WASC 15
- Solicitud de autenticación: identificación de patrones de login
- Información sensible en URL: CWE 598, WASC 13
- Comentarios sospechosos: CWE 615, WASC 13
- Aplicación web moderna: indicador de stack moderno""")

# Guardar el PDF
pdf.output("reporte_zap_checkmarx.pdf")
pdf_path
