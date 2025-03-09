import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict


def return_clusters(waypoints, number_of_clusters):
    X = np.array(waypoints)
    n = len(X)
    m = number_of_clusters

    # Initial K-means to find centroids
    kmeans = KMeans(n_clusters=m, random_state=0, n_init=10)
    kmeans.fit(X)
    initial_centroids = kmeans.cluster_centers_

    # Calculate target cluster sizes
    base_size = n // m
    remainder = n % m
    cluster_sizes = [base_size + 1 if i < remainder else base_size for i in range(m)]

    # Prepare point assignments
    point_data = []
    for i, point in enumerate(X):
        dists = [np.linalg.norm(point - c) for c in initial_centroids]
        sorted_clusters = np.argsort(dists)
        point_data.append((min(dists), i, sorted_clusters))

    # Sort points by their proximity to nearest centroid
    point_data.sort(key=lambda x: x[0])

    # Distribute points evenly across clusters
    clusters = [[] for _ in range(m)]
    remaining = cluster_sizes.copy()

    for _, idx, cluster_order in point_data:
        for cluster_idx in cluster_order:
            if remaining[cluster_idx] > 0:
                clusters[cluster_idx].append(idx)
                remaining[cluster_idx] -= 1
                break

    # Create final labels and calculate new centroids
    labels = np.zeros(n, dtype=int)
    balanced_centroids = []

    for cluster_idx, point_indices in enumerate(clusters):
        for pi in point_indices:
            labels[pi] = cluster_idx
        cluster_points = X[point_indices]
        balanced_centroids.append(cluster_points.mean(axis=0))

    # Print results
    # print("Balanced Cluster Assignments:")
    # for i, point in enumerate(X):
    #     print(f"Point {i + 1}: {point} → Cluster {labels[i]}")

    res = defaultdict(list)
    for i, point in enumerate(X):
        res[labels[i]].append(point)


    return res

if __name__ == "__main__":
    waypoints = [[-71.08811, 42.33862], [-71.111504, 42.331211], [-71.08193, 42.326472], [-71.0964012, 42.3179773], [-71.1097564, 42.3330016], [-71.08628, 42.323179], [-71.108287, 42.331544], [-71.083486, 42.336311], [-71.083993, 42.336548], [-71.096476, 42.318023], [-71.109834, 42.332984], [-71.07458, 42.342381], [-71.090158, 42.342187], [-71.0742583, 42.3400459], [-71.1059822, 42.3330928], [-71.086572, 42.326477], [-71.0647906, 42.3456187], [-71.110153, 42.324272], [-71.1388971, 42.3005787], [-71.088022, 42.351494], [-71.08321, 42.33162], [-71.0786002, 42.3343545], [-71.0694371, 42.3231914], [-71.072526, 42.325599], [-71.1026905, 42.3224559], [-71.0720022, 42.3248608], [-71.0835138, 42.336362], [-71.104075, 42.3202273], [-71.103949, 42.346195], [-71.079928, 42.339777], [-71.1089212, 42.3331073], [-71.0799812, 42.3390315], [-71.0889463, 42.3292934], [-71.094373, 42.323232], [-71.0865851, 42.3263984], [-71.091277, 42.322489], [-71.08811, 42.33862]]
    return_clusters(waypoints, 3)