from os import listdir
import csv

# import perso
from normalisation import normalisation
from caracterisation import caracterisation


############################
# Caractérisation database #
############################


def indexation(path: str) -> list[str]:
    """
    Parcourt un dossier racine pour lister l'ensemble des chemins des images disponibles.

    Args:
        path (str): Le chemin vers le dossier contenant les sous-dossiers (0 à 9).

    Returns:
        list[str]: Une liste contenant les chemins relatifs de chaque fichier image.
    """
    files = []

    for numberFolder in listdir(path):
        if numberFolder.isdigit() or numberFolder == "perso":
            for file in listdir(path + "/" + numberFolder):
                if file[0] != ".":
                    files.append(f"{path}/{numberFolder}/{file}")

    return files


def indexFile(path: str, taille_grille: int = 4) -> tuple[float, ...]:
    """
    Traite un fichier image unique (Normalisation et Caractérisation).

    Args:
        path (str): Le chemin vers le fichier image à lire.
        taille_grille (int, optional): La taille de la grille pour le zoning. Par défaut à 4.

    Returns:
        tuple[float, ...]: Le vecteur de caractéristiques mathématiques du chiffre.
    """
    image = normalisation(path)
    data = caracterisation(image, taille_grille)
    return data


#######################
# fonction principale #
#######################


def create_db(path: str, taille_grille: int) -> list[tuple[list[float], str]]:
    """
    Construit la base de données de référence en mémoire (RAM).
    
    Itère sur toutes les images d'un dataset, extrait leurs caractéristiques 
    et leur associe leur vraie étiquette déduite de leur nom.

    Args:
        path (str): Le chemin racine du dataset d'entraînement.
        taille_grille (int): La taille de la grille pour le zoning.

    Returns:
        list[tuple[list[float], str]]: Une liste de tuples regroupant le vecteur 
                                       et le label pour chaque image traitée.
    """
    tab = indexation(path)
    data_base = []
    for fichier in tab:
        data_base.append(
            (list(indexFile(fichier, taille_grille)), fichier.split("/")[-1])
        )
    return data_base


def creer_journal(
    path: str, db: list[tuple[list[float], str]], taille_grille: int
) -> None:
    """
    Sérialise et sauvegarde la base de données en mémoire vers un fichier CSV.

    Args:
        path (str): Le chemin du fichier CSV de destination.
        db (list[tuple[list[float], str]]): La base de données en mémoire.
        taille_grille (int): Permet de calculer dynamiquement les en-têtes des colonnes de zones.
    """
    with open(path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")

        nb_zones = taille_grille * taille_grille
        colonnes_zones = [f"zone_{i}" for i in range(nb_zones)]

        en_tete = colonnes_zones + ["x_inter", "y_inter", "ratio_size", "label"]
        writer.writerow(en_tete)

        for image in db:
            caracteristiques = image[0]
            nom_image = image[1]

            line = [str(val) for val in caracteristiques] + [nom_image]

            writer.writerow(line)


def charger_journal(path: str) -> list[tuple[list[float], str]]:
    """
    Charge rapidement une base de données existante depuis un fichier CSV.

    Args:
        path (str): Le chemin vers le fichier CSV de la base de données.

    Returns:
        list[tuple[list[float], str]]: La base de données formatée et prête à être 
                                       utilisée par l'algorithme K-NN.
    """
    db = []

    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")

        next(reader)

        for row in reader:
            caracteristiques_str = row[:-1]
            caracteristiques_float = [float(val) for val in caracteristiques_str]

            nom_image = row[-1]

            db.append((caracteristiques_float, nom_image))

    return db