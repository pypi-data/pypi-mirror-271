import pandas as pd
import pytest
from stock_analysis.moving_averages import calculate_moving_average, plot_moving_averages

@pytest.fixture
def sample_stock_data():
    """Sample stock data for testing."""
    data = {
        'Date': pd.date_range(start='2022-01-01', periods=10),
        'Close': [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
    }
    return pd.DataFrame(data)

def test_calculate_moving_average(sample_stock_data):
    """Test calculate_moving_average function."""
    moving_avg = calculate_moving_average(sample_stock_data)
    assert len(moving_avg) == len(sample_stock_data)

def test_plot_moving_averages(sample_stock_data):
    """Test plot_moving_averages function."""
    plot_moving_averages(sample_stock_data)
