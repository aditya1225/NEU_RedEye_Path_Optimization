import random
from Route_maps_generation.generate_latitude_longitude import get_coordinates
import pandas as pd
import json

df = pd.read_csv("../Locations_dataset/House_locations_dataset_with_coordinates.csv", header=None)
waypoints = []
waypoints.append(get_coordinates('Snell Library, Northeastern University'))
numbers = random.sample(range(61), 35)
for num in numbers:
    waypoints.append((df.iloc[num][1], df.iloc[num][2]))
waypoints.append(get_coordinates('Snell Library, Northeastern University'))
with open("../waypoints.json", "w") as file:
    json.dump(waypoints, file)