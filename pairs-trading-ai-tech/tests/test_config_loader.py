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