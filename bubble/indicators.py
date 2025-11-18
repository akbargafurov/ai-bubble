import numpy as np
import pandas as pd


def calculate_returns(fin_data, log_returns=False):
    """
    Calculate daily returns from financial data on a percentage change basis.

    Parameters:
        fin_data (pd.DataFrame): pandas DataFrame of closing prices indexed by date.
        log_returns (bool, optional): If True, calculates log returns instead of simple returns. Otherwise, defaults to False.

    Returns:
        pd.DataFrame: pandas DataFrame of daily returns.
    """

    # handle cases where no data exists
    if fin_data.empty:
        raise ValueError(f"Input financial data is empty.")

    # calculate daily percentage returns
    if log_returns:
        returns = fin_data.apply(lambda x: np.log(x) - np.log(x.shift(1))).dropna()
    else:
        returns = fin_data.pct_change().dropna()

    return returns


def calculate_rolling_volatility(returns, window=60):
    """
    Calculate rolling volatility of returns over a specific window.
    
    Parameters:
        returns (pd.DataFrame): pandas DataFrame of daily returns indexed by date.
        window (int, optional): rolling window size in number of days. Defaults to 60 days.
        
        
    Returns:
        pd.DataFrame: pandas DataFrame of rolling volatility values indexed by date.
    """

    # handle cases where no data exists
    if returns.empty:
        raise ValueError(f"Input data on returns is empty.")
    
    # handle cases where there are not enough data points
    if len(returns) < window:
        raise ValueError(f"Not enough data points to compute rolling volatility with window size {window}.")
    
    # calculate rolling volatility (standard deviation) for each stock
    rolling_volume = returns.rolling(window=window).std() * (252 ** 0.5)

    return rolling_volume