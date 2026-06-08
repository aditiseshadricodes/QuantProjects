""" 
The purpose of this module is to take the stocks present in the universe(Large Cap 
Tech Stocks) and using the given price matrix and dollar volume matrix, identify suitable
pairs for pairs trading.

Inputs:
-price_matrix which is a validated pandas DataFrame of adjusted close price values
-dollar_volume_matrix which is validated and contains the product of price and volume 
matrix data.

Outputs:
-A ranked Dataframe of candidate pairs.

Warning: This module does not compute spreads, z-scores, backtests or metrics.

Model Assumptions: This module uses a set of configurable default assumptions for 
pair selection. These defaults are chosen for a simple and interpretable v1
daily-data research pipeline. They are not treated as universal truths; they are 
parameters that can be stress-tested in later research.

1. lag = 1
The half-life estimate uses a one-observation lag because the input data is
daily. This means the model tests whether yesterday's spread helps explain
today's change in spread. Alternative approaches include testing multiple
lags, using an AR(p) model, or calibrating a continuous-time Ornstein-Uhlenbeck
process. A one-lag model is used in v1 because it is simple, interpretable,
and appropriate for a first-pass mean-reversion diagnostic.
2. min_avg_dollar_volume = 10_000_000
The liquidity filter uses average dollar volume rather than raw share volume
because dollar volume accounts for both price and trading activity. A $10M
threshold is used as a configurable v1 liquidity floor to remove obviously
illiquid assets while keeping the large-cap universe broad enough for testing.
Alternatives include stricter thresholds such as $50M or $100M, bid-ask
spread filters, or market-impact models.
3. pvalue_threshold = 0.05
The cointegration test uses a 5% p-value threshold as a standard first-pass
statistical significance cutoff. This helps identify pairs with evidence of
a stable long-run relationship. Alternatives include stricter thresholds such
as 0.01, ranking pairs by p-value without a hard cutoff, or applying
multiple-testing corrections when many pairs are tested.
4. min_observations = 60
The minimum observation count is set to 60 to avoid estimating correlations,
cointegration, or half-life on very small samples. For daily data, this is
roughly three months of observations. For more robust research, this value
can be increased to 126, 252, or higher.
5. trend = "c"
The cointegration test uses a constant-only trend assumption. This reflects
the pairs-trading idea that two assets may have a stable long-run relationship
around an intercept. Alternatives include no constant, a constant plus linear
trend, or testing multiple trend specifications.
6. use_log_prices = True
Log prices are used because they make price relationships more proportional
and consistent with the spread modeling step. This is useful when assets have
different price levels. Alternatives include raw price levels or normalized
price series, but log prices are preferred in v1 for interpretability and
consistency.
7. correlation on log returns
Pair correlation is computed using log returns rather than raw price levels.
This avoids overstating relationships simply because price series trend over
time. Correlation is used only as a first filter; it is combined with
cointegration, half-life, and liquidity checks.
8. top_n = 5
The pipeline returns the top five candidate pairs to keep the modeling
notebook readable while avoiding manual selection of a single pair. Later
versions can test different top-N choices or backtest all pairs passing the
selection filters.
"""

import pandas as pd
import numpy as np
import itertools
from statsmodels.tsa.stattools import coint
from src.spread_model import compute_log_prices, estimate_hedge_model, compute_spread

def generate_candidate_pairs(price_matrix):
    
    #Pandas Dataframe check
    if not isinstance(price_matrix, pd.DataFrame):
        raise TypeError("Price matrix should be a pandas DataFrame.")
    
    #Price matrix is not empty check
    if price_matrix.empty:
        raise ValueError("The price matrix should not be empty.")
    
    #Price matrix should have at least 2 assets
    if price_matrix.shape[1] < 2:
        raise ValueError("Price matrix should have at least 2 assets.")
    
    #Price matrix shouldn't have duplicated columns
    if price_matrix.columns.duplicated().any():
        raise ValueError("The price matrix columns should be unique.")
    
    asset_list = list(price_matrix.columns)
    
    pairs_list = list(itertools.combinations(asset_list,2))
    
    return pairs_list

