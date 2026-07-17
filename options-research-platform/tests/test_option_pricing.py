import math
import pytest
import pandas as pd

from src.option_pricing import (
    _norm_cdf,
    _standardize_option_type,
    _validate_finite_float,
    _validate_positive_float,
    _validate_non_negative_float,
    intrinsic_value,
    _validate_scalar_pricing_inputs,
    _d1d2,
    black_scholes_price,
    _time_to_expiry,
    _get_spot_price,
    _price_option_row,
    price_option_chain,
)

@pytest.fixture
def sample_option_chain():
    return pd.DataFrame({
        "strike_price":[100.0, 100.0],
        "expiry_date":["2024-12-31", "2024-12-31"],
        "option_type":["call", "put"],
        "implied_volatility":[0.20, 0.20],
    })

def test_norm_cdf_valid_inputs():
    
    assert _norm_cdf(0) == pytest.approx(0.5)
    assert _norm_cdf(1) == pytest.approx(0.8413, rel=1e-4)
    assert _norm_cdf(-1) == pytest.approx(0.15865525393145713, rel=1e-10)

def test_norm_cdf_str_input():
    
    with pytest.raises(TypeError):
        _norm_cdf("1")

def test_norm_cdf_list_input():
    
    with pytest.raises(TypeError):
        _norm_cdf([1, 2, 3])

def test_norm_cdf_dict_input():
    
    with pytest.raises(TypeError):
        _norm_cdf({"x": 1})

def test_norm_cdf_bool_input():
    with pytest.raises(TypeError):
        _norm_cdf(True)

def test_norm_cdf_nan_input():
    with pytest.raises(ValueError):
        _norm_cdf(float("nan"))

def test_norm_cdf_inf_input():
    with pytest.raises(ValueError):
        _norm_cdf(float("inf"))

def test_standardize_option_type_valid_inputs():
    
    assert _standardize_option_type("call") == "call"
    assert _standardize_option_type("put") == "put"
    assert _standardize_option_type("c") == "call"
    assert _standardize_option_type("p") == "put"
    assert _standardize_option_type("CALL") == "call"
    assert _standardize_option_type("PUT") == "put"
    assert _standardize_option_type("Call") == "call"
    assert _standardize_option_type("Put") == "put"
    assert _standardize_option_type(" CALL ") == "call"
    assert _standardize_option_type(" PUT ") == "put"

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
        spot_price=100,
        strike_price=100,
        time_to_expiry=1,
        risk_free_rate=0.05,
        volatility=0.2,
        option_type="call",
        dividend_yield=0.02
    )
    
    assert inputs == (100, 100, 1, 0.05, 0.2, "call", 0.02)

def test_validate_scalar_pricing_inputs_zero_expiry():
    
    inputs = _validate_scalar_pricing_inputs(
        spot_price=100,
        strike_price=100,
        time_to_expiry=0,
        risk_free_rate=0.05,
        volatility=0.2,
        option_type="put",
        dividend_yield=0.02
    )
    
    assert inputs == (100, 100, 0, 0.05, 0.2, "put", 0.02)

def test_validate_scalar_pricing_inputs_negative_risk_free_rate():
    
    inputs = _validate_scalar_pricing_inputs(
        spot_price=100,
        strike_price=100,
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
            spot_price="100",
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2,
            option_type="call",
            dividend_yield=0.02
        )
        
    #Negative time to expiry
    with pytest.raises(ValueError):
        _validate_scalar_pricing_inputs(
            spot_price=100,
            strike_price=100,
            time_to_expiry=-1,
            risk_free_rate=0.05,
            volatility=0.2,
            option_type="call",
            dividend_yield=0.02
        )
        
    #Infinite risk free rate
    with pytest.raises(ValueError):
        _validate_scalar_pricing_inputs(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=float('inf'),
            volatility=0.2,
            option_type="call",
            dividend_yield=0.02
        )
        
    #Negative volatility
    with pytest.raises(ValueError):
        _validate_scalar_pricing_inputs(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=-0.2,
            option_type="call",
            dividend_yield=0.02
        )
        
    #Invalid option type
    with pytest.raises(ValueError):
        _validate_scalar_pricing_inputs(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2,
            option_type="invalid_option",
            dividend_yield=0.02
        )
        
    #Negative dividend yield
    with pytest.raises(ValueError):
        _validate_scalar_pricing_inputs(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2,
            option_type="call",
            dividend_yield=-0.01
        )
        
    #Wrong strike type
    with pytest.raises(TypeError):
        _validate_scalar_pricing_inputs(
            spot_price=100,
            strike_price="100",
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2,
            option_type="call",
            dividend_yield=0.02
        )

