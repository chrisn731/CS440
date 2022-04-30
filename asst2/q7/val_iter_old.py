import sys
from mdp import MDP

def value_iteration(mdp, thresh):
    curr = [0 for i in range(len(mdp.get_states()))]
    prev = []

    i = 0
    while True:
        prev = curr.copy()
        curr_thresh = 0
        for node in mdp.get_states():
            curr[node - 1] = get_max_Q(mdp, node, prev)
            if abs(curr[node - 1] - prev[node - 1]) > curr_thresh:
                curr_thresh = abs(curr[node - 1] - prev[node - 1])
        if curr_thresh <= (thresh * (1 - mdp.discount())) / mdp.discount():
            break
        i += 1
    print(i)
    return prev

def get_max_Q(mdp, node, prev):
    qmax = -float("inf")
    for action in mdp.get_actions(node):
        q = Q_val(mdp, node, action, prev)
        qmax = max(q, qmax)
    return qmax

def Q_val(mdp, node, action, prev):
    summation = 0
    for i in range(len(mdp.get_states())):
        summation += (mdp.transition(node, action, i + 1) *
            (mdp.reward(node, action, i + 1) + mdp.discount() * prev[i]))
    return summation

if __name__ == '__main__':
    utilities = value_iteration(MDP(), .001)
    print(utilities)
