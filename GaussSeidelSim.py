import torch

class GaussSeidel():
    def __init__(self,rows, cols,ts):
        # grid dimensions
        self.cols = cols
        self.rows =  rows
        self.DT = ts # timestep
        self.G = -9.8 # gravity constant

        # test for invalid dimensions
        if (rows < 1 or cols < 1):
            raise ValueError("domain must have dimensions larger than 0")

        #initialize domain
        self.u = torch.zeros(self.rows, self.cols+1)
        self.v = torch.zeros(self.rows+1, self.cols)
        self.s = torch.ones(self.rows, self.cols)
        self.p = torch.zeros(self.rows, self.cols)

    # Add the gravity vector to the domain velocities.
    def gravity_update(self):
        self.v = self.v+self.DT*self.G
    
    # calculate the divergence for each cell
    def next_iteration(self):
        for i in range(1,self.cols-2):
            for j in range(1,self.rows-2):
                d = self.u[i+1,j]-self.u[i,j]+self.u[i,j+1]-self.v[i,j]
                s = self.s[i+1,j]+self.s[i-1,j]+self.s[i,j+1]+self.s[i,j-1]
                if(d!=0):
                    self.u_new[i,j] = self.u[i,j] + d/s
                    self.u_new[i+1,j] = self.u[i+1,j] - d/s
                    self.v_new[i,j] = self.v[i,j] + d/s
                    self.v_new[i,j+1] = self.v[i,j+1] - d/s

        #update velocity field

        #set boundary conditions equal to domain.
        self.u[0,:] = self.u[1,:]
        self.u[self.rows-1,:] = self.u[self.rows-2,:]
        self.u[:,self.cols-1] = self.u[:,self.cols-2]

        self.v[0,:] = self.v[1,:]
        self.v[self.rows-1,:] = self.v[self.rows-2,:]
        self.v[:,self.cols-1] = self.v[:,self.cols-2]


    # set uniform inlet velocity
    def set_inlet(self,v):
        for i in range(self.rows):
            self.u[i,0] = v

    # run the simulation
    def run(self,n):
        self.gravity_update()
        for i in range(n):
            self.next_iteration()

        