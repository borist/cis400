import os
from PIL import Image
import numpy as np


def get_imlist(path):
    """
    Return a list of filenames for all jpg images in a directory
    """
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]


def imresize(im, size):
    """ Resize an image array using PIL. """
    pil_im = Image.fromarray(np.uint8(im))
    return np.array(pil_im.resize(size))


def histeq(im, nbr_bins=256):
    """ Histogram equalization of a grayscale image. """

    # get image histogram
    imhist, bins = np.histogram(im.flatten(), nbr_bins, normed=True)
    cdf = imhist.cumsum()  # cumulative distribution function
    cdf = 255 * cdf / cdf[-1]  # normalize

    # use linear interpolation of cdf to find new pixel values
    im2 = np.interp(im.flatten(), bins[:-1], cdf)

    return im2.reshape(im.shape), cdf


def compute_average(imlist):
    """ Compute the average of a list of images """

    # open first image and make into array of type float
    avg_im = np.array(Image.open(imlist[0]), 'f')

    for im_name in imlist[1:]:
        try:
            avg_im += np.array(Image.open(im_name))
        except:
            print im_name + '...skipped'
    avg_im /= len(imlist)

    # return average as unit8
    return np.array(avg_im, 'uint8')
