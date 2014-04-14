import cv, cv2
import numpy as np

PATH_TO_IMAGES = 'images/'


def open_image(filename):
    # no "cv" prepended before all method names
    img = cv.LoadImageM(filename, cv.CV_LOAD_IMAGE_GRAYSCALE)
    # let's show the image in a window
    cv.NamedWindow('your name', 1)
    cv.ShowImage('your name', img)
    cv.WaitKey()


def detect_corners(filename, max_accurary=False):
    """
    adapted from: https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html#harris-corners
    """
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)  # translate into a numpy array
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    # result is dilated for marking the corners
    dst = cv2.dilate(dst, None)

    # Threshold for an optimal value, it may vary depending on the image.
    img[dst > 0.01*dst.max()] = [0, 0, 255]

    cv2.imshow('dst', img)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    image_name = 'empire.jpg'
    full_filename = PATH_TO_IMAGES + image_name
    # open_image(full_filename)
    detect_corners(full_filename)
