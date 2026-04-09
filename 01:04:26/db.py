from os import listdir
from typing import Any
import csv

# import perso
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


def indexFile(path: str, taille_grille: int = 4) -> tuple:
    image = normalisation(path)
    data = caracterisation(image, taille_grille)
    return data


#######################
# fonction principale #
#######################


def create_db(path: str, taille_grille: int):
    tab = indexation(path)
    data_base = []
    for fichier in tab:
        data_base.append((list(indexFile(fichier, taille_grille)), fichier.split("/")[-1]))
    return data_base


def creer_journal(path: str, db, taille_grille: int):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        
        # S'il y a une grille 7x7, ça créera automatiquement 49 colonnes "zone_X"
        nb_zones = taille_grille * taille_grille
        colonnes_zones = [f"zone_{i}" for i in range(nb_zones)]
        
        en_tete = colonnes_zones + ['x_inter', 'y_inter', 'ratio_size', 'label']
        writer.writerow(en_tete)
        
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
