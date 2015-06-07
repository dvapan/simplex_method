# coding=utf-8
__author__ = 'dvapan'

import scipy as sc
import scipy.linalg as lin
import pprint
#
# c = sc.matrix([2.0, 3.0]).transpose()
# A = sc.matrix([[-10.0, 5.0], [6.0, 20.0], [8.0, 15.0]])
# b = sc.matrix([600.0, 600.0, 600.0]).transpose()



# I = [2, 3, 4]
def transform_to_classic(A,b,c):
    count_vars = A.shape[1]
    addition_vars = A.shape[0]
    count_all_vars = count_vars + addition_vars
    _A = sc.resize(A, (A.shape[0], count_all_vars))
    _A[:, :count_vars] = A
    _A[:, count_vars:] = sc.eye(addition_vars)
    _c = sc.resize(c, (count_all_vars, 1))
    _c[count_vars:, :] = sc.zeros((addition_vars, 1))
    I = range(count_vars, count_vars+addition_vars)
    return _A, b, _c, I


# A = sc.matrix([[1, 1, -1, 1],
#                [1, 14, 10, -10]])
# b = sc.matrix([2, 24]).transpose()
# c = sc.matrix([1, 2, 3, -4]).transpose()

def get_point_from_basis(A, b, I):
    B_sigma = A[:, I]
    x_sigma = lin.solve(B_sigma, b)
    x = sc.zeros(A.shape[1])
    #print x_sigma
    x[I] = x_sigma
    return x


def simplex_method(A, b, c, I, eps):
    count_all_vars = A.shape[1]
    q = 50
    while q > 0:
        B_sigma = A[:, I]
        c_sigma = c[I, :]

        x_sigma = lin.solve(B_sigma, b)
        y = lin.solve(B_sigma.transpose(), c_sigma)

        D = sc.matrix(A).transpose()*y - c
        non_base_I = [e for e in range(count_all_vars) if e not in I]

        q-=1
        finish = reduce(lambda x, y: x and y, map(lambda x: x > -eps, D[non_base_I]), True)

        # print I
        # print D.transpose().tolist()[0], get_point_from_basis(A, b, I)


        if finish:
            x = get_point_from_basis(A, b, I)
            return x, I, (sc.matrix(x)*sc.matrix(c))[0, 0]

        k = min([i for i in non_base_I if D[i] < 0])

        lmd_k = lin.solve(B_sigma, A[:, k])
        finish = reduce(lambda x, y: x and y, map(lambda x: x < 0, lmd_k),True)
        if finish:
            return None, None, sc.nan


        tmp = sc.array(x_sigma.transpose())[0].tolist()
        min_i = 0
        while lmd_k[min_i] <= 0:
            min_i += 1
        for i in xrange(len(lmd_k)):
            if lmd_k[i] > 0 and tmp[i]/lmd_k[i] < tmp[min_i]/lmd_k[min_i]:
                min_i = i
        s = min_i
        I[s] = k
    return None,None,None


def artificial_basis_method(A, b, c, eps):
    # TODO В методе искуственного базиса в выводимом базисе заменить искусственные векторы на векторы из задачи
    count_vars = A.shape[1]
    addition_vars = A.shape[0]
    count_all_vars = count_vars + addition_vars
    _A = sc.resize(A, (A.shape[0], count_all_vars))
    _A[:, :count_vars] = A
    _A[:, count_vars:] = sc.eye(addition_vars)
    _c = sc.resize(c, (count_all_vars, 1))
    _c[:count_vars, :] = sc.zeros((count_vars, 1))
    _c[count_vars:, :] = sc.full((addition_vars, 1), -1)
    # if I is None:
    I = range(count_vars, count_vars+addition_vars)
    # pprint.pprint((_A, b, _c ,I))
    Res = simplex_method(_A, b, _c, I, eps)
    if Res[2] < -eps:
        return None, None, None
    Real_I = [i for i in range(count_vars) if i not in Res[1]]

    for i in range(len(Res[1])):
        if Res[1][i] >= count_vars:
            Res[1][i] = Real_I.pop(0)

    return Res


def double_phase_simplex_method(A, b, c, eps):
    Res = artificial_basis_method(A, b, c, eps)
    while Res[1] is not None and len(filter(lambda x: x >= A.shape[1], Res[1])) > 0:
        print "NEED NEXT ITER OF FIRST PHASE"
        Res = artificial_basis_method(A, b, c, eps, Res[1])
    if Res[1] is not None:
        return simplex_method(A, b, c, Res[1], eps)
    else:
        return None, None, None
