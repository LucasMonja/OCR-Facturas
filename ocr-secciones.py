import pytesseract
import numpy as np
import argparse
import imutils
import cv2
import re

#region - ARGAPRSE

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = False, help = "Path to the image to be scanned", default= 'OCR-Facturas/imagenes/Imagen_3.jpg')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
print(image.shape)
'''try:
	image = imutils.resize(image, height= 1500)
except:
	print('No se encontró una imagen para procesar.')
	exit()'''


#endregion

#region - DATOS BUSCADOS (REGEX)
REGEX_FECHA = re.compile(r'(3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])([\-/.])(\d{4}$)')
REGEX_CUIT = re.compile(r'(20|23|27|30|33)(-{0,1})([0-9]{8,9})(-{0,1})([0-9]{1}$)')
REGEX_TOTAL = re.compile(r'(TOTAL)(.*)')

#endregion

#region - OBTENER LINEAS HORIZONTALES
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)[1]
result = image.copy()
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=12)
cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#endregion

#region - VARIABLES UTILIZADAS
puntos = []
niveles = set([])
secciones = []
ocr_secciones = {}
#endregion

#region - FUNCIONES DEF
def obtener_puntos():
	for c in cnts:
		inicio = c[0][0]
		fin = c[-1][0]
		niveles.add(inicio[1])
		puntos.append((inicio[0],inicio[1]))
		puntos.append((fin[0], fin[1]))


def obtener_lineas(puntos, niveles):
	lineas = []
	for nivel in niveles:
		posibles = []
		for punto in puntos:
			if punto[1] == nivel:
				posibles.append(punto[0])
		lineas.append([(min(posibles), nivel),(max(posibles), nivel)])
	return lineas

def obtener_secciones(lineas):
	# LINEA -> [(anchura inicial, altura inicial), (anchura final, altura inicial)] 
	for i in range(len(lineas) - 1):
		if (lineas[i + 1][0][1] - lineas[i][0][1]) > 15:
			alturas = [lineas[i][0][1],lineas[i+1][0][1]]
			#anchuras = [min([lineas[i][0][0], lineas[i+1][0][0]]),max([lineas[i][1][0], lineas[i+1][1][0]])]
			#if anchuras[1] - anchuras[0] > 3500:
			#AGARRO EL ANCHO ENTERO PORQUE A VECES ME CORTABA PALABRAS MUY PEGADAS AL BORDE DEL RECUADRO
			imagen_cortada = image[alturas[0]:alturas[1], 0:image.shape[1]]
			secciones.append(imagen_cortada)

def limpiar_boxes(boxes):
    boxes_nuevo = []
    for x, box in enumerate(boxes.splitlines()):
        if x != 0:
            box = box.split()
            if len(box) == 12:
                boxes_nuevo.append(box)
    return boxes_nuevo 

def obtener_razon_social(seccion):
	nombre = seccion[0][11]
	tamaño_letra = int(seccion[0][9])
	x_coord_ini = int(seccion[0][6])
	_, ancho, _ = image.shape
	x_coord_fin = (ancho / 2) - 10
	for i in range(1,len(seccion)):
		if ((int(seccion[i][9]) <= tamaño_letra + 2) and (int(seccion[i][9]) >= tamaño_letra - 2) 
		and ((int(seccion[i][6]) >= x_coord_ini) and (int(seccion[i][6]) <= x_coord_fin))):
			nombre = nombre + ' ' + seccion[i][11]
	return nombre

def obtener_emision(seccion):
	for palabra in seccion:
		fecha = REGEX_FECHA.search(palabra[11])
		if fecha:
			return ''.join(fecha.groups())

def obtener_cuit(seccion):
	for palabra in seccion:
		cuit = REGEX_CUIT.search(palabra[11])
		if cuit:
			return ''.join(cuit.groups())

	
#endregion

#region - "MAIN"
if __name__ == "__main__":

	obtener_puntos()
	niveles = sorted(niveles)
	lineas = obtener_lineas(puntos, niveles)
	obtener_secciones(lineas)

	for sec in range(len(secciones)):
		key = 'Seccion-' + str(sec + 1)
		boxes = pytesseract.image_to_data(secciones[sec])
		ocr_secciones[key] = limpiar_boxes(boxes)
		'''cv2.imshow("Seccion", secciones[sec])
		cv2.waitKey(0)'''
	
	print(ocr_secciones)
	cv2.destroyAllWindows()


#endregion
#region - PROCESAMIENTO PALABRAS

nombre_obtenido = False
for key in ocr_secciones:
	if len(ocr_secciones[key]) > 3 and (not nombre_obtenido):
		#print(ocr_secciones[key])
		razon_social = obtener_razon_social(ocr_secciones[key])
		nombre_obtenido = True
		fecha_emision = obtener_emision(ocr_secciones[key])
		cuit = obtener_cuit(ocr_secciones[key])
		print('Razon Social: ', razon_social, ' Fecha de Emision: ', fecha_emision, ' C.U.I.T: ', cuit)

#endregion

REGEX_CUIT