import pandas as pd
import random
import json
from pathlib import Path

def get_points(number_of_locations):
    '''
    Generates random points from a dataset of house locations.
    The dataset is expected to be in CSV format with latitude and longitude
    coordinates in the second and third columns respectively.
    The generated points are saved in a JSON file.
    :param number_of_locations: Number of random locations to generate
    :return: None
    '''
    # path = Path("../Locations_dataset/House_locations_dataset_with_coordinates.csv.csv")
    path = Path(__file__).parent / "../Locations_dataset/House_locations_dataset_with_coordinates.csv"
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    df = pd.read_csv(path, header=None)
    waypoints = []
    numbers = random.sample(range(60), number_of_locations)
    for num in numbers:
        waypoints.append((df.iloc[num][1], df.iloc[num][2]))
    
    # with open("../locations.json", "w") as file:
    output_path = Path(__file__).parent / "../locations.json"
    with output_path.open("w") as file:
        json.dump(waypoints, file)
if __name__ == "__main__":
    get_points(35)