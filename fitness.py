import numpy as np
from sklearn.metrics import accuracy_score

def fitness(rule, y_train, true_class, depth, depth_limit):
    predicted_class = np.zeros(len(y_train))
    predicted_class[y_train > rule] = 1
    penalty = 0
    if depth>depth_limit:
        penalty = 0.05 * ( depth - depth_limit )
    fit = accuracy_score(true_class, predicted_class) - penalty
    return fit

def check_adequacy(rule):
    # true если есть None, inf
    
    return np.any(rule == None) or np.any(rule == np.inf) or np.any(rule == (-np.inf))