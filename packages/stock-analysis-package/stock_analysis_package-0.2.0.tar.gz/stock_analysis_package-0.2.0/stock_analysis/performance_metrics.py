import numpy as np
import logging

logger = logging.getLogger(__name__)


def sharpe_ratio(stock_returns, risk_free_rate=0.01):
    """Calculate the Sharpe ratio for a stock or portfolio."""
    try:
        excess_returns = stock_returns - risk_free_rate
        return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
    except Exception as e:
        logger.error(f"Error calculating volatility: {str(e)}", exc_info=True)
        raise
