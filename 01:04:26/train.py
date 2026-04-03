from hashlib import file_digest

import numpy as np
from matplotlib import pyplot as plt
from typing import Any

import os

from normalisation import *
from caracterisation import *
import db
import knn


path = "/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/01:04:26/Image/MNIST"
path_csv = '/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/database.csv'

win = 0
total_image = 100

if os.path.exists(path_csv):
    database = db.charger_journal(path_csv)

for i in range(0,9):
    for j in range(10):

        file = f"/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/train_image/MNIST/{i}/{i}_dataset_{j}.png"

        print("")
        mon_image = (list(db.indexFile(file)), file.split("/")[-1])
        # print("Données de mon image :",mon_image)

        distances = knn.calcul_distance_total(database,mon_image)

        prediction = knn.find(distances, 101)

        if int(prediction) == int(i):
            win +=1
        
print("winrate :", win/total_image)
