import folium
import openrouteservice
from config import API_KEY as key
import random
import pandas as pd
from Route_maps_generation.generate_latitude_longitude import get_coordinates

def route_generator(waypoints, algorithm_name):
    '''
    This generates a routemap for multiple stops.
    :param waypoints: a list of waypoints.
    :return: a route map in html format.
    '''
    client = openrouteservice.Client(key=key)

    if isinstance(waypoints[0], str):
        temp =[]
        for i in range(len(waypoints)):
            temp.append(get_coordinates(waypoints[i]))
        waypoints = temp

    print(f"Waypoints: {waypoints}")

    try:
        route = client.directions(
            coordinates=waypoints,
            profile='driving-car',
            format='geojson'
        )
        print("API response received successfully.")
    except openrouteservice.exceptions.ApiError as e:
        print(f"OpenRouteService API error: {e}")
        return

    if route is not None:
        route_coords = [(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]

        m = folium.Map(location=[waypoints[0][1], waypoints[0][0]], zoom_start=14)

        for i, (lon, lat) in enumerate(waypoints):
            folium.Marker(
                location=[lat, lon],
                popup=f"Stop {i+1}",
                icon=folium.Icon(color="blue" if i not in [0, len(waypoints)-1] else "green" if i == 0 else "red")
            ).add_to(m)

        folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)

        m.save(f"{algorithm_name}.html")
        print("Map saved as multi_stop_route_map.html.")

# Below is sample code to test.
# df = pd.read_csv("../Locations_dataset/House_locations_dataset.csv")
#
# num_stops = 3
# waypoints = []
#
# for _ in range(num_stops):
#     random_index = random.randint(0, len(df) - 1)
#     random_name = df.iloc[random_index, 0]
#     waypoints.append(get_coordinates(random_name))
#
#
# route_generator(waypoints)
