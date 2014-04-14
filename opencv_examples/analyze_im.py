from PIL import Image
import pylab as pl
import numpy as np

PATH_TO_IMAGES = 'images/'


# ------------------------------------
# PIL - the Python Imaging Library
# ------------------------------------
def open_image(image_name):
    pil_im = Image.open(PATH_TO_IMAGES + image_name)
    pil_im.show()


if __name__ == "__main__":
    image_name = 'empire.jpg'
    open_image(image_name)
