import json
import pytest
from src.config_loader import (
    load_universe_config,
    load_run_config
)

#Universe ticker checks

#Valid case
def test_load_universe_config_valid(
    tmp_path
):
    
    data = {"tickers":["aapl","msft","nvda"]}
    path = tmp_path / "v1_universe.json"
    
    with open(path, 'w') as  file:
        json.dump(data,file)
        
    result = load_universe_config(path)
    
    assert result["tickers"] == ["AAPL","MSFT","NVDA"]

#Ticker key missing
def test_load_universe_config_missing_key(
    tmp_path
):
    
    data = {"symbols":["aapl","msft","nvda"]}
    path = tmp_path / "v1_universe.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_universe_config(path)
    
#Tickers was not a list
def test_load_universe_config_tickers_bad_type(
    tmp_path
):
    
    data = {"tickers":"AAPL"}
    path = tmp_path / "v1_universe.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(TypeError):
        load_universe_config(path)
        
#Tickers had duplicate values
def test_load_universe_config_duplicate_tickers(
    tmp_path
):
    
    data = {"tickers":["AAPL","MSFT","AAPL"]}
    path = tmp_path / "v1_universe.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_universe_config(path)

#tickers list was empty
def test_load_universe_config_empty_tickers(
    tmp_path
):
    
    data = {"tickers":[]}
    path = tmp_path/"v1_universe.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_universe_config(path)

#A ticker was an empty string
def test_load_universe_config_empty_str_tickers(
    tmp_path
):
    
    data = {"tickers":["AAPL","MSFT","","TSLA"]}
    path = tmp_path/"v1_universe.json"
    
    with open(path,'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_universe_config(path)

#a ticker given was not a string
def test_load_universe_config_non_str_tickers(
    tmp_path
):
    
    data = {"tickers":["AAPL",123,"MSFT"]}
    path = tmp_path/"v1_universe.json"
    
    with open(path,'w') as file:
        json.dump(data,file)
    
    with pytest.raises(TypeError):
        load_universe_config(path)

#Run config date check
#Valid case for start_date, end_date and pvalue_threshold
def test_load_run_config_valid_date_pvalue(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":60,
            "min_correlation":0.4,
            "pvalue_threshold":0.05,
            "min_avg_dollar_volume":10000000
        },
        "data_loader":{
            "missing_threshold":0.05
        },
        "data_files":{},
        "spread_model":{},
        "backtest":{}
    }
    path = tmp_path/"run_config.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
        
    results = load_run_config(path)
    
    assert results["date_range"]["start_date"] == "2020-01-01"
    assert results["date_range"]["end_date"] == "2024-12-31"
    assert results["pairs_selection"]["pvalue_threshold"] == 0.05
    
#Missing start_date
def test_load_run_config_missing_start_date(
    tmp_path
):
    
    data = {
        "date_range":{
            "start":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":60,
            "min_correlation":0.4,
            "pvalue_threshold":0.05,
            "min_avg_dollar_volume":10000000
        },
        "data_loader":{
            "missing_threshold":0.05
        },
        "data_files":{},
        "spread_model":{},
        "backtest":{}
    }
    path = tmp_path/"run_config.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_run_config(path)

#Missing end_date
def test_load_run_config_missing_end_date(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":60,
            "min_correlation":0.4,
            "pvalue_threshold":0.05,
            "min_avg_dollar_volume":10000000
        },
        "data_loader":{
            "missing_threshold":0.05
        },
        "data_files":{},
        "spread_model":{},
        "backtest":{}
    }
    path = tmp_path/"run_config.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_run_config(path)

#End_date less than or equal to start_date
def test_load_run_config_wrong_end_date(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2019-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":60,
            "min_correlation":0.4,
            "pvalue_threshold":0.05,
            "min_avg_dollar_volume":10000000
        },
        "data_loader":{
            "missing_threshold":0.05
        },
        "data_files":{},
        "spread_model":{},
        "backtest":{}
    }
    path = tmp_path/"run_config.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_run_config(path)

#Missing pvalue_threshold
def test_load_run_config_missing_pvalue_threshold(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":60,
            "min_correlation":0.4,
            "pvalue":0.05,
            "min_avg_dollar_volume":10000000
        },
        "data_loader":{
            "missing_threshold":0.05
        },
        "data_files":{},
        "spread_model":{},
        "backtest":{}
    }
    path = tmp_path/"run_config.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
        
    with pytest.raises(ValueError):
        load_run_config(path)
        
#Non-numeric pvalue_threshold
def test_load_run_config_non_numeric_pvalue(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":60,
            "min_correlation":0.4,
            "pvalue_threshold":"0.05",
            "min_avg_dollar_volume":10000000
        },
        "data_loader":{
            "missing_threshold":0.05
        },
        "data_files":{},
        "spread_model":{},
        "backtest":{}
    }
    path = tmp_path/"run_config.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(TypeError):
        load_run_config(path)
        
#negative_pvalue
def test_load_run_config_negative_pvalue(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":60,
            "min_correlation":0.4,
            "pvalue_threshold":-1.05,
            "min_avg_dollar_volume":10000000
        },
        "data_loader":{
            "missing_threshold":0.05
        },
        "data_files":{},
        "spread_model":{},
        "backtest":{}
    }
    path = tmp_path/"run_config.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_run_config(path)
        
#Large positive pvalue over 1
def test_load_run_config_abnormal_pvalue(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":60,
            "min_correlation":0.4,
            "pvalue_threshold":1.5,
            "min_avg_dollar_volume":10000000
        },
        "data_loader":{
            "missing_threshold":0.05
        },
        "data_files":{},
        "spread_model":{},
        "backtest":{}
    }
    path = tmp_path/"run_config.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_run_config(path)
