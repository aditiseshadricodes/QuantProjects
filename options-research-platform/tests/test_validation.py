import pandas as pd
import pytest

from src.validation import validate_option_chain_df

def make_valid_option_chain_df(
    
):
    
    data = {
        "ticker":["AAPL","AAPL","MSFT","MSFT"],
        "option_type":["call","put","call","put"],
        "expiry":["2026-05-31","2026-05-31","2026-05-31","2026-05-31"],
        "contractSymbol":["AAPL260531C00100000","AAPL260531P00100000", "MSFT260531C00100000","MSFT260531P00100000"],
        "strike":[100.0, 100.0, 150, 150],
        "bid":[5.0,4.5, 5, 5.5],
        "ask":[5.5,5.0, 5.5, 6],
        "lastPrice":[5.25,4.75, 5.25, 5.75],
        "volume":[100,80, 120, 100],
        "openInterest":[1000,900, 1200, 1100]
    }
    
    return pd.DataFrame(data)

#valid df case
def test_validate_option_chain_valid_df():
    
    df = make_valid_option_chain_df()
    
    result = validate_option_chain_df(
        df,
        expected_tickers=["AAPL","MSFT"]
    )
    
    assert result["validation_passed"] is True
    assert result["rows"] == 4
    assert result["n_tickers"] == 2

#not a DataFrame
def test_validate_option_chain_not_df():
    
    df = {}
    
    with pytest.raises(TypeError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )
        
#empty DataFrame
def test_validate_option_chain_empty_df():
    
    df = pd.DataFrame()
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#missing ticker
def test_validate_option_chain_missing_ticker():
    
    df = make_valid_option_chain_df()
    df = df.drop(columns = ['ticker'])
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#null ticker
def test_validate_option_chain_null_ticker():
    
    df = make_valid_option_chain_df()
    df["ticker"] = None
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#missing expected ticker
def test_validate_option_chain_missing_expected_ticker():
    
    df = make_valid_option_chain_df()
    df = df[df["ticker"] == "AAPL"]
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#extra ticker
def test_validate_option_chain_extra_ticker():
    
    df = make_valid_option_chain_df()
    extra_row = df.iloc[[0]].copy()
    extra_row["ticker"] = "TSLA"
    
    df = pd.concat([df,extra_row])
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#missing option_type
def test_validate_option_chain_missing_option_type():
    
    df = make_valid_option_chain_df()
    df = df.drop(columns=['option_type'])
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#invalid option_type
def test_validate_option_chain_invalid_option_type():
    
    df = make_valid_option_chain_df()
    df.loc[0, "option_type"] = "banana"
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#missing strike
def test_validate_option_chain_missing_strike():
    
    df = make_valid_option_chain_df()
    df = df.drop(columns=['strike'])
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#negative strike
def test_validate_option_chain_negative_strike():
    
    df = make_valid_option_chain_df()
    df.loc[0, "strike"] = -100
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )
        
#missing expiry
def test_validate_option_chain_missing_expiry():
    
    df = make_valid_option_chain_df()
    df = df.drop(columns=['expiry'])
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#bad expiry
def test_validate_option_chain_bad_expiry():
    
    df = make_valid_option_chain_df()
    df.loc[0, "expiry"] = "2026-13-01"
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )
#missing contractSymbol
def test_validate_option_chain_missing_contractSymbol():
    
    df = make_valid_option_chain_df()
    df = df.drop(columns=['contractSymbol'])
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#null contractSymbol
def test_validate_option_chain_null_contractSymbol():
    
    df = make_valid_option_chain_df()
    df.loc[0, "contractSymbol"] = None
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )
#missing bid
def test_validate_option_chain_missing_bid():
    
    df = make_valid_option_chain_df()
    df = df.drop(columns=['bid'])
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#negative bid
def test_validate_option_chain_negative_bid():
    
    df = make_valid_option_chain_df()
    df.loc[0, "bid"] = -5
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#missing ask
def test_validate_option_chain_missing_ask():
    
    df = make_valid_option_chain_df()
    df = df.drop(columns=['ask'])
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#negative ask
def test_validate_option_chain_negative_ask():
    
    df = make_valid_option_chain_df()
    df.loc[0, "ask"] = -5
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#bid > ask
def test_validate_option_chain_bid_greater_than_ask():
    
    df = make_valid_option_chain_df()
    df.loc[0, "bid"] = 10
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )
    
#missing lastPrice
def test_validate_option_chain_missing_lastPrice():
    
    df = make_valid_option_chain_df()
    df = df.drop(columns=['lastPrice'])
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#negative lastPrice
def test_validate_option_chain_negative_lastPrice():
    
    df = make_valid_option_chain_df()
    df.loc[0, "lastPrice"] = -5.25
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )
#missing volume
def test_validate_option_chain_missing_volume():
    
    df = make_valid_option_chain_df()
    df = df.drop(columns=['volume'])
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#negative volume
def test_validate_option_chain_negative_volume():
    
    df = make_valid_option_chain_df()
    df.loc[0, "volume"] = -150
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )
#missing openInterest
def test_validate_option_chain_missing_openInterest():
    
    df = make_valid_option_chain_df()
    df = df.drop(columns=['openInterest'])
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )

#negative openInterest
def test_validate_option_chain_negative_openInterest():
    
    df = make_valid_option_chain_df()
    df.loc[0, "openInterest"] = -900
    
    with pytest.raises(ValueError):
        validate_option_chain_df(
            df,
            expected_tickers = ["AAPL","MSFT"]
        )