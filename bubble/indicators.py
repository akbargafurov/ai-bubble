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

    Raises:
        ValueError: If the input data is empty.
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

    Raises:
        ValueError: If the input data is empty.
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


def build_equal_weight_index(returns):
    """
    Build an equal-weight index from a panel of returns.

    Parameters:
        returns (pd.DataFrame): DataFrame of returns indexed by date.

    Returns:
        pd.Series: equal-weight index level normalized to 1.0 at the start.

    Raises:
        ValueError: If the input data is empty.
    """

    # handle cases where no data exists
    if returns.empty:
        raise ValueError("Input financial data is empty.")

    # normalize returns to 1.0 on the first date
    normalized_returns = returns / returns.iloc[0]
    index = normalized_returns.mean(axis=1)
    index.name = "equal_weight_index"

    return index


def calculate_rolling_volatility(returns, window=60):
    """
    Calculate rolling volatility of returns over a specific window.

    Parameters:
        returns (pd.DataFrame): DataFrame of daily returns indexed by date.
        window (int, optional): rolling window size in trading days. Defaults to 60 days.

    Returns:
        pd.DataFrame: DataFrame of rolling volatility values indexed by date.

    Raises:
        ValueError: If the input data is empty or has insufficient data points.
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

    Raises:
        ValueError:
            If the input data is empty, has insufficient data points, or has less than two columns.
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


def calculate_rolling_sharpe(returns, window=60, risk_free_rate=0.0):
    """
    Calculate an approximate annualized rolling Sharpe ratio.

    Parameters:
        returns (pd.Series): Series of daily returns of an index.
        window (int, optional): rolling window size in trading days. Defaults to 60 days.
        risk_free_rate (float, optional): annual risk-free rate as a decimal. Defaults to 0.0.

    Returns:
        pd.Series: Series of rolling Sharpe ratios indexed by date.

    Raises:
        ValueError: If the input data is empty or has insufficient data points.
    """

    # handle cases where no data exists
    if returns.empty:
        raise ValueError(f"Input data on returns is empty.")

    # handle cases where there are not enough data points
    if len(returns) < window:
        raise ValueError(
            f"Not enough data points to compute rolling Sharpe ratio "
            f"with window size {window}."
        )

    # convert annual risk-free rate to a daily rate
    daily_risk_free_rate = risk_free_rate / 252.0
    excess_returns = returns - daily_risk_free_rate

    # calculate rolling mean and std dev of excess returns
    rolling_mean = excess_returns.rolling(window=window).mean()
    rolling_std = excess_returns.rolling(window=window).std()

    # calculate rolling Sharpe ratio
    sharpe = (rolling_mean / rolling_std) * np.sqrt(252.0)

    return sharpe


def calculate_drawdown(index):
    """
    Compute the drawdown series for an index level.

    Parameters:
        index (pd.Series): Series of index level indexed by date.

    Returns:
        pd.Series: Series of drawdown values, which are negative or zero.

    Raises:
        ValueError: If the input data is empty.
    """

    # handle cases where no data exists
    if index.empty:
        raise ValueError("Index level series is empty.")

    # calculate running maximum
    running_max = index.cummax()

    # calculate drawdown and name the series
    drawdown = index / running_max - 1.0
    drawdown.name = "drawdown"

    return drawdown


def calculate_max_drawdown(index):
    """
    Return the single worst drawdown for an index level series.

    Parameters:
        index (pd.Series): Series of index level indexed by date.

    Returns:
        float: maximum drawdown value (the most negative drawdown).
    """

    # compute drawdown series
    drawdown = calculate_drawdown(index)

    return drawdown.min()
