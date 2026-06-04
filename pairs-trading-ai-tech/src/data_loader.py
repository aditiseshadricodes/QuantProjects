from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import os
import time
import pandas as pd
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

@dataclass
class TiingoConfig:
    api_key:str
    base_url:str = "https://api.tiingo.com/tiingo/daily"
    request_pause_seconds:float = 1.2
    
def load_tiingo_config() -> TiingoConfig:
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.getenv("TIINGO_API_KEY")
    
    if not api_key:
        raise ValueError("TIINGO_API_KEY not found in environment variables.")
    
def cache_path(ticker:str,start_date:str,end_date:str) -> Path:
    RAW_DATA_DIR.mkdir(parents=True,exist_ok=True)
    return RAW_DATA_DIR / f"{ticker}_{start_date}_{end_date}.csv"

def fetch_tiingo_prices(ticker:str,start_date:str,end_date:str,config:TiingoConfig | None=None,force_refresh:bool = False,use_cache:bool=True) -> pd.DataFrame:
    if config is None:
        config=load_tiingo_config()
    cache_file = cache_path(ticker,start_date,end_date)
    
    if use_cache and cache_file.exists() and not force_refresh:
        df=pd.read_csv(cache_file,parse_dates=["date"])
        df["date"]=pd.to_datetime(df["date"]).dt.tz_localize(None)
        
    url=f"{config.base_url}/ticker/prices"
    
    headers={"Content-Type": "application/json", "Authorization":f"Token {config.api_key}"} 
    params={"tickers":ticker,"startDate":start_date,"endDate":end_date,"format":"json"}
    
    response=requests.get(url,headers=headers,params=params,timeout=30) 
    response.raise_for_status()
    data=response.json()
    
    if not data:
        raise ValueError(f"No data returned for {ticker}.")
    
    df=pd.DataFrame(data)
    df["date"]=pd.to_datetime(df["date"]).dt.tz_localize(None)
    df=df.sort_values("date").set_index("date")
    
    if use_cache:
        df.reset_index().to_csv(cache_file,index=False)
        
    time.sleep(config.request_pause_seconds)
    return df

def fetch_adjusted_close_series(ticker:str,start_date:str,end_date:str,config: TiingoConfig |None=None,force_refresh:bool=False,use_cache:bool=True) -> pd.Series:
    df=fetch_tiingo_prices(ticker,start_date,end_date,config,force_refresh,use_cache)
    series=df["adjClose"].copy()
    series.name=ticker
    return series

def fetch_price_matrix(tickers:Iterable[str],start_date:str,end_date: str,config: TiingoConfig|None=None, force_refresh:bool=False, use_cache:bool=True) -> pd.DataFrame:
    if config is None:
        config=load_tiingo_config()
        
    series_list=[]
    for ticker in tickers:
        s = fetch_adjusted_close_series(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            config=config,
            force_refresh=force_refresh,
            use_cache=use_cache,
        )
        series_list.append(s)
        
        return pd.concat(series_list,axis=1).sort_index()