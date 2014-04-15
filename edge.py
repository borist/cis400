#edge class defines an edge used for vanishing point detection

import sys

class Edge:
    def __init__(self, endpoint1, endpoint2):
        #endpoint 1
        self.ep1 = (int(endpoint1[0]), int(endpoint1[1]))
        self.ep2 = (int(endpoint2[0]), int(endpoint2[1]))

    def __repr__(self):
        return "(endpoint1: %s endpoint2: %s)" % (self.ep1, self.ep2)
    # compute the midpoint of the edge
    def midpoint(self):
        x1,y1 = self.ep1
        x2,y2 = self.ep2
        return ((x1+x2)/2, (y1+y2)/2)

# compute a vanishing point hypothesis common to two edges
def vanishingPoint(edge1, edge2):
    x1, y1 = edge1.ep1
    x2, y2 = edge2.ep2

    x3, y3 = edge2.ep1
    x4, y4 = edge2.ep2

    if (x2 - x1 == 0 and x4 - x3 == 0):
        return ((x4 + x2)/2, sys.maxint)
    elif (x2 - x1 == 0):
        m2 = (y4 - y3) / (x4 - x3)
        b2 = (m2 * x3) + y3
        return (x2, m2 * x2 + b2)
    elif (x4 - x3 == 0):
        m1 = (y2 - y1) / (x2 - x1)
        b1 = (m1 * x1) + y1
        return (x4, m1 * x4 + b1)

    if (x2 - x1 != 0):
        m1 = (y2-y1)/(x2-x1)
        b1 = (m1 * x1) + y1

    if (x4 - x3 != 0):
        m2 = (y4-y3)/(x4-x3)
        b2 = (m2 * x3) + y3

    if (m2 - m1 != 0):
        x = (b1 - b2)/(m2 - m1)
        y = (m2 * x) + b2

        return (x, y)
    else:
        return (-1,-1)
