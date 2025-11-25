import pandas as pd
import yfinance as yf
from datetime import datetime


def _normalize_tickers(tickers):
    # ensure tickers is a list of tickers as strings
    if isinstance(tickers, str):
        tickers = [
            tick.strip()
            for tick in tickers.replace(',', ' ').split()
            if tick.strip()
        ]

    # ensure tickers is a list
    if not isinstance(tickers, list):
        raise TypeError(
            "Tickers must be provided as a list or a string separated by commas or spaces."
        )
    
    # ensure at least one ticker is provided
    if not tickers:
        raise ValueError("At least one ticker must be provided.")

    # ensure all tickers are strings
    if not all(isinstance(ticker, str) for ticker in tickers):
        raise ValueError("All tickers must be strings.")

    # sort tickers for consistent order
    sorted_tickers = sorted(tickers)

    return sorted_tickers


def load_stock_data(tickers, start="2020-01-01", end=None, adjusted=True, include_volume=False):
    """
    Load historical stock data for given tickers using Yahoo Finance.
    
    Parameters:
        tickers (list or str): 
            list of stock ticker symbols or string of tickers separated by commas or spaces.
        start (str, optional): 
            start date in YYYY-MM-DD format.
        end (str, optional): 
            end date in YYYY-MM-DD format. If None, defaults to today's date.
        adjusted (bool, optional): 
            If True, use adjusted close prices. 
            If False, use raw close prices.
        include_volume (bool, optional): 
            If True, also include volume data. 
            If False, don't include volume data.

    Returns:
        pd.DataFrame: 
        - if include_volume is True: pandas DataFrame of closing prices and volume indexed by date.
        - if include_volume is False: pandas DataFrame of closing prices indexed by date.
    """
    # normalize and sort tickers
    symbols = _normalize_tickers(tickers)

    # set end date to today if no end date is provided
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')

    # download data and suppress progress bar
    try:
        data = yf.download(
            symbols, 
            start=start, 
            end=end, 
            progress=False, 
            auto_adjust=adjusted
        )
    except Exception as e:
        raise RuntimeError(f"Failed to download data from Yahoo Finance: {e}")

    # handle cases where no data exists
    if data.empty:
        raise ValueError(f"No data fetched for given tickers: {symbols}")
    
    # handle cases where 'Close' column is missing
    if 'Close' not in data.columns.get_level_values(0):
        raise KeyError("'Close' column not found in downloaded data.")

    # extract closing prices
    close = data['Close'].copy()

    # drop empty columns
    close.dropna(axis=1, how="all", inplace=True)

    # return close data only
    if not include_volume:
        return close
    
    # handle cases where 'Close' column is missing
    if 'Volume' not in data.columns.get_level_values(0):
        raise KeyError("'Volume' column not found in downloaded data.")
    
    # extract closing prices
    volume = data['Volume'].copy()

    # drop empty columns
    volume.dropna(axis=1, how="all", inplace=True)

    return close, volume