import numpy as np

class Genetic_Node():
    IsOperator = None
    IsTerminal = None
    parent = None
    dimension_count = None


class Function(Genetic_Node):
    def calculate(self, x):
        return 0

class unary_function(Function):
    def __init__(self):
        self.IsOperator = "unary_function"
        self.node_sons = {
            'left': None,
            'right':None
        }
    def calculate(self, x):
        return 0
    def get_self(self, nodes):
        nodes.append(self)
        self.node_sons['left'].get_self(nodes)
    def define_parent(self, reference):
        self.parent = reference
        self.node_sons['left'].define_parent([self,'left'])
    # def change_child(self,new_child):
    #     self.ref_in_parent = new_child

class binary_function(Function):
    def __init__(self):
        self.IsOperator = "binary_function"
        self.node_sons = {
            'left': None,
            'right':None
        }
    def calculate(self, x):
        return 0
    def get_self(self, nodes):
        nodes.append(self)
        self.node_sons['left'].get_self(nodes)
        self.node_sons['right'].get_self(nodes)
    def define_parent(self, reference):
        self.parent = reference
        self.node_sons['left'].define_parent([self,'left'])
        self.node_sons['right'].define_parent([self,'right'])

class GP_sin(unary_function):
    def calculate(self, x):
        return np.sin(self.node_sons['left'].calculate(x))
    
class GP_abs(unary_function):
    def calculate(self, x):
        return np.abs(self.left_node.calculate(x))
    
class GP_exp(unary_function):
    def calculate(self, x):
        return np.exp(self.left_node.calculate(x))

class GP_sum(binary_function):
    def calculate(self, x):
        return self.node_sons['left'].calculate(x) + self.node_sons['right'].calculate(x)

class GP_differense(binary_function):
    def calculate(self, x):
        return self.node_sons['left'].calculate(x) - self.node_sons['right'].calculate(x)
    
class GP_product(binary_function):
    def calculate(self, x):
        return self.node_sons['left'].calculate(x) * self.node_sons['right'].calculate(x)

class GP_division(binary_function):
    def calculate(self, x):
        return self.node_sons['left'].calculate(x) / self.node_sons['right'].calculate(x)

class Terminal(Genetic_Node):
    def calculate(self, x):
        return 0
    def get_self(self, nodes):
        nodes.append(self)
    def define_parent(self, reference):
        self.parent = reference

    
class Variable(Terminal):
    var_index = None
    # def __init__(self, index):
    #     self.var_index = index
    #     self.IsTerminal = f'variable_{index}'
    def __init__(self):
        self.IsTerminal = 'variable'
    def calculate(self, x):
        return x[:,self.var_index]
    
class Value(Terminal):
    value = [None, None]  # первое - значение константы, второе - размерность задачи
    # def __init__(self, value):
    #     self.value = value
    #     self.IsTerminal = 'vaule'
    def __init__(self):
        self.IsTerminal = 'value'
    def calculate(self, x):
        return self.value[0] * np.ones(self.value[1])




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