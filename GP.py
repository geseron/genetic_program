import numpy as np

class Genetic_Node():
    IsOperator = None
    IsTerminal = None
    ref_in_parent = [0]


class Function(Genetic_Node):
    left_node = None
    right_node = None
    def calculate(self, x):
        return 0

class unary_function(Function):
    def __init__(self, left_node):
        self.IsOperator = 'unary_function'
        self.left_node = left_node
    def calculate(self, x):
        return 0
    def get_self(self, nodes):
        nodes.append(self)
        self.left_node.get_self(nodes)
    def define_parent(self, reference):
        self.ref_in_parent[0] = reference
        self.left_node.define_parent(self.left_node)
    def change_child(self,new_child):
        self.ref_in_parent = new_child

class binary_function(Function):
    def __init__(self, left_node, right_node):
        self.IsOperator = "binary_function"
        self.left_node = left_node
        self.right_node = right_node
    def calculate(self, x):
        return 0
    def get_self(self, nodes):
        nodes.append(self)
        self.left_node.get_self(nodes)
        self.right_node.get_self(nodes)
    def define_parent(self, reference):
        self.ref_in_parent[0] = reference
        self.left_node.define_parent(self.left_node)
        self.right_node.define_parent(self.right_node)

class GP_sin(unary_function):
    def calculate(self, x):
        return np.sin(self.left_node.calculate(x))
    
class GP_abs(unary_function):
    def calculate(self, x):
        return np.abs(self.left_node.calculate(x))
    
class GP_exp(unary_function):
    def calculate(self, x):
        return np.exp(self.left_node.calculate(x))

class GP_sum(binary_function):
    def calculate(self, x):
        return self.left_node.calculate(x) + self.right_node.calculate(x)

class Terminal(Genetic_Node):
    def calculate(self, x):
        return 0
    def get_self(self, nodes):
        nodes.append(self)
    def define_parent(self, reference):
        self.ref_in_parent[0] = reference

    
class Variable(Terminal):
    var_index = None
    def __init__(self, index):
        self.var_index = index
        self.IsTerminal = f'variable_{index}'
    def calculate(self, x):
        return x[self.var_index]
    
class Value(Terminal):
    value = None
    def __init__(self, value):
        self.value = value
        self.IsTerminal = 'vaule'
    def calculate(self, x):
        return self.value   




# class Individ:
#     def __init__(self, n, q, f, cr, uplimit, lowlimit, g, fofma):
#         self.n = n                      # количество измерений в целевой функции
#         self.Q = q
#         self.F = f
#         self.Cr = cr
#         self.uplimit = uplimit
#         self.lowlimit = lowlimit
#         self.Sigma = 0.000001           #  точность
#         self.fofma = fofma              #  целевая функция
#         self.result = {"Point": None,
#                        "Minimum": None,
#                        "Time_to_minimum": None,
#                        "Minimum_of_Demand": None,
#                        "Time_of_Demand": None,
#                        "Point_of_Demand": None
#                        }
#         self.progressOfFitness = list() # построение графика
#         self.CountOfGeneration = g      # количество вычислений целевой функции