import pandas as pd
from pathlib import Path

def get_coordinates(address):
    """
    Get the coordinates of a given address from a CSV file.
    :param address: Address to find the coordinates for
    :return: Tuple of latitude and longitude
    """
    # df = pd.read_csv("../Locations_dataset/House_locations_dataset_with_coordinates.csv", header=None)
    input_path = Path(__file__).parent / "../Locations_dataset/House_locations_dataset_with_coordinates.csv"
    df = pd.read_csv(input_path, header=None)
    origin_index = 0
    for i in range(df.shape[0] + 1):
        if df.iloc[i][0] == address:
            origin_index = i
            break
    origin_coords = (df.iloc[origin_index][1], df.iloc[origin_index][2])

    return origin_coords
