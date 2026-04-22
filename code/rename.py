import os


def renommer_dataset() -> None:
    chemin_base = "MacsOCR/dataset/train/ipad_dataset_train"

    for nom_dossier in os.listdir(chemin_base):
        if nom_dossier.isdigit():
            chemin_dossier = os.path.join(chemin_base, nom_dossier)

            fichiers = os.listdir(chemin_dossier)

            for index, nom_fichier in enumerate(fichiers):
                if nom_fichier.endswith((".png", ".jpg", ".jpeg", ".JPG")):
                    # if nom_fichier.startswith(nom_dossier):
                    #     continue

                    ancien_chemin = os.path.join(chemin_dossier, nom_fichier)

                    nouveau_nom = f"{nom_dossier}_dataset_{str(index)}.png"
                    nouveau_chemin = os.path.join(chemin_dossier, nouveau_nom)

                    os.rename(ancien_chemin, nouveau_chemin)

            print(f"Dossier '{nom_dossier}' : images renommées avec succès !")


if __name__ == "__main__":
    renommer_dataset()
    print("Opération terminée !")
