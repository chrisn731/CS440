from queue import PriorityQueue
import math

def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))

def update_vertex(s, e, cost_so_far, parent, nodes, edge, fringe, goal):
    if line_of_sight(parent[s], e, nodes):
        # We found a straight line from our parent to the destination
        new = cost_so_far[parent[s]] + distance(parent[s], e)
        if new < cost_so_far[e]:
            cost_so_far[e] = new
            parent[e] = parent[s]
            fringe.put((cost_so_far[e] + heuristic(e, goal), e))
    else:
        new = cost_so_far[s] + edge.weight
        if new < cost_so_far[e]:
            cost_so_far[e] = new
            parent[e] = s
            fringe.put((cost_so_far[e] + heuristic(e, goal), e))

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

def line_of_sight(s, e, nodes):
    x0 = s[0]
    y0 = s[1]
    x1 = e[0]
    y1 = e[1]
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
            if dx == 0 and nodes[x0][y0 + ((sy - 1)//2)] and nodes[x0 - 1][y0 + ((sy - 1)//2)]:
                return False
            y0 += sy
    return True

def theta_star(start, goal, nodes, edges):
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
                update_vertex(s, end, cost_so_far, parent, nodes, edge, fringe, goal)

    print("No path found")