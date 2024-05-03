import pytest
import yfinance as yf
from stock_analysis.comparison_analysis import compare_two_stocks


@pytest.fixture(scope="module")
def stock_data():
    """Fetches real stock data for use in tests."""
    data_aapl = yf.download('AAPL', start='2021-01-01', end='2021-12-31')
    data_googl = yf.download('GOOGL', start='2021-01-01', end='2021-12-31')
    return data_aapl, data_googl


def test_compare_two_stocks_successful(stock_data):
    """Test that compare_two_stocks can execute without exceptions with valid data."""
    data_aapl, data_googl = stock_data
    try:
        compare_two_stocks('AAPL', 'GOOGL', '2021-01-01', '2021-12-31')
        assert True
    except Exception as e:
        pytest.fail(f"Function should not have raised an exception: {e}")


def test_empty_data_handling():
    """Test how compare_two_stocks handles cases where no data is available."""
    empty_data = yf.download('INVALID', start='2021-01-01', end='2021-12-31')
    with pytest.raises(ValueError, match="no data available for the given dates"):
        compare_two_stocks('INVALID', 'INVALID', '2021-01-01', '2021-12-31')


def test_invalid_dates():
    """Test that compare_two_stocks raises an error with invalid date formats."""
    invalid_date = '2021-31-12'  # Incorrect format, should be YYYY-MM-DD
    with pytest.raises(ValueError, match="time data .* does not match format"):
        compare_two_stocks('AAPL', 'GOOGL', invalid_date, '2021-12-31')
