import matplotlib.pyplot as plt
import numpy as np

dataFile = '../data/eta_0.0/order.txt'

data = np.genfromtxt(dataFile, skip_header = 2, usecols = 2, delimiter = ',', dtype=str, comments='@')

x = data.astype(float)

x_4 = x**4
x_2 = x**2

binderCum = 1 - (np.sum(x_4)/(3*np.sum(x_2)**2))
print(binderCum)