def compute_pair_correlation(price_matrix,asset_y,asset_x,min_observations=60):
    
    #Pandas Dataframe check
    if not isinstance(price_matrix, pd.DataFrame):
        raise TypeError("Price matrix should be a pandas DataFrame.")
    
    #Price matrix is not empty check
    if price_matrix.empty:
        raise ValueError("The price matrix should not be empty.")
    
    #Check that asset_y and asset_x are in the columns of price matrix
    if not asset_y in price_matrix.columns or not asset_x in price_matrix.columns:
        raise ValueError("Asset is missing from the price matrix.")
    
    #The two assets are different
    if asset_y == asset_x:
        raise ValueError("The two assets should be different.")
    
    #Extracting the 2 price series
    price_y = price_matrix[asset_y]
    price_x = price_matrix[asset_x]
    
    #Obtaining returns. Here we will be using log returns as spread_model.py uses log_prices
    # Formula used: log_return = log(price_today) - log(price_yesterday)
    log_ret_y = np.log(price_y).diff()
    log_ret_x = np.log(price_x).diff()
    
    #Combining into one DataFrame and dropping null values
    log_returns = pd.concat([log_ret_y,log_ret_x],axis=1)
    log_returns = log_returns.dropna()
    
    #Checking if enough returns are present
    if log_returns.shape[0] < min_observations:
        raise ValueError("Insufficient number of observations in log returns present.")
    
    #Calculate the correlation between asset_y and asset_x
    correlation = log_returns[asset_y].corr(log_returns[asset_x])
    
    #Summary Dictionary
    summary = {
    "asset_y": asset_y,
    "asset_x": asset_x,
    "correlation": correlation,
    "num_observations": log_returns.shape[0],
    "method": "log_return_correlation"
    }
    
    return summary

def run_cointegration_test(price_matrix,asset_y,asset_x,min_observations=60,pvalue_threshold=0.05,trend='c',use_log_prices=True):
    
    #Pandas Dataframe check
    if not isinstance(price_matrix, pd.DataFrame):
        raise TypeError("Price matrix should be a pandas DataFrame.")
    
    #Price matrix is not empty check
    if price_matrix.empty:
        raise ValueError("The price matrix should not be empty.")
    
    #Check that asset_y and asset_x are in the columns of price matrix
    if not asset_y in price_matrix.columns or not asset_x in price_matrix.columns:
        raise ValueError("Asset is missing from the price matrix.")
    
    #The two assets are different
    if asset_y == asset_x:
        raise ValueError("The two assets should be different.")
    
    #Extracting the 2 price series
    price_y = price_matrix[asset_y]
    price_x = price_matrix[asset_x]
    
    #Checking type of use_log_prices
    if not isinstance(use_log_prices,bool):
        raise TypeError("The flag for using log prices should be True or False.")
    
    #Check for using log prices
    if use_log_prices:
        if (price_y<=0).any() or (price_x<=0).any():
            raise ValueError("Price values can only be positive.")
        price_y = np.log(price_y)
        price_x = np.log(price_x)
        
    #Combining into one DataFrame
    price_vals = pd.concat([price_y,price_x], axis=1).dropna()
    
    #Checking if enough returns are present
    if price_vals.shape[0] < min_observations:
        raise ValueError("Insufficient number of observations in price values present.")
    
    #Performing the cointegration test
    results = coint(price_vals[asset_y],price_vals[asset_x],trend=trend)
    
    t_stat, p_value, critical_vals = results
    
    cointegration_passed = p_value < pvalue_threshold
    
    summary_dict = {
        "asset_y":asset_y,
        "asset_x":asset_x,
        "pvalue_threshold": pvalue_threshold,
        "trend": trend,
        "use_log_prices": use_log_prices,
        "cointegration_stat":t_stat,
        "cointegration_pvalue":p_value,
        "critical_values":critical_vals,
        "cointegration_passed":cointegration_passed,
        "num_observations":price_vals.shape[0],
        "method":"statsmodels_coint_optional_log_prices"
    }
    
    return summary_dict

