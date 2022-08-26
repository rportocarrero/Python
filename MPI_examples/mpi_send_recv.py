from mpi4py import MPI

n_ranks = MPI.COMM_WORLD.Get_size()

rank = MPI.COMM_WORLD.Get_rank()

if rank % 2 == 1:
    my_pair = rank - 1
else:
    my_pair = rank + 1

if my_pair < n_ranks:
    if rank % 2 == 0:
        message = "Hello World!"
        MPI.COMM_WORLD.send(message, dest=my_pair, tag=0)
    if rank % 2 == 1:
        message = MPI.COMM_WORLD.recv(source=my_pair, tag=0)
        print(message)

