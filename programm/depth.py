import numpy as np
from GP import *
import graphviz

def obj_set(node):
    for i in node:
        print(f'{i}')
    print()

function_list = {
    'sin':GP_sin,
    'abs':GP_abs,
    'exp':GP_exp,
    'sum':GP_sum,
    'differense':GP_differense,
    'product':GP_product,
    'division':GP_division
}
terminal_list = {
    'variable':Variable,
    'value':Value
}

x = np.array([  [5, 10],
                [7, 3]
            ])

functions = list(function_list.values())
u_functions = list(filter(lambda x: x.IsOperator == "unary_function", functions))
bi_functions = list(filter(lambda x: x.IsOperator == "binary_function", functions))
terminals = list(terminal_list.values())

function_count = len(function_list.values())
terminal_count = len(terminal_list.values())

nodes = []
nodes_count = 1     # заголовок - первый узел
dimension_count = 2
vaule_borders = [0,1]
depth = 1
depth_limit = 10 # ограничение на длину дерева

head = functions[np.random.randint(function_count)]()
nodes.append(head)

def fill_functions(nodes, depth_limit, functions):
    depth = 1
    nodes_count = 1
    while depth<depth_limit:
        temp_nodes = []
        for node in nodes:
            if node.node_sons['left'] is None:
                if node.IsOperator == "unary_function":
                    node.node_sons['left'] = functions[np.random.randint(function_count)]()
                    temp_nodes.append(node.node_sons['left'])
                    nodes_count += 1
                else:
                    node.node_sons['left'] = functions[np.random.randint(function_count)]()
                    node.node_sons['right'] = functions[np.random.randint(function_count)]()
                    temp_nodes.append(node.node_sons['left'])
                    temp_nodes.append(node.node_sons['right'])
                    nodes_count += 2
        for temp in temp_nodes:
            nodes.append(temp)
        depth +=1
    return nodes_count

def fill_terminals(nodes, nodes_count, dimension_count, vaule_borders, terminals):
    temp_nodes = []
    for i in reversed(range(1,nodes_count)):
        if nodes[i].IsOperator == "unary_function" and nodes[i].node_sons['left'] is None:
            nodes[i].node_sons['left'] = terminals[np.random.randint(terminal_count)]()

            if nodes[i].node_sons['left'].IsTerminal == 'variable': nodes[i].node_sons['left'].var_index = np.random.randint(dimension_count)
            else: nodes[i].node_sons['left'].value = [np.random.uniform(vaule_borders[0],vaule_borders[1]), dimension_count]

            temp_nodes.append(nodes[i].node_sons['left'])
        elif nodes[i].IsOperator == "binary_function":
            if (nodes[i].node_sons['left'] is None) and (nodes[i].node_sons['right'] is None): 
                nodes[i].node_sons['left'] = terminals[np.random.randint(terminal_count)]()
                nodes[i].node_sons['right'] = terminals[np.random.randint(terminal_count)]()

                if nodes[i].node_sons['left'].IsTerminal == 'variable': nodes[i].node_sons['left'].var_index = np.random.randint(dimension_count)
                else: nodes[i].node_sons['left'].value = [np.random.uniform(vaule_borders[0],vaule_borders[1]), dimension_count]
                if nodes[i].node_sons['right'].IsTerminal == 'variable': nodes[i].node_sons['right'].var_index = np.random.randint(dimension_count)
                else: nodes[i].node_sons['right'].value = [np.random.uniform(vaule_borders[0],vaule_borders[1]), dimension_count]

                temp_nodes.append(nodes[i].node_sons['left'])
                temp_nodes.append(nodes[i].node_sons['right'])
            elif (nodes[i].node_sons['left'] is None):
                nodes[i].node_sons['left'] = terminals[np.random.randint(terminal_count)]()

                if nodes[i].node_sons['left'].IsTerminal == 'variable': nodes[i].node_sons['left'].var_index = np.random.randint(dimension_count)
                else: nodes[i].node_sons['left'].value = [np.random.uniform(vaule_borders[0],vaule_borders[1]), dimension_count]

                temp_nodes.append(nodes[i].node_sons['left'])
            elif (nodes[i].node_sons['right'] is None):
                nodes[i].node_sons['right'] = terminals[np.random.randint(terminal_count)]()

                if nodes[i].node_sons['right'].IsTerminal == 'variable': nodes[i].node_sons['right'].var_index = np.random.randint(dimension_count)
                else: nodes[i].node_sons['right'].value = [np.random.uniform(vaule_borders[0],vaule_borders[1]), dimension_count]
                
                temp_nodes.append(nodes[i].node_sons['right'])
    for temp in temp_nodes:
        nodes.append(temp)
    return len(nodes)

nodes_count = fill_functions(nodes, depth_limit-1, functions)
nodes_count = fill_terminals(nodes, nodes_count, dimension_count, vaule_borders, terminals)
depth = head.get_depth()

print(head.calculate(x))

obj_set(nodes)
print(f"Количество узлов: {len(nodes)}  {nodes_count}")

head.define_parent(None)
for i in nodes:
    if i.IsTerminal == 'variable':
        print(f'ObJ: {i}        parent:  {i.parent}     {i.var_index}')
    elif i.IsTerminal == 'value':
        print(f'ObJ: {i}        parent:  {i.parent}     {i.value}')
    else:
        print(f'ObJ: {i}        parent:  {i.parent}')

print("Depth of the tree:", depth)
# Пример использования
graph = graphviz.Digraph()
head.visualize(graph)
graph.render('tree', format='png', view=True)
