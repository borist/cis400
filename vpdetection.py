#!/usr/bin/python

#python implementation of the algorithm described in Non-Iterative Approach for
#Fast and Accurate Vanishing Point Detection by Jean-Philippe Tardif

# input: set of edges from the image
# output: set of vanishing points and each edge references a vp or is an outlier

# magic numbers
# phi = 2 ; consensus threshold
# M = 500 ; number of vp hypotheses

from __future__ import division
import cv2
from edge import Edge, vanishingPoint
from itertools import combinations
import math
import numpy as np
import random
import subprocess
import sys
#from matplotlib import pyplot as plt

def buildPrefMatrix(edgeList, phi, M):
    numEdges = len(edgeList)

    prefMatrix = []
    for edge in edgeList:
        prefMatrix.append(([edge], set()))

    for i in range(M):
        # sample 2 edges and determine the vanishing point hypothesis
        edgeSample = random.sample(xrange(numEdges), 2)
        vph = vanishingPoint(edgeList[edgeSample[0]], edgeList[edgeSample[1]])

        #cv2.namedWindow('image')
        #img = cv2.imread("./images/high_contrast/high1.pgm", cv2.IMREAD_COLOR)
        #cv2.circle(img, vph, 10, (0,0,255))
        #cv2.line(img, edgeList[edgeSample[0]].ep1, edgeList[edgeSample[0]].ep2, (0,0,255))
        #cv2.line(img, edgeList[edgeSample[1]].ep1, edgeList[edgeSample[1]].ep2, (0,0,255))
        #print "plotting (%s,%s)" % vph
        #print "with lines %s and %s" % (edgeList[edgeSample[0]], edgeList[edgeSample[1]])

        #cv2.imshow('image', img)
        #press 'q' to exit
        #if cv2.waitKey(0) == ord('q'):
            #cv2.destroyAllWindows()
        #if cv2.waitKey(0) == ord('x'):
            #break

        #given the vanishing point hypothesis, determine if the particular edge
        #votes for that hypothesis
        for (edges, hypotheses) in prefMatrix:
            if (calc_D_lt_phi(vph, edges[0], phi)):
                hypotheses.add(i)

    for (edges, hypotheses) in prefMatrix:
        print "(%s, %s)" % (edges, hypotheses)

    return prefMatrix

def calc_D(vph, edge):
    x1, y1 = edge.ep1
    x2, y2 = edge.ep2
    vpx, vpy = vph

    #find the centroid of the edge
    xc = (x1 + x2)/2
    yc = (y1 + y2)/2

    #calculate parameters of line between centroid and vph
    if (xc - vpx != 0):
        return math.fabs(x1 - (ml * y1) - bl)/math.sqrt(ml ** 2 + 1)
    else:
        return math.fabs(x1 - xc)

# Determine D(v_m,edge)
def calc_D_lt_phi(vph, edge, phi):
    return calc_D(vph, edge) <= phi

# calculates Jaccard Distance between two groups.
def jaccardDistance(setA, setB):
    if (len(setA | setB) > 0):
        return 1 - len(setA & setB)/len(setA | setB)
    else:
        return 1

# reduce clusters in cluster list
def reduceClusters(clusterList):
    # keep a table of Jaccard distances
    validIndices = range(len(clusterList))
    distances = {}

    for ii, i in enumerate(validIndices):
        for j in validIndices[ii+1:]:
            distances[(i,j)] = -1

    edgelist, preferenceSets = zip(*clusterList)
    outliers = []

    while True:
        minDistance = 2.0
        minPair = (-1, -1)
        for ii, i in enumerate(validIndices):
            for j in validIndices[ii+1:]:
                #if not valid, update
                if distances[(i,j)] < 0:
                    distances[(i,j)] = jaccardDistance(preferenceSets[i], preferenceSets[j])

                #update the minimum distance
                if distances[(i,j)] < minDistance and distances[(i,j)] >= 0:
                    minPair = i,j
                    minDistance = distances[(i,j)]

        print "minDistance found: %s" % minDistance
        if minDistance >= 1.0:
            break

        #update the distances
        print "merging %s with %s" % minPair
        edgelist[minPair[0]].extend(edgelist[minPair[1]])
        preferenceSets[minPair[0]].intersection_update(preferenceSets[minPair[1]])
        validIndices.remove(minPair[1])

        #mark distances as invalid
        for i in validIndices:
            distances[(minPair[0],i)] = distances[(i,minPair[0])] = -1

    return edgelist, preferenceSets

