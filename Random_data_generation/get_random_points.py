import pandas as pd
import random
import json
from pathlib import Path

def get_points(number_of_locations):
    # path = Path("../Locations_dataset/House_locations_dataset_with_coordinates.csv.csv")
    path = Path(__file__).parent / "../Locations_dataset/House_locations_dataset_with_coordinates.csv"
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    df = pd.read_csv(path, header=None)
    waypoints = []
    numbers = random.sample(range(60), number_of_locations)
    for num in numbers:
        waypoints.append((df.iloc[num][1], df.iloc[num][2]))

    # Save waypoints to JSON file
    # Ensure the parent directory exists
    # output_path = Path(__file__).parent / "../locations.json"
    # output_path.parent.mkdir(parents=True, exist_ok=True)
    # with output_path.open("w") as file:
    #     json.dump(waypoints, file)
    
    # with open("../locations.json", "w") as file:
    output_path = Path(__file__).parent / "../locations.json"
    with output_path.open("w") as file:
        json.dump(waypoints, file)
if __name__ == "__main__":
    get_points(35)