import random
import pandas as pd
import json
from config import API_KEY as key
from Local_Search.objective_function import objective
from Route_maps_generation.generate_routemap_multiple import route_generator
from Route_maps_generation.get_address_from_lat_long import get_address_from_lat_long
from Parameters.get_commute_time_without_traffic import get_commute_time_for_multiple_points

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

# if __name__ == "__main__":
#     dataset_path = "../Locations_dataset/House_locations_dataset_with_coordinates.csv"
#
#     df = pd.read_csv("../Locations_dataset/House_locations_dataset_with_coordinates.csv", header=None)
#     waypoints = [[-71.08811,42.33862]]
#     with open("../locations_0.json", "r") as file:
#         waypoints.extend(json.load(file))
#
#     waypoints.append([-71.08811,42.33862])
#     best_order = hillClimbing(
#         waypoints=waypoints,
#         max_iterations=100
#     )
#
#     print("Best order of waypoints found by Hill Climbing:")
#     route_generator(best_order, 'Hill Climbing-2')
#     for coord in best_order:
#         print(get_address_from_lat_long(coord))
#
#     print(f"Total route length: {objective(best_order, key)} miles")
#     print(f"Total commute time: {get_commute_time_for_multiple_points(best_order)} minutes")