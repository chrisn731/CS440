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