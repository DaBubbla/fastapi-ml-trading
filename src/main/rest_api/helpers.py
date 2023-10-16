import io
import pandas as pd
import numpy as np

def assemble_data(response):
    data = pd.read_csv(io.StringIO(response.text), index_col=False)

    # Sort the entire dataset in ascending order by timestamp
    data = data.sort_values(by="timestamp", ascending=True)

    return data
