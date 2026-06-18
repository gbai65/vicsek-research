import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt


eta, rho, v0, label = np.loadtxt(f'fixedLabeledDataset.csv', delimiter=',', unpack=True)

customMap = ListedColormap(['purple', 'orange', 'blue'])

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(projection='3d')
img = ax.scatter(eta, rho, v0, c=label, cmap=customMap)
plt.xlabel("Noise ɳ")
plt.ylabel("Density ρ")
ax.set_zlabel('Speed v0')

ax.view_init(elev=90, azim=-90)
plt.title(f"Phase Diagram")
plt.savefig(f"phaseDiagramTop.png")
plt.close()

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(projection='3d')
img = ax.scatter(eta, rho, v0, c=label, cmap=customMap)
plt.xlabel("Noise ɳ")
plt.ylabel("Density ρ")
ax.set_zlabel('Speed v0')
plt.title(f"Phase Diagram")
plt.savefig(f"phaseDiagram.png")
plt.close()