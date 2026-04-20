from typing import Any

import os

from normalisation import *
from caracterisation import *
import db
import knn
import time


def main():
    db_csv = "MacsOCR/database.csv"
    dataset = "ipad_dataset"
    win = 0
    k = 7
    taille_grille = 7
    affichage = True

    if os.path.exists(db_csv):
        database = db.charger_journal(db_csv)

    for i in range(10):
        for j in range(len(os.listdir(f'MacsOCR/dataset/test_image/{dataset}/{i}'))):
            file = f"MacsOCR/dataset/test_image/{dataset}/{i}/{i}_dataset_{j}.png"

            mon_image = (list(db.indexFile(file, taille_grille)), file.split("/")[-1])

            distances = knn.calcul_distance_total(database, mon_image)
            prediction = knn.find(distances, k, False)

            if prediction is not None:
                if int(prediction) == int(i):
                    win += 1
                else:
                    if affichage:
                        print(f"dataset : {dataset} | image : {file.split('/')[-1]} | prediction : {prediction} | réponse : {i}")


    print("\ndataset :", dataset)
    print("winrate :", float(win / ((i + 1) * (j + 1))))


if __name__ == "__main__":
    t = time.time()
    main()
    print("\ntemps d'execution :", time.time() - t)
