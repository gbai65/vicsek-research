import matplotlib.pyplot as plt
import numpy as np


data = np.loadtxt('LHSpoints.txt')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for line in data:
    ax.plot(line[0], line[1], line[2], marker='o')

ax.set_xlabel('Noise')
ax.set_ylabel('Density')
ax.set_zlabel('Speed')
ax.set_title('3D visualization of LHS sampling')

plt.show()
