import math

# Node
# Holds information about the status of a node.
# Nodes exist on the corners of "cells".
# x: X coordinate
# y: Y coordinate
# blocked: 1 if blocked, 0 otherwise
class Node():
    def __init__(self, x, y, blocked):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.blocked = blocked

# Edge
# Holds information about an edge.
# p1: Point 1 (Start point)
# p2: Point 2 (End point)
# weight: Weight of the edge
class Edge():
    def __init__(self, p1, p2, weight):
        self.p1 = p1
        self.p2 = p2
        self.weight = weight

class GridGraph():
    def __init__(self, f):
        self.nodes = []
        self.edges = dict()
        self.width = 10
        self.height = 10
        self.src = None
        self.dst = None
        self.read_file(f)

    def init_graph(self, cells):
        for x in range(self.width + 1):
            row = []
            for y in range(self.height + 1):
                if x == self.width or y == self.height:
                    b = 1
                else:
                    b = cells[(x,y)]
                row.append(Node(x, y, b))
            self.nodes.append(row)

        # Time to build the edges!
        for x in range(self.width + 1):
            for y in range(self.height + 1):
                # Draw edge to the top left
                if x > 0 and y > 0 and self.nodes[x-1][y-1].blocked == 0:
                    self.edges[((x,y),(x-1,y-1))] = Edge((x,y), (x-1,y-1), math.sqrt(2))

                # Draw edge to the top right
                if x < self.width and y > 0 and self.nodes[x][y-1].blocked == 0:
                    self.edges[((x,y),(x+1, y-1))] = Edge((x,y), (x+1, y-1), math.sqrt(2))

                # Draw edge straight up
                if y > 0:
                    if x == 0 and self.nodes[x][y-1].blocked == 0:
                        self.edges[((x,y),(x, y-1))] = Edge((x,y), (x, y-1), 1)
                    elif x > 0 and (self.nodes[x-1][y-1].blocked == 0 or self.nodes[x][y-1].blocked == 0):
                        self.edges[((x,y),(x, y-1))] = Edge((x,y), (x, y-1), 1)

                # Draw edge to the right
                if x < self.width:
                    if y == 0 and self.nodes[x][y].blocked == 0:
                        self.edges[((x,y),(x+1, y))] = Edge((x,y), (x+1, y), 1)
                    elif y > 0 and (self.nodes[x][y-1].blocked == 0 or self.nodes[x][y].blocked == 0):
                        self.edges[((x,y),(x+1, y))] = Edge((x,y), (x+1, y), 1)

    def read_file(self, fi):
        with open(fi, 'r') as f:
            line = f.readline().strip().split()
            self.src = (int(line[0]) - 1, int(line[1]) - 1) # Get the start point
            line = f.readline().strip().split()
            self.dst = (int(line[0]) - 1, int(line[1]) - 1) # Get the end point
            line = f.readline().strip().split()
            self.width = int(line[0])
            self.height = int(line[1])

            # Everything from here on is about (un)blocked cells...
            cells = dict()
            for line in f.readlines():
                split = line.strip().split()
                cells[(int(split[0]) - 1, int(split[1]) - 1)] = int(split[2])

            self.init_graph(cells)
