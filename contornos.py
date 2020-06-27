import numpy as np
import argparse
import imutils
import cv2

image = cv2.imread('OCR-Facturas/imagenes/Imagen_3.jpg')
image = imutils.resize(image, height= 1000)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)[1]
result = image.copy()

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

puntos = []
niveles = set([])
secciones = []
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
	# LINEA -> [(altura inicial, anchura inicial), (altura inicial, anchura final)] 
	for i in range(len(lineas) - 1):
		if (lineas[i + 1][0][1] - lineas[i][0][1]) > 10:
			alturas = [lineas[i][0][1],lineas[i+1][0][1]]
			anchuras = [min([lineas[i][0][0], lineas[i+1][0][0]]),max([lineas[i][1][0], lineas[i+1][1][0]])]
			imagen_cortada = image[alturas[0]:alturas[1], anchuras[0]:anchuras[1]]
			secciones.append(imagen_cortada)

obtener_puntos()
niveles = sorted(niveles)
lineas = obtener_lineas(puntos, niveles)
obtener_secciones(lineas)
print('SECCIONES: ')
print(secciones)

for sec in secciones:
	cv2.imshow("Seccion", sec)
	cv2.waitKey(0)

cv2.destroyAllWindows()