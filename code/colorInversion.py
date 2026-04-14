import os
from PIL import Image, ImageOps


def inverser_dataset():
    chemin_base = "image_test/MNIST"

    for nom_dossier in os.listdir(chemin_base):
        if nom_dossier.isdigit():
            chemin_dossier = os.path.join(chemin_base, nom_dossier)
            fichiers = os.listdir(chemin_dossier)

            for nom_fichier in fichiers:
                if nom_fichier.endswith((".png", ".jpg", ".jpeg")):
                    chemin_image = os.path.join(chemin_dossier, nom_fichier)

                    try:
                        img = Image.open(chemin_image).convert("RGB")

                        img_inverse = ImageOps.invert(img)

                        img_inverse.save(chemin_image)

                    except Exception as e:
                        print(f"Erreur sur {nom_fichier}: {e}")

            print(f"Dossier '{nom_dossier}' : Couleurs inversées avec succès !")


if __name__ == "__main__":
    inverser_dataset()
    print("Toutes les images sont maintenant en Noir sur fond Blanc !")
