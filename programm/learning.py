import numpy as np
from fitness import *
from recombination import *


def generate_new_population(main_obj):
    # main_obj - ссылка на объект gp_population
    new_population = []
    while len(new_population) < main_obj.pop_size:
        attempts = 0
        bad_winners = True
        while bad_winners and attempts < 10:    
            winners = main_obj.selection(main_obj)
            rookie = gp_recombination(winners, main_obj.X_train, main_obj.y_train, main_obj.class_labels)
            if rookie is None:
                attempts += 1
                continue
            else:
                bad_winners = False
        if bad_winners: 
            continue
        else: 
            attempts = 0
            bad_mutation = True
            while bad_mutation and attempts < 10:
                temp_individ = copy.deepcopy(rookie[0])
                temp_individ.mutation()
                if np.random.uniform(0,1) < 0.1:    
                    temp_individ.variable_check()
                rule = temp_individ.predict(main_obj.X_train)
                if check_adequacy(rule): # true если есть None, inf
                    attempts += 1
                    continue
                else:
                    fitness_value = fitness(rule, main_obj.y_train, main_obj.class_labels, temp_individ.depth, main_obj.depth_limit)
                    new_population.append( [temp_individ, fitness_value] )
                    bad_mutation = False
            if bad_mutation: 
                new_population.append( rookie )
    new_population = np.array(new_population)
    return new_population