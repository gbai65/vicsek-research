import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

eta, rho, v0, order, binder, suscep = np.loadtxt('overall_metrics.txt', delimiter=',', unpack=True)

plt.figure()
sns.histplot(suscep, kde=True, bins=100, stat="density", color='blue', edgecolor='white')

plt.title('Susceptibility Distribution')
plt.xlabel('Susceptibility')
plt.ylabel('Frequency')
plt.savefig("suscepDistPlot.png")

plt.figure()
sns.histplot(order, kde=True, bins=100, stat="density", color='blue', edgecolor='white')

plt.title('Order Distribution')
plt.xlabel('Order')
plt.ylabel('Frequency')
plt.savefig("orderDistPlot.png")

plt.figure()
sns.histplot(binder, kde=True, bins=100, stat="density", color='blue', edgecolor='white')

plt.title('Binder Cumulant Distribution')
plt.xlabel('Binder Cumulant')
plt.ylabel('Frequency')
plt.savefig("binderDistPlot.png")
