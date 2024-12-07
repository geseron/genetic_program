import numpy as np
from GP import *

def obj_set(node):
    for i in nodes:
        print(f'{i}')
    print()



x = [5, 10]

function_list = {
    'sin':GP_sin,
    'sum':GP_sum
}
terminal_list = {
    'var':Variable,
    'value':Value
}

individ = function_list['sum'](left_node = function_list['sin'](terminal_list['var'](0)),
                               right_node = function_list['sum'](terminal_list['value'](5),
                                                                 function_list['sin'](terminal_list['var'](1)))
                               )

nodes = []
individ.get_self(nodes)
obj_set(nodes)

individ.define_parent(None)

for i in nodes:
    print(f'ObJ: {i}        ref_in_parent:  {i.ref_in_parent}')

#print(nodes[1])


print(individ.calculate(x))
nodes[5].ref_in_parent[0] = nodes[3]
print(individ.calculate(x))

nodes = []
individ.get_self(nodes)
obj_set(nodes)

#print(nodes[5].ref_in_parent)