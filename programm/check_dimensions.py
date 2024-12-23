import numpy as np
from individ import gp_individ
import pandas as pd
from population import gp_population
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score




data = pd.read_csv('RandomUniformD5.csv')
true_class = np.array(data['Class'])
y_train = np.array( data['Y'] )
size = len(y_train)
train = []
for column in data.columns[:-3]:
    train.append( np.reshape( data[column].to_numpy() , (size,1) ) )
X_train = np.array(train[0])
for i in range(1, len(data.columns)-3 ):
    X_train = np.append( X_train, train[1], axis=1 )

model = gp_population(X_train, y_train, true_class, 4, generations_count=20, mutation_probability=0.4, selection_type='tournament',depth=7)
model.fit()
model.best_individ_of_generation[0][0].draw_tree()

rule = model.final_rule
if len(rule) == 1:
    rule = np.ones(len(X_train)) * rule

data['predicted_class'] = model.final_labels
data['predicted_rule'] = rule



plt.plot(model.history[:,0], label='Лучший')
plt.plot(model.history[:,1], label='Худший')
plt.legend()
plt.show()


print(f"Достигнутая точность: {accuracy_score(model.final_labels, true_class)}")
print('Done!')