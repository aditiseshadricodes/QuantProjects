import logging
import pytest
from src.cost_model import (
    bps_to_decimal,
    estimate_one_way_trade_event_cost_bps,
    estimate_holding_cost_bps,
    estimate_total_pair_cost_bps,
    compute_pair_cost_series
)
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

def test_bps_to_decimal_valid_case():
    
    assert bps_to_decimal(100) == 0.01
    assert bps_to_decimal(50) == 0.005
    
def test_estimate_one_way_trade_event_cost_bps_valid_case(
    commission = 10,
    bid_ask_spread = 10,
    slippage = 5,
    market_impact = 2,
    tax=20
):
    
    assert estimate_one_way_trade_event_cost_bps(
        commission,
        bid_ask_spread,
        slippage,
        market_impact,
        tax
    ) == 47
    
    assert estimate_one_way_trade_event_cost_bps(
        commission_bps=1,
        bid_ask_spread_bps=2,
        slippage_bps=3,
        market_impact_bps=4,
        tax_bps=5
    ) == 15

def test_pair_roundtrip_trade_cost_valid():
    result =  4 * estimate_one_way_trade_event_cost_bps(
        commission_bps=1,
        bid_ask_spread_bps=2,
        slippage_bps=3,
        market_impact_bps=4,
        tax_bps=5,
    )

    assert result == 60 

def test_holding_cost_valid():
    result = estimate_holding_cost_bps(
        holding_days=21,
        borrow_cost_annual_bps=252,
        financing_cost_annual_bps=252,
        trading_days=252,
    )

    assert result == 42

def test_total_pair_trade_cost_valid():
    result = estimate_total_pair_cost_bps(
        holding_days=21,
        commission_bps=1,
        bid_ask_spread_bps=2,
        slippage_bps=3,
        market_impact_bps=4,
        tax_bps=5,
        borrow_cost_annual_bps=252,
        financing_cost_annual_bps=252,
        trading_days=252,
    )

    assert result == 102
    
def test_bps_to_decimal_wrong_type(
    bps = "30"
):
    
    with pytest.raises(TypeError):
        bps_to_decimal(bps)

def test_bps_to_decimal_negative_value(
    bps = -45
):
    
    with pytest.raises(ValueError):
        bps_to_decimal(bps)

def test_estimate_one_way_trade_event_cost_bad_commission(
    commission = "10",
    bid_ask_spread = 10,
    slippage = 5,
    market_impact = 2,
    tax=20
):
    
    with pytest.raises(TypeError):
        estimate_one_way_trade_event_cost_bps(
            commission,
            bid_ask_spread,
            slippage,
            market_impact,
            tax
        )
        
def test_estimate_one_way_trade_event_cost_negative_commission(
    commission = -10,
    bid_ask_spread = 10,
    slippage = 5,
    market_impact = 2,
    tax=20
):
    
    with pytest.raises(ValueError):
        estimate_one_way_trade_event_cost_bps(
            commission,
            bid_ask_spread,
            slippage,
            market_impact,
            tax
        )

def test_estimate_one_way_trade_event_cost_bad_bid_ask_spread(
    commission = 10,
    bid_ask_spread = "10",
    slippage = 5,
    market_impact = 2,
    tax=20
):
    
    with pytest.raises(TypeError):
        estimate_one_way_trade_event_cost_bps(
            commission,
            bid_ask_spread,
            slippage,
            market_impact,
            tax
        )
        
def test_estimate_one_way_trade_event_cost_negative_bid_ask_spread(
    commission = 10,
    bid_ask_spread = -10,
    slippage = 5,
    market_impact = 2,
    tax=20
):
    
    with pytest.raises(ValueError):
        estimate_one_way_trade_event_cost_bps(
            commission,
            bid_ask_spread,
            slippage,
            market_impact,
            tax
        )

def test_estimate_one_way_trade_event_cost_bad_slippage(
    commission = 10,
    bid_ask_spread = 10,
    slippage = "5",
    market_impact = 2,
    tax=20
):
    
    with pytest.raises(TypeError):
        estimate_one_way_trade_event_cost_bps(
            commission,
            bid_ask_spread,
            slippage,
            market_impact,
            tax
        )

