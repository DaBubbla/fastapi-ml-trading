from fastapi.testclient import TestClient
from src.main.application import app

# Create a TestClient instance
client = TestClient(app)

def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello from the other side.",
        "version": "0.0.0"
    }

def test_predict_stock_price(mock_app_config):
    # You can write similar tests for the /predict endpoint
    query_params = {
        "symbol": "AAPL",
        "start_date": "09-10-2023"
    }
    headers = {
        "trackingId": "12345"
    }
    response = client.get(
        "/predict",
        params=query_params,
        headers=headers
    )
    assert response.status_code == 200
    # Add more assertions based on the expected response data

# Add more test functions for other endpoints as needed
