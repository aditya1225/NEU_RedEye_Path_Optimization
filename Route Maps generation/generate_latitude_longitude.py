import openrouteservice
from config import API_KEY as key

def get_coordinates(address):
    client = openrouteservice.Client(key= f'{key}')
    address = address + " Boston, MA"
    geocode = client.pelias_search(text=address)

    if geocode and "features" in geocode and len(geocode["features"]) > 0:
        coords = geocode["features"][0]["geometry"]["coordinates"]

    if coords:
        return (coords[0], coords[1])
    else:
        return (None, None)
