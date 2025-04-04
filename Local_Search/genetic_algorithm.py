import random
from config import Sai_Api_Key as key
from Local_Search.objective_function import objective

class GeneticTSP:
    """
    Genetic Algorithm for Traveling Salesman Problem (TSP).
    This class implements a genetic algorithm to find the shortest route
    visiting all waypoints, with fixed start and end points.
    The algorithm uses a population-based approach with selection,
    crossover, and mutation to evolve solutions over generations.
    :param waypoints: List of waypoints including start and end points (start = end for TSP)
    :param pop_size: Population size for genetic algorithm
    :param elite_size: Number of elite individuals to carry over to the next generation
    :param mutation_rate: Probability of mutation for each individual
    """
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
        if len(parent1) < 3:
            return parent1[:]

        start, end = sorted(random.sample(range(1, len(parent1) - 2), 2))
        child = [None] * len(parent1)

        child[0] = parent1[0]
        child[-1] = parent1[-1]
        child[start:end + 1] = parent1[start:end + 1]

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

