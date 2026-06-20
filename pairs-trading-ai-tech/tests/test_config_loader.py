import json
import pytest
from src.config_loader import (
    load_universe_config,
    load_run_config,
    load_metrics_config
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
    assert results["pairs_selection"]["top_n"] == 5
    assert results["data_loader"]["missing_threshold"] == 0.05
    assert results["pairs_selection"]["min_avg_dollar_volume"] == 10000000
    assert results["pairs_selection"]["min_observations"] == 60
    
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

#Missing top_n 
def test_load_run_config_missing_top_n(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "n":5,
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
    
    with open(path,'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_run_config(path)
        
#Non-numeric top_n
def test_load_run_config_str_top_n(
    tmp_path
):
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":"5",
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
    
    with open(path, 'w') as f:
        json.dump(data,f)
    
    with pytest.raises(TypeError):
        load_run_config(path)

#decimal number top_n
def test_load_run_config_float_top_n(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5.0,
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
        json.dump(data, file)
    
    with pytest.raises(TypeError):
        load_run_config(path)
        
#negative integer top_n
def test_load_run_config_negative_top_n(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":-5,
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
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_run_config(path)
        
#top_n is 0
def test_load_run_config_zero_top_n(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":0,
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
        
#Missing missing_threshold
def test_load_run_config_missing_missing_threshold(
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
            "missing":0.05
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
        
#Non-numeric missing_threshold
def test_load_run_config_not_num_missing_threshold(
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
            "missing_threshold":"0.05"
        },
        "data_files":{},
        "spread_model":{},
        "backtest":{}
    }
    path = tmp_path/"run_config.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(TypeError):
        load_run_config(path)

#Negative missing_threshold
def test_load_run_config_negative_missing_threshold(
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
            "missing_threshold":-0.05
        },
        "data_files":{},
        "spread_model":{},
        "backtest":{}
    }
    path = tmp_path/"run_config.json"
    
    with open(path,'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_run_config(path)
        
#Abnormal positive missing threshold
def test_load_run_config_large_missing_threshold(
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
            "missing_threshold":0.25
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
        
#Missing min_avg_dollar_volume
def test_load_run_config_missing_min_avg_dollar_volume(
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
            "avg_dollar_volume":10000000
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
        
#Non-numeric min_avg_dollar_volume
def test_load_run_config_non_num_min_avg_dollar_volume(
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
            "min_avg_dollar_volume":"10000000"
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
        
#Negative min_avg_dollar_volume
def test_load_run_config_negative_min_avg_dollar_volume(
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
            "min_avg_dollar_volume":-10000000
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
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_run_config(path)
        
#Missing_min_observations
def test_load_run_config_missing_min_observations(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "observations":60,
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
        
#Non-numeric min_observations
def test_load_run_config_non_num_min_observations(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":"60",
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
        json.dump(data, file)
    
    with pytest.raises(TypeError):
        load_run_config(path)
        
#Decimal number as min_observations
def test_load_run_config_float_min_observations(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":60.0,
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
        json.dump(data, file)
    
    with pytest.raises(TypeError):
        load_run_config(path)
        
#Negative min_observations
def test_load_run_config_negative_min_observations(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":-60,
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
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_run_config(path)
        
#min_observations is 0
def test_load_run_config_zero_min_observations(
    tmp_path
):
    
    data = {
        "date_range":{
            "start_date":"2020-01-01",
            "end_date":"2024-12-31"
            },
        "pairs_selection":{
            "top_n":5,
            "min_observations":0,
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
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_run_config(path)
    
#Metrics config use cases
#Valid config
def test_load_metrics_config_valid_metrics(
    tmp_path
):
    
    data = {
        "periods_per_year":252,
        "risk_free_rate":0.03,
        "newey_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    results = load_metrics_config(path)
    
    assert results["periods_per_year"] == 252
    assert results["risk_free_rate"] == 0.03
    assert results["newey_west_lags"] == 5
    
#Not a dictionary
def test_load_metrics_config_not_a_dict(
    tmp_path
):
    
    data = ""
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(TypeError):
        load_metrics_config(path)
        
#empty dictionary
def test_load_metrics_config_empty_dict(
    tmp_path
):
    
    data = {}
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_metrics_config(path)
        
#periods_per_year missing
def test_load_metrics_config_missing_periods_per_year(
    tmp_path
):
    
    data = {
        "periods_in_ a_year":252,
        "risk_free_rate":0.03,
        "newey_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_metrics_config(path)
    
#non numeric periods_per_year
def test_load_metrics_config_non_num_periods_per_year(
    tmp_path
):
    
    data = {
        "periods_per_year":"252",
        "risk_free_rate":0.03,
        "newey_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path,'w') as file:
        json.dump(data,file)
    
    with pytest.raises(TypeError):
        load_metrics_config(path)

#floating point periods_per_year
def test_load_metrics_config_float_periods_per_year(
    tmp_path
):
    
    data = {
        "periods_per_year":252.0,
        "risk_free_rate":0.03,
        "newey_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(TypeError):
        load_metrics_config(path)

#Negative periods_per_year
def test_load_metrics_config_negative_periods_per_year(
    tmp_path
):
    
    data = {
        "periods_per_year":-252,
        "risk_free_rate":0.03,
        "newey_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_metrics_config(path)

#Zero periods_per_year
def test_load_metrics_config_zero_periods_per_year(
    tmp_path
):
    
    data = {
        "periods_per_year":0,
        "risk_free_rate":0.03,
        "newey_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_metrics_config(path)

#Abnormally large positive periods_per_year
def test_load_metrics_config_large_periods_per_year(
    tmp_path
):
    
    data = {
        "periods_per_year":366,
        "risk_free_rate":0.03,
        "newey_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_metrics_config(path)

#missing risk_free_rate
def test_load_metrics_config_missing_risk_free_rate(
    tmp_path
):
    
    data = {
        "periods_per_year":252,
        "risc_free_rate":0.03,
        "newey_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_metrics_config(path)

#non numeric risk_free_rate
def test_load_metrics_config_non_num_risk_free_rate(
    tmp_path
):
    
    data = {
        "periods_per_year":252,
        "risk_free_rate":"0.03",
        "newey_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
        
    with pytest.raises(TypeError):
        load_metrics_config(path)

#negative risk_free_rate
def test_load_metrics_config_negative_risk_free_rate(
    tmp_path
):
    
    data = {
        "periods_per_year":252,
        "risk_free_rate":-0.03,
        "newey_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_metrics_config(path)

#abnormal positive risk_free_rate
def test_load_metrics_config_large_risk_free_rate(
    tmp_path
):
    
    data = {
        "periods_per_year":252,
        "risk_free_rate":1.03,
        "newey_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_metrics_config(path)

#missing newey_west_lags
def test_load_metrics_config_missing_newey_west_lags(
    tmp_path
):
    
    data = {
        "periods_per_year":252,
        "risk_free_rate":0.03,
        "newy_west_lags":5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(ValueError):
        load_metrics_config(path)

#non numeric newey_west_lags
def test_load_metrics_config_non_num_newey_west_lags(
    tmp_path
):
    
    data = {
        "periods_per_year":252,
        "risk_free_rate":0.03,
        "newey_west_lags":"5"
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    with pytest.raises(TypeError):
        load_metrics_config(path)

#floating point newey_west_lags
def test_load_metrics_config_float_newey_west_lags(
    tmp_path
):
    
    data = {
        "periods_per_year":252,
        "risk_free_rate":0.03,
        "newey_west_lags":5.0
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path, 'w') as file:
        json.dump(data,file)
    
    with pytest.raises(TypeError):
        load_metrics_config(path)

#negative_newey_west_lags
def test_load_metrics_config_negative_newey_west_lags(
    tmp_path
):
    
    data = {
        "periods_per_year":252,
        "risk_free_rate":0.03,
        "newey_west_lags":-5
    }
    path = tmp_path/"v1_metrics.json"
    
    with open(path,'w') as file:
        json.dump(data, file)
    
    with pytest.raises(ValueError):
        load_metrics_config(path)