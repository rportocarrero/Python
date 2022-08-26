from mpi4py import MPI
import sys

numbers = 10

n_ranks = MPI.COMM_WORLD.Get_size()
if n_ranks < 2:
    print("This example requires at least two ranks")
    sys.exit(1)

rank = MPI.COMM_WORLD.Get_rank()

if rank == 0:
    message = "Hello, world!"
    req = MPI.COMM_WORLD.isend(message, dest=1, tag=0)

if rank == 1:
    req = MPI.COMM_WORLD.irecv(source=0, tag=0)
    message = req.wait()
    print(message)