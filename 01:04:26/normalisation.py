from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math
from typing import Any


#######################
# Normalisation image #
#######################


def binariasation(imagePath: str) -> list[Any]:
    """
    Permet de binariser une image donc le chemin est passé en paramètre
    pixel noir si la moyenne de ces couleur (RVB) < 128 et blanc sinon.
    Retourne une matrice (listes python)
    """
    img = Image.open(imagePath)
    pixelArray = []

    pixels = img.load()

    if pixels is not None :

        for y in range(img.size[1]):
            coordX = []

            for x in range(img.size[0]):
                
                pixel = pixels[x,y]

                
                if isinstance(pixel, tuple):
                    colorAverage = (pixel[0] + pixel[1] + pixel[2]) / 3
                elif isinstance(pixel, (int, float)):
                    colorAverage = pixel

                if colorAverage < 128:
                    coordX.append((0, 0, 0))
                else:
                    coordX.append((255, 255, 255))

            pixelArray.append(coordX)

    return pixelArray


def regression(img) -> tuple[float, float]:
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

    return pente, float(p)


def cropping(image: Image.Image) -> Image.Image:
    pixels = image.load()

    Xmin = image.size[0]
    Ymin = image.size[1]
    Xmax = 0
    Ymax = 0

    if pixels is not None :
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                if pixels[x,y] == (0, 0, 0):
                    if x < Xmin:
                        Xmin = x
                    if x > Xmax:
                        Xmax = x
                    if y < Ymin:
                        Ymin = y
                    if y > Ymax:
                        Ymax = y

    image_recadree = image.crop((Xmin, Ymin, Xmax + 1, Ymax + 1))
    image_standardisee = image_recadree.resize((28, 28), Image.Resampling.LANCZOS)
    pixels_std = image_standardisee.load()
    if pixels_std is not None :
        for x in range(28):
            for y in range(28):
                if sum(pixels_std[x,y][:3]) / 3 < 128: # Si c'est plutôt sombre
                    pixels_std[x,y] = (0, 0, 0)        # Noir pur
                else:
                    pixels_std[x,y] = (255, 255, 255)  # Blanc pur
                    
    return image_standardisee


def rotateImage(imgMatrix, slope) -> Image.Image:
    img = np.asarray(imgMatrix, dtype=np.uint8)
    img = Image.fromarray(img)
    imgRotated = img.rotate(slope, expand=True, fillcolor=(255, 255, 255))

    return imgRotated


#######################
# Fonction principale #
#######################


def normalisation(path: str) -> Image.Image:
    binaryImage = binariasation(path)
    pente, p = regression(binaryImage)

    angle_rad = math.atan(pente)
    angle_deg = math.degrees(angle_rad)

    rotatedImage = rotateImage(binaryImage, -angle_deg)
    croppedImage = cropping(rotatedImage)
    return croppedImage
