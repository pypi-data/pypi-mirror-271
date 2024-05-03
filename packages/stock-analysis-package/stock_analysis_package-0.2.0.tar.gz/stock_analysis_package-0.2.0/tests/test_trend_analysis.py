import pytest
import yfinance as yf
from stock_analysis.trend_analysis import plot_linear_trend


@pytest.fixture(scope="module")
def stock_data():
    return yf.download('AAPL', start='2021-01-01', end='2021-12-31')


def test_plot_linear_trend(stock_data):
    assert plot_linear_trend(stock_data) is None
