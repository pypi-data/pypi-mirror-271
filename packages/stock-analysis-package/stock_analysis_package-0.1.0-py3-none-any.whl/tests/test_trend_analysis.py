import pandas as pd
import pytest
from stock_analysis.trend_analysis import plot_linear_trend

@pytest.fixture
def sample_stock_data():
    """Sample stock data for testing."""
    data = {
        'Date': pd.date_range(start='2022-01-01', periods=10),
        'Close': [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
    }
    return pd.DataFrame(data)

def test_plot_linear_trend(sample_stock_data):
    """Test that the plot_linear_trend function does not raise an error."""
    assert plot_linear_trend(sample_stock_data) is None  # Assuming it either plots or raises an error
