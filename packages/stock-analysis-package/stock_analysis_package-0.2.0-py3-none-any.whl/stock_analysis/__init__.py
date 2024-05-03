import logging

from .trend_analysis import plot_linear_trend
from .moving_averages import calculate_moving_average, plot_moving_averages
from .volume_analysis import plot_volume
from .volatility_analysis import calculate_volatility
from .performance_metrics import sharpe_ratio

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

__all__ = [
    'plot_linear_trend',
    'calculate_moving_average',
    'plot_moving_averages',
    'plot_volume',
    'calculate_volatility',
    'sharpe_ratio'
]