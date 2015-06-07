# coding=utf-8
__author__ = 'dvapan'

import unittest
from simplex_method import simplex_method, transform_to_classic, sc, artificial_basis_method, double_phase_simplex_method


class TestSimplexMethod(unittest.TestCase):
    def test_simplex_method_for_classic_task(self):
        c = sc.matrix([-1, 1, -2, 3, 1]).transpose()
        A = sc.matrix([[-1, 2, -1, -2, 1],
                      [-1, -1, 1, 2, 1],
                      [2, 1, 1, -1, 0]])
        b = sc.matrix([3, 1, 1]).transpose()

        Task = transform_to_classic(A, b, c)

        Res = simplex_method(Task[0], Task[1], Task[2], Task[3], 0.00001)
        #print Res
        #print double_phase_simplex_method(A, b, c, 0.0001)
        #print A*sc.matrix([0,3,0,2,0]).transpose()
        self.assertEqual(Res[0].tolist()[:5], [0, 3, 0, 2, 0])

    def test_artificial_basis_method(self):
        c = sc.matrix([5, 4, 3, 2, -3]).transpose()
        A = sc.matrix([[2, 1, 1, 1, -1],
                       [1, -1, 0, 1, 1],
                       [-2, -1, -1, 1, 0],
                       [-1, -2, -1, 2, 1]])
        b = sc.matrix([3, 1, 1, 2]).transpose()

        Res = artificial_basis_method(A, b, c, 0.00001)
        self.assertEqual(Res[1][:2], [1, 3])
        for el in Res[1]:
            self.assertLessEqual(el, len(Res))

    def test_double_phase_simplex_method(self):
        c = sc.matrix([-2, 2, 1, 2, -3]).transpose()
        A = sc.matrix([[-2, 1, -1, -1, 0],
                       [1, -1, 2, 1, 1],
                       [-1, 1, 0, 0, -1]])
        b = sc.matrix([1, 4, 4]).transpose()
        Res = double_phase_simplex_method(A, b, c, 0.001)
        self.assertEqual(Res[0].tolist(), [0, 9, 0, 8, 5])

        c = sc.matrix([5, 4, 3, 2, -3]).transpose()
        A = sc.matrix([[2, 1, 1, 1, -1],
                       [1, -1, 0, 1, 1],
                       [-2, -1, -1, 1, 0]])
        b = sc.matrix([3, 1, 1]).transpose()
        Res = double_phase_simplex_method(A, b, c, 0.001)
        self.assertEqual(Res[0].tolist(), [0, 1, 0, 2, 0])



if __name__ == '__main__':
    unittest.main()
