
from unittest import TestCase
from ..base import *


def checkEqualLists(a1, a2):
    return len(a1) == len(a2) and sorted(a1) == sorted(a2)


class TestGeodesic(TestCase):

    def test_rho(self):

        g = Geodesic()

        with self.assertRaises(TypeError):
            g.rho('a')

        with self.assertRaises(TypeError):
            g.rho(1.4)

        with self.assertRaises(ValueError):
            g.rho(0)
            
        with self.assertRaises(ValueError):
            g.rho(9)
            
        rm = sorted(g.rho(1))
        self.assertEqual(rm, sorted([[0, 0, 1], [1, 0, 0], [0, 1, 0]]))
        
        rm = g.rho(2)
        self.assertEqual(rm,  [[0, 0, 0, 1, 1, 2], [2, 1, 0, 1, 0, 0], [0, 1, 2, 0, 1, 0]])
        
        rm = g.rho(3)
        self.assertEqual(rm,[[0, 0, 0, 0, 1, 1, 1, 2, 2, 3],
                             [3, 2, 1, 0, 2, 1, 0, 1, 0, 0],
                             [0, 1, 2, 3, 0, 1, 2, 0, 1, 0]])
            
        rm = g.rho(4)
        self.assertEqual(rm, [[0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4],
                              [4, 3, 2, 1, 0, 3, 2, 1, 0, 2, 1, 0, 1, 0, 0],
                              [0, 1, 2, 3, 4, 0, 1, 2, 3, 0, 1, 2, 0, 1, 0]])
        
        # This should satisfy us.
        
    def test_apices(self):
        
        g = Geodesic()
        
        with self.assertRaises(TypeError):
            g.apices('a')
            
        with self.assertRaises(TypeError):
            g.apices(2.3)
            
        with self.assertRaises(ValueError):
            g.apices(0)
            
        am = g.apices(1)
        self.assertTrue(checkEqualLists([a.xyz for a in am], [[0, 1, 0], [0, 0, 1], [1, 0, 0]]))

        am = g.apices(2)
        self.assertTrue(checkEqualLists([a.xyz for a in am], [[0, 2, 0], [0, 1, 1], [0, 0, 2], [1, 1, 0], [1, 0, 1], [2, 0, 0]]))
        
        am = g.apices(4)
        self.assertTrue(checkEqualLists([a.xyz for a in am], [[0, 4, 0],
                         [0, 3, 1],
                         [0, 2, 2],
                         [0, 1, 3],
                         [0, 0, 4],
                         [1, 3, 0],
                         [1, 2, 1],
                         [1, 1, 2],
                         [1, 0, 3],
                         [2, 2, 0],
                         [2, 1, 1],
                         [2, 0, 2],
                         [3, 1, 0],
                         [3, 0, 1],
                         [4, 0, 0]]))
        
        def test_dist(self):
            
            g = Geodesic()
            