import pandas as pd
import numpy as np

def validation_price_matrix(prices,min_observations=756,max_missing_threshold=0.05):
    """This function performs a variety of checks on the price matrix to ensure that
        it is in the correct format, values are present, no duplications for timestamps
        and that the data is sorted by timestamp.
        
        The list of checks performed are as follows:
        
        1. Check if the price matrix is a pandas DataFrame.
        2. Check that prices matrix is not empty.
        3. The index is date-like
        4. There are at least 2 assets in the price matrix.
        5. There are no duplicated timestamps in the price matrix.
        6. There are enough observations in the price matrix to perform the analysis.
        7. The prices are positive values.
        8. Missing values are within an acceptable threshold.
        
        The expected input is:
        A pandas DataFrame with the following structure:
        rows represent dates
        columns represent assets/tickers
        values represent adjusted close prices or another positive price series
        
        Returns:
        a dictionary of validation diagnostics, such as shape, date range,
        missing-value summary, and validation status
        
        Raises:
        TypeError if the input type is invalid
        ValueError if the data fails a required validation check
    """
    validation_checks_passed=[]
    # Check if the price matrix is a pandas DataFrame
    if not isinstance(prices,pd.DataFrame):
        raise TypeError("Input price matrix must be a pandas DataFrame.")
    validation_checks_passed.append('DataFrame check passed.')
    
    #Check that prices matrix is not empty
    if prices.empty:
        raise ValueError("Input price matrix is empty.")
    validation_checks_passed.append('Non-empty check passed.')
    
    #Check if the index is date-like
    if not isinstance(prices.index, pd.DatetimeIndex):
        raise TypeError("Index of the price matrix must be a DatetimeIndex.")
    validation_checks_passed.append('datetime index check passed.')
    
    #Check for duplicate dates in the index
    if prices.index.duplicated().any():
        raise ValueError("The price matrix cannot have duplicated timestamps.")
    validation_checks_passed.append('Duplicate timestamps check passed.')
    
    #Check for minimum 2 assets in the price matrix
    if prices.shape[1] < 2:
        raise ValueError("The price matrix should contain at least 2 asset columns")
    validation_checks_passed.append('Minimum 2 assets check passed.')
    
    #Check for minimum number of observations in the price matrix. we have taken 3 years
    #of data which each year having 252 trading days, so 3*252 = 756 observations.
    if prices.shape[0] < min_observations:
        raise ValueError(f"The price matrix should contain at least {min_observations} rows of data.")
    validation_checks_passed.append('Minimum observations present check passed.')
    
    #Check for positive price values
    if(prices <=0).any().any():
        raise ValueError("The price matrix should contain only positive values.")
    validation_checks_passed.append('Positive price values check passed.')
    
    #Missing value check
    if(prices.isnull().mean() > max_missing_threshold).any():
        raise ValueError(f"The price matrix has more than {max_missing_threshold*100}% missing values in at least 1 asset.")
    validation_checks_passed.append('Missing values check passed.')
    
    #If all checks are passed
    list_of_diagnostics = {
        'is_valid':True,
        'num_observations':prices.shape[0],
        'num_assets':prices.shape[1],
        'start_date':prices.index.min(),
        'end_date':prices.index.max(),
        'missing_fraction_by_asset':prices.isnull().mean().to_dict(),
        'max_missing_threshold':max_missing_threshold,
        'min_observations_required':min_observations,
        'asset_list':list(prices.columns),
        'validation_checks_passed':validation_checks_passed
    }
    return prices, list_of_diagnostics

def validation_volume_matrix(volumes,min_observations=756,max_missing_threshold=0.05):
    """This function performs a variety of checks on the volume matrix to ensure that
        it is in the correct format, values are present, no duplications for timestamps
        and that the data is sorted by timestamp.
        
        The list of checks performed are as follows:
        
        1. Check if the volume matrix is a pandas DataFrame.
        2. Check that volumes matrix is not empty.
        3. The index is date-like
        4. There are at least 2 assets in the volume matrix.
        5. There are no duplicated timestamps in the volume matrix.
        6. There are enough observations in the price matrix to perform the analysis.
        7. The volumes are nonnegative values.
        8. Missing values are within an acceptable threshold.
        
        The expected input is:
        A pandas DataFrame with the following structure:
        rows represent dates
        columns represent assets/tickers
        values represent adjusted volumes or another positive volume series
        
        Returns:
        a dictionary of validation diagnostics, such as shape, date range,
        missing-value summary, and validation status
        
        Raises:
        TypeError if the input type is invalid
        ValueError if the data fails a required validation check
    """
    validation_checks_passed=[]
    # Check if the volume matrix is a pandas DataFrame
    if not isinstance(volumes,pd.DataFrame):
        raise TypeError("Input volume matrix must be a pandas DataFrame.")
    validation_checks_passed.append('DataFrame check passed.')
    
    #Check that prices matrix is not empty
    if volumes.empty:
        raise ValueError("Input volume matrix is empty.")
    validation_checks_passed.append('Non-empty check passed.')
    
    #Check if the index is date-like
    if not isinstance(volumes.index, pd.DatetimeIndex):
        raise TypeError("Index of the volume matrix must be a DatetimeIndex.")
    validation_checks_passed.append('datetime index check passed.')
    
    #Check for duplicate dates in the index
    if volumes.index.duplicated().any():
        raise ValueError("The volume matrix cannot have duplicated timestamps.")
    validation_checks_passed.append('Duplicate timestamps check passed.')
    
    #Check for minimum 2 assets in the volume matrix
    if volumes.shape[1] < 2:
        raise ValueError("The volume matrix should contain at least 2 asset columns")
    validation_checks_passed.append('Minimum 2 assets check passed.')
    
    #Check for minimum number of observations in the volume matrix. we have taken 3 years
    #of data which each year having 252 trading days, so 3*252 = 756 observations.
    if volumes.shape[0] < min_observations:
        raise ValueError(f"The volume matrix should contain at least {min_observations} rows of data.")
    validation_checks_passed.append('Minimum observations present check passed.')
    
    #Check for nonnegative volume values
    if(volumes <0).any().any():
        raise ValueError("The volume matrix should contain only values greater than or equal to 0.")
    validation_checks_passed.append('Nonnegative volume values check passed.')
    
    #Missing value check
    if(volumes.isnull().mean() > max_missing_threshold).any():
        raise ValueError(f"The volume matrix has more than {max_missing_threshold*100}% missing values in at least 1 asset.")
    validation_checks_passed.append('Missing values check passed.')
    
    #If all checks are passed
    list_of_diagnostics = {
        'is_valid':True,
        'num_observations':volumes.shape[0],
        'num_assets':volumes.shape[1],
        'start_date':volumes.index.min(),
        'end_date':volumes.index.max(),
        'missing_fraction_by_asset':volumes.isnull().mean().to_dict(),
        'max_missing_threshold':max_missing_threshold,
        'min_observations_required':min_observations,
        'asset_list':list(volumes.columns),
        'validation_checks_passed':validation_checks_passed
    }
    return volumes, list_of_diagnostics