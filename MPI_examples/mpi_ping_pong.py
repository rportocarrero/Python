from mpi4py import MPI

max_count = 1000000
ball = 1

rank = MPI.COMM_WORLD.Get_rank()

if rank == 0:
    neighbour = 1
else:
    neighbour = 0

if rank == 0:
    MPI.COMM_WORLD.send(ball, dest=1, tag=0)

counter = 0
bored = False
while not bored:
    ball = MPI.COMM_WORLD.recv(source=neighbour, tag=0)

    counter +=1
    MPI.COMM_WORLD.send(ball, dest=neighbour, tag=0)

    bored = (counter >= max_count)

print("Rank {:d} is bored and giving up.".format(rank))