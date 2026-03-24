import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('LHSpoints.txt')
labels = ['Noise', 'Density', 'Speed']

fig, axs = plt.subplots(3, 3, figsize=(10, 10))

for i in range(3):
    for j in range(3):
        ax = axs[i, j]
        ax.scatter(data[:, j], data[:, i], marker='o', s=10, edgecolors='black')
        ax.set_xlabel(labels[j])
        ax.set_ylabel(labels[i])

        if i == j:
            ax.set_title(f'Self-pair: {labels[i]}')

fig.tight_layout(pad=3.0, w_pad=0.5, h_pad=2.0)
plt.savefig('latinSlices.png')
