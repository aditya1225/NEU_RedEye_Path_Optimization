import openrouteservice
from config import API_KEY as key
import time

def objective(waypoints):
    """Calculate total distance of a route using OpenRouteService API"""
    time.sleep(3)
    client = openrouteservice.Client(key=key)
    route = client.directions(
        coordinates=waypoints,
        profile='driving-car',
        format='geojson'
    )
    return route["features"][0]["properties"]["segments"][0]["distance"]