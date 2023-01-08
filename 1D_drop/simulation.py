import math
import matplotlib.pyplot as plt

rho = 1.225
c_d = 0.5
m = 0.2# kg (softball)
g = 9.8 #m/s^2

A = (math.pi*0.044**2) # cross-sectional area of a softball
b = (rho * c_d * A)/2 # constant for aerodynamic drag

def acceleration(v): 
    return ((b * v ** 2)/m - g)
  
# forward euler method
def forward_Euler(function, v, ts):
	return v + ts * function(v)

#second-order runge kutta method
def RK2(function, v,ts):
    f1 = function(v)
    f2 = function(v+ts/2*f1)
    return v + dt * f2

# set up simulation
t_0 = 0
t_n = 15 # 10 second simulation
dt = 0.01 # 1 hundreth of a second timestep

v_0 = 0 # initial velocity

T = [t_0]  # output time
V = [v_0]  # output velocity
V_rk = [v_0] # runge-kutta method
diff = [0] # differences between integrators

# run simulation timesteps
for t in range(int((t_n-t_0)/dt)):
    v = V[t]
    v_fe = forward_Euler(acceleration,v,dt)
    v_rk = RK2(acceleration,v,dt)
    T.append(T[t]+dt)
    V.append(v_fe)
    V_rk.append(v_rk)
    diff.append(v_rk-v_fe)

# plot velocity 
def plot_euler_rk2():
    plt.figure(1)
    plt.plot(T,V)
    #plt.plot(T, V_rk)
    plt.title("Velocity")
    plt.xlabel("Time")
    plt.ylabel("Velocity")
    plt.show()


# plot integrator differences
def plot_rk2_euler_err():
    plt.figure(2)
    plt.plot(T,diff)
    plt.title("Integrator Difference")
    plt.xlabel("Time")
    plt.ylabel("RK4 - Forwad Euler")
    plt.show()

plot_euler_rk2()
plot_rk2_euler_err()