def test_estimate_one_way_trade_event_cost_negative_slippage(
    commission = 10,
    bid_ask_spread=10,
    slippage = -5,
    market_impact = 2,
    tax = 20
):
    
    with pytest.raises(ValueError):
        estimate_one_way_trade_event_cost_bps(
            commission,
            bid_ask_spread,
            slippage,
            market_impact,
            tax
        )

def test_estimate_one_way_trade_event_bad_market_impact(
    commission =10,
    bid_ask_spread=10,
    slippage = 5,
    market_impact = "2",
    tax=20
):
    
    with pytest.raises(TypeError):
        estimate_one_way_trade_event_cost_bps(
            commission,
            bid_ask_spread,
            slippage,
            market_impact,
            tax
        )

def test_estimate_one_way_trade_event_negative_market_impact(
    commission = 10,
    bid_ask_spread = 10,
    slippage = 5,
    market_impact = -2,
    tax = 20
):
    
    with pytest.raises(ValueError):
        estimate_one_way_trade_event_cost_bps(
            commission,
            bid_ask_spread,
            slippage,
            market_impact,
            tax
        )

def test_estimate_one_way_trade_event_bad_tax_rate(
    commission = 10,
    bid_ask_spread = 10,
    slippage = 5,
    market_impact = 2,
    tax = "20"
):
    
    with pytest.raises(TypeError):
        estimate_one_way_trade_event_cost_bps(
            commission,
            bid_ask_spread,
            slippage,
            market_impact,
            tax
        )

def test_estimate_one_way_trade_event_negative_tax_rate(
    commission = 10,
    bid_ask_spread = 10,
    slippage = 5,
    market_imoact = 2,
    tax = -20
):
    
    with pytest.raises(ValueError):
        estimate_one_way_trade_event_cost_bps(
            commission,
            bid_ask_spread,
            slippage,
            market_imoact,
            tax
        )

def test_estimate_holding_cost_str_holding_days(
    holding_days="21",
    borrow_cost_annual_bps=252,
    financing_cost_annual_bps=252,
    trading_days=252
):
    
    with pytest.raises(TypeError):
        estimate_holding_cost_bps(
            holding_days,
            borrow_cost_annual_bps,
            financing_cost_annual_bps,
            trading_days
        )

def test_estimate_holding_cost_float_holding_days(
    holding_days=21.0,
    borrow_cost_annual_bps=252,
    financing_cost_annual_bps=252,
    trading_days=252
):
    
    with pytest.raises(TypeError):
        estimate_holding_cost_bps(
            holding_days,
            borrow_cost_annual_bps,
            financing_cost_annual_bps,
            trading_days
        )

def test_estimate_holding_cost_negative_holding_days(
    holding_days = -21,
    borrow_cost_annual_bps=252,
    financing_cost_annual_bps = 252,
    trading_days=252
):
    
    with pytest.raises(ValueError):
        estimate_holding_cost_bps(
            holding_days,
            borrow_cost_annual_bps,
            financing_cost_annual_bps,
            trading_days
        )

def test_estimate_holding_cost_str_borrow_cost(
    holding_days=21,
    borrow_cost_annual_bps="252",
    financing_cost_annual_bps=252,
    trading_days=252
):
    
    with pytest.raises(TypeError):
        estimate_holding_cost_bps(
            holding_days,
            borrow_cost_annual_bps,
            financing_cost_annual_bps,
            trading_days
        )

def test_estimate_holding_cost_negative_borrow_cost(
    holding_days=21,
    borrow_cost_annual_bps = -252,
    financing_cost_annual_bps = 252,
    trading_days=252
):
    
    with pytest.raises(ValueError):
        estimate_holding_cost_bps(
            holding_days,
            borrow_cost_annual_bps,
            financing_cost_annual_bps,
            trading_days
        )

def test_estimate_holding_cost_str_financing_cost(
    holding_days=21,
    borrow_cost_annual_bps=252,
    financing_cost_annual_bps="252",
    trading_days=252
):
    
    with pytest.raises(TypeError):
        estimate_holding_cost_bps(
            holding_days,
            borrow_cost_annual_bps,
            financing_cost_annual_bps,
            trading_days
        )

