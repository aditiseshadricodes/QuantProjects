"""
This module builds the functions for spread and z-scores in the pairs trading strategy.

Inputs:
-Validated price matrix with rows representing dates, columns representing assets/tickers, and values representing adjusted close prices or another positive price series.

Outputs:
-Log computation of prices
-The spread calculated between the two assets in the pair
-The z-score pointing to entry and exit points.

Warning:
-This module does not execute trades or perform any backtesting.
"""
import pandas as pd
import numpy as np

def compute_log_prices(price_matrix):
    
    if not isinstance(price_matrix,pd.DataFrame):
        raise TypeError("Input price matrix must be a pandas DataFrame.")
    
    if price_matrix.empty:
        raise ValueError("Input price matrix is empty.")
    
    if (price_matrix <=0).any().any():
        raise ValueError("Price matrix contains non-positive values, cannot compute log prices.")
    
    log_price_matrix = np.log(price_matrix)
    
    return log_price_matrix

def estimate_hedge_model(log_price_matrix,asset_y,asset_x,min_observations=60):
    
    #Validation checks similar to data_validator.py    
    if not isinstance(log_price_matrix,pd.DataFrame):
        raise TypeError("Input log price matrix must be a pandas DataFrame.")
    
    if log_price_matrix.empty:
        raise ValueError("Input log price matrix is empty.")
    
    if asset_y not in log_price_matrix.columns or asset_x not in log_price_matrix.columns:
        raise ValueError("Both assets must be present in the log price matrix.")
    
    if asset_y == asset_x:
        raise ValueError("Asset Y and Asset X must be different for pairs trading.")
    
    #Extract the 2 series
    y=log_price_matrix[asset_y]
    x=log_price_matrix[asset_x]
    
    #combine the 2 series into 1 dataframe and drop any missing values
    regression_data = pd.concat([y,x],axis=1).dropna() 
    
    if regression_data.shape[0] < min_observations:
        raise ValueError(f"Not enough observations to estimate hedge ratio. Minimum required is {min_observations}.")    
    
    #Calculate the alpha and beta using a simple line regression 
    #We can use np.polyfit to estimate the slope (hedge ratio) and intercept
    beta, alpha = np.polyfit(regression_data[asset_x],regression_data[asset_y],1) 
    
    hedge_model = {
        'asset_y':asset_y,
        'asset_x':asset_x,
        'alpha':alpha,
        'beta':beta,
        'num_observations':regression_data.shape[0],
        'method':'np.polyfit_degree_1'
    }
    
    return hedge_model

def compute_spread(log_price_matrix,hedge_model):
        
    #log_price_matrix is a pandas DataFrame check
    if not isinstance(log_price_matrix, pd.DataFrame):
        raise TypeError("Input log price matrix must be a pandas DataFrame.")
    
    #Log price matrix is non-empty check
    if log_price_matrix.empty:
        raise ValueError("Input log price matrix is empty.")
    
    #Hedge model is a dictionary check
    if not isinstance(hedge_model, dict):
        raise TypeError("Hedge model must be a dictionary containing 'asset_y', 'asset_x', 'alpha', and 'beta'.")
    
    #Hedge model contains required keys check
    if not all(key in hedge_model for key in ['alpha','beta','asset_y','asset_x']):
        raise ValueError("Hedge model dictionary must contain 'asset_y', 'asset_x', 'alpha', and 'beta'.")
    
    #asset_y and asset_x are present in log price matrix check
    if not asset_y in log_price_matrix.columns or not asset_x in log_price_matrix.columns:
        raise ValueError("Both assets in the hedge model must be present in the log price matrix.")
    
    #Alpha and beta are numeric values check
    if not isinstance(hedge_model['alpha'],(int, float, np.number)) or not isinstance(hedge_model['beta'],(int, float, np.number)):
        raise TypeError("Alpha and Beta in the hedge model must be numeric values.")   
    
    asset_y = hedge_model['asset_y']
    asset_x = hedge_model['asset_x']
    alpha = hedge_model['alpha']
    beta = hedge_model['beta']
    
    #Compute the spread using the formula: spread = log(y) - alpha - beta*log(x)
    spread = log_price_matrix[asset_y] - alpha - beta*log_price_matrix[asset_x]
    spread.name = f"{asset_y}_{asset_x}_spread"
    
    return spread

def compute_zscore(spread, window=60):
    
    #spread is a pandas Series check
    if not isinstance(spread, pd.Series):
        raise TypeError("Spread must be a pandas Series.")
    
    #Spread is non-empty check
    if spread.empty:
        raise ValueError("Spread should not be empty.")
    
    #Window is positive, an integer and less than the length of the spread
    if not isinstance(window, int) or window <=0  or window >= len(spread):
        raise ValueError("Window should be a positive integer less than the length of spread.")
    
    #Rolling standard deviation should not be zero check
    rolling_std = spread.rolling(window=window).std()
    if (rolling_std == 0).any():
        raise ValueError("The rolling standard deviation of spread should not be zero.")
    
    rolling_mean = spread.rolling(window=window).mean()
    zscore = (spread - rolling_mean)/rolling_std
    zscore.name = f"{spread.name}_zscore"
    return zscore