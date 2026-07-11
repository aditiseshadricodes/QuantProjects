import pandas as pd
import pytest

from src.option_pricing import (
    _norm_cdf,
    _standardize_option_type,
    _validate_finite_float,
    _validate_positive_float,
    _validate_non_negative_float,
    intrinsic_value,
    _validate_scalar_pricing_inputs
)

def test_norm_cdf_valid_inputs():
    
    assert _norm_cdf(0) == pytest.approx(0.5)
    assert _norm_cdf(1) > 0.5
    assert _norm_cdf(-1) < 0.5

def test_norm_cdf_str_input():
    
    with pytest.raises(TypeError):
        _norm_cdf("1")

def test_norm_cdf_list_input():
    
    with pytest.raises(TypeError):
        _norm_cdf([1, 2, 3])

def test_norm_cdf_dict_input():
    
    with pytest.raises(TypeError):
        _norm_cdf({"x": 1})

def test_standardize_option_type_valid_inputs():
    
    assert _standardize_option_type("call") == "call"
    assert _standardize_option_type("put") == "put"
    assert _standardize_option_type("c") == "call"
    assert _standardize_option_type("p") == "put"
    assert _standardize_option_type("CALL") == "call"
    assert _standardize_option_type("PUT") == "put"

def test_standardize_option_type_numeric_input():
    
    with pytest.raises(TypeError):
        _standardize_option_type(1)

def test_standardize_option_type_list_input():
    
    with pytest.raises(TypeError):
        _standardize_option_type(["call", "put"])

def test_standardize_option_type_dict_input():
    
    with pytest.raises(TypeError):
        _standardize_option_type({"option": "call"})

def test_standardize_option_type_invalid_string():
    
    with pytest.raises(ValueError):
        _standardize_option_type("invalid_option")

def test_validate_finite_float_valid_inputs():
    
    assert _validate_finite_float(1.0,"positive") == 1.0
    assert _validate_finite_float(-1.0,"negative") == -1.0
    assert _validate_finite_float(0.0,"zero") == 0.0

def test_validate_finite_float_nan_input():
    
    with pytest.raises(ValueError):
        _validate_finite_float(float('nan'),"nan")

def test_validate_finite_float_inf_input():
    
    with pytest.raises(ValueError):
        _validate_finite_float(float('inf'),"infinite")

def test_validate_finite_float_str_input():
    
    with pytest.raises(TypeError):
        _validate_finite_float("1.0","string")

def test_validate_finite_float_list_input():
    
    with pytest.raises(TypeError):
        _validate_finite_float([1.0, 2.0],"list")

def test_validate_finite_float_dict_input():
    
    with pytest.raises(TypeError):
        _validate_finite_float({"value": 1.0},"dict")

def test_validate_finite_float_none_input():
    
    with pytest.raises(TypeError):
        _validate_finite_float(None,"None")

def test_validate_finite_float_bool_input():
    
    with pytest.raises(TypeError):
        _validate_finite_float(True,"boolean")

def test_validate_positive_float_valid_inputs():
    
    assert _validate_positive_float(1.0, "positive_above_1") == 1.0
    assert _validate_positive_float(0.1, "positive_below_1") == 0.1

def test_validate_positive_float_zero_input():
    
    with pytest.raises(ValueError):
        _validate_positive_float(0.0, "zero")

def test_validate_positive_float_negative_input():
    
    with pytest.raises(ValueError):
        _validate_positive_float(-1.0, "negative")

def test_validate_non_negative_float_valid_inputs():
    
    assert _validate_non_negative_float(1.0, "positive_above_1") == 1.0
    assert _validate_non_negative_float(0.1, "positive_below_1") == 0.1
    assert _validate_non_negative_float(0.0, "zero") == 0.0

def test_validate_non_negative_float_negative_input():
    
    with pytest.raises(ValueError):
        _validate_non_negative_float(-1.0, "negative")

