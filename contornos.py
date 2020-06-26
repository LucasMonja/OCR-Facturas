import argparse
import imutils
import cv2

image = cv2.imread('OCR-Facturas/imagenes/Imagen_0.jpg')
image = imutils.resize(image, height= 1000)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)[1]

# LOS CONTORNOS LOS ENCUENTRA DE ARRIBA HACIA ABAJO (DE LA IMAGEN)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image.copy()

print(len(cnts))
for c in cnts:
	ejemplo = image.copy()
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	if (len(approx) == 4) and (peri > 500):
		'''for p in approx:
			cv2.circle(ejemplo, p,1,(0,0,255), -1)'''
		cv2.drawContours(output, [c], -1, (0, 255, 0), 2)
		cv2.drawContours(ejemplo, [c], -1, (0, 255, 0), 2)
		cv2.imshow("Ej", ejemplo)
		cv2.waitKey(0)
'''		
# we apply erosions to reduce the size of foreground objects
mask = thresh.copy()
mask = cv2.erode(mask, None, iterations=5)

# similarly, dilations can increase the size of the ground objects
mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations=5)

# a typical operation we may want to apply is to take our mask and
# apply a bitwise AND to our input image, keeping only the masked
# regions
mask = thresh.copy()
output = cv2.bitwise_and(image, image, mask=mask)'''
cv2.imshow("Output", output)
cv2.waitKey(0)
cv2.destroyAllWindows()