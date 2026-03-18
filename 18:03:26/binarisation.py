from PIL import Image
import numpy as np
from matplotlib import pyplot as plt


def binariasation(imagePath:str) -> list[list]:
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
                coordX.append((256,256,256))
            
            # print(str(pixel)+" ", end="|")
        # print(coordX)

        pixelArray.append(coordX)

    return pixelArray


def showImage(matrix) -> None:
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.viridis)
    plt.show()


def main() -> None:
    imagePath = "MacsOCR/18:03:26/Image/imageDepart/0/0a.png"
    binaryImage = binariasation(imagePath)
    showImage(binaryImage)


if __name__ == "__main__" :
    main()