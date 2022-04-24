import ctypes

class FilterData:
    NUM_ROWS = 100
    NUM_COLS = 50

    def __init__(self, world_file = "", actions = "", sensors = "", library_name = "./filter.so"):
        self.lib = ctypes.cdll.LoadLibrary(library_name)
        if len(world_file) != 0:
            self.load_world(world_file)
        if len(actions) != 0 and len(sensors) != 0:
            self.__calculate_prob_distrs(actions, sensors)

    def get_next_prob_distr(self):
        if self.num_data_sets == 0:
            return None
        self.current_distr_idx += 1
        if self.current_distr_idx >= self.num_data_sets:
            self.current_distr_idx = 0
        return self.data[self.current_distr_idx]

    def get_prev_prob_distr(self):
        if self.num_data_sets == 0:
            return None
        self.current_distr_idx -= 1
        if self.current_distr_idx < 0:
            self.current_distr_idx = self.num_data_sets - 1
        return self.data[self.current_distr_idx]

    def get_curr_prob_distr(self):
        return self.data[self.current_distr_idx]

    # Use with caution
    def get_prob_distr_at(self, idx):
        return self.data[idx] if idx < self.num_data_sets and idx >= 0 else None

    def load_world(self, world_file):
        file = ctypes.c_char_p(bytes(world_file, encoding='utf-8'))
        self.lib.load_world.restype = ctypes.c_uint
        size = self.lib.load_world(file)
        self.__reset_data_sets()
        self.lib.filter_step.restype = ctypes.POINTER(ctypes.c_double * size)

    def set_action_sensor_data(self, actions, sensors):
        # Clear out previous data sets
        self.__reset_data_sets()
        self.__calculate_prob_distrs(actions, sensors)

    def __calculate_prob_distrs(self, actions, sensor_readings):
        if len(actions) != len(sensor_readings):
            print("Actions and sensor readings should be the same length!!!")
            return

        prev_distr = None
        for i in range(len(actions)):
            sensor = ctypes.c_char(bytes(sensor_readings[i], encoding='utf-8'))
            action = ctypes.c_char(bytes(actions[i], encoding='utf-8'))
            ret = self.lib.filter_step(sensor, action, prev_distr)
            prev_distr = ret
            self.data.append([elm for elm in ret.contents])
        self.num_data_sets = len(self.data)

    def __reset_data_sets(self):
        self.data = []
        self.current_distr_idx = 0
        self.num_data_sets = 0
