import pytest
import pandas as pd

from src.portfolio import (
    validate_selected_pairs,
    normalize_weights,
    equal_weight,
    rank_weight,
    inverse_half_life,
    inverse_volatility
)

def make_selected_pairs_df():
    return pd.DataFrame({
        "asset_1": ["AAPL", "MSFT", "JPM"],
        "asset_2": ["MSFT", "GOOG", "BAC"],
        "rank": [1, 2, 3],
        "half_life": [10.0, 20.0, 40.0],
        "spread_volatility": [0.05, 0.10, 0.20],
    })

def test_validate_selected_pairs_valid_case():
    
    df = make_selected_pairs_df()
    
    assert df.shape[0] == 3
    assert df.shape[1] == 5
    assert "asset_1" in df.columns
    assert "asset_2" in df.columns

def test_equal_weight_valid_case():
    
    df = make_selected_pairs_df()
    
    equal_weights = equal_weight(df,["asset_1","asset_2"])
    
    assert len(equal_weights) == 3
    assert equal_weights[0] == pytest.approx(1/3)

def test_ranked_weight_valid_case():
    
    df = make_selected_pairs_df()
    ranked_weights = rank_weight(df, "rank")
    
    assert len(ranked_weights) == 3
    assert ranked_weights.iloc[0] == pytest.approx(6/11)
    assert ranked_weights.iloc[1] == pytest.approx(3/11)
    
def test_inv_half_life_valid_case():
    
    df = make_selected_pairs_df()
    half_life_weights = inverse_half_life(df)
        
    assert len(half_life_weights) == 3
    assert half_life_weights.iloc[0] == pytest.approx(4/7)
    assert half_life_weights.iloc[1] == pytest.approx(2/7)
    
def test_inv_vol_valid_case():
    
    df = make_selected_pairs_df()
    inv_vol_weights = inverse_volatility(df)
        
    assert len(inv_vol_weights) == 3
    assert inv_vol_weights.iloc[0] == pytest.approx(4/7)
    assert inv_vol_weights.iloc[1] == pytest.approx(2/7)
    
def test_validate_selected_pairs_not_df():
    
    df = {}
    
    with pytest.raises(TypeError):
        validate_selected_pairs(df)

def test_validate_selected_pairs_empty_df():
    
    df = pd.DataFrame()
    
    with pytest.raises(ValueError):
        validate_selected_pairs(df,None)

def test_validate_selected_pairs_no_asset1():
    
    df = make_selected_pairs_df()
    df = df.drop(columns=["asset_1"])
    
    with pytest.raises(ValueError):
        validate_selected_pairs(df,["asset_1","asset_2"])

def test_validate_selected_pairs_no_asset2():
    
    df = make_selected_pairs_df()
    df = df.drop(columns=["asset_2"])
    
    with pytest.raises(ValueError):
        validate_selected_pairs(df,["asset_1","asset_2"])

def test_rank_weight_no_rank():
    df = make_selected_pairs_df()
    df = df.drop(columns=["rank"])
    
    with pytest.raises(ValueError):
        rank_weight(df)

def test_rank_weight_no_half_life():
    df = make_selected_pairs_df()
    df = df.drop(columns=["half_life"])
    
    with pytest.raises(ValueError):
        inverse_half_life(df)
    
def test_rank_weight_no_spread_volatility():
    df = make_selected_pairs_df()
    df = df.drop(columns=["spread_volatility"])
    
    with pytest.raises(ValueError):
        inverse_volatility(df)

def test_rank_weight_negative_rank():
    df = make_selected_pairs_df()
    df.loc[0, "rank"] = -1
    
    with pytest.raises(ValueError):
        rank_weight(df)

def test_rank_weight_negative_half_life():
    df = make_selected_pairs_df()
    df.loc[0, "half_life"] = -1
    
    with pytest.raises(ValueError):
        inverse_half_life(df)

def test_rank_weight_negative_spread_volatility():
    df = make_selected_pairs_df()
    df.loc[0, "spread_volatility"] = -1
    
    with pytest.raises(ValueError):
        inverse_volatility(df)

def test_rank_weight_zero_rank():
    df = make_selected_pairs_df()
    df.loc[0, "rank"] = 0
    
    with pytest.raises(ValueError):
        rank_weight(df)

def test_rank_weight_zero_half_life():
    df = make_selected_pairs_df()
    df.loc[0, "half_life"] = 0
    
    with pytest.raises(ValueError):
        inverse_half_life(df)

def test_rank_weight_zero_spread_volatility():
    df = make_selected_pairs_df()
    df.loc[0, "spread_volatility"] = 0
    
    with pytest.raises(ValueError):
        inverse_volatility(df)

def test_rank_weight_none_rank():
    df = make_selected_pairs_df()
    df.loc[0, "rank"] = None
    
    with pytest.raises(ValueError):
        rank_weight(df)

def test_rank_weight_none_half_life():
    df = make_selected_pairs_df()
    df.loc[0, "half_life"] = None
    
    with pytest.raises(ValueError):
        inverse_half_life(df)

def test_rank_weight_none_spread_volatility():
    df = make_selected_pairs_df()
    df.loc[0, "spread_volatility"] = None
    
    with pytest.raises(ValueError):
        inverse_volatility(df)