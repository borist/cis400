#python implementation of the algorithm described in Non-Iterative Approach for
#Fast and Accurate Vanishing Point Detection by Jean-Philippe Tardif

# input: set of edges from the image
# output: set of vanishing points and each edge references a vp or is an outlier

# magic numbers
# phi = 2 ; consensus threshold
# M = 500 ; number of vp hypotheses

import numpy as np
import sys
import random
import edge

def buildPrefMatrix(edgeList, phi, M):
    numEdges = len(edgeList)
    prefMatrix = np.zeros(numEdges * M).reshape((numEdges, M))

    for i in range(M):
        # sample 2 edges and determine the vanishing point hypothesis
        edgeSample = random.sample(xrange(numEdges), 2)
        vph = vanishingPoint(edgeList[edgeSample[0]], edgeList[edgeSample[1]])

        #given the vanishing point hypothesis, determine if the particular edge
        #votes for that hypothesis
        j = 0
        for edge in edgeList:
            if (calc_D_lt_phi(vph, edge, phi)):
                prefMatrix[j,i] = 1
            else:
                prefMatrix[j,i] = 0
            j += 1

    return prefMatrix

# determine D(v_m,edge)
def calc_D_lt_phi(vph, edge, phi):
    x1, y1 = edge.ep1
    x2, y2 = edge.ep2

    m1 = (y2 - y1)/(x2 - x1)
    b1 = (m1 * x1) + y1

    vpx, vpy = vph

    D = math.fabs(vpy - (m1 * vpx) - b1)/math.sqrt(m1 ** 2 + 1)
    return (D <= phi)

# size of the set union of two preference sets
def unionAB(setA, setB):
    return reduce (lambda x, y: x + y, map(lambda x, y: x or y, setA, setB))

# size of the set intersection of two preference sets
def intersectAB(setA, setB):
    return reduce (lambda x, y: x + y, map(lambda x, y: x and y, setA, setB))

# calculates Jaccard Distance between two groups.
def jaccardDistance(setA, setB):
    return 1 - intersectAB(setA, setB)/unionAB(setA, setB)

# construct the data structure that will hold the clusters
def buildClusters(edgeList):
    return
# merge the clusters in the cluster list
def mergeClusters():
    return
