import random
import pandas as pd
from config import API_KEY as key
from Local_Search.objective_function import objective

def hillClimbing(waypoints, max_iterations=100):
    """
    Hill Climbing algorithm for TSP: finds a tour visiting all waypoints.
    :param waypoints: List of waypoints including start and end points (start = end for TSP)
    :param max_iterations: Maximum number of iterations to prevent infinite loops
    :return: List of waypoints visiting all points
    """
    best = waypoints.copy()
    min_dist = objective(best, key)
    iterations_without_improvement = 0
    available_indices = list(range(1, len(waypoints)-1))

    for _ in range(max_iterations):
        #print(f"Iteration : {_}")
        neighbor = best.copy()
        if len(available_indices) >= 2:
            i, j = random.sample(available_indices, 2)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbor_dist = objective(neighbor, key)
            if neighbor_dist < min_dist:
                best = neighbor
                min_dist = neighbor_dist
                iterations_without_improvement = 0
            else:
                iterations_without_improvement += 1

        if iterations_without_improvement >= 10:
            break
    return best
