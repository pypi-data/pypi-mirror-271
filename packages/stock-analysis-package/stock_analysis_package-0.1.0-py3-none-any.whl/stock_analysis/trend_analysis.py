import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def plot_linear_trend(stock_data, column='Close'):
    """Plot linear trend line of stock prices."""
    stock_data = stock_data.dropna(subset=[column])
    x = np.arange(len(stock_data))
    y = stock_data[column].values
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, y, label='Stock Price')
    plt.plot(stock_data.index, intercept + slope * x, 'r', label='Trend Line')
    plt.title('Stock Price Trend Analysis')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.show()