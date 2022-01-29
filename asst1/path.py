import random
import math
import tkinter as tk
from graph_ent import Node, Edge

nodes = []
edges = dict()

WIDTH = 100
HEIGHT = 50
SCALE = 25

def init_graph(g_nodes):
    for x in range(WIDTH + 1):
        row = []
        for y in range(HEIGHT + 1):
            if x == WIDTH or y == HEIGHT:
                b = 1
            else:
                b = g_nodes[(x,y)]
            row.append(Node(x, y, b))
        nodes.append(row)

    for x in range(WIDTH + 1):
        for y in range(HEIGHT + 1):
            #top left
            if x > 0 and y > 0 and nodes[x-1][y-1].blocked == 0:
                edges[((x,y),(x-1,y-1))] = Edge((x,y), (x-1,y-1), math.sqrt(2))
            #top right
            if x < WIDTH and y > 0 and nodes[x][y-1].blocked == 0:
                edges[((x,y),(x+1, y-1))] = Edge((x,y), (x+1, y-1), math.sqrt(2))
            #up
            if y > 0:
                if x == 0 and nodes[x][y-1].blocked == 0:
                    edges[((x,y),(x, y-1))] = Edge((x,y), (x, y-1), 1)
                elif x > 0 and (nodes[x-1][y-1].blocked == 0 or nodes[x][y-1].blocked == 0):
                    edges[((x,y),(x, y-1))] = Edge((x,y), (x, y-1), 1)
            #right
            if x < WIDTH:
                if y == 0 and nodes[x][y].blocked == 0:
                    edges[((x,y),(x+1, y))] = Edge((x,y), (x+1, y), 1)
                elif y > 0 and (nodes[x][y-1].blocked == 0 or nodes[x][y].blocked == 0):
                    edges[((x,y),(x+1, y))] = Edge((x,y), (x+1, y), 1)

def create_grid(start, end):
    w = c.winfo_width() # Get current width of canvas
    h = c.winfo_height() # Get current height of canvas
    #c.delete('grid_line') # Will only remove the grid_line

    for row in nodes:
        for node in row:
            if node.blocked == 1:
                c.create_rectangle(node.x * SCALE, node.y * SCALE, (node.x + 1) * SCALE, (node.y + 1) * SCALE, fill='gray', outline='')


    for edge in edges.values():
        p1 = edge.p1
        p2 = edge.p2
        c.create_line([(p1[0] * SCALE, p1[1] * SCALE), (p2[0] * SCALE, p2[1] * SCALE)])

    c.create_oval(scale(start[0]) - 5,
                  scale(start[1]) + 5,
                  scale(start[0]) + 5,
                  scale(start[1]) - 5,
                  fill='blue'
                 )
    c.create_oval(scale(end[0]) - 5,
                  scale(end[1]) + 5,
                  scale(end[0]) + 5,
                  scale(end[1]) - 5,
                  fill='red'
                 )

def scale(x):
    return x * SCALE

def choose_endpoints():
    r1 = random.randrange(100) * SCALE
    r2 = random.randrange(50) * SCALE
    start = (r1, r2)
    print(start)
    e1 = random.randrange(100) * SCALE
    e2 = random.randrange(50) * SCALE
    end = (e1, e2)

    return (start, end)

def zoom_out():
    global SCALE
    SCALE = SCALE / 2
    create_grid()
    print("zoomed out")

def zoom_in():
    global SCALE
    SCALE = SCALE * 2
    create_grid()
    print("zoomed in")

#init_graph(g_nodes)
endpoints = choose_endpoints()

#Create main window
root = tk.Tk()

#Set window size
root.geometry("1600x900")

#Set window title
root.title("Path Finding")

#c = tk.Canvas(root, height=SCALE * HEIGHT, width=SCALE * WIDTH, bg='gray')
#c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#create_grid()
#c.bind('<Configure>', create_grid)

#Sets up a canvas and scrollbars inside of a frame
frame = tk.Frame(root, width = SCALE * WIDTH, height = SCALE * HEIGHT)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
c = tk.Canvas(frame,
              width = SCALE * WIDTH,
              height = SCALE * HEIGHT,
              scrollregion = (0, 0, SCALE * WIDTH, SCALE * HEIGHT)
             )
hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
hbar.pack(side=tk.BOTTOM, fill=tk.X)
hbar.config(command=c.xview)
vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT, fill=tk.Y)
vbar.config(command=c.yview)
c.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

menubar = tk.Menu(root)
zoom_menu = tk.Menu(menubar, tearoff=0)
zoom_menu.add_command(label="In", command=zoom_in)
zoom_menu.add_command(label="Out", command=zoom_out)
menubar.add_cascade(label="Zoom", menu=zoom_menu)
root.config(menu=menubar)

with open("graph.txt", 'r') as f:
    line = f.readline().strip().split()
    start = (int(line[0]),int(line[1]))
    line = f.readline().strip().split()
    end = (int(line[0]),int(line[1]))
    line = f.readline().strip().split()
    WIDTH = int(line[0])
    HEIGHT = int(line[1])
    g_nodes = dict()
    for line in f.readlines():
        split = line.strip().split()
        g_nodes[(int(split[0]),int(split[1]))] = int(split[2])
    init_graph(g_nodes)
    create_grid(start, end)

root.mainloop()

