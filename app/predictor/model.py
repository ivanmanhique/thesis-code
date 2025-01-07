import yfinance as yf
import numpy as np
import joblib
from keras._tf_keras.keras.models import load_model
import matplotlib.pyplot as plt
import pandas as pd
import io
import os

# Get the directory of the current file (predictor.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the absolute path to scaler.pkl
scaler_path = os.path.join(current_dir, '../../data/scaler.pkl')
model_path = os.path.join(current_dir, '../../data/model.h5')
# Load the scaler and app
scaler = joblib.load(scaler_path)
model = load_model(model_path)

def forecast(number_of_days_to_forecast: int) ->io.BytesIO :
    """
    Generate a stock price forecast plot and return it as a BytesIO object.
    """
    # Fetch the last 60 days of data from yfinance
    symbol = 'AAPL'  # Replace with the desired stock symbol
    last_60_days_data = yf.download(symbol, period='3mo', interval='1d')

    # Ensure we are only working with the 'Close' column
    last_3_months = last_60_days_data['Close'].values.reshape(-1, 1)

    # Scale the data using the saved scaler
    scaled_last_3_mo = scaler.transform(last_3_months)

    # Reshape to match the app's input shape
    input_data = np.reshape(scaled_last_3_mo, (1, scaled_last_3_mo.shape[0], 1))

    # Forecast the specified number of days
    forecasted_prices = []
    num_rows = input_data.shape[1]

    for _ in range(number_of_days_to_forecast):
        predicted_price_scaled = model.predict(input_data)
        predicted_price = scaler.inverse_transform(predicted_price_scaled)[0, 0]
        forecasted_prices.append(predicted_price)
        new_input_data = np.append(input_data[0, 1:, 0], predicted_price_scaled[0, 0])
        input_data = np.reshape(new_input_data, (1, num_rows, 1))

    # Prepare data for plotting
    actual_prices = last_3_months.flatten()
    forecasted_prices = np.array(forecasted_prices)
    combined_prices = np.concatenate((actual_prices, forecasted_prices))

    # Compute moving averages
    moving_average_10 = pd.Series(combined_prices).rolling(window=10).mean()
    moving_average_20 = pd.Series(combined_prices).rolling(window=20).mean()
    moving_average_50 = pd.Series(combined_prices).rolling(window=50).mean()

    # Create the plot
    plt.figure(figsize=(12, 6))
    actual_indices = list(range(1, len(actual_prices) + 1))
    forecast_indices = list(range(len(actual_prices), len(actual_prices) + len(forecasted_prices)))

    plt.plot(actual_indices, actual_prices, label=f'Actual Prices', linewidth=2)
    plt.plot(forecast_indices, forecasted_prices, label='Forecasted Prices', linewidth=2)
    plt.plot(range(1, len(combined_prices) + 1), moving_average_10, label='10-Day MA', color='orange', linestyle='--')
    plt.plot(range(1, len(combined_prices) + 1), moving_average_20, label='20-Day MA', color='green', linestyle='--')
    plt.plot(range(1, len(combined_prices) + 1), moving_average_50, label='50-Day MA', color='purple', linestyle='--')

    plt.title('Stock Prices: Actual, Forecasted, and Moving Averages', fontsize=16)
    plt.xlabel('Days', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.legend()
    plt.grid()

    # Save plot to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf
