from queue import Queue
from graph import Edge

def get_edge(s, e, edges):
    if (s, e) in edges:
        return edges[s, e]
    elif (e, s) in edges:
        return edges[e, s]
    else:
        return None

def bfs(start, goal, edges):
    print("Start: " + str(start))
    print("Goal: " + str(goal))
    fringe = Queue()
    closed = []

    fringe.put(start)
    while not fringe.empty():
        s = fringe.get()

        if s == goal:
            print("Path found with BFS!")
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
    print("No path found with BFS")
    return False
