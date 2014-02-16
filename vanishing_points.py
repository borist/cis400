#!/usr/bin/python

from __future__ import division
import cv2
import numpy as np
import sys

points = []
# mouse callback function
def get_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print (x, y)
        points.append([x, y])
        if len(points) == 12:
            compute_vanishing_points()

# elements 1-4 in points specify v1, elements 5-8 specify v2, elements 9-12 specify v3
def compute_vanishing_points():
    for i in xrange(0, 12, 4):
        p0 = np.array(points[i + 0])
        p1 = np.array(points[i + 1])
        p2 = np.array(points[i + 2])
        p3 = np.array(points[i + 3])
        v = compute_intersect(p0, p1, p2, p3)
        print v

def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def compute_intersect(a1, a2, b1, b2):
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perp(da)
    denom = np.dot(dap, db)
    num = np.dot(dap, dp)
    return (num / denom) * db + b1

cv2.namedWindow('image')
cv2.setMouseCallback('image', get_point)

# other options: IMREAD_GRAYSCALE, IMREAD_UNCHANGED
img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)

cv2.imshow('image', img)
# press 'q' to exit
if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()


