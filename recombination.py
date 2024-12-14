import numpy as np
import copy
from fitness import *

def gp_recombination(winners, X_train, y_train, class_labels):
    bad_rookie = True
    attempts = 0
    while bad_rookie or attempts < 10:
        new_individ = copy.deepcopy(winners[0])
        friend = copy.deepcopy(winners[1])
        nodes_ind = new_individ.nodes
        nodes_fri = friend.nodes

        individ_node = np.random.randint(1,len(nodes_ind))
        friend_node = np.random.randint(1,len(nodes_fri))

        side = nodes_ind[individ_node].parent[1]
        nodes_ind[individ_node].parent[0].node_sons[side] = nodes_fri[friend_node]
        rule = new_individ.predict(X_train)
        if check_adequacy(rule): # true если есть None, inf
            attempts+=1
            continue
        fitness_value = fitness(rule, y_train, class_labels, new_individ.depth, new_individ.depth_limit)
        bad_rookie = False
    return [new_individ,fitness_value]