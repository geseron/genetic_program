import numpy as np
from sklearn.metrics import accuracy_score

def fitness(rule, y_train, true_class):
    predicted_class = np.zeros(len(y_train))
    mask = y_train > rule
    # if len(mask) == 0:
    #     return 0
    predicted_class[mask] = 1
    fit = accuracy_score(true_class, predicted_class)
    return fit