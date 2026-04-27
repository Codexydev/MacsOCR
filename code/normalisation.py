from PIL import Image
import numpy as np
import math
from typing import Any
from skimage import morphology

#######################
# Normalisation image #
#######################


def binariasation(imagePath: str) -> list[Any]:
    """
    Convertit une image brute en une matrice binaire (Noir et Blanc).
    
    Chaque pixel est évalué selon sa luminance moyenne (RVB). S'il est 
    inférieur au seuil de 128, il devient noir (encre), sinon blanc (fond).

    Args:
        imagePath (str): Le chemin absolu ou relatif vers l'image source.

    Returns:
        list[Any]: Une matrice (liste de listes) contenant les tuples (R, V, B) 
                   binarisés de chaque pixel.
    """
    img = Image.open(imagePath)
    pixelArray = []

    pixels = img.load()

    if pixels is not None:

        for y in range(img.size[1]):
            coordX = []

            for x in range(img.size[0]):

                pixel = pixels[x, y]

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


def regression(img: list) -> tuple[float, float]:
    """
    Calcule la droite de régression linéaire de l'encre présente sur l'image.
    
    Cette fonction repère les pixels noirs et applique la méthode des moindres carrés 
    pour déterminer l'axe vertical moyen du tracé.

    Args:
        img (list): La matrice de pixels représentant l'image binarisée.

    Returns:
        tuple[float, float]: Un tuple contenant le coefficient directeur (la pente) 
                             et l'ordonnée à l'origine de la droite.
    """
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

def rotateImage(imgMatrix: list, slope: float) -> Image.Image:
    """
    Applique une rotation à la matrice de pixels pour redresser le caractère.

    Args:
        imgMatrix (list): La matrice binaire de l'image d'origine.
        slope (float): L'angle de rotation (en degrés) à appliquer.

    Returns:
        Image.Image: L'objet image redressé, avec un remplissage blanc pour les marges créées.
    """
    img = np.asarray(imgMatrix, dtype=np.uint8)
    img = Image.fromarray(img)
    imgRotated = img.rotate(slope, expand=True, fillcolor=(255, 255, 255))

    return imgRotated

def cropping(image: Image.Image) -> Image.Image:
    """
    Recadre et redimensionne une image pour l'adapter à un format standard.
    
    L'algorithme coupe les marges blanches inutiles (bounding box), puis 
    redimensionne le tracé de manière proportionnelle avec un filtre de Lanczos 
    pour l'insérer au centre d'une matrice stricte de 28x28 pixels.

    Args:
        image (Image.Image): L'objet image redressé à recadrer.

    Returns:
        Image.Image: La nouvelle image normalisée au format 28x28 pixels et re-binarisée.
    """
    pixels = image.load()

    Xmin = image.size[0]
    Ymin = image.size[1]
    Xmax = 0
    Ymax = 0

    if pixels is not None:
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                if pixels[x, y] == (0, 0, 0):
                    if x < Xmin:
                        Xmin = x
                    if x > Xmax:
                        Xmax = x
                    if y < Ymin:
                        Ymin = y
                    if y > Ymax:
                        Ymax = y

    if Xmin > Xmax or Ymin > Ymax:
        return image

    image_recadree = image.crop((Xmin, Ymin, Xmax + 1, Ymax + 1))

    image_recadree.thumbnail((28, 28), Image.Resampling.LANCZOS)
    image_standardisee = Image.new("RGB", (28, 28), color=(255, 255, 255))
    pos_x = (28 - image_recadree.size[0]) // 2
    pos_y = (28 - image_recadree.size[1]) // 2
    image_standardisee.paste(image_recadree, (pos_x, pos_y))

    pixels_std = image_standardisee.load()

    if pixels_std is not None:
        for x in range(28):
            for y in range(28):
                pixel = pixels_std[x, y]

                if isinstance(pixel, tuple):
                    moyenne = sum(pixel[:3]) / 3
                elif isinstance(pixel, (int, float)):
                    moyenne = float(pixel)
                else:
                    moyenne = 255.0

                if moyenne < 128:
                    pixels_std[x, y] = (0, 0, 0)
                else:
                    pixels_std[x, y] = (255, 255, 255)

    return image_standardisee


#######################
# Fonction principale #
#######################


def normalisation(path: str) -> Image.Image:
    """
    Exécute le pipeline complet de normalisation sur une image.
    
    Enchaîne la binarisation, le calcul de régression, le redressement par rotation 
    et enfin le recadrage à 28x28 pixels.

    Args:
        path (str): Le chemin du fichier image à traiter.

    Returns:
        Image.Image: L'image finale normalisée et prête pour l'extraction de caractéristiques.
    """
    binaryImage = binariasation(path)
    pente, p = regression(binaryImage)

    angle_rad = math.atan(pente)
    angle_deg = math.degrees(angle_rad)

    rotatedImage = rotateImage(binaryImage, -angle_deg)
    croppedImage = cropping(rotatedImage)
    return croppedImage
