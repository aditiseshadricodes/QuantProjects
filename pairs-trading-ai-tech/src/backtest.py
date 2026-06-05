import pandas as pd
import numpy as np
import statsmodels.api as sm
""" 
This module contains functions  for converting spread/z-scores into positions and 
backtest returns for the pairs trading strategy.
 
It does not fetch data or estimate hedge ratios. It assumes that the spread and 
z-score features have already been created using spread_model.py.
"""