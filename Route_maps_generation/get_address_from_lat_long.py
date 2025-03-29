import pandas as pd
def get_address_from_lat_long(lat_long):
    df = pd.read_csv("../Locations_dataset/House_locations_dataset_with_coordinates.csv", header=None)
    origin_index = 0
    for i in range(df.shape[0] + 1):
        if df.iloc[i][1] == lat_long[0] and df.iloc[i][2] == lat_long[1]:
            origin_index = i
            break
    address = df.iloc[origin_index][0]

    return address