from Local_Search.objective_function import objective
from Parameters.get_commute_time_without_traffic import get_commute_time_for_multiple_points
from Random_data_generation.get_random_points import get_points
from K_means.k_means_clustering import return_clusters
from Local_Search.hill_climbing import hillClimbing
from Local_Search.simulated_annealing import simulated_annealing
from Local_Search.local_beam_search import local_beam_search
from Local_Search.genetic_algorithm import GeneticTSP
from Route_maps_generation.generate_routemap_multiple import route_generator
from Route_maps_generation.get_address_from_lat_long import get_address_from_lat_long
from config import Sai_Api_Key as key
import re
import os
import json

def startup(number_of_locations, number_of_vans):
    get_points(number_of_locations)
    return_clusters(number_of_vans)

    pattern = re.compile(r"locations_\d+\.json")

    controller_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    location_files = [
        filename for filename in os.listdir(controller_path)
        if pattern.match(filename)
    ]

    for i in range(len(location_files)):
        waypoints=[]
        waypoints.clear()
        waypoints.append([-71.08811, 42.33862])
        with open(f"../locations_{i}.json", "r") as file:
            waypoints.extend(json.load(file))
        waypoints.append([-71.08811, 42.33862])

        hill_climbing_distance, hill_climbing_time = hill_climbing_order(waypoints, 100, i)
        print(f'Best distance by hil climbing for Van{i}- {hill_climbing_distance} miles')
        print(f'Best time by hil climbing for Van{i}- {hill_climbing_time} minutes')

        simulated_annealing_distance, simulated_annealing_time = simulated_annealing_order(waypoints, 100, i)
        print(f'Best distance by simulated annealing for Van{i}- {simulated_annealing_distance} miles')
        print(f'Best time by simulated annealing for Van{i}- {simulated_annealing_time} minutes')

        local_beam_distance, local_beam_time = local_beam_search_order(waypoints, 100, i)
        print(f'Best distance by local beam search for Van{i}- {local_beam_distance} miles')
        print(f'Best time by local beam search for Van{i}- {local_beam_time} minutes')

        genetic_algorithm_distance, genetic_algorithm_time = genetic_algorithm_order(waypoints, 100, i)
        print(f'Best distance by genetic algorithm for Van{i}- {genetic_algorithm_distance} miles')
        print(f'Best time by genetic algorithm for Van{i}- {genetic_algorithm_time} minutes')

def hill_climbing_order(waypoints, max_iterations, van_number):
    best_order = hillClimbing(
        waypoints=waypoints,
        max_iterations=max_iterations
    )

    best_order_address = []
    for coords in best_order:
        best_order_address.append(get_address_from_lat_long(coords))

    controller_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Route_orders'))
    with open(os.path.join(controller_path, f"hill_climbing_{van_number}"), "w") as file:
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

    controller_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Route_orders'))
    with open(os.path.join(controller_path, f"simulated_annealing_{van_number}"), "w") as file:
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

    controller_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Route_orders'))
    with open(os.path.join(controller_path, f"local_beam_search_{van_number}"), "w") as file:
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

    controller_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Route_orders'))
    with open(os.path.join(controller_path, f"genetic_algorithm_{van_number}"), "w") as file:
        json.dump(best_order_address, file)

    route_generator(best_order, f'Genetic Algorithm-{van_number}')

    Total_route_length = objective(best_order, key)
    Total_commute_time = get_commute_time_for_multiple_points(best_order)
    return [Total_route_length, Total_commute_time]

if __name__ == "__main__":
    startup(number_of_locations=15, number_of_vans=3)
