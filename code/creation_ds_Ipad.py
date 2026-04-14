import cv2
import os


def decouper_grille_vers_dataset(chemin_image_grille: str, dossier_dataset_racine: str):
    image = cv2.imread(chemin_image_grille, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Erreur : Impossible de charger l'image.")
        return

    for i in range(10):
        os.makedirs(os.path.join(dossier_dataset_racine, str(i)), exist_ok=True)

    _, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"{len(contours)} formes détectées sur la page !")

    contours_tries = sorted(
        contours, key=lambda c: (cv2.boundingRect(c)[0] // 100, cv2.boundingRect(c)[1])
    )

    compteur_chiffre_actuel = -1
    derniere_colonne_x = -1000

    for contour in contours_tries:
        x, y, w, h = cv2.boundingRect(contour)

        if w > 30 and h > 30:

            if x - derniere_colonne_x > 50:
                compteur_chiffre_actuel += 1
                derniere_colonne_x = x

                if compteur_chiffre_actuel > 9:
                    print(
                        "Attention: Plus de 10 colonnes détectées. Les chiffres supplémentaires seront ignorés."
                    )
                    break

            y_start = max(0, y - 5)
            y_end = min(image.shape[0], y + h + 5)
            x_start = max(0, x - 5)
            x_end = min(image.shape[1], x + w + 5)

            chiffre_decoupe = image[y_start:y_end, x_start:x_end]

            dossier_cible = os.path.join(
                dossier_dataset_racine, str(compteur_chiffre_actuel)
            )
            fichiers_existants = [
                f for f in os.listdir(dossier_cible) if f.endswith(".png")
            ]
            nouvel_index = len(fichiers_existants)

            nom_fichier = f"{compteur_chiffre_actuel}_dataset_{nouvel_index}.png"
            chemin_sauvegarde = os.path.join(dossier_cible, nom_fichier)

            cv2.imwrite(chemin_sauvegarde, chiffre_decoupe)

    print(f"Extraction terminée et rangée dans '{dossier_dataset_racine}'.")


if __name__ == "__main__":
    decouper_grille_vers_dataset(
        "MacsOCR/test_image/dataset.jpg",
        "MacsOCR/code/dataset_train/ipad_dataset_train",
    )
