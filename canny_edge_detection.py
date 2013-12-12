import cv2
import numpy as np
import sys
from matplotlib import pyplot as plt

PATH_TO_IMAGES = 'images/'


def canny_edge_detection(filename):
    img = cv2.imread(filename, 0)
    edges = cv2.Canny(img, 100, 200)

    plt.subplot(121), plt.imshow(img, cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()

if __name__ == "__main__":
    print "Usage:", sys.argv[0], "image"
    print sys.argv
    image_path = sys.argv[1]
    canny_edge_detection(image_path)
