import json
import pytest
from src.config_loader import load_universe_config

def test_load_universe_config_valid(
    tmp_path
):
    
    data = {"tickers":["aapl","nvda","msft"]}
    path = tmp_path/"v1_universe.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    result = load_universe_config(path)
    assert result["tickers"] == ["AAPL","NVDA","MSFT"]

def test_load_universe_config_missing_key(
    tmp_path
):
    
    data = {"symbols":["aapl","msft"]}
    path = tmp_path/"v1_universe.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_universe_config(path)

def test_load_universe_config_bad_tickers(
    tmp_path
):
    
    data = {"tickers":"AAPL"}
    path = tmp_path/"v1_universe.json"
    
    with open(path,'w') as file:
        json.dump(data,file)
    
    with pytest.raises(TypeError):
        load_universe_config(path)

def test_load_universe_config_duplicate_tickers(
    tmp_path
):
    
    data = {"tickers":["AAPL","MSFT","aapl "]}
    path = tmp_path/"v1_universe.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_universe_config(path)

def test_load_universe_config_empty_tickers(
    tmp_path
):
    
    data = {"tickers":[]}
    path = tmp_path/"v1_universe.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_universe_config(path)

def test_load_universe_config_empty_str_tickers(
    tmp_path
):
    
    data = {"tickers":["AAPL","MSFT","","TSLA"]}
    path = tmp_path/"v1_universe.json"
    
    with open(path,'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_universe_config(path)

def test_load_universe_config_non_str_tickers(
    tmp_path
):
    
    data = {"tickers":["AAPL",123,"MSFT"]}
    path = tmp_path/"v1_universe.json"
    
    with open(path,'w') as file:
        json.dump(data,file)
    
    with pytest.raises(TypeError):
        load_universe_config(path)