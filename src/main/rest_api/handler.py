"""
Main handler for API requests.
"""
import json
import os
import asyncio
import requests

from src.main.framework.exceptions import (
    RequestBodyException, DownstreamException
)
from src.main.framework.ml_models import StockPricePredictor
from src.main.framework.models import ResponseModel
from src.main.rest_api.helpers import assemble_data, get_last_10_data_points


def get_response(session_handler={}, url="", params=""):
    """
    Calls the API and returns the response.
    Params:
        session_handler (SessionHandler): The session object containing 
        configs/request/etc.
    Returns:
        JSON: The JSON response.
    """

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise DownstreamException
    return response


def call_api(session_handler):
    """
    Calls the API and returns the response.
    Params:
        request (Request): The request object.
    Returns:
        JSON: The JSON response.
    """
    try:
        url = session_handler.config.get("alphavantage_url", "")
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": session_handler.req_body.query_params.symbol,
            "outputsize": "full",  # for now full will return all data compact will return recent 100
            "apikey": session_handler.config.get("alphavantage_api_key"),
            "datatype": "csv"
        }

        response = get_response(
            session_handler=session_handler, url=url, params=params
        )
        return response
    except requests.exceptions.RequestException as e:
        raise RequestBodyException


def panda_to_json(data):
    data_frame = data.to_json(orient="records")
    json_data = json.loads(data_frame)
    return json_data


def numpy_to_list(data):
    return data.tolist()  # Convert the numpy array to a Python list


def get_closing_summary(predicted_close):
    return {
        "min_close": round(min(predicted_close), 2),
        "mean_close": round(sum(predicted_close) / len(predicted_close), 2),
        "max_close": round(max(predicted_close), 2),
    }


async def prediction_handler(session_handler):
    response = call_api(session_handler=session_handler)
    assembled_data, ml_data = assemble_data(response)

    # Create a StockPricePredictor instance
    stock_predictor = StockPricePredictor(ml_data)
    X_train, X_test, y_train, y_test = stock_predictor.split_data()

    # Extract the last 10 data points for prediction (sample_data)
    sample_data = get_last_10_data_points(ml_data)

    # Train and predict using Random Forest
    await stock_predictor.train_random_forest(X_train, y_train)
    predicted_rf = stock_predictor.predict_random_forest(sample_data)

    # Train and predict using Linear Regression
    await stock_predictor.train_linear_regression(X_train, y_train)
    predicted_lr = stock_predictor.predict_linear_regression(sample_data)

    response = {
        "predicted_close_rf": get_closing_summary(numpy_to_list(predicted_rf)),
        "predicted_close_lr": get_closing_summary(numpy_to_list(predicted_lr)),
        "demark_data": panda_to_json(assembled_data.tail(100))
    }

    return ResponseModel(**response)
