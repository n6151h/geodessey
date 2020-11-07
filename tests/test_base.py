
from unittest import TestCase

from ..base import *

class TestFunctions(TestCase):
    
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
            
        rm = g.rho(1)
        self.assertEqual(rm, [[0, 0, 1], [1, 0, 0], [0, 1, 0]])
        
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