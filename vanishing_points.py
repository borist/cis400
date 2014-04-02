#!/usr/bin/python

from __future__ import division
from scipy import optimize as opt
import numpy as np
import cv2
import sys
import math

points = []

# mouse callback function
def get_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print (x, y)
        points.append([x, y])
        if len(points) == 10:
            res = optimize()
            transform(res, img)
            # compute_centroid_pp()

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
        #print "vanishing point: {}".format(v)
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
    compute_focal_length(v0, o, h0)
    return (v0, o, h0)

# Takes in a vanishing point, the image center, and the endpoint corresponding
# to the vanishing point.
def compute_focal_length(v, o, h):
    r = np.linalg.norm(v - h) / 2    # radius
    c = np.linalg.norm(v - o) / 2
    f = (2 * r * c  - c ** 2) ** .5
    print "Focal length: %d" % f
    return f

# Takes in the width and height of the image, as well as the computed focal
# length. All inputs are measured in pixels.
def compute_fov(w, h, f):
    d = ((w ** 2) + (h ** 2)) ** .5
    angle = 2 * np.arctan(d/(2*f))
    print "FOV, in radians: %f" % angle
    print "FOV, in degrees: %f" % np.degrees(angle)
    return angle

# Computes the distance between two points, specified in the form of arrays.
def compute_centroid_pp():
    vps = []
    for i in xrange(0, 3, 1):
        current = []
        for j in xrange(0, 4, 2):
            a1 = np.array(points[(6 * i + j + 1) % (6 * (i + 1))])
            a2 = np.array(points[(6 * i + j + 2) % (6 * (i + 1))])
            b1 = np.array(points[(6 * i + j + 3) % (6 * (i + 1))])
            b2 = np.array(points[(6 * i + j + 4) % (6 * (i + 1))])
            current.append(compute_intersect(a1, a2, b1, b2))
        centr = centroid(current)
        vps.append(centr)

    # orthocenter computation
    p0 = vps[0]
    p1 = vps[1]
    p2 = vps[2]

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
    f = compute_focal_length(v0, o, h0)
    h, w, d = img.shape
    compute_fov(w, h, f)
    return (v0, o, h0)

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
    return np.array([totalX/k,totalY/k])

# Computes the intersection of two line segments. Line segment a is given by
# endpoints a1, a2. Line segment b is given by endpoints b1, b2.
def compute_intersect(a1, a2, b1, b2):
    a = a2 - a1
    b = b2 - b1
    a_perp = perp(a)
    denom = np.dot(a_perp, b)
    num = np.dot(a_perp, a1 - b1)
    return (num / denom) * b + b1

# TODO:
# 1) is one edge enough? how do we best organize a1-a3 as global parameters?

def objective_function(x):
    obj = 0
    a1 = x[0]
    a = x[1]
    b = x[2]
    c = x[3]
    d = x[4]
    e = x[5]
    f = x[6]
    x0 = x[7]
    y0 = x[8]
    for i in range(len(points)):
        xd = points[i][0]
        yd = points[i][1]
        r2 = math.pow(xd-x0,2) + math.pow(yd-y0,2)
        denom = 1 + a1 * r2 
        xu = (xd-x0)/denom
        yu = (yd-y0)/denom
        if i < 5:
            obj += math.fabs(a*xu + b*yu + c)
        else:
            obj += math.fabs(d*xu + e*yu + f)
    return obj

def optimize():
    maxY, maxX = img.shape[:2]
    x0 = np.array([0.0001,1,0,0,1,0,0,maxX/2,maxY/2]) 
    b = [[-1000,1000], [-1,1], [-1,1], [-1000,1000], [-1,1], [-1,1], [-1000,1000], [0,maxX], [0,maxY]]
    cons = ({'type': 'eq', 'fun': lambda x: math.pow(x[1],2) + math.pow(x[2],2) - 1},
            {'type': 'eq', 'fun': lambda x: math.pow(x[4],2) + math.pow(x[5],2) - 1})
    result = opt.minimize(objective_function, x0, method = 'SLSQP', bounds = b, constraints = cons)  
    print result
    return result.x 

# correct distortion
def update(params):
    for i in xrange(rows):
        for j in xrange(cols):
            r2 = math.pow(i-params[7],2) + math.pow(j-params[8],2)
            #r2 = r2/10000 #I shouldn't need to do this, but r is so damn big it zooms in too much
            denom = 1 + params[0] * r2
            map_x.itemset((i,j), ((j-params[8])/denom) + params[8])
            map_y.itemset((i,j), ((i-params[7])/denom) + params[7])

def updatef(params): #decreases focal length by factor of 2 (accounting for centralization)
    for i in xrange(rows):
        for j in xrange(cols):
            map_x.itemset((i,j), ((j-params[8])/2) + params[8])
            map_y.itemset((i,j), ((i-params[7])/2) + params[7])

def transform(params, img):
    global map_x, map_y, rows, cols
    map_x = np.zeros(img.shape[:2], np.float32)
    map_y = np.zeros(img.shape[:2], np.float32)
    rows, cols = img.shape[:2]
    while(True):
        updatef(params)
        dst = cv2.remap(img, map_x, map_y, cv2.INTER_CUBIC)
        cv2.imshow('result', dst)
        if cv2.waitKey(0) == ord('q'):
            break

cv2.namedWindow('image')
cv2.setMouseCallback('image', get_point)
img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
cv2.imshow('image', img)

#press 'q' to exit
if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()


      


