import random

from Parameters.get_commute_time_without_traffic import get_commute_time_for_multiple_points
from config import Sai_Api_Key as key
from Route_maps_generation.generate_routemap_multiple import route_generator
import json
from Local_Search.objective_function import objective
from Route_maps_generation.get_address_from_lat_long import get_address_from_lat_long



class GeneticTSP:
    def __init__(self, waypoints, pop_size=50, elite_size=10, mutation_rate=0.01):
        self.waypoints = waypoints
        self.pop_size = pop_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.fixed_indices = [0, -1]  # First and last points (Snell Library)

        # Initialize population
        self.population = [self.create_individual() for _ in range(pop_size)]

    def create_individual(self):
        """Create a route with fixed start/end points"""
        middle = self.waypoints[1:-1]
        random.shuffle(middle)
        return [self.waypoints[0]] + middle + [self.waypoints[-1]]

    def rank_routes(self):
        """Evaluate and sort population by fitness"""
        fitness = [(ind, objective(ind, key)) for ind in self.population]
        return sorted(fitness, key=lambda x: x[1])

    def selection(self, ranked_pop):
        """Tournament selection"""
        selection_results = []
        # Elitism: carry over best performers
        selection_results.extend([ind for ind, _ in ranked_pop[:self.elite_size]])

        # Tournament selection for remaining spots
        for _ in range(self.pop_size - self.elite_size):
            candidates = random.sample(ranked_pop, 3)
            winner = min(candidates, key=lambda x: x[1])
            selection_results.append(winner[0])
        return selection_results

    def crossover(self, parent1, parent2):
        """Ordered Crossover (OX) for middle section"""
        start, end = sorted(random.sample(range(1, len(parent1) - 2), 2))
        child = [None] * len(parent1)

        # Keep fixed points
        child[0] = parent1[0]
        child[-1] = parent1[-1]

        # Copy segment from parent1
        child[start:end + 1] = parent1[start:end + 1]

        # Fill remaining from parent2
        remaining = [gene for gene in parent2[1:-1] if gene not in child]
        ptr = 1
        for i in range(1, len(child) - 1):
            if child[i] is None:
                child[i] = remaining[ptr - 1]
                ptr += 1
        return child

    def mutate(self, individual):
        """Swap mutation for middle section"""
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(1, len(individual) - 1), 2)
            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
        return individual

    def next_generation(self):
        """Create new generation with proper elitism"""
        ranked_pop = self.rank_routes()
        elites = [ind for ind, _ in ranked_pop[:self.elite_size]]  # Direct elites

        # Generate remaining via selection, crossover, mutation
        selection = self.selection(ranked_pop)
        children = []
        while len(children) < self.pop_size - self.elite_size:
            parent1, parent2 = random.sample(selection, 2)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            children.append(child)

        self.population = elites + children  # Preserve elites directly

    def run(self, generations=100):
        best_individual = None
        best_distance = float('inf')

        for gen in range(generations):
            #print("Generation {}".format(gen))
            self.next_generation()

            # Track best solution
            current_best = min(self.rank_routes(), key=lambda x: x[1])
            if current_best[1] < best_distance:
                best_distance = current_best[1]
                best_individual = current_best[0]

            #print(f"Generation {gen + 1}: Best Distance = {best_distance / 1000:.2f} km")

        return best_individual


# if __name__ == "__main__":
#     # Load waypoints (ensure first and last are Snell Library)
#     waypoints = [[-71.08811, 42.33862]]
#     with open("../locations_0.json", "r") as file:
#         waypoints.extend(json.load(file))
#
#     waypoints.append([-71.08811, 42.33862])
#
#     # Initialize and run genetic algorithm
#     ga = GeneticTSP(
#         waypoints,
#         pop_size=30,
#         elite_size=5,
#         mutation_rate=0.01
#     )
#
#     best_order = ga.run(generations=10)
#
#     print("\nBest order found by Genetic Algorithm:")
#     route_generator(best_order, 'Genetic Algorithm')
#     for coord in best_order:
#         print(get_address_from_lat_long(coord))
#     print(f"Best distance : {objective(best_order, key)} miles")
#     print(f"Total commute time: {get_commute_time_for_multiple_points(best_order)} minutes")