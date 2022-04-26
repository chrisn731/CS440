import matplotlib.pyplot as plt
import sys
import os
from filter_data import FilterData

NUM_ACTIONS = 100
NUM_EXPERIMENTS = 100
class AgentCellPlot:
    def __init__(self, world_dir, action_dir):
        self.exp_avg = []
        self.map_world_to_actions(world_dir, action_dir)
        for key in self.world_action_map:
            world_file = os.path.join(world_dir, key)
            self.fd = FilterData(world_file)
            for f in self.world_action_map[key]:
                action_file = os.path.join(action_dir, f)
                self.read_action(action_file)
                self.fd.set_action_sensor_data(self.action_seq, self.sensor_seq)
                self.fill_data()

    def fill_data(self):
        agent_prob_distr = []
        for i in range(NUM_ACTIONS):
            prob_distr = self.fd.get_prob_distr_at(i)
            agent_location = self.locations[i + 1]
            agent_prob = prob_distr[(agent_location[0] * self.num_cols + agent_location[1])]
            agent_prob_distr.append(agent_prob)
        self.exp_avg.append(agent_prob_distr)


    def calc_avg(self):
        self.prob_distr = []
        for i in range(NUM_ACTIONS):
            exp_sum = 0
            for j in range(NUM_EXPERIMENTS):
                exp_sum += self.exp_avg[j][i]
            self.prob_distr.append(exp_sum / NUM_EXPERIMENTS)

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
        return self.avg_err

    def show(self):
        agent_prob_distr = []
        for i in range(NUM_ACTIONS):
            prob_distr = self.fd.get_prob_distr_at(i)
            agent_location = self.locations[i + 1]
            agent_prob = prob_distr[(agent_location[0] * self.num_cols + agent_location[1])]
            agent_prob_distr.append(agent_prob)

        plt.plot([i for i in range(NUM_ACTIONS)], agent_prob_distr)
        plt.xlabel('Action Number')
        plt.ylabel('Probability of the Agent\'s Cell')
        plt.title('Average Probability of the Agent\'s Cell over 100 Experiments')
        plt.show()

def main():
    if len(sys.argv) == 3:
        AgentCellPlot(sys.argv[1], sys.argv[2]).show()

if __name__ == "__main__":
    main()
