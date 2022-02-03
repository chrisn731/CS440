import random
from a_star import a_star
import math
import tkinter as tk
from graph_ent import Node, Edge

# TODO: Remove commented out code that is no longer used

# Nodes 2d array.
# nodes[x][y] returns the location of a Node at the coordinate x,y
nodes = []

# Edges dictionary.
# To use: edges[((x0, y0), (x1, y1))] returns the edge where the starting
# point is x0, y0 and the ending point is x1, y1.
edges = dict()
c = None # Canvas

WIDTH = 100
HEIGHT = 50
SCALE = 25  # Scale factor for the elements to show properly on the canvas
MIN_SCALE = 25
MAX_SCALE = 100

# init_graph - initialize the graph data structures.
# Builds the nodes (vertexes) into the 2d nodes array
# Builds the edges dictionary
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

    # Time to build the edges!
    for x in range(WIDTH + 1):
        for y in range(HEIGHT + 1):
            # Draw edge to the top left
            if x > 0 and y > 0 and nodes[x-1][y-1].blocked == 0:
                edges[((x,y),(x-1,y-1))] = Edge((x,y), (x-1,y-1), math.sqrt(2))

            # Draw edge to the top right
            if x < WIDTH and y > 0 and nodes[x][y-1].blocked == 0:
                edges[((x,y),(x+1, y-1))] = Edge((x,y), (x+1, y-1), math.sqrt(2))

            # Draw edge straight up
            if y > 0:
                if x == 0 and nodes[x][y-1].blocked == 0:
                    edges[((x,y),(x, y-1))] = Edge((x,y), (x, y-1), 1)
                elif x > 0 and (nodes[x-1][y-1].blocked == 0 or nodes[x][y-1].blocked == 0):
                    edges[((x,y),(x, y-1))] = Edge((x,y), (x, y-1), 1)

            # Draw edge to the right
            if x < WIDTH:
                if y == 0 and nodes[x][y].blocked == 0:
                    edges[((x,y),(x+1, y))] = Edge((x,y), (x+1, y), 1)
                elif y > 0 and (nodes[x][y-1].blocked == 0 or nodes[x][y].blocked == 0):
                    edges[((x,y),(x+1, y))] = Edge((x,y), (x+1, y), 1)

# create_grid - Draws elements on the canvas
def create_grid(start, end):
    w = c.winfo_width() # Get current width of canvas
    h = c.winfo_height() # Get current height of canvas
    #c.delete('grid_line') # Will only remove the grid_line

    # Draw the blocked cells
    for row in nodes:
        for node in row:
            if node.blocked == 1:
                c.create_rectangle(scale(node.x),
                                    scale(node.y),
                                    scale(node.x + 1),
                                    scale(node.y + 1),
                                    fill='gray',
                                    outline='')

    # Draw the edges
    for edge in edges.values():
        p1 = edge.p1
        p2 = edge.p2
        c.create_line([(scale(p1[0]), scale(p1[1])), (scale(p2[0]), scale(p2[1]))])

    offset = int(SCALE / 5)

    # Draw the start point
    c.create_oval(scale(start[0]) - offset,
                  scale(start[1]) + offset,
                  scale(start[0]) + offset,
                  scale(start[1]) - offset,
                  fill='blue')

    # Draw the end point
    c.create_oval(scale(end[0]) - offset,
                  scale(end[1]) + offset,
                  scale(end[0]) + offset,
                  scale(end[1]) - offset,
                  fill='red')

