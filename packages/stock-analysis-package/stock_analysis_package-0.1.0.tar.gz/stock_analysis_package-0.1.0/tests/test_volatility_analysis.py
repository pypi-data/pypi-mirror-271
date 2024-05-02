import pandas as pd
import pytest
from stock_analysis.volatility_analysis import calculate_volatility

@pytest.fixture
def sample_stock_data():
    """Sample stock data for testing."""
    data = {
        'Date': pd.date_range(start='2022-01-01', periods=10),
        'Close': [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
    }
    return pd.DataFrame(data)

def test_calculate_volatility(sample_stock_data):
    """Test calculate_volatility function."""
    volatility = calculate_volatility(sample_stock_data)
    assert len(volatility) == len(sample_stock_data)
