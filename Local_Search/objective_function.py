import openrouteservice
import time
import numpy as np
from pathlib import Path

def objective(waypoints, api_key):
    """
    Calculate the total distance of a route using cached distances stored in a NumPy file.
    If a distance between a source and destination pair is not cached, an API call is made.
    Note: Distance from A to B might differ from B to A.
    :param waypoints: List of tuples (latitude, longitude) representing the route.
    :param api_key: API key for the OpenRouteService.
    :return: Total distance in miles.
    """
    # file_path = "../Locations_dataset/pre_stored_distances.npy"
    file_path = Path(__file__).parent / "../Locations_dataset/pre_stored_distances.npy"

    # Define a structured dtype for our data.
    dtype = np.dtype([
        ('src_lat', np.float64),
        ('src_lon', np.float64),
        ('dest_lat', np.float64),
        ('dest_lon', np.float64),
        ('dist', np.float64)
    ])

    try:
        data = np.load(file_path, allow_pickle=True)
        # Ensure data is a structured array
        if data.size == 0:
            data = np.empty(0, dtype=dtype)
    except Exception:
        data = np.empty(0, dtype=dtype)

    total_distance = 0.0
    client = openrouteservice.Client(key=api_key)

    for i in range(len(waypoints) - 1):
        src = waypoints[i]
        dest = waypoints[i + 1]
        mask = (
                (data['src_lat'] == src[1]) &
                (data['src_lon'] == src[0]) &
                (data['dest_lat'] == dest[1]) &
                (data['dest_lon'] == dest[0])
        )
        if np.any(mask):
            d = data['dist'][mask][0]
        else:
            time.sleep(3)
            coords = [list(src), list(dest)]
            route = client.directions(
                coordinates=coords,
                profile='driving-car',
                format='geojson'
            )
            d = route["features"][0]["properties"]["segments"][0]["distance"]

            new_row = np.array([(src[1], src[0], dest[1], dest[0], d)], dtype=dtype)
            if data.size == 0:
                data = new_row
            else:
                data = np.concatenate((data, new_row))
            np.save(file_path, data)
        total_distance += d

    distance_miles = total_distance / 1609.34
    return distance_miles
