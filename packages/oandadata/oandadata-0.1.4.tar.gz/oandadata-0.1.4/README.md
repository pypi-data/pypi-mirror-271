# Financial Data Retrieval Library


# oandadata

`oandadata` is a Python library designed to retrieve financial data from the OANDA API. It provides a simple and efficient way to access candle data for a specified currency pair.

## Features

- **Easy-to-use API**: With just a few lines of code, you can retrieve candle data for any currency pair available on the OANDA platform.
- **Flexible Parameters**: You can specify the number of candles to retrieve, the timeframe for each candle, the type of price data to retrieve, and the currency pair.
- **Pandas Integration**: The retrieved data is returned as a pandas DataFrame, making it easy to analyze and manipulate the data.

## Example

Here's an example of how you can use `oandadata` to retrieve candle data:

```python
import oandadata

# Define your parameters
token = 'your_api_token'
count = 100
timeframe = 'H1'
price_type = 'MBA'
currency_pair = 'XAU_CAD'

# Retrieve the candle data
df = oandadata.get_candles(token, count, timeframe, price_type, currency_pair)

# Now 'df' is a DataFrame containing the candle data

