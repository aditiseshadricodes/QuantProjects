"""" 
This file is currently used to validate the option chain of all the tickers in the v1 
universe. This universe is currently 20 top us stocks plus SPY. 
"""

import pandas as pd

def validate_option_chain_df(
    df,
    expected_tickers = None
):
    
    #df is a non-empty pandas DataFrame.
    if not isinstance(df,pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")
    
    if df.empty:
        raise ValueError("df must not be empty.")
    
    #required columns exist
    required_cols = [
        "ticker","option_type","expiry","contractSymbol","strike"
        ,"bid","ask","lastPrice","volume","openInterest"
    ]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    #ticker exists and has no null values
    if df["ticker"].isna().any():
        raise ValueError("ticker cannot be null.")
    
    #option_type has only call or put values
    if not df["option_type"].isin(["call","put"]).all():
        raise ValueError("option_type can only be call or put.")    
    
    #expiry is parseable
    try:
        pd.to_datetime(df["expiry"], errors="raise")
    except Exception as e:
        raise ValueError("expiry must be parseable as a date.") from e
    
    #strike is greater than 0
    if (df["strike"] <=0 ).any():
        raise ValueError("Strike must be positive.")
    
    #bid, ask, lastPrice are nonnegative
    if (df["bid"] < 0 ).any():
        raise ValueError("bid must be nonnegative.")
    
    if (df["ask"] < 0 ).any():
        raise ValueError("ask must be nonnegative.")
    
    if (df["lastPrice"] < 0 ).any():
        raise ValueError("lastPrice must be nonnegative.")
    
    #bid is less than or equal to ask
    if any(df["bid"]>df["ask"]):
        raise ValueError("bid must be less than or equal to ask.")
    
    #Volume / openInterest is greater than or equal to 0
    if (df["volume"] < 0).any():
        raise ValueError("volume must be nonnegative.")
    
    if (df["openInterest"] < 0).any():
        raise ValueError("openInterest must be nonnegative.")
    
    #contractSymbol cannot have a null
    if df["contractSymbol"].isna().any():
        raise ValueError("contractSymbol cannot be null.")
    
    #Each ticker must have at least 1 row
    if expected_tickers is not None:
        actual_tickers = set(df["ticker"].dropna().unique())
        expected_tickers = set(expected_tickers)
        
        missing_tickers = expected_tickers - actual_tickers
        extra_tickers = actual_tickers - expected_tickers
        
        if missing_tickers:
            raise ValueError(f"Missing tickers:{sorted(missing_tickers)}")
        
        if extra_tickers:
            raise ValueError(f"Extra tickers: {sorted(extra_tickers)}")
        
    summary_checks = {
        "validation_passed": True,
        "rows": len(df),
        "n_tickers": df["ticker"].nunique(),
        "tickers": sorted(df["ticker"].dropna().unique()),
        "is_dataframe": True,
        "not_empty": True,
        "required_columns_present": True,
        "option_type_valid": True,
        "expiry_parseable": True,
        "strike_positive": True,
        "prices_non_negative": True,
        "ask_greater_equal_bid": True,
        "volume_open_interest_non_negative": True,
        "contract_symbol_not_null": True,
        "expected_tickers_present": True
    }
    
    return summary_checks