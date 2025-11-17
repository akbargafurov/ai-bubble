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