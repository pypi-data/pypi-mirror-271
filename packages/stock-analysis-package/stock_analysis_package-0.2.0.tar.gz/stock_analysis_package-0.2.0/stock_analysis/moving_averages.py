import matplotlib.pyplot as plt
import logging

# Set up logging specifically for this module
logger = logging.getLogger(__name__)


def calculate_moving_average(stock_data, window_size=20, column='Close'):
    """Calculate moving averages for the given window size."""
    try:
        return stock_data[column].rolling(window=window_size).mean()
    except Exception as e:
        logger.error(f"Error calculating volatility: {str(e)}", exc_info=True)
        raise


def plot_moving_averages(stock_data, window_sizes=None, column='Close'):
    """Plot stock prices with moving averages."""

    try:
        if window_sizes is None:
            window_sizes = [20, 50, 200]

        plt.figure(figsize=(10, 5))
        plt.plot(stock_data.index, stock_data[column], label='Stock Price')
        for window in window_sizes:
            moving_avg = calculate_moving_average(stock_data, window, column)
            plt.plot(stock_data.index, moving_avg, label=f'{window}-day MA')
        plt.title('Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.grid(True)
        plt.show()
    except Exception as e:
        logger.error(f"Error calculating volatility: {str(e)}", exc_info=True)
        raise
