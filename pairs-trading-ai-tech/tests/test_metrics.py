import pytest
import pandas as pd
import numpy as np

from src.metrics import (
    _validate_returns,
    compute_cumulative_returns,
    compute_mean_daily_return,
    compute_annualized_return,
)

def test_strategy_returns_valid_fixture():
    
    returns = pd.Series(
        [0.1, np.nan, -0.05, 0.02],
        index=pd.date_range("2024-01-01",
        periods=4)
    )
    returns = _validate_returns(returns)
    
    assert len(returns) == 3
    

def test_cumulative_returns_valid_case():
    
    returns = pd.Series(
        [0.1, np.nan, -0.05, 0.02],
        index=pd.date_range("2024-01-01",
        periods=4)
    )
    
    cumulative_rets = compute_cumulative_returns(
        returns
    )
    expected_rets = pd.Series(
        [0.1,0.045,0.0659],
        index = [
            returns.index[0],
            returns.index[2],
            returns.index[3]
        ]
    )
    
    assert len(cumulative_rets) == 3
    pd.testing.assert_series_equal(
        cumulative_rets,
        expected_rets,
        check_names=False
    )

def test_strategy_return_wrong_object_type():
    
    returns1 = []
    returns2 = pd.DataFrame(dtype=float)
    returns3 = {}
    
    with pytest.raises(TypeError):
        compute_cumulative_returns(returns1)
    
    with pytest.raises(TypeError):
        compute_cumulative_returns(returns2)
    
    with pytest.raises(TypeError):
        compute_cumulative_returns(returns3)

def test_strategy_returns_empty_series():
    
    returns = pd.Series(dtype=float)
    with pytest.raises(ValueError):
        compute_cumulative_returns(returns)

def test_strategy_returns_all_nan_series():
    
    returns = pd.Series(
        [np.nan, np.nan, np.nan, np.nan],
        index=pd.date_range("2024-01-01",
        periods=4)
    )
    
    with pytest.raises(ValueError):
        compute_cumulative_returns(returns)

def test_strategy_returns_non_numeric_series():
    
    returns = pd.Series(
        ['a', 'b', 'c', '3'],
        index=pd.date_range("2024-01-01",
        periods=4)
    )
    
    with pytest.raises(TypeError):
        compute_cumulative_returns(returns)

def test_mean_daily_return_valid_case():
    
    returns = pd.Series(
        [0.1, np.nan, -0.05, 0.02],
        index=pd.date_range("2024-01-01",
        periods=4)
    )
    
    mean_daily_return = compute_mean_daily_return(returns)
    
    expected = 0.07/3
    
    assert mean_daily_return == pytest.approx(expected)

def test_annualized_return_valid_case():
    
    returns = pd.Series(
        [0.1, np.nan, -0.05, 0.02],
        index=pd.date_range("2024-01-01",
        periods=4)
    )
    
    result = compute_annualized_return(
        returns,
        periods_per_year=3
    )
    
    assert result == pytest.approx(0.0659)
    
    result2 = compute_annualized_return(returns)
    
    expected_total_growth = (
        1.10 * 0.95 * 1.02
    )
    expected2 = (
        expected_total_growth**(252/3) -1
    )
    
    assert result2 == pytest.approx(expected2)

@pytest.mark.parametrize(
    "invalid_periods_per_year",
    [252.0,"252",np.nan,[252],True]
)
def test_compute_annualized_return_reject_non_integer_periods_per_year(
    invalid_periods_per_year
):
    
    returns = pd.Series(
        [0.1, np.nan, -0.05, 0.02],
        index=pd.date_range("2024-01-01",
        periods=4)
    )
    
    with pytest.raises(TypeError):
        compute_annualized_return(
            returns,
            periods_per_year=invalid_periods_per_year
        )

@pytest.mark.parametrize(
    "invalid_periods_per_year",
    [0,-1,-252]
)
def test_compute_annualized_return_reject_nonpositive_periods_per_year(
    invalid_periods_per_year
):
    
    returns = pd.Series(
        [0.1, np.nan, -0.05, 0.02],
        index=pd.date_range("2024-01-01",
        periods=4)
    )
    with pytest.raises(ValueError):
        compute_annualized_return(
            returns,
            periods_per_year=invalid_periods_per_year
        )
    