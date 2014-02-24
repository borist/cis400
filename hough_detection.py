import cv2
import numpy as np
import sys
from matplotlib import pyplot as plt

PATH_TO_IMAGES = 'images/'


def hough_detection(filename):
    img = cv2.imread(filename, 0)
    blur = cv2.GaussianBlur(img, (17,17), 0)
    edges = cv2.Canny(blur,20,100,apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
    output = cv2.imread(filename, 0)

    negslop = []
    posslop = []
    vertical = []
    for rho, theta in lines[0]:
        direction = theta * 180/np.pi

        if (direction > 0 and direction < 90):
            posslop.append((rho,theta))
        elif (direction > 90):
            negslop.append((rho,theta))
        elif (direction == 0):
            vertical.append((rho,theta))

        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * -b)
        y1 = int(y0 + 1000 * a)
        x2 = int(x0 - 1000 * -b)
        y2 = int(y0 - 1000 * a)
        cv2.line(output,(x1,y1),(x2,y2),(0,0,255),2)

    plt.subplot(121), plt.imshow(edges,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(output,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()

    return (negslop,vertical,posslop)
if __name__ == "__main__":
    print "Usage:", sys.argv[0], "image"
    print sys.argv
    image_path = sys.argv[1]
    print hough_detection(image_path)
