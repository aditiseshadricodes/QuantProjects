from __future__ import annotations 

import numpy as np
import pandas as pd


def compute_log_spread(price_a: pd.Series, price_b: pd.Series) -> pd.Series:
    aligned = pd.concat([price_a, price_b], axis=1).dropna()
    log_a = np.log(aligned.iloc[:, 0])
    log_b = np.log(aligned.iloc[:, 1])
    spread = log_a - log_b
    spread.name = f"{price_a.name}_{price_b.name}_spread"
    return spread


def compute_zscore(spread: pd.Series, window: int = 60) -> pd.Series:
    rolling_mean = spread.rolling(window=window).mean()
    rolling_std = spread.rolling(window=window).std()
    zscore = (spread - rolling_mean) / rolling_std
    zscore.name = f"{spread.name}_zscore"
    return zscore