def test_estimate_holding_cost_negative_financing_cost(
    holding_days=21,
    borrow_cost_annual_bps=252,
    financing_cost_annual_bps=-252,
    trading_days=252
):
    
    with pytest.raises(ValueError):
        estimate_holding_cost_bps(
            holding_days,
            borrow_cost_annual_bps,
            financing_cost_annual_bps,
            trading_days
        )

def test_estimate_holding_cost_str_trading_days(
    holding_days=21,
    borrow_cost_annual_bps=252,
    financing_cost_annual_bps=252,
    trading_days="252"
):
    
    with pytest.raises(TypeError):
        estimate_holding_cost_bps(
            holding_days,
            borrow_cost_annual_bps,
            financing_cost_annual_bps,
            trading_days
        )

def test_estimate_holding_cost_float_trading_days(
    holding_days=21,
    borrow_cost_annual_bps=252,
    financing_cost_annual_bps=252,
    trading_days=252.0
):
    
    with pytest.raises(TypeError):
        estimate_holding_cost_bps(
            holding_days,
            borrow_cost_annual_bps,
            financing_cost_annual_bps,
            trading_days
        )

def test_estimate_holding_cost_negative_trading_days(
    holding_days=21,
    borrow_cost_annual_bps=252,
    financing_cost_annual_bps=252,
    trading_days=-252
):
    
    with pytest.raises(ValueError):
        estimate_holding_cost_bps(
            holding_days,
            borrow_cost_annual_bps,
            financing_cost_annual_bps,
            trading_days
        )

def test_estimate_holding_cost_zero_trading_days(
    holding_days=21,
    borrow_cost_annual_bps=252,
    financing_cost_annual_bps=252,
    trading_days=0
):
    
    with pytest.raises(ValueError):
        estimate_holding_cost_bps(
            holding_days,
            borrow_cost_annual_bps,
            financing_cost_annual_bps,
            trading_days
        )

def make_cost_kwargs(**overrides):
    
    kwargs = {
        "beta":1.0,
        "commission_bps":0.0,
        "bid_ask_spread_bps":0.0,
        "slippage_bps":0.0,
        "market_impact_bps":0.0,
        "tax_bps":0.0,
        "borrow_cost_annual_bps":0.0,
        "financing_cost_annual_bps":0.0,
        "trading_days":252,
    }
    
    kwargs.update(overrides)
    return kwargs

def test_returns_zero_costs_when_all_cost_rates_are_zero():
    
    positions = pd.Series(
        [0.0, 1.0, 1.0, 0.0, -1.0, 0.0],
        index=pd.date_range("2024-01-01", periods=6),
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(beta=1.5),
    )

    expected = pd.Series(
        np.zeros(len(positions)),
        index=positions.index,
    )

    pd.testing.assert_series_equal(
        result["total_cost"],
        expected,
        check_names=False,
    )
    
    cost_columns = [
        "total_cost",
        "trade_event_cost",
        "borrow_cost",
        "financing_cost"
    ]
    assert (result[cost_columns]==0).all().all()
    
def test_returns_zero_costs_when_positions_are_always_flat():
    
    positions =  pd.Series(
        [0.0,0.0,0.0,0.0],
        index =pd.date_range("2024-01-01", periods=4)
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.50,
            commission_bps=10.0,
            bid_ask_spread_bps=20.0,
            slippage_bps=30.0,
            market_impact_bps=40.0,
            tax_bps=50.0,
            borrow_cost_annual_bps=100.0,
            financing_cost_annual_bps=200.0,
        ),
    )
    
    cost_columns = result.filter(like="_cost")

    assert (cost_columns == 0.0).all().all()
    assert (result["position_change"] == 0.0).all()

def test_commission_is_charged_only_when_positions_change():
    
    positions =  pd.Series(
        [0.0,1.0,1.0,0.0],
        index =pd.date_range("2024-01-01", periods=4)
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            commission_bps=100.0,
        ),
    )
    
    expected_position_change = pd.Series(
        [0.0,1.0,0.0,1.0],
        index=positions.index
    )
    
    pd.testing.assert_series_equal(
        result["position_change"],
        expected_position_change,
        check_names=False
    )
    
    assert result.loc["2024-01-03","trade_event_cost"] == 0.0
    assert result.loc["2024-01-02","trade_event_cost"] > 0.0
    assert result.loc["2024-01-04","trade_event_cost"] > 0.0

