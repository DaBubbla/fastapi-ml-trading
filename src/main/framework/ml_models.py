"""
Define Machine Learning models for training .
"""
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor  # Use RandomForestRegressor for regression tasks

def rm_regressor(data, test_size=0.2, random_state=42):
    """
    Split data into training and testing sets and train a regression model.

    Args:
        data (DataFrame): DataFrame containing columns like "open," "high," "low," "close," and "volume."
        test_size (float, optional): Fraction of data to reserve for testing. Default is 0.2.
        random_state (int, optional): Random seed for reproducibility. Default is 42.

    Returns:
        Tuple: trained_model, X_train, X_test, y_train, y_test
    """
    # Extract features from the DataFrame
    features = data[["open", "high", "low", "volume"]]  # Removing "close" as it's the target variable

    # Extract the target variable ("close" price)
    target = data["close"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=test_size, random_state=random_state)

    # Initialize and train the regression model (RandomForestRegressor)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    sample = data.tail(1)
    # Extract values from the Series and create a list for prediction
    x_new = [[
        sample["open"].values[0], 
        sample["high"].values[0], 
        sample["low"].values[0], 
        sample["volume"].values[0]
        ]]

    # Make the prediction
    predicted_close_price = model.predict(x_new)

    return predicted_close_price#, X_train, X_test, y_train, y_test
