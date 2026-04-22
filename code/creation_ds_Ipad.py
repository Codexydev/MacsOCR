import cv2
import os
import numpy as np

def decouper_grille_vers_dataset(chemin_image_grille: str, dossier_dataset_racine: str)  -> None:
    image = cv2.imread(chemin_image_grille, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Erreur : Impossible de charger l'image.")
        return

    for i in range(10):
        os.makedirs(os.path.join(dossier_dataset_racine, str(i)), exist_ok=True)

    _, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3, 3), np.uint8)
    thresh_fusion = cv2.dilate(thresh, kernel, iterations=1)

    contours, _ = cv2.findContours(thresh_fusion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    valid_boxes = [b for b in bounding_boxes if b[2] > 8 and b[3] > 15]

    valid_boxes.sort(key=lambda b: b[1])

    lignes = []
    ligne_actuelle = []
    
    if valid_boxes:
        derniere_y = valid_boxes[0][1]

    for box in valid_boxes:
        x, y, w, h = box
        
        if abs(y - derniere_y) > 25 and len(ligne_actuelle) > 0:
            lignes.append(ligne_actuelle)
            ligne_actuelle = []
            
        ligne_actuelle.append(box)
        derniere_y = y

    if ligne_actuelle:
        lignes.append(ligne_actuelle)

    print(f"Analyse : {len(lignes)} lignes détectées sur l'image.")

    images_sauvegardees = 0

    for index_ligne, ligne in enumerate(lignes):
        ligne.sort(key=lambda b: b[0])
        
        if len(ligne) != 10:
            print(f"-> Attention : La ligne {index_ligne + 1} contient {len(ligne)} formes. Elle a été ignorée.")
            continue
            
        for vrai_chiffre, box in enumerate(ligne):
            x, y, w, h = box
            
            y_start = max(0, y - 5)
            y_end = min(image.shape[0], y + h + 5)
            x_start = max(0, x - 5)
            x_end = min(image.shape[1], x + w + 5)

            chiffre_decoupe = image[y_start:y_end, x_start:x_end]
            
            dossier_cible = os.path.join(dossier_dataset_racine, str(vrai_chiffre))
            nouvel_index = len(os.listdir(dossier_cible))
            
            nom_fichier = f"{vrai_chiffre}_dataset_{nouvel_index}.png"
            chemin_sauvegarde = os.path.join(dossier_cible, nom_fichier)
            cv2.imwrite(chemin_sauvegarde, chiffre_decoupe)
            
            images_sauvegardees += 1

    print(f"Succès : {images_sauvegardees} images ajoutées proprement à ton dataset !")


if __name__ == "__main__":
    decouper_grille_vers_dataset(
        "MacsOCR/dataset/combined/dataset7train.jpg",
        "MacsOCR/dataset/train/ipad_dataset_train",
    )