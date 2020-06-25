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
cuit_propio = "30-61398599-5"

# REGEX

REGEX_FECHA = r'(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$'
REGEX_CUIT = r'(20|23|27|30|33)-([0-9]{8}|[0-9]{9})-[0-9]{1}$'

#FLAGS

fecha_obtenida = False
proximo_es_monto = False

img = cv2.imread('OCR-Facturas/imagenes/Imagen_3.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print("Aplicando OCR")
boxes = pytesseract.image_to_data(img)
print("OCR terminado")

''' No funciona bien, solo con algunos casos
def obtener_nombre(boxes):
    nombre = ''
    for box in boxes:
        if box[11].upper() != 'FACTURA':
            nombre = nombre + box[11].upper() + ' '
        else: break
    return nombre.rstrip()
'''
def limpiar_boxes(boxes):
    boxes_nuevo = []
    for x, box in enumerate(boxes.splitlines()):
        if x != 0:
            box = box.split()
            if len(box) == 12:
                boxes_nuevo.append(box)
    return boxes_nuevo    

boxes = limpiar_boxes(boxes)
print(boxes)
#factura['Nombre_Remitente'] = obtener_nombre(boxes)

for box in boxes:
    if (re.match(REGEX_FECHA, box[11])) and (not (fecha_obtenida)):
        factura['Fecha'] = box[11]
        fecha_obtenida = True
    elif (re.match(REGEX_CUIT, box[11])) and (box[11] != cuit_propio):
        factura['CUIT'] = box[11]
    # LO QUE SIGUE ES HORRIBLE PERO QUERIA TENER ALGO PARA OBTENER TOTAL
    # SE BASA EN QUE EL ULTIMO MONTO SEGUIDO DE UN $ VA A SER EL TOTAL
    elif box[11] == '$':
        proximo_es_monto = True
    elif proximo_es_monto:
        factura['Total'] = box[11]
        proximo_es_monto = False

print(factura)
