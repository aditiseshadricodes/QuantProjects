""" 
option_pricing.py

Black-Scholes-Merton pricing utilities for vanilla European-style options.

This module provides:
1. Scalar Black-Scholes pricing for individual call/put options.
2. Helper functions for input validation, time-to-expiry calculation, and option type normalization.
3. A DataFrame-level wrapper to price a validated option chain.

Assumptions:
- Spot price, strike, and option prices are positive floats.
- Time to expiry is expressed in years.
- Risk-free rate, dividend yield, and volatility are annualized decimals.
- Volatility is expected as a decimal, e.g. 0.25 for 25%.
- Options are treated as European-style vanilla options for V1.
- American exercise effects, early exercise, discrete dividends, and transaction costs are out of scope for V1.

Main public functions:
- intrinsic_value()
- black_scholes_price()
- price_option_chain()
"""

import math
import logging
from numbers import Real

from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)

# =========================
# Private Functions
# =========================

def _standardize_option_type(
    option_type: str
) -> str:
    """ 
    Normalize option type input to either 'call' or 'put'.

    Parameters
    ----------
    option_type : str
        Option type label. Accepted values include 'call', 'put', 'c', 'p'.

    Returns
    -------
    str
        Normalized option type: 'call' or 'put'.

    Raises
    ------
    TypeError
        If option_type is not a string.
    ValueError
        If option_type is not recognized.
    """
    if not isinstance(option_type,str):
        raise TypeError(f"Option type must be a string, got {type(option_type)}")
    
    option_type = option_type.strip().lower()
    if option_type in ['call', 'c']:
        return 'call'
    elif option_type in ['put', 'p']:
        return 'put'
    else:
        raise ValueError(f"Unrecognized option type: {option_type}")

def _option_sign(
    option_type: str
) -> int:
    """ 
    Returns the sign multiplier for option type: +1 for call, -1 for put.
    
    Parameters
    ----------
    option_type : str
        Normalized option type: 'call' or 'put'.
    
    Results
    -----------
    sign: int
        +1 if option type is call, -1 if option type is put.
    
    """
    option_type = _standardize_option_type(option_type)
    sign = 1 if option_type == 'call' else -1
    return sign

