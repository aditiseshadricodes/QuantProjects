""" 
This file will be used to validate the universe and run config files that are 
present in the json file format. The universe files are v1_universe.json and 
v2_universe.json for versions 1 and 2 of the pairs trading project respectively.

The functions will take a file path as an input for the file and then use it
to obtain a python dictionary as an output. this dictionary will be validated 
before it is returned.
"""

import json

def load_universe_config(
    universe_file_path
):
    
    #Load the json file into a dictionary
    with open(universe_file_path, 'r') as file:
        data = json.load(file)
        
    #Check if data is a dictionary and is not empty
    if not isinstance(data, dict):
        raise TypeError("data should be a dictionary.")
    
    if len(data) == 0:
        raise ValueError("Data should not be empty.")
    
    #tickers exist in data
    if not "tickers" in data:
        raise ValueError("tickers should be present in data.")
    
    tickers = data["tickers"]
        
    #Check if tickers is a non-empty list containing strings without duplicates
    if not isinstance(tickers, list):
        raise TypeError("tickers should be a list.")
    
    if len(tickers) == 0:
        raise ValueError("tickers should not be empty.")
    
    if any(not isinstance(ticker,str) for ticker in tickers):
        raise TypeError("tickers should only contain strings.")
    
    if any(ticker.strip(' ')=="" for ticker in tickers):
        raise ValueError("tickers should not have empty strings.")
    
    tickers = [ticker.upper().strip() for ticker in tickers]
    
    if len(tickers) != len(set(tickers)):
        raise ValueError("tickers should not be duplicated.")
    
    data["tickers"] = tickers
    
    return data

def load_run_config(
    run_config_file_path
):
    
    with open(run_config_file_path,'r') as file:
        data = json.load(file)
        
    #Check that data is a non-empty dictionary
    if not isinstance(data, dict):
        raise TypeError("data should be a dictionary.")
    
    if len(data) == 0:
        raise ValueError("Data should not be empty.")
    
    #Key check for date_range, data loader, backtest, spread_model, saving files
    # and pair selection.
    if not "date_range" in data:
        raise ValueError("date_range should be present in data.")
    
    if not "data_loader" in data:
        raise ValueError("data_loader should be present in data.")
    
    if not "data_files" in data:
        raise ValueError("data_files should be present in data.")
    
    if not "pairs_selection" in data:
        raise ValueError("pairs_selection should be present in data.")
    
    if not "spread_model" in data:
        raise ValueError("spread_model should be present in data.")
    
    if not "backtest" in data:
        raise ValueError("backtest should be present in data.")
    
    #Extracting important values like date range, cointegration_pvalue,
    #missing_threshold, min_observations, liquidity_threshold and top_n
    
    date_range = data["date_range"]
    data_loader = data["data_loader"]
    pairs_selection = data["pairs_selection"]
    
    if not "start_date" in date_range:
        raise ValueError("start_date should be present in data.")
    
    if not "end_date" in date_range:
        raise ValueError("end_date should be present in data.")
    
    if not "pvalue_threshold" in pairs_selection:
        raise ValueError("pvalue_threshold should be present in data.")
    
    if not "top_n" in pairs_selection:
        raise ValueError("top_n should be present in data.")
    
    if not "missing_threshold" in data_loader:
        raise ValueError("missing_threshold should be present in data.")
    
    if not "min_avg_dollar_volume" in pairs_selection:
        raise ValueError("min_avg_dollar_volume should be present in data.")
    
    if not "min_observations" in pairs_selection:
        raise ValueError("min_observations should be present in data.")
    
    start_date = data["date_range"]["start_date"]
    end_date = data["date_range"]["end_date"]
    pvalue_threshold = data["pairs_selection"]["pvalue_threshold"]
    top_n = data["pairs_selection"]["top_n"]
    missing_threshold = data["data_loader"]["missing_threshold"]
    min_avg_dollar_volume = data["pairs_selection"]["min_avg_dollar_volume"]
    min_observations = data["pairs_selection"]["min_observations"]
    
    #Domain-specific Validation Checks
    if not isinstance(start_date, str):
        raise TypeError("start_date should be a string.")
    
    if not isinstance(end_date, str):
        raise TypeError("end_date should be a string.")
    
    if end_date <= start_date:
        raise ValueError("the start_date should be before the end date.")
    
    if not isinstance(pvalue_threshold, (int, float)):
        raise TypeError("pvalue_threshold should be numeric.")
    
    if pvalue_threshold < 0 or pvalue_threshold>0.1:
        raise ValueError("pvalue_threshold should be between 0 and 0.1.")
    
    if not isinstance(top_n, int):
        raise TypeError("top_n should be an integer.")
    
    if top_n <= 0:
        raise ValueError("top_n should be positive")
    
    if not isinstance(missing_threshold, (int, float)):
        raise TypeError("missing_threshold should be numeric.")
    
    if missing_threshold < 0 or missing_threshold > 0.1:
        raise ValueError("The missing value_threshold must be less than 10%.")
    
    if not isinstance(min_avg_dollar_volume, (int, float)):
        raise TypeError("min_avg_dollar_volume should be numeric.")
    
    if min_avg_dollar_volume <= 0:
        raise ValueError("The min_avg_dollar_volume must be positive.")
    
    if not isinstance(min_observations, int):
        raise TypeError("min_observations should be an integer.")
    
    if min_observations <= 0:
        raise ValueError("There should be a positive number of minimum required observations.")
    
    return data

def load_metrics_config(metrics_json_file_path):
    
    with open(metrics_json_file_path, 'r') as file:
        data = json.load(file)
        
    #Check that data is a non-empty dictionary
    if not isinstance(data, dict):
        raise TypeError("data should be a dictionary.")
    
    if len(data) == 0:
        raise ValueError("Data should not be empty.")
    
    #Check if metrics needed are present as keys.
    if not "periods_per_year" in data:
        raise ValueError("periods_per_year should be present in data.")
    
    if not "risk_free_rate" in data:
        raise ValueError("risk_free_rate should be present in data.")
    
    if not "newey_west_lags" in data:
        raise ValueError("newey_west_lags should be present in data.")
    
    periods_per_year = data["periods_per_year"]
    risk_free_rate = data["risk_free_rate"]
    newey_west_lags = data["newey_west_lags"]
    
    #Type and Value checks for metrics
    if not isinstance(periods_per_year, int):
        raise TypeError("periods_per_year should be an integer.")
    
    if not isinstance(risk_free_rate, (int, float)):
        raise TypeError("risk_free_rate should be a decimal value.")
    
    if not isinstance(newey_west_lags, int):
        raise TypeError("newey_west_lags should be an integer.")
    
    if periods_per_year <= 0 or periods_per_year>270:
        raise ValueError("periods_per_year should be between 1 and number of trading days in a year.")
    
    if risk_free_rate < 0.0 or risk_free_rate > 1.0:
        raise ValueError("risk_free_rate is a percentage value between 0 and 1.")
    
    if newey_west_lags < 0:
        raise ValueError("newey_west_lags should be a positive integer.")
    
    return data