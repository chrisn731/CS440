from queue import PriorityQueue
from graph_ent import Edge
import math
import window

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

def a_star(window, start, goal, nodes, edges):
    print("Start: " + str(start))
    print("Goal: " + str(goal))
    fringe = PriorityQueue() # [(f, (x, y))]
    closed = []
    cost_so_far = dict()
    parent = dict()
    answer = []

    cost_so_far[start] = 0
    parent[start] = start
    fringe.put((0, start))

    while not fringe.empty():
        t = fringe.get()
        s = t[1]

        if s == goal:
            for i in range(len(nodes)):
                for j in range(len(nodes[i])):
                    if (i, j) in cost_so_far:
                        nodes[i][j].g = cost_so_far[(i,j)]
                    else:
                        nodes[i][j].g = 0
                    nodes[i][j].h = heuristic((i,j), goal)
                    nodes[i][j].f = nodes[i][j].h + nodes[i][j].g
            print("Path Found with cost: " + str(t[0]))
            curr = s
            p = parent[s]
            while p != start:
                print(curr)
                answer.append(curr)
                curr = p
                p = parent[p]
            print(curr)
            print(p)
            answer.append(curr)
            answer.append(p)
            print(answer)
            break

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
                window.draw_line(s, end)

    if len(answer) == 0:
        print("No path found")
    return answer