def estimate_half_life(spread, min_observations=60, max_missing_threshold = 0.05):
    
    """ 
    The purpose of this function is to check the half-life of the spread.
    The main idea here is: If the spread is away from its mean, how long does it
    typically take to move halfway back? For pairs trading, this matters because 
    a pair can be cointegrated but still mean-revert too slowly to be useful.
    """
    
    #Spread is a pandas Series.
    if not isinstance(spread, pd.Series):
        raise TypeError("The spread should be a pandas Series.")
    
    #Spread is not empty
    if spread.empty:
        raise ValueError("The spread cannot be empty.")
    
    #integer type check for min_observations
    if not isinstance(min_observations, int):
        raise TypeError("min_observations should be of type integer.")
    
    #min_observations is a positive integer
    if min_observations <= 0:
        raise ValueError("min_observations should be a positive integer.")
    
    #Type check of max_missing_threshold
    if not isinstance(max_missing_threshold, (int,float,np.number)):
        raise TypeError("max_missing_threshold should be a numeric value.")
    
    #Value check of max_missing_threshold
    if max_missing_threshold < 0 or max_missing_threshold >=1:
        raise ValueError("The max_missing_threshold is incorrect.")
    
    #missing values is in an acceptable threshold
    if spread.isnull().mean() > max_missing_threshold:
        raise ValueError("There are too many missing values.")
    
    #obtaining a clean spread
    clean_spread = spread.dropna()
    
    if len(clean_spread) < min_observations:
        raise ValueError("There are too few observations in the clean spread.")
    
    #Obtaining lagged spread and delta of spread
    spread_lag = clean_spread.shift(1)
    
    delta_spread = clean_spread - spread_lag
    
    #Obtaining regression data and dropping null values
    regression_data = pd.concat([delta_spread,spread_lag],axis=1).dropna()
    regression_data.columns = ["delta_spread", "spread_lag"]
    
    #Check for sufficient rows for half-life regression
    if regression_data.shape[0] < min_observations:
        raise ValueError("There are too few observations for half-life regression.")
    
    #Regressing using np.polyfit, as we need the beta value
    beta, alpha = np.polyfit(regression_data["spread_lag"],regression_data["delta_spread"],1)
    
    #Half-life calculation based on beta
    if beta >= 0:
        half_life = np.inf
    else:
        half_life = -np.log(2) / beta
        
    summary_dict = {
        "half_life":half_life,
        "mean_reversion_beta":beta,
        "alpha":alpha,
        "num_observations":regression_data.shape[0],
        "method":"lagged_spread_regression"
    }
    
    
    return summary_dict

def compute_liquidity_metrics(dollar_volume_matrix, asset_y, asset_x, min_observations=60,min_avg_dollar_volume =10_000_000):
    
    #dollar_volume_matrix is a pandas DataFrame
    if not isinstance(dollar_volume_matrix,pd.DataFrame):
        raise TypeError("dollar_volume_matrix must be a pandas DataFrame.")
    
    #dollar_volume_matrix is not empty check
    if dollar_volume_matrix.empty:
        raise ValueError("dollar_volume_matrix should not be empty.")
    
    #asset_y and asset_x exist in the columns
    if not asset_y in dollar_volume_matrix.columns or not asset_x in dollar_volume_matrix.columns:
        raise ValueError("asset_y and asset_x should be in dollar_volume_matrix.")
    
    #check that the assets are different
    if asset_y == asset_x:
        raise ValueError("asset_y should be different from asset_x.")
    
    #Check that min_observations is an integer
    if not isinstance(min_observations, int):
        raise TypeError("min_observations should be an integer.")
    
    #Check that min_observations is a positive integer:
    if min_observations <= 0:
        raise ValueError("min_observations must be a positive integer.")
    
    #Check that min_avg_dollar_volume is numeric
    if not isinstance(min_avg_dollar_volume,(int,float,np.number)):
        raise TypeError("min_avg_dollar_volume must be numeric.")
    
    #Check that min_average_dollar_volume is positive
    if min_avg_dollar_volume <= 0:
        raise ValueError("min_avg_dollar_volume must be positive.")
    
    #Extracting both dollar volume series
    dollar_vol_y = dollar_volume_matrix[asset_y]
    dollar_vol_x = dollar_volume_matrix[asset_x]
    
    #Combining into one DataFrame and dropping null values
    liquidity_data = pd.concat([dollar_vol_y,dollar_vol_x],axis=1).dropna()
    
    #Checking that liquidity_data has only positive values
    if (liquidity_data<0).any().any():
        raise ValueError("The dollar volume data should not be negative.")
    
    if liquidity_data.shape[0] < min_observations:
        raise ValueError("There are too few observations in the liquidity data.")
    
    #Calculating average dollar volume per asset.
    avg_dollar_volume = liquidity_data.mean()
    
    #Obtaining liquidity passed per asset, i.e., average dollar volume > min_avg_dollar_volume
    liquidity_passed = all(avg_dollar_volume >= min_avg_dollar_volume)
    
    summary_dict = {
        'asset_y':asset_y,
        'asset_x':asset_x,
        'avg_dollar_volume_y':avg_dollar_volume[asset_y],
        'avg_dollar_volume_x':avg_dollar_volume[asset_x],
        'min_avg_dollar_volume':min_avg_dollar_volume,
        'liquidity_passed':liquidity_passed,
        'num_observations':liquidity_data.shape[0],
        'method':"average_dollar_volume_filter"
    }
    
    return summary_dict

