import numpy as np
from matplotlib import pyplot as plt
import math
from typing import Any

import time

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


def testFichier():
    #########################
    # import de notre image #
    #########################
    number = 7
    font = "t"
    imagePath = f"MacsOCR/25:03:26/Image/imageDepart/{number}/{number}{font}.png"

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
    path = "MacsOCR/01:04:26/Image/imageDepart"
    file = "/Users/antoine/Documents/etude/l2/s4/MaCs/projet/image_test/test24.png"
    ############################
    # création base de données #
    ############################

    mon_image = (list(db.indexFile(file)), file.split("/")[-1])
    print(mon_image)

    database = db.create_db(path)

    distances = knn.calcul_distance_total(database,mon_image)

    print(knn.find(distances, k=3))
    
    # print(database)


if __name__ == "__main__":
    t = time.time()
    main()
    print("temps :",time.time()-t)