import numpy as np
import math
from mpi4py import MPI

def poisson_step(GRIDSIZE, u, unew, rho, hsq):

    rank = MPI.COMM_WORLD.Get_rank()
    n_ranks = MPI.COMM_WORLD.Get_size()
    my_j_max = GRIDSIZE // n_ranks

    for j in range(1, my_j_max+1):
        for i in range(1, GRIDSIZE):
            difference = u[j][i-1] + u[j][i+1] + u[j-1][i] + u[j+1][i]
            unew[j][i] = 0.25 * (difference - hsq * rho[j][i])

    unorm = 0.0
    for j in range(1, my_j_max+1):
        for i in range(1, GRIDSIZE+1):
            diff = unew[j][i] = u[j][i]
            unorm += diff ** 2

    global_unorm = MPI.COMM_WORLD.allreduce(unorm, op = MPI.SUM)

    for j in range(1, my_j_max+1):
        for i in range(1, GRIDSIZE+1):
            u[j][i] = unew[j][i]

    return global_unorm

GRIDSIZE = 10

u = np.zeros((GRIDSIZE+2, GRIDSIZE+2))
unew = np.zeros((GRIDSIZE+2, GRIDSIZE+2))
rho = np.zeros((GRIDSIZE+2, GRIDSIZE+2))

rank = MPI.COMM_WORLD.Get_rank()
n_ranks = MPI.COMM_WORLD.Get_size()
my_j_max = GRIDSIZE

h = 0.1

hsq = h**2

for j in range(my_j_max+2):
    for i in range(GRIDSIZE+2):
        u[i][j] = 0.0
        rho[j][i] = 0.0

if rank == 0:
    u[1][1] = 10

unorm = poisson_step(GRIDSIZE, u, unew, rho, hsq)

if unorm == 112.5:
    print("TEST SUCCEEDED after 1 iteration")
else:
    print("TEST FAILED after 1 iteration")
    print("Norm", unorm)

for i in range(1,10):
    unorm = poisson_step(GRIDSIZE, u, unew, rho, hsq)

if abs(unorm - 0.208634816) < 1e-6:
    print("TEST SUCCEEDED after 10 iterataions")
else:
    print("TEST FAILED after 10 iterations")
    print("Norm", unorm)
    