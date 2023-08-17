import yfinance as yf
import datetime

# Define the stock symbols
stock_symbols = ['AAPL','AMZN', 'BA', 'GOOG', 'IBM','MGM','T', '^GSPC']  # Add more symbols as needed

# Define the date range from 2013-01-01 to 2023-08-16
start_date = datetime.datetime(2013, 1, 1)
end_date = datetime.datetime(2023, 8, 16)

# Fetch historical stock data
stock_data = yf.download(stock_symbols, start=start_date, end=end_date)

# Select the 'Open' column for each stock
open_prices = stock_data['Open']

# Order the data from earliest to latest
open_prices_sorted = open_prices.sort_index()

# Save the open prices to a CSV file
csv_filename = 'stock_open_prices.csv'
open_prices_sorted.to_csv(csv_filename)

print(f"Open prices (sorted) from 2013 to 2023 saved to {csv_filename}")
