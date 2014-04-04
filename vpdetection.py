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
import math
from edge import Edge, vanishingPoint
import subprocess
#from matplotlib import pyplot as plt

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

# determine D(v_m,edge) the implementation at the moment is not as described in the paper
def calc_D_lt_phi(vph, edge, phi):
    x1, y1 = edge.ep1
    x2, y2 = edge.ep2
    vpx, vpy = vph
    if (x2 - x1 != 0):
        m1 = (y2 - y1)/(x2 - x1)
        b1 = (m1 * x1) + y1

        D = math.fabs(vpy - (m1 * vpx) - b1)/math.sqrt(m1 ** 2 + 1)
        return (D <= phi)
    else:
        D = math.fabs(vpx - x1)
        return (D <= phi)

# size of the set union of two preference sets
def unionAB(setA, setB):
    return sum([x or y for x in setA for y in setB])

# size of the set intersection of two preference sets
def intersectAB(setA, setB):
    return sum([x and y for x in setA for y in setB])

# calculates Jaccard Distance between two groups.
def jaccardDistance(setA, setB):
    return 1 - intersectAB(setA, setB)/unionAB(setA, setB)

# construct the data structure that will hold the clusters which is a dictionary mapping edge indexes to preference sets
def buildClusters(edgeList, prefMatrix):
    i = 0
    clusters = []
    for edge in edgeList:
        cluster = (set([i]), prefMatrix[i])
        clusters.append(cluster)
        i += 1
    return clusters

# merge two clusters
def mergeClusters(cluster1, cluster2):
    clusterset1, clustermat1 = cluster1
    clusterset2, clustermat2 = cluster2
    return clusterset1 ^ clusterset2, [x and y for x in clustermat1 for y in clustermat2]

# reduce clusters in cluster list
def reduceClusters(clusterList):
    while True:
        #find minimum Jaccard distance
        i = 0
        minDist = 1
        minCluster1 = ()
        minCluster2 = ()

        for cluster1 in clusterList[:]:
            for cluster2 in clusterList[i+1:]:
                cluster1Set = cluster1[0]
                cluster2Set = cluster2[0]
                newDist = jaccardDistance(cluster1Set, cluster2Set)
                if newDist < minDist:
                    minDist = newDist
                    minCluster1 = cluster1
                    minCluster2 = cluster2

        if minDist == 1:
            return clusterList

        if (minCluster1 != minCluster2):
            newCluster = mergeClusters(minCluster1, minCluster2)
            print "Merge Clusters %s, %s" % (minCluster1[0], minCluster2[0])
            clusterList.remove(minCluster1)
            clusterList.remove(minCluster2)
            clusterList.append(newCluster)

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
        e1 = (float(edgeParams[0]), float(edgeParams[1]))
        e2 = (float(edgeParams[2]), float(edgeParams[3]))
        newEdge = Edge(e1, e2)
        edgeList.append(newEdge)

    prefMatrix = buildPrefMatrix(edgeList, 2, 500)
    clusters = buildClusters(edgeList, prefMatrix)
    reducedClusters = reduceClusters(clusters)
    print reducedClusters


if __name__ == "__main__":
    main(sys.argv)