#Valid _d1d2 inputs
@pytest.mark.parametrize(
    "spot_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield,expected_d1,expected_d2",
    [
        (100,100,1,0.05,0.2,0.0,0.35,0.15),
        (100,100,1,0.05,0.2,0.02,0.25,0.05),
        (100,100,1,-0.01,0.2,0.0,0.05,-0.15)
    ],
)
def test_d1d2_benchmark_cases(
    spot_price,
    strike_price,
    time_to_expiry,
    risk_free_rate,
    volatility,
    dividend_yield,
    expected_d1,
    expected_d2
):
    d1,d2 = _d1d2(
        spot_price=spot_price,
        strike_price=strike_price,
        time_to_expiry=time_to_expiry,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        dividend_yield=dividend_yield
    )
    
    assert d1 == pytest.approx(expected_d1, rel=1e-2)
    assert d2 == pytest.approx(expected_d2, rel=1e-2)

#Zero time to expiry should raise ValueError for _d1d2 function
def test_d1d2_zero_time_to_expiry_input():
    
    with pytest.raises(ValueError):
        _d1d2(
            spot_price=100,
            strike_price=100,
            time_to_expiry=0,
            risk_free_rate=0.05,
            volatility=0.2,
            dividend_yield=0.02
        )

#Basic Smoke test for _d1d2 function with wrong inputs.
def test_d1d2_invalid_inputs():
    
    with pytest.raises(TypeError):
        _d1d2(
            spot_price="100",
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2,
            dividend_yield=0.02
        )
        
    with pytest.raises(ValueError):
        _d1d2(
            spot_price=100,
            strike_price=100,
            time_to_expiry=-1,
            risk_free_rate=0.05,
            volatility=0.2,
            dividend_yield=0.02
        )
        
    with pytest.raises(ValueError):
        _d1d2(
            spot_price=100,
            strike_price=100,
            time_to_expiry=1,
            risk_free_rate=0.05,
            volatility=0.2,
            dividend_yield=-0.01
        )

#Valid Black-Scholes pricing inputs and expected outputs for call and put options
@pytest.mark.parametrize(
    "spot_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield, option_type, expected_price",
    [
        (100,100,1,0.05,0.2,0.0,"call",10.4506),
        (100,100,1,0.05,0.2,0.0,"put",5.5735)
    ],
)
def test_black_scholes_price_benchmark_cases(
    spot_price,
    strike_price,
    time_to_expiry,
    risk_free_rate,
    volatility,
    dividend_yield,
    option_type,
    expected_price
):
    price = black_scholes_price(
        spot_price=spot_price,
        strike_price=strike_price,
        time_to_expiry=time_to_expiry,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        option_type=option_type,
        dividend_yield=dividend_yield
    )
    
    assert price == pytest.approx(expected_price, rel=1e-4)

#Cases for time to expiry = 0, where option price = intrinsic value
@pytest.mark.parametrize(
    "spot_price, strike_price, option_type, expected_price",
    [
        (100, 90, "call", 10),  # ITM call
        (100, 110, "call", 0),  # OTM call
        (100, 100, "call", 0),  # ATM call
        (100, 110, "put", 10),   # ITM put
        (100, 90, "put", 0),     # OTM put
        (100, 100, "put", 0)     # ATM put
    ],
)
def test_black_scholes_price_zero_time_to_expiry(
    spot_price,
    strike_price,
    option_type,
    expected_price
):
    price = black_scholes_price(
        spot_price=spot_price,
        strike_price=strike_price,
        time_to_expiry=0,
        risk_free_rate=0.05,
        volatility=0.2,
        option_type=option_type,
        dividend_yield=0.02
    )
    
    assert price == pytest.approx(expected_price, rel=1e-4)

