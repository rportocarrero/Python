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
for i in range (n_numbers):
    send_message.append(i)

if rank == 0:
    MPI.COMM_WORLD.send(send_message, dest=1, tag=0)

if rank == 1: 
    recv_message = MPI.COMM_WORLD.recv(source = 0, tag = 0)
    print("Message received by rank", rank)

if rank == 1:
    MPI.COMM_WORLD.send(send_message, dest=0, tag=0)

if rank == 0:
    recv_message = MPI.COMM_WORLD.recv(source=1, tag=0)
    print("Message received by rank", rank)