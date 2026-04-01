from curses.ascii import isdigit
from os import listdir
from os.path import isfile, join
from typing import Any
from xml.dom.expatbuilder import FilterCrutch

from normalisation import normalisation
from caracterisation import caracterisation


############################
# Caractérisation database #
############################


def indexation(path: str) -> list:
    files = []

    for numberFolder in listdir(path):
        if numberFolder.isdigit():
            for file in listdir(path + "/" + numberFolder):
                files.append(f"{path}/{numberFolder}/{file}")

    return files


def indexFile(
    path: str,
) -> tuple[Any | int, Any | int, Any | int, Any | int, Any | int, int, int]:
    image = normalisation(path)
    data = caracterisation(image)
    return data


#######################
# fonction principale #
#######################


def create_db(path: str):
    tab = indexation(path)
    data_base = []
    for fichier in tab:
        data_base.append((list(indexFile(fichier)), fichier.split("/")[-1]))
    return data_base


##################################
# main #
##################################


def main():
    ...
    # print(create_db("MacsOCR/01:04:26/Image/imageDepart"))


if __name__ == "__main__":
    main()
