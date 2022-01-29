import random

nodes = dict()
range_x = 100 # How large the X-axis will be
range_y = 50 # How large the Y-axis will be

def gen_endpoints():
    while True:
        s1 = random.randrange(range_x)
        s2 = random.randrange(range_y)
        start = (s1, s2)
        if valid_endpoint(start):
            break

    while True:
        e1 = random.randrange(range_x)
        e2 = random.randrange(range_y)
        end = (e1, e2)
        if valid_endpoint(end):
            break

    return (start, end)

def valid_endpoint(p):
    s1 = p[0]
    s2 = p[1]
    if nodes[(s1,s2)] == False:
        #left
        if s1 > 0 and nodes[(s1-1,s2)] == True:
            return True
        #up
        if s2 > 0 and nodes[(s1,s2-1)] == True:
            return True
        #top left
        if s1 > 0 and s2 > 0 and nodes[(s1-1,s2-1)] == True:
            return True
        return False
    return True

def gen_cells():
    for x in range(range_x):
        for y in range(range_y):
            nodes[(x,y)] = True

    perc_blocked = float(0)
    num_blocked = 0
    while perc_blocked < float(.1):
        randx = random.randrange(range_x)
        randy = random.randrange(range_y)
        if nodes[(randx, randy)] is True:
            nodes[(randx, randy)] = False
            num_blocked += 1
            perc_blocked = float(num_blocked / (range_x * range_y))

gen_cells()
endpoints = gen_endpoints()
with open("graph.txt", 'w') as f:
    f.write(str(endpoints[0][0]) + " " + str(endpoints[0][1]) + "\n")
    f.write(str(endpoints[1][0]) + " " + str(endpoints[1][1]) + "\n")
    f.write(str(range_x) + " " + str(range_y) + "\n")
    for x in range(range_x):
        for y in range(range_y):
            blocked = 0
            if nodes[(x,y)] is False:
                blocked = 1
            f.write(str(x) + " " + str(y) + " " + str(blocked) + "\n")