import numpy as np

# acceleration function
def acceleration(position, mass, length, gravity):
    x, y, z = position
    lambda_multiplier = gravity * z / length**2
    
    a_x = -2 * lambda_multiplier * x
    a_y = -2 * lambda_multiplier * y
    a_z = gravity - 2 * lambda_multiplier * z

    return np.array([a_x, a_y, a_z])

#  verlet integration function
def verlet(current, previous, dt, acceleration):
    return 2*current-previous+acceleration*dt**2

# Initial values
A=np.array([1,0.5,0])
print(A/np.linalg.norm(A))

P_current=A
P_prev=A
L=1
M=1
G=-9.81



# Time step
dt=0.01
end_time = 5
N=int(end_time/dt)

# Simulation
for i in range(N):
    P_next = verlet(P_current, P_prev, dt, acceleration(P_current, M, L, G))
    print(P_current)
    P_prev, P_current = P_current, P_next

