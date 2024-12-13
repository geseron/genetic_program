from individ import gp_individ
import numpy as np
from fitness import *
from selection import *

class gp_population():
    selection_type = { 'tournament': tournament_selection,
                        'proportional': proportional_selection
                     }
    def __init__(self, X_train, y_train, true_class_labels, dimension_count, selection_type='tournament', pop_size = 5, generations_count=20, mutation_probability = 0.3, depth = 4):
        self.X_train = X_train
        self.y_train = y_train
        self.class_labels = true_class_labels
        self.pop_size = pop_size
        self.generations_count = generations_count
        self.dimensions = dimension_count
        self.mutation_probability = mutation_probability
        self.depth_limit = depth
        self.selection = self.selection_type[selection_type]
        self.population = self.generate_population()



    def generate_population(self):
        population = []
        while len(population) < self.pop_size:
            temp_individ = gp_individ(self.dimensions, self.mutation_probability, depth=self.depth_limit)
            rule = temp_individ.predict(self.X_train)
            if check_adequacy(rule): # true если есть None, inf
                continue
            fitness_value = fitness(rule, self.y_train, self.class_labels, temp_individ.depth, self.depth_limit)
            population.append( [temp_individ, fitness_value] )
        population = np.array(population)
        return population
            
            


