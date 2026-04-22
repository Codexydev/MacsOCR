from email.mime import image
from turtle import listen

from matplotlib.patheffects import Normal
import numpy as np
from matplotlib import pyplot as plt
import math
from typing import Any

import time
import os

# import perso
from normalisation import *
from caracterisation import *
import db
import knn

###################
# Affichage Image #
###################


def showImage(
    matrix: list[Any],
    rotatedImage: Image.Image,
    imageCropped: Image.Image,
    pente: float,
    p: float,
) -> None:
    """
    Affiche notre image
    """
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


###############################
# Test complet sur in fichier #
###############################


def NormalisationFichier(imagePath: str) -> None:
    ################################
    # normalisation de notre image #
    ################################

    binaryImage = binariasation(imagePath)
    pente, p = regression(binaryImage)

    angle_rad = math.atan(pente)
    angle_deg = math.degrees(angle_rad)
    print("Angle : ", angle_deg)

    rotatedImage = rotateImage(binaryImage, -angle_deg)
    croppedImage = cropping(rotatedImage)

    ##################################
    # Caractérisation de notre image #
    ##################################

    print("Nombre intersection en x et y :", intersect(croppedImage))

    showImage(binaryImage, rotatedImage, croppedImage, pente, p)


############################
# création base de données #
############################


def CreateDb(
    dataset: str, k: int, db_csv: str, taille_grille: int, recalcul_db: bool
) -> list[tuple[list[float], str]]:
    print("")

    if os.path.exists(db_csv) and not recalcul_db:
        print("\nChargement rapide de la base de données depuis le CSV...")
        database = db.charger_journal(db_csv)
    else:
        os.remove(db_csv) if os.path.exists(db_csv) else None
        print("\nCalcul de la base de données en cours...")
        database = db.create_db(dataset, taille_grille)
        db.creer_journal(db_csv, database, taille_grille)
        print("Base de données sauvegardée dans le CSV !\n")

    return database
    # print(f"Nombre d'images dans la base : {len(database)}")


#############################
# Main du projet au complet #
#############################


def main() -> None:
    dataset = "ipad_dataset_train"
    k = 3
    taille_grille = 7
    db_csv = "MacsOCR/database.csv"
    dataset_train = f"MacsOCR/dataset/train/{dataset}/"
    recalcule_db = False

    number_test = 1
    number_image = 5
    file_dt = f"MacsOCR/dataset/test_image/{dataset}/{number_test}/{number_test}_dataset_{number_image}.png"
    file_perso = f"MacsOCR/dataset/test_image/perso/73.jpeg"
    file = file_perso

    database = CreateDb(dataset_train, k, db_csv, taille_grille, recalcule_db)

    ##################################
    # prédiction de notre image test #
    ##################################

    mon_image = (
        list(db.indexFile(file, taille_grille)),
        file.split("/")[-1],
    )
    # print("Données de mon image :",mon_image)

    distances = knn.calcul_distance_total(database, mon_image)
    print("dataset :", dataset)
    print("Prédiction :", knn.find(distances, k, True))
    print("réponse :", file.split("/")[-1][0])
    print("")

    # NormalisationFichier(file)


if __name__ == "__main__":
    t = time.time()
    main()
    print("\ntemps d'execution :", time.time() - t)
    # NormalisationFichier("MacsOCR/dataset/test_image/perso/22.png")
