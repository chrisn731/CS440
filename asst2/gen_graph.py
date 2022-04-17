import random
import shutil
import os
from graph import Terrain

GRAPH_DIR = "./graphs/" # Name of the directory to create
range_x = 100 # How large the X-axis will be
range_y = 50 # How large the Y-axis will be
N_PERCENT = .5
H_PERCENT = .2
T_PERCENT = .2
B_PERCENT = .1
terrain_distr = {Terrain.N: N_PERCENT, Terrain.H: H_PERCENT,
        Terrain.T: T_PERCENT, Terrain.B: B_PERCENT}

def set_attr(nodes, terrain_type, thresh):
    percent = float(0)
    count = 0
    while percent < thresh:
        randx = random.randrange(range_x)
        randy = random.randrange(range_y)
        if nodes.get((randx, randy), None) is None:
            nodes[(randx, randy)] = terrain_type
            count += 1
            percent = float(count) / float(range_x * range_y)

# Generate the cells for the graph.
# It creates both open and blocked cells.
def gen_cells(nodes):
    for x in range(range_x):
        for y in range(range_y):
            nodes[(x,y)] = None

    for terrain_type, percent in terrain_distr.items():
        set_attr(nodes, terrain_type, percent)


def gen_world():
    nodes = dict()
    gen_cells(nodes)
    return nodes

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
for i in range(1):
    nodes = dict()
    graph_fname = graphs_path + "graph" + str(i) + ".txt"
    gen_cells(nodes)
    with open(graph_fname, 'w') as f:
        f.write(str(range_x) + " " + str(range_y) + "\n")
        for x in range(range_x):
            for y in range(range_y):
                if nodes[(x,y)] == Terrain.N:
                    letter = 'N'
                elif nodes[(x,y)] == Terrain.H:
                    letter = 'H'
                elif nodes[(x,y)] == Terrain.T:
                    letter = 'T'
                else:
                    letter = 'B'

                f.write(str(x + 1) + " " + str(y + 1) + " " + str(letter) + "\n")
