from graph import Terrain
from graph import Node
from operator import add
import numpy as np
import sys

class transition_array:
    def __init__(self, array, p1, p2):
        self.array = array
        self.p1 = p1
        self.p2 = p2

# Size of the world
size = 9
num_rows = 3
num_cols = 3

# PR of executing a move
PR_DO_MOVE = .9

# PR of failing to move
PR_STAY = .1

# PR of detecting the actual terrain we're on
PR_CORRECT_T = .9

# PR of incorrectly detecting the terrain we're on
PR_INCORRECT_T = .1

# PR of choosing incorrectly and picking a certain terrain (not including blocked)
PR_OTHER = .05

# Multiplies corresponding elements of two equally size vectors
# If one vector is of size 1, the other vector is scaled by that value
# Otherwise, return an empty list
def point_mult(v1, v2):
    ret = []
    if len(v1) == len(v2):
        ret = np.multiply(v1, v2)
        #ret = map(lambda x,y : x * y, v1, v2)
    elif len(v1) == 1:
        ret = np.multiply(v2, v1[0])
        #ret = map(lambda x : x * v1[0], v2)
    elif len(v2) == 1:
        ret = np.multiply(v1, v2[0])
        #ret = map(lambda x : x * v2[0], v1)
    return ret

def point_mult_trans(t_array, v):
    arr = t_array.array
    p1 = t_array.p1
    p2 = t_array.p2
    if len(arr) == len(v):
        arr[p1] *= v[p1]
        arr[p2] *= v[p2]
    elif len(v) == 1:
        arr[p1] *= v[0]
        arr[p2] *= v[0]
    return arr

# Adds corresponding elements of two equally sized vectors
def add_vectors(v1, v2):
    if (len(v1) == 0):
        return v2
    if (len(v2) == 0):
        return v1
    if len(v1) != len(v2):
        return None
    return list(map(add, v1, v2))

