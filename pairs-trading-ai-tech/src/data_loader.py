import pandas as pd
import os
import requests
from src.data_validator import validate_price_matrix

def fetch_tiingo_price_matrix(tickers,start_date,end_date,api_key=None,price_field='adjClose',validate=True):
    """
     Fetch historical adjusted close prices from Tiingo and return a clean price matrix.
     The function is intended to support the pairs trading research pipeline
     by loading price data for a list of assets over a specified date range and 
     reshaping the data into a format suitable for downstream validation and research.
     
     Expected output is a pandas DataFrame where-
     -rows represent dates
     -columns represent assets/tickers
     -values represent adjusted close prices or another positive price series
     -index should  be a pandas DatetimeIndex
     
     Inputs:
     -tickers: list of asset tickers to fetch
     -start_date: start date for historical data
     -end_date: end date for historical data
     -api_key: Tiingo API key, loaded from environment variables if not provided
     -price_field: the price field to fetch, default is 'adjClose'
     -validate: whether to perform validation on the fetched data, default is True
     
     Returns:
     -A pandas DataFrame containing the price matrix
     -validation diagnostics if validation is applied inside the loader.
     
     Raises:
     -ValueError if required inputs are missing or invalid
     -TypeError if input types are incorrect
     -RuntimeError if the Tiingo request fails
     -ValueError if the returned data is empty or cannot be converted into a price matrix
     
    """
    #API Key present check
    data_loader_checks_passed = []
    if api_key is None:
        api_key = os.getenv("TIINGO_API_KEY")
        
    if not api_key:
        raise ValueError("Tiingo API key is required. Please set it as an environment variable or pass it directly.")
    data_loader_checks_passed.append('API key check passed.')
    
    #Tickers is filled check
    if not tickers:
        raise ValueError("Tickers list cannot be empty.")
    data_loader_checks_passed.append('Tickers list check passed.')
    
    #Ticker is a list check
    if not isinstance(tickers, list): 
        raise TypeError("Tickers should be provided as a list.")
    data_loader_checks_passed.append('Tickers type check passed.')
    
    #Each item in tickers list is a string check
    if not all(isinstance(ticker,str) for ticker in tickers):
        raise TypeError("Each ticker should be a string.")   
    data_loader_checks_passed.append('Each ticker is a string check passed.')
    
    #Each ticker in tickers list is not empty string check
    for ticker in tickers:
        if ticker.strip()=="":
            raise ValueError("Tickers list cannot contain empty strings.")
    data_loader_checks_passed.append('Each ticker is not an empty string check passed.')
        
    #Startdate and enddate check
    if not start_date or not end_date:
        raise ValueError("Start date and end date are required.")
    data_loader_checks_passed.append('Start date and end date presence check passed.')
    
    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    
    except Exception as e:
        raise ValueError("Start date and end date should be convertible to pandas Timestamp.") from e
    data_loader_checks_passed.append('Start date and end date are convertible.')
    
    if start_date>=end_date:
        raise ValueError("Start date should be earlier than end date.")
    data_loader_checks_passed.append('Start date is less than end date.')
    
    #Validate is a boolean value check
    if not isinstance(validate,bool):
        raise TypeError("Validate parameter should be a boolean value.")
    data_loader_checks_passed.append('Validate parameter type check passed.')
    
    #Tiingo API request and response handling
    start_date_str=start_date.strftime('%Y-%m-%d')
    end_date_str=end_date.strftime('%Y-%m-%d')
    price_series_by_ticker = {}
    ticker_loader_diagnostics = []
    
    for ticker in tickers:
        url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices"
        params = {
            'startDate': start_date_str,
            'endDate': end_date_str,
            'token': api_key
        }
        ticker_diagnostics={"ticker":ticker}
        try:
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()
        except requests.HTTPError as exc:
            raise RuntimeError(f"HTTP error occurred while fetching data for {ticker} from Tiingo: {exc}") from exc
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"Failed to fetch data for {ticker} from Tiingo: {exc}") from exc
        ticker_diagnostics['tiingo_request_successful']=True
        
        ticker_df = pd.DataFrame(data)
        if ticker_df.empty:
            raise ValueError(f"No data returned for ticker {ticker} from Tiingo.")
        ticker_diagnostics['data_not_empty']=True
        
        if "date" not in ticker_df.columns:
            raise ValueError(f"Expected 'date' column not found in data for ticker {ticker} from Tiingo.")
        ticker_diagnostics['date_column_present']=True
        
        if price_field not in ticker_df.columns:
            raise ValueError(f"Expected price field '{price_field}' not found in data for ticker {ticker} from Tiingo.")
        ticker_diagnostics['price_field_present']=True
        
        try:
            ticker_df['date'] = pd.to_datetime(ticker_df['date'])
        except Exception as e:
            raise ValueError(f"Failed to convert 'date' column to datetime for ticker {ticker} from Tiingo.") from e
        ticker_diagnostics['date_column_converted']=True
        price_series_by_ticker[ticker] = ticker_df.set_index('date')[price_field]
        ticker_diagnostics['price_series_extracted']=True
        ticker_diagnostics['num_observations']=len(price_series_by_ticker[ticker])
        ticker_loader_diagnostics.append(ticker_diagnostics)
        
    price_matrix = pd.DataFrame(price_series_by_ticker)
    price_matrix.sort_index(inplace=True)
    
    data_loader_checks_passed.append("Price matrix created.")
    data_loader_checks_passed.append("Price matrix sorted by date.")
    
    if validate:
        price_matrix,validation_diagnostics = validate_price_matrix(price_matrix)
        data_loader_checks_passed.append('Price matrix validation applied.')
    else:
        data_loader_checks_passed.append('Price matrix validation skipped.')
        validation_diagnostics = None
    
    complete_diagnostics = {
        "data_source": "Tiingo",
        "tickers_requested": tickers,
        "start_date": start_date_str,
        "end_date": end_date_str,
        "price_field": price_field,
        'data_loader_checks_passed': data_loader_checks_passed,
        'ticker_loader_diagnostics': ticker_loader_diagnostics,
        'matrix_summary':{
            'num_observations': price_matrix.shape[0],
            'num_assets': price_matrix.shape[1],
            'start_date': price_matrix.index.min(),
            'end_date': price_matrix.index.max(),
            'asset_list' : list(price_matrix.columns)
            },
        'validation_was_run':validate,
        'validation_diagnostics': validation_diagnostics
    }
        
    return price_matrix, complete_diagnostics        
        