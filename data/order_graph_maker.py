import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0.0, 2.0, 0.01)
y = 1 + np.sin(2 * np.pi * x)

fig, ax = plt.subplots()

ax.plot(x, y)

ax.set(xlabel='Time (steps)', ylabel='Order ɸ',
       title='A Simple Matplotlib Line Graph')
ax.grid()

plt.show()
