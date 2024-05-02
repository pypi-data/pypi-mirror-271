import numpy as np
import pytest
from stock_analysis.performance_metrics import sharpe_ratio

@pytest.fixture
def sample_stock_returns():
    """Sample stock returns for testing."""
    return np.random.normal(loc=0.001, scale=0.02, size=100)

def test_sharpe_ratio(sample_stock_returns):
    """Test sharpe_ratio function."""
    ratio = sharpe_ratio(sample_stock_returns)
    assert isinstance(ratio, float)
