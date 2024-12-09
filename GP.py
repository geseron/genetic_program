import numpy as np

class Genetic_Node():
    IsOperator = None
    IsTerminal = None
    parent = None
    dimension_count = None

    def visualize(self, graph, parent_id=None):
        node_id = str(id(self))
        graph.node(node_id, self.__class__.__name__)
        if parent_id:
            graph.edge(parent_id, node_id)


class Function(Genetic_Node):
    def calculate(self, x):
        return 0

class unary_function(Function):
    IsOperator = "unary_function"
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
    def get_depth(self):
        return 1 + self.node_sons['left'].get_depth()
    def visualize(self, graph, parent_id=None):
        node_id = str(id(self))
        graph.node(node_id, self.__class__.__name__)
        if parent_id:
            graph.edge(parent_id, node_id)
        self.node_sons['left'].visualize(graph, node_id)

class binary_function(Function):
    IsOperator = "binary_function"
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
    def get_depth(self):
        return 1 + max(self.node_sons['left'].get_depth(), self.node_sons['right'].get_depth())
    def visualize(self, graph, parent_id=None):
        node_id = str(id(self))
        graph.node(node_id, self.__class__.__name__)
        if parent_id:
            graph.edge(parent_id, node_id)
        self.node_sons['left'].visualize(graph, node_id)
        self.node_sons['right'].visualize(graph, node_id)
    
class GP_sin(unary_function):
    kind_function = "sin"
    def __init__(self):
        self.node_sons = {
            'left': None,
            'right':None
        }
    def calculate(self, x):
        return np.sin(self.node_sons['left'].calculate(x))
    
class GP_abs(unary_function):
    kind_function = "abs"
    def __init__(self):
        self.node_sons = {
            'left': None,
            'right':None
        }
    def calculate(self, x):
        return np.abs(self.node_sons['left'].calculate(x))
    
class GP_exp(unary_function):
    kind_function = "exp"
    def __init__(self):
        self.node_sons = {
            'left': None,
            'right':None
        }
    def calculate(self, x):
        return np.exp(self.node_sons['left'].calculate(x))

class GP_sum(binary_function):
    kind_function = "sum"
    def __init__(self):
        self.node_sons = {
            'left': None,
            'right':None
        }
    def calculate(self, x):
        return self.node_sons['left'].calculate(x) + self.node_sons['right'].calculate(x)

class GP_differense(binary_function):
    kind_function = "differense"
    def __init__(self):
        self.node_sons = {
            'left': None,
            'right':None
        }
    def calculate(self, x):
        return self.node_sons['left'].calculate(x) - self.node_sons['right'].calculate(x)
    
class GP_product(binary_function):
    kind_function = "product"
    def __init__(self):
        self.node_sons = {
            'left': None,
            'right':None
        }
    def calculate(self, x):
        return self.node_sons['left'].calculate(x) * self.node_sons['right'].calculate(x)

class GP_division(binary_function):
    kind_function = "division"
    def __init__(self):
        self.node_sons = {
            'left': None,
            'right':None
        }
    def calculate(self, x):
        return self.node_sons['left'].calculate(x) / self.node_sons['right'].calculate(x)

class Terminal(Genetic_Node):
    def calculate(self, x):
        return 0
    def get_self(self, nodes):
        nodes.append(self)
    def define_parent(self, reference):
        self.parent = reference
    def get_depth(self):
        return 1

    
class Variable(Terminal):
    var_index = None
    def __init__(self):
        self.IsTerminal = 'variable'
    def calculate(self, x):
        return x[:,self.var_index]
    def visualize(self, graph, parent_id=None):
        node_id = f'{str(id(self))}'
        graph.node(node_id, f"x_{self.var_index}")
        if parent_id:
            graph.edge(parent_id, node_id)
    
class Value(Terminal):
    value = [None, None]  # первое - значение константы, второе - размерность задачи
    def __init__(self):
        self.IsTerminal = 'value'
    def calculate(self, x):
        return self.value[0] * np.ones(self.value[1])
    def visualize(self, graph, parent_id=None):
        node_id = f'{str(id(self))}'
        graph.node(node_id, f"{self.value[0]:.2f}")
        if parent_id:
            graph.edge(parent_id, node_id)


