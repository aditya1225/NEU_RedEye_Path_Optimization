import openrouteservice
import requests
import pandas as pd
from Route_maps_generation.generate_latitude_longitude import get_coordinates


from config import API_KEY as key

def get_distance(origin, destination):
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
        distance_meters = data['routes'][0]['summary']['distance']
        distance_miles = distance_meters / 1609.34
        return distance_miles
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Example usage:
distance = get_distance("Snell Library, Northeastern University", "36, Mozart St. - Jamaica Plain")
if distance is not None:
    print(f"Distance: {distance} miles")
else:
    print("Failed to calculate distance.")