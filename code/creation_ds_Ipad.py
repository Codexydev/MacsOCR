import cv2
import os

def decouper_grille_vers_dataset(chemin_image_grille: str, dossier_dataset_racine: str):
    image = cv2.imread(chemin_image_grille, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Erreur : Impossible de charger l'image.")
        return

    # Création des 10 sous-dossiers (0 à 9)
    for i in range(10):
        os.makedirs(os.path.join(dossier_dataset_racine, str(i)), exist_ok=True)

    _, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"{len(contours)} formes détectées sur la page !")

    # 1. Tri primaire de GAUCHE à DROITE (pour classer par Chiffre)
    # On arrondit la position X (ex: // 100) pour grouper les chiffres d'une même colonne
    contours_tries = sorted(contours, key=lambda c: (cv2.boundingRect(c)[0] // 100, cv2.boundingRect(c)[1]))

    compteur_chiffre_actuel = -1  
    derniere_colonne_x = -1000

    for contour in contours_tries:
        x, y, w, h = cv2.boundingRect(contour)

        # Filtre anti-bruit
        if w > 10 and h > 10:
            
            # Détection du changement de colonne (on passe au chiffre suivant)
            if x - derniere_colonne_x > 50: # Si on se décale de plus de 50 pixels à droite
                compteur_chiffre_actuel += 1
                derniere_colonne_x = x
                
                if compteur_chiffre_actuel > 9:
                    print("Attention: Plus de 10 colonnes détectées. Les chiffres supplémentaires seront ignorés.")
                    break

            y_start = max(0, y - 5)
            y_end = min(image.shape[0], y + h + 5)
            x_start = max(0, x - 5)
            x_end = min(image.shape[1], x + w + 5)
            
            chiffre_decoupe = image[y_start:y_end, x_start:x_end]
            
            # Calcul du prochain index disponible dans le dossier de destination
            dossier_cible = os.path.join(dossier_dataset_racine, str(compteur_chiffre_actuel))
            fichiers_existants = [f for f in os.listdir(dossier_cible) if f.endswith('.png')]
            nouvel_index = len(fichiers_existants)
            
            # Sauvegarde au format officiel : "3_dataset_12.png"
            nom_fichier = f"{compteur_chiffre_actuel}_dataset_{nouvel_index}.png"
            chemin_sauvegarde = os.path.join(dossier_cible, nom_fichier)
            
            cv2.imwrite(chemin_sauvegarde, chiffre_decoupe)

    print(f"Extraction terminée et rangée dans '{dossier_dataset_racine}'.")

if __name__ == "__main__":
    # Il va tout ranger dans MacsOCR/01:04:26/Image/ImageDepart/
    decouper_grille_vers_dataset("/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/test_image/dataset.jpg", "/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/test_image/ipad_dataset")