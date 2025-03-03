import openrouteservice
import requests

from config import API_KEY as key
from Route_maps_generation.generate_latitude_longitude import get_coordinates

def get_commute_time_without_traffic(origin, destination):
    client = openrouteservice.Client(key=key)

    origin_coords = get_coordinates(origin)
    destination_coords = get_coordinates(destination)

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
        duration_seconds = data['routes'][0]['summary']['duration']
        duration_minutes = duration_seconds / 60
        return duration_minutes
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Example usage:
commute_time = get_commute_time_without_traffic("Snell Library, Northeastern University", "36, Mozart St. - Jamaica Plain")
if commute_time is not None:
    print(f"Commute Time (without traffic): {commute_time:.2f} minutes")
else:
    print("Failed to calculate commute time.")