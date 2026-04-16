import cv2
import os

def decouper_grille_vers_dataset(chemin_image_grille: str, dossier_dataset_racine: str):
    image = cv2.imread(chemin_image_grille, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return

    for i in range(10):
        os.makedirs(os.path.join(dossier_dataset_racine, str(i)), exist_ok=True)

    _, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    valid_boxes = [b for b in bounding_boxes if b[2] > 10 and b[3] > 30]

    valid_boxes.sort(key=lambda b: b[0])

    colonnes = []
    colonne_actuelle = []
    
    if valid_boxes:
        derniere_x = valid_boxes[0][0]

    for box in valid_boxes:
        x, y, w, h = box
        
        if x - derniere_x > 30 and len(colonne_actuelle) > 0:
            colonnes.append(colonne_actuelle)
            colonne_actuelle = []
            
        colonne_actuelle.append(box)
        derniere_x = x

    if colonne_actuelle:
        colonnes.append(colonne_actuelle)

    for i, colonne in enumerate(colonnes):
        if i > 9:
            break
            
        colonne.sort(key=lambda b: b[1])
        
        for j, box in enumerate(colonne):
            x, y, w, h = box
            y_start = max(0, y - 5)
            y_end = min(image.shape[0], y + h + 5)
            x_start = max(0, x - 5)
            x_end = min(image.shape[1], x + w + 5)

            chiffre_decoupe = image[y_start:y_end, x_start:x_end]
            nom_fichier = f"{i}_dataset_{j}.png"
            chemin_sauvegarde = os.path.join(dossier_dataset_racine, str(i), nom_fichier)
            cv2.imwrite(chemin_sauvegarde, chiffre_decoupe)


if __name__ == "__main__":
    decouper_grille_vers_dataset(
        "MacsOCR/test_image/dataset3train.jpg",
        "MacsOCR/code/dataset_train/ipad_dataset_train",
    )