import sys

import graphics as gx
import structures
import algorithms as algo


__author__ = 'Bartosz'


def main():
    win = gx.GraphWin("go_triangulacja", 800, 600)
    State.win = win
    win.setMouseHandler(input_handler)
    while not State.done:
        win.getMouse()
    draw_polygon()
    init_broom(win)
    win.getMouse()
    win.close()


def input_handler(point):
    if point.getX() < 20 and point.getY() < 20:
        State.done = True
        State.win.setMouseHandler(None)
    else:
        State.points.append(point)
        draw_point(State.win, point.getX(), point.getY(), 2)


def init_broom(win):
    broom = gx.Line(gx.Point(0, 0), gx.Point(800, 0))
    broom.setFill("green")
    broom.draw(win)
    State.broom = broom
    solver = algo.Algorithm(State.polygon)
    solver.run(move_broom)
    print 'Finish!'


def move_broom(p, r):
    State.broom.move(0, p.y - State.y)
    State.y = p.y
    if r:
        draw_line(p.x, p.y, r.x, r.y, State.win, 'green')
    State.win.getMouse()


def draw_line(x1, y1, x2, y2, win, color='black'):
    line = gx.Line(gx.Point(x1, y1), gx.Point(x2, y2))
    line.setFill(color)
    line.draw(win)


def draw_point(win, x, y, r, color='black'):
    point = gx.Circle(gx.Point(x, y), r)
    point.setFill(color)
    point.draw(win)


def draw_polygon():
    points = State.points
    for i in range(len(points)):
        draw_line(points[i].getX(), points[i].getY(), points[(i + 1) % len(points)].getX(),
                  points[(i + 1) % len(points)].getY(), State.win, 'black')
        State.polygon.add_vertex(structures.Vertex(points[i].getX(), points[i].getY()))

    State.polygon.make_round()

    algo.set_vertex_types(State.polygon)

    # to nie blad - dzielimy tu wierzchoki na strony
    a = algo.Algorithm(State.polygon)

    for v in State.polygon.vertices:
        if v.type == structures.Type.START:
            color = 'green'
        elif v.type == structures.Type.END:
            color = 'yellow'
        elif v.type == structures.Type.MERGE:
            color = 'blue'
        elif v.type == structures.Type.SPLIT:
            color = 'lightblue'
        else:
            color = 'brown'
        draw_point(State.win, v.x, v.y, 3, color)


class State(object):
    points = []
    polygon = structures.Polygon()
    win = None
    done = False
    y = 0
    broom = None


class Solver(object):
    help_str = "Program usage: sage:\n  " \
               "call_main - runs triangulation"

    def run(self):
        print self.help_str
        while True:
            try:
                read_text = raw_input()
                tokens = read_text.split()
                if tokens:
                    self.run_command(tokens)
            except EOFError:
                break

    def run_command(self, tokens):
        try:
            handler = getattr(self, tokens[0])
            handler(*tokens[1:])
        except AttributeError:
            traceback.print_exc()
            print 'Wrong command name:', tokens[0]
        except Exception as e:
            print 'Error: occurred', e

    def call_main(self):
        main()


if __name__ == '__main__':
    app = Solver()
    app.run()
    sys.exit(0)