
""" 
This module contains functions  for converting spread/z-scores into positions and 
backtest returns for the pairs trading strategy.
 
 Module tasks:
 -generate z-score based trading signals
 -convert signals into held positions
 -apply one-period lag to reduce look-ahead bias
 -compute pair-level strategy returns
 -optionally estimate transaction costs
 
It does not fetch data or estimate hedge ratios. It assumes that the spread and 
z-score features have already been created using spread_model.py.
"""

import pandas as pd
import numpy as np
from src.cost_model import compute_pair_cost_series

def generate_zscore_signals(
    zscore,
    entry_threshold = 2.0,
    exit_threshold = 0.5
):
    
    #z-score is a pandas Series
    if not isinstance(zscore, pd.Series):
        raise TypeError("zscore should be a pandas Series.")
    
    #z-score is not empty check
    if zscore.empty:
        raise ValueError("zscore should not be empty.")
    
    #entry_threshold is positive and numeric
    if not isinstance( entry_threshold,(int,float,np.number)):
        raise TypeError("entry_threshold should be numeric")
    
    if entry_threshold <= 0:
        raise ValueError("entry_threshold should be positive.")
    
    #exit_threshold is positive and numeric
    if not isinstance( exit_threshold,(int,float,np.number)):
        raise TypeError("exit_threshold should be numeric")
    
    if exit_threshold < 0:
        raise ValueError("exit_threshold should be positive.")
    
    #exit_threshold should be less than entry_threshold
    if exit_threshold >= entry_threshold:
        raise ValueError("entry_threshold should be greater than exit_threshold.")
    
    #conditions
    conditions = [zscore < -entry_threshold, zscore > entry_threshold, zscore.abs() <= exit_threshold]
    
    #signal vals
    values = [1, -1, 0]
    
    #create signal
    signals = pd.Series(np.select(conditions, values, default=np.nan), index = zscore.index)
    signals.name = "zscore_signal"
    
    return signals

def generate_positions_from_signals(
    signals
):
    
    #signals is a pandas Series
    if not isinstance(signals, pd.Series):
        raise TypeError("signals should be a pandas Series.")
    
    #signals is not empty
    if signals.empty:
        raise ValueError("signals should not be empty.")
    
    #signals should only contain 1, -1, 0, or nan.
    if not signals.dropna().isin([-1, 0, 1]).all():
        raise ValueError("signals should only contain 1, -1, 0, or nan.")
    
    current_position = 0
    positions = []
    
    for signal in signals:
        if pd.isna(signal):
            pass 
        
        else:
            current_position = signal
        
        positions.append(current_position)
    
    positions = pd.Series(positions, index = signals.index)
    positions.name = "position"
    
    return positions

def compute_pair_returns(
    price_matrix,
    asset_y,
    asset_x,
    min_observations = 60
):
    
    #price_matrix is a pandas DataFrame
    if not isinstance(price_matrix, pd.DataFrame):
        raise TypeError("price_matrix should be a pandas DataFrame.")
    
    #price matrix is not empty
    if price_matrix.empty:
        raise ValueError("price_matrix should not be empty.")
    
    #min_observations is positive and an integer
    if not isinstance(min_observations, (int, np.number)):
        raise TypeError("min_observations should be an integer.")
    
    if min_observations <= 0:
        raise ValueError("min_observations should be positive.")
    
    #asset_y and asset_x exist in the columns of price-matrix
    if not asset_y in price_matrix.columns or not asset_x in price_matrix.columns:
        raise ValueError("asset_y and asset_x must exist in the price_matrix.")
    
    #there are enough observations in price_matrix
    if price_matrix.shape[0] < min_observations:
        raise ValueError("Too few observations in price_matrix.")
    
    #asset_y is different from asset_x
    if asset_y == asset_x:
        raise ValueError("asset_y must be different from asset_x.")
    
    #Extract both series
    prices_y = price_matrix[asset_y]
    prices_x = price_matrix[asset_x]
    
    #Prices for both series are positive
    if (prices_y<=0).any() or (prices_x<=0).any():
        raise ValueError("price values must be positive.")
    
    #compute log returns
    log_ret_y = np.log(prices_y).diff()
    log_ret_x = np.log(prices_x).diff()
    
    #combine into one DataFrame
    pair_returns = pd.concat([log_ret_y, log_ret_x], axis=1).dropna()
    pair_returns.columns = ["asset_y_returns", "asset_x_returns"]
    
    #there are enough observations in log_returns
    if pair_returns.shape[0] < min_observations:
        raise ValueError("Too few observations in log_returns.")
    
    return pair_returns

