from PIL import Image
import numpy as np

##################################
# Caractérisation de notre image #
##################################


def intersect(image: Image.Image) -> tuple[int, int]:
    """
    Analyse les intersections du chiffre via ses axes médians.

    L'algorithme trace un axe horizontal et un axe vertical au centre de l'image 
    et compte le nombre de transitions (fond blanc vers encre noire).

    Args:
        image (Image.Image): L'image normalisée de 28x28 pixels.

    Returns:
        tuple[int, int]: Le nombre d'intersections sur l'axe X (horizontal) 
                         et sur l'axe Y (vertical).
    """
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
    Extrait la densité spatiale de l'encre (Zoning) selon une grille définie.

    Découpe l'image en blocs (ex: 7x7) et calcule pour chaque bloc la proportion 
    d'encre relative par rapport à la quantité totale d'encre du caractère.

    Args:
        image (Image.Image): L'image normalisée de 28x28 pixels.
        taille_grille (int): Le nombre de subdivisions par côté (ex: 7 pour une grille de 49 zones).

    Returns:
        list[float]: Une liste contenant les densités relatives de chaque bloc (valeurs entre 0 et 1).
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


def caracterisation(image: Image.Image, taille_grille: int = 4) -> tuple[float, ...]:
    """
    Génère le vecteur de caractéristiques mathématiques complet du chiffre.

    Concatène les densités du zoning, les intersections normalisées et le ratio 
    de forme (largeur/hauteur) pour créer une signature numérique.

    Args:
        image (Image.Image): L'image normalisée à analyser.
        taille_grille (int, optional): La dimension du zoning. Par défaut à 4.

    Returns:
        tuple[float, ...]: Le vecteur multidimensionnel représentant l'image 
                           (généralement de dimension 52 pour une grille 7x7).
    """
    x_inter, y_inter = intersect(image)

    zones = zoning_dynamique(image, taille_grille)

    largeur, hauteur = image.size
    ratio_size = float(largeur) / float(hauteur) if hauteur != 0 else 1.0

    resultat = zones + [x_inter / 5.0, y_inter / 5.0, ratio_size]

    return tuple(resultat)
