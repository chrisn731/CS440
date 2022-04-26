import ctypes
import math

class FilterData:
    def __init__(self, world_file = "", actions = "", sensors = "", library_name = "./filter.so"):
        self.lib = ctypes.cdll.LoadLibrary(library_name)
        if len(world_file) != 0:
            self.load_world(world_file)
        if len(actions) != 0 and len(sensors) != 0:
            self.__calculate_prob_distrs(actions, sensors)
        self.__reset_data_sets()

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

    def calculate_error(self, num_cols, num_rows, true_locations, iters_to_skip):
        self.avg_err = []
        err_val = []
        if self.num_data_sets == 0:
            return self.avg_err

        for i in range(len(true_locations)):
            if i < iters_to_skip:
                err_val.append(0.0)
                self.avg_err.append(0.0)
                continue
            max_val = 0.0
            max_idx = 0
            for idx in range(len(self.data[i])):
                if self.data[i][idx] > max_val:
                    max_val = self.data[i][idx]
                    max_idx = idx
            row = max_idx // num_cols
            col = max_idx % num_cols
            true_coord = true_locations[i]
            distance = math.sqrt((true_coord[0] - row)**2 + (true_coord[1] - col)**2)
            err_val.append(distance)
            self.avg_err.append(math.fsum(err_val) / (i - iters_to_skip + 1))
        return self.avg_err

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
        self.current_distr_idx = -1
        self.num_data_sets = 0