# init_window - Initalize the tkinter window
# Sets up the window, frame, scrolling, etc.
def init_window(root):
    global c
    #Set window size
    root.geometry("1600x900")

    #Set window title
    root.title("Path Finding")

    #c = tk.Canvas(root, height=SCALE * HEIGHT, width=SCALE * WIDTH, bg='gray')
    #c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    #create_grid()
    #c.bind('<Configure>', create_grid)

    #Set up topbar
    topbar = tk.Frame(root, width = scale(WIDTH), height = 20)
    topbar.pack(fill=tk.BOTH, expand=True)
    label_x = tk.Label(topbar, text="X: ")
    label_x.grid(row=0, column=0)
    button1 = tk.Text(topbar, width=5, height=1)
    button1.grid(row=0, column=1)
    label_y = tk.Label(topbar, text="Y: ")
    label_y.grid(row=0, column=2)
    button2 = tk.Text(topbar, width=5, height=1)
    button2.grid(row=0, column=3)


    #Sets up a canvas and scrollbars inside of a frame
    frame = tk.Frame(root, width = scale(WIDTH), height = scale(HEIGHT))
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    c = tk.Canvas(frame,
                width = scale(WIDTH),
                height = scale(HEIGHT),
                scrollregion = (0, 0, scale(WIDTH), scale(HEIGHT)))
    hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    hbar.pack(side=tk.BOTTOM, fill=tk.X)
    hbar.config(command=c.xview)
    vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    vbar.pack(side=tk.RIGHT, fill=tk.Y)
    vbar.config(command=c.yview)
    c.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    menubar = tk.Menu(root)
    algorithms_menu = tk.Menu(menubar, tearoff=0)
    algorithms_menu.add_command(label="A*")
    algorithms_menu.add_command(label="Theta*")
    menubar.add_cascade(label="Algorithms", menu=algorithms_menu)
    zoom_menu = tk.Menu(menubar, tearoff=0)
    zoom_menu.add_command(label="In", command=zoom_in)
    zoom_menu.add_command(label="Out", command=zoom_out)
    menubar.add_cascade(label="Zoom", menu=zoom_menu)
    root.config(menu=menubar)

    c.bind("<Button-1>", mouse_click)

def mouse_click(event):
    x = c.canvasx(event.x)
    y = c.canvasy(event.y)
    modx = x % SCALE
    mody = y % SCALE
    lower_thresh = int(.2 * SCALE)
    upper_thresh = SCALE - int(.2 * SCALE)

    if modx < lower_thresh:
        x = x - modx
    elif modx > upper_thresh:
        x = x + (SCALE - modx)
    else:
        return

    if mody < lower_thresh:
        y = y - mody
    elif mody > upper_thresh:
        y = y + (SCALE - mody)
    else:
        return

    offset = int(SCALE / 5)
    c.create_oval(x - offset,
                  y + offset,
                  x + offset,
                  y - offset,
                  fill='white')


    print(x)
    print(y)

# Scale a number for the canvas
def scale(x):
    return x * SCALE

# TODO: I dont think we need this anymore
def choose_endpoints():
    r1 = scale(random.randrange(100))
    r2 = scale(random.randrange(50))
    start = (r1, r2)
    e1 = scale(random.randrange(100))
    e2 = scale(random.randrange(50))
    end = (e1, e2)
    return (start, end)

def do_draw(p1, p2):
    pass

def draw_path(path):
    for i in range(len(path) - 1):
        p1 = path[i]
        p2 = path[i + 1]
        c.create_line([(scale(p1[0]), scale(p1[1])), (scale(p2[0]), scale(p2[1]))], fill='red', width=3)

def zoom_out():
    global SCALE
    if SCALE <= MIN_SCALE:
        return

    c.delete("all")
    SCALE = SCALE / 2
    create_grid((0,0), (0,1))
    print("zoomed out")

#TODO: Scroll doesn't cover whole canvas; dots move to 0,0
def zoom_in():
    global SCALE
    if SCALE >= MAX_SCALE:
        return

    c.delete("all")
    SCALE = SCALE * 2
    create_grid((0,0), (0,1))
    print("zoomed in")

if __name__ == "__main__":
    #init_graph(g_nodes)
    endpoints = choose_endpoints()

    # Create main window
    root = tk.Tk()
    init_window(root)

    with open("graph.txt", 'r') as f:
        line = f.readline().strip().split()
        start = (int(line[0]), int(line[1])) # Get the start point
        line = f.readline().strip().split()
        end = (int(line[0]), int(line[1])) # Get the end point
        line = f.readline().strip().split()
        WIDTH = int(line[0])
        HEIGHT = int(line[1])

    # Everything from here on is about (un)blocked cells...
        g_nodes = dict()
        for line in f.readlines():
            split = line.strip().split()
            g_nodes[(int(split[0]), int(split[1]))] = int(split[2])

        init_graph(g_nodes)
        create_grid(start, end)
    path = a_star(start, end, edges)
    draw_path(path)
    root.mainloop() # Startup UI
