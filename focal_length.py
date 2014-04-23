#!/usr/bin/python

from __future__ import division
from vpdetection import getOrthogonalVPs
import numpy as np
import cv2
import sys


# Takes in a vanishing point, the image center, and the endpoint corresponding
# to the vanishing point.
def compute_focal_length(v, o, h):
    r = np.linalg.norm(v - h) / 2    # radius
    c = np.linalg.norm(v - o) / 2
    f = (2 * r * c  - c ** 2) ** .5
    print "Focal length: {}".format(f)
    return f

# Takes in the width and height of the image, as well as the computed focal
# length. All inputs are measured in pixels.
def compute_fov(w, h, f):
    d = ((w ** 2) + (h ** 2)) ** .5
    angle = 2 * np.arctan(d/(2*f))
    print "FOV, in radians: %f" % angle
    print "FOV, in degrees: %f" % np.degrees(angle)
    return angle

# Computes the principal point, or image center by computing the orthocenter of
# the 3 vanishing points.
def compute_pp(imagePath):
    vps = getOrthogonalVPs(imagePath)

    p0 = np.array(vps[0][0])
    p1 = np.array(vps[1][0])
    p2 = np.array(vps[2][0])

    # vectors representing 3 sides of triangle
    v0 = p2 - p1
    v1 = p2 - p0
    v2 = p1 - p0

    # h0 is the other endpoint of the height from p0.
    # (projection of v1 onto v2) * (unit vector of v1) + starting point of v1
    mag_v0 = np.linalg.norm(v0)
    h0 = (np.dot(v0, v2) / mag_v0) * (v0 / mag_v0) + p1
    mag_v1 = np.linalg.norm(v1)
    h1 = (np.dot(v1, v2) / mag_v1) * (v1 / mag_v1) + p0

    o = compute_intersect(v0, h0, v1, h1)
    print o
    # cv2.circle(img, (int(o[0]), int(o[1])), 100, (255, 0, 0), -1)
    return (v0, o, h0)

# Computes a line segment perpendicular to the specified line segment.
def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# Computes the intersection of two line segments. Line segment a is given by
# endpoints a1, a2. Line segment b is given by endpoints b1, b2.
def compute_intersect(a1, a2, b1, b2):
    a = a2 - a1
    b = b2 - b1
    a_perp = perp(a)
    denom = np.dot(a_perp, b)
    num = np.dot(a_perp, a1 - b1)
    return (num / denom) * b + b1

if __name__ == "__main__":
    (v0, o, h) = compute_pp(sys.argv[1])
    f = compute_focal_length(v0, o, h)
    img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
    h, w = img.shape[:2]
    compute_fov(w, h, f)
