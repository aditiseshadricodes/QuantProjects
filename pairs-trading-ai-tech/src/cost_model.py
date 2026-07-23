""" 
This module is used to simulate transaction costs of pairs trading. In V1, a simple 
pair level cost of 20bps was assumed. However, in V2, costs supported are:

- commission
- bid ask spread
- slippage
- market impact
- borrow costs
- financing costs
- taxes

Costs are grouped into:

1. Trade-event costs
    applied when positions open or close

2. Holding-period costs
    applied while positions remain active

Multiple cost scenarios may be evaluated
for robustness testing.
"""

import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

def bps_to_decimal(
    bps
):
    
    """ 
    Converts basis points into a decimal value by dividing by 10000
    """
    
    if not isinstance(bps,(int,float)):
        logger.error("The basis points value should be a number.")
        raise TypeError("The basis points value should be numeric.")
    logger.info("The value in basis points is numeric.")
    
    if bps < 0:
        logger.error("The value in basis points should not be negative.")
        raise ValueError("The value in basis points should not be negative.")
    logger.info("The value in basis points is valid.")
    
    return bps / 10_000

def estimate_one_way_trade_event_cost_bps(
    commission_bps,
    bid_ask_spread_bps,
    slippage_bps,
    market_impact_bps,
    tax_bps
):
    
    """ 
    The input is in basis points and the output will be converted to decimals 
    when costs are applied in the notebooks, therefore, the function output is
    also in bps. this function is calculating cost on a single leg, one event basis.
    """
    
    #Validate that all costs are numeric and greater than or equal to 0.
    if not isinstance(commission_bps,(int,float)):
        logger.error("The commission in basis points should be a number.")
        raise TypeError("The commission cost in basis points should be numeric.")
    logger.info("The commission value in basis points is numeric.")
    
    if commission_bps < 0:
        logger.error("The commission cost in basis points should not be negative.")
        raise ValueError("The commission cost in basis points should not be negative.")
    logger.info("Commission cost in basis points is valid.")
    
    if not isinstance(bid_ask_spread_bps,(int,float)):
        logger.error("The bid-ask spread in basis points should be a number.")
        raise TypeError("The bid-ask spread in basis points should be numeric.")
    logger.info("The bid-ask spread in basis points is numeric.")
    
    if bid_ask_spread_bps < 0:
        logger.error("The bid-ask spread in basis points should not be negative.")
        raise ValueError("The bid-ask spread in basis points should not be negative.")
    logger.info("The bid-ask spread in basis points is valid.")
    
    if not isinstance(slippage_bps,(int,float)):
        logger.error("The slippage in basis points should be a number.")
        raise TypeError("The slippage in basis points should be numeric.")
    logger.info("The slippage in basis points is numeric.")
    
    if slippage_bps < 0:
        logger.error("The slippage in basis points should not be negative.")
        raise ValueError("The slippage in basis points should not be negative.")
    logger.info("Slippage in basis points is valid.")
    
    if not isinstance(market_impact_bps,(int,float)):
        logger.error("The market impact in basis points should be a number.")
        raise TypeError("The market impact in basis points should be numeric.")
    logger.info("The market impact in basis points is numeric.")
    
    if market_impact_bps < 0:
        logger.error("The market impact in basis points should not be negative.")
        raise ValueError("The market impact in basis points should not be negative.")
    logger.info("The market impact value in basis points is valid.")
    
    if not isinstance(tax_bps,(int,float)):
        logger.error("The tax rate in basis points should be a number.")
        raise TypeError("The tax rate in basis points should be numeric.")
    logger.info("The tax rate in basis points is numeric.")
    
    if tax_bps < 0:
        logger.error("The tax rate in basis points should not be negative.")
        raise ValueError("The tax rate in basis points should not be negative.")
    logger.info("The tax rate in basis points is valid.")
        
    #Calculate the one-way trading cost when a trading event happens
    total_trade_cost_one_way = (
        commission_bps + 
        bid_ask_spread_bps + 
        slippage_bps + 
        market_impact_bps + 
        tax_bps
    )
        
    
    return total_trade_cost_one_way

