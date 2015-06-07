__author__ = 'dvapan'

import random
import scipy as sc

from simplex_method import double_phase_simplex_method

import pprint
min_val = -50
max_val = 50

def generate_task(m,n):
    A = sc.matrix([[random.randint(min_val, max_val)
         for i in range(n)] for j in range(m)])
    b = sc.matrix([random.randint(1, max_val) for i in range(m)]).transpose()
    c = sc.matrix([random.randint(min_val, max_val) for i in range(n)]).transpose()
    return A, b, c

Task = generate_task(3, 5)
pprint.pprint(Task)
#print double_phase_simplex_method(Task[0], Task[1], Task[2], 0.01)

print "A:"
print Task[0]
print "b:"
print Task[1]
print "c:"
print Task[2]
Res = double_phase_simplex_method(Task[0], Task[1], Task[2], 0.0001)
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
