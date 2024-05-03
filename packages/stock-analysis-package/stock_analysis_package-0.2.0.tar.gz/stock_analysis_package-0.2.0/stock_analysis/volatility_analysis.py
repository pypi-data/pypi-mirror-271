import numpy as np
import logging

# Set up logging specifically for this module
logger = logging.getLogger(__name__)


def calculate_volatility(stock_data, column='Close'):
    """Calculate rolling volatility of stock prices."""
    try:
        # Assuming stock_data is a DataFrame with a 'Close' column
        log_returns = np.log(stock_data[column] / stock_data[column].shift(1))
        volatility = log_returns.rolling(window=252).std() * np.sqrt(252)  # Annualized volatility
        return volatility
    except Exception as e:
        logger.error(f"Error calculating volatility: {str(e)}", exc_info=True)
        raise
