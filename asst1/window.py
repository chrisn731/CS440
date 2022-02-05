import tkinter as tk

class Window():
    DELAY_INC = 10
    def __init__(self, x, y):
        self.delay = 0
        self.x = x
        self.y = y
        self.root = tk.Tk()
        self.c = None
        self.WIDTH = 100
        self.HEIGHT = 50
        self.SCALE = 25  # Scale factor for the elements to show properly on the canvas
        self.MIN_SCALE = 25
        self.MAX_SCALE = 100
        self.selected = None
        self.selected_widget = None
        self.label_x = None
        self.label_y = None
        self.label_g = None
        self.label_h = None
        self.label_f = None
        self.init_window()

    def init_window(self):
        #Set window size
        self.root.geometry(str(self.x) + "x" + str(self.y))

        #Set window title
        self.root.title("Path Finding")

        #Set up topbar
        topbar = tk.Frame(self.root, width = self.scale(self.WIDTH), height = 20)
        topbar.pack(fill=tk.BOTH, expand=True)
        label_cell = tk.Label(topbar, text="Selected node: ")
        label_cell.grid(row=0, column=0)
        self.label_x = tk.Label(topbar, text="(x, ")
        self.label_x.grid(row=0, column=1)
        self.label_y = tk.Label(topbar, text="y)")
        self.label_y.grid(row=0, column=2)
        self.label_g = tk.Label(topbar, text="g: ")
        self.label_g.grid(row=0, column=3)
        self.label_h = tk.Label(topbar, text="h: ")
        self.label_h.grid(row=0, column=4)
        self.label_f = tk.Label(topbar, text="f: ")
        self.label_f.grid(row=0, column=5)
        #Sets up a canvas and scrollbars inside of a frame
        frame = tk.Frame(self.root, width = self.scale(self.WIDTH), height = self.scale(self.HEIGHT))
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.c = tk.Canvas(frame,
                    width = self.scale(self.WIDTH),
                    height = self.scale(self.HEIGHT),
                    borderwidth=0,
                    highlightthickness=0,
                    scrollregion = (0, 0, self.scale(self.WIDTH), self.scale(self.HEIGHT)))
        hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        hbar.config(command=self.c.xview)
        vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=self.c.yview)
        self.c.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        menubar = tk.Menu(self.root)
        algorithms_menu = tk.Menu(menubar, tearoff=0)
        algorithms_menu.add_command(label="A*")
        algorithms_menu.add_command(label="Theta*")
        menubar.add_cascade(label="Algorithms", menu=algorithms_menu)
        self.root.config(menu=menubar)

        self.c.bind("<Button-1>", self.mouse_click)

    def scale(self, x):
        return x * self.SCALE

    def draw_graph(self, graph):
        self.graph = graph
        start = graph.src
        end = graph.dst
        # Draw the blocked cells
        for row in graph.nodes:
            for node in row:
                if node.blocked == 1:
                    self.c.create_rectangle(self.scale(node.x),
                                        self.scale(node.y),
                                        self.scale(node.x + 1),
                                        self.scale(node.y + 1),
                                        fill='gray',
                                        outline='')

        # Draw the edges
        for edge in graph.edges.values():
            p1 = edge.p1
            p2 = edge.p2
            self.c.create_line([(self.scale(p1[0]), self.scale(p1[1])), (self.scale(p2[0]), self.scale(p2[1]))])

        offset = int(self.SCALE / 5)

        # Draw the start point
        self.start = self.c.create_oval(self.scale(start[0]) - offset,
                      self.scale(start[1]) + offset,
                      self.scale(start[0]) + offset,
                      self.scale(start[1]) - offset,
                      fill='green')

        # Draw the end point
        self.end = self.c.create_oval(self.scale(end[0]) - offset,
                      self.scale(end[1]) + offset,
                      self.scale(end[0]) + offset,
                      self.scale(end[1]) - offset,
                      fill='red')

    def mouse_click(self, event):
        x = self.c.canvasx(event.x)
        y = self.c.canvasy(event.y)
        modx = x % self.SCALE
        mody = y % self.SCALE
        lower_thresh = int(.2 * self.SCALE)
        upper_thresh = self.SCALE - int(.2 * self.SCALE)

        if modx < lower_thresh:
            x = x - modx
        elif modx > upper_thresh:
            x = x + (self.SCALE - modx)
        else:
            return

        if mody < lower_thresh:
            y = y - mody
        elif mody > upper_thresh:
            y = y + (self.SCALE - mody)
        else:
            return

        offset = int(self.SCALE / 5)
        self.c.delete(self.selected_widget)
        self.selected_widget = self.c.create_oval(x - offset,
                      y + offset,
                      x + offset,
                      y - offset,
                      fill='white')
        x = int(x / 25)
        y = int(y / 25)

        self.label_x.config(text="(" + str(x) + ",")
        self.label_y.config(text=str(y) + ")")
        self.label_g.config(text="g: " + str(self.graph.nodes[x][y].g))
        self.label_h.config(text="h: " + str(self.graph.nodes[x][y].h))
        self.label_f.config(text="f: " + str(self.graph.nodes[x][y].f))
        print(self.graph.nodes[x][y].g)
        print(self.graph.nodes[x][y].h)
        print(self.graph.nodes[x][y].f)
        x0 = self.c.canvasx(0)
        y0 = self.c.canvasy(0)
        #print("Visible region: (" + str(x0) + ", " + str(y0) + "), (" + str(x0 + self.c.winfo_width()) + ", " + str(y0 + self.c.winfo_height()) + ")")

    def __raise_ends(self):
        self.c.tag_raise(self.start)
        self.c.tag_raise(self.end)

    def __draw_line(self, p1, p2, fill, width):
        self.c.create_line([(self.scale(p1[0]), self.scale(p1[1])), (self.scale(p2[0]), self.scale(p2[1]))], fill=fill, width=width)
        if self.scale(p1[0]) < self.c.canvasx(0):
            self.c.xview_moveto((self.c.canvasx(0) - self.SCALE) / self.scale(self.WIDTH))
        if self.scale(p1[1]) < self.c.canvasy(0):
            self.c.yview_moveto((self.c.canvasy(0) - self.SCALE) / self.scale(self.HEIGHT))
        if self.scale(p2[0]) > (self.c.canvasx(0) + self.c.winfo_width()):
            self.c.xview_moveto((self.c.canvasx(0) + self.SCALE) / self.scale(self.WIDTH))
        if self.scale(p2[1]) > (self.c.canvasy(0) + self.c.winfo_height()):
            self.c.yview_moveto((self.c.canvasy(0) + self.SCALE) / self.scale(self.HEIGHT))

    def draw_line(self, p1, p2):
        self.c.after(self.delay, self.__draw_line, p1, p2, '#5c9aff', 1.5)
        self.delay += Window.DELAY_INC

    def draw_path(self, path):
        scale = self.scale
        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i + 1]
            self.c.after(self.delay, self.__draw_line, p1, p2, 'red', 3)
            self.delay += Window.DELAY_INC
            #self.c.create_line([(scale(p1[0]), scale(p1[1])), (scale(p2[0]), scale(p2[1]))], fill='red', width=3)

    def run(self):
        self.c.after(self.delay, self.__raise_ends)
        self.root.mainloop()
