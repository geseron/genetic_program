import numpy as np
from GP import *

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
nodes_limit = 3 # ограничение на количество узлов в дереве
dimension_count = 2
vaule_borders = [0,1]

head = functions[np.random.randint(function_count)]()
nodes.append(head)

def fill_functions(nodes, nodes_count, nodes_limit, functions):
    previos_add_nodes = 1
    while nodes_count<nodes_limit:
        temp_nodes = []
        for node in nodes[nodes_count-previos_add_nodes:]:
            if node.IsOperator == "unary_function":
                node.node_sons['left'] = functions[np.random.randint(function_count)]()
                temp_nodes.append(node.node_sons['left'])
                previos_add_nodes = 1
                nodes_count+= previos_add_nodes
                if nodes_count>nodes_limit: continue
            else:
                node.node_sons['left'] = functions[np.random.randint(function_count)]()
                node.node_sons['right'] = functions[np.random.randint(function_count)]()
                temp_nodes.append(node.node_sons['left'])
                temp_nodes.append(node.node_sons['right'])
                previos_add_nodes = 2
                nodes_count+=previos_add_nodes
                if nodes_count>nodes_limit: continue
        for temp in temp_nodes:
            nodes.append(temp)
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

nodes_count = fill_functions(nodes, nodes_count, nodes_limit, functions)
nodes_count = fill_terminals(nodes, nodes_count, dimension_count, vaule_borders, terminals)

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


def mutation(nodes, nodes_count, function_list, u_functions, bi_functions, terminals):
    mutant_index = np.random.randint(1,nodes_count)
    mutant = nodes[mutant_index]
    if mutant.IsOperator == "unary_function":
        variants = u_functions.copy()

        variants.remove( function_list[mutant.kind_function] )
        new_node = np.random.choice(variants)()

        new_node.parent = mutant.parent
        new_node.parent[0].node_sons[mutant.parent[1]] = new_node
        new_node.node_sons = mutant.node_sons.copy()
        new_node.node_sons['left'].parent = [new_node,'left']

        nodes[mutant_index] = new_node
    elif mutant.IsOperator == "binary_function":
        variants = bi_functions.copy()
        variants.remove( function_list[mutant.kind_function] )

        new_node = np.random.choice(variants)()

        new_node.parent = mutant.parent
        new_node.parent[0].node_sons[mutant.parent[1]] = new_node
        new_node.node_sons = mutant.node_sons.copy()
        new_node.node_sons['left'].parent = [new_node,'left']
        new_node.node_sons['right'].parent = [new_node,'right']

        nodes[mutant_index] = new_node
    elif not(mutant.IsTerminal == None):
        variants = terminals.copy()
        
        new_node = np.random.choice(variants)()

        if new_node.IsTerminal == 'value':
            new_node.value = [np.random.uniform(vaule_borders[0],vaule_borders[1]), dimension_count]
        elif new_node.IsTerminal == 'variable':
            new_node.var_index = np.random.randint(dimension_count)
        
        new_node.parent = mutant.parent
        new_node.parent[0].node_sons[mutant.parent[1]] = new_node
        
        nodes[mutant_index] = new_node


