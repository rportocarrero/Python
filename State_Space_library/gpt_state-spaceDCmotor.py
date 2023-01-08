import numpy as np

def rk4(f, x0, t):
    # RK4 integration
    n = len(t)
    x = np.zeros((n, len(x0)))
    x[0,:] = x0
    for i in range(n-1):
        h = t[i+1] - t[i]
        k1 = h*f(x[i,:], t[i])
        k2 = h*f(x[i,:] + 0.5*k1, t[i] + 0.5*h)
        k3 = h*f(x[i,:] + 0.5*k2, t[i] + 0.5*h)
        k4 = h*f(x[i,:] + k3, t[i+1])
        x[i+1,:] = x[i,:] + (k1 + 2*k2 + 2*k3 + k4)/6
    return x

def motor_dynamics(x, t):
    # State-space dynamics for DC motor
    J = 0.01  # inertia
    b = 0.1   # damping
    K = 0.01  # motor constant
    R = 1.0   # resistance
    L = 0.5   # inductance
    u = 1.0   # input voltage
    dx = np.zeros(2)
    dx[0] = x[1]
    dx[1] = -b/J*x[1] - K/J*x[0] + u/J
    return dx

# Initial state
x0 = [0, 0]

# Time points for integration
t = np.linspace(0,30, 1000)

# Integrate the state-space dynamics
x = rk4(motor_dynamics, x0, t)

# Extract the angular position and velocity from the state vector
theta = x[:,0]
omega = x[:,1]

# Plot the results
import matplotlib.pyplot as plt
plt.plot(t, omega)
plt.xlabel('Time (s)')
plt.ylabel('Angular velocity (rad/s)')
plt.show()