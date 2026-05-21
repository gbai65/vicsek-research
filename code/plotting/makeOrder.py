import matplotlib.pyplot as plt
import numpy as np

dataFile = 'py_temp_logs/order.txt'

data = np.genfromtxt(dataFile, skip_header = 2, usecols = (0, 2), delimiter = ',', dtype=str, comments='@')

x = np.char.replace(data[:, 0], '#', '')
x = x.astype(int)
y = data[:, 1].astype(float)

plt.figure(figsize=(8, 5))
plt.plot(x, y, linestyle='-', color='c')
plt.xlabel('Time (steps)')
plt.ylabel('Order Parameter ɸ')
plt.title('Order vs. Time')
plt.ylim(0, 1)
plt.grid(True)
plt.show()
