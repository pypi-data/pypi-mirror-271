import pytest
import yfinance as yf
from stock_analysis.performance_metrics import sharpe_ratio


@pytest.fixture(scope="module")
def stock_returns():
    data = yf.download('AAPL', start='2021-01-01', end='2021-12-31')
    return data['Adj Close'].pct_change().dropna()


def test_sharpe_ratio(stock_returns):
    ratio = sharpe_ratio(stock_returns)
    assert isinstance(ratio, float)
