import numpy as np

def calculate_volatility(stock_data, column='Close'):
    """Calculate rolling volatility of stock prices."""
    log_returns = np.log(stock_data[column] / stock_data[column].shift(1))
    return log_returns.rolling(window=252).std() * np.sqrt(252)  # Annualized volatility
