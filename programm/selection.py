import numpy as np

def tournament_selection(main_obj):
    # main_obj - ссылка на объект gp_population
    # выбираем случайных индивидов
    tournament_players = np.random.choice(main_obj.pop_indexes, main_obj.tournament_size, replace=False)
    # сортируем по возрастанию индексы
    tournament_players.sort()
    # Выбираем ТОП 2 победителя
    winners = main_obj.population[tournament_players][np.argsort(main_obj.population[tournament_players][:,1])][-2:][:,0]
    return winners

def proportional_selection(main_obj):
    total_fitness = sum(main_obj.population[:,1])
    selection_probs = np.float64(main_obj.population[:,1] / total_fitness)
    winners = np.random.choice(main_obj.population[:,0], size = 2, replace=False, p=selection_probs)
    return winners