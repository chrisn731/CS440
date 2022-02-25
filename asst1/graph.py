import math
from bfs import bfs

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
        self.closed = False

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
    """
    A class used to represent the underlying 8-neighbor vertex graph.

    nodes : List
        List of nodes on the graph
    edges : dict
        Dictionary that holds every edge connection on the graph.
        The key to the dictionary is a start and end point (p1, p2) where p1 and p2 are tuples.
        Therefore, the expanded key looks like this: ((x0, y0), (x1, y1)).
    width : int
        Holds the width of the graph
    height : int
        Holds the height of the graph
    src : Tuple
        x, y coordinate tuple of the starting node
    dst : Tuple
        x, y coordinate tuple of the goal node
    solution_available : bool
        Cached result of a Best-First Search of a path from the start to the goal.
        This is kept here just so we do not have to run BFS each time we want to run out algorithms.
    """

    def __init__(self, f):
        self.nodes = []
        self.edges = dict()
        self.vedges = None
        self.width = 10
        self.height = 10
        self.src = None
        self.dst = None
        self.read_file(f)
        self.solution_available = bfs(self.src, self.dst, self.edges)

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

    def has_solution(self):
        return self.solution_available


    def visibility_graph(self):
        print("Calculating visibility graph. Please wait a moment...")
        if self.vedges:
            return self.vedges

        # Only calculate the visibility edges once
        self.vnodes = []
        self.vedges = dict()
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                if (i == self.src[0] and j == self.src[1]) or (i == self.dst[0] and j == self.dst[1]):
                    self.vnodes.append(self.nodes[i][j])
                elif self.nodes[i][j].blocked == 1:
                    if i == len(self.nodes) - 1 or j == len(self.nodes[i]) - 1:
                        continue
                    self.vnodes.extend([self.nodes[i][j], self.nodes[i+1][j], self.nodes[i][j+1], self.nodes[i+1][j+1]])

        for vnode in self.vnodes:
            for vis in self.vnodes:
                if vis == vnode:
                    continue
                if self.line_of_sight(vnode, vis, self.nodes):
                    self.vedges[((vnode.x, vnode.y), (vis.x, vis.y))] = Edge((vnode.x, vnode.y), (vis.x, vis.y), 1)

        return self.vedges


    def line_of_sight(self, s, e, nodes):
        x0 = s.x
        y0 = s.y
        x1 = e.x
        y1 = e.y
        f = 0
        dy = y1 - y0
        dx = x1 - x0

        if dy < 0:
            dy = -dy
            sy = -1
        else:
            sy = 1

        if dx < 0:
            dx = -dx
            sx = -1
        else:
            sx = 1

        if dx >= dy:
            while x0 != x1:
                f += dy
                if f >= dx:
                    if nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1)//2)].blocked:
                        return False
                    y0 += sy
                    f -= dx
                if f != 0 and nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1)//2)].blocked:
                    return False
                if dy == 0 and nodes[x0 + ((sx - 1)//2)][y0].blocked and nodes[x0 + ((sx - 1)//2)][y0 - 1].blocked:
                    return False
                x0 += sx
        else:
            while y0 != y1:
                f += dx
                if f >= dy:
                    if nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1 )//2)].blocked:
                        return False
                    x0 += sx
                    f -= dy

                if f != 0 and nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1)//2)].blocked:
                    return False
                if dx == 0 and nodes[x0][y0 + ((sy - 1)//2)].blocked and nodes[x0 - 1][y0 + ((sy - 1)//2)].blocked:
                    return False
                y0 += sy
        return True

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
