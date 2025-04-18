from Local_Search.objective_function import objective
from Parameters.get_commute_time_without_traffic import get_commute_time_for_multiple_points
from Random_data_generation.get_random_points import get_points
from K_means.k_means_clustering import return_clusters
from Local_Search.hill_climbing import hillClimbing
from Local_Search.simulated_annealing import simulated_annealing
from Local_Search.local_beam_search import local_beam_search
from Local_Search.genetic_algorithm import GeneticTSP
from Local_Search.a_star import a_star_search
from Route_maps_generation.generate_routemap_multiple import route_generator
from Route_maps_generation.get_address_from_lat_long import get_address_from_lat_long
from config import API_KEY_3 as key
from pathlib import Path
import re
import os
import json

def startup(number_of_locations, number_of_vans):
    """
    This function initializes the routing process by generating random points,
    clustering them, and then applying various search algorithms to find the best route.
    It cleans up any existing location files, generates new ones, and computes the best routes
    using different algorithms such as Hill Climbing, Simulated Annealing, Local Beam Search,
    Genetic Algorithm, and A* Search. The results are printed and saved to files.
    :param number_of_locations: Number of locations to generate
    :param number_of_vans: Number of vans to cluster the locations
    :return: A dictionary containing the best distances and times for each algorithm and van
    :rtype: dict
    :raises Exception: If the number of vans is greater than the number of locations
    :raises Exception: If the number of vans is less than 1
    :raises Exception: If the number of locations is less than 1
    :raises Exception: If the number of locations is greater than 59
    """
    metrics = {}
    pattern = re.compile(r"locations_\d+\.json")
    controller_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    for filename in os.listdir(controller_path):
        if pattern.match(filename):
            os.remove(os.path.join(controller_path, filename))

    get_points(number_of_locations)
    return_clusters(number_of_vans)
    location_files = [f"locations_{i}.json" for i in range(number_of_vans)]

    cumulative_metrics = {
        'Hill Climbing': {'distance': 0, 'time': 0},
        'Simulated Annealing': {'distance': 0, 'time': 0},
        'Local Beam Search': {'distance': 0, 'time': 0},
        'Genetic Algorithm': {'distance': 0, 'time': 0},
        'A* Search': {'distance': 0, 'time': 0}
    }

    for i in range(len(location_files)):
        waypoints = []
        waypoints.clear()
        waypoints.append([-71.08811, 42.33862])
        output_path = Path(__file__).parent / f"../{location_files[i]}"
        with output_path.open("r") as file:
            waypoints.extend(json.load(file))
        waypoints.append([-71.08811, 42.33862])

        # Hill Climbing
        hill_climbing_distance, hill_climbing_time = hill_climbing_order(waypoints, 100, i)
        hill_climbing_distance = round(hill_climbing_distance, 2)
        hill_climbing_time = round(hill_climbing_time, 2)
        metrics[f'Hill Climbing-{i}'] = {'distance': hill_climbing_distance, 'time': hill_climbing_time}
        cumulative_metrics['Hill Climbing']['distance'] += hill_climbing_distance
        cumulative_metrics['Hill Climbing']['time'] += hill_climbing_time
        print(f'Best distance by hill climbing for Van{i}- {hill_climbing_distance} miles')
        print(f'Best time by hill climbing for Van{i}- {hill_climbing_time} minutes')

        # Simulated Annealing
        simulated_annealing_distance, simulated_annealing_time = simulated_annealing_order(waypoints, 100, i)
        simulated_annealing_distance = round(simulated_annealing_distance, 2)
        simulated_annealing_time = round(simulated_annealing_time, 2)
        metrics[f'Simulated Annealing-{i}'] = {'distance': simulated_annealing_distance, 'time': simulated_annealing_time}
        cumulative_metrics['Simulated Annealing']['distance'] += simulated_annealing_distance
        cumulative_metrics['Simulated Annealing']['time'] += simulated_annealing_time
        print(f'Best distance by simulated annealing for Van{i}- {simulated_annealing_distance} miles')
        print(f'Best time by simulated annealing for Van{i}- {simulated_annealing_time} minutes')

        # Local Beam Search
        local_beam_distance, local_beam_time = local_beam_search_order(waypoints, 100, i)
        local_beam_distance = round(local_beam_distance, 2)
        local_beam_time = round(local_beam_time, 2)
        metrics[f'Local Beam Search-{i}'] = {'distance': local_beam_distance, 'time': local_beam_time}
        cumulative_metrics['Local Beam Search']['distance'] += local_beam_distance
        cumulative_metrics['Local Beam Search']['time'] += local_beam_time
        print(f'Best distance by local beam search for Van{i}- {local_beam_distance} miles')
        print(f'Best time by local beam search for Van{i}- {local_beam_time} minutes')

        # Genetic Algorithm
        genetic_algorithm_distance, genetic_algorithm_time = genetic_algorithm_order(waypoints, 100, i)
        genetic_algorithm_distance = round(genetic_algorithm_distance, 2)
        genetic_algorithm_time = round(genetic_algorithm_time, 2)
        metrics[f'Genetic Algorithm-{i}'] = {'distance': genetic_algorithm_distance, 'time': genetic_algorithm_time}
        cumulative_metrics['Genetic Algorithm']['distance'] += genetic_algorithm_distance
        cumulative_metrics['Genetic Algorithm']['time'] += genetic_algorithm_time
        print(f'Best distance by genetic algorithm for Van{i}- {genetic_algorithm_distance} miles')
        print(f'Best time by genetic algorithm for Van{i}- {genetic_algorithm_time} minutes')

        # A* Search
        a_star_distance, a_star_time = a_star_order(waypoints, 1000, i)
        a_star_distance = round(a_star_distance, 2)
        a_star_time = round(a_star_time, 2)
        metrics[f'A Search-{i}'] = {'distance': a_star_distance, 'time': a_star_time}
        cumulative_metrics['A* Search']['distance'] += a_star_distance
        cumulative_metrics['A* Search']['time'] += a_star_time
        print(f'Best distance by A* search for Van{i}- {a_star_distance} miles')
        print(f'Best time by A* search for Van{i}- {a_star_time} minutes')

    # Print cumulative results
    print("\nCumulative Results Across All Vans:")
    for algo, values in cumulative_metrics.items():
        print(f"{algo}: Total Distance = {values['distance']:.2f} miles, Total Time = {values['time']:.2f} minutes")

    # Create and print leaderboards
    print("\nDistance Leaderboard (Shortest to Longest):")
    distance_sorted = sorted(cumulative_metrics.items(), key=lambda x: x[1]['distance'])
    for rank, (algo, values) in enumerate(distance_sorted, 1):
        print(f"{rank}. {algo}: {values['distance']:.2f} miles")

    print("\nTime Leaderboard (Shortest to Longest):")
    time_sorted = sorted(cumulative_metrics.items(), key=lambda x: x[1]['time'])
    for rank, (algo, values) in enumerate(time_sorted, 1):
        print(f"{rank}. {algo}: {values['time']:.2f} minutes")

    return metrics, cumulative_metrics, distance_sorted, time_sorted

