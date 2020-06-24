import pytesseract
import pdf2image
import cv2
import os

pdf_path = './recursos/Conferencia.pdf'

def armar_output(imagenes):
    i = 0
    for x, page in enumerate(imagenes):
        while True:
            filename = 'Imagen_' + str(i) + '.jpg'
            if filename in os.listdir('./imagenes'):
                i += 1
                continue
            else:
                path_out = os.getcwd() + '/imagenes/' + filename
                page.save(path_out, 'JPEG')
                break


def convertir(path):
    print('Convirtiendo PDF a imágen (JPEG).')
    try:
        imagenes = pdf2image.convert_from_path(path,500)
        print('Convertido satisfactoriamente.')
    except:
        print ('Ha ocurrido un error en la conversión del PDF a imágen.')
        exit()

    armar_output(imagenes)
        
convertir(pdf_path)
    