import numpy as np

def sharpe_ratio(stock_returns, risk_free_rate=0.01):
    """Calculate the Sharpe ratio for a stock or portfolio."""
    excess_returns = stock_returns - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
