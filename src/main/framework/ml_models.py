"""
Define Machine Learning models for training .
"""
import asyncio
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from pandas.api.types import CategoricalDtype



class StockPricePredictor:
    def __init__(self, data, config={}):
        """
        Initialize the StockPricePredictor.

        Args:
            data (DataFrame): DataFrame containing columns like 
            "open," "high," "low," "close," "volume," and DeMark indicators.
        """
        self.data = data
        self.config = config

        if self.config.get('demark', False):
            self.feature_names = ["open", "high",
                                  "low", "volume", "setup", "countdown"]
        else:
            self.feature_names = ["open", "high", "low", "volume"]

        
        self.features = data[self.feature_names]
        self.target = data["close"]  # Target variable
    
    # def get_categorical_columns(self):
    #     categorical_columns = self.features # Update with your actual categorical column names
    #     data = pd.get_dummies(self.data, columns=categorical_columns)
        
    #     categorical_columns = [self.feature_names]
    #     for column in categorical_columns:
    #         self.data[column] = self.data[column].astype(CategoricalDtype())


    def add_demarker_indicators(self):
        self.data['setup'] = 0
        self.data['countdown'] = 0

        data = self.data.copy()  # Create a copy of the DataFrame
        for i in range(1, len(data)):
            if np.isnan(data['high'].iloc[i]) or np.isnan(data['low'].iloc[i]):
                continue

            if data['high'].iloc[i] < data['high'].iloc[i - 1]:
                data['setup'].iloc[i] = max(
                    data['high'].iloc[i - 1] - data['low'].iloc[i], 0)
            else:
                data['setup'].iloc[i] = 0

            if data['low'].iloc[i] > data['low'].iloc[i - 1]:
                data['countdown'].iloc[i] = max(
                    data['high'].iloc[i - 1] - data['low'].iloc[i], 0)
            else:
                data['countdown'].iloc[i] = 0

        self.data = data  
        
    def split_data(self, test_size=0.2, random_state=42):
        """
        Split data into training and testing sets.

        Args:
            test_size (float, optional): Fraction of data to reserve for testing. Default is 0.2.
            random_state (int, optional): Random seed for reproducibility. Default is 42.

        Returns:
            Tuple: X_train, X_test, y_train, y_test
        """
        X_train, X_test, y_train, y_test = train_test_split(
            self.features, self.target, test_size=test_size, random_state=random_state
        )
        return X_train, X_test, y_train, y_test

    async def train_and_evaluate_model(self, model, X_train, y_train, X_test, y_test, n_estimators=None, random_state=None):
        if n_estimators is not None and isinstance(model, RandomForestRegressor):
            model.set_params(n_estimators=n_estimators, random_state=random_state)

        await asyncio.to_thread(model.fit, X_train, y_train)
        metrics = self.evaluate_model(model, X_test, y_test)
        return metrics

    def evaluate_model(self, model, X_test, y_test):
        """
        Evaluate the trained model on the test data.

        Args:
            model (RandomForestRegressor): The trained RandomForestRegressor model.
            X_test (array-like): Test feature matrix.
            y_test (array-like): True target values for the test data.

        Returns:
            dict: Dictionary containing evaluation metrics.
        """
        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        return {
            "mean_squared_error": mse,
            "r_squared": r2
        }


    # Train models
    async def train_random_forest(self, X_train, y_train, X_test, y_test, n_estimators=100, random_state=42):
        self.rf_model = RandomForestRegressor()
        metrics = await self.train_and_evaluate_model(self.rf_model, X_train, y_train, X_test, y_test, n_estimators, random_state)
        return metrics

    async def train_linear_regression(self, X_train, y_train, X_test, y_test):
        self.lr_model = LinearRegression()
        metrics = await self.train_and_evaluate_model(self.lr_model, X_train, y_train, X_test, y_test)
        return metrics

    async def train_xgboost(self, X_train, y_train, X_test, y_test, n_estimators=100, learning_rate=0.1, max_depth=3):
        # self.get_categorical_columns()
        self.xgb_model = xgb.XGBRegressor(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth)
        metrics = await self.train_and_evaluate_model(self.xgb_model, X_train, y_train, X_test, y_test)
        return metrics

    # Predict Models
    def predict_random_forest(self, sample_data):
        x_new = sample_data[self.feature_names].values
        return self.rf_model.predict(x_new)

    def predict_linear_regression(self, sample_data):
        x_new = sample_data[self.feature_names].values
        return self.lr_model.predict(x_new)

    def predict_xgboost(self, sample_data):
        x_new = sample_data[self.feature_names].values
        return self.xgb_model.predict(x_new)
