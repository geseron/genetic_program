import numpy as np
from GP import *

def obj_set(node):
    for i in nodes:
        print(f'{i}')



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

h = nodes[3].calculate(x)
z = []
nodes[3].get_self(z)
print(f'{z}  result: {h}')

friend = function_list['sum'](left_node = function_list['sin'](terminal_list['var'](0)),
                               right_node = function_list['sum'](terminal_list['value'](2),
                                                                 function_list['sin'](terminal_list['var'](1)))
                               )

print(f'{friend.calculate(x)=}')

friend_nodes = []
friend.get_self(friend_nodes)
obj_set(friend_nodes)

temp = friend_nodes[3]