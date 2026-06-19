""" 
This file will be used to validate the universe and run config files that are 
present in the json file format. The universe files are v1_universe.json and a 
possible v2_universe.json for versions 1 and 2 of the options platform project 
respectively.

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
    
    #Check if data is a non-empty dictionary
    if not isinstance(data, dict):
        raise TypeError("data should be a dictionary.")
    
    if len(data) == 0:
        raise ValueError("data should not be empty.")
    
    #Check if tickers exist in data
    if not "tickers" in data:
        raise ValueError("tickers should exist in data.")
    
    tickers = data["tickers"]
    
    #Check if tickers is a list of strings
    if not isinstance(tickers, list):
        raise TypeError("tickers should be a list.")
    
    if len(tickers) == 0:
        raise ValueError("tickers should not be empty.")
    
    if any(not isinstance(ticker, str) for ticker in tickers):
        raise TypeError("tickers should contain strings only.")
    
    if any(ticker.strip()=="" for ticker in tickers):
        raise ValueError("tickers cannot have empty strings as tickers.")
    
    tickers = [ticker.upper().strip() for ticker in tickers]
    
    if len(tickers) != len(set(tickers)):
        raise ValueError("tickers cannot contain duplicate values.")
    
    data["tickers"] = tickers
    
    return data