def estimate_holding_cost_bps(
    holding_days,
    borrow_cost_annual_bps,
    financing_cost_annual_bps,
    trading_days = 252
):
    
    """ 
    Converting the annual borrowing and financing costs into a per day basis and 
    multiplying by trading days.
    """
    
    #Validate that all costs are numeric and greater than or equal to 0.
    if not isinstance(holding_days,(int)):
        logger.error("The holding_days duration should be an integer.")
        raise TypeError("The holding_days duration should be an integer.")
    logger.info("The holding days duration is numeric.")
    
    if holding_days < 0:
        logger.error("The holding_days duration should be positive.")
        raise ValueError("The holding_days duration should be positive.")
    logger.info("The holding_days duration is valid.")
    
    if not isinstance(borrow_cost_annual_bps,(int,float)):
        logger.error("The annual borrowing cost in  basis points should be a number.")
        raise TypeError("The annual borrowing cost in basis points should be numeric.")
    logger.info("The annual borrowing cost in basis points is numeric.")
    
    if borrow_cost_annual_bps < 0:
        logger.error("The annual borrowing cost in basis points should not be negative.")
        raise ValueError("The annual borrowing cost in basis points should not be negative.")
    logger.info("The annual borrowing cost in basis points is valid.")
    
    if not isinstance(financing_cost_annual_bps,(int,float)):
        logger.error("The annual financing cost should be a number.")
        raise TypeError("The annual financing cost in basis points should be numeric.")
    logger.info("The annual financing cost in basis points is numeric.")
    
    if financing_cost_annual_bps < 0:
        logger.error("The annual financing cost in basis points should not be negative.")
        raise ValueError("The annual financing cost in basis points should not be negative.")
    logger.info("The annual financing cost in basis points is valid.")
    
    if not isinstance(trading_days, int):
        logger.error("Trading days should be an integer.")
        raise TypeError("Trading days should be an integer.")
    
    if trading_days <= 0:
        logger.error("Trading days should be positive.")
        raise ValueError("Trading days should be positive.")
    
    #Calculate cost of holding an asset in pairs trading
    borrow_cost_daily = borrow_cost_annual_bps / trading_days
    financing_cost_daily = financing_cost_annual_bps / trading_days
    
    borrow_cost_holding = borrow_cost_daily * holding_days
    financing_cost_holding = financing_cost_daily * holding_days
    
    total_holding_cost = borrow_cost_holding + financing_cost_holding
    
    return total_holding_cost

def estimate_total_pair_cost_bps(
    holding_days,
    commission_bps,
    bid_ask_spread_bps,
    slippage_bps,
    market_impact_bps,
    tax_bps,
    borrow_cost_annual_bps,
    financing_cost_annual_bps,
    trading_days = 252
):
    
    """
    Estimate the total round-trip cost for a pairs trade in basis points.

    The total cost combines:

    1. Trade-event costs:
        Costs incurred when opening and closing both legs of the pair.
        Since a pairs trade has two legs and both entry and exit events,
        the one-way single-leg trade-event cost is multiplied by 4.

    2. Holding-period costs:
        Borrowing and financing costs prorated over the number of holding days.

    Parameters
    ----------
    holding_days : int
        Number of trading days the pair position is held.
    commission_bps : int or float
        Commission or brokerage cost per leg-event, in basis points.
    bid_ask_spread_bps : int or float
        Bid-ask spread cost per leg-event, in basis points.
    slippage_bps : int or float
        Slippage cost per leg-event, in basis points.
    market_impact_bps : int or float
        Market impact cost per leg-event, in basis points.
    tax_bps : int or float
        Tax or transaction-tax proxy per leg-event, in basis points.
    borrow_cost_annual_bps : int or float
        Annualized borrow cost for the short leg, in basis points.
    financing_cost_annual_bps : int or float
        Annualized financing or margin cost, in basis points.
    trading_days : int, default 252
        Number of trading days used for annual-to-daily cost conversion.

    Returns
    -------
    int or float
        Total estimated pair trade cost in basis points.
    """
    
    #Computing both trade event and holding costs
    total_pair_trade_cost = 4 * estimate_one_way_trade_event_cost_bps(
        commission_bps=commission_bps,
        bid_ask_spread_bps=bid_ask_spread_bps,
        slippage_bps=slippage_bps,
        market_impact_bps=market_impact_bps,
        tax_bps=tax_bps
    )
        
    total_holding_cost = estimate_holding_cost_bps(
        holding_days=holding_days,
        borrow_cost_annual_bps=borrow_cost_annual_bps,
        financing_cost_annual_bps=financing_cost_annual_bps,
        trading_days=trading_days
    )
    
    total_pair_cost = total_pair_trade_cost + total_holding_cost
    
    return total_pair_cost

