import torch

class StateSpace():
    def __init__(self, A, B, C, D, x, t):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.x = x
        self.t = t
        
    def step(self, u):
        x_dot = torch.matmul(self.A,self.x)+torch.matmul(self.B,u)
        self.x = torch.matmul(x_dot,self.t)+self.x
        return torch.matmul(self.C,self.x)+torch.matmul(self.D,u)


class Integrator():
    def forwardEuler(x, x_1, h):
        return torch.div(x-x_1, h)