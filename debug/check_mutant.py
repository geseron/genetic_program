import numpy as np
#from GP import *
from individ import gp_individ
import graphviz

x = np.array([  [5, 10],
                [7, 3]
            ])


c = gp_individ(2, depth=3)
print(c.predict(x))
c.draw_tree()
c.mutation()