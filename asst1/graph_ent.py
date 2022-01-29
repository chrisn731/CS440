class Node():
    def __init__(self, x, y, blocked):
        self.x = x
        self.y = y
        self.blocked = blocked

class Edge():
    def __init__(self, p1, p2, weight):
        self.p1 = p1
        self.p2 = p2
        self.weight = weight

