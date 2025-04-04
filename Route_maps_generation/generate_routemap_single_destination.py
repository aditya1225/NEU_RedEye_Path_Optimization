import folium
import openrouteservice
from config import API_KEY as key

def route_generator(start, end):
    """
    Generate a route map using OpenRouteService API and Folium.
    This function takes a start and end location, retrieves the route from the OpenRouteService API,
    and generates an HTML file with the route map.
    :param start: The starting location as a tuple (longitude, latitude).
    :param end: The ending location as a tuple (longitude, latitude).
    """
    route = None
    client = openrouteservice.Client(key=f'{key}')

    try:
        route = client.directions(
            coordinates=[start, end],
            profile='driving-car',
            format='geojson'
        )
        print("API response received successfully.")
    except openrouteservice.exceptions.ApiError as e:
        print(f"OpenRouteService API error: {e}")

    if route is not None:
        route_coords = [(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]
        m = folium.Map(location=[42.35, -71.09], zoom_start=14) #TODO: Replace the coordinates here with snell's

        folium.Marker(location=[start[1], start[0]], popup="Start Location", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker(location=[end[1], end[0]], popup="End Location", icon=folium.Icon(color="red")).add_to(m)
        folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)

        # Save map
        # m.save("route_map.html")
        output_path = Path(__file__).parent / "route_map.html"
        m.save(output_path)
        print("Map saved as route_map.html.")
    else:
        print("Route could not be generated.")

