__author__ = 'dvapan'

import random
import scipy as sc

from simplex_method import solver
import pprint
min_val = -50
max_val = 50

def generate_task(m,n):
    A = sc.matrix([[random.randint(min_val, max_val)
         for i in range(n)] for j in range(m)])
    b = sc.matrix([random.randint(1, max_val) for i in range(m)]).transpose()
    c = sc.matrix([random.randint(min_val, max_val) for i in range(n)]).transpose()
    return A, b, c

Task = generate_task(4, 4)
pprint.pprint(Task)
print solver(Task[0], Task[1], Task[2], 0.01)