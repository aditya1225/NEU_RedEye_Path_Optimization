import time

import openrouteservice
import requests

from config import API_KEY as key

def get_commute_time_without_traffic(origin, destination):
    client = openrouteservice.Client(key=key)
    time.sleep(2)

    origin_coords = origin
    destination_coords = destination

    coordinates = [origin_coords, destination_coords]

    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        'Authorization': key,
        'Content-Type': 'application/json; charset=utf-8'
    }

    body = {
        "coordinates": coordinates,
        "instructions": False,
        "preference": "fastest"
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        try:
            duration_seconds = data['routes'][0]['summary']['duration']
        except (KeyError, IndexError) as e:
            print("Unexpected response structure:", data)
            return None
        duration_minutes = duration_seconds / 60
        return duration_minutes
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def get_commute_time_for_multiple_points(waypoints):
    total_time = 0
    for i in range(len(waypoints) - 1):
        commute_time = get_commute_time_without_traffic(waypoints[i], waypoints[i+1])
        if commute_time is None:
            print(f"Corrupted api response received for point {waypoints[i]} to point {waypoints[i+1]}. Taking commute time as 0 for this.")
            commute_time = 0
        total_time += commute_time
    return total_time

# # Example usage:
# commute_time = get_commute_time_without_traffic("Snell Library, Northeastern University", "36, Mozart St. - Jamaica Plain")
# if commute_time is not None:
#     print(f"Commute Time (without traffic): {commute_time:.2f} minutes")
# else:
#     print("Failed to calculate commute time.")