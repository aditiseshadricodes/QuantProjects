import json
import pytest
from src.config_loader import load_universe_config

def test_load_universe_config_valid(
    tmp_path
):
    
    data = {"tickers":["aapl","msft","nvda"]}
    path = tmp_path / "v1_universe.json"
    
    with open(path, 'w') as  file:
        json.dump(data,file)
        
    result = load_universe_config(path)
    
    assert result["tickers"] == ["AAPL","MSFT","NVDA"]
    
def test_load_universe_config_missing_key(
    tmp_path
):
    
    data = {"symbols":["aapl","msft","nvda"]}
    path = tmp_path / "v1_universe.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_universe_config(path)
    
def test_load_universe_config_tickers_bad_type(
    tmp_path
):
    
    data = {"tickers":"AAPL"}
    path = tmp_path / "v1_universe.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(TypeError):
        load_universe_config(path)
        
def test_load_universe_config_duplicate_tickers(
    tmp_path
):
    
    data = {"tickers":["AAPL","MSFT","AAPL"]}
    path = tmp_path / "v1_universe.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_universe_config(path)