import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# simulate inputs
rowpts = 257
colpts = 257
length = 4
breadth = 4

# go to results directory
cwdir = os.getcwd()
dir_path = os.path.join(cwdir, "Result")
os.chdir(dir_path)

# go through filenames and store filenames
filenames = []
iterations = []
for root, dirs, files in os.walk(dir_path):
    for datafile in files:
        if "PUV" in datafile:
            filenames.append(datafile)
            no_ext_file = datafile.replace(".txt", "").strip()
            iter_no = int(no_ext_file.split("V")[-1])
            iterations.append(iter_no)

# grab final iteration and interval
initial_iter = np.amin(iterations)
final_iter = np.amax(iterations)
inter = (final_iter - initial_iter) / (len(iterations)-1)
number_of_frames=len(iterations)
sorted_iterations=np.sort(iterations)

def read_datafile(iteration):
    # set filename and path
    filename = "PUV{0}.txt".format(iteration)
    filepath = os.path.join(dir_path, filename)

    # load text file as numpy array
    arr = np.loadtxt(filepath, delimiter ="\t")
    rows,cols = arr.shape

    # define empty array for pressure and velocities
    p_p = np.zeros((rowpts, colpts))
    u_p = np.zeros((rowpts, colpts))
    v_p = np.zeros((rowpts, colpts))

    # organize imported array into variables
    p_arr = arr[:,0]
    u_arr = arr[:,1]
    v_arr = arr[:,2]

    # reshape 1d data into 2d
    p_p = p_arr.reshape((rowpts, colpts))
    u_p = u_arr.reshape((rowpts, colpts))
    v_p = v_arr.reshape((rowpts, colpts))

    return p_p, u_p, v_p

# create mesh for x and y inputs
x = np.linspace(0, length, colpts)
y = np.linspace(0, breadth, rowpts)
[X, Y] = np.meshgrid(x, y)

# determinet indexing for stream plot
index_cut_x = int(colpts/10)
index_cut_y = int(rowpts/10)

# create blank figure
fig = plt.figure(figsize=(16,8))
ax = plt.axes(xlim=(0,length), ylim = (0,breadth))

# create initial contour and stream plot as well as color bar
p_p, u_p, v_p = read_datafile(0)
ax.set_xlim([0, length])
ax.set_ylim([0, breadth])
ax.set_xlabel("$x$", fontsize=12)
ax.set_ylabel("$y$", fontsize=12)
ax.set_title("Frame No: 0")
cont=ax.contour(X, Y, p_p)
stream = ax.streamplot(X[::index_cut_y, ::index_cut_x], Y[::index_cut_y, ::index_cut_x], u_p[::index_cut_y, ::index_cut_x], v_p[::index_cut_y, ::index_cut_x], color="k")
fig.colorbar(cont)
fig.tight_layout()

def animate(i):
    # print frames remaining
    sys.stdout.write("\rFrames remaining: {0.03d}".format(len(sorted_iterations)-i))
    sys.stdout.flush()

    # get ierations sequentially
    iteration = sorted_iterations[i]

    # use datfile to get pressure/vel
    p_p, u_p, v_p = read_datafile(iteration)

    # clear previous plot and make contour and stream plots for current timestep
    ax.clear()
    ax.set_xlim([0, length])
    ax.set_ylim([0, breadth])
    ax.set_xlabel("$x$",fontsize=12)
    ax.set_ylabel("$y$", fontsize=12)
    ax.set_title("Frame No: {0}".format(i))
    cont = ax.contour(X, Y, p_p)
    stream = ax.streamplot(X[::index_cut_y, ::index_cut_x], \
        Y[::index_cut_y, ::index_cut_x], \
        u_p[::index_cut_y,::index_cut_x], \
        v_p[::index_cut_y, ::index_cut_x], \
        color="k")

    return cont,stream

print("Making animation")
anim = animation.FuncAnimation(fig, animate, frames=number_of_frames, interval=50, blit=False)
movie_path = os.path.join(dir_path, "FluidFlowAnimation.mp4")
anim.save(r"{0}".format(movie_path))
print("\nAnimation saved as FluidFlowAnimation.mp4 in Results")