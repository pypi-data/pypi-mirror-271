import pytest
import yfinance as yf
from stock_analysis.volume_analysis import plot_volume


@pytest.fixture(scope="module")
def stock_data():
    return yf.download('AAPL', start='2021-01-01', end='2021-12-31')


def test_plot_volume(stock_data):
    plot_volume(stock_data)
