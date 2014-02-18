import cv2
import numpy as np
import sys
from matplotlib import pyplot as plt

PATH_TO_IMAGES = 'images/'


def houghp_detection(filename):
    img = cv2.imread(filename, 0)
    edges = cv2.Canny(img,20,350,apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 20, 50, 50)

    output = cv2.imread(filename, 0)

    print lines
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(output,(x1,y1),(x2,y2),(0,0,255),2)

    plt.subplot(121), plt.imshow(edges,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(output,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()
    #plt.subplot(121), plt.imshow(img, cmap = 'gray')
    #plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    #plt.subplot(122), plt.imshow(edges,cmap = 'gray')
    #plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

if __name__ == "__main__":
    print "Usage:", sys.argv[0], "image"
    print sys.argv
    image_path = sys.argv[1]
    houghp_detection(image_path)