#Put-Call Parity test cases
@pytest.mark.parametrize(
    "spot_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield",
    [
        (100, 100, 1, 0.05, 0.2, 0.0),
        (100, 100, 1, 0.05, 0.2, 0.02),
        (100, 100, 1, -0.01, 0.2, 0.0)
    ],
)
def test_black_scholes_price_put_call_parity(
    spot_price,
    strike_price,
    time_to_expiry,
    risk_free_rate,
    volatility,
    dividend_yield
):
    call_price = black_scholes_price(
        spot_price=spot_price,
        strike_price=strike_price,
        time_to_expiry=time_to_expiry,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        option_type="call",
        dividend_yield=dividend_yield
    )
    
    put_price = black_scholes_price(
        spot_price=spot_price,
        strike_price=strike_price,
        time_to_expiry=time_to_expiry,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        option_type="put",
        dividend_yield=dividend_yield
    )
    
    # Calculate the present value of the strike price and spot price
    present_value_spot = spot_price*math.exp(-dividend_yield*time_to_expiry)
    present_value_strike = strike_price*math.exp(-risk_free_rate*time_to_expiry)
    expected_parity = present_value_spot - present_value_strike
    
    # Check Put-Call Parity: C - P = S - PV(K)
    assert call_price - put_price == pytest.approx(expected_parity, rel=1e-4)

#Invalid input smoke test
def test_black_scholes_price_invalid_inputs():
    
    with pytest.raises(TypeError):
        black_scholes_price(
            "100",
            100,
            1,
            0.05,
            0.2,
            "call",
            0.0
        )
    
    with pytest.raises(ValueError):
        black_scholes_price(
            100,
            100,
            1,
            0.05,
            0.2,
            "banana",
            0.0
        )

def test_time_to_expiry_one_year_returns_one():
    result = _time_to_expiry("2024-01-01", "2024-12-31")
    assert result == pytest.approx(365 / 365.0)

def test_time_to_expiry_same_day_returns_zero():
    result = _time_to_expiry("2024-01-01","2024-01-01")
    assert result == 0.0

def test_time_to_expiry_expiry_before_valuation_raises_value_error():
    with pytest.raises(ValueError):
        _time_to_expiry("2024-01-02", "2024-01-01")

def test_time_to_expiry_string_inputs_parse_correctly():
    result = _time_to_expiry("2024-01-01","2024-01-31")
    assert result == pytest.approx(30/365.0)

def test_time_to_expiry_timestamp_inputs_work():
    result = _time_to_expiry(
        pd.Timestamp("2024-01-01"),
        pd.Timestamp("2024-04-01")
    )
    assert result == pytest.approx(91/365.0)

def test_time_to_expiry_invalid_date():
    with pytest.raises(ValueError):
        _time_to_expiry("not-a-date", "2024-01-01")

def test_get_spot_price_valid_input():
    
    assert _get_spot_price(100) == pytest.approx(100.0)
    assert _get_spot_price(150.625) == pytest.approx(150.625, rel=1e-2)

def test_get_spot_price_invalid_inputs():
    
    with pytest.raises(ValueError):
        _get_spot_price(0)
    
    with pytest.raises(ValueError):
        _get_spot_price(-100)
    
    with pytest.raises(TypeError):
        _get_spot_price("100.50")
    
    with pytest.raises(TypeError):
        _get_spot_price(True)
    
    with pytest.raises(ValueError):
        _get_spot_price(float('inf'))
    
    with pytest.raises(ValueError):
        _get_spot_price(float('nan'))

def test_prices_option_row_valid_call():
    row = pd.Series({
        "strike_price":100.0,
        "expiry_date":"2024-12-31",
        "option_type":"call",
        "implied_volatility":0.20,
    })
    
    result = _price_option_row(
        row=row,
        valuation_date="2024-01-01",
        spot_price=100.0,
        risk_free_rate=0.05,
        dividend_yield=0.0,
        volatility_col="implied_volatility"
    )
    
    assert result == pytest.approx(10.4506,rel=1e-4)

def test_prices_option_row_valid_put():
    row = pd.Series({
        "strike_price":100.0,
        "expiry_date":"2024-12-31",
        "option_type":"put",
        "implied_volatility":0.20,
    })
    
    result = _price_option_row(
        row=row,
        valuation_date="2024-01-01",
        spot_price=100.0,
        risk_free_rate=0.05,
        dividend_yield=0.0,
        volatility_col="implied_volatility"
    )
    
    assert result == pytest.approx(5.5735,rel=1e-4)

def test_prices_option_row_same_day_expiry():
    row = pd.Series({
        "strike_price":90.0,
        "expiry_date":"2024-01-01",
        "option_type":"call",
        "implied_volatility":0.20,
    })
    
    result = _price_option_row(
        row=row,
        valuation_date="2024-01-01",
        spot_price=100.0,
        risk_free_rate=0.05,
        dividend_yield=0.0,
        volatility_col="implied_volatility"
    )
    
    assert result == pytest.approx(10.0, rel=1e-2)