def _validate_finite_float(
    value,
name: str) -> float:
    """ 
    Validate that a value is a finite real scalar and return it as float.
    
    Parameters
    ----------
    value : any
        Input value to validate.
    name : str
        Name of the parameter for error messages.
    
    Returns
    -------
    float
        The validated float value.
    
    Raises
    ------
    TypeError
        If value is not a float or int.
    ValueError
        If value is not finite (NaN or infinite).
    """
    if isinstance(value,bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a numeric type (int or float), got {type(value)}")
    
    value = float(value)
    
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number, got {value}")
    
    return value

def _validate_positive_float(
    value,
    name: str
) -> float:
    """ 
    Validate that value is a positive finite scalar and return it as float.
    
    Parameters
    ----------
    value : any
        Input value to validate.
    name : str
        Name of the parameter for error messages.

    Returns
    -------
    float
        The validated float value.

    Raises
    ------
    TypeError
        If value is not a float or int.
    ValueError
        If value is not finite or not positive.
    """
    value = _validate_finite_float(value,name)
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value

def _validate_non_negative_float(
    value,
    name: str
) -> float:
    """ 
    Validate that value is a non-negative finite scalar and return it as float.
    
    Parameters
    ----------
    value : any
        Input value to validate.
    name : str
        Name of the parameter for error messages.

    Returns
    -------
    float
        The validated float value.

    Raises
    ------
    TypeError
        If value is not a float or int.
    ValueError
        If value is not finite or is negative.
    """
    value = _validate_finite_float(value,name)
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")
    return value

def _norm_cdf(
    x: float
) -> float:
    """ 
    Return the cumulative distribution function value for a standard
    normal variable.
    
    Parameters
    -------------
    x : float
        Input value.
    
    Returns
    -------------
    Standard normal CDF value between 0 and 1.
    
    Raises
    -------------
    TypeError
        If x is not a numeric type(int or float).
    ValueError
        If x is not finite.
    """
    x = _validate_finite_float(x,"x")
    
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def _validate_scalar_pricing_inputs(
    spot_price,
    strike_price,
    time_to_expiry,
    risk_free_rate,
    volatility,
    option_type,
    dividend_yield=0.0
):
    """ 
    Validate scalar Black-Scholes pricing inputs.

    Parameters
    ----------
    S : float
        Spot price of the underlying.
    K : float
        Strike price.
    T : float
        Time to expiry in years.
    r : float
        Annualized continuously compounded risk-free rate.
    sigma : float
        Annualized volatility as a decimal.
    option_type : str
        Option type: call/put.
    q : float, default 0.0
        Annualized continuous dividend yield.

    Returns
    -------
    all input parameters.

    Raises
    ------
    TypeError
        If numeric inputs are not numeric.
    ValueError
        If inputs violate pricing constraints.
    """
    spot_price = _validate_positive_float(spot_price,"spot")
    strike_price = _validate_positive_float(strike_price,"strike")
    time_to_expiry = _validate_non_negative_float(time_to_expiry,"time_to_expiry")
    risk_free_rate = _validate_finite_float(risk_free_rate,"risk_free_rate")
    volatility = _validate_positive_float(volatility,"volatility")
    dividend_yield = _validate_non_negative_float(dividend_yield,"dividend_yield")
    option_type = _standardize_option_type(option_type)
    
    return (
        spot_price,
        strike_price, 
        time_to_expiry, 
        risk_free_rate,
        volatility, 
        option_type,
        dividend_yield
    )

def _d1d2(
    spot_price,
    strike_price,
    time_to_expiry,
    risk_free_rate,
    volatility,
    dividend_yield=0.0
):
    """ 
    Calculate the Black-Scholes d1 and d2 terms.
    The d1 and d2 terms are intermediate quantities used in the
    Black-Scholes-Merton pricing formula for European call and put options.
    This helper assumes strictly positive time to expiry because d1 and d2
    divide by sqrt(time_to_expiry).

    Parameters
    ----------
    spot_price : float
        Current price of the underlying asset. Must be positive and finite.
    strike_price : float
        Strike price of the option. Must be positive and finite.
    time_to_expiry : float
        Time to expiry in years. Must be strictly positive.
    risk_free_rate : float
        Annualized continuously compounded risk-free rate. Must be finite.
        Negative rates are allowed.
    volatility : float
        Annualized volatility as a decimal. Must be positive and finite.
    dividend_yield : float, default 0.0
        Annualized continuous dividend yield. Must be non-negative and finite.

    Returns
    -------
    tuple[float, float]
        The d1 and d2 values used in Black-Scholes-Merton pricing.

    Raises
    ------
    TypeError
        If any numeric input is not a real numeric scalar.
    ValueError
        If spot, strike, time_to_expiry, or volatility are not positive;
        if dividend_yield is negative; or if any numeric input is not finite.
        """
    spot_price = _validate_positive_float(spot_price,"spot")
    strike_price = _validate_positive_float(strike_price,"strike")
    time_to_expiry = _validate_positive_float(time_to_expiry,"time_to_expiry")
    risk_free_rate = _validate_finite_float(risk_free_rate,"risk_free_rate")
    volatility = _validate_positive_float(volatility,"volatility")
    dividend_yield = _validate_non_negative_float(dividend_yield,"dividend_yield")
    
    #Compute square root of time to expiry and ln(moneyness)
    sqrt_t = math.sqrt(time_to_expiry)
    log_moneyness = math.log(spot_price / strike_price)
    
    #Compute d1 and d2 using the Black-Scholes-Merton formulas
    d1 = (log_moneyness + (risk_free_rate - dividend_yield + 0.5 *volatility**2) * time_to_expiry) / (volatility * sqrt_t)
    d2 = d1 - volatility * sqrt_t
    
    return d1, d2

def _time_to_expiry(
    valuation_date,
    expiry_date
) -> float:
    """ 
    Compute a time to expiry in years using a simple calendar-day convention.
    
    Parameters
    ----------
    valuation_date:str, datetime-like or pandas.Timestamp 
        Date on which the option is valued.
    expiry_date:str, datetime-like or pandas.Timestamp 
        Option expiry date.
    
    Returns
    -------
    float
        Time to expiry in years. 
        computed as calendar days / 365.0
    
    Raises
    ------
    ValueError
        If expiry_date is before valuation_date or if dates can't be parsed.
    
    Notes
    -----
    V1 uses calendar days and a 365-day year. It does not use trading-day calendars,
    holiday calendars, intraday expiry times, or timezone logic.
    """
    try:
        valuation_ts = pd.Timestamp(valuation_date).normalize()
        expiry_ts = pd.Timestamp(expiry_date).normalize()
    except Exception as e:
        raise ValueError("valuation_date and expiry_date must be parseable.") from e
    
    if pd.isna(valuation_ts) or pd.isna(expiry_ts):
        raise ValueError("valuation_date and expiry_date must be valid dates.")
    
    if expiry_ts < valuation_ts:
        raise ValueError("expiry_date cannot be before valuation_date.")
    
    calendar_days = (expiry_ts - valuation_ts).days
    return calendar_days/365.0

def _get_spot_price(
    spot_price
) -> float:
    """ 
    Fetches the clean, positive spot price from the given spot input.
    
    Parameters
    ----------
    input spot value provided.
    
    Returns
    -------
    float
        Positive numeric spot price.
    
    Raises
    ------
    TypeError
        If the input spot is not numeric.
    ValueError
        If spot is infinite or not positive.
    """
    spot_price = _validate_positive_float(spot_price,"spot")
    return spot_price

def _price_option_row(
    row,
    valuation_date,
    spot_price,
    risk_free_rate,
    dividend_yield=0.0,
    
volatility_col = "implied_volatility",
):
    """ 
    Price a single option-chain row using the Black-Scholes model.

    The row is expected to represent one option contract. Contract-specific
    fields, such as strike, expiry date, option type, and volatility, are read
    from the row. Pricing-run inputs, such as valuation date, spot price,
    risk-free rate, and dividend yield, are supplied separately.

    Time to expiry is computed internally using:

        T = _time_to_expiry(valuation_date, row["expiry_date"])

    Parameters
    ----------
    row : pandas.Series or mapping
        One option contract row. Must contain ``strike``, ``expiry_date``,
        ``option_type``, and the selected volatility column.
    valuation_date : str, datetime-like, or pandas.Timestamp
        Date on which the option is valued. Used with the row-level expiry
        date to compute Black-Scholes time to expiry.
    spot_price : float
        Current underlying spot price for the option chain.
    risk_free_rate : float
        Annualized continuously compounded risk-free rate, in decimal form.
    dividend_yield : float, default 0.0
        Annualized continuous dividend yield, in decimal form.
    volatility_col : str, default "implied_volatility"
        Name of the row column containing annualized volatility, in decimal
        form.

    Returns
    -------
    float
        Black-Scholes model price for the option row.

    Raises
    ------
    KeyError
        If the row is missing a required option-pricing field.
    TypeError
        If scalar inputs have invalid types.
    ValueError
        If scalar inputs contain invalid values.
    """
    required_cols = ["strike_price","expiry_date","option_type",volatility_col]
    missing_cols = [col for col in required_cols if col not in row]
    
    if missing_cols:
        raise KeyError(f"Missing required option row columns: {missing_cols}")
    
    spot_price = _get_spot_price(spot_price)
    
    time_to_expiry = _time_to_expiry(
        valuation_date=valuation_date,
        expiry_date=row["expiry_date"],
    )
    
    return black_scholes_price(
        spot_price=spot_price,
        strike_price=row["strike_price"],
        time_to_expiry=time_to_expiry,
        risk_free_rate=risk_free_rate,
        volatility=row[volatility_col],
        option_type=row["option_type"],
        dividend_yield=dividend_yield
    )

# ==========================
# Public Functions
# ==========================

def intrinsic_value(
    spot_price,
    strike_price,
    option_type
):
    """ 
    Calculate the intrinsic value of a European call or put option.
    
    Intrinsic Value is the immediate exercise value of an option. 
    For a call option, this is max(spot-strike,0).
    For a put option, this is max(strike-spot,0).
    
    Parameters
    ----------
    spot_price : float
        Current price of the underlying asset.
    strike_price : float
        Strike price of the option.
    option_type : str
        Type of the option: 'call' or 'put'.
    
    Returns
    -------
    float
        The intrinsic value of the option.
    
    Raises
    ------
    TypeError
        If spot or strike are not numeric, or if option_type is not a string.
    ValueError
        If spot or strike are not positive or real, or if option_type is not recognized.
    """
    spot_price = _validate_positive_float(spot_price,"spot")
    strike_price = _validate_positive_float(strike_price,"strike")
    option_type = _standardize_option_type(option_type)
    sign = _option_sign(option_type)
    
    intrinsic = max(sign*(spot_price-strike_price),0)
    return intrinsic

def black_scholes_price(
    spot_price,
    strike_price,
    time_to_expiry,
    risk_free_rate,
    volatility,
    option_type,
    dividend_yield=0.0
):
    """ 
    Calculate the Black-Scholes-Merton price for a European call or put option.

    This function prices a single vanilla European-style option using scalar
    inputs. It supports continuous dividend yield and handles expiry-day pricing
    by returning intrinsic value when time_to_expiry is zero.

    Parameters
    ----------
    spot_price : float
        Current price of the underlying asset. Must be positive and finite.
    strike_price : float
        Strike price of the option. Must be positive and finite.
    time_to_expiry : float
        Time to expiry in years. Must be non-negative.
    risk_free_rate : float
        Annualized continuously compounded risk-free rate. Must be finite.
        Negative rates are allowed.
    volatility : float
        Annualized volatility as a decimal. Must be positive and finite.
    option_type : str
        Option type. Accepted values are call/c or put/p, case-insensitive.
    dividend_yield : float, default 0.0
        Annualized continuous dividend yield. Must be non-negative and finite.

    Returns
    -------
    float
        Black-Scholes-Merton theoretical option price.

    Raises
    ------
    TypeError
        If numeric inputs are not real numeric scalars, or if option_type is not a string.
    ValueError
        If spot, strike, or volatility are not positive; if time_to_expiry
        or dividend_yield are negative; if any numeric input is not finite;
        or if option_type is invalid.

    """
    #Validate option type and scalars
    spot_price = _validate_positive_float(spot_price,"spot")
    strike_price = _validate_positive_float(strike_price,"strike")
    time_to_expiry = _validate_non_negative_float(time_to_expiry,"time_to_expiry")
    risk_free_rate = _validate_finite_float(risk_free_rate,"risk_free_rate")
    volatility = _validate_positive_float(volatility,"volatility")
    dividend_yield = _validate_non_negative_float(dividend_yield,"dividend_yield")
    option_type = _standardize_option_type(option_type)
    sign = _option_sign(option_type)
    
    #If option is at expiry return intrinsic value.
    if time_to_expiry == 0:
        return intrinsic_value(spot_price,strike_price,option_type)
    
    #Calculate d1,d2 for Black-Scholes-Merton formula
    d1,d2 = _d1d2(
        spot_price,
        strike_price,
        time_to_expiry,
        risk_free_rate,
        volatility,
        dividend_yield
    )
    
    #Compute the discount factors for risk-free rate and dividend yield
    spot_dividend_discount = math.exp(-dividend_yield * time_to_expiry)
    risk_free_discount = math.exp(-risk_free_rate * time_to_expiry)
    
    #Calculate the Black-Scholes-Merton price using the formula
    price = sign * (spot_price *spot_dividend_discount * _norm_cdf(sign*d1) - strike_price * risk_free_discount * _norm_cdf(sign*d2))
    return price

def price_option_chain(
    option_chain,
    valuation_date,
    spot_price,
    risk_free_rate,
    dividend_yield=0.0,
    volatility_col="implied_volatility",
    output_col="model_price",
):
    """ 
    Price an option chain using the Black-Scholes model.

    The input DataFrame is expected to contain one row per option contract.
    Contract-specific fields are read from each row, while pricing-run inputs
    such as valuation date, spot price, risk-free rate, and dividend yield are
    supplied once and shared across the chain.

    Each row is priced by ``_price_option_row``. The returned DataFrame is a
    copy of the input with an additional model price column.

    Parameters
    ----------
    option_chain : pandas.DataFrame
        Option chain with one row per contract. Must contain ``strike``,
        ``expiry_date``, ``option_type``, and the selected volatility column.
    valuation_date : str, datetime-like, or pandas.Timestamp
        Date on which the options are valued. Used with each row's expiry date
        to compute time to expiry.
    spot_price : float
        Current underlying spot price shared by the option chain.
    risk_free_rate : float
        Annualized continuously compounded risk-free rate, in decimal form.
    dividend_yield : float, default 0.0
        Annualized continuous dividend yield, in decimal form.
    volatility_col : str, default "implied_volatility"
        Name of the column containing annualized volatility, in decimal form.
    output_col : str, default "model_price"
        Name of the output column containing Black-Scholes model prices.

    Returns
    -------
    pandas.DataFrame
        Copy of the input option chain with an added model price column.

    Raises
    ------
    TypeError
        If option_chain is not a pandas DataFrame.
    KeyError
        If required option-pricing columns are missing.
    ValueError
        If scalar pricing inputs contain invalid values.
    """
    if not isinstance(option_chain, pd.DataFrame):
        raise TypeError("option_chain must be a pandas DataFrame.")
    
    required_cols = ["strike_price","expiry_date","option_type",volatility_col]
    missing_cols = [col for col in required_cols if col not in option_chain.columns]
    
    if missing_cols:
        raise KeyError(f"{missing_cols} is not present in the DataFrame.")
    
    options = option_chain.copy()
    spot_price = _get_spot_price(spot_price)
    
    for index, row in options.iterrows():
        
        price = _price_option_row(
            row=row,
            valuation_date=valuation_date,
            spot_price=spot_price,
            risk_free_rate=risk_free_rate,
            dividend_yield=dividend_yield,
            volatility_col=volatility_col,
        )
        
        options.loc[index, output_col] = price
    
    return options