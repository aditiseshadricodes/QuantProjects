""" 
Reasons for choosing the lower volatility bound, upper volatility bound,
price_tolerance, volatility_tolerance and  max_iterations:
- lower_volatility_bound: 1e-6 is low enough to avoid passing 0 as a lower bound.
This is because d1 and d2 divide by volatility*sqrt(time_to_expiry)
- upper_volatility_bound: 5.0 is 500% annualized volatility. This is a broad range
that brackets most ordinary cases. A valid theoretical market price can still 
fail to bracket within 5.0; that means the search interval is insufficient, 
not necessarily that the market price violates no-arbitrage bounds.
Automatic expansion can be planned as an improvement.
- max_iterations: Bisection halves the interval every iteration.
Starting with a width close to 5.0, reaching an interval width around 1e-8 
requires only about 29 halvings. So 100 is generous while still bounded.
- price_tolerance: This gives highly accurate synthetic recovery tests.
Real market quotes are much noisier because of bid–ask spreads and tick sizes, 
but keeping numerical error small is still reasonable.
- volatility_tolerance: Stop when the remaining half-width of the volatility bracket 
is at most 1e-8. That means the numerical uncertainty in the returned decimal 
volatility is extremely small.
"""

import pytest
from src.option_pricing import(
    black_scholes_price,
)
from src.implied_vol import(
    implied_vol_bisection,
)

def test_implied_vol_call_option_valid_input():
    
    known_volatility =  0.20
    
    bsm_price = black_scholes_price(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        volatility=0.20, #Fixed Value to get market price
        option_type="call",
        dividend_yield=0.0,
    )
    
    implied_vol = implied_vol_bisection(
        bsm_price,
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        dividend_yield=0.0,
        option_type="call",
        volatility_lower_bound=1e-6,
        volatility_upper_bound=5.0,
        price_tolerance=1e-8,
        volatility_tolerance=1e-8,
        max_iterations=100
    )
    
    assert implied_vol == pytest.approx(known_volatility, rel=1e-6)

def test_implied_vol_put_option_valid_input():
    
    known_volatility =  0.20
    
    bsm_price = black_scholes_price(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        volatility=0.20, #Fixed Value to get market price
        option_type="put",
        dividend_yield=0.0,
    )
    
    implied_vol = implied_vol_bisection(
        bsm_price,
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        dividend_yield=0.0,
        option_type="put",
        volatility_lower_bound=1e-6,
        volatility_upper_bound=5.0,
        price_tolerance=1e-8,
        volatility_tolerance=1e-8,
        max_iterations=100
    )
    
    assert implied_vol == pytest.approx(known_volatility, rel=1e-6)
    
def test_implied_vol_call_option_price_lower_bound_failure():
    
    with pytest.raises(ValueError):
        implied_vol_bisection(
            market_price=1.0,
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.02,
            dividend_yield=0.0,
            option_type="call",
            volatility_lower_bound=1e-6,
            volatility_upper_bound=5.0,
            price_tolerance=1e-8,
            volatility_tolerance=1e-8,
            max_iterations=100
        )

def test_implied_vol_call_option_price_upper_bound_failure():
        
    with pytest.raises(ValueError):
        implied_vol_bisection(
            market_price=100.0,
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.02,
            dividend_yield=0.0,
            option_type="call",
            volatility_lower_bound=1e-6,
            volatility_upper_bound=5.0,
            price_tolerance=1e-8,
            volatility_tolerance=1e-8,
            max_iterations=100
        )

def test_implied_vol_put_option_price_lower_bound_failure():
        
    with pytest.raises(ValueError):
        implied_vol_bisection(
            market_price=1.0,
            spot_price=80.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.02,
            dividend_yield=0.0,
            option_type="put",
            volatility_lower_bound=1e-6,
            volatility_upper_bound=5.0,
            price_tolerance=1e-8,
            volatility_tolerance=1e-8,
            max_iterations=100
        )
        
def test_implied_vol_put_option_price_upper_bound_failure():
        
    with pytest.raises(ValueError):
        implied_vol_bisection(
            market_price=100.0,
            spot_price=80.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.02,
            dividend_yield=0.0,
            option_type="put",
            volatility_lower_bound=1e-6,
            volatility_upper_bound=5.0,
            price_tolerance=1e-8,
            volatility_tolerance=1e-8,
            max_iterations=100
        )
        
