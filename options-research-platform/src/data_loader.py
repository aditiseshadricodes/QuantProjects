""" 
Data Loader for Options Research Platform.

Uses yfinance to fetch US listed equity and ETF option chain snapshots.

V1 Responsibilities:
- Fetch available expiries for a ticker.
- Fetch calls and puts for one expiry.
- Return a clean pandas DataFrame.
"""

import pandas as pd
import yfinance as yf

def get_option_expiries(
    ticker
):
    
    #ticker is a non-empty string
    if not isinstance(ticker, str):
        raise TypeError("Ticker should be a string.")
    
    if ticker.strip() == "":
        raise ValueError("Ticker cannot be empty.")
    
    #ticker should be uppercase
    ticker = ticker.upper().strip(' ')
    
    #Creating yf.Ticker object
    data = yf.Ticker(ticker)
    expirations = data.options
    
    expirations = list(expirations)
    
    #Check if expirations is empty
    if len(expirations) == 0:
        raise ValueError("Expirations should not be empty.")
    
    return expirations
    