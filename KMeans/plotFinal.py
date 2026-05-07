import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt


eta, rho, v0, order, binder, suscep, label = np.loadtxt(f'fullDataset.csv', delimiter=',', unpack=True)

customMap = ListedColormap(['purple', 'orange', 'blue'])

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(projection='3d')
img = ax.scatter(eta, rho, v0, c=label, cmap=customMap)
plt.xlabel("Noise ɳ")
plt.ylabel("Density ρ")
ax.set_zlabel('Speed v0')

ax.view_init(elev=90, azim=-90)
plt.title(f"Visualized Averaged K-Means Results in (ɳ, ρ, v) space")
plt.savefig(f"visualizedTopResults1.png")
plt.close()

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(projection='3d')
img = ax.scatter(order, binder, suscep, c=label, cmap=customMap)
plt.xlabel("Order Parameter ɸ")
plt.ylabel("Binder Cumulant G")
ax.set_zlabel('Susceptibility χ')
ax.set_zlim(0, 0.04)

ax.view_init(elev=90, azim=-90)
plt.title(f"Visualized Averaged K-Means Results in (ɸ, G, χ) space")
plt.savefig(f"visualizedTopResults2.png")
plt.close()