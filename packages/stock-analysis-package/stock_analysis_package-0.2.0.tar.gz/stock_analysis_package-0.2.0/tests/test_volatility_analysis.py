import pytest
import yfinance as yf
from stock_analysis.volatility_analysis import calculate_volatility


@pytest.fixture(scope="module")
def stock_data():
    return yf.download('AAPL', start='2021-01-01', end='2021-12-31')


def test_calculate_volatility(stock_data):
    volatility = calculate_volatility(stock_data, column='Close')
    assert len(volatility) == len(stock_data)
