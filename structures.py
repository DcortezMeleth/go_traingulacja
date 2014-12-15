__author__ = 'Bartosz'


class Type(object):
    START, END, REGULAR, SPLIT, MERGE = range(5)


class Side(object):
    LEFT, RIGHT = range(2)


class Vertex(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = None
        self.prev = None
        self.next = None
        self.side = None

    def below(self, other):
        return self.y > other.y or (self.y == other.y and self.x > other.x)

    def above(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)


class Polygon(object):
    def __init__(self):
        self.vertices = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def make_round(self):
        for i in range(len(self.vertices)):
            self.vertices[i].prev = self.vertices[(i-1) % len(self.vertices)]
            self.vertices[i].next = self.vertices[(i+1) % len(self.vertices)]

    def sort(self):
        self.vertices = sorted(self.vertices, key=lambda v: v.y)