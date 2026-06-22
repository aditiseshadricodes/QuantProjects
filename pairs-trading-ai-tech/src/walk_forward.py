""" 
Generate train, test and out-of-sample(OOS)datasets for walk-forward training
and testing of the pairs trading strategy.

Each fold contains:
- 3 years for training / pair  selection
- 1 year for testing
- 1 year for OOS validation.

With 7 years of total data, this produces 3 rolling fields.
"""
import logging

logger = logging.Logger(__name__)

def generate_walk_forward_folds(
    start_year = 2019,
    n_folds = 3,
    train_years = 3,
    test_years = 1,
    oos_years=1
):
    
    """ 
    Generate rolling walk-forward folds for pairs trading validation.
    
    Each fold contains:
    - train period for pair selection/model fitting
    - test period for validation
    - OOS period for final out-of-sample evaluation
    """
    
    folds = []
    
    for i in range(n_folds):
        train_start = start_year + i
        train_end = train_start + train_years -1
        test_year = train_end + 1
        oos_year = test_year + 1
        
        folds.append({
            "fold": i+1,
            "train":(f"{train_start}-01-01",f"{train_end}-12-31"),
            "test":(f"{test_year}-01-01",f"{test_year}-12-31"),
            "oos":(f"{oos_year}-01-01",f"{oos_year}-12-31")
        })
    
    return folds

def get_fold_data(
    price_matrix,
    fold
):
    
    """ 
    Slice a price matrix into train, test, and OOS datasets using a fold definition.
    
    Parameters
    ----------
    price_matrix : pd.DataFrame
        Price matrix with dates as index and tickers as columns.
    fold : dict
        Fold dictionary containing train, test, and oos date ranges.
        
    Returns
    -------
    tuple
        train_prices, test_prices, oos_prices
    """
    train_start = fold["train"][0]
    train_end = fold["train"][1]
    test_start = fold["test"][0]
    test_end = fold["test"][1]
    oos_start = fold["oos"][0]
    oos_end = fold["oos"][1]
    train_prices = price_matrix.loc[train_start:train_end]
    test_prices = price_matrix.loc[test_start:test_end]
    oos_prices = price_matrix.loc[oos_start:oos_end]
    logger.info("Train data sliced: shape=%s, start=%s, end=%s",
    train_prices.shape,
    train_prices.index.min(),
    train_prices.index.max())
    logger.info("Test data sliced: shape=%s, start=%s, end=%s",
    test_prices.shape,
    test_prices.index.min(),
    test_prices.index.max(),)
    logger.info("OOS data sliced: shape=%s, start=%s, end=%s",
    oos_prices.shape,
    oos_prices.index.min(),
    oos_prices.index.max(),)
    
    return train_prices, test_prices, oos_prices