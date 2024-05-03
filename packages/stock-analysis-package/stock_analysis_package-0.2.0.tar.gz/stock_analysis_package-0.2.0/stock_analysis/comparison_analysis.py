import yfinance as yf
import matplotlib.pyplot as plt
import logging
from datetime import datetime

# Set up logging specifically for this module
logger = logging.getLogger(__name__)


def compare_two_stocks(stock1, stock2, start_date, end_date):
    """
    Fetches historical price data for two stocks and plots their closing prices for comparison.

    Parameters:
        stock1 (str): The ticker symbol of the first stock.
        stock2 (str): The ticker symbol of the second stock.
        start_date (str): Start date for the data in format 'YYYY-MM-DD'.
        end_date (str): End date for the data in format 'YYYY-MM-DD'.

    Returns:
        None: Plots the data and logs errors if any occur.
    """
    try:
        # Validate date format
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')

        # Fetch data from Yahoo Finance
        data1 = yf.download(stock1, start=start_date, end=end_date)
        data2 = yf.download(stock2, start=start_date, end=end_date)

        # Check if data is empty
        if data1.empty or data2.empty:
            raise ValueError("One of the stock ticker symbols may be incorrect, or no data available for the given "
                             "dates.")

        # Plotting the closing prices
        plt.figure(figsize=(14, 7))
        plt.plot(data1['Close'], label=f'{stock1} Closing Price')
        plt.plot(data2['Close'], label=f'{stock2} Closing Price')
        plt.title('Stock Comparison')
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.legend()
        plt.grid(True)
        plt.show()

    except Exception as e:
        logging.error(f"Failed to fetch or plot data for stocks {stock1} and {stock2}: {str(e)}")
        raise
