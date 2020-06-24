import re
import cv2
import pytesseract

# FORMATO DATOS FACTURA

factura = {'Nombre_Remitente': None,
'Fecha': None,
'CUIT': None,
'Total': None
}

#CUIT propio para descartarlo en el regex
cuit_propio = ["30-61398599-5", "30613985995"]

# REGEX

REGEX_FECHA = re.compile(r'(3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])([\-/.])(\d{4}$)')
REGEX_CUIT = re.compile(r'(20|23|27|30|33)-{0,1}([0-9]{8}|[0-9]{9})-{0,1}[0-9]{1}$')
REGEX_TOTAL = re.compile(r'(Importe Total: )(.*)')
REGEX_NOMBRE = r'([A-Z] )'

#FLAGS

fecha_obtenida = False
proximo_es_monto = False

img = cv2.imread('OCR-Facturas/imagenes/Imagen_0.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print("Aplicando OCR")
boxes = pytesseract.image_to_string(img)
print("OCR terminado")


# REGEX

REGEX_FECHA = re.compile(r'(3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])([\-/.])(\d{4}$)')
REGEX_CUIT = re.compile(r'(20|23|27|30|33)-{0,1}([0-9]{8}|[0-9]{9})-{0,1}[0-9]{1}$')
REGEX_TOTAL = re.compile(r'(Importe Total: )(.*)')
REGEX_NOMBRE = r'([A-Z] )'

for line in boxes.split('\n'):
    if len(line) > 1:
        #print(line)
        cuit = REGEX_CUIT.search(line)
        if cuit and not ( ''.join(cuit.groups()) in cuit_propio):
            factura['CUIT'] = ''.join(cuit.groups())
            continue
        fecha = REGEX_FECHA.search(line)
        # LA FECHA DEPENDE DE LA FACTURA, SI ES (A, B, C)
        # AHORA ESTARÍA QUEADNDO LA ÚLTIMA FECHA QUE ENCUENTRA
        if fecha and not (fecha_obtenida):
            factura['Fecha'] = ''.join(fecha.groups())
            fecha_obtenida = True
            continue
        monto = REGEX_TOTAL.search(line)
        if monto:
            factura['Total'] = monto.group(2).split(' ')[-1]
            continue
        

print(factura)
        
