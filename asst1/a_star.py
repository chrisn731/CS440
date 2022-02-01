from queue import PriorityQueue
from graph_ent import Edge
import math

def get_edge(s, e, edges):
    if (s, e) in edges:
        return edges[s, e]
    elif (e, s) in edges:
        return edges[e, s]
    else:
        return None

def heuristic(s, goal):
    x = min(abs(s[0] - goal[0]), abs(s[1] - goal[1]))
    y = max(abs(s[0] - goal[0]), abs(s[1] - goal[1]))
    return math.sqrt(2) * x + y - x

def update_vertex(s, e, cost_so_far, parent, edge: Edge, fringe: PriorityQueue, goal):
    new = cost_so_far[s] + edge.weight
    if new < cost_so_far[e]:
        cost_so_far[e] = new
        parent[e] = s
        fringe.put((cost_so_far[e] + heuristic(e, goal), e))

def a_star(start, goal, edges):
    print("Start: " + str(start))
    print("Goal: " + str(goal))
    fringe = PriorityQueue() # [(f, (x, y))]
    closed = []
    cost_so_far = dict()
    parent = dict()
    
    cost_so_far[start] = 0
    parent[start] = start
    fringe.put((0, start))

    while not fringe.empty():
        t = fringe.get()
        s = t[1]

        if s == goal:
            print("Path Found with cost: " + str(t[0]))
            curr = s
            p = parent[s]
            while p != start:
                print(curr)
                curr = p
                p = parent[p]
            print(curr)
            print(p)
            return

        closed.append(s)
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = s[0]
                y = s[1]
                end = (x + i, y + j)
                if end in closed:
                    continue

                edge = get_edge(s, end, edges)
                if not edge:
                    continue

                is_new = True
                for element in fringe.queue:
                    if element[1] == end:
                        is_new = False

                if is_new:
                    cost_so_far[end] = float('inf')
                    parent[end] = None
                update_vertex(s, end, cost_so_far, parent, edge, fringe, goal)

    print("No path found")