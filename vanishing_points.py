#!/usr/bin/python

from __future__ import division
import numpy as np
import cv2
import sys

points = []

# mouse callback function
def get_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print (x, y)
        points.append([x, y])
        if len(points) == 18:
            compute_pp()
            compute_centroid_pp()

# Computes the principal point, or image center by finding the vanishing
# points implied in the list points and computing their orthocenter.
# Each set of 4 elements in points specifies one vanishing point. i.e. elements
# 1-4 specify v0, elements 5-8 specify v1, and elements 9-12 specify v2.
def compute_pp():
    # vanishing point computation
    vs = []
    for i in xrange(0, 12, 4):
        a1 = np.array(points[i + 0])
        a2 = np.array(points[i + 1])
        b1 = np.array(points[i + 2])
        b2 = np.array(points[i + 3])
        v = compute_intersect(a1, a2, b1, b2)
        print v
        vs.append(v)

    # orthocenter computation
    p0 = vs[0]
    p1 = vs[1]
    p2 = vs[2]

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

def compute_centroid_pp():
    vps = []
    
    for i in range(2):
        current = []
        for j in range(2):
            a1 = np.array(points[6*i + (j % 3) + 1])
            a2 = np.array(points[6*i + (j % 3) + 2])
            b1 = np.array(points[6*i + (j % 3) + 3])
            b2 = np.array(points[6*i + (j % 3) + 4])
            current.append(compute_intersect(a1, a2, b1, b2))
        centr = centroid(current)
        vps.append(centr)

    res = centroid(vps)
    print res
    return res

# Computes a line segment perpendicular to the specified line segment.
def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def centroid(xy):
    totalX = 0
    totalY = 0
    k = 0
    for [x,y] in xy:
        totalX += x
        totalY += y
        k += 1
    return [totalX/k,totalY/k]

# Computes the intersection of two line segments. Line segment a is given by
# endpoints a1, a2. Line segment b is given by endpoints b1, b2.
def compute_intersect(a1, a2, b1, b2):
    a = a2 - a1
    b = b2 - b1
    a_perp = perp(a)
    denom = np.dot(a_perp, b)
    num = np.dot(a_perp, a1 - b1)
    return (num / denom) * b + b1

cv2.namedWindow('image')
cv2.setMouseCallback('image', get_point)

# other options: IMREAD_GRAYSCALE, IMREAD_UNCHANGED
img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)

cv2.imshow('image', img)
# press 'q' to exit
if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()


