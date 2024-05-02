import pandas as pd
import pytest
from stock_analysis.volume_analysis import plot_volume

@pytest.fixture
def sample_stock_data():
    """Sample stock data for testing."""
    data = {
        'Date': pd.date_range(start='2022-01-01', periods=10),
        'Volume': [1000, 1200, 1300, 1500, 1400, 1600, 1700, 1800, 1900, 2000]
    }
    return pd.DataFrame(data)

def test_plot_volume(sample_stock_data):
    """Test plot_volume function."""
    plot_volume(sample_stock_data)
