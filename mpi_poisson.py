import numpy as np
import math

def poisson_step(GRIDSIZE, u, unew, rho, hsq):

    for j in range(1, GRIDSIZE+1):
        for i in range(1, GRIDSIZE+1):
            difference = u[j][i-1] + u[j][i+1] + u[j-1][i] + u[j+1][i]
            unew[j][i] = 0.25*(difference - hsq*rho[j][i])

    unorm = 0.0
    for j in range(1, GRIDSIZE+1):
        for i in range(1, GRIDSIZE+1):
            diff = unew[j][i] - u[j][i]
            unorm += diff * diff

    for j in range(1, GRIDSIZE+1):
        for i in range(1, GRIDSIZE+1):
            u[j][i] = unew[j][i]

    return unorm

GRIDSIZE = 10

u = np.zeros((12, 12))
unew = np.zeros((12, 12))
rho = np.zeros((12, 12))

h = 0.1
hsq = h*h
residual = 1e-5

for j in range(1, GRIDSIZE+1):
        for i in range(1, GRIDSIZE+1):
            u[j][i] = 0.0
            rho[j][i] = 0.0

for j in range(1, GRIDSIZE+1):
        u[j][i] = 10.0

for i in range(10000):
    unorm = poisson_step(GRIDSIZE, u, unew, rho, hsq)
    print("Iteration {:d}: Residual {:g}".format(i, unorm))

    if math.sqrt(unorm) < math.sqrt(residual):
        break
print("Run completed with residual",unorm)