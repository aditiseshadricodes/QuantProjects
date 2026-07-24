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