def test_intrinsic_value_call():
    
    assert intrinsic_value(100, 90, "call") == 10 #ITM
    assert intrinsic_value(100, 110, "call") == 0 #OTM
    assert intrinsic_value(100, 100, "call") == 0 #ATM

def test_intrinsic_value_put():
    
    assert intrinsic_value(100, 110, "put") == 10 #ITM
    assert intrinsic_value(100, 90, "put") == 0 #OTM
    assert intrinsic_value(100, 100, "put") == 0 #ATM
    
def test_intrinsic_value_invalid_option_type():
    
    with pytest.raises(ValueError):
        intrinsic_value(100, 100, "invalid_option")

def test_intrinsic_value_invalid_inputs():
    
    with pytest.raises(TypeError):
        intrinsic_value("100", 100, "call")
    with pytest.raises(TypeError):
        intrinsic_value(100, "100", "put")
    with pytest.raises(TypeError):
        intrinsic_value(100, 100, 1)

def test_validate_scalar_pricing_inputs_valid_inputs():
    
    inputs = _validate_scalar_pricing_inputs(
        spot=100,
        strike=100,
        time_to_expiry=1,
        risk_free_rate=0.05,
        volatility=0.2,
        option_type="call",
        dividend_yield=0.02
    )
    
    assert inputs == (100, 100, 1, 0.05, 0.2, "call", 0.02)

def test_validate_scalar_pricing_inputs_zero_expiry():
    
    inputs = _validate_scalar_pricing_inputs(
        spot=100,
        strike=100,
        time_to_expiry=0,
        risk_free_rate=0.05,
        volatility=0.2,
        option_type="put",
        dividend_yield=0.02
    )
    
    assert inputs == (100, 100, 0, 0.05, 0.2, "put", 0.02)

def test_validate_scalar_pricing_inputs_negative_risk_free_rate():
    
    inputs = _validate_scalar_pricing_inputs(
        spot=100,
        strike=100,
        time_to_expiry=1,
        risk_free_rate=-0.01,
        volatility=0.2,
        option_type="call",
        dividend_yield=0.02
    )
    
    assert inputs == (100, 100, 1, -0.01, 0.2, "call", 0.02)

def test_validate_scalar_pricing_inputs_invalid_inputs():
    
    #Wrong spot type
    with pytest.raises(TypeError):
        _validate_scalar_pricing_inputs(
            spot="100",
            strike=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2,
            option_type="call",
            dividend_yield=0.02
        )
        
    #Negative time to expiry
    with pytest.raises(ValueError):
        _validate_scalar_pricing_inputs(
            spot=100,
            strike=100,
            time_to_expiry=-1,
            risk_free_rate=0.05,
            volatility=0.2,
            option_type="call",
            dividend_yield=0.02
        )
        
    #Infinite risk free rate
    with pytest.raises(ValueError):
        _validate_scalar_pricing_inputs(
            spot=100,
            strike=100,
            time_to_expiry=1,
            risk_free_rate=float('inf'),
            volatility=0.2,
            option_type="call",
            dividend_yield=0.02
        )
        
    #Negative volatility
    with pytest.raises(ValueError):
        _validate_scalar_pricing_inputs(
            spot=100,
            strike=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=-0.2,
            option_type="call",
            dividend_yield=0.02
        )
        
    #Invalid option type
    with pytest.raises(ValueError):
        _validate_scalar_pricing_inputs(
            spot=100,
            strike=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2,
            option_type="invalid_option",
            dividend_yield=0.02
        )
        
    #Negative dividend yield
    with pytest.raises(ValueError):
        _validate_scalar_pricing_inputs(
            spot=100,
            strike=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2,
            option_type="call",
            dividend_yield=-0.01
        )
        
    #Wrong strike type
    with pytest.raises(TypeError):
        _validate_scalar_pricing_inputs(
            spot=100,
            strike="100",
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2,
            option_type="call",
            dividend_yield=0.02
        )