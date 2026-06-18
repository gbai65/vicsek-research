import numpy as np
import matplotlib.pyplot as plt
for i in range(1, 6):
    order, binder, susc = np.loadtxt(f'overall_metrics_trial{i}.txt', delimiter=',', unpack=True, usecols=range(3,6))
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(projection='3d')
    img = ax.scatter(order, binder, susc)
    plt.xlabel("Order Parameter ɸ")
    plt.ylabel("Binder Cumulant G")
    ax.set_zlabel('Susceptibility χ')
    ax.set_zlim(0, 0.04)
    plt.title(f"Formed Simulation Clusters - Trial {i}")
    plt.savefig(f"metricDistTrial{i}.png")
    plt.close()