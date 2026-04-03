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

def showImage(matrix, rotatedImage, imageCropped, pente, p) -> None:
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


def testFichier(path):
    #########################
    # import de notre image #
    #########################
    number = 7
    font = "t"
    imagePath = path

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

    print("densité : ", densite(croppedImage))
    print("densite par morceaux : ", densite_par_morceaux(croppedImage))

    showImage(binaryImage, rotatedImage, croppedImage, pente, p)

#############################
# Main du projet au complet #
#############################

def main() -> None:
    path = "/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/01:04:26/Image/MNIST"
    number_test = 1
    number_image = 5
    
    file_MNIST = f"/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/train_image/MNIST/{number_test}/{number_test}_dataset_{number_image}.png"
    file_perso = f"/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/train_image/perso/test24.png"

    file  = file_MNIST
    path_csv = '/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/database.csv'

    ############################
    # création base de données #
    ############################

    print("")
    mon_image = (list(db.indexFile(file)), file.split("/")[-1])
    print("Données de mon image :",mon_image)

    if os.path.exists(path_csv):
        print("\nChargement rapide de la base de données depuis le CSV...")
        database = db.charger_journal(path_csv)
    else:
        print("\nCalcul de la base de données en cours...")
        database = db.create_db(path)
        db.creer_journal(path_csv, database)
        print("Base de données sauvegardée dans le CSV !\n")

    print(f"Nombre d'images dans la base : {len(database)}")
    print(ratio(normalisation(file)))

    distances = knn.calcul_distance_total(database,mon_image)

    print("Prédiction :", knn.find(distances, 101, True))

    print("")
    # testFichier(file)
    # testFichier("/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/01:04:26/Image/MNIST/2/2_dataset_19.png")
if __name__ == "__main__":
    t = time.time()
    main()
    print("\ntemps d'execution :",time.time()-t)
    # testFichier("/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/train_image/perso/test24.png")