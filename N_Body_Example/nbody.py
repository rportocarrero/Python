import scipy as sci
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import numpy

#gravitational constant
G = 6.67408e-11

#Reference quantities
m_nd = 1.989e+30 # sun mass
r_nd = 5.326e+12
v_nd = 30000 # velocity of earth
t_nd = 79.91 * 365 * 24 * 3600 * 0.51

# net constants
K1 = G*t_nd*m_nd/(r_nd**2 * v_nd)
K2 = v_nd * t_nd / r_nd

# masses
m1 = 1.1
m2 = 0.907

# define initial position
r1 = [-0.5, 0, 0]
r2 = [0.5, 0, 0]

r1=numpy.array(r1, dtype="float64")
r2 = numpy.array(r2, dtype="float64")

# center of mass
r_com = (m1*r1 + m2 * r2) / (m1 + m2)

# initial velocities
v1=[0.01, 0.01, 0]
v2 = [-0.05, 0, -0.1]

v1 = numpy.array(v1, dtype="float64")
v2 = numpy.array(v2, dtype="float64")

# velocity of com
v_com = (m1 * v1 + m2 * v2) / (m1 + m2)

def TwoBodyEquations(w, t, G, m1, m2):
    r1 = w[:3]
    r2 = w[3:6]
    v1 = w[6:9]
    v2 = w[9:12]

    r = sci.linalg.norm(r2-r1)

    dv1bydt = K1 * m2 * (r2-r1) / r ** 3
    dv2bydt = K1 * m1 * (r1-r2) / r ** 3
    dr1bydt = K2 * v1
    dr2bydt = K2 * v2

    r_derivs = numpy.concatenate((dr1bydt, dr2bydt))
    derivs = numpy.concatenate((r_derivs, dv1bydt, dv2bydt))
    return derivs

# initial parameters
init_params = numpy.array([r1, r2, v1, v2])
init_params=init_params.flatten()
time_span = numpy.linspace(0, 8, 500)

# run ODE solver
import scipy.integrate

two_body_sol = sci.integrate.odeint(TwoBodyEquations, init_params, time_span, args=(G, m1, m2))

r1_sol = two_body_sol[:,:3]
r2_sol = two_body_sol[:,3:6]


# create figure
fig = plt.figure(figsize = (15,15))

# ceate axis
ax = fig.add_subplot(111, projection="3d")

# plot the orbits
ax.plot(r1_sol[:,0], r1_sol[:,1], r1_sol[:,2], color="darkblue")
ax.plot(r2_sol[:,0], r2_sol[:,1], r2_sol[:,2], color="tab:red")

# plot final positions
ax.scatter(r1_sol[-1,0], r1_sol[-1,1], r1_sol[-1,2], color="darkblue", marker="o", s=100, label="Alpha Centauri A")
ax.scatter(r2_sol[-1,0], r2_sol[-1,1], r2_sol[-1,2], color="tab:red", marker="o", s=100, label="Alpha Centauri B")

# Add a few more bells and whistles
ax.set_xlabel("x-coordinate", fontsize=14)
ax.set_ylabel("y-coordinate", fontsize=14)
ax.set_zlabel("z-coordinate", fontsize=14)
ax.set_title("Visualization of obrits of stars in a two-body system\n", fontsize=14)
ax.legend(loc="upper left", fontsize=14)

plt.show()
