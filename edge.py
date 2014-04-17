#edge class defines an edge used for vanishing point detection

import sys

class Edge:
    def __init__(self, endpoint1, endpoint2):
        #endpoint 1
        self.ep1 = endpoint1
        self.ep2 = endpoint2
        x1,y1 = self.ep1
        x2,y2 = self.ep2
        self.length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5

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

    xdiff = x1 - x2, x3 - x4
    ydiff = y1 - y2, y3 - y4

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return (-1,-1)

    d = (det(edge1.ep1, edge1.ep2), det(edge2.ep1, edge2.ep2))

    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return x,y
