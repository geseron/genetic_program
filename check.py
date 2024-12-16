import numpy as np
from individ import gp_individ
import pandas as pd
from population import gp_population
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score




data = pd.read_csv('TwoGaussD2.csv')

true_class = np.array(data['Class'])
y_train = np.array( data['Y'] )
X_train = np.array( data['X'] )



model = gp_population(X_train, y_train, true_class, 1, generations_count=20, mutation_probability=0.5, selection_type='proportional',depth=5, tournament_size=5)
model.fit()
model.best_individ_of_generation[0][0].draw_tree()

rule = model.final_rule


data['predicted_class'] = model.final_labels
data['predicted_rule'] = rule

data = data.sort_values(by='X', ascending=True)

plt.scatter(data.loc[data['predicted_class'] == 0, 'X'],data.loc[data['predicted_class'] == 0, 'Y'], color='green')
plt.scatter(data.loc[data['predicted_class'] == 1, 'X'],data.loc[data['predicted_class'] == 1, 'Y'], color='magenta')
# plt.plot(data['X'], data['true_rule'], color='blue', label='Истинное правило')
plt.plot(data['X'], data['predicted_rule'],'--', color='red', label='Предсказанное правило')
plt.legend()
plt.xlim(0,10)
plt.ylim(0,10)
plt.show()

plt.plot(model.history[:,0], label='Лучший')
plt.plot(model.history[:,1], label='Худший')
plt.legend()
plt.show()


print(f"Достигнутая точность: {accuracy_score(model.final_labels, true_class)}")
print('Done!')