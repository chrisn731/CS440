import matplotlib.pyplot as plt
import sys
import os
from filter_data import FilterData

NUM_ACTIONS = 100
NUM_EXPERIMENTS = 100
class ErrorPlot:
    def __init__(self, world_dir, action_dir):
        self.error_probs = []
        self.exp_avg = []
        self.map_world_to_actions(world_dir, action_dir)
        for key in self.world_action_map:
            world_file = os.path.join(world_dir, key)
            self.fd = FilterData(world_file)
            for f in self.world_action_map[key]:
                action_file = os.path.join(action_dir, f)
                self.read_action(action_file)
                self.fd.set_action_sensor_data(self.action_seq, self.sensor_seq)
                self.avg_err = self.fd.calculate_error(self.num_cols, self.num_rows, self.locations[1:], 5)
                self.exp_avg.append(self.avg_err)
        self.calc_avg()

    def calc_avg(self):
        for i in range(NUM_ACTIONS):
            exp_sum = 0
            for j in range(NUM_EXPERIMENTS):
                exp_sum += self.exp_avg[j][i]
            self.error_probs.append(exp_sum / NUM_EXPERIMENTS)

    def map_world_to_actions(self, world_dir, action_dir):
        self.world_action_map = {}
        for world_file in os.listdir(world_dir):
            self.world_action_map[world_file] = []
            for action_file in os.listdir(action_dir):
                if world_file[:world_file.find('.')] in action_file:
                    self.world_action_map[world_file].append(action_file)
            self.world_action_map[world_file].sort()
        return self.world_action_map

    def read_action(self, action_file):
        self.num_rows = 100
        self.num_cols = 50
        with open(action_file, 'r') as f:
            locations = [next(f) for x in range(NUM_ACTIONS + 1)]
            self.action_seq = f.readline().strip()
            self.sensor_seq = f.readline().strip()

        self.locations = []
        for location in locations:
            coords = location.split(', ')
            self.locations.append((int(coords[0]), int(coords[1])))

    def get_probabilities(self):
        return self.error_probs

    def show(self):
        plt.plot([i for i in range(NUM_EXPERIMENTS)], self.get_probabilities())
        plt.xlabel('Action Number')
        plt.ylabel('Average Cell Distance Error')
        plt.title('Average # of Cells Away from Truth over 100 Experiments')
        plt.show()

def main():
    if len(sys.argv) == 3:
        ErrorPlot(sys.argv[1], sys.argv[2]).show()

if __name__ == "__main__":
    main()
