from mpi4py import MPI
import sys

n_numbers = 10000

rank = MPI.COMM_WORLD.Get_rank()
n_ranks = MPI.COMM_WORLD.Get_size()

if n_ranks != 2:
    print("This example requires exactly two ranks")
    sys.exit(1)

if rank == 0:
    neighbour = 1
else:
    neighbour = 0

send_message = []
for i in range(n_numbers):
    send_message.append(i)

req = MPI.COMM_WORLD.isend(send_message, dest=neighbour, tag=0)

req = MPI.COMM_WORLD.irecv(source=neighbour, tag=0)
recv_message = req.wait()
print("Message received by rank", rank)
