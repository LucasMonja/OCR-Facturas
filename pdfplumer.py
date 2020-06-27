import pdfplumber
import re

# Pruebo plumber que lo vi en un video que me pasó mati: 
# https://www.youtube.com/watch?v=eTz3VZmNPSE&feature=youtu.be

# FORMATO DATOS FACTURA

factura = {'Nombre_Remitente': None,
'Fecha_Emision': None,
'CUIT': None,
'Total': None
}

#CUIT propio para descartarlo en el regex
cuit_propio = ["30-61398599-5", "30613985995"]

#FLAGS

fecha_emision_obtenida = False
proximo_es_monto = False

# REGEX

REGEX_FECHA = re.compile(r'(3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])([\-/.])(\d{4}$)')
REGEX_CUIT = re.compile(r'(20|23|27|30|33)(-{0,1})([0-9]{8,9})(-{0,1})([0-9]{1}$)')
REGEX_TOTAL = re.compile(r'(TOTAL)(.*)')
REGEX_NOMBRE = r'([A-Z] )'


with pdfplumber.open('OCR-Facturas/recursos/Alarma.pdf') as pdf:
    page = pdf.pages[0]
    text = page.extract_text()

for line in text.split('\n'):
    if len(line) > 1:
        print(line)
        cuit = REGEX_CUIT.search(line)
        if cuit and not ( ''.join(cuit.groups()) in cuit_propio):
            factura['CUIT'] = ''.join(cuit.groups())
            continue
        fecha = REGEX_FECHA.search(line)
        # LA FECHA DEPENDE DE LA FACTURA, SI ES (A, B, C)
        # AHORA ESTARÍA QUEADNDO PRIMER FECHA QUE ENCUENTRA QUE SIEMPRE ES LA DE EMISION (POR LO QUE ENTIENDO)
        if fecha and not (fecha_emision_obtenida):
            factura['Fecha_Emision'] = ''.join(fecha.groups())
            fecha_obtenida = True
            continue
        monto = REGEX_TOTAL.search(line.upper())
        if monto:
            #print(line)
            factura['Total'] = monto.group(2).split(' ')[-1]
            continue
        

print(factura)