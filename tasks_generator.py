__author__ = 'dvapan'

import random
import scipy as sc

from simplex_method import *

min_val = -20
max_val = 20

def generate_task(m, n):
    A = sc.matrix([[float(random.randint(min_val, max_val))
         for i in range(n)] for j in range(m)])
    b = sc.matrix([float(random.randint(1, max_val)) for i in range(m)]).transpose()
    c = sc.matrix([float(random.randint(min_val, max_val)) for i in range(n)]).transpose()
    return A, b, c

if random.random() > 0.5:
    c *= random.randint(1, max_val)
    b *= random.randint(1, max_val)
    A *= random.randint(1, max_val)
    Task = A, b, c
else:
    Task = generate_task(2, 4)

print "A:"
print Task[0]
print "b:"
print Task[1]
print "c:"
print Task[2]
Res = solver(Task[0], Task[1], Task[2], 0.0001)
print "###########"
if Res[0] != None:
    print "x:"
    print Res[0]
    print "I:"
    print Res[1]
    print "<c,x>:"
    print Res[2]
else:
    print "Task has not solve"
