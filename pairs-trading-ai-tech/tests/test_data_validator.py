import pandas as pd
import pytest
import numpy as np
from src.data_validator import (
    validation_price_matrix,
    validation_volume_matrix
)

def make_valid_price_matrix(n=800):
    
    dates = pd.date_range('2020-01-01', periods=n, freq='B')
    
    df = pd.DataFrame(
        {
            "AAPL":np.linspace(100,200,n),
            "MSFT":np.linspace(200,300,n)
        },
        index=dates
    )
    
    return df

def make_valid_volume_matrix(n=800):
    
    dates = pd.date_range('2020-01-01', periods=n, freq='B')
    
    df = pd.DataFrame(
        {
            "AAPL":np.linspace(1000000,2000000,n),
            "MSFT":np.linspace(2000000,3000000,n)
        },
        index=dates
    )
    
    return df

#Price Validation
#Valid use case
def test_validation_price_matrix_valid_case():
    
    df = make_valid_price_matrix(800)
    
    assert df.shape[0] == 800
    assert df.shape[1] == 2

#Not a DataFrame
def test_validation_price_matrix_not_dataframe():
    
    df = {}
    
    with pytest.raises(TypeError):
        validation_price_matrix(df)
        
#Empty DataFrame
def test_validation_price_matrix_empty_dataframe():
    
    df = pd.DataFrame()
    
    with pytest.raises(ValueError):
        validation_price_matrix(df)

#Index is not DateTimeIndex
def test_validation_price_matrix_bad_index_type():
    
    df = make_valid_price_matrix(800)
    
    df = df.reset_index(0)
    
    with pytest.raises(TypeError):
        validation_price_matrix(df)

#Index has duplicated dates
def test_validation_price_matrix_duplicate_index():
    
    df = make_valid_price_matrix(800)
    
    target_date = pd.Timestamp('2020-01-02')
    target_df = df.loc[[target_date]]
    
    df = pd.concat([df, target_df], axis=0)
    
    with pytest.raises(ValueError):
        validation_price_matrix(df)
    
#less than 2 assets in price matrix
def test_validation_price_matrix_less_assets():
    
    df = make_valid_price_matrix(800)
    df = df[["AAPL"]]
    
    with pytest.raises(ValueError):
        validation_price_matrix(df)

#DataFrame does not have minimum number of observations
def test_validation_price_matrix_less_observations():
    
    df = make_valid_price_matrix(100)
    
    with pytest.raises(ValueError):
        validation_price_matrix(df)

#Price matrix has a negative value.
def test_validation_price_matrix_negative_price():
    
    df = make_valid_price_matrix(800)
    df.loc[pd.Timestamp("2020-01-02"), "AAPL"] = -100
    
    with pytest.raises(ValueError):
        validation_price_matrix(df)
    
#Price matrix has a 0 value.
def test_validation_price_matrix_zero_price():
    
    df = make_valid_price_matrix(800)
    df.loc[pd.Timestamp("2020-01-02"), "AAPL"] = 0
    
    with pytest.raises(ValueError):
        validation_price_matrix(df)

#Too many nulls in price matrix
def test_validation_price_matrix_missing_vals():
    
    df = make_valid_price_matrix(800)
    df.iloc[-100:, df.columns.get_loc("AAPL")] = np.nan
    
    with pytest.raises(ValueError):
        validation_price_matrix(df)

#Volume validation
#Valid use case
def test_validation_volume_matrix_valid_case():
    
    df = make_valid_volume_matrix(800)
    
    assert df.shape[0] == 800
    assert df.shape[1] == 2

#Not a DataFrame
def test_validation_volume_matrix_not_dataframe():
    
    df = {}
    
    with pytest.raises(TypeError):
        validation_volume_matrix(df)
        
#Empty DataFrame
def test_validation_volume_matrix_empty_dataframe():
    
    df = pd.DataFrame()
    
    with pytest.raises(ValueError):
        validation_volume_matrix(df)

#Index is not DateTimeIndex
def test_validation_volume_matrix_bad_index_type():
    
    df = make_valid_volume_matrix(800)
    
    df = df.reset_index(0)
    
    with pytest.raises(TypeError):
        validation_volume_matrix(df)

#Index has duplicated dates
def test_validation_volume_matrix_duplicate_index():
    
    df = make_valid_volume_matrix(800)
    
    target_date = pd.Timestamp('2020-01-02')
    target_df = df.loc[[target_date]]
    
    df = pd.concat([df, target_df], axis=0)
    
    with pytest.raises(ValueError):
        validation_volume_matrix(df)
    
#less than 2 assets in volume matrix
def test_validation_volume_matrix_less_assets():
    
    df = make_valid_volume_matrix(800)
    df = df[["AAPL"]]
    
    with pytest.raises(ValueError):
        validation_volume_matrix(df)

#DataFrame does not have minimum number of observations
def test_validation_volume_matrix_less_observations():
    
    df = make_valid_volume_matrix(100)
    
    with pytest.raises(ValueError):
        validation_volume_matrix(df)

#Volume matrix has a negative value.
def test_validation_volume_matrix_negative_volume():
    
    df = make_valid_volume_matrix(800)
    df.loc[pd.Timestamp("2020-01-02"), "AAPL"] = -100
    
    with pytest.raises(ValueError):
        validation_volume_matrix(df)
    
#Too many nulls in volume matrix
def test_validation_volume_matrix_missing_vals():
    
    df = make_valid_volume_matrix(800)
    df.iloc[-100:, df.columns.get_loc("AAPL")] = np.nan
    
    with pytest.raises(ValueError):
        validation_volume_matrix(df)