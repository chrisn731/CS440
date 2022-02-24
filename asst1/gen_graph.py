import random
import shutil
import os

GRAPH_DIR = "./graphs/" # Name of the directory to create
range_x = 100 # How large the X-axis will be
range_y = 50 # How large the Y-axis will be
BLOCKED_PERCENT = .1 # Fraction of the cells to be blocked
NUM_GEN_GRAPHS = 50 # Number of graphs to be generated`

# Generate the start and goal points for the graph.
# This also ensures that the points will reside on a valid cell.
# More specifically, ensures that a point can not spawn in the middle
# of some blocked cells.
def gen_endpoints(nodes):
    while True:
        s1 = random.randrange(range_x)
        s2 = random.randrange(range_y)
        start = (s1, s2)
        if valid_endpoint(start, nodes):
            break

    while True:
        e1 = random.randrange(range_x)
        e2 = random.randrange(range_y)
        end = (e1, e2)
        if end != start and valid_endpoint(end, nodes):
            break

    return (start, end)

# Checks that a point is not in an area of blocked cells
def valid_endpoint(p, nodes):
    s1 = p[0]
    s2 = p[1]

    # If the point we chose belongs to a blocked cell we need to check...
    if nodes[(s1,s2)] == False:
        # Is the node to the left of us open?
        if s1 > 0 and nodes[(s1-1,s2)]:
            return True
        # Is the node above us open?
        if s2 > 0 and nodes[(s1,s2-1)]:
            return True
        # Is the node to our top left open?
        if s1 > 0 and s2 > 0 and nodes[(s1-1,s2-1)]:
            return True
        return False
    return True

# Generate the cells for the graph.
# It creates both open and blocked cells.
def gen_cells(nodes):
    for x in range(range_x):
        for y in range(range_y):
            nodes[(x,y)] = True

    perc_blocked = float(0)
    num_blocked = 0
    while perc_blocked < BLOCKED_PERCENT:
        randx = random.randrange(range_x)
        randy = random.randrange(range_y)
        if nodes[(randx, randy)] is True:
            nodes[(randx, randy)] = False
            num_blocked += 1
            perc_blocked = float(num_blocked / (range_x * range_y))

# Wipe out the currently existing graphs if it exists
graphs_path = os.path.join(os.getcwd(), GRAPH_DIR)
if os.path.exists(graphs_path):
    try:
        shutil.rmtree(graphs_path)
    except OSError as e:
        print("Error removing (%s): %s" % (graphs_path, e.strerror))

# Create the graphs directory
try:
    os.mkdir(graphs_path)
except OSError as e:
    if not os.path.exists(graphs_path):
        print("Error creating graph directory!")
        print("Error: %s" % (e.strerror))
        exit(1)

# Begin generating our graph files
for i in range(NUM_GEN_GRAPHS):
    nodes = dict()
    graph_fname = graphs_path + "graph" + str(i) + ".txt"
    gen_cells(nodes)
    endpoints = gen_endpoints(nodes)
    with open(graph_fname, 'w') as f:
        f.write(str(endpoints[0][0] + 1) + " " + str(endpoints[0][1] + 1) + "\n")
        f.write(str(endpoints[1][0] + 1) + " " + str(endpoints[1][1] + 1) + "\n")
        f.write(str(range_x) + " " + str(range_y) + "\n")
        for x in range(range_x):
            for y in range(range_y):
                blocked = 0
                if not nodes[(x,y)]:
                    blocked = 1
                f.write(str(x + 1) + " " + str(y + 1) + " " + str(blocked) + "\n")
