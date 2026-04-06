import numpy as np
from matplotlib import pyplot as plt
from typing import Any

import os

from normalisation import *
from caracterisation import *
import db
import knn
import time


def main():
    db_csv = "/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/database.csv"

    win = 0
    total_image = 100

    if os.path.exists(db_csv):
        database = db.charger_journal(db_csv)

    for i in range(10):
        for j in range(10):
            file = f"/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/test_image/MNIST/{i}/{i}_dataset_{j}.png"

            mon_image = (list(db.indexFile(file)), file.split("/")[-1])
            # print("Données de mon image :",mon_image)

            distances = knn.calcul_distance_total(database, mon_image)
            prediction = knn.find(distances, 5, False)

            if prediction is not None:
                if int(prediction) == int(i):
                    win += 1

    print("winrate :", float(win / total_image))


if __name__ == "__main__":
    t = time.time()
    main()
    print("\ntemps d'execution :", time.time() - t)
