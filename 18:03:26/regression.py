from PIL import Image
import numpy as np

img = Image.open("/Users/lelaurearnaud/Documents/cours_S4/MaCs/projet/18:03:26/Image/imageDepart/0/0t.png")
x = []
y = []

def regression(img) -> float:
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

    return pente


def main():
    pente = regression(img)
    print(f"pente : {pente}")


if __name__ == "__main__":
    main()
