"""
Define Machine Learning models for training .
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

class StockPricePredictor:
    def __init__(self, data):
        """
        Initialize the StockPricePredictor.

        Args:
            data (DataFrame): DataFrame containing columns like "open," "high," "low," "close," "volume," and DeMark indicators.
        """
        self.data = data
        # Include DeMark indicators along with other features
        self.features = data[["open", "high", "low", "volume", "setup", "countdown"]]  
        self.target = data["close"]  # Target variable

    def add_demarker_indicators(self):
        self.data['setup'] = 0
        self.data['countdown'] = 0

        for i in range(1, len(self.data)):
            if np.isnan(self.data['high'].iloc[i]) or np.isnan(self.data['low'].iloc[i]):
                continue

            if self.data['high'].iloc[i] < self.data['high'].iloc[i - 1]:
                self.data['setup'].iloc[i] = max(self.data['high'].iloc[i - 1] - self.data['low'].iloc[i], 0)
            else:
                self.data['setup'].iloc[i] = 0

            if self.data['low'].iloc[i] > self.data['low'].iloc[i - 1]:
                self.data['countdown'].iloc[i] = max(self.data['high'].iloc[i - 1] - self.data['low'].iloc[i], 0)
            else:
                self.data['countdown'].iloc[i] = 0

        

    def split_data(self, test_size=0.2, random_state=42):
        """
        Split data into training and testing sets.

        Args:
            test_size (float, optional): Fraction of data to reserve for testing. Default is 0.2.
            random_state (int, optional): Random seed for reproducibility. Default is 42.

        Returns:
            Tuple: X_train, X_test, y_train, y_test
        """
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.target, test_size=test_size, random_state=random_state)
        return X_train, X_test, y_train, y_test

    def train_model(self, X_train, y_train, n_estimators=100, random_state=42):
        """
        Train a RandomForestRegressor model.

        Args:
            X_train (array-like): Training feature matrix.
            y_train (array-like): Target variable for training.
            n_estimators (int, optional): Number of trees in the forest. Default is 100.
            random_state (int, optional): Random seed for reproducibility. Default is 42.

        Returns:
            RandomForestRegressor: The trained RandomForestRegressor model.
        """
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        model.fit(X_train, y_train)
        return model

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
        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate evaluation metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        return {
            "mean_squared_error": mse,
            "r-squared": r2
        }

    def predict(self, model, sample_data):
        """
        Make predictions using the trained model.

        Args:
            model (RandomForestRegressor): The trained RandomForestRegressor model.
            sample_data (DataFrame): DataFrame containing a single data point for prediction, including DeMark indicators.

        Returns:
            float: Predicted close price.
        """
        # Include DeMark indicators in the prediction
        x_new = sample_data[["open", "high", "low", "volume", "setup", "countdown"]].values
        predicted_close_price = model.predict(x_new)
        return predicted_close_price
