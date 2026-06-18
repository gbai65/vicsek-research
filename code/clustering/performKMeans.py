from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import pandas as pd
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

def metrics(X, labels, alg):
    sil = silhouette_score(X, labels)
    db = davies_bouldin_score(X, labels)
    ch = calinski_harabasz_score(X, labels)
    print("\n"+alg)
    print(f"Silhouette: {sil:.3f} (higher better, max 1)")
    print(f"Davies-Bouldin: {db:.3f} (lower better, min 0)")
    print(f"Calinski-Harabasz: {ch:.1f} (higher better)")
for i in range(1, 6):
    X = np.loadtxt(f'new_metrics/combined_metrics_trial{i}.txt', delimiter=',', usecols=range(3,6))
    df = pd.DataFrame(X)
    X = StandardScaler().fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=18)
    cluster_labels = kmeans.fit_predict(X)

    metrics(X, cluster_labels, f"KMeans Trial {i}")
    df[len(df.columns)] = cluster_labels

    df.to_csv(f'new_metrics/combined_labeled_metrics_trial{i}.csv', index=False)
    
    customMap = ListedColormap(['purple', 'orange', 'blue'])

    order, binder, susc, label = np.loadtxt(f'new_metrics/combined_labeled_metrics_trial{i}.csv', delimiter=',', unpack=True)
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(projection='3d')
    img = ax.scatter(order, binder, susc, c=label, cmap=customMap)
    plt.xlabel("Order Parameter ɸ")
    plt.ylabel("Binder Cumulant G")
    ax.set_zlabel('Susceptibility χ')
    ax.set_zlim(0, 0.04)
    plt.title(f"Classified Simulation Clusters - Trial {i}")
    plt.savefig(f"new_metrics/KMeansMetricDistTrial{i}.png")
    plt.close()