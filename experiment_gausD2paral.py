import numpy as np
from individ import gp_individ
import pandas as pd
from population import gp_population
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import sympy
from joblib import Parallel, delayed

data = pd.read_csv('TwoGaussD2.csv')
data = data.sort_values(by='X', ascending=True)
true_class = np.array(data['Class'])
y_train = np.array(data['Y'])
X_train = np.array(data['X'])

# selections = ['tournament', 'proportional']
selections = ['proportional']

def process_iteration(iteration, selection, data):
    print(f"{iteration=}")
    true_class = np.array(data['Class'])
    y_train = np.array(data['Y'])
    X_train = np.array(data['X'])
    model = gp_population(X_train, y_train, true_class, 1, generations_count=50, mutation_probability=0.4, selection_type=selection, depth=4, tournament_size=10)
    model.fit()
    model.best_individ_of_generation[0][0].draw_tree(iteration, selection)

    rule = model.final_rule
    if len(rule) == 1:
        rule = np.ones(len(X_train)) * rule

    data['predicted_class'] = model.final_labels
    data['predicted_rule'] = rule
    data = data.sort_values(by='X', ascending=True)

    plt.scatter(data.loc[data['predicted_class'] == 0, 'X'], data.loc[data['predicted_class'] == 0, 'Y'], color='green')
    plt.scatter(data.loc[data['predicted_class'] == 1, 'X'], data.loc[data['predicted_class'] == 1, 'Y'], color='magenta')
    plt.plot(data['X'], data['predicted_rule'], '--', color='red', label='Предсказанное правило')
    plt.legend()
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.savefig(f"exp\D2\gausD2\\figs\\rule\\{selection}{iteration}.png")
    plt.close()

    plt.plot(model.history[:, 0], label='Лучший')
    plt.plot(model.history[:, 1], label='Худший')
    plt.legend()
    plt.savefig(f"exp\D2\gausD2\\figs\\history\\{selection}{iteration}.png")
    plt.close()

    expr = model.best_individ_of_generation[0][0].head.get_formula()
    expr = sympy.sympify(expr)
    return {
        'loss': model.best_individ_of_generation[0][1],
        'accuracy': accuracy_score(model.final_labels, true_class),
        'f1': f1_score(model.final_labels, true_class),
        'rule': sympy.latex(expr)
    }

for selection in selections:
    print(selection)
    statistics = {
        'loss': [],
        'accuracy': [],
        'f1': [],
        'rule': []
    }

    results = Parallel(n_jobs=-1)(delayed(process_iteration)(iteration, selection, data) for iteration in range(40))

    for result in results:
        statistics['loss'].append(result['loss'])
        statistics['accuracy'].append(result['accuracy'])
        statistics['f1'].append(result['f1'])
        statistics['rule'].append(result['rule'])

    df = pd.DataFrame(statistics)
    df.to_csv(f"exp\D2\gausD2\\{selection}.csv")

print('Done!')
