import pandas as pd
import yfinance as yf
from datetime import datetime


def load_stock_data(tickers, start="2020-01-01", end=None):
    """
    Load historical stock data for given tickers using Yahoo Finance.
    
    Parameters:
        tickers (list or str): list of stock ticker symbols or string of tickers separated by commas or spaces.
        start (str, optional): start date in YYYY-MM-DD format.
        end (str, optional): end date in YYYY-MM-DD format. If None, defaults to today's date.

    Returns:
        pd.DataFrame: pandas DataFrame of closing prices indexed by date.
    """
    # ensure list of tickers
    if isinstance(tickers, str):
        tickers = [tickers.strip() for tick in tickers.replace(',', ' ').split()]

    # ensure tickers is a list
    if not isinstance(tickers, list):
        raise TypeError("Tickers must be provided as a list or a string separated by commas or spaces.")
    
    # ensure all tickers are strings
    if not all(isinstance(ticker, str) for ticker in tickers):
        raise ValueError("All tickers must be strings.")

    # sort tickers for consistent order
    sorted_tickers = sorted(tickers)

    # set end date to today if no end date is provided
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')

    # download data and suppress progress bar
    data = yf.download(sorted_tickers, start=start, end=end, progress=False, auto_adjust=True)

    # handle cases where no data exists
    if data.empty:
        raise ValueError(f"No data fetched for given tickers: {sorted_tickers}")
    
    # handle cases where 'Close' column is missing
    if 'Close' not in data.columns.get_level_values(0):
        raise KeyError("'Close' column not found in downloaded data.")

    # extract closing prices
    close_data = data['Close'].copy()

    # drop empty columns
    close_data.dropna(axis=1, how="all", inplace=True)

    # print loaded data summary
    print(f"✅ stock data loaded")
    print(f"tickers: {', '.join(sorted_tickers)}")
    print(f"data range: {close_data.index.min().date()} → {close_data.index.max().date()}")
    print(f"number of rows: {len(close_data)}")

    return close_data