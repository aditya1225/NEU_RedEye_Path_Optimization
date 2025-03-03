import requests
from config import TOMTOM_API_KEY as key
import pandas as pd
from Route_maps_generation.generate_latitude_longitude import get_coordinates

df = pd.read_csv("../Locations_dataset/House_locations_dataset_with_coordinates.csv", header=None)
def get_commute_time_with_traffic(origin, destination):

    origin_coords = get_coordinates(origin)
    destination_coords = get_coordinates(destination)


    url = "https://api.tomtom.com/routing/1/calculateRoute/{start_lat},{start_lon}:{end_lat},{end_lon}/json"

    url = url.format(
        start_lat=origin_coords[1],
        start_lon=origin_coords[0],
        end_lat=destination_coords[1],
        end_lon=destination_coords[0],
    )

    params = {
        "key": key,
        "traffic": "true",
        "travelMode": "car",
        "routeType": "fastest",
    }


    response = requests.get(url, params=params)


    if response.status_code == 200:
        data = response.json()
        if data.get("routes"):
            travel_time_seconds = data["routes"][0]["summary"]["travelTimeInSeconds"]
            travel_time_minutes = travel_time_seconds / 60
            print(travel_time_minutes)
            return travel_time_minutes
        else:
            print("Error: No routes found in the response.")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Example usage:
# commute_time = get_commute_time_with_traffic("Snell Library, Boston, USA", "36 Mozart Street, Boston, USA")
# if commute_time is not None:
#     print(f"Commute Time (with traffic): {commute_time:.2f} minutes")
# else:
#     print("Failed to calculate commute time.")