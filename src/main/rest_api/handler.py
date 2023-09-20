"""
Main handler for API requests.
"""
import os

import requests

from src.main.framework.exceptions import (
    RequestBodyException, DownstreamException
)
from src.main.rest_api.helpers import assemble_data



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
        url = session_handler.config.ge("alphavantage_url", "")
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
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RequestBodyException


def prediction_handler(session_handler):

    response = call_api(session_handler=session_handler)

    assemble_data(response)
