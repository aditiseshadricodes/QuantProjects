# Options Research Project

## Current Status: Options Pricing V1

This project now includes a tested European Black-Scholes pricing foundation.

Implemented components:

- Scalar Black-Scholes call/put pricing
- Input validation for pricing parameters
- Option type normalization
- Intrinsic value handling at expiry
- Time-to-expiry calculation
- Spot price validation
- Row-level option pricing
- Option-chain pricing with a model price output column

The pricing flow is:

```text
option_chain DataFrame
→ _price_option_row
→ _time_to_expiry
→ black_scholes_price
→ model_price
```
## V1 Assumptions

V1 focuses on vanilla European option pricing using the Black-Scholes model.

Current assumptions:

- European exercise only
- Continuous risk-free rate
- Continuous dividend yield
- Annualized volatility input
- Calendar-day time to expiry using a 365-day year
- No American exercise
- No discrete dividends
- No transaction costs
- No live market-data fetching inside the pricing module