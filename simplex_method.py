__author__ = 'dvapan'

import scipy as sc
import scipy.linalg as lin

# c = sc.matrix([2.0, 3.0]).transpose()
# A = sc.matrix([[10.0, 5.0], [6.0, 20.0], [8.0, 15.0]])
# b = sc.matrix([600.0, 600.0, 600.0]).transpose()
#
# I = [2, 3, 4]
# count_vars = A.shape[1]
# addition_vars = A.shape[0]
# count_all_vars = count_vars + addition_vars
# _A = sc.resize(A, (A.shape[0], count_all_vars))
# _A[:, :count_vars] = A
# _A[:, count_vars:] = sc.eye(addition_vars)
# _c = sc.resize(c, (count_all_vars, 1))
# _c[count_vars:, :] = sc.zeros((addition_vars, 1))


# c = sc.matrix([1, 2, 3, -4]).transpose()
# A = sc.matrix([[1, 1, -1, 1],
#                [1, 14, 10, -10]])
# b = sc.matrix([2, 24]).transpose()

def get_point_from_basis(A, b, I):
    B_sigma = A[:, I]
    x_sigma = lin.solve(B_sigma, b)
    x = sc.zeros(A.shape[1])
    x[I] = x_sigma
    return x


def simplex_method(A, b, c, I, eps):
    count_all_vars = A.shape[1]
    while 1:
        B_sigma = A[:, I]
        c_sigma = c[I, :]

        x_sigma = lin.solve(B_sigma, b)
        y = lin.solve(B_sigma.transpose(), c_sigma)

        D = sc.matrix(A).transpose()*y - c
        non_base_I = [e for e in range(count_all_vars) if e not in I]


        finish = reduce(lambda x, y: x and y, map(lambda x: x > -eps, D[non_base_I]), True)

        if finish:
            x = get_point_from_basis(A, b, I)
            return x, I, (sc.matrix(x)*sc.matrix(c))[0,0]

        k = min([i for i in non_base_I if D[i] < 0])

        lmd_k = lin.solve(B_sigma, A[:, k])
        finish = reduce(lambda x, y: x and y, map(lambda x: x < 0, lmd_k),True)
        if finish:
            return None, None, sc.nan

        tmp = (sc.array(x_sigma.transpose())[0]/sc.array(lmd_k)).tolist()
        s = tmp.index(min(tmp))
        I[s] = k


def first_phase(A, b, c, eps):
    count_vars = A.shape[1]
    addition_vars = A.shape[0]
    count_all_vars = count_vars + addition_vars
    _A = sc.resize(A, (A.shape[0], count_all_vars))
    _A[:, :count_vars] = A
    _A[:, count_vars:] = sc.eye(addition_vars)
    _c = sc.resize(c, (count_all_vars, 1))
    _c[:count_vars, :] = sc.zeros((count_vars, 1))
    _c[count_vars:, :] = sc.full((addition_vars, 1), -1)
    I = range(count_vars, count_vars+addition_vars)
    return simplex_method(_A, b, _c, I, eps)


def solver(A, b, c, eps):
    Res = first_phase(A, b, c, eps)
    if Res[2] < -eps:
        return None, None, None
    else:
        return simplex_method(A, b, c, Res[1], eps)

#Res = simplex_method(_A, b, _c, I, 0.0001)
#Res = first_phase(A, b, c, 0.0001)
#print solver(A, b, c, 0.0001)
