from individ import gp_individ
import numpy as np
from fitness import *
from selection import *
from recombination import *
from learning import *
from tqdm import tqdm
import gc

class gp_population():
    selection_type = { 'tournament': tournament_selection,
                        'proportional': proportional_selection
                     }
    def __init__(self, X_train, y_train, true_class_labels, dimension_count, selection_type='tournament', pop_size = 100, generations_count=20, mutation_probability = 0.3, depth = 5, tournament_size = 10):
        np.seterr(over='ignore', divide='ignore', invalid='ignore')
        self.X_train = X_train
        self.y_train = y_train
        self.data_size = len(X_train)
        self.class_labels = true_class_labels
        self.pop_size = pop_size
        self.generations_count = generations_count
        self.dimensions = dimension_count
        self.mutation_probability = mutation_probability
        self.depth_limit = depth
        self.tournament_size = tournament_size
        self.selection = self.selection_type[selection_type]
        self.pop_indexes = list(range(pop_size))
        self.history = [] # [лучшее решение в поколении, худшее решение в поколении]
        self.final_labels = []
        self.final_rule = []

        self.best_individ_of_generation = []

        self.population = self.generate_population()
        



    def generate_population(self):
        population = []

        while len(population) < self.pop_size:
            # print(f"{len(population)}")
            temp_individ = gp_individ(self.dimensions, self.data_size, self.mutation_probability, depth=self.depth_limit)
            rule = temp_individ.predict(self.X_train)
            if check_adequacy(rule): # true если есть None, inf
                # del temp_individ
                continue
            fitness_value = fitness(rule, self.y_train, self.class_labels, temp_individ.depth, self.depth_limit)
            population.append( [temp_individ, fitness_value] )
        population = np.array(population)
        self.best_individ_of_generation = np.reshape(population[ np.argmax(population[:,1]) ], (1,2))
        return population
    
    def fit(self):
        for i in tqdm(range(self.generations_count)) :
        # for i in range(self.generations_count) :
            self.population = generate_new_population(self)
            gc.collect()
            self.population = np.append( self.population, self.best_individ_of_generation, axis=0 )
            best_fitness = self.population[:,1][np.argmax(self.population[:,1])]
            worts_fintness = self.population[:,1][np.argmin(self.population[:,1])]
            self.history.append([best_fitness, worts_fintness])

            temp_best = copy.deepcopy(self.population[ np.argmax(self.population[:,1]) ][0])
            temp_best_rule = temp_best.predict(self.X_train)
            if check_adequacy(temp_best_rule):
                continue
            else:
                fitness_value = fitness(temp_best_rule, self.y_train, self.class_labels, temp_best.depth, self.depth_limit)
                self.best_individ_of_generation = np.reshape([temp_best, fitness_value], (1,2))
        
        print(f"Значение фитнесса: {self.best_individ_of_generation[0][1]}")
        self.final_rule = self.best_individ_of_generation[0][0].predict(self.X_train)
        self.final_labels = np.zeros(len(self.y_train))
        self.final_labels[self.y_train > self.final_rule] = 1
        self.history = np.array(self.history)


        
            
            
            
            
            


