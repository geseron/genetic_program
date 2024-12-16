import numpy as np
from GP import *
import graphviz

class gp_individ():
    def __init__(self, dimensions, data_size, mutation_probability = 0.3, vaule_borders=[0,1], depth=5):
        self.depth_limit = depth # ограничение на длину дерева
        self.dimension_count = dimensions # нужно для количества переменных. Так же для разграничения в классе Variable одномерного и многомерного случаев
        self.data_size = data_size # нужно для правильного понимания констант. Должна представлять собой вектор
        self.vaule_borders = vaule_borders
        self.mutation_probability = mutation_probability
        self.function_list = {
            'sin':GP_sin,
            'abs':GP_abs,
            'exp':GP_exp,
            'sum':GP_sum,
            'differense':GP_differense,
            'product':GP_product,
            'division':GP_division
        }
        self.terminal_list = {
            'variable':Variable,
            'value':Value
        }
        self.functions = list(self.function_list.values())
        self.u_functions = list(filter(lambda x: x.IsOperator == "unary_function", self.functions))
        self.bi_functions = list(filter(lambda x: x.IsOperator == "binary_function", self.functions))
        self.terminals = list(self.terminal_list.values())

        self.function_count = len(self.function_list.values())
        self.terminal_count = len(self.terminal_list.values())
        self.nodes = []
        self.nodes_count = 1     # заголовок - первый узел

        self.head = self.functions[np.random.randint(self.function_count)]()
        self.nodes.append(self.head)
        self.head.dimension_count = self.dimension_count

        self.nodes_count = self.fill_functions()
        self.nodes_count = self.fill_terminals()
        self.depth = self.head.get_depth()
        self.head.define_parent(None)


    def fill_functions(self):
        depth = 1
        nodes_count = 1
        while depth < self.depth_limit:
            temp_nodes = []
            for node in self.nodes:
                if node.node_sons['left'] is None:
                    if node.IsOperator == "unary_function":
                        node.node_sons['left'] = self.functions[np.random.randint(self.function_count)]()
                        temp_nodes.append(node.node_sons['left'])
                        nodes_count += 1
                    else:
                        node.node_sons['left'] = self.functions[np.random.randint(self.function_count)]()
                        node.node_sons['right'] = self.functions[np.random.randint(self.function_count)]()
                        temp_nodes.append(node.node_sons['left'])
                        temp_nodes.append(node.node_sons['right'])
                        nodes_count += 2
            for temp in temp_nodes:
                self.nodes.append(temp)
            depth +=1
        return nodes_count

    def fill_terminals(self):
        temp_nodes = []
        for i in reversed(range(1,self.nodes_count)):
            if self.nodes[i].IsOperator == "unary_function" and self.nodes[i].node_sons['left'] is None:
                self.nodes[i].node_sons['left'] = self.terminals[np.random.randint(self.terminal_count)](self.dimension_count, self.data_size)

                if self.nodes[i].node_sons['left'].IsTerminal == 'variable': self.nodes[i].node_sons['left'].var_index = np.random.randint(self.dimension_count)
                else: self.nodes[i].node_sons['left'].value = np.random.uniform(self.vaule_borders[0],self.vaule_borders[1])

                temp_nodes.append(self.nodes[i].node_sons['left'])
            elif self.nodes[i].IsOperator == "binary_function":
                if (self.nodes[i].node_sons['left'] is None) and (self.nodes[i].node_sons['right'] is None): 
                    self.nodes[i].node_sons['left'] = self.terminals[np.random.randint(self.terminal_count)](self.dimension_count, self.data_size)
                    self.nodes[i].node_sons['right'] = self.terminals[np.random.randint(self.terminal_count)](self.dimension_count, self.data_size)

                    if self.nodes[i].node_sons['left'].IsTerminal == 'variable': self.nodes[i].node_sons['left'].var_index = np.random.randint(self.dimension_count)
                    else: self.nodes[i].node_sons['left'].value = np.random.uniform(self.vaule_borders[0],self.vaule_borders[1])
                    if self.nodes[i].node_sons['right'].IsTerminal == 'variable': self.nodes[i].node_sons['right'].var_index = np.random.randint(self.dimension_count)
                    else: self.nodes[i].node_sons['right'].value = np.random.uniform(self.vaule_borders[0],self.vaule_borders[1])

                    temp_nodes.append(self.nodes[i].node_sons['left'])
                    temp_nodes.append(self.nodes[i].node_sons['right'])
                elif (self.nodes[i].node_sons['left'] is None):
                    self.nodes[i].node_sons['left'] = self.terminals[np.random.randint(self.terminal_count)](self.dimension_count, self.data_size)

                    if self.nodes[i].node_sons['left'].IsTerminal == 'variable': self.nodes[i].node_sons['left'].var_index = np.random.randint(self.dimension_count)
                    else: self.nodes[i].node_sons['left'].value = np.random.uniform(self.vaule_borders[0],self.vaule_borders[1])

                    temp_nodes.append(self.nodes[i].node_sons['left'])
                elif (self.nodes[i].node_sons['right'] is None):
                    self.nodes[i].node_sons['right'] = self.terminals[np.random.randint(self.terminal_count)](self.dimension_count, self.data_size)

                    if self.nodes[i].node_sons['right'].IsTerminal == 'variable': self.nodes[i].node_sons['right'].var_index = np.random.randint(self.dimension_count)
                    else: self.nodes[i].node_sons['right'].value = np.random.uniform(self.vaule_borders[0],self.vaule_borders[1])
                    
                    temp_nodes.append(self.nodes[i].node_sons['right'])
        for temp in temp_nodes:
            self.nodes.append(temp)
        return len(self.nodes)

    def mutation(self):
        nodes_indexes = np.array(range(1,self.nodes_count))
        nodes_for_mutation = nodes_indexes[np.random.rand(self.nodes_count-1) < self.mutation_probability]
        if len(nodes_for_mutation) == 0: 
            return
        for mutant_index in nodes_for_mutation:
            mutant = self.nodes[mutant_index]
            if mutant.IsOperator == "unary_function":
                variants = self.u_functions.copy()

                variants.remove( self.function_list[mutant.kind_function] )
                new_node = np.random.choice(variants)()

                new_node.parent = mutant.parent
                new_node.parent[0].node_sons[mutant.parent[1]] = new_node
                new_node.node_sons = mutant.node_sons.copy()
                new_node.node_sons['left'].parent = [new_node,'left']

                self.nodes[mutant_index] = new_node           
            elif mutant.IsOperator == "binary_function":
                variants = self.bi_functions.copy()
                variants.remove( self.function_list[mutant.kind_function] )

                new_node = np.random.choice(variants)()

                new_node.parent = mutant.parent
                new_node.parent[0].node_sons[mutant.parent[1]] = new_node
                new_node.node_sons = mutant.node_sons.copy()
                new_node.node_sons['left'].parent = [new_node,'left']
                new_node.node_sons['right'].parent = [new_node,'right']

                self.nodes[mutant_index] = new_node
            elif not(mutant.IsTerminal == None):
                variants = self.terminals.copy()

                new_node = np.random.choice(variants)(self.dimension_count, self.data_size)

                if new_node.IsTerminal == 'value':
                    new_node.value = np.random.uniform(self.vaule_borders[0],self.vaule_borders[1])
                elif new_node.IsTerminal == 'variable':
                    new_node.var_index = np.random.randint(self.dimension_count)
                
                new_node.parent = mutant.parent
                new_node.parent[0].node_sons[mutant.parent[1]] = new_node
                
                self.nodes[mutant_index] = new_node
                # del variants
        self.head.define_parent(None)

    def variable_check(self):
        terminals = []
        for i in range(1,self.nodes_count):
            if self.nodes[i].IsOperator is None:
                terminals.append( [self.nodes[i], self.nodes[i].IsTerminal, i ] )
        terminals = np.array(terminals)
        mask_value = terminals[:,1] == 'value'
        values = terminals[mask_value]
        if len( values ) == 0: return
        elif len( terminals[np.logical_not(mask_value)] ) > 2: return
        else:
            node_index_for_replace = np.random.randint(0,len(values))
            new_node = Variable(self.dimension_count, self.data_size)
            old_node_index = values[node_index_for_replace][2]
            new_node.var_index = np.random.randint(0,self.dimension_count)
            new_node.parent = values[node_index_for_replace][0].parent
            new_node.parent[0].node_sons[new_node.parent[1]] = new_node
            self.nodes[old_node_index] = new_node
        self.head.define_parent(None)
        self.nodes = []
        self.head.get_self(self.nodes)
        self.nodes_count = len(self.nodes)

    def predict(self, x):
        return self.head.calculate(x)


    def draw_tree(self, iteration=0, selection = None):
        self.graph = graphviz.Digraph()
        self.head.visualize(self.graph)
        if not(selection is None):
            self.graph.render(f'exp\\trees\\{selection}{iteration}', format='png', view=False)
        else:
            self.graph.render(f'trees\\tree{str(id(self))[-4:]}', format='png', view=True)

    def __del__(self):
        del self.nodes
        del self.head



    x = np.array([  [5, 10],
                    [7, 3]
                ])




