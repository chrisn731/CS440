from mdp import MDP

def value_iteration(mdp, thresh):
    # Initalize U'
    curr = [0 for i in range(len(mdp.get_states()))]
    prev = []

    iterations = 0
    while True:
        # U = U'
        prev = curr.copy()
        curr_thresh = 0
        for node in mdp.get_states():
            # U'[s] = r(s) + γ * max(SUM[P(s'|s, a) * U[s']])
            curr[node - 1] = mdp.reward(node) + (mdp.discount() * get_max_Q(mdp, node, prev))
            curr_thresh = max(curr_thresh, abs(curr[node - 1] - prev[node - 1]))
        # if δ <= (ε(1 - γ))/γ
        if curr_thresh <= (thresh * (1 - mdp.discount())) / mdp.discount():
            break
        iterations += 1
        print(str(iterations) + ": " + str(prev) + "\n\t" + str(optimal_policy(mdp, prev)))
    print("Iterations: " + str(iterations))
    # Return U
    return prev

# Helper function for max(SUM[P(s'|s, a) * U[s']])
def get_max_Q(mdp, node, prev):
    qmax = -float("inf")
    for action in mdp.get_actions(node):
        q = Q_val(mdp, node, action, prev)
        qmax = max(q, qmax)
    return qmax

# Helper function to compute SUM[P(s'|s, a) * U[s']]
def Q_val(mdp, node, action, prev):
    return sum(mdp.transition(node, action, i + 1) * prev[i] for i in range(len(mdp.get_states())))

def optimal_policy(mdp, util):
    # Initalize π*
    policy = [0 for i in range(len(mdp.get_states()))]

    for node in mdp.get_states():
        argmax = -float("inf")
        max_action = -1
        for action in mdp.get_actions(node):
            # SUM[P(s'|s, a) * U[s']
            q = Q_val(mdp, node, action, util)
            # argmax of SUM
            if q > argmax:
                argmax = q
                max_action = action
        # π*(s) = argmax(SUM)
        policy[node - 1] = max_action
    # Return π*
    return policy

if __name__ == '__main__':
    mdp = MDP()
    utilities = value_iteration(mdp, .00001)
    policy = optimal_policy(mdp, utilities)
    print("Optimal utilities final result: " + str(utilities))
    print("Optimal policy final result: " + str(policy))
