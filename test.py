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
print(image.shape[1])
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
detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#endregion

#region - VARIABLES UTILIZADAS
puntos = []
niveles = set([])
secciones = []
ocr_secciones = {}
#endregion

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

obtener_puntos()
niveles = sorted(niveles)
lineas = obtener_lineas(puntos, niveles)

'''for linea in lineas:


    cv2.imshow("Seccion", secciones[sec])
	cv2.waitKey(0)'''

print(lineas)