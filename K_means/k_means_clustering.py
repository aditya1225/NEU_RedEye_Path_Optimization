import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict
from pathlib import Path
import json


def return_clusters(number_of_clusters):
    with open('../locations.json', 'r') as f:
        locations = json.load(f)

    X = np.array(locations)
    n = len(X)
    m = number_of_clusters

    kmeans = KMeans(n_clusters=m, random_state=0, n_init=10)
    kmeans.fit(X)
    initial_centroids = kmeans.cluster_centers_

    base_size = n // m
    remainder = n % m
    cluster_sizes = [base_size + 1 if i < remainder else base_size for i in range(m)]

    point_data = []
    for i, point in enumerate(X):
        dists = [np.linalg.norm(point - c) for c in initial_centroids]
        sorted_clusters = np.argsort(dists)
        point_data.append((min(dists), i, sorted_clusters))

    point_data.sort(key=lambda x: x[0])

    clusters = [[] for _ in range(m)]
    remaining = cluster_sizes.copy()

    for _, idx, cluster_order in point_data:
        for cluster_idx in cluster_order:
            if remaining[cluster_idx] > 0:
                clusters[cluster_idx].append(idx)
                remaining[cluster_idx] -= 1
                break

    labels = np.zeros(n, dtype=int)
    balanced_centroids = []

    for cluster_idx, point_indices in enumerate(clusters):
        for pi in point_indices:
            labels[pi] = cluster_idx
        cluster_points = X[point_indices]
        balanced_centroids.append(cluster_points.mean(axis=0))


    res = defaultdict(list)
    for i, point in enumerate(X):
        res[labels[i]].append(point)

    for key in res.keys():
        # with open(f"../locations_{key}.json", 'w') as f:
        output_path = Path(__file__).parent / f"../locations_{key}.json"
        with output_path.open("w") as f:
            json.dump(res[key], f, default=lambda x: x.tolist())

if __name__ == "__main__":
    return_clusters(3)