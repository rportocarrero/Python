from mpi4py import MPI

def find_sum(vector):
    my_sum = 0.0
    for i in range(len(vector)):
        my_sum += vector[i]

    global_sum = MPI.COMM_WORLD.allreduce(my_sum, op=MPI.SUM)

    return global_sum

def find_maximum(vector):
    my_max = 0.0
    for i in range(len(vector)):
        if vector[i] > my_max:
            my_max = vector[i]

    global_max = MPI.COMM_WORLD.allreduce(my_max, op=MPI.SUM)

    return global_max

n_numbers = 1024

rank = MPI.COMM_WORLD.Get_rank()

my_first_number = n_numbers * rank

vector = []
for i in range(n_numbers):
    vector.append(float(my_first_number + i))

my_sum = find_sum(vector)
print("The sum of the numbers is", my_sum)

my_max = find_maximum(vector)
print("The largets number is", my_max)