import random
import math
import pandas as pd
import json

from Parameters.get_commute_time_without_traffic import get_commute_time_for_multiple_points
from Route_maps_generation.generate_routemap_multiple import route_generator
from Route_maps_generation.get_address_from_lat_long import get_address_from_lat_long
from Local_Search.objective_function import objective
from config import API_KEY_2 as key

def simulated_annealing(locations_0,
                        max_iterations=100,
                        initial_temp=1000.0,
                        alpha=0.8):
    """
    Performs a simulated annealing search to minimize the distance of a route.

    Parameters:
    -----------
    locations_0 : list of [lon, lat]
        The list of coordinates representing the route to be optimized.
    max_iterations : int
        Maximum number of iterations to run the annealing process.
    initial_temp : float
        The starting temperature for annealing.
    alpha : float
        The cooling rate (each iteration temperature = temperature * alpha).

    Returns:
    --------
    best_solution : list of [lon, lat]
        The best found ordering of locations_0.
    """
    # Current solution
    current_solution = locations_0.copy()
    current_distance = objective(current_solution, key)

    # Best solution found
    best_solution = current_solution
    best_distance = current_distance

    # Initialize temperature
    temperature = initial_temp

    available_indices = list(range(1, len(locations_0) - 1))

    for iteration in range(max_iterations):
        #print('Iteration:', iteration)
        # Generate a neighbor solution by swapping two random locations_0
        neighbor = current_solution.copy()
        i, j = random.sample(available_indices, 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbor_distance = objective(neighbor, key)

        # Calculate the difference in cost (distance)
        delta = neighbor_distance - current_distance

        # If the neighbor is better, accept it
        if delta < 0:
            current_solution = neighbor
            current_distance = neighbor_distance

            # Update the best solution if improved
            if neighbor_distance < best_distance:
                best_solution = neighbor
                best_distance = neighbor_distance
        else:
            # If the neighbor is worse, accept it with a probability based on the temperature
            acceptance_prob = math.exp(-delta / temperature)
            if random.random() < acceptance_prob:
                current_solution = neighbor
                current_distance = neighbor_distance

        # Cool down the temperature
        temperature *= alpha

    return best_solution


# if __name__ == "__main__":
#
#     dataset_path = "../Locations_dataset/House_locations_dataset_with_coordinates.csv"
#
#
#
#     df = pd.read_csv("../Locations_dataset/House_locations_dataset_with_coordinates.csv", header=None)
#     locations_0=[[-71.08811,42.33862]]
#     with open("../locations_0.json", "r") as file:
#         locations_0.extend(json.load(file))
#     locations_0.append([-71.08811,42.33862])
#
#
#
#     best_order = simulated_annealing(
#         locations_0=locations_0,
#         max_iterations=1000,
#         initial_temp=10000.0,
#         alpha=0.99
#     )
#
#     # Print or process the best route found
#     print("Best order of locations_0 found by Simulated Annealing:")
#     route_generator(best_order,'Simulated Annealing')
#     for coord in best_order:
#         print(get_address_from_lat_long(coord))
#     print(f"Best distance : {objective(best_order, key)} miles")
#     print(f"Total commute time: {get_commute_time_for_multiple_points(best_order)} ")
