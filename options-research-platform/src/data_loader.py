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

def fetch_option_chain(
    ticker, 
    expiry=None
):
    
    #ticker is a non-empty string
    if not isinstance(ticker, str):
        raise TypeError("Ticker should be a string.")
    
    if ticker.strip() == "":
        raise ValueError("Ticker cannot be empty.")
    
    #ticker should be uppercase
    ticker = ticker.strip().upper()
    
    expiries = get_option_expiries(ticker)
    
    #checking for provided expiry.
    if expiry is None:
        expiry = expiries[0]
    else:
        if not isinstance(expiry, str):
            raise TypeError("expiry should be a string.")
        else:
            if expiry not in expiries:
                raise ValueError("invalid expiry provided.")
    
    #Fetching option chain
    chain = yf.Ticker(ticker).option_chain(expiry)
    
    #copying calls and puts
    calls = chain.calls.copy()
    puts = chain.puts.copy()
    
    #Noting option type, ticker and expiry
    calls["ticker"] = ticker
    puts["ticker"] = ticker
    calls["expiry"] = expiry
    puts["expiry"] = expiry
    calls["option_type"] = "call"
    puts["option_type"] = "put"
    
    #Combine into 1 DataFrame
    options_df = pd.concat([calls,puts], axis=0, ignore_index = True)
    
    #Validation checks for options_df
    if not isinstance(options_df, pd.DataFrame):
        raise TypeError("options_df should be a pandas DataFrame.")
    
    if options_df.empty:
        raise ValueError(f"options_df for {ticker} should not be empty.")
    
    required_cols = [
        "contractSymbol","strike","lastPrice","bid",
        "ask","volume","openInterest","impliedVolatility",
        "ticker","expiry","option_type"
        ]
    
    if any(not col in options_df.columns for col in required_cols):
        raise ValueError(f"{col} should be in options_df for {ticker}.")
    
    if len(set(options_df["ticker"])) >1:
        raise ValueError("ticker should be a unique value.")
    
    if len(set(options_df["expiry"])) >1:
        raise ValueError("expiry should be a unique value.")
    
    if not options_df["option_type"].isin(["call","put"]).all():
        raise ValueError(f"option_type for {ticker} can only be call or put.")
    
    valid_option_types = {"call","put"}
    options_types = set(options_df["option_type"].dropna().unique())
    
    if not options_types.issubset(valid_option_types):
        raise ValueError("option types contain invalid values.")
    
    if not valid_option_types.issubset(options_types):
        raise ValueError("Option cahin must have atleast one call and one put.")
    
    return options_df

def fetch_option_chains_for_universe(
    tickers,
    expiry=None
):
    
    #ticker list validation
    if not isinstance(tickers, list):
        raise TypeError("tickers should be a list.")
    
    if len(tickers) == 0:
        raise ValueError("tickers should not be empty.")
    
    if any(not isinstance(ticker, str) for ticker in tickers):
        raise TypeError("all elements of tickers should be strings.")
    
    #create empty container.
    all_option_chains = []
    
    for ticker in tickers:
        
        #Call option chain per ticker
        chain = fetch_option_chain(ticker, expiry=expiry)
        
        #Append to list
        all_option_chains.append(chain)
        
    #concatenate to a single DataFrame
    options_df = pd.concat(all_option_chains, axis=0, ignore_index=True)
    
    return options_df