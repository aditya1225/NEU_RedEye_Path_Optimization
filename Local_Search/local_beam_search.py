import random
from config import API_KEY_3 as key
from Local_Search.objective_function import objective

def generate_neighbors(solution):
    """Generate all possible neighbors by swapping middle points"""
    neighbors = []
    available_indices = list(range(1, len(solution) - 1))

    for i in available_indices:
        for j in available_indices:
            if i < j:
                neighbor = solution.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)
    return neighbors

def local_beam_search(waypoints, k=5, max_iterations=20):
    """
    Local Beam Search for TSP: finds a tour visiting all waypoints.
    :param waypoints: List of waypoints including start and end points (start = end for TSP)
    :param k: Number of beams (solutions) to maintain
    :param max_iterations: Maximum number of iterations to prevent infinite loops
    :return: List of waypoints visiting all points
    """
    # Initialize beam with k copies of initial solution
    beam = [waypoints.copy() for _ in range(k)]
    best_solution = waypoints.copy()
    best_distance = objective(best_solution, key)
    available_indices = list(range(1, len(waypoints) - 1))

    for _ in range(max_iterations):
        #print("Iteration: ", _)
        all_neighbors = []
        for candidate in beam:
            for _ in range(3):
                neighbor = candidate.copy()
                i, j = random.sample(available_indices, 2)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                all_neighbors.append(neighbor)

        # Evaluate all neighbors
        evaluated = [(neighbor, objective(neighbor, key)) for neighbor in all_neighbors]

        # Sort neighbors by distance
        sorted_neighbors = sorted(evaluated, key=lambda x: x[1])

        # Update best solution
        current_best = sorted_neighbors[0]
        if current_best[1] < best_distance:
            best_solution = current_best[0]
            best_distance = current_best[1]

        # Select top k neighbors for next beam
        beam = [n[0] for n in sorted_neighbors[:k]]

    return best_solution