def test_direct_position_reversal_charges_full_turnover():
    
    positions =  pd.Series(
        [0.0,1.0,-1.0],
        index =pd.date_range("2024-01-01", periods=3)
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            commission_bps=100.0,
        ),
    )
    
    expected_position_change = pd.Series(
        [0.0,1.0,2.0],
        index=positions.index
    )
    
    pd.testing.assert_series_equal(
        result["position_change"],
        expected_position_change,
        check_names=False
    )
    
    assert result.iloc[2]["trade_event_cost"] == pytest.approx(
        2 * result.iloc[1]["trade_event_cost"]
    )

@pytest.mark.parametrize(
    "cost_name",
    [
        "bid_ask_spread_bps",
        "slippage_bps",
        "market_impact_bps",
        "tax_bps",
    ]
)
def test_each_execution_cost_component_is_applied_on_turnover(
    cost_name
):
    
    positions =  pd.Series(
        [0.0,1.0,1.0,0.0],
        index =pd.date_range("2024-01-01", periods=4)
    )
    
    cost_kwargs = make_cost_kwargs(
        beta=1.0
    )
    cost_kwargs[cost_name] = 100.0
    
    result = compute_pair_cost_series(
        positions=positions,
        **cost_kwargs,
    )
    
    assert result.iloc[0]["trade_event_cost"] == 0.0
    assert result.iloc[1]["trade_event_cost"] > 0.0
    assert result.iloc[2]["trade_event_cost"] == 0.0
    assert result.iloc[3]["trade_event_cost"] > 0.0
    
def test_trade_event_cost_components_sum_correctly():
    
    positions =  pd.Series(
        [0.0,1.0,1.0,0.0],
        index =pd.date_range("2024-01-01", periods=4)
    )
    
    commission_result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            commission_bps=10.0,
        ),
    )
    
    spread_result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            bid_ask_spread_bps=20.0,
        ),
    )
    
    slippage_result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            slippage_bps=30.0,
        ),
    )
    
    impact_result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            market_impact_bps=40.0,
        ),
    )
    
    combined_result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            commission_bps=10.0,
            bid_ask_spread_bps=20.0,
            slippage_bps=30.0,
            market_impact_bps=40.0,
        ),
    )
    #Tax is skipped until its convention is tested separately.
    expected = (
        commission_result["trade_event_cost"]
        +
        spread_result["trade_event_cost"]
        +
        impact_result["trade_event_cost"]
        +
        slippage_result["trade_event_cost"]
    )
    
    pd.testing.assert_series_equal(
        combined_result["trade_event_cost"],
        expected,
        check_names=False
    )
#Tax is charged on trade events notionally
def test_tax_is_applied_to_trade_events():
    
    positions =  pd.Series(
        [0.0,1.0,1.0,0.0],
        index =pd.date_range("2024-01-01", periods=4)
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            tax_bps=100.0,
        ),
    )
    
    assert result.iloc[0]["trade_event_cost"] == 0
    assert result.iloc[1]["trade_event_cost"] > 0
    assert result.iloc[2]["trade_event_cost"] == 0
    assert result.iloc[3]["trade_event_cost"] > 0
    
def test_borrow_cost_is_charged_while_position_is_open():
    
    positions =  pd.Series(
        [0.0,1.0,1.0,0.0],
        index =pd.date_range("2024-01-01", periods=4)
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            borrow_cost_annual_bps=252.0,
            trading_days=252,
        ),
    )
    
    assert result.iloc[0]["borrow_cost"] == 0
    assert result.iloc[1]["borrow_cost"] > 0
    assert result.iloc[2]["borrow_cost"] > 0
    assert result.iloc[3]["borrow_cost"] == 0

def test_financing_cost_is_charged_while_position_is_open():
    
    positions =  pd.Series(
        [0.0,1.0,1.0,0.0],
        index =pd.date_range("2024-01-01", periods=4)
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            financing_cost_annual_bps=252.0,
            trading_days=252,
        ),
    )
    
    assert result.iloc[0]["financing_cost"] == 0
    assert result.iloc[1]["financing_cost"] > 0
    assert result.iloc[2]["financing_cost"] > 0
    assert result.iloc[3]["financing_cost"] == 0
    
    assert (result["trade_event_cost"]==0.0).all()
    assert (result["borrow_cost"]==0.0).all()
    
    daily_financing_cost = 252.0 / 10_000 / 252
    
    expected = (
        result["long_notional"]*daily_financing_cost
    )
    
    pd.testing.assert_series_equal(
        result["financing_cost"],
        expected,
        check_names=False
    )
    
