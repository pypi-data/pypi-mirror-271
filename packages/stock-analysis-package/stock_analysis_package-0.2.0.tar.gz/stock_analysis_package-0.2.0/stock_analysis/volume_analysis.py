import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


def plot_volume(stock_data, column='Volume'):
    """Plot trading volume."""
    try:
        plt.figure(figsize=(10, 5))
        plt.bar(stock_data.index, stock_data[column], color='blue')
        plt.title('Trading Volume Over Time')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.grid(True)
        plt.show()
    except Exception as e:
        logger.error(f"Error calculating volatility: {str(e)}", exc_info=True)
        raise
