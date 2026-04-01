from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math
from typing import Any


def binariasation(imagePath: str) -> list[Any]:
    """
    Permet de binariser une image donc le chemin est passé en paramètre
    pixel noir si la moyenne de ces couleur (RVB) < 128 et blanc sinon.
    Retourne une matrice (listes python)
    """
    img = Image.open(imagePath)
    pixelArray = []

    for y in range(img.size[1]):
        coordX = []

        for x in range(img.size[0]):
            pixel = img.getpixel((x, y))

            if isinstance(pixel, tuple):
                colorAverage = (pixel[0] + pixel[1] + pixel[2]) / 3
            elif isinstance(pixel, (int, float)):
                colorAverage = pixel

            if colorAverage < 128:
                coordX.append((0, 0, 0))
            else:
                coordX.append((255, 255, 255))

            # print(str(pixel)+" ", end="|")
        # print(coordX)

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


def rotateImage(imgMatrix, slope) -> Image.Image:
    img = np.asarray(imgMatrix, dtype=np.uint8)
    img = Image.fromarray(img)
    imgRotated = img.rotate(slope, expand=True, fillcolor=(255, 255, 255))

    return imgRotated


def cropping(image:Image.Image) -> Image.Image:
    Xmin = image.size[0]
    Ymin = image.size[1]
    Xmax = 0
    Ymax = 0

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if image.getpixel((x, y)) == (0, 0, 0):
                if x < Xmin:
                    Xmin = x
                if x > Xmax:
                    Xmax = x
                if y < Ymin:
                    Ymin = y
                if y > Ymax:
                    Ymax = y

    return image.crop((Xmin, Ymin, Xmax + 1, Ymax + 1))


def intersect(image: Image.Image) -> tuple[int, int]:
    middle_x = image.size[0] / 2
    middle_y = image.size[1] / 2

    lx = [False]
    ly = [False]

    for i in range(image.size[0]):
        if (image.getpixel((i, int(middle_y))) == (0, 0, 0)) != lx[-1]:
            lx.append(image.getpixel((i, int(middle_y))) == (0, 0, 0))

    for j in range(image.size[1]):
        if (image.getpixel((int(middle_x), j)) == (0, 0, 0)) != ly[-1]:
            ly.append(image.getpixel((int(middle_x), j)) == (0, 0, 0))

    lx.append(False)
    ly.append(False)

    return (lx.count(True), ly.count(True))


def showImage(matrix, rotatedImage, imageCropped, pente, p) -> None:
    figure = plt.figure()

    im1 = figure.add_subplot(1, 3, 1)
    im1.imshow(matrix, interpolation="nearest")

    hauteur = len(matrix)
    y_vals = np.linspace(0, hauteur - 1, 100)
    x_vals = pente * y_vals + p

    im1.plot(x_vals, y_vals, "-r")
    im1.set_title("Image d'origine + Régression")

    im2 = figure.add_subplot(1, 3, 2)
    im2.imshow(rotatedImage, interpolation="nearest")
    im2.set_title("Image redressée")

    im3 = figure.add_subplot(1, 3, 3)
    im3.imshow(imageCropped, interpolation="nearest")
    im3.set_title("Image cropped")

    plt.show()


def densité(image) -> Any | int:
    largeur = image.size[0]
    hauteur = image.size[1]
    nb_pixels_noirs = 0
    nb_pixels_total = largeur * hauteur

    for i in range(largeur):
        for j in range(hauteur):
            if image.getpixel((i, j)) == (0, 0, 0):
                nb_pixels_noirs += 1

    if nb_pixels_total == 0:
        return 0
    else:
        return nb_pixels_noirs / nb_pixels_total


def densité_par_morceaux(image) -> tuple[Any | int, Any | int, Any | int, Any | int]:
    largeur = image.size[0]
    hauteur = image.size[1]

    img = cropping(image)

    img_hg = img.crop(
        (0, 0, (largeur // 2 + largeur // 10), (hauteur // 2 + hauteur // 10))
    )
    img_hd = img.crop(
        ((largeur // 2 - largeur // 10), 0, largeur, (hauteur // 2 + hauteur // 10))
    )
    img_bg = img.crop(
        (0, (hauteur // 2 - hauteur // 10), (largeur // 2 + largeur // 10), hauteur)
    )
    img_bd = img.crop(
        (
            (largeur // 2 - largeur // 10),
            (hauteur // 2 - hauteur // 10),
            largeur,
            hauteur,
        )
    )

    densite_hg = densité(img_hg)
    densite_hd = densité(img_hd)
    densite_bg = densité(img_bg)
    densite_bd = densité(img_bd)

    return (densite_bg, densite_bd, densite_hg, densite_hd)


def main() -> None:
    number = 7
    font = "t"
    imagePath = f"MacsOCR/25:03:26/Image/imageDepart/{number}/{number}{font}.png"
    binaryImage = binariasation(imagePath)

    pente, p = regression(binaryImage)

    angle_rad = math.atan(pente)
    angle_deg = math.degrees(angle_rad)
    print("Angle : ", angle_deg)

    rotatedImage = rotateImage(binaryImage, -angle_deg)
    croppedImage = cropping(rotatedImage)

    print("Nombre intersection en x et y :", intersect(croppedImage))

    print("densité : ", densité(croppedImage))
    print("densite par morceaux : ", densité_par_morceaux(croppedImage))

    showImage(binaryImage, rotatedImage, croppedImage, pente, p)


if __name__ == "__main__":
    main()
