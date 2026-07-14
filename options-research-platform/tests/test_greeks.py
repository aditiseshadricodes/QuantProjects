import pytest

from src.greeks import (
    _norm_pdf,
    black_scholes_delta,
    black_scholes_gamma,
    black_scholes_vega,
)

SPOT=100.0
STRIKE=100.0
TIME_TO_EXPIRY = 1.0
RISK_FREE_RATE = 0.05
VOLATILITY = 0.20
DIVIDEND_YIELD = 0.0

#Normal probability density at 0.0
def test_norm_pdf_at_zero():
    
    assert _norm_pdf(0.0) == pytest.approx(0.398942280, rel=1e-8)

#Is normal probability density symmetric.
def test_norm_pdf_is_symmetric():
    
    assert _norm_pdf(1.25) == pytest.approx(_norm_pdf(-1.25), rel=1e-12)

#Calculating delta for call option.
def test_black_scholes_delta_call_benchmark():
    delta = black_scholes_delta(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="call",
        dividend_yield=DIVIDEND_YIELD,
    )
    
    assert delta == pytest.approx(0.6368, rel=1e-4)

#Calculating delta for put option
def test_black_scholes_delta_put_benchmark():
    delta = black_scholes_delta(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="put",
        dividend_yield=DIVIDEND_YIELD,
    )
    
    assert delta == pytest.approx(-0.3632, rel=1e-4)

#Is delta for call option positive?
def test_black_scholes_delta_call_is_positive():
    delta = black_scholes_delta(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="call",
        dividend_yield=DIVIDEND_YIELD,
    )
    
    assert delta > 0

#Is delta for put option negative?
def test_black_scholes_delta_put_is_negative():
    delta = black_scholes_delta(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="put",
        dividend_yield=DIVIDEND_YIELD,
    )
    
    assert delta < 0

#Option type standardization.
def test_black_scholes_delta_call_standardization():
    delta = black_scholes_delta(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type=" CALL ",
        dividend_yield=DIVIDEND_YIELD,
    )
    
    assert delta == pytest.approx(0.6368, rel=1e-4)

#Invalid Option input
def test_black_scholes_delta_invalid_option_input():
    
    with pytest.raises(ValueError):
        black_scholes_delta(
            spot_price=SPOT,
            strike_price=STRIKE,
            time_to_expiry=TIME_TO_EXPIRY,
            risk_free_rate=RISK_FREE_RATE,
            volatility=VOLATILITY,
            option_type=" INVALID ",
            dividend_yield=DIVIDEND_YIELD,
        )
    
def test_black_scholes_gamma_benchmark_values():
    
    benchmark_gamma = black_scholes_gamma(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="call",
        dividend_yield=DIVIDEND_YIELD,
    )
        
    assert benchmark_gamma == pytest.approx(0.01876, rel=2e-4)

def test_black_scholes_gamma_is_positive():
    
    gamma = black_scholes_gamma(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="call",
        dividend_yield=DIVIDEND_YIELD,
    )
    
    assert gamma > 0

def test_black_scholes_gamma_is_same_call_put_options():
    
    call_gamma = black_scholes_gamma(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="call",
        dividend_yield=DIVIDEND_YIELD,
    )
    
    put_gamma = black_scholes_gamma(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="put",
        dividend_yield=DIVIDEND_YIELD,
    )
    
    assert call_gamma == pytest.approx(put_gamma, rel=1e-12)

def test_black_scholes_gamma_invalid_option_type():
    
    with pytest.raises(ValueError):
        black_scholes_gamma(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="invalid",
        dividend_yield=DIVIDEND_YIELD,
    )

#Benchmark Vega test
def test_black_scholes_vega_benchmark_value():
    vega = black_scholes_vega(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="call",
        dividend_yield=DIVIDEND_YIELD,
    )

    assert vega == pytest.approx(37.5240, rel=1e-3)

#Vega is positive for long call
def test_black_scholes_vega_is_positive_for_call():
    vega = black_scholes_vega(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="call",
        dividend_yield=DIVIDEND_YIELD,
    )

    assert vega > 0.0

#Vega is positive for long put
def test_black_scholes_vega_is_positive_for_put():
    vega = black_scholes_vega(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="put",
        dividend_yield=DIVIDEND_YIELD,
    )

    assert vega > 0.0

#Vega is same for both call and put
def test_black_scholes_vega_same_for_call_and_put():
    call_vega = black_scholes_vega(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="call",
        dividend_yield=DIVIDEND_YIELD,
    )

    put_vega = black_scholes_vega(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="put",
        dividend_yield=DIVIDEND_YIELD,
    )

    assert call_vega == pytest.approx(put_vega, rel=1e-12)

#Invalid option Error
def test_black_scholes_vega_invalid_option_input():
    with pytest.raises(ValueError):
        black_scholes_vega(
            spot_price=SPOT,
            strike_price=STRIKE,
            time_to_expiry=TIME_TO_EXPIRY,
            risk_free_rate=RISK_FREE_RATE,
            volatility=VOLATILITY,
            option_type="INVALID",
            dividend_yield=DIVIDEND_YIELD,
        )