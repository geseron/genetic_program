import numpy as np
import copy
from fitness import *
import sys



def gp_recombination(winners, X_train, y_train, class_labels):
    bad_rookie = True
    attempts = 0
    rule = 0
    while bad_rookie and attempts < 10:
        new_individ = copy.deepcopy(winners[0])
        nodes_ind = new_individ.nodes
        nodes_fri = winners[1].nodes

        individ_node = np.random.randint(1,len(nodes_ind))
        friend_node = np.random.randint(1,len(nodes_fri))

        side = nodes_ind[individ_node].parent[1]
        nodes_ind[individ_node].parent[0].node_sons[side] = nodes_fri[friend_node]
        new_individ.variable_check()
        rule = new_individ.predict(X_train)
        if check_adequacy(rule): # true если есть None, inf
            rule = None
            attempts+=1
            continue
        else:
            fitness_value = fitness(rule, y_train, class_labels, new_individ.depth, new_individ.depth_limit)
            bad_rookie = False
            new_individ.head.define_parent(None)
            new_individ.depth = new_individ.head.get_depth()
            new_individ.nodes = []
            new_individ.head.get_self(new_individ.nodes)
            new_individ.nodes_count = len(new_individ.nodes)
    if bad_rookie:
        return None
    else:
        return [new_individ, fitness_value]