def compute_strategy_returns(
    pair_returns,
    positions,
    hedge_model,
    commission_bps,
    bid_ask_spread_bps,
    slippage_bps,
    market_impact_bps,
    tax_bps,
    borrow_cost_annual_bps,
    financing_cost_annual_bps,
    trading_days=252,
):
    
    #pair_returns is a pandas DataFrame
    if not isinstance(pair_returns, pd.DataFrame):
        raise TypeError("pair_returns should be a pandas DataFrame.")
    
    #pair_returns is  not empty
    if pair_returns.empty:
        raise ValueError("pair_returns should not be empty.")
    
    #asset_y_returns and asset_x_returns are in pair_returns
    required_cols = ["asset_y_returns","asset_x_returns"]
    if not all(col in pair_returns.columns for col in required_cols):
        raise ValueError("asset_y_returns and asset_x_returns should be in pair_returns.")
    
    
    #positions is a pandas Series
    if not isinstance(positions, pd.Series):
        raise TypeError("positions should be a pandas Series.")
    
    #positions is not empty
    if positions.empty:
        raise ValueError("positions should not be empty.")
    
    #positions can only contain 0, -1 and 1
    if not (positions.dropna().isin([-1, 1, 0])).all():
        raise ValueError("positions can only contain -1, 1, 0.")
    
    #hedge model is a dictionary
    if not isinstance(hedge_model, dict):
        raise TypeError("hedge_model should be a dictionary.")
    
    #hedge_model contains beta
    if not "beta" in hedge_model:
        raise ValueError("hedge_model should have beta.")
    
    #beta is numeric
    beta = hedge_model["beta"]
    if not isinstance(beta, (int, float, np.number)):
        raise TypeError("beta should be numeric.")
    
    #transaction cost is numeric and nonnegative
    if not isinstance(commission_bps,(int,float,np.number)):
        raise TypeError("commission should be numeric.")
    
    if commission_bps < 0:
        raise ValueError("commission should be nonnegative.")
    
    #align returns and positions by date
    positions = positions.copy()
    positions.name = "position"
    returns_position_df = pd.concat([pair_returns,positions],axis=1).dropna()
    
    if returns_position_df.empty:
        raise ValueError("No overlapping observations between pair_returns and positions.")
    
    #spread_return computation
    returns_position_df["spread_return"] = returns_position_df["asset_y_returns"] - beta*returns_position_df["asset_x_returns"]
    
    #lag the position
    returns_position_df["lagged_position"] = returns_position_df["position"].shift(1).fillna(0)
    
    
    #compute strategy_return
    returns_position_df["strategy_return_before_cost"] = returns_position_df["lagged_position"]* returns_position_df["spread_return"]
    
    #adding in transaction costs
    returns_position_df["position_change"] = returns_position_df["lagged_position"].diff().abs().fillna(0)
    cost_result = compute_pair_cost_series(
        positions=returns_position_df["lagged_position"],
        beta=beta,
        commission_bps=commission_bps,
        bid_ask_spread_bps=bid_ask_spread_bps,
        slippage_bps=slippage_bps,
        market_impact_bps=market_impact_bps,
        tax_bps=tax_bps,
        borrow_cost_annual_bps=borrow_cost_annual_bps,
        financing_cost_annual_bps=financing_cost_annual_bps,
        trading_days=trading_days
    )
    returns_position_df["total_cost"] = cost_result["total_cost"]
    returns_position_df["strategy_return"] = returns_position_df["strategy_return_before_cost"] - returns_position_df["total_cost"]
    
    return returns_position_df

def run_pair_backtest(
    price_matrix,
    zscore,
    hedge_model,
    commission_bps,
    bid_ask_spread_bps,
    slippage_bps,
    market_impact_bps,
    tax_bps,
    borrow_cost_annual_bps,
    financing_cost_annual_bps,
    entry_threshold = 2.0,
    exit_threshold = 0.5,
    trading_days=252,
    min_observations = 60
):
    
    #price_matrix is a pandas DataFrame which is not empty
    if not isinstance(price_matrix, pd.DataFrame):
        raise TypeError("price_matrix must be a pandas DataFrame.")
    
    if price_matrix.empty:
        raise ValueError("price_matrix must not be empty.")
    
    #zscore is a pandas Series and is not empty
    if not isinstance(zscore, pd.Series):
        raise TypeError("zscore must be a pandas Series.")
    
    if zscore.empty:
        raise ValueError("zscore must not be empty.")
    
    #hedge_model ia a dictionary and has asset_y, asset_x and beta
    if not isinstance(hedge_model,dict):
        raise TypeError("hedge_model should be a dictionary.")
    
    if "beta" not in hedge_model:
        raise ValueError("hedge_model must contain beta.")
    
    if "asset_y" not in hedge_model:
        raise ValueError("hedge_model must contain asset_y.")
    
    if "asset_x" not in hedge_model:
        raise ValueError("hedge_model must contain asset_x.")
    
    asset_x = hedge_model["asset_x"]
    asset_y = hedge_model["asset_y"]
    beta = hedge_model["beta"]
    
    if not isinstance(asset_y,str):
        raise TypeError("asset_y should be a string.")
    
    if not isinstance(asset_x, str):
        raise TypeError("asset_x should be a string.")
    
    if not isinstance(beta,(int,float,np.number)):
        raise TypeError("beta must be numeric.")
    
    #Orchestration of the backtest functions
    
    signals = generate_zscore_signals(zscore,entry_threshold,exit_threshold)
    
    positions = generate_positions_from_signals(signals)
    
    pair_returns = compute_pair_returns(
        price_matrix,
        asset_y,
        asset_x,
        min_observations
    )
    
    backtest_df = compute_strategy_returns(
        pair_returns,
        positions,
        hedge_model,
        commission_bps,
        bid_ask_spread_bps,
        slippage_bps,
        market_impact_bps,
        tax_bps,
        borrow_cost_annual_bps,
        financing_cost_annual_bps,
        trading_days,
    )
    
    results = {
        "asset_y":asset_y,
        "asset_x":asset_x,
        "hedge_model":hedge_model,
        "entry_threshold":entry_threshold,
        "exit_threshold":exit_threshold,
        "total_cost":backtest_df["total_cost"],
        "signals":signals,
        "positions":positions,
        "pair_returns":pair_returns,
        "backtest_df":backtest_df,
        "method":"zscore_threshold_pairs_backtest"
    }
    
    return results