def hill_climbing_order(waypoints, max_iterations, van_number):
    best_order = hillClimbing(
        waypoints=waypoints,
        max_iterations=max_iterations
    )

    best_order_address = []
    for coords in best_order:
        best_order_address.append(get_address_from_lat_long(coords))

    # with open(f"../Route_orders/hill_climbing_{van_number}", "w") as file:
    output_path = Path(__file__).parent / f"../Route_orders/hill_climbing_{van_number}"
    with output_path.open("w") as file:
        json.dump(best_order_address, file)

    route_generator(best_order, f'Hill Climbing-{van_number}')

    Total_route_length = objective(best_order, key)
    Total_commute_time = get_commute_time_for_multiple_points(best_order)
    return [Total_route_length, Total_commute_time]

def simulated_annealing_order(waypoints, max_iterations, van_number):
    best_order = simulated_annealing(
        locations_0=waypoints,
        max_iterations=max_iterations,
        initial_temp=10000.0,
        alpha=0.99
    )

    best_order_address = []
    for coords in best_order:
        best_order_address.append(get_address_from_lat_long(coords))

    # with open(f"../Route_orders/simulated_annealing_{van_number}", "w") as file:
    output_path = Path(__file__).parent / f"../Route_orders/simulated_annealing_{van_number}"
    with output_path.open("w") as file:
        json.dump(best_order_address, file)

    route_generator(best_order, f'Simulated Annealing-{van_number}')

    Total_route_length = objective(best_order, key)
    Total_commute_time = get_commute_time_for_multiple_points(best_order)
    return [Total_route_length, Total_commute_time]

