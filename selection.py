import numpy as np

def tournament_selection(population, pop_indexes,  tournament_size):
    # выбираем случайных индивидов
    tournament_players = np.random.choice(pop_indexes, tournament_size, replace=False)
    # сортируем по возрастанию индексы
    tournament_players.sort()
    # Выбираем ТОП 2 победителя
    winners = population[tournament_players][np.argsort(population[tournament_players][:,1])][-2:][:,0]
    return winners

def proportional_selection(population):
    total_fitness = sum(population[:,1])
    selection_probs = np.float64(population[:,1] / total_fitness)
    winners = np.random.choice(population[:,0], size = 2, replace=False, p=selection_probs)
    return winners