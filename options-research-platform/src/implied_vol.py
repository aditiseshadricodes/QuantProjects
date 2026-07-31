"""
Implied-volatility utilities.

This module estimates the volatility implied by an observed option market
price. The solver repeatedly evaluates the existing Black–Scholes–Merton
pricing function and searches for the volatility at which the model price
approximately matches the observed price.

Expected inputs include the market option price, spot price, strike price,
time to expiry, risk-free rate, option type, and dividend yield.

The returned implied volatility is expressed as a decimal, for example
0.20 for 20%.

TODO:
- Validate theoretical option-price bounds.
- Choose and implement a root-finding method.
- Reuse the existing Black–Scholes–Merton pricer.
- Add call and put volatility-recovery tests.
- Handle cases where no valid solution exists within the search interval.
"""

import numpy as np
import math
from functools import partial
from src.option_pricing import (
    black_scholes_price,
    _validate_positive_float,
    _standardize_option_type,
    _validate_finite_float,
    _validate_non_negative_float,
)
from src.validation import (
    _validate_positive_int,
)

def _compute_pricing_error(
    candidate_volatility,
    *,
    market_price,
    spot_price,
    strike_price,
    time_to_expiry,
    risk_free_rate,
    dividend_yield,
    option_type
):
    theoretical_price = black_scholes_price(
        spot_price=spot_price,
        strike_price=strike_price,
        time_to_expiry=time_to_expiry,
        risk_free_rate=risk_free_rate,
        dividend_yield=dividend_yield,
        volatility=candidate_volatility,
        option_type=option_type,
    )

    return theoretical_price - market_price

def implied_vol_bisection(
    market_price,
    spot_price,
    strike_price,
    time_to_expiry,
    risk_free_rate,
    dividend_yield,
    option_type,
    volatility_lower_bound,
    volatility_upper_bound,
    price_tolerance,
    volatility_tolerance,
    max_iterations
):
    
    #Validate inputs
    #This is a scalar market price, it could be midpoint of bid and ask values.
    market_price = _validate_positive_float(
        market_price,
        "market_price"
    )
    spot_price = _validate_positive_float(
        spot_price,
        "spot_price"
    )
    strike_price = _validate_positive_float(
        strike_price,
        "strike_price"
    )
    #Here time_to_expiry rejects even the 0 value.
    #At expiry, the price collapses to intrinsic value in this project.
    time_to_expiry = _validate_positive_float(
        time_to_expiry,
        "time_to_expiry"
    )
    risk_free_rate = _validate_finite_float(
        risk_free_rate,
        "risks_free_rate"
    )
    dividend_yield = _validate_non_negative_float(
        dividend_yield,
        "dividend_yield"
    )
    option_type = _standardize_option_type(
        option_type
    )
    volatility_lower_bound = _validate_positive_float(
        volatility_lower_bound,
        "volatility_lower_bound"
    )
    volatility_upper_bound = _validate_positive_float(
        volatility_upper_bound,
        "volatility_lower_bound"
    )
    price_tolerance = _validate_positive_float(
        price_tolerance,
        "price_tolerance"
    )
    volatility_tolerance = _validate_positive_float(
        volatility_tolerance,
        "volatility_tolerance"
    )
    max_iterations = _validate_positive_int(
        max_iterations,
        "max_iterations"
    )
    
    if volatility_lower_bound >= volatility_upper_bound:
        raise ValueError(
            "Lower Volatility bound cannot be greater than or equal to Upper Volatility bound"
        )
    #Calculate price bounds
    discounted_spot = spot_price * math.exp(-dividend_yield*time_to_expiry)
    discounted_strike = strike_price * math.exp(-risk_free_rate*time_to_expiry)
    
    if option_type == "call":
        lower_price_bound = max(
            discounted_spot - discounted_strike,
            0.0
        )
        
        upper_price_bound = discounted_spot
    
    elif option_type == "put":
        lower_price_bound = max(
            discounted_strike - discounted_spot,
            0.0
        )
        
        upper_price_bound = discounted_strike
        
    #Validate that the price inside the price bounds
    #The price bound variables retain scope throughout the function.
    if market_price < lower_price_bound - price_tolerance:
        raise ValueError(
            "Market price is below the theoretical lower price bound."
        )

    if market_price > upper_price_bound + price_tolerance:
        raise ValueError(
            "Market price is above the theoretical upper price bound."
        )
    
    #Obtain pricing errors for lower and upper bounds
    pricing_error = partial(
        _compute_pricing_error,
        market_price=market_price,
        spot_price=spot_price,
        strike_price=strike_price,
        time_to_expiry=time_to_expiry,
        risk_free_rate=risk_free_rate,
        dividend_yield=dividend_yield,
        option_type=option_type,
    )
    
    lower_error = pricing_error(volatility_lower_bound)
    upper_error = pricing_error(volatility_upper_bound)
    left_volatility = volatility_lower_bound
    right_volatility = volatility_upper_bound
    
    #Check if an endpoint is already the solution
    if abs(lower_error) <= price_tolerance:
        return volatility_lower_bound

    if abs(upper_error) <= price_tolerance:
        return volatility_upper_bound
    
    if lower_error * upper_error > 0:
        raise ValueError(
            "The volatility interval does not bracket an implied-volatility root."
        )
    
    #Compute bisection
    for _ in range(max_iterations):
        
        #Find the midpoint
        midpoint_volatility = (
            left_volatility + right_volatility
        ) / 2.0
        
        #Evaluate the pricing error
        midpoint_error = pricing_error(midpoint_volatility)
        
        #Check convergence
        if abs(midpoint_error) <= price_tolerance:
            return midpoint_volatility
        
        half_interval_width = (
            right_volatility - left_volatility
        ) / 2.0

        if half_interval_width <= volatility_tolerance:
            return midpoint_volatility
        
        #Retain the half containing the root
        if lower_error * midpoint_error <= 0:
            right_volatility = midpoint_volatility
            upper_error = midpoint_error
        
        else:
            left_volatility = midpoint_volatility
            lower_error = midpoint_error
    
    raise RuntimeError(
        "Implied-volatility bisection did not converge "
        "within the maximum number of iterations."
    )