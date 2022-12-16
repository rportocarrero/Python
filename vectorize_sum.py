from time import *
import numpy as np
import sys

N = int(sys.argv[1])
tot = 0
start = time()
for i in range(0, N):
    tot = tot + i

print(f"loop Sum is: {tot}")
end = time()
print(f"loop time: {end-start}")

# vectorized version
start = time()
tot = np.sum(np.arange(N))
print(f"vectorized sum:{tot}")
end = time()
print(f"vectorized time: {end-start}")
