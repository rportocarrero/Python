import unittest
from taylor_Series import *

class TestTaylorSeries(unittest.TestCase):
    def test_taylor_series(self):
        # Test the taylor_series function with some known expansions
        def f(x):
            return x**2
        self.assertAlmostEqual(taylor_series(f, 0, 1), 0.0, places=10)
        self.assertAlmostEqual(taylor_series(f, 0, 2), 0.0, places=10)
        self.assertAlmostEqual(taylor_series(f, 0, 3), 0.0, places=10)
        self.assertAlmostEqual(taylor_series(f, 1, 1), 1.0, places=10)
        self.assertAlmostEqual(taylor_series(f, 1, 2), 1.0, places=10)
        self.assertAlmostEqual(taylor_series(f, 1, 3), 1.0, places=10)
        self.assertAlmostEqual(taylor_series(f, 2, 1), 4.0, places=10)
        self.assertAlmostEqual(taylor_series(f, 2, 2), 4.0, places=10)
        self.assertAlmostEqual(taylor_series(f, 2, 3), 4.0, places=10)

if __name__ == '__main__':
    unittest.main()
