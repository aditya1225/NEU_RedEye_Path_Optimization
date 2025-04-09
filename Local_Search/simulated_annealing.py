import random
import math
from Local_Search.objective_function import objective
from config import Sai_Api_Key as key

def simulated_annealing(locations_0, max_iterations=100, initial_temp=1000.0, alpha=0.8):
    """
    Simulated Annealing algorithm for TSP: finds a tour visiting all waypoints.
    :param locations_0: List of waypoints including start and end points (start = end for TSP)
    :param max_iterations: Maximum number of iterations to prevent infinite loops
    :param initial_temp: Initial temperature for the annealing schedule
    :param alpha: Cooling rate for the temperature
    :return: List of waypoints visiting all points
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
