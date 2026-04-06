from typing import Any
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math

from normalisation import cropping

##################################
# Caractérisation de notre image #
##################################


def intersect(image: Image.Image) -> tuple[int, int]:
    middle_x = image.size[0] / 2
    middle_y = image.size[1] / 2

    lx = [False]
    ly = [False]

    pixels = image.load()

    if pixels is not None :
        for i in range(image.size[0]):
            if (pixels[i, int(middle_y)] == (0, 0, 0)) != lx[-1]:
                lx.append(pixels[i, int(middle_y)] == (0, 0, 0))

        for j in range(image.size[1]):
            if (pixels[int(middle_x), j] == (0, 0, 0)) != ly[-1]:
                ly.append(pixels[int(middle_x), j] == (0, 0, 0))

    lx.append(False)
    ly.append(False)

    return (lx.count(True), ly.count(True))


def compter_pixels_noirs(image: Image.Image) -> int:
    """Fonction utilitaire pour compter uniquement les pixels noirs d'une image"""
    largeur = image.size[0]
    hauteur = image.size[1]
    nb_pixels_noirs = 0

    pixels = image.load()
    if pixels is not None :
        for i in range(largeur):
            for j in range(hauteur):
                if pixels[i,j] == (0, 0, 0):
                    nb_pixels_noirs += 1
                
    return nb_pixels_noirs


def densite(image: Image.Image) -> float:
    """Densité globale : ratio de noir par rapport à la taille totale de l'image"""
    nb_pixels_total = image.size[0] * image.size[1]
    nb_pixels_noirs = compter_pixels_noirs(image)

    if nb_pixels_total == 0:
        return 0.0
    else:
        return float(nb_pixels_noirs) / float(nb_pixels_total)


def densite_par_morceaux(image: Image.Image)  -> tuple[float, float, float, float, float, float, float, float]:
    """Répartition de l'encre : pourcentage de noir dans chaque quadrant par rapport à l'encre totale"""
    largeur = image.size[0]
    hauteur = image.size[1]

    img = cropping(image)
    
    total_noirs = compter_pixels_noirs(img)
    if total_noirs == 0:
        total_noirs = 1 

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

    img_h = img.crop((0,0,largeur, hauteur//2 + hauteur//10))
    img_b = img.crop((0, hauteur//2 - hauteur//10, largeur, hauteur))

    img_g = img.crop((0,0,largeur//2 + largeur//10, hauteur))
    img_d = img.crop((largeur//2 - largeur//10, 0, largeur, hauteur))

    densite_hg = compter_pixels_noirs(img_hg) / total_noirs
    densite_hd = compter_pixels_noirs(img_hd) / total_noirs
    densite_bg = compter_pixels_noirs(img_bg) / total_noirs
    densite_bd = compter_pixels_noirs(img_bd) / total_noirs

    densite_h = compter_pixels_noirs(img_h) / total_noirs
    densite_b = compter_pixels_noirs(img_b) / total_noirs

    densite_g = compter_pixels_noirs(img_g) / total_noirs
    densite_d = compter_pixels_noirs(img_d) / total_noirs


    return (densite_hg, densite_hd, densite_bg, densite_bd, densite_h,densite_b, densite_g, densite_d)

def zoning_4x4(image: Image.Image) -> list[float]:
    """
    Découpe l'image 28x28 en 16 blocs de 7x7 pixels.
    Calcule la densité d'encre pour chaque bloc de manière ultra-rapide avec Numpy.
    """
    matrice = np.array(image)

    if len(matrice.shape) == 3:
        matrice = matrice[:, :, 0]

    total_noirs = np.sum(matrice == 0)
    if total_noirs == 0:
        total_noirs = 1

    densites_zones = []

    hauteur_bloc = matrice.shape[0] // 4
    largeur_bloc = matrice.shape[1] // 4
    
    for ligne in range(4):
        for col in range(4):
            bloc = matrice[
                ligne * hauteur_bloc : (ligne + 1) * hauteur_bloc,
                col * largeur_bloc : (col + 1) * largeur_bloc
            ]

            noirs_bloc = np.sum(bloc == 0)
            densites_zones.append(float(noirs_bloc) / total_noirs)

    return densites_zones

def caracterisation(image: Image.Image) -> tuple:
    x_inter, y_inter = intersect(image)
    
    zones = zoning_4x4(image)

    largeur, hauteur = image.size
    ratio_size = float(largeur) / float(hauteur) if hauteur != 0 else 1.0

    resultat = zones + [x_inter / 5.0, y_inter / 5.0, ratio_size]

    return tuple(resultat)

def ratio(image:Image.Image):
    return image.size

#######################
# Fonction principale #
#######################


# def caracterisation(img: Image.Image,) -> Any:
#     dens = densite(img)

#     (hg, hd, bg, bd, h, b, g, d) = densite_par_morceaux(img)
#     (inter_x, inter_y) = intersect(img)

#     (size_x,size_y) = ratio(img)
#     ratio_size = float(size_x) / float(size_y)

#     return (dens, hg, hd, bg, bd, h, b, g, d, inter_x / 8.0, inter_y / 8.0, ratio_size)