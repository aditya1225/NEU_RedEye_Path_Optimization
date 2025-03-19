import random
import json
import time
from Route_maps_generation.generate_routemap_multiple import route_generator
from objective_function import objective
from K_means.k_means_clustering import return_clusters


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
    """Local Beam Search implementation with fixed start/end points"""
    # Initialize beam with k copies of initial solution
    beam = [waypoints.copy() for _ in range(k)]
    best_solution = waypoints.copy()
    time.sleep(2)
    best_distance = objective(best_solution)

    available_indices = list(range(1, len(waypoints) - 1))

    for _ in range(max_iterations):
        print("Iteration: ", _)
        time.sleep(2)  # Respect API rate limits
        all_neighbors = []

        # Generate neighbors for each candidate in the beam
        for candidate in beam:
            # Generate multiple neighbors per candidate
            for _ in range(3):  # Generate 3 neighbors per candidate
                neighbor = candidate.copy()
                i, j = random.sample(available_indices, 2)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                all_neighbors.append(neighbor)

        # Evaluate all neighbors
        time.sleep(2)
        evaluated = [(neighbor, objective(neighbor)) for neighbor in all_neighbors]

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


if __name__ == "__main__":
    # Load waypoints (ensure first and last are Snell Library)
    with open("../waypoints.json", "r") as file:
        waypoints = json.load(file)

    map = return_clusters(waypoints, 3)
    i=0
    for key in map.keys():
        temp = []
        temp.append([-71.08811, 42.33862])
        temp.extend(waypoints)
        temp.append([-71.08811, 42.33862])
        assert temp[0] == temp[-1], "Start and end points must be the same"
        best_order = local_beam_search(
            waypoints=temp,
            k=5,
            max_iterations=20
        )
        route_generator(best_order, f'Local Beam Search-{i}')
        i+=1
