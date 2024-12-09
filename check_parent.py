import numpy as np
from GP import *
# from GP import GP_sin
# from GP import GP_sum
# from GP import Variable
# from GP import Value
#import GP

def obj_set(node):
    for i in node:
        print(f'{i}')
    print()

def gp_sin():
    return GP_sin()
def gp_sum():
    return GP_sum()
def gp_variable():
    return Variable()
def gp_value():
    return Value()


x = [5, 10]

# function_list = {
#     'sin':gp_sin,
#     'sum':gp_sum
# }
# terminal_list = {
#     'var':gp_variable,
#     'value':gp_value
# }
function_list = {
    'sin':GP_sin,
    'sum':GP_sum
}
terminal_list = {
    'var':Variable,
    'value':Value
}

componets = [function_list['sum'](),
             function_list['sin'](), terminal_list['var'](), 
             function_list['sum'](), terminal_list['value'](), function_list['sin'](),
             terminal_list['var']()]
# componets = (GP.GP_sum(),
#              GP.GP_sin(), GP.Variable(), 
#              GP.GP_sum(), GP.Value(), GP.GP_sin(),
#              GP.Variable())

print(f"{componets[0] is componets[3]=}")

individ_0 = componets[0]
individ_0.node_sons['left'] = componets[1]
individ_0.node_sons['right'] = componets[3]
componets[1].node_sons['left'] = componets[2]
componets[2].var_index = 0
componets[3].node_sons['left'] = componets[4]
componets[3].node_sons['right'] = componets[5]
componets[4].value = 5
componets[5].node_sons['left'] = componets[6]
componets[6].var_index = 1



h = individ_0.calculate(x)
print(h)


nodes_ind = []
individ_0.get_self(nodes_ind)
obj_set(nodes_ind)

individ_0.define_parent(None)
for i in nodes_ind:
    print(f'ObJ: {i}        parent:  {i.parent}')

# temp = componets[1]
# side = componets[1].parent[1]
# componets[1].parent[0].node_sons[side] = componets[4]
# side = componets[4].parent[1]
# componets[4].parent[0].node_sons[side] = temp

# temp = componets[2]
# side = componets[2].parent[1]
# componets[2].parent[0].node_sons[side] = componets[6]
# side = componets[6].parent[1]
# componets[6].parent[0].node_sons[side] = temp
# individ_0.define_parent(None)

nodes_ind = []
individ_0.get_self(nodes_ind)
obj_set(nodes_ind)

for i in nodes_ind:
    print(f'ObJ: {i}        parent:  {i.parent}')

print(f"{individ_0.calculate(x)}")

componets = [function_list['sum'](),
             function_list['sin'](), terminal_list['var'](), 
             function_list['sum'](), terminal_list['value'](), function_list['sin'](),
             terminal_list['var']()]


friend = componets[0]
friend.node_sons['left'] = componets[1]
friend.node_sons['right'] = componets[3]
componets[1].node_sons['left'] = componets[2]
componets[2].var_index = 0
componets[3].node_sons['left'] = componets[4]
componets[3].node_sons['right'] = componets[5]
componets[4].value = 2
componets[5].node_sons['left'] = componets[6]
componets[6].var_index = 1

friend.define_parent(None)
nodes_fri = []
friend.get_self(nodes_fri)
obj_set(nodes_fri)
for i in nodes_fri:
    print(f'ObJ: {i}        parent:  {i.parent}')
print(f"{friend.calculate(x)}")

individ_node = 5
friend_node = 3
temp = nodes_ind[individ_node]
side = nodes_ind[individ_node].parent[1]
nodes_ind[individ_node].parent[0].node_sons[side] = nodes_fri[friend_node]
side = nodes_fri[friend_node].parent[1]
nodes_fri[friend_node].parent[0].node_sons[side] = temp
individ_0.define_parent(None)
friend.define_parent(None)

nodes_fri = []
friend.get_self(nodes_fri)
nodes_ind = []
individ_0.get_self(nodes_ind)

for i in nodes_fri:
    print(f'ObJ: {i}        parent:  {i.parent}')

for i in nodes_ind:
    print(f'ObJ: {i}        parent:  {i.parent}')

print(f"{friend.calculate(x)=}")
print(f"{individ_0.calculate(x)=}")