def select_top_pairs(price_matrix, dollar_volume_matrix, top_n=5, min_observations=60, min_correlation=0.7, pvalue_threshold=0.05, max_half_life=60, min_avg_dollar_volume=10_000_000, trend='c',use_log_prices=True):
    
    """
    This function converts the pair-level functions into a pairs selection pipeline.
    price_matrix + dollar_volume_matrix
    > generate all candidate pairs
    > calculate correlation, cointegration, half-life, liquidity for each pair
    > store results
    > rank pairs
    > return top N
    
    Why assumed parameters are chosen:
    top_n=5 controls how many pairs Notebook 02 will model.
    min_correlation=0.7 keeps pairs with reasonably strong return co-movement.
    pvalue_threshold=0.05 keeps cointegrated pairs.
    max_half_life=60 avoids spreads that revert too slowly.
    min_avg_dollar_volume=10_000_000 filters for tradability.
    """
    
    #Check that price matrix is a DataFrame
    if not isinstance(price_matrix, pd.DataFrame):
        raise TypeError("The price_matrix should be a pandas DataFrame.")
    
    #Check that the price matrix is not empty
    if price_matrix.empty:
        raise ValueError("The price matrix should not be empty.")
    
    #Check that dollar volume matrix is a DataFrame
    if not isinstance(dollar_volume_matrix, pd.DataFrame):
        raise TypeError("The dollar_volume_matrix should be a pandas DataFrame.")
    
    #Check that the dollar volume matrix is not empty
    if dollar_volume_matrix.empty:
        raise ValueError("The dollar_volume_matrix should not be empty.")  
    
    #Price and dollar volume matrices have the same columns
    if not price_matrix.columns.equals(dollar_volume_matrix.columns):
        raise ValueError("The price and dollar volume matrices should have the same columns.")
    
    #Price and dollar volume matrices have the same columns
    if not price_matrix.index.equals(dollar_volume_matrix.index):
        raise ValueError("The price and dollar volume matrices should have the same index.")
    
    #top_n is an integer
    if not isinstance(top_n, int):
        raise TypeError("top_n should be an integer.")
    
    #top_n is positive
    if top_n <= 0:
        raise ValueError("top_n should be positive.")
    
    #min_observations is an integer
    if not isinstance(min_observations, int):
        raise TypeError("min_observations should be an integer.")
    
    #min_observations is positive
    if min_observations <= 0:
        raise ValueError("min_observations should be positive.")
    
    #min_correlation is numeric
    if not isinstance(min_correlation, (int,float,np.number)):
        raise TypeError("min_correlation should be numeric.")
    
    #min_correlation is between -1 and 1
    if abs(min_correlation) > 1:
        raise ValueError("min_correlation must be between -1 and 1.")
    
    #pvalue_threshold is numeric
    if not isinstance(pvalue_threshold, (int,float,np.number)):
        raise TypeError("pvalue_threshold should be numeric.")
    
    #pvalue_threshold is between 0 and 1
    if pvalue_threshold > 1 or pvalue_threshold < 0:
        raise ValueError("pvalue_threshold must be between 0 and 1.")
    
    #max_half_life is numeric
    if not isinstance(max_half_life, (int,float,np.number)):
        raise TypeError("max_half_life should be numeric.")
    
    #max_half_life is positive
    if max_half_life <= 0:
        raise ValueError("max_half_life should be positive.")
    
    #min_avg_dollar_volume is numeric
    if not isinstance(min_avg_dollar_volume, (int,float,np.number)):
        raise TypeError("min_avg_dollar_volume should be numeric.")
    
    #min_avg_dollar_volume is positive
    if min_avg_dollar_volume <= 0:
        raise ValueError("min_avg_dollar_volume should be positive.")
    
    #Obtaining candidate pairs and preparing pair results
    candidate_pairs = generate_candidate_pairs(price_matrix)
    pairs_results = []
    log_price_matrix = compute_log_prices(price_matrix)
    
    #Evaluating the candidate pairs by iterating through a loop
    for asset_y, asset_x in candidate_pairs:
        
        correlation_result = compute_pair_correlation(price_matrix, asset_y,asset_x,min_observations=min_observations)
        cointegration_result = run_cointegration_test(price_matrix,asset_y,asset_x,min_observations=min_observations,pvalue_threshold=pvalue_threshold,trend=trend,use_log_prices=use_log_prices)
        liquidity_result = compute_liquidity_metrics(dollar_volume_matrix, asset_y, asset_x, min_observations=min_observations,min_avg_dollar_volume =min_avg_dollar_volume)
        
        hedge_model = estimate_hedge_model(log_price_matrix, asset_y, asset_x)
        spread = compute_spread(log_price_matrix, hedge_model)
        half_life_result = estimate_half_life(spread, min_observations)
        
        pair_result = {
            "asset_y": asset_y,
            "asset_x": asset_x,
            "correlation": correlation_result["correlation"],
            "cointegration_pvalue": cointegration_result["cointegration_pvalue"],
            "cointegration_passed": cointegration_result["cointegration_passed"],
            "half_life": half_life_result["half_life"],
            "liquidity_passed": liquidity_result["liquidity_passed"],
            "avg_dollar_volume_y": liquidity_result["avg_dollar_volume_y"],
            "avg_dollar_volume_x": liquidity_result["avg_dollar_volume_x"]
        }
        pairs_results.append(pair_result)
    
    pairs_result_df = pd.DataFrame(pairs_results)
    
    #Checking if pairs_result_df is empty
    if pairs_result_df.empty:
        raise ValueError("pairs_result_df should be populated.")
    
    #Filtering pairs_result_df
    #Here we are counting only pairs with positive correlation and not pairs where 1 asset offsets the other.
    condition_1 = pairs_result_df["correlation"] >= min_correlation
    condition_2 = pairs_result_df["cointegration_passed"] == True
    condition_3 = pairs_result_df["half_life"] <= max_half_life
    condition_4 = pairs_result_df["liquidity_passed"] == True
    
    #success_pairs_df = pairs_result_df
    success_pairs_df = pairs_result_df[condition_1 & condition_2 & condition_3 & condition_4].reset_index(drop=True)
    
    #check if success_pairs_df is empty
    if success_pairs_df.empty:
        raise ValueError("The conditions are too restrictive.")
    
    #Sorting success_pairs_df on the basis on cointegration, correlation and half_life
    ranked_pairs_df = success_pairs_df.sort_values(by = ["cointegration_pvalue","correlation","half_life"],ascending=[True,False,True]).reset_index(drop=True)
    ranked_pairs_df["rank"] = ranked_pairs_df.index+1
    
    #Return the top_n pairs
    return ranked_pairs_df.head(top_n)