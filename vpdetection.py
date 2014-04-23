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
from colorToPgm import convert

# edgeList - list of edges
# phi - voting parameter (distance in pixels between endpoint of an edge and line between vanishing point and edge midpoint)
# M - number of hypothesized vanishing points
# Output: N x M matrix, where N = # of edges, and M = # of hypotheses
def buildPrefMatrix(edgeList, phi, M):
    numEdges = len(edgeList)

    # a list of tuples where each tuple is (edge, [set of hypothesis IDs that this edge votes for])
    prefMatrix = []
    for edge in edgeList:
        prefMatrix.append(([edge], set()))

    random.seed(0)
    for i in range(M):
        # sample 2 edges and find their intersection, which forms one vanishing point hypothesis
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

        # given the vanishing point hypothesis, determine if the particular edge
        # votes for that hypothesis
        for (edges, hypotheses) in prefMatrix:
            if (calc_D_lt_phi(vph, edges[0], phi)):
                hypotheses.add(i)

    return prefMatrix

def calc_D(vph, edge):
    x1, y1 = edge.ep1
    x2, y2 = edge.ep2
    vpx, vpy = vph[:2]

    #find the centroid of the edge
    xc = (x1 + x2)/2
    yc = (y1 + y2)/2

    #calculate parameters of line between centroid and vph
    if (xc - vpx != 0):
        # calculations relative to centroid
        m = (vpy - yc) / (vpx - xc)
        return math.fabs(m * (x1 - xc) - (y1 - yc)) / math.sqrt(m ** 2 + 1)
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

    while True:
        minDistance = 2.0
        minPair = (-1, -1)
        for ii, i in enumerate(validIndices):
            for j in validIndices[ii+1:]:
                # if not valid, update
                if distances[(i,j)] < 0:
                    distances[(i,j)] = jaccardDistance(preferenceSets[i], preferenceSets[j])

                #update the minimum distance
                if distances[(i,j)] < minDistance and distances[(i,j)] >= 0:
                    minPair = i,j
                    minDistance = distances[(i,j)]

        print "minDistance found: %s" % minDistance
        if minDistance >= 1.0:
            break

        # update the distances
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
    avgX = np.mean([x for (x, y) in points])
    avgY = np.mean([y for (x, y) in points])
    return (avgX, avgY)

# Input: takes in a list of 3 tuples, each representing a vanishing point. Each tuple is in the form ((x, y), [Edge])
def calculateManhattanDist(vps):
    v1 = tuple(vps[0][0])
    v2 = tuple(vps[1][0])
    v3 = tuple(vps[2][0])

    v1Err = calculateConsistency(v2, vps[0][1]) + calculateConsistency(v3, vps[0][1])
    v2Err = calculateConsistency(v1, vps[1][1]) + calculateConsistency(v3, vps[1][1])
    v3Err = calculateConsistency(v1, vps[2][1]) + calculateConsistency(v2, vps[2][1])

    # return np.mean([v1Err, v2Err, v3Err])
    return np.mean([v1Err, v2Err, v3Err])

# Helper function to calculateManhattanDist
def calculateConsistency(v, edges):
    return np.mean([calc_D(v, edge) for edge in edges])

#given list of clusters with their vanishing points, reduce them until less than 50 exist
def reduceClustersMore(clusters):
    #magic number threshhold for deciding if 2 vanishing points are close enough together
    mn = .1
    startinglen = len(clusters)

    result = [(calculateVanishingPoint(edges1 + edges2), edges1 + edges2) for (vp1, edges1)
              in clusters
                for (vp2, edges2)
                in clusters[(clusters.index((vp1, edges1)) + 1):]
              if math.sqrt((vp1[0] - vp2[0]) ** 2 + (vp1[1] - vp2[1]) ** 2) < math.sqrt(vp1[0] ** 2 + vp1[1] ** 2) * mn]
    print len(result)
    return result


def getOrthogonalVPs(imagePath):

    convert(imagePath, "temp.pgm")
    # runs LSD via command line
    inputfile = "temp.pgm"

    # runs LSD via command line
    outputfile = "/dev/stdout" # dump lsd output to stdout for python to read
    cmd = ['./lsd_1.6/lsd', inputfile, outputfile]
    lines = subprocess.check_output(cmd).strip()

    img = cv2.imread(imagePath, cv2.IMREAD_COLOR)
    width, height = img.shape[:2]

    edgeList = []
    for line in lines.split('\n'):
        edgeParams = line.split()
        e1 = (int(round(float(edgeParams[0]))), int(round(float(edgeParams[1]))))
        e2 = (int(round(float(edgeParams[2]))), int(round(float(edgeParams[3]))))
        newEdge = Edge(e1, e2)
        if (newEdge.length > .03 * (width ** 2 + height ** 2) ** .5):
            edgeList.append(newEdge)

    prefMatrix = buildPrefMatrix(edgeList, 2, 1000)

    print "starting clusters: %s" % len(edgeList)
    reducedClusters = reduceClusters(prefMatrix)

    reducedEdges = [cluster for cluster in reducedClusters[0] if len(cluster) > 2]
    print "reduced to %s clusters" % len(reducedEdges)

    # preserve pairing of vanishing points with edge clusters for Manhattan distance calculation
    vps = [(calculateVanishingPoint(cluster), cluster) for cluster in reducedEdges]
    if len(vps) > 70:
        vps = reduceClustersMore(vps)

    print "reduced further to %s clusters" % len(vps)


    # compute Manhattan distance
    maxDist = 0
    for t in combinations(vps, 3):
        dist = calculateManhattanDist(t)
        if (dist > maxDist):
            print "distance %f" % dist
            maxDist = dist
            triplet = t

    print triplet
    return triplet

if __name__ == "__main__":
    vps = getOrthogonalVPs(sys.argv[1])

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

    # display final image
    cv2.namedWindow('image')
    img = cv2.imread("temp.pgm", cv2.IMREAD_COLOR)
    k = 0
    for (v, edges) in vps:
        for edge in edges:
            cv2.line(img, edge.ep1, edge.ep2, colorlist[k % 10], 10) # thickness 2
        k += 1

    width, height = img.shape[:2]
    if (height > 720):
        img = cv2.resize(img, (0,0), fx=720/height, fy=720/height)

    cv2.imshow('image', img)
    # press 'q' to exit
    if cv2.waitKey(0) == ord('q'):
        cv2.destroyAllWindows()
