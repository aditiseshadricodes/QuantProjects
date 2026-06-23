import logging
import pytest
from src.cost_model import (
    bps_to_decimal,
    estimate_one_way_trade_event_cost_bps,
    estimate_holding_cost_bps,
    estimate_total_pair_cost_bps
)

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