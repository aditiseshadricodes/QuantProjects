import pytest
import math
import numpy as np

from src.option_pricing import black_scholes_price
from src.greeks import (
    _norm_pdf,
    black_scholes_delta,
    black_scholes_gamma,
    black_scholes_vega,
    black_scholes_rho,
    black_scholes_theta
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

#Benchmark Rho test
def test_black_scholes_rho_benchmark_case():
    
    result = black_scholes_rho(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="call",
        dividend_yield=DIVIDEND_YIELD,
    )
    assert result == pytest.approx(0.5323248, rel=1e-3)
    
    result = black_scholes_rho(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="put",
        dividend_yield=DIVIDEND_YIELD,
    )
    assert result == pytest.approx(
        -0.418904609047,
        rel=1e-3,
    )

BASE = {
    "spot_price": 100.0,
    "strike_price": 100.0,
    "time_to_expiry": 1.0,
    "risk_free_rate": 0.05,
    "dividend_yield": 0.0,
    "volatility": 0.20,
}


def test_rho_has_correct_sign_for_call_and_put():
    call_rho = black_scholes_rho(
        **BASE,
        option_type="call",
    )
    put_rho = black_scholes_rho(
        **BASE,
        option_type="put",
    )

    assert call_rho > 0.0
    assert put_rho < 0.0

@pytest.mark.parametrize("option_type", ["call", "put"])
def test_rho_matches_finite_difference(option_type):
    rate_bump = 1e-5

    price_up = black_scholes_price(
        **{
            **BASE,
            "risk_free_rate": (
                BASE["risk_free_rate"] + rate_bump
            ),
        },
        option_type=option_type,
    )

    price_down = black_scholes_price(
        **{
            **BASE,
            "risk_free_rate": (
                BASE["risk_free_rate"] - rate_bump
            ),
        },
        option_type=option_type,
    )

    numerical_rho = (
        price_up - price_down
    ) / (2.0 * rate_bump) / 100.0

    analytical_rho = black_scholes_rho(
        **BASE,
        option_type=option_type,
    )

    assert analytical_rho == pytest.approx(
        numerical_rho,
        rel=1e-3,
        abs=1e-3,
    )

def test_call_put_rho_parity():
    call_rho = black_scholes_rho(
        **BASE,
        option_type="call",
    )
    put_rho = black_scholes_rho(
        **BASE,
        option_type="put",
    )

    expected_difference = (
        BASE["strike_price"]
        * BASE["time_to_expiry"]
        * math.exp(
            -BASE["risk_free_rate"]
            * BASE["time_to_expiry"]
        ) / 100.0
    )

    assert call_rho - put_rho == pytest.approx(
        expected_difference,
        rel=1e-9,
    )

@pytest.mark.parametrize(
    ("option_type", "expected"),
    [
        ("call", 0.444808223402),
        ("put", -0.565241943682),
    ],
)
def test_rho_accepts_negative_interest_rate(
    option_type,
    expected,
):
    result = black_scholes_rho(
        **{
            **BASE,
            "risk_free_rate": -0.01,
        },
        option_type=option_type,
    )

    assert result == pytest.approx(
        expected,
        rel=1e-9,
    )

@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("spot_price", 0.0),
        ("strike_price", -100.0),
        ("time_to_expiry", -1.0),
        ("volatility", -0.20),
        ("risk_free_rate", np.nan),
        ("dividend_yield", np.inf),
        ("option_type", "banana"),
    ],
)
def test_rho_rejects_invalid_inputs(
    field,
    invalid_value,
):
    inputs = {
        **BASE,
        "option_type": "call",
    }
    inputs[field] = invalid_value

    with pytest.raises((TypeError, ValueError)):
        black_scholes_rho(**inputs)

#Benchmark theta value
def test_black_scholes_theta_benchmark_case():
    
    result = black_scholes_theta(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="call",
        dividend_yield=DIVIDEND_YIELD,
    )
    assert result == pytest.approx(-0.0175726782, rel=5e-3)
    
    result = black_scholes_theta(
        spot_price=SPOT,
        strike_price=STRIKE,
        time_to_expiry=TIME_TO_EXPIRY,
        risk_free_rate=RISK_FREE_RATE,
        volatility=VOLATILITY,
        option_type="put",
        dividend_yield=DIVIDEND_YIELD,
    )
    assert result == pytest.approx(
        -0.0045421381,
        rel=1e-3,
    )

#Sign check for theta
def test_theta_has_correct_sign_for_call_and_put():
    call_theta = black_scholes_theta(
        **BASE,
        option_type="call",
    )
    put_theta = black_scholes_theta(
        **BASE,
        option_type="put",
    )

    assert call_theta < 0.0
    assert put_theta < 0.0

#Theta finite difference
@pytest.mark.parametrize("option_type", ["call", "put"])
def test_theta_matches_finite_difference(option_type):
    time_delta = 1e-5

    price_less_time = black_scholes_price(
        **{
            **BASE,
            "time_to_expiry": (
                BASE["time_to_expiry"] - time_delta
            ),
        },
        option_type=option_type,
    )

    price_more_time = black_scholes_price(
        **{
            **BASE,
            "time_to_expiry": (
                BASE["time_to_expiry"] + time_delta
            ),
        },
        option_type=option_type,
    )

    numerical_theta = (
        price_less_time - price_more_time
    ) / (2.0 * time_delta) / 365.0

    analytical_theta = black_scholes_theta(
        **BASE,
        option_type=option_type,
    )

    assert analytical_theta == pytest.approx(
        numerical_theta,
        rel=1e-3,
        abs=1e-3,
    )

#Call - Put Theta Parity
def test_call_put_theta_parity():
    call_theta = black_scholes_theta(
        **BASE,
        option_type="call",
    )
    put_theta = black_scholes_theta(
        **BASE,
        option_type="put",
    )

    expected_difference = (
        -BASE["strike_price"]
        * BASE["risk_free_rate"]
        * math.exp(
            -BASE["risk_free_rate"]
            * BASE["time_to_expiry"]
        ) / 365.0
    )

    assert call_theta - put_theta == pytest.approx(
        expected_difference,
        rel=1e-9,
    )

#Invalid case
@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("spot_price", 0.0),
        ("strike_price", -100.0),
        ("time_to_expiry", -1.0),
        ("volatility", -0.20),
        ("risk_free_rate", np.nan),
        ("dividend_yield", np.inf),
        ("option_type", "banana"),
    ],
)
def test_theta_rejects_invalid_inputs(
    field,
    invalid_value,
):
    inputs = {
        **BASE,
        "option_type": "call",
    }
    inputs[field] = invalid_value

    with pytest.raises((TypeError, ValueError)):
        black_scholes_theta(**inputs)