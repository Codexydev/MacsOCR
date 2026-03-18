from PIL import Image
import numpy as np


def regression(img) -> tuple[float,list]:

    x = []
    y = []

    for i in range(128):
        for j in range(128):
            r,v,b,o=img.getpixel((i,j))
            if r<128 or v<128 or b < 128:
                x.append(i)
                y.append(j)

    xa = np.array(x)
    ya = np.array(y)
    x_moy = np.mean(xa)
    y_moy = np.mean(ya)

    pente = np.sum((xa - x_moy) * (ya - y_moy)) / np.sum((xa - x_moy) ** 2)

    return (pente,np.array([x,y]))


def rotateImage(imgMatrix, slope) -> None :
    # imageArray = 
    img = Image.fromarray((imgMatrix * 255).astype(np.uint8))
    img.rotate(slope)

    img.show


def main():
    img = Image.open("MacsOCR/18:03:26/Image/imageDepart/7/7a.png")

    pente, matrix = regression(img)
    print(f"pente : {pente}")



    rotateImage(matrix,pente)



if __name__ == "__main__":
    main()
