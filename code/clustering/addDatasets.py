import numpy as np
import pandas as pd
from scipy import stats

eta, rho, v0 = np.loadtxt('new_metrics/overall_metrics_trial1.txt', delimiter=',', usecols=range(0, 3), unpack=True)

orders, binders, susceps, labels = [], [], [], []
for i in range(1, 6):
    o, b, s, l = np.loadtxt(f'new_metrics/labeled_metrics_trial{i}.csv', delimiter=',', unpack=True)
    orders.append(o)
    binders.append(b)
    susceps.append(s)
    labels.append(l)

avgOrder = np.mean(orders, axis=0)
avgBinder = np.mean(binders, axis=0)
avgSuscep = np.mean(susceps, axis=0)
domLabel = stats.mode(labels, axis=0).mode

df1 = pd.DataFrame({'eta': eta, 'rho': rho, 'v0': v0, 'label': domLabel})
df1.to_csv('new_metrics/labeledDataset.csv', index=False)

df2 = pd.DataFrame({
    'eta': eta, 'rho': rho, 'v0': v0, 
    'avgOrder': avgOrder, 'avgBinder': avgBinder, 
    'avgSuscep': avgSuscep, 'label': domLabel
})
df2.to_csv('new_metrics/fullDataset.csv', index=False)
