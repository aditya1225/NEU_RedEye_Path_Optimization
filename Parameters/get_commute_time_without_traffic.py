import time
import openrouteservice
import requests
from config import API_KEY as key

def get_commute_time_without_traffic(origin, destination):
    """
    Get commute time between two locations using OpenRouteService API.
    :param origin: Starting point (latitude, longitude)
    :param destination: Ending point (latitude, longitude)
    :return: Estimated commute time in minutes
    :rtype: float
    :raises Exception: If the API response is not as expected
    """
    client = openrouteservice.Client(key=key)
    retries = 3
    delay = 5  # seconds
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
    """
    Get total commute time for multiple waypoints using OpenRouteService API.
    :param waypoints: List of waypoints (latitude, longitude)
    :return: Total commute time in minutes
    :rtype: float
    """
    total_time = 0
    for i in range(len(waypoints) - 1):
        commute_time = get_commute_time_without_traffic(waypoints[i], waypoints[i+1])
        if commute_time is None:
            print(f"Corrupted api response received for point {waypoints[i]} to point {waypoints[i+1]}. Taking commute time as 0 for this.")
            commute_time = 0
        total_time += commute_time
    return total_time