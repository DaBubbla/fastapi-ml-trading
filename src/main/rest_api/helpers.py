import io
import pandas as pd
import numpy as np


def assemble_data(response):
    data = pd.read_csv(io.StringIO(response.text), index_col=False)

    # Sort the entire dataset in ascending order by timestamp
    data = data.sort_values(by="timestamp", ascending=True)

    # Calculate DeMark indicators for the entire sorted dataset
    demark_added = calculate_demarker(data)

    return demark_added, data


def calculate_demarker(data):
    data['setup'] = 0
    data['countdown'] = 0

    for i in range(1, len(data)):
        if np.isnan(data['high'].iloc[i]) or np.isnan(data['low'].iloc[i]):
            continue

        if data['high'].iloc[i] < data['high'].iloc[i - 1]:
            data['setup'].iloc[i] = max(data['high'].iloc[i - 1] - data['low'].iloc[i], 0)
        else:
            data['setup'].iloc[i] = 0

        if data['low'].iloc[i] > data['low'].iloc[i - 1]:
            data['countdown'].iloc[i] = max(data['high'].iloc[i - 1] - data['low'].iloc[i], 0)
        else:
            data['countdown'].iloc[i] = 0

    return data

def get_last_10_data_points(data):
    # Get the last 10 data points
    last_10_data_points = data.tail(10)

    # Drop any rows with missing values (NaN)
    last_10_data_points = last_10_data_points.dropna()

    return last_10_data_points