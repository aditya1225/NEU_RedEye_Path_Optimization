import random
import openrouteservice
from config import API_KEY as key
def objective(waypoints):
    obj = 0
    client = openrouteservice.Client(key=f'{key}')
    route = client.directions(
        coordinates=waypoints,
        profile='driving-car',
        format='geojson'
    )
    distance_m = route["features"][0]["properties"]["segments"][0]["distance"]
    obj = obj + distance_m
    return obj

def hillClimbing(waypoints, max_iterations=100):
    best = waypoints.copy()
    min_dist = objective(best)
    iterations_without_improvement = 0
    for _ in range(max_iterations):
        neighbor = best.copy()
        i, j = random.sample(range(len(neighbor)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbor_dist = objective(neighbor)
        if neighbor_dist < min_dist:
            best = neighbor
            min_dist = neighbor_dist
            iterations_without_improvement = 0
        else:
            iterations_without_improvement += 1

        if iterations_without_improvement >= 10:
            break
    return best