def compute_pair_cost_series(
    positions,
    beta,
    commission_bps,
    bid_ask_spread_bps,
    slippage_bps,
    market_impact_bps,
    tax_bps,
    borrow_cost_annual_bps,
    financing_cost_annual_bps,
    trading_days=252
):
    """
    Compute daily trade-event and holding-period costs for a pair position.
    Costs are returned in decimal-return units, not basis points.
    The strategy is assumed to be flat immediately before the first observation.
    """
    
    if not isinstance(positions, pd.Series):
        raise TypeError("positions must be a pandas Series.")

    if positions.empty:
        raise ValueError("positions cannot be empty.")

    if positions.isna().any():
        raise ValueError("positions cannot contain missing values.")

    if not positions.isin([-1, 0, 1]).all():
        raise ValueError("positions must contain only -1, 0, or 1.")

    if not isinstance(beta, (int, float)) or not np.isfinite(beta):
        raise ValueError("beta must be a finite numeric value.")

    if not isinstance(trading_days, int) or trading_days <= 0:
        raise ValueError("trading_days must be a positive integer.")

    previous_position = positions.shift(1).fillna(0)
    position_change = (positions - previous_position).abs()
    
    #Estimate one-way transaction cost in bps and as decimal.
    one_way_cost_bps = estimate_one_way_trade_event_cost_bps(
        commission_bps,
        bid_ask_spread_bps,
        slippage_bps,
        market_impact_bps,
        tax_bps
    )
    one_way_cost_rate = bps_to_decimal(
        one_way_cost_bps
    )
    
    #Calculating scaled costs
    gross_pair_notional = 1 + abs(beta)
    trade_event_cost = (
        position_change
        * gross_pair_notional
        * one_way_cost_rate
    )
    y_exposure = positions.astype(float)
    x_exposure = -beta * positions.astype(float)
    
    long_notional = (
        y_exposure.clip(lower=0)
        + x_exposure.clip(lower=0)
    )

    short_notional = (
        y_exposure.clip(upper=0).abs()
        + x_exposure.clip(upper=0).abs()
    )
    
    daily_borrow_rate = bps_to_decimal(borrow_cost_annual_bps) / trading_days
    borrow_cost = short_notional * daily_borrow_rate
    
    daily_financing_rate = bps_to_decimal(financing_cost_annual_bps) / trading_days
    financing_cost = long_notional * daily_financing_rate
    
    result_df = pd.DataFrame(
        {
            "position":positions,
            "position_change":position_change,
            "long_notional":long_notional,
            "short_notional":short_notional,
            "trade_event_cost":trade_event_cost,
            "borrow_cost":borrow_cost,
            "financing_cost":financing_cost,
        },
        index=positions.index
    )
    
    result_df["total_cost"] = result_df[
        ["trade_event_cost","borrow_cost","financing_cost"]
    ].sum(axis=1)
    
    cost_columns = [
        "trade_event_cost",
        "borrow_cost",
        "financing_cost",
        "total_cost",
    ]

    if result_df[cost_columns].isna().any().any():
        raise ValueError("Cost calculation produced missing values.")

    if (result_df[cost_columns] < 0).any().any():
        raise ValueError("Cost calculation produced negative costs.")
    
    return result_df