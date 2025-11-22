import matplotlib.pyplot as plt
import seaborn as sns


def plot_correlation_matrix(returns):
    """
    Plot the correlation matrix of stock returns.
    
    Parameters:
        returns (pd.DataFrame): pandas DataFrame of daily returns indexed by date.
    
    Returns:
        None"""

    # plot correlation matrix of returns
    corr_matrix = returns.corr()

    # create a heatmap with specified settings
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('correlation matrix of AI stock returns')
    plt.show()