# Input: a list of edges. Output: vanishing point corresponding to these edges.
def calculateVanishingPoint(cluster):
    points = [vanishingPoint(e1, e2) for (e1, e2) in combinations(cluster, 2)]

    # find the centroid of these points
    totalX = 0
    totalY = 0
    k = 0
    for (x, y) in points:
        totalX += x
        totalY += y
        k += 1
    return (totalX / k, totalY / k)

def null(A, eps=1e-3):
    u,s,vh = np.linalg.svd(A, full_matrices=1, compute_uv=1)
    null_space = np.compress(s <= eps, vh, axis=0)
    return null_space.T

# Input: takes in a list of 3 tuples, each representing a vanishing point. Each tuple is in the form ((x, y), [Edge])
def calculateManhattanDist(vps):
    v1 = vps[0][0]
    v2 = vps[1][0]
    v3 = vps[2][0]

    v1_p = null(np.matrix([v2, v3]))
    v2_p = null(np.matrix([v1, v3]))
    v3_p = null(np.matrix([v1, v2]))

    v1Err = calculateConsistency(v1_p, vps[0][1])
    v2Err = calculateConsistency(v2_p, vps[1][1])
    v3Err = calculateConsistency(v3_p, vps[2][1])

    return max(v1Err, v2Err, v3Err)

# Helper function to calculateManhattanDist
def calculateConsistency(v, edges):
    return np.mean([calc_D(v, edge) for edge in edges])

def main(argv=None):
    if argv == None:
        argv = sys.argv

    inputfile = argv[1]
    outputfile = "/dev/stdout" # dump lsd output to stdout for python to read
    cmd = ['./lsd_1.6/lsd', inputfile, outputfile]
    lines = subprocess.check_output(cmd)

    edgeList = []
    lines = lines.strip()

    for line in lines.split('\n'):
        edgeParams = line.split()
        e1 = (int(round(float(edgeParams[0]))), int(round(float(edgeParams[1]))))
        e2 = (int(round(float(edgeParams[2]))), int(round(float(edgeParams[3]))))
        newEdge = Edge(e1, e2)
        if (newEdge.length > 30):
            edgeList.append(newEdge)

    prefMatrix = buildPrefMatrix(edgeList, 2, 1000)

    print "starting clusters: %s" % len(edgeList)
    reducedClusters = reduceClusters(prefMatrix)

    reducedEdges = [cluster for cluster in reducedClusters[0] if len(cluster) > 1]
    print "reduced to %s clusters" % len(reducedEdges)

    # preserve pairing of vanishing points with edge clusters for Manhattan distance calculation
    vps = [(vanishingPoint(cluster), cluster) for cluster in reducedEdges]

    # compute Manhattan distance
    minDist = sys.maxint
    for (t1, t2, t3) in combinations(vps, 3):
        dist = calculateManhattanDist(t1, t2, t3)
        if (dist < minDist):
            triplet = (t1, t2, t3)
    print "final vanishing points"
    print triplet

    cv2.namedWindow('image')
    img = cv2.imread(inputfile, cv2.IMREAD_COLOR)

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

    k = 0
    for edgeCluster in reducedClusters[0]:
        print edgeCluster
        if len(edgeCluster) > 2:
            for edge in edgeCluster:
                cv2.line(img, edge.ep1, edge.ep2, colorlist[k % 10])
            k += 1


    cv2.imshow('image', img)
    #press 'q' to exit
    if cv2.waitKey(0) == ord('q'):
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv)
