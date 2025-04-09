import pandas as pd
import random
import json
from pathlib import Path
def get_points(number_of_locations, number_of_vans):
    df = pd.read_csv("d:/Masters/Northeastern/Course work/Spring25/FAI/Project/Locations_dataset/House_locations_dataset_with_coordinates.csv", header=None)
    waypoints = []
    numbers = random.sample(range(60), number_of_locations)
    for num in numbers:
        waypoints.append((df.iloc[num][1], df.iloc[num][2]))

    output_dir = "d:/Masters/Northeastern/Course work/Spring25/FAI/Project/"
    for i in range(number_of_vans):
        output_file = f"{output_dir}locations_{i}.json"
        with open(output_file, "w") as file:
            json.dump(waypoints, file)
