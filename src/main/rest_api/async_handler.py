# import asyncio

# async def train_and_predict_models(stock_predictor, X_train, y_train, sample_data):
#     # Train Random Forest model
#     task_rf = asyncio.create_task(stock_predictor.train_random_forest(X_train, y_train))

#     # Train Linear Regression model
#     task_lr = asyncio.create_task(stock_predictor.train_linear_regression(X_train, y_train))

#     await asyncio.gather(task_rf, task_lr)  # Wait for both models to finish training

#     # Predict using both models
#     predicted_rf = stock_predictor.predict_random_forest(sample_data)
#     predicted_lr = stock_predictor.predict_linear_regression(sample_data)

#     return predicted_rf, predicted_lr

# def prediction_handler(session_handler, model_type="random_forest"):
#     response = call_api(session_handler=session_handler)
#     assembled_data, ml_data = assemble_data(response)

#     # Create a StockPricePredictor instance
#     stock_predictor = StockPricePredictor(ml_data)
#     X_train, X_test, y_train, y_test = stock_predictor.split_data()

#     # Extract the last 10 data points for prediction (sample_data)
#     sample_data = get_last_10_data_points(ml_data)

#     if model_type == "random_forest":
#         # Use asyncio to train and predict with both models in parallel
#         predicted_rf, predicted_lr = asyncio.run(
#             train_and_predict_models(stock_predictor, X_train, y_train, sample_data)
#         )

#         response = {
#             "predicted_close_rf": get_closing_summary(numpy_to_list(predicted_rf)),
#             "predicted_close_lr": get_closing_summary(numpy_to_list(predicted_lr)),
#             "demark_data": panda_to_json(assembled_data)
#         }
#     elif model_type == "linear_regression":
#         # Train and predict with Linear Regression model
#         await stock_predictor.train_linear_regression(X_train, y_train)
#         predicted_close = stock_predictor.predict_linear_regression(sample_data)

#         response = {
#             "predicted_close_lr": get_closing_summary(numpy_to_list(predicted_close)),
#             "demark_data": panda_to_json(assembled_data)
#         }
#     else:
#         raise ValueError("Invalid model_type. Choose 'random_forest' or 'linear_regression'.")

#     return ResponseModel(**response)
