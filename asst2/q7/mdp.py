class Node:
    def __init__(self, reward, actions):
        self.reward = reward
        self.actions = actions

class MDP:
    def __init__(self):
        self.states = self.init_states()
        self.t_model = self.init_t_model()
        self.DISCOUNT = .9

    def init_states(self):
        s = dict()
        s[1] = Node(0, [1, 2])
        s[2] = Node(0, [2, 3])
        s[3] = Node(1, [3, 4])
        s[4] = Node(0, [1, 4])
        return s

    def init_t_model(self):
        t = dict()
        t[(1, 1, 1)] = .2
        t[(1, 1, 2)] = .8
        t[(1, 2, 1)] = .2
        t[(1, 2, 4)] = .8
        t[(2, 2, 2)] = .2
        t[(2, 2, 3)] = .8
        t[(2, 3, 2)] = .2
        t[(2, 3, 1)] = .8
        t[(3, 4, 2)] = 1
        t[(3, 3, 4)] = 1
        t[(4, 1, 4)] = .1
        t[(4, 1, 3)] = .9
        t[(4, 4, 4)] = .2
        t[(4, 4, 1)] = .8
        return t

    def get_states(self):
        return self.states

    def get_actions(self, n):
        return self.states[n].actions

    def transition(self, s1, a, s2):
        return self.t_model.get((s1, a, s2), 0)

    def reward(self, s):
        return self.states[s].reward

    def discount(self):
        return self.DISCOUNT