def test_annual_holding_cost_respect_trading_days():
    
    positions =  pd.Series(
        [0.0,1.0,1.0,0.0],
        index =pd.date_range("2024-01-01", periods=4)
    )
    
    result_252 = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            borrow_cost_annual_bps=252.0,
            trading_days=252,
        ),
    )
    
    result_126 = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            borrow_cost_annual_bps=252.0,
            trading_days=126,
        ),
    )
    
    assert (result_126["trade_event_cost"]==0.0).all()
    assert (result_126["financing_cost"]==0.0).all()
    
    assert (result_252["trade_event_cost"]==0.0).all()
    assert (result_252["financing_cost"]==0.0).all()
    
    assert result_126.iloc[2]["borrow_cost"] == pytest.approx(
        2 * result_252.iloc[2]["borrow_cost"]
    )

def test_beta_scales_trade_event_cost_by_gross_pair_notional():
    
    positions = pd.Series(
        [0.0,1.0,1.0],
        index = pd.date_range("2024-01-01", periods=3)
    )
    
    result_beta1 = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            commission_bps=100.0,
        ),
    )
    
    result_beta2 = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=2.00,
            commission_bps=100.0,
        ),
    )
    
    gross_pair_notional1 = 1 + 1.0
    gross_pair_notional2 = 1 + 2.0
    
    gross_pair_ratio = gross_pair_notional2 / gross_pair_notional1
    
    assert gross_pair_ratio == pytest.approx(1.50)
    
    assert (result_beta1["borrow_cost"]==0.0).all()
    assert (result_beta1["financing_cost"]==0.0).all()
    
    assert (result_beta2["borrow_cost"]==0.0).all()
    assert (result_beta2["financing_cost"]==0.0).all()
    
    assert result_beta2.iloc[1]["trade_event_cost"] == pytest.approx(
        gross_pair_ratio * result_beta1.iloc[1]["trade_event_cost"]
    )
    
def test_beta_scales_borrow_cost_by_beta():
    
    positions = pd.Series(
        [0.0,1.0,1.0],
        index = pd.date_range("2024-01-01", periods=3)
    )
    
    result_beta1 = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            borrow_cost_annual_bps=252.0,
            trading_days=252
        ),
    )
    
    result_beta2 = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=2.00,
            borrow_cost_annual_bps=252.0,
            trading_days = 252
        ),
    )
    
    beta_1 = 1.0
    beta_2 = 2.0
    beta_ratio = beta_2 / beta_1
    
    assert beta_ratio == pytest.approx(2.0)
    
    assert (result_beta1["trade_event_cost"]==0.0).all()
    assert (result_beta1["financing_cost"]==0.0).all()
    
    assert (result_beta2["trade_event_cost"]==0.0).all()
    assert (result_beta2["financing_cost"]==0.0).all()
    
    assert result_beta2.iloc[1]["borrow_cost"] == pytest.approx(
        beta_ratio * result_beta1.iloc[1]["borrow_cost"]
    )

def test_beta_scales_financing_cost_by_beta():
    
    positions = pd.Series(
        [0.0,-1.0,-1.0],
        index = pd.date_range("2024-01-01", periods=3)
    )
    
    result_beta1 = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            financing_cost_annual_bps=252.0,
            trading_days=252
        ),
    )
    
    result_beta2 = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=2.00,
            financing_cost_annual_bps=252.0,
            trading_days = 252
        ),
    )
    
    beta_1 = 1.0
    beta_2 = 2.0
    beta_ratio = beta_2 / beta_1
    
    assert beta_ratio == pytest.approx(2.0)
    
    assert (result_beta1["trade_event_cost"]==0.0).all()
    assert (result_beta1["borrow_cost"]==0.0).all()
    
    assert (result_beta2["trade_event_cost"]==0.0).all()
    assert (result_beta2["borrow_cost"]==0.0).all()
    
    assert result_beta2.iloc[1]["financing_cost"] == pytest.approx(
        beta_ratio * result_beta1.iloc[1]["financing_cost"]
    )

