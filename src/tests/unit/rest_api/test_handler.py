import json
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from src.main.framework.models import ResponseModel
from src.main.rest_api.handler import (
    get_response,
    call_api,
    panda_to_json,
    numpy_to_list,
    get_closing_summary,
    prediction_handler,
)


class TestHandler:

    @pytest.fixture
    def mock_response(self):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"example_key": "example_value"}
        return response

    @patch("requests.get")
    def test_get_response(self, mock_get, mock_response):
        mock_get.return_value = mock_response
        result = get_response(url="http://example.com")
        assert result.status_code == 200

    @pytest.fixture
    def mock_session_handler(self):
        session_handler = Mock()
        session_handler.config = {
            "alphavantage_url": "http://example.com",
            "alphavantage_api_key": "your_api_key",
        }
        session_handler.req_body.query_params.symbol = "AAPL"
        return session_handler

    @patch("requests.get")
    def test_call_api(self, mock_get, mock_response, mock_session_handler):
        mock_get.return_value = mock_response
        result = call_api(session_handler=mock_session_handler)
        assert result.status_code == 200

    def test_panda_to_json(self):
        df = {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}
        result = panda_to_json(pd.DataFrame(df))
        assert result == [{"column1": 1, "column2": "a"}, {"column1": 2, "column2": "b"}, {"column1": 3, "column2": "c"}]

    def test_numpy_to_list(self):
        np_array = np.array([1, 2, 3])
        result = numpy_to_list(np_array)
        assert result == [1, 2, 3]

    def test_get_closing_summary(self):
        predicted_close = [10.5, 12.3, 9.8, 11.2]
        result = get_closing_summary(predicted_close)
        assert result == {"min_close": 9.8, "mean_close": 11.2, "max_close": 12.3}

    @patch("src.main.rest_api.handler.call_api")
    @patch("src.main.rest_api.handler.assemble_data")
    @patch("src.main.rest_api.handler.get_last_10_data_points")
    @patch("src.main.rest_api.handler.StockPricePredictor")
    def test_prediction_handler(
        self, mock_stock_predictor, mock_last_10_data_points, mock_assemble_data, mock_call_api
    ):
        # Mock the necessary dependencies and data
        session_handler = Mock()
        session_handler.state.config = Mock()
        mock_call_api.return_value = Mock()
        mock_assemble_data.return_value = (Mock(), Mock())
        mock_last_10_data_points.return_value = Mock()
        mock_stock_predictor_instance = mock_stock_predictor.return_value
        mock_stock_predictor_instance.predict_random_forest.return_value = [10.5, 12.3, 9.8, 11.2]
        mock_stock_predictor_instance.predict_linear_regression.return_value = [9.7, 11.1, 10.0, 12.0]

        # Call the prediction_handler function
        result = prediction_handler(session_handler=session_handler)

        # Assert the expected ResponseModel
        expected_response = ResponseModel(
            predicted_close_rf={"min_close": 9.8, "mean_close": 11.2, "max_close": 12.3},
            predicted_close_lr={"min_close": 9.7, "mean_close": 10.95, "max_close": 12.0},
            demark_data=Mock(),
        )
        assert result == expected_response
