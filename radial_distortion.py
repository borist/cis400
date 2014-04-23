#!/usr/bin/python

from __future__ import division
from scipy import optimize as opt
import numpy as np
import cv2
import sys
import math
import cv2.cv as cv

points = []
x0 = 0
y0 = 0

def objective_function(x):
    obj = 0
    a1 = x[0]
    a = x[1]
    b = x[2]
    c = x[3]
    d = x[4]
    e = x[5]
    f = x[6]
    for i in range(len(points)):
        xd = points[i][0]
        yd = points[i][1]
        r2 = math.pow(xd-x0,2) + math.pow(yd-y0,2)
        denom = 1 + a1 * r2
        xu = (xd-x0)
        yu = (yd-y0)
        if i < 10:
            obj += math.fabs(a*xu + b*yu + c*denom)
        else:
            obj += math.fabs(d*xu + e*yu + f*denom)
    return obj

def optimize():
    x0 = np.array([.1,.70,.70,0,.70,.70,0])
    b = [[-.1,.1], [-1,1], [-1,1], [-1000,1000], [-1,1], [-1,1], [-1000,1000]]
    cons = ({'type': 'eq', 'fun': lambda x: math.pow(x[1],2) + math.pow(x[2],2) - 1},
            {'type': 'eq', 'fun': lambda x: math.pow(x[4],2) + math.pow(x[5],2) - 1})
    result = opt.minimize(objective_function, x0, method = 'SLSQP', bounds = b, constraints = cons)
    if result.status == 0:
        return result.x[0]
    else:
        return 0

def hough_circles(img):
    maxY, maxX = img.shape[:2]
    minR = int(min(maxY,maxX)/2)
    maxR = int(max(maxY,maxX)*2)
    imgMod = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(imgMod,cv2.COLOR_BGR2GRAY)
    x = 65
    circles = []
    while(((circles is None) or len(circles) == 0 or len(circles[0]) < 2) and x > 30):
        x = x-0.5
        circles = cv2.HoughCircles(cimg,cv.CV_HOUGH_GRADIENT,1,.0001,param1=100,param2=x,minRadius=minR,maxRadius=maxR)

    #for i in circles[0,:]:
    #  cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    #  cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    #while(True):
    #    cv2.imshow('detected circles',cimg)
    #    if cv2.waitKey(0) == ord('q'):
    #        break
    return circles

# correct distortion
def update(params):
    for i in xrange(rows):
        for j in xrange(cols):
            r2 = math.pow(i-params[7],2) + math.pow(j-params[8],2)
            denom = 1 + params[0] * r2
            map_x.itemset((i,j), ((j-params[8])*denom) + params[8])
            map_y.itemset((i,j), ((i-params[7])*denom) + params[7])

def transform(params, img):
    global map_x, map_y, rows, cols
    map_x = np.zeros(img.shape[:2], np.float32)
    map_y = np.zeros(img.shape[:2], np.float32)
    rows, cols = img.shape[:2]
    while(True):
        update(params)
        dst = cv2.remap(img, map_x, map_y, cv2.INTER_CUBIC)
        cv2.imshow('result', dst)
        if cv2.waitKey(0) == ord('q'):
            break

def main(argv=None):

    if type(argv) == str:
        img = cv2.imread(argv)
    else:
        #cv2.namedWindow('image')
        img = cv2.imread(argv[1])

    #cv2.imshow('image', img)
    result = hough_circles(img)

    #pick 2 closest circles
    minDist = float("inf")
    circle1 = None
    circle2 = None

    if circles is None:
        return 0

    for i in result[0,:]:
        for j in result[0,:]:
            dist = (i[0] - j[0])**2 + (i[1] - j[1])**2
            if (dist < minDist and dist != 0):
                circle1 = i
                circle2 = j
                minDist = dist

    #run fitting on 2 closest circles
    #compute average center
    x0 = (circle1[0] + circle2[0])/2
    y0 = (circle1[1] + circle2[1])/2

    maxY, maxX = img.shape[:2]
    for i in range(0,360,36):
        x = math.cos(math.radians(i)) * circle1[2] + x0
        y = math.sin(math.radians(i)) * circle1[2] + y0
        if(x < maxX and y < maxY):
            points.append([x,y])

    for i in range(0,360,36):
        x = math.cos(math.radians(i)) * circle2[2] + x0
        y = math.sin(math.radians(i)) * circle2[2] + y0
        if(x < maxX and y < maxY):
            points.append([x,y])

    # #press 'q' to exit
    # if cv2.waitKey(0) == ord('q'):
    #     cv2.destroyAllWindows()

    return optimize()

if(__name__ == "__main__"):
    main(sys.argv)




