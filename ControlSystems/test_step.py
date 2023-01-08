from step import *
import unittest

class TestStepFunction(unittest.TestCase):
    def test_zero_nodelay(self):
        """
       the value at zero with no delay should be 1
        """
        self.assertEqual(step(0,0),1)

    def test_zero_delay(self):
        """
        The value at zero with a delay should be 0
        """
        self.assertEqual(step(0,1),0)

    def test_delay_withdelay(self):
        """
        The value at the delay time should be 1"""
        self.assertEqual(step(1,1),1)

    def test_afterDelay_withDelay(self):
        """
        The value after the delay time should be 1"""
        self.assertEqual(step(2,1),1)

    def test__array_withDelay(self):
        """
        This tests that the function can be mapped over a series of timesteps
        """
        timesteps = [0,1,2,3,4,5]
        delay = [3,3,3,3,3,3]
        expected = [0,0,0,1,1,1]
        result = map(step,timesteps,delay)
        self.assertEqual(expected,result)


if __name__== '__main__':
    unittest.main()