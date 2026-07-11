import pandas as pd
import pytest

from src.data_loader import (
    get_option_expiries,
    fetch_option_chain,
    fetch_option_chains_for_universe
)

def test_get_option_expiries_valid_ticker():
    
    ticker = "AAPL"
    expiries = get_option_expiries(ticker)
    
    assert isinstance(expiries,list)
    assert len(expiries) > 0

def test_get_option_expiries_valid_lowercase_ticker():
    
    ticker = "aapl"
    expiries = get_option_expiries(ticker)
    
    assert isinstance(expiries,list)
    assert len(expiries) > 0

def test_get_option_expiries_not_str_ticker():
    
    ticker = 12
    with pytest.raises(TypeError):
        get_option_expiries(ticker)

def test_get_option_expiries_empty_str_ticker():
    
    ticker = ""
    with pytest.raises(ValueError):
        get_option_expiries(ticker)

def test_fetch_option_chain_valid_ticker():
    
    ticker = "AAPL"
    expiries = fetch_option_chain(ticker)
    
    assert isinstance(expiries,pd.DataFrame)

def test_fetch_option_chain_valid_lowercase_ticker():
    
    ticker = "aapl"
    expiries = fetch_option_chain(ticker)
    
    assert isinstance(expiries,pd.DataFrame)
    