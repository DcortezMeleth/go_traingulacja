import math
import structures


__author__ = 'Bartosz'


def get_side(n1, v, n2):
    return (n1.x - n2.x)*(v.y - n2.y) - (v.x - n2.x)*(n1.y - n2.y)


def get_angle(n1, v, n2):
    angle = vector_angle(structures.Vertex(v.x - n1.x, v.y - n1.y), structures.Vertex(n2.x - v.x, n2.y - v.y))
    if get_side(n1, v, n2) > 0:
        return math.pi + angle
    else:
        return math.pi - angle


def vector_angle(v1, v2):
    return math.acos((v1.x*v2.x + v1.y*v2.y)/
                (math.sqrt(math.pow(v1.x, 2) + math.pow(v1.y, 2))*math.sqrt(math.pow(v2.x, 2) + math.pow(v2.y, 2))))


def classify_vertices(polygon):
    for v in polygon.vertices:
        v1 = v.prev
        v2 = v.next
        ang = get_angle(v1, v, v2)
        if v1.below(v) and v2.below(v):
            if ang < math.pi:
                v.type = structures.Type.START
            else:
                v.type = structures.Type.SPLIT
        elif v1.above(v) and v2.above(v):
            if ang < math.pi:
                v.type = structures.Type.END
            else:
                v.type = structures.Type.MERGE
        else:
            v.type = structures.Type.REGULAR


class Algorithm(object):
    def __init__(self, polygon):
        self.polygon = polygon
        self.vertices = polygon.vertices[:]
        self.polygon.sort()
        self.divide()
        self.stack = self.polygon.vertices[0:2]

    def divide(self):
        v = self.polygon.vertices[0].prev
        while v is not self.polygon.vertices[-1]:
            v.side = structures.Side.RIGHT
            v = v.prev
        v = self.polygon.vertices[0].next
        while v is not self.polygon.vertices[-1]:
            v.side = structures.Side.LEFT
            v = v.next

    def run(self, move_broom_func):
        stack = self.polygon.vertices[0:2]
        move_broom_func(stack[0], None)
        move_broom_func(stack[1], None)
        stack.reverse()
        vertices = self.polygon.vertices[2:]
        while len(vertices) > 0:
            p = vertices[0]
            move_broom_func(p, None)
            vertices = vertices[1:]
            q = stack[0]
            if p.side != q.side:
                while len(stack) > 0:
                    r = stack[0]
                    stack = stack[1:]
                    move_broom_func(p, r)
            else:
                stack = stack[1:]
                r = stack[0]
                ind = sorted([self.vertices.index(p), self.vertices.index(q), self.vertices.index(r)])
                first, second, third = self.vertices[ind[0]], self.vertices[ind[1]], self.vertices[ind[2]]
                while (p.side == structures.Side.LEFT and get_angle(first, second, third) < math.pi) \
                        or (p.side == structures.Side.RIGHT and get_angle(first, second, third) > math.pi):
                    move_broom_func(p, r)
                    q = r
                    stack = stack[1:]
                    if len(stack) == 0:
                        break
                    r = stack[0]
            stack = [p, q] + stack