def test_implied_vol_call_option_valid_price_out_of_bounds():
    
    known_volatility =  0.20
    
    bsm_price = black_scholes_price(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        volatility=0.20, #Fixed Value to get market price
        option_type="call",
        dividend_yield=0.0,
    )
    
    with pytest.raises(ValueError):
        implied_vol_bisection(
            bsm_price,
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.02,
            dividend_yield=0.0,
            option_type="call",
            volatility_lower_bound=1e-6,
            volatility_upper_bound=0.10,
            price_tolerance=1e-8,
            volatility_tolerance=1e-8,
            max_iterations=100
        )

def test_implied_vol_call_option_lower_bound_output():
    
    known_volatility =  0.10
    
    bsm_price = black_scholes_price(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        volatility=0.10, #Fixed Value to get market price
        option_type="call",
        dividend_yield=0.0,
    )
    
    implied_vol = implied_vol_bisection(
        bsm_price,
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        dividend_yield=0.0,
        option_type="call",
        volatility_lower_bound=0.1,
        volatility_upper_bound=5.0,
        price_tolerance=1e-8,
        volatility_tolerance=1e-8,
        max_iterations=100
    )
    
    assert implied_vol == pytest.approx(known_volatility, rel=1e-6)

def test_implied_vol_call_option_upper_bound_output():
    
    known_volatility =  1.0
    
    bsm_price = black_scholes_price(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        volatility=1.0, #Fixed Value to get market price
        option_type="call",
        dividend_yield=0.0,
    )
    
    implied_vol = implied_vol_bisection(
        bsm_price,
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        dividend_yield=0.0,
        option_type="call",
        volatility_lower_bound=1e-6,
        volatility_upper_bound=1.0,
        price_tolerance=1e-8,
        volatility_tolerance=1e-8,
        max_iterations=100
    )
    
    assert implied_vol == pytest.approx(known_volatility, rel=1e-6)

def test_implied_vol_call_option_lower_bound_output():
        
    bsm_price = black_scholes_price(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        volatility=0.23, #Fixed Value to get market price
        option_type="call",
        dividend_yield=0.0,
    )
    
    with pytest.raises(RuntimeError):
        implied_vol_bisection(
            bsm_price,
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.02,
            dividend_yield=0.0,
            option_type="call",
            volatility_lower_bound=0.1,
            volatility_upper_bound=5.0,
            price_tolerance=1e-8,
            volatility_tolerance=1e-8,
            max_iterations=1
        )

@pytest.mark.parametrize(
    ("lower_volatility_bound","upper_volatility_bound"),
    [
        (0.20,0.20),
        (0.30,0.20),
    ]
)
def test_implied_vol_rejects_invalid_volatility_bounds_relationship(
    lower_volatility_bound,
    upper_volatility_bound
):
    
    bsm_price = black_scholes_price(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        volatility=0.23, #Fixed Value to get market price
        option_type="call",
        dividend_yield=0.0,
    )
    
    with pytest.raises(ValueError):
        implied_vol_bisection(
            bsm_price,
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.02,
            dividend_yield=0.0,
            option_type="call",
            volatility_lower_bound=lower_volatility_bound,
            volatility_upper_bound=upper_volatility_bound,
            price_tolerance=1e-8,
            volatility_tolerance=1e-8,
            max_iterations=100
        )

@pytest.mark.parametrize(
    "max_iterations",
    [1.5,None,[1],True,False,"1"],
)
def test_implied_vol_non_integer_max_iterations(
    max_iterations
):
    
    bsm_price = black_scholes_price(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        volatility=0.23, #Fixed Value to get market price
        option_type="call",
        dividend_yield=0.0,
    )
    
    with pytest.raises(TypeError):
        implied_vol_bisection(
            bsm_price,
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.02,
            dividend_yield=0.0,
            option_type="call",
            volatility_lower_bound=1e-6,
            volatility_upper_bound=5.0,
            price_tolerance=1e-8,
            volatility_tolerance=1e-8,
            max_iterations=max_iterations
        )

@pytest.mark.parametrize(
    "max_iterations",
    [0,-1],
)
def test_implied_vol_non_positive_max_iterations(
    max_iterations
):
    
    bsm_price = black_scholes_price(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        volatility=0.23, #Fixed Value to get market price
        option_type="call",
        dividend_yield=0.0,
    )
    
    with pytest.raises(ValueError):
        implied_vol_bisection(
            bsm_price,
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.02,
            dividend_yield=0.0,
            option_type="call",
            volatility_lower_bound=1e-6,
            volatility_upper_bound=5.0,
            price_tolerance=1e-8,
            volatility_tolerance=1e-8,
            max_iterations=max_iterations
        )
        
