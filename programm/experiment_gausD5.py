import numpy as np
from individ import gp_individ
import pandas as pd
from population import gp_population
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import sympy




data = pd.read_csv('TwoGaussD5.csv')
true_class = np.array(data['Class'])
y_train = np.array( data['Y'] )
size = len(y_train)
train = []
for column in data.columns[:-3]:
    train.append( np.reshape( data[column].to_numpy() , (size,1) ) )
X_train = np.array(train[0])
for i in range(1, len(data.columns)-2 ):
    X_train = np.append( X_train, train[1], axis=1 )

selections = ['tournament','proportional']


for selection in selections:
    print(selection)
    statistics = {
    'loss': [],
    'accuracy': [],
    'f1': [],
    'rule': []
    }
    for iteration in range(40):
        print(f"{iteration=}")
        model = gp_population(X_train, y_train, true_class, 4, generations_count=20, mutation_probability=0.5, selection_type=selection, depth=5)
        model.fit()
        model.best_individ_of_generation[0][0].draw_tree(iteration, selection)

        rule = model.final_rule

        data['predicted_class'] = model.final_labels
        data['predicted_rule'] = rule


        plt.plot(model.history[:,0], label='Лучший')
        plt.plot(model.history[:,1], label='Худший')
        plt.legend()
        plt.savefig(f"exp\\D5\\gaus\\figs\\history\\{selection}{iteration}.png")
        plt.close()

        expr = model.best_individ_of_generation[0][0].head.get_formula()
        expr = sympy.sympify(expr)
        statistics['loss'].append( model.best_individ_of_generation[0][1] )
        statistics['accuracy'].append( accuracy_score(model.final_labels, true_class) )
        statistics['f1'].append( f1_score(model.final_labels, true_class) )
        statistics['rule'].append( sympy.latex(expr) )

    df = pd.DataFrame(statistics)
    df.to_csv(f"exp\\D5\\gaus\\{selection}.csv")
print('Done!')