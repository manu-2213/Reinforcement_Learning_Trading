import yfinance as yf
import pandas as pd
from typing import List, Optional

class DataLoader:
    """
    A class for fetching historical stock data using Yahoo Finance.
    """
    
    valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m',
                       '1h', '1d', '5d', '1wk', '1mo', '3mo']
    
    valid_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    
    def __init__(self, 
                 tickers: List[str], 
                 start_date: str, 
                 end_date: str, 
                 interval: str = '1d',
                 columns: Optional[List[str]] = None):
        """
        Initializes the DataLoader with stock tickers, date range, and interval.
        
        Parameters:
        -----------
        tickers : List[str]
            List of stock tickers.
        start_date : str
            Start date in 'YYYY-MM-DD' format.
        end_date : str
            End date in 'YYYY-MM-DD' format.
        interval : str, optional
            Data retrieval frequency (default is '1d').
            Options: '1m', '2m', '5m', '15m', '30m', '60m', '90m',
                     '1h', '1d', '5d', '1wk', '1mo', '3mo'.
        columns : List[str], optional
            List of columns to retrieve (default is ['Close']).
        """
        if not tickers:
            raise ValueError("The 'tickers' list is empty. Provide at least one ticker.")
        
        if interval not in self.valid_intervals:
            raise ValueError(f"Invalid interval '{interval}'. Choose from {self.valid_intervals}.")
        
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.columns = columns or ['Close']
    
    def load_data(self) -> pd.DataFrame:
        """
        Fetch historical stock data.

        Returns:
        --------
        pd.DataFrame
            A DataFrame with historical stock data.
        """
        data = yf.download(
            tickers=self.tickers,
            start=self.start_date,
            end=self.end_date,
            interval=self.interval,
            group_by='ticker',
            auto_adjust=True,
            threads=True
        )

        if len(self.tickers) == 1:
            data.columns = pd.MultiIndex.from_product([self.tickers, data.columns])

        data.dropna(how='all', inplace=True)

        # Extract the selected columns correctly from multi-indexed DataFrame
        if isinstance(data.columns, pd.MultiIndex):
            data = data.loc[:, (slice(None), self.columns)]
            data.columns = data.columns.droplevel(1)  # Drop the second level to make it easier to access

        return data

