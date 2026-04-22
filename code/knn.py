import math
from sre_constants import ANY
import numpy as np
from typing import Any


def calcul_distance(x: tuple[list[float], str], y: tuple[list[float], str]) -> float:
    vecteur_x = np.array(x[0])
    vecteur_y = np.array(y[0])
    return float(np.linalg.norm(vecteur_x - vecteur_y))


def calcul_distance_total(tab: list[tuple[list[float], str]], mon_image: tuple[list[float], str]) -> list[tuple[float, str]]:
    result = []
    for x in tab:
        result.append((calcul_distance(x, mon_image), x[1]))
    result.sort()
    return result


def find(distances: list[tuple[float, str]], k: int, display: bool) -> str | None:
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