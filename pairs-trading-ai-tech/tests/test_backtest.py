import pandas as pd
import pytest

from src.backtest import(
    compute_strategy_returns
)

def test_compute_strategy_returns_zero_costs_preserves_gross_returns():
    """
    When all cost assumptions are zero:

    strategy_return == strategy_return_before_cost

    This verifies that the detailed cost model behaves as a transparent
    layer when costs are disabled.
    """

    dates = pd.date_range(
        start="2024-01-01",
        periods=5,
        freq="D",
    )

    pair_returns = pd.DataFrame({
        "asset_y_returns":[0.00, 0.01, -0.02, 0.015, -0.005],
        "asset_x_returns":[0.00, 0.02, -0.01, 0.010, -0.015]
    },
        index=dates,
    )

    positions = pd.Series(
        [0.0, 1.0, 1.0, 0.0, 0.0],
        index=dates,
    )
    
    hedge_model = {
        "beta": 1.0,
    }

    result = compute_strategy_returns(
        pair_returns=pair_returns,
        positions=positions,
        hedge_model=hedge_model,
        commission_bps=0.0,
        bid_ask_spread_bps=0.0,
        slippage_bps=0.0,
        market_impact_bps=0.0,
        tax_bps=0.0,
        borrow_cost_annual_bps=0.0,
        financing_cost_annual_bps=0.0,
        trading_days=252,
    )
    
    assert (result["total_cost"]==0.0).all()
    pd.testing.assert_series_equal(
        result["strategy_return"],
        result["strategy_return_before_cost"],
        check_names=False,
    )
    
    assert(
        result["strategy_return_before_cost"]
        .abs()
        .gt(0)
        .any()
    )
    