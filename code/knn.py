import numpy as np


def calcul_distance(x: tuple[list[float], str], y: tuple[list[float], str]) -> float:
    """
    Mesure la distance Euclidienne entre deux vecteurs de caractéristiques.

    Args:
        x (tuple[list[float], str]): Les caractéristiques et le label de la première image.
        y (tuple[list[float], str]): Les caractéristiques et le label de la seconde image.

    Returns:
        float: La distance géométrique séparant les deux points dans l'espace vectoriel.
    """
    vecteur_x = np.array(x[0])
    vecteur_y = np.array(y[0])
    return float(np.linalg.norm(vecteur_x - vecteur_y))


def calcul_distance_total(
    tab: list[tuple[list[float], str]], mon_image: tuple[list[float], str]
) -> list[tuple[float, str]]:
    """
    Calcule la distance entre une image mystère et l'intégralité de la base de données.

    Args:
        tab (list[tuple[list[float], str]]): La base de données contenant tous les vecteurs d'apprentissage.
        mon_image (tuple[list[float], str]): Les données vectorielles de l'image à identifier.

    Returns:
        list[tuple[float, str]]: Une liste triée (par ordre croissant) des distances 
                                 et des labels associés.
    """
    result = []
    for x in tab:
        result.append((calcul_distance(x, mon_image), x[1]))
    result.sort()
    return result


def find(distances: list[tuple[float, str]], k: int, display: bool) -> str | None:
    """
    Réalise la prédiction finale via un vote majoritaire (Algorithme K-NN).
    
    Isole les K plus proches voisins et détermine l'étiquette la plus fréquente 
    parmi eux pour déduire la classe de l'image mystère.

    Args:
        distances (list[tuple[float, str]]): La liste de tous les voisins triés par distance croissante.
        k (int): Le paramètre K, déterminant la taille du voisinage à analyser.
        display (bool): Si True, affiche dans la console le détail des votes.

    Returns:
        str | None: Le label (chiffre de 0 à 9) prédit par le modèle, ou None en cas d'erreur.
    """
    k_voisins = distances[:k]

    votes = {}

    for distance, nom_image in k_voisins:
        vrai_chiffre = str(nom_image)[0]

        if vrai_chiffre in votes:
            votes[vrai_chiffre] += 1
        else:
            votes[vrai_chiffre] = 1

    if display:
        print(f"Détail des {k} votes : {votes}")

    meilleur_chiffre = None
    max_votes = 0

    for chiffre, nb_votes in votes.items():
        if nb_votes > max_votes:
            max_votes = nb_votes
            meilleur_chiffre = chiffre

    return meilleur_chiffre
