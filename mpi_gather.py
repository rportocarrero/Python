from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()
n_ranks = MPI.COMM_WORLD.Get_size()

send_message = "Hello world, I'm rank {:d}".format(rank)
receive_message = MPI.COMM_WORLD.gather(send_message, root=0)

if rank == 0:
    for i in range(n_ranks):
        print(receive_message[i])
        