def test_prices_option_row_missing_col():
    row = pd.Series({
        "Strike":100.0,
        "expiry_date":"2024-12-31",
        "option_type":"call",
        "volatility_col":0.20,
    })
    
    with pytest.raises(KeyError):
        _price_option_row(
            row=row,
            valuation_date="2024-01-01",
            spot_price=100.0,
            risk_free_rate=0.05,
            dividend_yield=0.0,
            volatility_col=0.2
        )

def test_prices_option_row_custom_vol():
    row = pd.Series({
        "strike_price":100.0,
        "expiry_date":"2024-12-31",
        "option_type":"call",
        "vol":0.20,
    })
    
    result = _price_option_row(
        row=row,
        valuation_date="2024-01-01",
        spot_price=100.0,
        risk_free_rate=0.05,
        dividend_yield=0.0,
        volatility_col="vol"
    )
    
    assert result == pytest.approx(10.4506,rel=1e-4)

def test_price_option_chain_valid_chain(sample_option_chain):
    result = price_option_chain(
        option_chain=sample_option_chain,
        valuation_date="2024-01-01",
        spot_price=100.0,
        risk_free_rate=0.05,
        dividend_yield=0.0,
    )
    
    assert "model_price" in result.columns

def test_price_option_chain_correct_call_put_prices(sample_option_chain):
    result = price_option_chain(
        option_chain=sample_option_chain,
        valuation_date="2024-01-01",
        spot_price=100.0,
        risk_free_rate=0.05,
        dividend_yield=0.0,
    )
    
    assert result.loc[0,"model_price"] == pytest.approx(10.4506,rel=1e-4)
    assert result.loc[1,"model_price"] == pytest.approx(5.5735,rel=1e-4)

def test_price_option_chain_original_df(sample_option_chain):
    
    assert "model_price" not in sample_option_chain.columns

def test_price_option_chain_custom_output_col(sample_option_chain):
    result = price_option_chain(
        option_chain=sample_option_chain,
        valuation_date="2024-01-01",
        spot_price=100.0,
        risk_free_rate=0.05,
        dividend_yield=0.0,
        output_col="bs_price"
    )
    
    assert "bs_price" in result.columns
    assert "model_price" not in result.columns

def test_price_option_chain_custom_vol_column():
    option_chain = pd.DataFrame({
        "strike_price":[100.0, 100.0],
        "expiry_date":["2024-12-31", "2024-12-31"],
        "option_type":["call", "put"],
        "vol":[0.20, 0.20],
    })
    
    result = price_option_chain(
        option_chain=option_chain,
        valuation_date="2024-01-01",
        spot_price=100.0,
        risk_free_rate=0.05,
        dividend_yield=0.0,
        volatility_col="vol"
    )
    
    assert result.loc[0,"model_price"] == pytest.approx(10.4506,rel=1e-4)
    assert result.loc[1,"model_price"] == pytest.approx(5.5735,rel=1e-4)

def test_price_option_chain_missing_key():
    option_chain = pd.DataFrame({
        "Strike":[100.0, 100.0],
        "expiry_date":["2024-12-31", "2024-12-31"],
        "option_type":["call", "put"],
        "implied_volatility":[0.20, 0.20],
    })
    
    with pytest.raises(KeyError):
        price_option_chain(
            option_chain=option_chain,
            valuation_date="2024-01-01",
            spot_price=100.0,
            risk_free_rate=0.05,
            dividend_yield=0.0
        )

def test_price_option_chain_bad_option_chain():
    option_chain = []
    
    with pytest.raises(TypeError):
        price_option_chain(
            option_chain=option_chain,
            valuation_date="2024-01-01",
            spot_price=100.0,
            risk_free_rate=0.05,
            dividend_yield=0.0
        )

def test_price_option_chain_invalid_vol():
    option_chain = pd.DataFrame({
        "strike_price":[100.0, 100.0],
        "expiry_date":["2024-12-31", "2024-12-31"],
        "option_type":["call", "put"],
        "implied_volatility":[0.0, 0.0],
    })
    
    with pytest.raises(ValueError):
        price_option_chain(
            option_chain=option_chain,
            valuation_date="2024-01-01",
            spot_price=100.0,
            risk_free_rate=0.05,
            dividend_yield=0.0
        )