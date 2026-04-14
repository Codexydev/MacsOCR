from PIL import Image
import numpy as np

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

    if pixels is not None:
        for i in range(image.size[0]):
            if (pixels[i, int(middle_y)] == (0, 0, 0)) != lx[-1]:
                lx.append(pixels[i, int(middle_y)] == (0, 0, 0))

        for j in range(image.size[1]):
            if (pixels[int(middle_x), j] == (0, 0, 0)) != ly[-1]:
                ly.append(pixels[int(middle_x), j] == (0, 0, 0))

    lx.append(False)
    ly.append(False)

    return (lx.count(True), ly.count(True))

def zoning_dynamique(image: Image.Image, taille_grille: int) -> list[float]:
    """
    Découpe l'image en une grille de (taille_grille x taille_grille).
    Gère automatiquement les divisions imparfaites sans perdre de pixels.
    """
    matrice = np.array(image)

    if len(matrice.shape) == 3:
        matrice = matrice[:, :, 0]

    total_noirs = np.sum(matrice == 0)
    if total_noirs == 0:
        total_noirs = 1

    densites = []

    limites = np.linspace(0, matrice.shape[0], taille_grille + 1, dtype=int)

    for i in range(taille_grille):
        for j in range(taille_grille):

            bloc = matrice[limites[i] : limites[i + 1], limites[j] : limites[j + 1]]
            noirs = np.sum(bloc == 0)
            densites.append(float(noirs) / total_noirs)

    return densites


def caracterisation(image: Image.Image, taille_grille: int = 4) -> tuple:
    x_inter, y_inter = intersect(image)

    zones = zoning_dynamique(image, taille_grille)

    largeur, hauteur = image.size
    ratio_size = float(largeur) / float(hauteur) if hauteur != 0 else 1.0

    resultat = zones + [x_inter / 5.0, y_inter / 5.0, ratio_size]

    return tuple(resultat)