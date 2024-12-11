import numpy as np
from sklearn.metrics import accuracy_score

def fitness(rule, y_train, true_class):
    predicted_class = np.zeros(len(rule))
    predicted_class[y_train > rule] = 1
    fit = accuracy_score(true_class, predicted_class)
    return fit