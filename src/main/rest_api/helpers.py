import io
import pandas as pd
import numpy as np


def assemble_data(query_params, response):
    data = pd.read_csv(io.StringIO(response.text), index_col=False)

    start_date = query_params.start_date
    end_date = query_params.calculate_end_date

    filtered_data = data[(data["timestamp"] >= start_date) & (data["timestamp"] <= end_date)]
    filtered_data = filtered_data.sort_values(by="timestamp", ascending=True)
    

    demark_added = calculate_demarker(filtered_data.head(10))
    return demark_added, data.sort_values(by="timestamp", ascending=True)


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