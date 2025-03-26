import pandas as pd

def get_coordinates(address):
    df = pd.read_csv("../Locations_dataset/House_locations_dataset_with_coordinates.csv", header=None)
    origin_index = 0
    for i in range(df.shape[0] + 1):
        if df.iloc[i][0] == address:
            origin_index = i
            break
    origin_coords = (df.iloc[origin_index][1], df.iloc[origin_index][2])

    return origin_coords
