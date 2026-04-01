from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math
from typing import Any
from normalisation import cropping

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
