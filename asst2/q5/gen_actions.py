import sys
import random
import os
import shutil
from graph import Terrain

GRAPH_DIR = "./actions/"
NUM_ACTIONS = 100
width = 0
height = 0
cells = dict()

# Generate the start and goal points for the graph.
# This also ensures that the points will reside on a valid cell.
# More specifically, ensures that a point can not spawn in the middle
# of some blocked cells.
def gen_src(nodes, width, height):
    while True:
        s1 = random.randrange(width)
        s2 = random.randrange(height)
        start = (s1, s2)
        if valid_endpoint(start, nodes):
            break

    return start

# Checks that a point is not in an area of blocked cells
def valid_endpoint(p, nodes):
    s1 = p[0]
    s2 = p[1]

    if nodes[(s1,s2)] == Terrain.B:
        return False
    return True



def read_file(fi):
    with open(fi, 'r') as f:
        line = f.readline().strip().split()
        global width
        global height
        width = int(line[0])
        height = int(line[1])

        # Everything from here on is about (un)blocked cells...
        for line in f.readlines():
            split = line.strip().split()
            if split[2] == 'N':
                e = Terrain.N
            elif split[2] == 'H':
                e = Terrain.H
            elif split[2] == 'T':
                e = Terrain.T
            elif split[2] == 'B':
                e = Terrain.B
            cells[(int(split[0]) - 1, int(split[1]) - 1)] = e

def gen_sequence(cells, width, height):
    src = gen_src(cells, width, height)
    action_str = ""
    for x in range(NUM_ACTIONS):
        rand = random.random()
        if rand <= .25:
            action_str += 'U'
        elif rand <= .5:
            action_str += 'R'
        elif rand <= .75:
            action_str += 'L'
        elif rand <= 1.0:
            action_str += 'D'
    return (src, action_str)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Bad usage!!!")
        exit(1)

    read_file(sys.argv[1])
    gen_src(cells)

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
        graph_fname = graphs_path + "actions" + str(i) + ".txt"
        with open(graph_fname, 'w') as f:
            for x in range(NUM_ACTIONS):
                rand = random.random()
                if rand <= .25:
                    action = "UP"
                elif rand <= .5:
                    action = "RIGHT"
                elif rand <= .75:
                    action = "LEFT"
                elif rand <= 1.0:
                    action = "DOWN"
                f.write(action + "\n")
