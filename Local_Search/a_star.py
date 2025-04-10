import heapq
from math import sqrt
from Local_Search.objective_function import objective
from config import API_KEY_3 as key

def euclidean_dist(point1, point2):
    """Calculate Euclidean distance between two points"""
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def heuristic(current, remaining_points, end):
    """Estimate remaining distance: max distance to any unvisited point plus distance to end"""
    if not remaining_points:
        return euclidean_dist(current, end)
    max_to_remaining = max(euclidean_dist(current, p) for p in remaining_points)
    return max_to_remaining + min(euclidean_dist(p, end) for p in remaining_points)

def complete_path(partial_path, remaining_points, end):
    """
    Complete a partial path by greedily adding remaining points and returning to end.
    :param partial_path: Current path from A*
    :param remaining_points: Set of unvisited points
    :param end: Final point (Snell Library)
    :return: Complete tour visiting all points
    """
    current_path = partial_path.copy()
    remaining = list(remaining_points)
    
    # Greedy nearest-neighbor to add remaining points
    while remaining:
        current = current_path[-1]
        next_point = min(remaining, key=lambda p: euclidean_dist(current, p))
        current_path.append(list(next_point))
        remaining.remove(next_point)
    
    # Return to end if not there
    if current_path[-1] != end:
        current_path.append(end)
    
    return current_path

def a_star_search(waypoints, max_iterations=1000):
    """
    A* search algorithm adapted for TSP: finds a tour visiting all waypoints.
    If iterations exhaust, completes the path with remaining points.
    :param waypoints: List of waypoints including start and end points (start = end for TSP)
    :param max_iterations: Maximum number of iterations to prevent infinite loops
    :return: List of waypoints visiting all points
    """
    start = waypoints[0]
    end = waypoints[-1]
    points_to_visit = set(tuple(p) for p in waypoints[1:-1])
    
    # Priority queue: (f_score, g_score, current_path, remaining_points)
    open_set = [(0, 0, [start], points_to_visit)]
    heapq.heapify(open_set)
    
    closed_set = set()
    iteration = 0
    
    while open_set and iteration < max_iterations:
        f_score, g_score, current_path, remaining = heapq.heappop(open_set)
        
        # For hashing
        path_tuple = tuple(tuple(coord) for coord in current_path)
        if path_tuple in closed_set:
            continue
            
        closed_set.add(path_tuple)
        
        # Solution found
        if not remaining and current_path[-1] != end:
            new_path = current_path + [end]
            new_g_score = objective(new_path, key)
            if new_g_score < float('inf'):
                # print(f"Optimal waypoints: {new_path}")
                return new_path
        
        # Explore remaining points
        for next_point_tuple in remaining:
            next_point = list(next_point_tuple)
            if next_point not in current_path:
                new_path = current_path + [next_point]
                new_remaining = remaining - {next_point_tuple}
                new_g_score = objective(new_path, key)
                h_score = heuristic(new_path[-1], new_remaining, end)
                new_f_score = new_g_score + h_score
                heapq.heappush(open_set, (new_f_score, new_g_score, new_path, new_remaining))
        iteration += 1
    
    # Iteration exhausted – complete the path with greedy approach
    if open_set:
        _, _, best_path, remaining = heapq.heappop(open_set)
        complete_path_result = complete_path(best_path, remaining, end)
        # print(f"Completed path (iterations exhausted): {complete_path_result}")
        return complete_path_result
    
    # Worst case if no solution found
    print("No solution found, returning original waypoints")
    return waypoints