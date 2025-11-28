import matplotlib.pyplot as plt
import seaborn as sns


def plot_correlation_matrix(returns):
    """
    Plot the correlation matrix of stock returns.
    
    Parameters:
        returns (pd.DataFrame): pandas DataFrame of daily returns indexed by date.
    
    Returns:
        None
    """

    # plot correlation matrix of returns
    corr_matrix = returns.corr()

    # create a heatmap with specified settings
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('correlation matrix of AI stock returns')
    plt.tight_layout()
    plt.show()


def plot_rolling_correlation(rolling_corr):
    """
    Plot the rolling average correlation of stock returns.
    Parameters:
        rolling_corr (pd.Series): pandas Series of rolling average correlations indexed by date.
        
    Returns:
        None
    """

    # create a line plot with specified settings
    plt.figure(figsize=(10, 6))
    plt.plot(rolling_corr, color='purple', label='average 60 days rolling correlation')
    plt.axhline(y=0.5, color='gray', linestyle='--')
    
    plt.title('60-day rolling average correlation among AI stocks')
    plt.ylabel('average correlation')
    plt.xlabel('date')
    
    plt.legend()
    plt.tight_layout()
    plt.show()