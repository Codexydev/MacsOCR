from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math


def binariasation(imagePath:str):
    '''
    Permet de binariser une image donc le chemin est passé en paramètre
    pixel noir si la moyenne de ces couleur (RVB) < 128 et blanc sinon.
    Retourne une matrice (listes python)
    '''
    img = Image.open(imagePath)
    pixelArray  = []

    for y in range(img.size[1]):
        coordX = []

        for x in range(img.size[0]):    
            pixel = img.getpixel((x,y))
            colorAverage = ( pixel[0] + pixel[1] + pixel[2] ) / 3

            if colorAverage < 128:
                coordX.append((0,0,0))
            else :
                coordX.append((255,255,255))
            
            # print(str(pixel)+" ", end="|")
        # print(coordX)

        pixelArray.append(coordX)

    return pixelArray


def regression(img):
    x = []
    y = []

    for i in range(len(img)):
        for j in range(len(img[0])):
            r, v, b = img[i][j]
            if r < 128 or v < 128 or b < 128: 
                x.append(j) 
                y.append(i) 

    xa = np.array(x)
    ya = np.array(y)
    x_moy = np.mean(xa)
    y_moy = np.mean(ya)

    pente = np.sum((xa - x_moy) * (ya - y_moy)) / np.sum((ya - y_moy) ** 2)

    p = x_moy - pente * y_moy

    return pente, p

def rotateImage(imgMatrix, slope) -> None :
    img = np.asarray(imgMatrix, dtype=np.uint8)
    img = Image.fromarray(img)
    imgRotated = img.rotate(slope, fillcolor=(255,255,255))

    return imgRotated


def showImage(matrix, rotatedImage, pente, p) -> None:
    figure = plt.figure()

    im1 = figure.add_subplot(1, 2, 1)
    im1.imshow(matrix, interpolation='nearest')

    hauteur = len(matrix)
    y_vals = np.linspace(0, hauteur - 1, 100)
    x_vals = pente * y_vals + p
    
    im1.plot(x_vals, y_vals, '-r')
    im1.set_title("Image d'origine + Régression")

    im2 = figure.add_subplot(1, 2, 2)
    im2.imshow(rotatedImage, interpolation='nearest')
    im2.set_title("Image redressée")

    plt.show()


def main() -> None:
    number = 2
    font = "t"
    imagePath = f"MacsOCR/25:03:26/Image/imageDepart/{number}/{number}{font}.png"
    binaryImage = binariasation(imagePath)

    pente, p = regression(binaryImage)
    
    angle_rad = math.atan(pente)
    angle_deg = math.degrees(angle_rad)
    print("Angle : ",angle_deg)

    rotatedImage = rotateImage(binaryImage, -angle_deg)

    showImage(binaryImage, rotatedImage, pente, p)


if __name__ == "__main__" :
    main()