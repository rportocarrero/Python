from math import *
from random import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def genWing(a):
    span = random()
    rle = [0,0]
    tle = [span, random()]
    rte = [0, random()]
    tte = [span, uniform(0,rte[1])+tle[1]]
    
    return (rle*a), tle*a, tte*a, rte*a

wing = genWing(100)
offset = random()
tail = genWing(50)

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')

x = [tail[0][0], tail[1][0], tail[2][0], tail[3][0]]
y = [tail[0][1], tail[1][1], tail[2][1], tail[3][1]]

for n in range(0,4):
    y[n] += offset

ax.add_patch(patches.Polygon(xy=list(zip(x,y)), fill=False))

# Trapez
x = [wing[0][0], wing[1][0], wing[2][0], wing[3][0]]
y = [wing[0][1], wing[1][1], wing[2][1], wing[3][1]]
ax.add_patch(patches.Polygon(xy=list(zip(x,y)), fill=False))

plt.autoscale(enable=True, axis='both', tight=None)
plt.show()
