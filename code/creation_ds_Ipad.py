import cv2
import os

def decouper_grille(chemin_image_grille: str, dossier_sortie: str):
    image = cv2.imread(chemin_image_grille, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        print("Erreur : Impossible de charger l'image.")
        return

    os.makedirs(dossier_sortie, exist_ok=True)

    _, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1] // 50, cv2.boundingRect(c)[0]))

    compteur = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if w > 10 and h > 10:
            y_start = max(0, y - 5)
            y_end = min(image.shape[0], y + h + 5)
            x_start = max(0, x - 5)
            x_end = min(image.shape[1], x + w + 5)
            
            chiffre_decoupe = image[y_start:y_end, x_start:x_end]
            
            chemin_sauvegarde = os.path.join(dossier_sortie, f"chiffre_brut_{compteur}.png")
            cv2.imwrite(chemin_sauvegarde, chiffre_decoupe)
            compteur += 1

    print(f"Extraction réussie : {compteur} images générées dans '{dossier_sortie}'.")

if __name__ == "__main__":
    decouper_grille("/Users/antoine/Documents/etude/l2/s4/MaCs/projet/MacsOCR/test_image/Dataset 2.png", "dataset_ipad/")