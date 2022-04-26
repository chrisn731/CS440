import tkinter.filedialog as fd
import tkinter as tk
from PIL import Image, ImageTk
from filter_data import FilterData

class Window():
    def __init__(self, width, height):
        # The window
        self.root = tk.Tk()

        # Canvas that the world is drawn on
        self.canvas = None

        # Number of rows in the world
        self.num_rows = 0

        # Number of columns in the world
        self.num_cols = 0

        # Scale of all canvas objects
        self.scalar = 30

        # The filter_data object that stores the filter probabilites of our world
        self.filter_data = FilterData()

        # Tuple of cell widget IDs and their terrain type
        self.cells = []

        # Tracks whether we have a world file opened
        self.has_world = False

        # Tracks whether we have an actions file opened
        self.has_actions = False

        # Number of actions. Consequently, length of action_seq and sensor_seq
        self.NUM_ACTIONS = 100

        # String of all actions
        self.action_seq = ""

        # String of all senses (correspond to action_seq)
        self.sensor_seq = ""

        # Tracks which action/sensor index we are looking at.
        self.seq_idx = 0

        # All locations after a given action.
        # NOTE: Index 0 is the src. Index 1 corresponds to the first action
        self.locations = []

        # Number of unblocked cells
        self.num_unblocked = 0

        self.rover = None
        self.init_window(width, height)

    def init_window(self, width, height):
        # Action/sensor readings
        self.action_sensor = tk.Frame(self.root, height = 20)
        self.action_sensor.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10,0))
        title = tk.Label(self.action_sensor, text="Action/Sensor Readings")
        title.pack(side='top')

        action_bar = tk.Frame(self.root, height = 20)
        action_bar.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10,0))
        self.prev_actions_label = tk.Label(action_bar, text="")
        self.curr_action_label = tk.Label(action_bar, text="", fg='red')
        self.next_actions_label = tk.Label(action_bar, text="")
        self.prev_actions_label.grid(row = 0, column = 1)
        self.curr_action_label.grid(row = 0, column = 2)
        self.next_actions_label.grid(row = 0, column = 3)
        action_bar.grid_columnconfigure(0, weight = 1)
        action_bar.grid_columnconfigure(4, weight = 1)

        senses_bar = tk.Frame(self.root, height = 20)
        senses_bar.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10,0))
        self.prev_senses_label = tk.Label(senses_bar, text="")
        self.curr_sense_label = tk.Label(senses_bar, text="", fg='red')
        self.next_senses_label = tk.Label(senses_bar, text="")
        self.prev_senses_label.grid(row = 0, column = 1)
        self.curr_sense_label.grid(row = 0, column = 2)
        self.next_senses_label.grid(row = 0, column = 3)
        senses_bar.grid_columnconfigure(0, weight = 1)
        senses_bar.grid_columnconfigure(4, weight = 1)

        # Input to change position of action sequence
        self.input = tk.Frame(self.root)
        self.input.pack(fill=tk.BOTH, expand=True)
        tmp = Image.open("arrow_left.png").resize((20,20))
        self.arrow_left = ImageTk.PhotoImage(tmp)
        self.prev_btn = tk.Button(self.input, image=self.arrow_left,
                command=self.prev_action)
        self.prev_btn.grid(row=0, column=1)
        tmp = Image.open("arrow_right.png").resize((20,20))
        self.arrow_right = ImageTk.PhotoImage(tmp)
        self.next_btn = tk.Button(self.input, image=self.arrow_right,
                command=self.next_action)
        self.next_btn.grid(row=0, column=2)
        self.input.grid_columnconfigure(0, weight=1)
        self.input.grid_columnconfigure(3, weight=1)

        # Displays open files
        self.header = tk.Frame(self.root, height = 20)
        self.header.pack(fill=tk.BOTH, expand=True, padx=10)
        world_file = tk.Label(self.header, text="World:")
        world_file.grid(row = 0, column = 1)
        self.world_file_val = tk.Label(self.header, text="NA")
        self.world_file_val.grid(row = 0, column = 2)
        action_file = tk.Label(self.header, text="Action:")
        action_file.grid(row = 0, column = 4)
        self.action_file_val = tk.Label(self.header, text="NA")
        self.action_file_val.grid(row = 0, column = 5)
        self.header.grid_columnconfigure(3, weight=1)

        # Set up a canvas with scrollbars inside a frame
        frame = tk.Frame(self.root,
                         width = self.scale(self.num_cols),
                         height = self.scale(self.num_rows))
        frame.pack(fill=tk.BOTH, expand=True, padx=10)
        self.canvas = tk.Canvas(frame,
                    width = width,
                    height = height,
                    borderwidth=0,
                    highlightthickness=0,
                    scrollregion = (0, 0, self.scale(self.num_cols), self.scale(self.num_rows)))
        hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        hbar.config(command=self.canvas.xview)
        vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open world", command=lambda: self.load_world())
        file_menu.add_command(label="Open actions", command=lambda: self.load_actions())
        menubar.add_cascade(label="File", menu=file_menu)
        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="Start", command=self.do_simulation)
        menubar.add_cascade(label="Run", menu=run_menu)
        zoom_menu = tk.Menu(menubar, tearoff=0)
        zoom_menu.add_command(label="In", command=lambda: self.zoom(True))
        zoom_menu.add_command(label="Out", command=lambda: self.zoom(False))
        menubar.add_cascade(label="Zoom", menu=zoom_menu)
        self.root.config(menu=menubar)

    def load_world(self):
        file_name = self.browse_files('w')
        if not file_name:
            return
        self.has_world = True

        self.filter_data.load_world(file_name)

        with open(file_name, 'r') as f:
            dim = f.readline().split()
            cells = f.readlines()

        self.num_rows = int(dim[0])
        self.num_cols = int(dim[1])

        self.num_unblocked = 0
        cell_terrains = []
        for cell in cells:
            cell_attr = cell.split()
            cell_terrains.append(cell_attr[2])
            if cell_attr[2] != 'B':
                self.num_unblocked += 1
        file_name = file_name[file_name.rfind('/') + 1:]
        self.world_file_val.config(text=file_name)
        self.init_canvas(cell_terrains)
        self.seq_idx = 0

    def load_actions(self):
        file_name = self.browse_files('a')
        if not file_name:
            return
        self.has_actions = True

        with open(file_name, 'r') as f:
            locations = [next(f) for x in range(self.NUM_ACTIONS + 1)]
            self.action_seq = f.readline().strip()
            self.sensor_seq = f.readline().strip()

        self.locations = []
        for location in locations:
            coords = location.split(', ')
            self.locations.append((int(coords[0]), int(coords[1])))

        self.update_action_sensor_labels()
        self.filter_data.set_action_sensor_data(self.action_seq, self.sensor_seq)
        self.avg_err = self.filter_data.calculate_error(self.num_cols, self.num_rows, self.locations[1:], 5)
        self.set_rover_widget_pos(self.locations[0])
        file_name = file_name[file_name.rfind('/') + 1:]
        self.action_file_val.config(text=file_name)
        self.seq_idx = 0

    def browse_files(self, typ):
        if typ == 'w':
            f_dir = './graphs/'
        elif typ == 'a':
            f_dir = './results/'
        else:
            f_dir = './'
        file_name = fd.askopenfilename(initialdir=f_dir,
                                       filetypes=[('text files', '*.txt')])
        return file_name

    def set_rover_widget_pos(self, coords):
        if not self.rover:
            tmp = Image.open("mars-rover.png")
            tmp = tmp.resize((self.scalar - 5, self.scalar - 5))
            self.rover_img = ImageTk.PhotoImage(tmp)
            self.rover = self.canvas.create_image(0, 0, image=self.rover_img)
        #print("Setting rover to: " + str(coords[1]) + ", " + str(coords[0]))
        self.canvas.moveto(self.rover,
                self.scale(coords[1]) + 5/2,
                self.scale(coords[0]) + 5/2)

    def do_simulation():
       pass

    # Creates the tiles on the canvas and stores them in a list for future use.
    def init_canvas(self, cell_terrains):
        self.canvas.delete('all')
        self.rover = None
        self.cells = []

        # Traverses the world by columns, not rows, as the world file has
        # the world in column order
        for y in range(self.num_rows):
            row = []
            for x in range(self.num_cols):
                cell_id = self.canvas.create_rectangle(self.scale(x),
                       self.scale(y),
                       self.scale(x) + self.scalar,
                       self.scale(y) + self.scalar)
                cell_t = cell_terrains[y * self.num_cols + x]
                if cell_t == 'B':
                    color = 'gray'
                else:
                    color = 'white'
                self.canvas.itemconfig(cell_id, fill=color)
                self.canvas.create_text(self.scale(x) + 1 + .5 * self.scalar,
                        self.scale(y) + 1 + .5 * self.scalar,
                        text=cell_t)
                row.append((cell_id, cell_t))
            self.cells.append(row)

        # Reconfigure scrollbar to fit the world
        self.canvas.config(scrollregion = (0,
            0,
            self.scale(self.num_cols),
            self.scale(self.num_rows)))
        if self.has_actions:
            self.set_rover_widget_pos(self.locations[0])

    def update_action_sensor_labels(self):
        if self.seq_idx == 0:
            self.next_actions_label.config(text = self.action_seq)
            self.prev_actions_label.config(text = "")
            self.curr_action_label.config(text = "")

            self.prev_senses_label.config(text = "")
            self.curr_sense_label.config(text = "")
            self.next_senses_label.config(text = self.sensor_seq)
            return

        self.prev_actions_label.config(text = self.action_seq[:self.seq_idx - 1])
        self.curr_action_label.config(text = self.action_seq[self.seq_idx - 1:self.seq_idx])
        self.next_actions_label.config(text = self.action_seq[self.seq_idx:])

        self.prev_senses_label.config(text = self.sensor_seq[:self.seq_idx - 1])
        self.curr_sense_label.config(text = self.sensor_seq[self.seq_idx - 1:self.seq_idx])
        self.next_senses_label.config(text = self.sensor_seq[self.seq_idx:])

    def next_action(self):
        if not self.has_world or not self.has_actions:
            return
        self.seq_idx += 1
        if self.seq_idx > self.NUM_ACTIONS:
            self.seq_idx = 0
        #curr_state = self.filter_data.get_next_prob_distr()
        if self.seq_idx != 0:
            curr_state = self.filter_data.get_prob_distr_at(self.seq_idx - 1)
        else:
            # seq_idx == 0 is not really a state with valid probability distr
            curr_state = [0.0 for i in range(self.num_cols * self.num_rows)]
        self.draw_heat_map(curr_state)
        self.set_rover_widget_pos(self.locations[self.seq_idx])
        self.update_action_sensor_labels()

    def prev_action(self):
        if not self.has_world or not self.has_actions:
            return
        self.seq_idx -= 1
        if self.seq_idx < 0:
            self.seq_idx = self.NUM_ACTIONS
        if self.seq_idx != 0:
            curr_distr = self.filter_data.get_prob_distr_at(self.seq_idx - 1)
        else:
            # seq_idx == 0 is not really a state with valid probability distr
            curr_distr = [0.0 for i in range(self.num_cols * self.num_rows)]
        #curr_distr = self.filter_data.get_prev_prob_distr()
        #curr_distr = self.filter_data.get_prob_distr_at(self.seq_idx - 1)
        self.draw_heat_map(curr_distr)
        self.set_rover_widget_pos(self.locations[self.seq_idx])
        self.update_action_sensor_labels()

    # Draws the heat map at a given world state
    def draw_heat_map(self, pr_distr):
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                cell = self.cells[y][x]
                if cell[1] == 'B':
                    continue
                self.canvas.itemconfig(cell[0],
                        fill=self.get_color(pr_distr[y * self.num_cols + x]))

    # Given a probability, calculates the corresponding color within the gradiant.
    # A probability of 1 gives max_val, while a probability of 0 gives min_val.
    # Any other probabilty gives an interpolated value.
    # Returns a string in "#0x" format.
    def get_color(self, pr):
        max_val = (255, 0, 0) #red
        min_val = (203, 195, 227) #light purple

        if pr < 1.0 / self.num_unblocked:
            return "#FFFFFF"

        r_delta = max_val[0] - min_val[0]
        g_delta = max_val[1] - min_val[1]
        b_delta = max_val[2] - min_val[2]
        color = (min_val[0] + round(pr * r_delta),
                 min_val[1] + round(pr * g_delta),
                 min_val[2] + round(pr * b_delta))
        return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

    def scale(self, x):
        return x * self.scalar

    def run(self):
        self.root.mainloop()
