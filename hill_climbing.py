import time

from Parameters.get_commute_time_with_traffic import get_commute_time_with_traffic
from Route_maps_generation.generate_routemap_multiple import route_generator

def total_travel_time(sequence):
    total_time = 0
    for i in range(len(sequence) - 1):
        total_time += get_commute_time_with_traffic(sequence[i], sequence[i + 1])
        time.sleep(2)
    total_time += get_commute_time_with_traffic(sequence[-1], sequence[0])
    return total_time

def generate_neighbors(sequence):
    neighbors = []
    for i in range(1, len(sequence) - 1):
        for j in range(i + 1, len(sequence)):
            neighbor = sequence.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def HILL_CLIMBING(waypoints, start):
    current_sequence = [start] + waypoints
    current_time = total_travel_time(current_sequence)
    print("Current time: ", current_time)

    while True:
        neighbors = generate_neighbors(current_sequence)
        best_neighbor = None
        best_time = current_time
        print('stuck here')
        for neighbor in neighbors:
            print('stuck here2')
            neighbor_time = total_travel_time(neighbor)
            print(neighbor_time)
            if neighbor_time < best_time:
                print('stuck here3')
                best_neighbor = neighbor
                best_time = neighbor_time
        print('stuck here4')
        if best_neighbor is None:
            print('stuck here5')
            break

        current_sequence = best_neighbor
        current_time = best_time
    print('stuck here6')
    current_sequence.append('Snell Library, Northeastern University')
    current_time = total_travel_time(current_sequence)
    route_generator(current_sequence)
    return current_sequence, current_time

waypoints = [
    '314, Centre St. - Jamaica Plain', '48, Hereford St. - Back Bay', '65, Burrell St. - Roxbury']
    #'848, Huntington Ave. - Mission Hill', '15, Aberdeen - Kenmore', '205, Highland St. - Fort Hill',
   # '10, Roxbury St. - Roxbury', '767, Tremont St. - South End', '90, Hammond St. - South End'

start = 'Snell Library, Northeastern University'

best_sequence, best_time = HILL_CLIMBING(waypoints, start)
print("Best Sequence:", best_sequence)
print("Total Travel Time (minutes):", best_time)