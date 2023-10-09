import os
from fastapi.testclient import TestClient
from src.main.application import app
from src.main.framework.models import ResponseModel
from src.main.rest_api.handler import prediction_handler
from fastapi import Request
from src.main.middleware import RequestMiddleware
import pytest

# Create a TestClient instance for testing
client = TestClient(app)

# Mocked SessionHandler class
class MockedSessionHandler:
    def __init__(self, config, req_body, app):
        pass

# Mocked prediction_handler function
async def mocked_prediction_handler(session_handler):
    return ResponseModel(predicted_close_rf={}, predicted_close_lr={}, demark_data={})

# Mock the SessionHandler class and prediction_handler function
app.dependency_overrides[RequestMiddleware] = MockedSessionHandler
app.dependency_overrides[prediction_handler] = mocked_prediction_handler

def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from the other side.", "version": "0.0.0"}

@pytest.fixture
def mocked_request():
    request = Request(scope=None, receive=None)
    return request

def test_predict_stock_price(mocked_request):
    response = client.get("/predict", request=mocked_request)
    assert response.status_code == 200
    assert response.json() == {"predicted_close_rf": {}, "predicted_close_lr": {}, "demark_data": {}}

# You can add more test cases for other routes as needed.
