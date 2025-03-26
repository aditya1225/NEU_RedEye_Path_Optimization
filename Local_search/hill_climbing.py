import random
import time
import pandas as pd
import openrouteservice
import json
from config import API_KEY as key
from objective_function import objective
from Route_maps_generation.generate_routemap_multiple import route_generator




def hillClimbing(waypoints, max_iterations=100):
    best = waypoints.copy()
    min_dist = objective(best)
    iterations_without_improvement = 0

    # Exclude first and last indices (Snell Library) from swapping
    available_indices = list(range(1, len(waypoints) - 1))

    for _ in range(max_iterations):
        time.sleep(2)
        neighbor = best.copy()
        # Ensure there are at least two middle points to swap
        if len(available_indices) >= 2:
            i, j = random.sample(available_indices, 2)
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


if __name__ == "__main__":
    dataset_path = "../Locations_dataset/House_locations_dataset_with_coordinates.csv"

    df = pd.read_csv("../Locations_dataset/House_locations_dataset_with_coordinates.csv", header=None)

    with open("../waypoints.json", "r") as file:
        waypoints = json.load(file)

    best_order = hillClimbing(
        waypoints=waypoints,
        max_iterations=100
    )

    print("Best order of waypoints found by Hill Climbing:")
    route_generator(best_order, 'Hill Climbing')
    for coord in best_order:
        print(coord)