# Iterate over all cells, xi, and calculate P(e | xi)
def observation(world, e):
    p = []
    for i in range(size):
        xi = world[i // num_cols][i % num_cols]
        if xi.terrain == Terrain.B:
            continue
        if xi.terrain == e:
            p.append(PR_CORRECT_T)
        else:
            p.append(PR_OTHER)
    return p

def get_dir(action):
    deltax = 0
    deltay = 0
    if action == 'U':
        deltay = -1
    elif action == 'D':
        deltay = 1
    elif action == 'L':
        deltax = -1
    elif action == 'R':
        deltax = 1
    return (deltay, deltax)

def index_check(row, col):
    ret = True
    if row < 0 or row >= num_rows or col < 0 or col >= num_cols:
        ret = False;
    return ret

# Over every cell in the world, calculates the probability of being in that
# cell, Xi, given the prev cell, xi
# Returns a vector containing the probability for all unblocked cells
def transition_old(world, xi, action):
    #print(str(xi.x) + " " + str(xi.y))
    move = get_dir(action)
    p = []
    destx = xi.x + move[0]
    desty = xi.y + move[1]

    for i in range(size):
        Xi = world[i // num_cols][i % num_cols]
        if Xi.terrain == Terrain.B:
            continue
        if destx == Xi.x and desty == Xi.y and Xi.terrain != Terrain.B:
            p.append(PR_DO_MOVE)
        elif xi.x == Xi.x and xi.y == Xi.y:
            # If we are going out of bounds or to a blocked cell, stay with 100% certainty.
            if not index_check(destx - 1, desty - 1) or world[destx - 1][desty - 1].terrain == Terrain.B:
                p.append(1.0)
            else:
                p.append(PR_STAY)
        else:
            p.append(0.0)
    return p


# Over every cell in the world, calculates the probability of being in that
# cell, Xi, given the prev cell, xi
# Returns a vector containing the probability for all unblocked cells
def transition(world, xi, action):
    #print(str(xi.x) + " " + str(xi.y))
    move = get_dir(action)
    exit(1)
    p = [0 for i in range(size)]
    destx = xi.x + move[0]
    desty = xi.y + move[1]

    if not index_check(destx - 1, desty - 1) or world[destx - 1][desty - 1].terrain == Terrain.B:
        p[(num_cols * (xi.x - 1)) + (xi.y - 1)] = 1.0
        ret = transition_array(p, (num_cols * (xi.x - 1)) + (xi.y - 1), 0)
    else:
        p[(num_cols * (xi.x - 1)) + (xi.y - 1)] = PR_STAY
        p[(num_cols * (destx - 1)) + (desty - 1)] = PR_DO_MOVE
        ret = transition_array(p, (num_cols * (xi.x - 1)) + (xi.y - 1), (num_cols * (destx - 1)) + (desty - 1))
    return ret

# Uses DP to calculate the probability
# State_seq and action_seq decrease in size from the front by 1 each iteration
# The function stops when there's no states and actions left.
def filter_method(world, state_seq, action_seq, prev):
    if not state_seq or not action_seq:
        return

    # Summation
    # ----------
    # This loop represents the outer sigma, where we traverse over all the calculated
    # probabilites over the domain of the previous state. If this is the fist call,
    # prev is a preset probability. The prev list should be the size of the world -
    # the number of blocked cells, as we cannot traverse them.
    idx = 0 # Only keeps track of how many unblocked cells are seen
    for i in range(size):
        prev_cell = world[i // num_cols][i % num_cols]

        # Can't move from blocked cell
        if prev_cell.terrain == Terrain.B:
            continue

        # This loop represents P(Xt | xt-1) * P(xt-1|e). We loop over every cell in the world
        # and get the probability that we are at each cell given our previous cell, xt-1, and
        # our action.
        summation = []
        for j in range(size):
            curr_cell = world[j // num_cols][j % num_cols]
            if curr_cell.terrain == Terrain.B:
                continue
            t_model = transition(world, curr_cell, action_seq[0])
            ans = point_mult_trans(t_model, [prev[idx]])
            # Summation vector += t_model vector * prev[i]
            # summation = add_vectors(summation, ans)
            # idx += 1
        idx = 0
        exit(1)
    # o_model * summation
    o_model = observation(world, state_seq[0])
    p = point_mult(o_model, summation)
    normalized_factor = list(np.full(len(p), 1.0 / sum(p)))
    p = point_mult(p, normalized_factor)
    print(p)
    print()

    filter_method(world, state_seq[1:], action_seq[1:], p)

def pre_build():
    world = []
    world.append([Node(1,1,Terrain.H), Node(1,2,Terrain.H), Node(1,3,Terrain.T)])
    world.append([Node(2,1,Terrain.N), Node(2,2,Terrain.N), Node(2,3,Terrain.N)])
    world.append([Node(3,1,Terrain.N), Node(3,2,Terrain.B), Node(3,3,Terrain.H)])
    return world

def read_file(file_name):
    with open(file_name, 'r') as f:
        return [l.strip() for l in f.readlines()]

def main():
    world_file = sys.argv[1]
    action_results_file = sys.argv[2]
    world = read_file(world_file)
    action_results = read_file(action_results_file)

    state_seq = []
    for c in action_results[len(action_results) - 1]:
        if c == 'N':
           state_seq.append(Terrain.N)
        elif c == 'T':
            state_seq.append(Terrain.T)
        elif c == 'H':
            state_seq.append(Terrain.H)

    action_seq = []
    for c in action_results[len(action_results) - 2]:
        action_seq.append(c)

    global num_rows
    global num_cols
    global size
    world_size = world[0].split()
    num_rows = int(world_size[0])
    num_cols = int(world_size[1])
    size = num_rows * num_cols

    num_unblocked = 0
    world_nodes = []
    row = []
    for i in range(1, len(world)):
        line = world[i].split()
        row.append(Node(int(line[0]), int(line[1]), Terrain(line[2])))
        if Terrain(line[2]) != Terrain.B:
            num_unblocked += 1
        if len(row) == num_cols:
            world_nodes.append(row)
            row = []
    init_distr = list(np.full(num_unblocked, 1.0 / float(num_unblocked)))
    filter_method(world_nodes, state_seq, action_seq, init_distr)

if __name__ == '__main__':
    main()
