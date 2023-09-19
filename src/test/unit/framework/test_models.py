import pytest
from datetime import datetime
from src.main.framework.models import QueryParams, RequestModel  # Replace 'your_module' with the actual module name where your models are defined

# Fixture to create a QueryParams instance
@pytest.fixture
def query_params():
    return QueryParams(symbol="AAPL", start_date="2023-09-10")

# Fixture to create a RequestModel instance
@pytest.fixture
def request_model(query_params):
    return RequestModel(query_params=query_params, trackingId="12345")

# Test functions can now use these fixtures as arguments
def test_calculate_end_date_with_start_date(query_params):
    end_date = query_params.calculate_end_date()
    expected_end_date = "2023-09-20"
    assert end_date == expected_end_date

def test_calculate_end_date_without_start_date(query_params):
    params = QueryParams(symbol="AAPL")
    end_date = params.calculate_end_date()
    today = datetime.today().strftime("%m-%d-%Y")
    assert end_date == today

def test_uppercase_symbol(request_model):
    assert request_model.query_params.symbol == "AAPL"
