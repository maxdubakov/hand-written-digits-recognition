from PIL import Image
import numpy as np
import os


def load_image(path: str) -> np.array:
    im = Image.open(path)

    width, height = im.size
    bottom = height - 100
    left = 0
    right = width
    top = 0

    im = im.crop((left, top, right, bottom))
    im = im.resize((28, 28))
    arr = np.array(list(im.getdata()))
    width, height = im.size

    # delete_image(path)
    return image_to_input(arr, height, width)


def image_to_input(image, height, width) -> np.array:
    output = list()
    for i in range(height * width):
        if image[i][0] < 50:
            image[i][0] = 0
        if image[i][1] < 50:
            image[i][1] = 0
        if image[i][2] < 50:
            image[i][2] = 0
        Y = 0.33 * image[i][0] + 0.33 * image[i][1] + 0.33 * image[i][2]
        output.append(Y)
    return np.array(output)


def delete_image(path):
    os.remove(path)

