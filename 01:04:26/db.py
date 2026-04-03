from os import listdir
from os.path import isfile, join
from typing import Any
import csv

from normalisation import normalisation
from caracterisation import caracterisation


############################
# Caractérisation database #
############################


def indexation(path: str) -> list:
    files = []

    for numberFolder in listdir(path):
        if numberFolder.isdigit() or numberFolder=="perso":
            for file in listdir(path + "/" + numberFolder):
                files.append(f"{path}/{numberFolder}/{file}")

    return files


def indexFile(path: str):
    image = normalisation(path)
    data = caracterisation(image)
    return data


#######################
# fonction principale #
#######################


def create_db(path: str):
    tab = indexation(path)
    data_base = []
    for fichier in tab:
        data_base.append((list(indexFile(fichier)), fichier.split("/")[-1]))
    return data_base


def creer_journal(path: str, db):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([
            'densite', 'densite_hg', 'densite_hd', 'densite_bg', 'densite_bd', 
            'densite_h', 'densite_b', 'densite_g', 'densite_d', 'x_inter', 'y_inter', 'ratio_size', 
            'label'
        ])
        for image in db:
                caracteristiques = image[0]
                nom_image = image[1]
                
                line = list(caracteristiques)
                line.append(nom_image)
                
                writer.writerow(line)

def charger_journal(path: str) -> list:
    db = []
    
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        
        next(reader) 
        
        for row in reader:
            caracteristiques_str = row[:-1]
            caracteristiques_float = [float(val) for val in caracteristiques_str]
            
            nom_image = row[-1]
            
            db.append((caracteristiques_float, nom_image))
            
    return db


##################################
# main #
##################################


def main():
    ...
    # print(create_db("MacsOCR/01:04:26/Image/imageDepart"))


if __name__ == "__main__":
    main()
