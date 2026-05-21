from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

def metrics(X, labels, alg):
    sil = silhouette_score(X, labels)
    db = davies_bouldin_score(X, labels)
    ch = calinski_harabasz_score(X, labels)
    print("\n"+alg)
    print(f"Silhouette: {sil:.3f} (higher better, max 1)")
    print(f"Davies-Bouldin: {db:.3f} (lower better, min 0)")
    print(f"Calinski-Harabasz: {ch:.1f} (higher better)")

X = np.loadtxt('overall_metrics.txt', delimiter=',', usecols=range(3,6))
X = StandardScaler().fit_transform(X)

db = DBSCAN(eps=0.3, min_samples=6).fit(X)
labels = db.labels_
metrics(X, labels, "DBSCAN")

gmm = GaussianMixture(n_components=3, covariance_type='full', n_init=20, random_state=42)
gmm.fit(X)
cluster_labels = gmm.predict(X)
metrics(X, cluster_labels, "GMM")

for k in range(2, 4):
    kmeans = KMeans(n_clusters=k, random_state=42)
    cluster_labels = kmeans.fit_predict(X)
    metrics(X, cluster_labels, f"KMeans{k}")
