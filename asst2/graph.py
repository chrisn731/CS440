import math
from enum import Enum

#Terrain
# Holds information about the terrain of a cell.
# N = normal
# H = highway
# T = hard to traverse
# B = blocked
class Terrain(Enum):
    N = 'N'
    H = 'H'
    T = 'T'
    B = 'B'

    def __str__(self):
        return "{0}".format(self.value)

# Node
# Holds information about the status of a node.
# Nodes exist on the corners of "cells".
# x: X coordinate
# y: Y coordinate
# blocked: 1 if blocked, 0 otherwise
class Node():
    def __init__(self, x, y, t = Terrain.N):
        self.x = x
        self.y = y
        self.terrain = t;

    def set_terrain(self, t):
        self.terrain = t;

class GridGraph():
    """
    A class used to represent the underlying 4-neighbor vertex graph.

    nodes : List
        List of nodes on the graph
    width : int
        Holds the width of the graph
    height : int
        Holds the height of the graph
    src : Tuple
        x, y coordinate tuple of the starting node
    """

    def __init__(self, f):
        self.nodes = []
        self.width = 10
        self.height = 10
        self.src = None
        self.read_file(f)

    def init_graph(self, cells):
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(Node(x, y))
            self.nodes.append(row)

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
