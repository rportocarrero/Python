import numpy as np
import math
import matplotlib.pyplot as plt

# Diode Model
class Diode:
    def __init__(self,sat_curr,T,a):
        #sat_curr: saturation current
        #T: temperature in K
        #a: ideality factor
        K = 1.380649e-23 # Boltzmann constant
        q = 1.602e-19 # elemetary charge
        self.Is = sat_curr
        self.n= 2 # emission coefficient (2 for silicon)
        self.a = a
        self.C=q/(self.n*K*T*a)
        
    def I(self,v):
        return self.Is * (math.exp(self.C*v)-1)

# Visualize Diode IV Plot
def plot_IV(diode, neg_v, v):
    V = np.linspace(neg_v,v)
    I = list(map(diode.I,V))
    plt.ylim([-0.1,1])
    plt.xlabel("V")
    plt.ylabel("I")
    plt.plot(V,I)

