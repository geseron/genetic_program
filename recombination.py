import numpy as np
import copy
from fitness import *
import sys



def gp_recombination(winners, X_train, y_train, class_labels):
    bad_rookie = True
    attempts = 0
    while bad_rookie and attempts < 10:
        new_individ = copy.deepcopy(winners[0])
        #friend = copy.deepcopy(winners[1])
        nodes_ind = new_individ.nodes
        nodes_fri = winners[1].nodes

        individ_node = np.random.randint(1,len(nodes_ind))
        friend_node = np.random.randint(1,len(nodes_fri))

        side = nodes_ind[individ_node].parent[1]
        nodes_ind[individ_node].parent[0].node_sons[side] = nodes_fri[friend_node]
        new_individ.variable_check()
        rule = new_individ.predict(X_train)
        if check_adequacy(rule): # true если есть None, inf
            # del new_individ
            # del nodes_fri
            # del nodes_ind
            attempts+=1
            continue
        fitness_value = fitness(rule, y_train, class_labels, new_individ.depth, new_individ.depth_limit)
        bad_rookie = False
        #print(f'Ссылок на друга: {sys.getrefcount(winners[1])} Попыток: {attempts}')
        #print(f'Ссылок на узлы друга: {sys.getrefcount(nodes_fri)} Попыток: {attempts}')

        #print(f'Ссылок на new_individ: {sys.getrefcount(new_individ)} Попыток: {attempts}')
        #print(f'Ссылок на узлы new_individ: {sys.getrefcount(nodes_fri)} Попыток: {attempts}')
        #del friend
        new_individ.head.define_parent(None)
        new_individ.depth = new_individ.head.get_depth()
        new_individ.nodes = []
        new_individ.head.get_self(new_individ.nodes)
        new_individ.nodes_count = len(new_individ.nodes)
    return [new_individ,fitness_value]