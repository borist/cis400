PATH_TO_IMAGES = 'images/'

# playing around with the info in CV with python

# ------------------------------------
# 1.1 PIL - the Python Imaging Library
# ------------------------------------

from PIL import Image

# Open an Image
pil_im = Image.open(PATH_TO_IMAGES + 'empire.jpg')
# pil_im.show()

# Convert image to grayscale
gray_im = pil_im.convert('L')
# gray_im.show()

# Rotate 180 degrees
rotated_im = pil_im.rotate(180)
# rotated_im.show()


# --------------
# 1.2 Matplotlib
# --------------

from matplotlib import pylab as pl

# Read image to array
im = pl.array(Image.open(PATH_TO_IMAGES + 'empire.jpg'))

# create figure 1
pl.figure()

# plot the image
pl.imshow(im)

# some points
x = [100, 100, 400, 400]
y = [200, 500, 200, 500]

# plot the points with red star-markers
pl.plot(x, y, 'r*')

# line plot connecting the first two points
pl.plot(x[:2], y[:2])

# add title and show the plot
pl.title('Plotting: "empire.jpg"')
pl.axis('off')


# Image Contours and Histograms
gray_im = pl.array(Image.open(PATH_TO_IMAGES + 'empire.jpg').convert('L'))

# figure 2
pl.figure()

# don't use clors
pl.gray()

# show contours with origin upper left corner
pl.contour(gray_im, origin='image')
pl.axis('equal')
pl.axis('off')

# Histogram - figure 3
pl.figure()
pl.hist(im.flatten(), 128)


# Interactive notation

# figure 4
pl.figure()

pl.imshow(im)
print 'Please click 3 points'
# x = pl.ginput(3)  # uncomment for interactive input
# print 'you clicked:', x

# Uncomment below to show pylab plots
# pl.show()

# -----------
# 1.3 - NumPy
# -----------

im = pl.array(Image.open(PATH_TO_IMAGES + 'empire.jpg'))
print im.shape, im.dtype

im_gray = pl.array(Image.open(PATH_TO_IMAGES + 'empire.jpg').convert('L'), 'f')
print im_gray.shape, im_gray.dtype

# Accessing values in NumPy arrays
i, j, k = 1, 1, 1

# value at coordinates i, j and color channel k
print im[i, j]
print im[i, j, k]

# slicing

im[i, :] = im[j, :]     # set the values of row i with values from row j
im[:, i] = 100          # set all values in column i to 100
im[:100, :50].sum()     # the sum of the values of the first 100 rows and 50 columns
im[50:100, 50:100]      # rows 50-100, columns 50-100 (100th not included)
im[i].mean()            # average of row i
im[:, -1]               # last column

im[-2, :]               # (or im[-2]) # second to last row


# Graylevel transforms
import numpy as np

im = np.array(Image.open(PATH_TO_IMAGES + 'empire.jpg').convert('L'))

im2 = 255 - im  # invert image (for each entry, entry = 255 - entry)

im3 = (100.0 / 255) * im + 100  # clamp to interval 100...200 (from 0...255)

im4 = 255 * (im / 255.0) ** 2  # squared

pil_im = Image.fromarray(im)

pil_im = Image.fromarray(np.uint8(im))  # may need to convert back to unit8 type

Image.fromarray(im2).show()


# -----------
# 1.4 - SciPy
# -----------
from scipy.ndimage import filters
