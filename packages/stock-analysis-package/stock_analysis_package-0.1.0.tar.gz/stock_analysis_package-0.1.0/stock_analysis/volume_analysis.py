import matplotlib.pyplot as plt

def plot_volume(stock_data, column='Volume'):
    """Plot trading volume."""
    plt.figure(figsize=(10, 5))
    plt.bar(stock_data.index, stock_data[column], color='blue')
    plt.title('Trading Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.grid(True)
    plt.show()
