import sys
from mdp import MDP
import numpy as np

def value_iteration(mdp, thresh):
    curr = [0 for i in range(len(mdp.get_states()))]
    prev = []

    iterations = 0
    while True:
        prev = curr.copy()
        curr_thresh = 0
        for node in mdp.get_states():
            curr[node - 1] = mdp.reward(node) + (mdp.discount() * get_max_Q(mdp, node, prev))
            curr_thresh = max(curr_thresh, abs(curr[node - 1] - prev[node - 1]))
        if curr_thresh <= (thresh * (1 - mdp.discount())) / mdp.discount():
            break
        iterations += 1
        print(str(iterations) + ": " + str(prev) + "\n\t" + str(optimal_policy(mdp, prev)))
    print("Iterations: " + str(iterations))
    return prev

def get_max_Q(mdp, node, prev):
    qmax = -float("inf")
    for action in mdp.get_actions(node):
        q = Q_val(mdp, node, action, prev)
        qmax = max(q, qmax)
    return qmax

def Q_val(mdp, node, action, prev):
    return sum(mdp.transition(node, action, i + 1) * prev[i] for i in range(len(mdp.get_states())))

def optimal_policy(mdp, util):
    policy = [0 for i in range(len(mdp.get_states()))]
    for node in mdp.get_states():
        argmax = -float("inf")
        max_action = -1
        for action in mdp.get_actions(node):
            q = Q_val(mdp, node, action, util)
            if q > argmax:
                argmax = q
                max_action = action
        policy[node - 1] = max_action
    return policy

if __name__ == '__main__':
    mdp = MDP()
    utilities = value_iteration(mdp, .00001)
    policy = optimal_policy(mdp, utilities)
    print(utilities)
    print(policy)
