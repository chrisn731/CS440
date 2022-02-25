from queue import Queue

"""
    A simple BFS implementation. Used only to ensure there is a path
    before running A* or Theta*.
"""

def get_edge(s, e, edges):
    return edges.get((s, e), edges.get((e, s), None))

def bfs(start, goal, edges):
    fringe = Queue()
    closed = []

    fringe.put(start)
    while not fringe.empty():
        s = fringe.get()

        if s == goal:
            return True

        closed.append(s)
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = s[0]
                y = s[1]
                end = (x + i, y + j)
                if end in closed or end in fringe.queue:
                    continue

                edge = get_edge(s, end, edges)
                if not edge:
                    continue

                fringe.put(end)
    return False