def test_total_cost_equals_sum_of_cost_components():
    
    positions = pd.Series(
        [0.0,1.0,1.0,0.0,-1.0,-1.0,0.0],
        index = pd.date_range("2024-01-01", periods=7)
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            commission_bps=10.0,
            bid_ask_spread_bps=20.0,
            slippage_bps=30.0,
            market_impact_bps=40.0,
            borrow_cost_annual_bps=252.0,
            financing_cost_annual_bps=252.0,
            trading_days=252
        ),
    )
    
    expected = (
        result["trade_event_cost"]
        +
        result["borrow_cost"]
        +
        result["financing_cost"]
    )
    
    pd.testing.assert_series_equal(
        result["total_cost"],
        expected,
        check_names=False
    )
    
    assert (result["total_cost"]>=0).all()
    
#Output Integrity Test
def test_cost_model_preserves_output_structure():
    
    positions = pd.Series(
        [0.0,1.0,1.0,0.0,-1.0,-1.0,0.0],
        index = pd.date_range("2024-01-01", periods=7)
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            commission_bps=10.0,
            bid_ask_spread_bps=20.0,
            slippage_bps=30.0,
            market_impact_bps=40.0,
            borrow_cost_annual_bps=252.0,
            financing_cost_annual_bps=252.0,
            trading_days=252
        ),
    )
    
    assert len(positions) == len(result)
    assert (positions.index == result.index).all()
    
    required_cols = {
        "position",
        "position_change",
        "long_notional",
        "short_notional",
        "trade_event_cost",
        "borrow_cost",
        "financing_cost",
        "total_cost",
    }
    
    assert required_cols.issubset(result.columns)

def test_cost_model_preserves_input_positions():
    
    positions = pd.Series(
        [0.0,1.0,1.0,0.0,-1.0,-1.0,0.0],
        index = pd.date_range("2024-01-01", periods=7)
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            commission_bps=10.0,
            bid_ask_spread_bps=20.0,
            slippage_bps=30.0,
            market_impact_bps=40.0,
            borrow_cost_annual_bps=252.0,
            financing_cost_annual_bps=252.0,
            trading_days=252
        ),
    )
    
    original_positions = positions.copy(deep=True)
    
    pd.testing.assert_series_equal(
        original_positions,
        result['position'],
        check_names=False,
        check_index=True
    )
    
    pd.testing.assert_series_equal(
        original_positions,
        positions,
        check_names=False
    )
    
def test_cost_model_returns_only_finite_numeric_values():
    
    positions = pd.Series(
        [0.0,1.0,1.0,0.0,-1.0,-1.0,0.0],
        index = pd.date_range("2024-01-01", periods=7)
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            commission_bps=10.0,
            bid_ask_spread_bps=20.0,
            slippage_bps=30.0,
            market_impact_bps=40.0,
            borrow_cost_annual_bps=252.0,
            financing_cost_annual_bps=252.0,
            trading_days=252
        ),
    )
    
    numeric_cols = [
        "position",
        "position_change",
        "long_notional",
        "short_notional",
        "trade_event_cost",
        "borrow_cost",
        "financing_cost",
        "total_cost",
    ]
    
    assert np.isfinite(result[numeric_cols].to_numpy()).all()
    
def test_cost_model_returns_non_negative_economic_quantities():
    
    positions = pd.Series(
        [0.0,1.0,1.0,0.0,-1.0,-1.0,0.0],
        index = pd.date_range("2024-01-01", periods=7)
    )
    
    result = compute_pair_cost_series(
        positions=positions,
        **make_cost_kwargs(
            beta=1.00,
            commission_bps=10.0,
            bid_ask_spread_bps=20.0,
            slippage_bps=30.0,
            market_impact_bps=40.0,
            borrow_cost_annual_bps=252.0,
            financing_cost_annual_bps=252.0,
            trading_days=252
        ),
    )
    
    non_negative_cols = [
        "position_change",
        "long_notional",
        "short_notional",
        "trade_event_cost",
        "borrow_cost",
        "financing_cost",
        "total_cost",
    ]
    
    assert (result[non_negative_cols]>=0).all().all()