# MacsOCR : Moteur de Reconnaissance Optique de Caractères

## Présentation du Projet
MacsOCR est une solution logicielle de reconnaissance de caractères manuscrits développée dans le cadre de l'Unité d'Enseignement "Mathématiques et Calcul Scientifique" (MaCs). L'objectif est de classifier des chiffres (0-9) en transformant une matrice de pixels brute en une signature mathématique exploitable par un algorithme de classification métrique.

Le projet se distingue par une approche déterministe basée sur le traitement du signal et la géométrie analytique, s'affranchissant des modèles de type "boîte noire" au profit d'une logique mathématique transparente et interprétable.

## Architecture Technique

Le système repose sur un pipeline de traitement divisé en trois segments majeurs :

### 1. Prétraitement et Normalisation
Pour obtenir une comparaison fiable, chaque image subit une standardisation rigoureuse :
* **Binarisation** : Conversion en noir et blanc pur (fond/encre) via un seuillage de luminance (moyenne RVB < 128).
* **Correction d'inclinaison (Slant Correction)** : Utilisation de la régression linéaire par la méthode des moindres carrés pour identifier l'axe principal du tracé. Le redressement est opéré par une rotation isométrique d'angle $-\theta$.
* **Standardisation Spatiale** : Recadrage au plus près de l'encre (*cropping*) et redimensionnement proportionnel avec filtre de Lanczos pour obtenir une matrice finale de 28x28 pixels.

### 2. Caractérisation (Extraction de caractéristiques)
L'image est projetée dans un espace vectoriel de dimension 52, constituant la signature unique du caractère :
* **Zoning Dynamique (49 dimensions)** : Calcul de la densité relative d'encre sur une grille de 7x7 blocs.
* **Analyse Topologique (2 dimensions)** : Comptage des transitions fond-encre sur les axes médians horizontal et vertical, normalisé par un facteur de 5.0.
* **Morphologie (1 dimension)** : Calcul du ratio largeur/hauteur de la boîte englobante originale.

### 3. Classification via K-NN
La décision finale est prise par l'algorithme des $K$-Plus-Proches-Voisins :
* **Métrique de similarité** : Calcul de la distance euclidienne (norme $L_2$) entre le vecteur test et l'intégralité de la base de données de référence.
* **Logique de décision** : Vote majoritaire parmi les $K=7$ voisins les plus proches.
* **Gestion des données** : Les caractéristiques sont indexées dans un fichier CSV structuré, permettant une recherche rapide et une extensibilité du dataset.

## Structure du Projet
```text
MacsOCR/code/
├── main.py                 # Point d'entrée principal et outils de visualisation
├── train.py                # Script d'évaluation des performances (Win Rate)
├── normalisation.py        # Algorithmes de traitement d'image et régression
├── caracterisation.py      # Fonctions d'extraction du vecteur de dimension 52
├── knn.py                  # Moteur mathématique de classification et calcul de distances
├── db.py                   # Gestionnaire de base de données (Indexation et CSV)
├── creation_ds_Ipad.py     # Script d'extraction automatisée via OpenCV
├── rename.py               # Utilitaire de renommage de fichiers dataset
└── database.csv            # Base de connaissances du modèle (vecteurs et étiquettes)
```

## Performance et Évaluation
Le modèle a été éprouvé sur un jeu de données propriétaire généré sur iPad, incluant des variations de styles d'écriture, d'épaisseurs de trait et d'inclinaisons.
* **Précision globale (Win Rate)** : ~92% sur des données inconnues.
* **Robustesse** : Excellente résistance aux translations et aux variations d'épaisseur.
* **Limites identifiées** : Sensibilité aux rotations extrêmes (proches de 90°) dues aux limites théoriques de la régression linéaire sur l'axe vertical.

## Installation et Dépendances
Le projet requiert Python 3.8+ et les bibliothèques suivantes :
* **NumPy** : Calcul vectoriel et matriciel.
* **Pillow (PIL)** : Manipulation d'images.
* **OpenCV (cv2)** : Segmentation et extraction du dataset.
* **Matplotlib** : Visualisation des étapes de normalisation.
* **Scikit-Image** : Outils de morphologie (optionnel).

```bash
pip install numpy pillow opencv-python matplotlib scikit-image
```

## Utilisation
Pour tester une image isolée et visualiser le pipeline de redressement :
```bash
python main.py
```
Pour évaluer le taux de réussite global sur le dossier de test :
```bash
python train.py
```

## Auteurs
* **Antoine Ragot -- Raillat**
* Étudiant en Licence 2 Informatique
* UE Mathématiques et Calcul Scientifique (MaCs)
