"""
Main handler for API requests.
"""
import os

import requests

from src.main.framework.exceptions import (
    RequestBodyException, DownstreamException
)



def get_response(session_handler={}, url=""):
    """
    Calls the API and returns the response.
    Params:
        session_handler (SessionHandler): The session object containing 
        configs/request/etc.
    Returns:
        JSON: The JSON response.
    """
    response = requests.get(url)

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
        url = session_handler.config.get("url", "")
        response = get_response(session_handler=session_handler, url=url)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RequestBodyException

