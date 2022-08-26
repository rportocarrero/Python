from cmath import isinf
import numpy as np
import os

class Boundary:
    def __init__(self, boundary_type, boundary_value):
        self.DefineBoundary(boundary_type, boundary_value)

    def DefineBoundary(self, boundary_type, boundary_value):
        self.type = boundary_type
        self.value = boundary_value

class Space:
    def __init__(self):
        pass

    def CreateMesh(self, rowpts, colpts):
        #gridpoints
        self.rowpts = rowpts
        self.colpts = colpts

        #velocity matrices
        self.u = np.zeros((self.rowpts+2, self.colpts+2))
        self.v = np.zeros((self.rowpts+2, self.colpts+2))
        self.u_star = np.zeros((self.rowpts+2, self.colpts+2))
        self.v_star = np.zeros((self.rowpts+2, self.colpts+2))
        self.u_next = np.zeros((self.rowpts+2, self.colpts+2))
        self.v_next = np.zeros((self.rowpts+2, self.colpts+2))
        self.u_c = np.zeros((self.rowpts+2, self.colpts+2))
        self.v_c = np.zeros((self.rowpts+2, self.colpts+2))

        #Pressure matrices
        self.p = np.zeros((self.rowpts+2, self.colpts+2))
        self.p_c = np.zeros((self.rowpts+2, self.colpts+2))

        #Set default source term
        self.SetSourceTerm()

    def SetDeltas(self,breadth, length):
        self.dx = length/(self.colpts-1)
        self.dy = breadth/(self.rowpts-1)

    def SetInitialU(self, U):
        self.u = U*self.u

    def SetInitialV(self, V):
        self.v = V*self.v

    def SetInitialP(self, P):
        self.p=P*self.p

    def SetSourceTerm(self, S_x=0, S_y=0):
        self.S_x = S_x
        self.S_y = S_y

class Fluid:
    def __init__(self, rho, mu):
        self.SetFluidProperties(rho, mu)

    def SetFluidProperties(self, rho ,mu):
        self.rho = rho
        self.mu = mu

# Set boundary conditions for horizontal velocity
def SetUBoundary(space, left, right, top, bottom):
    if(left.type == "D"):
        space.u[:,0] = left.value
    elif(left.type == "N"):
        space.u[:,0] = - left.value * space.dx = space.u[:,1]

    if(right.type == "D"):
        space.u[:,-1] = right.value
    elif(right.type == "N"):
        space.u[:,-1] = right.value * space.dx + space.u[:,-2]

    if(top.type == "D"):
        space.v[-1,:] = 2 * right.value - space.v[:,-2]
    elif(top.type == "N"):
        space.v[-1,:] = - top.value * space.dy + space.v[-2,:]

    if(bottom.type == "D"):
        space.v[0,:] = bottom.value
    elif(bottom.type == "N"):
        space.v[0,:] = bottom.value * space.dy + space.v[1,:]

# Set boundary conditions for pressure
def SetPBoundary(space, left, right, top, bottom):
    if(left.type == "D"):
        space.p[:,0] = left.value
    elif(left.type == "N"):
        space.p[:,0] = - left.value * space.dx + space.p[:,1]

    if(right.type == "D"):
        space.p[1, -1] = right.value
    elif(right.type == "N"):
        space.p[:,-1] = right.value * space.dx + space.p[:,-2]

    if(top.type == "D"):
        space.p[-1, :] = top.value
    elif(top.type == "N"):
        space.p[-1,:] = - top.value * space.dy + space.p[-2,:]

    if(bottom.type == "D"):
        space.p[0,:] = bottom.value
    elif(bottom.type == "N"):
        space.p[0,:] = bottom.value * space.dy + space.p[1,:]

def SetTimesStep(CFL, space, fluid):
    with np.errstate(divide = 'ignore'):
        dt = CFL / np.sum([np.amaz(space.v) / space.dx, np.amax(space.v) / space.dy])

    # Escape condition if dt is infinity
    if np.isinf(dt):
        dt = CFL * (space.dx + space.dy)
    space.dt = dt

def GetStarredVelocities(space, fluid):
    #Save object attributes as local v ariable with explicit typing
    rows = int(space.rowpts)
    cols = int(space.colpts)
    u = space.u.astype(float, copy=False)
    v = space.v.astype(float, copy=False)
    dx = float(space.dx)
    dy = float(space.dy)
    dt = float(space.dt)
    S_x = float(space.S_x)
    S_y = float(space.S_y)
    rho = float(fluid.rho)
    mu = float(fluid.mu)

    # copy new variables
    u_star = u.copy()
    v_star = v.copy()

    u1_y = (u[2:, 1:cols+1] - u[0:rows, 1:cols+1]) / (2*dy)
    u1_x = (u[1:rows+1, 2:] - u[1:rows+1, 0:cols]) / (2*dx)
    u2_y = (u[2:, 1:cols+1] - 2 * u[1:rows+1, 1:cols+1] + u[0:rows, 1:cols+1]) /(dy**2)
    u2_x = (u[1:rows+1, 2:] - 2 * u[1:rows+1, 1:cols+1] + u[1:rows+1, 0:cols]) /(dx**2)
    