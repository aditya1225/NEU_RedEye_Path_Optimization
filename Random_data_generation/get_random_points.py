import pandas as pd
import random
import json
def get_points(number_of_locations):
    df = pd.read_csv("d:/Masters/Northeastern/Course work/Spring25/FAI/Project/Locations_dataset/House_locations_dataset_with_coordinates.csv", header=None)
    waypoints = []
    numbers = random.sample(range(60), number_of_locations)
    for num in numbers:
        waypoints.append((df.iloc[num][1], df.iloc[num][2]))
    with open("../locations.json", "w") as file:
        json.dump(waypoints, file)
