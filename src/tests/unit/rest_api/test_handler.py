import json
import pytest
from unittest.mock import Mock
from src.main.rest_api.handler import (
    get_response,
    call_api,
    panda_to_json,
    numpy_to_list,
    get_closing_summary,
    prediction_handler
)


# Mock the requests module for testing
@pytest.fixture(autouse=True)
def mock_requests_get(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, content, status_code):
                self.content = content
                self.status_code = status_code

            def json(self):
                return json.loads(self.content)

        return MockResponse("{'data': 'sample data'}", 200)

    monkeypatch.setattr("requests.get", mock_get)

@pytest.fixture(autouse=True)
def mock_response(mock_get):


# Write test functions for each function in handler.py
def test_get_response():
    # Your test cases for get_response function


def test_call_api():
    # Your test cases for call_api function


def test_panda_to_json():
    # Your test cases for panda_to_json function


def test_numpy_to_list():
    # Your test cases for numpy_to_list function


def test_get_closing_summary():
    # Your test cases for get_closing_summary function


def test_prediction_handler():
    # Your test cases for prediction_handler function
