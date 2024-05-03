import pytest
import yfinance as yf
from stock_analysis.moving_averages import calculate_moving_average, plot_moving_averages


@pytest.fixture(scope="module")
def stock_data():
    """Fixture to download AAPL stock data for the year 2021."""
    return yf.download('AAPL', start='2021-01-01', end='2021-12-31')


def test_calculate_moving_average(stock_data):
    """Test that the moving average length matches the stock data length, and it calculates correctly."""
    window_size = 20
    moving_avg = calculate_moving_average(stock_data, window_size=window_size, column='Close')
    assert len(moving_avg) == len(stock_data), "The length of the moving average result should match the input data " \
                                               "length."
    assert not moving_avg.isna().all(), "The moving average should not be all NaNs."

    # Test the first non-NaN value to ensure the moving average starts correctly
    first_valid_index = moving_avg.first_valid_index()
    calculated_first_ma = moving_avg.loc[first_valid_index]
    expected_first_ma = stock_data['Close'].iloc[:window_size].mean()
    assert calculated_first_ma == expected_first_ma, "The first calculated moving average is incorrect."


def test_plot_moving_averages(stock_data):
    """Test plotting of moving averages does not raise exceptions."""
    try:
        plot_moving_averages(stock_data, window_sizes=[20, 50, 200], column='Close')
    except Exception as e:
        pytest.fail(f"plot_moving_averages raised an exception: {e}")
