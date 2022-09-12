import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from FlowPy import *

# spatial and temporal inputs
length = 4
breadth = 4
colpts = 257
rowpts = 257

# create an object of the class Space called cavity
cavity = Space()
cavity.CreateMesh(rowpts, colpts)
cavity.SetDeltas(breadth, length)

# fluid properties
rho = 1
mu = 0.01

# create a water object of the fluid class
water = Fluid(rho, mu)

# boundary specifications
u_in = 1
v_wall = 0
p_out = 0

# create boundary with dirichlet or neumann type boundaries
flow = Boundary("D", u_in)
noslip = Boundary("D", v_wall)
zeroflux = Boundary("N", 0)
pressureatm = Boundary("D", p_out)

# simulation parameters
time = 150
CFL_number = 0.8
file_flag = 1
interval = 100

# RUN Simulation

print("Beginning simulation...")
print("# Simulation Time: {0:.2f}".format(time))
print("# Mesh: {0} x {1}".format(colpts, rowpts))
print("# Re/u: {0:.2f}\tRe/v:{1:.2f}".format(rho*length/mu, rho*breadth/mu))
print("# save output s to text file: {0}".format(bool(file_flag)))

# initialize results directory
MakeResultDirectory(wipe=True)

# initialize counters
t = 0
i = 0

# run
while(t<time):
    # print time remaining
    sys.stdout.write("\rSimulation time left: {0:.2f}".format(time-t))
    sys.stdout.flush()

    # ste the time-step
    SetTimeStep(CFL_number, cavity, water)
    timestep = cavity.dt

    # set the boundary conditions
    SetUBoundary(cavity, noslip, noslip, flow, noslip)
    SetVBoundary(cavity, noslip, noslip, noslip, noslip)
    SetPBoundary(cavity, zeroflux, zeroflux, pressureatm, zeroflux)

    # calculate satrred velocities
    GetStarredVelocities(cavity ,water)

    # Solve the pressure poisson
    SolvePressurePoisson(cavity, water, zeroflux, zeroflux, pressureatm, zeroflux)

    # solve the momentum equation
    SolveMomentumEquation(cavity, water)

    # save variables and write to file
    SetCenterPUV(cavity)
    if(file_flag == 1):
        WriteToFile(cavity, i, interval)

    #Advance time step and dounter
    t += timestep
    i += 1
