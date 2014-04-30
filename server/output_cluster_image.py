#!/usr/bin/python

from __future__ import division
import cv2
from edge import Edge, vanishingPoint
from itertools import combinations
import math
import ntpath
import numpy as np
import os
import random
import subprocess
import sys
from colorToPgm import convert
from vpdetection import *


colorlist = [(255,0,0),
                (0,255,0),
                (0,0,255),
                (255,255,255),
                (255,0,255),
                (255,255,0),
                (0,255,255),
                (255,153,0),
                (255,255,102),
                (51,51,204),
                ]

if __name__ == "__main__":
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]


    convert(inputPath, "temp.pgm")
    # runs LSD via command line
    inputPath = "temp.pgm"

    # runs LSD via command line
    outputfile = "/dev/stdout" # dump lsd output to stdout for python to read
    cmd = ['./lsd_1.6/lsd', inputPath, outputfile]
    lines = subprocess.check_output(cmd).strip()

    img = cv2.imread(inputPath, cv2.IMREAD_COLOR)
    height, width = img.shape[:2]

    edgeList = []
    for line in lines.split('\n'):
        edgeParams = line.split()
        e1 = (int(round(float(edgeParams[0]))), int(round(float(edgeParams[1]))))
        e2 = (int(round(float(edgeParams[2]))), int(round(float(edgeParams[3]))))
        newEdge = Edge(e1, e2)
        if (newEdge.length > .02 * (width ** 2 + height ** 2) ** .5):
            edgeList.append(newEdge)

    prefMatrix = buildPrefMatrix(edgeList, 2, 1000)

    #print "starting clusters: %s" % len(edgeList)
    reducedClusters = reduceClusters(prefMatrix)

    reducedEdges = [cluster for cluster in reducedClusters[0] if len(cluster) > 3]
    #print "reduced to %s clusters" % len(reducedEdges)

    k = 0
    for cluster in reducedEdges:
        for edge in cluster:
            cv2.line(img, edge.ep1, edge.ep2, colorlist[k % 10], 2)
        k += 1

    cv2.imwrite(outputPath, img)
