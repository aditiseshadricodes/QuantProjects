"""
Portfolio construction utilities for the pairs trading framework.

This module assigns capital weights to selected pairs and combines
pair-level return streams into portfolio-level returns.

The module does not perform pair selection, signal generation, or
backtesting. It only handles portfolio weighting and return aggregation.
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)

def validate_selected_pairs(
    selected_pairs_df : pd.DataFrame,
    required_cols
) -> None:
    
    #Validate the selected_pair DataFrame.
        
    if not isinstance(selected_pairs_df, pd.DataFrame):
        raise TypeError("The selected pairs should be in a pandas DataFrame.")
    
    if selected_pairs_df.empty:
        raise ValueError("The selected pairs DataFrame should not be empty.")
    if required_cols is not None:
        required_cols = set(required_cols)
        missing_cols = required_cols - set(selected_pairs_df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

def normalize_weights(raw_scores: pd.Series, weight_name: str = "weight") -> pd.Series:
    if not isinstance(raw_scores, pd.Series):
        raise TypeError("raw_scores must be a pandas Series.")

    if raw_scores.empty:
        raise ValueError("raw_scores cannot be empty.")

    if raw_scores.isna().any():
        raise ValueError("raw_scores cannot contain null values.")

    if (raw_scores < 0).any():
        raise ValueError("raw_scores cannot contain negative values.")

    total_score = raw_scores.sum()

    if total_score <= 0:
        raise ValueError("raw_scores must sum to a positive value.")

    return pd.Series(
        raw_scores / total_score,
        index=raw_scores.index,
        name=weight_name,
    )
    
def equal_weight(
    selected_pairs_df : pd.DataFrame,
    required_cols
) -> pd.Series:
    
    validate_selected_pairs(selected_pairs_df,required_cols)
    
    n_pairs = len(selected_pairs_df)
    
    weights = pd.Series(
        1 / n_pairs,
        index = selected_pairs_df.index,
        name = "weight"
    )
    
    logger.info("Calculated equal weighted portfolio weights for %s pairs", len(selected_pairs_df))
    return weights

def rank_weight(
    selected_pairs_df : pd.DataFrame,
    rank_col: str = "rank"
):
    
    validate_selected_pairs(selected_pairs_df,None)
    
    #Validation checks for rank weighting
    
    
    if not rank_col in selected_pairs_df.columns:
        logger.error("ranked column should be present.")
        raise ValueError(f"{rank_col} should be in selected_pairs_df.")
    
    ranks = selected_pairs_df[rank_col]
    
    if ranks.isna().any():
        logger.error("ranked column should not have null values")
        raise ValueError(f"{rank_col} should not contain null values")
    
    if (ranks <= 0).any():
        logger.error("The ranks should be strictly positive integers.")
        raise ValueError("The ranks should be strictly positive integers.")
    
    logger.info("Calculating ranked weights.")
    
    score = 1/ranks.astype(float)
    
    logger.info("Calculating ranked weights for %s pairs.",len(selected_pairs_df))
    return normalize_weights(score, weight_name = "ranked_weights")

def inverse_half_life(
    selected_pairs_df: pd.DataFrame
):
    
    validate_selected_pairs(selected_pairs_df,None)
    
    #Validate required col
    if not "half_life" in selected_pairs_df.columns:
        logger.error("half-life is not present in the columns list")
        raise ValueError("half_life should be present in selected_pair_df.")
    
    logger.info("Computing inverse half-life weights.")
    
    half_life = selected_pairs_df["half_life"]
    
    if half_life.isna().any():
        logger.error("Half_life cannot have null values.")
        raise ValueError("Half_life cannot have null values.")
    
    if (half_life<=0).any():
        logger.error("Half_life must be strictly positive.")
        raise ValueError("Half_life must be strictly positive.")
    
    logger.info("Calculating inverse half life weights.")
    
    raw_score = 1 / half_life
    
    logger.info("Calculating inverse half_life weights for %s pairs.",len(selected_pairs_df))
    return normalize_weights(raw_score)

def inverse_volatility(
    selected_pairs_df: pd.DataFrame
):
    
    validate_selected_pairs(selected_pairs_df, None)
    
    if not "spread_volatility" in selected_pairs_df.columns:
        logger.error("spread_volatility is not present in the columns list")
        raise ValueError("spread_volatility must be present in selected_pair_df.")
    
    vol = selected_pairs_df["spread_volatility"]
    
    if vol.isna().any():
        logger.error("Volatility cannot have null values.")
        raise ValueError("Volatility cannot have null values.")
    
    if (vol<=0).any():
        logger.error("Volatility must be strictly positive.")
        raise ValueError("Volatility must be strictly positive.")
    
    logger.info("Calculating inverse spread_volatility weights.")
    
    inv_vol = 1 / vol
    
    logger.info("Calculating inverse spread_volatility weights for %s pairs.",len(selected_pairs_df))
    return normalize_weights(inv_vol)

def validate_portfolio_weights_by_fold(
    portfolio_weights_df: pd.DataFrame,
    fold_pair_model_artifacts: dict,
    tolerance: float = 1e-8
):
    
    required_cols = {"fold_id", "pair_key", "weight_method", "weight"}
    missing_cols = required_cols - set(portfolio_weights_df.columns)
    
    if missing_cols:
        raise ValueError(f"Missing required portfolio columns: {missing_cols}")
    
    if portfolio_weights_df.empty:
        raise ValueError("The portfolio_weights_dataframe should not be empty.")
    
    if portfolio_weights_df["weight"].isna().any():
        raise ValueError("Portfolio weights should not have any null values.")
    
    if (portfolio_weights_df["weight"] < 0).any():
        raise ValueError("Portfolio weights contain negative values.")
    
    weight_sums = (
        portfolio_weights_df
        .groupby(["fold_id","weight_method"])["weight"]
        .sum()
    )
    
    bad_sums = weight_sums[(weight_sums-1.0).abs() > tolerance]
    
    if not bad_sums.empty:
        raise ValueError(f"Portfolio weights do not sum to 1: {bad_sums.to_dict()}")
    
    for fold_id, fold_weights_df in portfolio_weights_df.groupby("fold_id"):
        if fold_id not in fold_pair_model_artifacts:
            raise ValueError(f"{fold_id} missing from fold_pair_model_artifacts.")

        model_pair_keys = set(
            fold_pair_model_artifacts[fold_id]["hedge_models_by_pair"].keys()
        )

        weight_pair_keys = set(fold_weights_df["pair_key"])

        missing_model_pairs = weight_pair_keys - model_pair_keys

        if missing_model_pairs:
            raise ValueError(
                f"{fold_id} has weights for pairs missing model artifacts: "
                f"{sorted(missing_model_pairs)}"
            )

    print("Portfolio weight validation passed.")