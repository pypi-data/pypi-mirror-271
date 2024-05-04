import requests
import pandas as pd

def get_candles(token, count, timeframe, price_type, currency_pair):
    """
    Retrieves candle data for a specified currency pair.

    Args:
        token (str): Personal access token for the API.
        count (int): Number of candles to retrieve.
        timeframe (str): Timeframe for each candle.
        price_type (str): Type of price data to retrieve (e.g., 'MBA' for Midpoint, Bid, and Ask).
        currency_pair (str): The currency pair to retrieve data for (e.g., 'XAU_CAD').

    Returns:
        pd.DataFrame: DataFrame containing the candle data.
    """
    # Define the API endpoint
    url = f'https://api-fxtrade.oanda.com/v3/instruments/{currency_pair}/candles'

    # Define the headers for the HTTP request
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Define the parameters for the query
    params = {
        'count': count,
        'granularity': timeframe,
        'price': price_type
    }

    # Make the HTTP request
    response = requests.get(url, headers=headers, params=params)

    # Convert the response to JSON
    data = response.json()

    # Extract the candles data
    candles = data['candles']

    # Prepare an empty list to store the candles data
    candles_data = []

    # Populate the list with the candles data
    for candle in candles:
        candles_data.append({
            'time': pd.to_datetime(candle['time']),
            'volume': int(candle['volume']),
            'open': float(candle['mid']['o']),
            'high': float(candle['mid']['h']),
            'low': float(candle['mid']['l']),
            'close': float(candle['mid']['c'])
        })

    # Convert the list into a DataFrame
    df = pd.DataFrame(candles_data)

    # Set the 'time' column as the index
    df.set_index('time', inplace=True)

    return df