def local_beam_search_order(waypoints, max_iterations, van_number):
    best_order = local_beam_search(
        waypoints=waypoints,
        k=5,
        max_iterations=max_iterations
    )

    best_order_address = []
    for coords in best_order:
        best_order_address.append(get_address_from_lat_long(coords))

    # with open(f"../Route_orders/local_beam_search_{van_number}", "w") as file:
    output_path = Path(__file__).parent / f"../Route_orders/local_beam_search_{van_number}"
    with output_path.open("w") as file:
        json.dump(best_order_address, file)

    route_generator(best_order, f'Local Beam Search-{van_number}')

    Total_route_length = objective(best_order, key)
    Total_commute_time = get_commute_time_for_multiple_points(best_order)
    return [Total_route_length, Total_commute_time]


def genetic_algorithm_order(waypoints, max_iterations, van_number):
    ga = GeneticTSP(
        waypoints,
        pop_size=30,
        elite_size=5,
        mutation_rate=0.01
    )
    best_order = ga.run(generations=max_iterations)

    best_order_address = []
    for coords in best_order:
        best_order_address.append(get_address_from_lat_long(coords))

    # with open(f"../Route_orders/genetic_algorithm_{van_number}", "w") as file:
    output_path = Path(__file__).parent / f"../Route_orders/genetic_algorithm_{van_number}"
    with output_path.open("w") as file:
        json.dump(best_order_address, file)

    route_generator(best_order, f'Genetic Algorithm-{van_number}')

    Total_route_length = objective(best_order, key)
    Total_commute_time = get_commute_time_for_multiple_points(best_order)
    return [Total_route_length, Total_commute_time]

def a_star_order(waypoints, max_iterations, van_number):
    best_order = a_star_search(
        waypoints=waypoints,
        max_iterations=max_iterations
    )

    best_order_address = []
    for coords in best_order:
        best_order_address.append(get_address_from_lat_long(coords))

    output_path = Path(__file__).parent / f"../Route_orders/a_star_{van_number}"
    with output_path.open("w") as file:
        json.dump(best_order_address, file)

    route_generator(best_order, f'A Search-{van_number}')

    Total_route_length = objective(best_order, key)
    Total_commute_time = get_commute_time_for_multiple_points(best_order)
    return [Total_route_length, Total_commute_time]

if __name__ == "__main__":
    num_locations = input("Enter number of locations ([1, 59]): ")
    num_vans = input("Enter number of vans (must be >= number of locations): ")
    if int(num_vans) > int(num_locations):
        raise Exception("Number of vans cannot be greater than number of locations")
    if int(num_vans) < 1:
        raise Exception("Number of vans cannot be less than 1")
    if int(num_locations) < 1:
        raise Exception("Number of locations cannot be less than 1")
    if int(num_locations) > 59:
        raise Exception("Number of locations cannot be greater than 59")
    startup(number_of_locations=int(num_locations), number_of_vans=int(num_vans))