import numpy as np
import pandas as pd


def calculate_returns(close, log_returns=False):
    """
    Calculate daily returns from closing prices.

    Parameters:
        close (pd.DataFrame): DataFrame of closing prices indexed by date.
        log_returns (bool, optional): 
            If True, calculates log returns instead of simple returns. 
            Else, defaults to False.

    Returns:
        pd.DataFrame: DataFrame of daily returns.
    """

    # handle cases where no data exists
    if close.empty:
        raise ValueError(f"Input financial data is empty.")

    # calculate daily returns (logarithmic or simple)
    if log_returns:
        returns = np.log(close / close.shift(1)).dropna()
    else:
        returns = close.pct_change().dropna()

    return returns


def calculate_index_returns(index, log_returns=False):
    """
    Calculate daily returns from closing prices (index level).

    Parameters:
        index (pd.DataFrame): Series of index level indexed by date.
        log_returns (bool, optional): 
            If True, calculates log returns instead of simple returns. 
            Else, defaults to False.

    Returns:
        pd.Series: Series of index level returns.
    """

    # handle cases where no data exists
    if index.empty:
        raise ValueError(f"Index level series is empty.")

    # calculate daily returns (logarithmic or simple)
    if log_returns:
        returns = np.log(index / index.shift(1)).dropna()
    else:
        returns = index.pct_change().dropna()

    return returns


def calculate_rolling_volatility(returns, window=60):
    """
    Calculate rolling volatility of returns over a specific window.
    
    Parameters:
        returns (pd.DataFrame): DataFrame of daily returns indexed by date.
        window (int, optional): rolling window size in trading days. Defaults to 60 days.
           
    Returns:
        pd.DataFrame: DataFrame of rolling volatility values indexed by date.
    """

    # handle cases where no data exists
    if returns.empty:
        raise ValueError(f"Input data on returns is empty.")
    
    # handle cases where there are not enough data points
    if len(returns) < window:
        raise ValueError(
            f"Not enough data points to compute rolling volatility "
            f"with window size {window}."
        )
    
    # calculate rolling volatility for each stock
    rolling_volatility = returns.rolling(window=window).std() * np.sqrt(252.0)

    return rolling_volatility


def calculate_rolling_correlation(returns, window=60):
    """
    Calculate the average rolling correlation of returns over a specific window.

    Parameters:
        returns (pd.DataFrame): DataFrame of daily returns indexed by date.
        window (int, optional): rolling window size in number of days. Defaults to 60 days.

    Returns:
        pd.Series: Series of average rolling correlation indexed by date.
    """

    # handle cases where no data exists
    if returns.empty:
        raise ValueError(f"Input data on returns is empty.")
    
    # handle cases with less than two columns
    if returns.shape[1] < 2:
        raise ValueError(
            f"At least two columns of stocks are required to compute correlation."
        )
    
    # handle cases where there are not enough data points
    if len(returns) < window:
        raise ValueError(
            f"Not enough data points to compute rolling volatility "
            f"with window size {window}."
        )
    
    # calculate rolling correlation for each pair of stocks
    rolling_corr = returns.rolling(window=window).corr()

    # group by dates and average correlations across all pairs
    rolling_corr_mean = rolling_corr.groupby(level=0).mean()

    # calculate mean correlation across pairs of stocks
    mean_corr = rolling_corr_mean.mean(axis=1)

    return mean_corr