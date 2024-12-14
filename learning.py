import numpy as np
from fitness import *
from recombination import *
import gc

def generate_new_population(main_obj):
    # main_obj - ссылка на объект gp_population
    new_population = []
    while len(new_population) < main_obj.pop_size:
        winners = main_obj.selection(main_obj)
        rookie = gp_recombination(winners, main_obj.X_train, main_obj.y_train, main_obj.class_labels)
        attempts = 0
        bad_mutation = True
        while bad_mutation and attempts < 10:
            temp_individ = copy.deepcopy(rookie[0])
            temp_individ.mutation()
            rule = temp_individ.predict(main_obj.X_train)
            if check_adequacy(rule): # true если есть None, inf
                #print(f'Ссылок на temp_individ: {sys.getrefcount(temp_individ)} Попыток: {attempts}')
                # while sys.getrefcount(temp_individ) != 2:
                #     del temp_individ
                attempts += 1
                continue
            fitness_value = fitness(rule, main_obj.y_train, main_obj.class_labels, temp_individ.depth, main_obj.depth_limit)
            new_population.append( [temp_individ, fitness_value] )
            bad_mutation = False
            

        if bad_mutation: new_population.append( rookie )
        gc.collect()
    new_population = np.array(new_population)
    return new_population