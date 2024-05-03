import yfinance as yf
from stock_analysis.trend_analysis import plot_linear_trend
from stock_analysis.moving_averages import plot_moving_averages
from stock_analysis.volume_analysis import plot_volume
from stock_analysis.volatility_analysis import calculate_volatility
from stock_analysis.performance_metrics import sharpe_ratio

# Fetch stock data
stock_data = yf.download('AAPL', start='2021-01-01', end='2021-12-31')

# Plot linear trend
plot_linear_trend(stock_data)

# Plot moving averages
plot_moving_averages(stock_data)

# Plot volume
plot_volume(stock_data)

# Calculate volatility
volatility = calculate_volatility(stock_data)
print("Volatility:", volatility.tail())

# Calculate Sharpe ratio
stock_returns = stock_data['Close'].pct_change().dropna()
sharpe = sharpe_ratio(stock_returns)
print("Sharpe Ratio:", sharpe)
