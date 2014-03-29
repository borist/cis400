#edge class defines an edge used for vanishing point detection

class Edge:
    def __init__(self, endpoint1, endpoint2, vanishingPoint=()):
        #endpoint 1
        self.ep1 = endpoint1
        self.ep2 = endpoint2
        self.vp = vanishingPoint

    # compute the midpoint of the edge
    def midpoint(self):
        x1,y1 = self.ep1
        x2,y2 = self.ep2
        return ((x1+x2)/2, (y1+y2)/2)

# compute a vanishing point common to two edges
def vanishingPoint(edge1, edge2):
    x1, y1 = edge1.ep1
    x2, y2 = edge2.ep2

    m1 = (y2-y1)/(x2-x1)
    b1 = (m1 * x1) + y1

    x3, y3 = edge2.ep1
    x4, y4 = edge2.ep2

    m2 = (y4-y3)/(x4-x3)
    b2 = (m2 * x3) + y3

    x = (b1 - b2)/(m2 - m1)
    y = (m2 * x) + b2

    return (x, y)
