import unittest
import torch
from GaussSeidelSim import *

class test_constructor_pos(unittest.TestCase):
    # ensure simulation constants are initialized properly
    def test_constructor_constants(self):
        sim = GaussSeidel(5,5,0.1)
        self.assertEqual(sim.DT,0.1,"timestep was not properly initialized")
        self.assertEqual(sim.G,-9.8,"gravitational acceleration was not properly initialized")

    # test that pressure field is initialized properly
    def test_constructor_p(self):
        sim = GaussSeidel(3,4,0.1)
        exp = torch.ones(3,4)
        self.assertEqual(sim.p.size(),exp.size(),"incrorrect p matrix dimensions")

    # test proper initialization of u matrix
    def test_constructor_u(self):
        sim = GaussSeidel(3,5,0.1)
        exp = torch.zeros(3,6)
        self.assertEqual(sim.u.size(),exp.size(),"incorrect initial u matrix dimensions")

    # test proper initialization of v matrix
    def test_constructor_u(self):
        sim = GaussSeidel(2,4,0.1)
        exp = torch.zeros(3,4)
        self.assertEqual(sim.v.size(),exp.size(),"incorrect initial v matrix dimensions")

class test_constructor_neg(unittest.TestCase):
    #test negative row input 
    def test_negative_row(self):
        with self.assertRaises(ValueError):
            sim = GaussSeidel(-1,2,0.1)

    #negative col input
    def test_negative_col(self):
        with self.assertRaises(ValueError):
            sim = GaussSeidel(2,-1,0.1)

class test_gravity_update(unittest.TestCase):
    def test_gravity_update(self):
        sim = GaussSeidel(3,4,1)
        exp_v = torch.zeros(4,4)-9.8
        exp_u = torch.zeros(3,5)
        sim.gravity_update()

        self.assertTrue(torch.equal(sim.u,exp_u), "incorrect u field after gravity update")
        self.assertTrue(torch.equal(sim.v,exp_v), "incorrect v field after gravity update")

# test inlet boundary condition
class test_inlet_set(unittest.TestCase):
    def test_inlet_set(self):
        sim = GaussSeidel(1,1,0.1)
        sim.set_inlet(3)
        exp = torch.tensor([[3,0]])

        self.assertTrue(torch.equal(sim.u,exp),"incorrect inlet values initialized")

# tests the gauss-seidel iteration
class test_gauss_seidel(unittest.TestCase):
    def test_gauss_seidel_iteration(self):
        sim = GaussSeidel(2,2,0.1)
        sim.set_inlet(3)
        sim.next_iteration()

        

unittest.main()