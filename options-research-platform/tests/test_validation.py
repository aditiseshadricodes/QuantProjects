import pandas as pd
import pytest

from src.validation import validate_option_chain_df

def make_valid_option_chain_df(
    
):
    
    data = {
        "ticker":["AAPL","AAPL"],
        "option_type":["call","put"],
        "expiry":["2026-05-31","2026-05-31"],
        "contractSymbol":["AAPL260531C00100000","AAPL260531P00100000"],
        "strike":[100.0, 100.0],
        "bid":[5.0,4.5],
        "ask":[5.5,5.0],
        "lastPrice":[5.25,4.75],
        "volume":[100,80],
        "openInterest":[1000,900]
    }
    
    return pd.DataFrame(data)

def test_validate_option_chain_valid_df():
    
    df = make_valid_option_chain_df()
    
    result = validate_option_chain_df(df, expected_tickers=["AAPL"])
    
    assert result["validation_passed"] is True
    assert result["rows"] == 2
    assert result["n_tickers"] == 1