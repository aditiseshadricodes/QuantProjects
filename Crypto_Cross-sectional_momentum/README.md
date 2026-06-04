# Cross-Sectional Crypto Momentum Research using Liquid Crypto Assets

This project explores a weekly rebalanced cross-sectional crypto momentum strategy across the top 15 crypto assets by trading volume. The research compares plain momentum, volatility-targeted momentum, residual momentum, and residual momentum with volatility targeting, with the goal of identifying the most robust implementation across train, validation, and out-of-sample periods.

## Project Objective

The purpose of this project is to test whether a simple and robust momentum signal can generate attractive risk-adjusted returns in liquid crypto assets, while controlling for turnover, drawdowns, and benchmark exposure.

## Universe

- Top 15 crypto assets by trading volume
- Stablecoins excluded
- 4-hour data sampling frequency
- Weekly rebalancing

## Strategy Variants Tested

1. Plain momentum
2. Volatility-targeted momentum
3. Residual momentum
4. Residual momentum with volatility targeting

## Methodology

- Construct weekly returns from 4-hour data
- Rank assets using momentum-style signals
- Build cross-sectional portfolio weights
- Compare variants across train / validation / out-of-sample splits
- Evaluate Sharpe, alpha vs BTC, beta vs BTC, drawdown, turnover, and Newey-West t-statistics

## Key Result

The preferred model was **Case 2: Volatility-Targeted Momentum**.

Best validation-period metrics:
- **Validation Sharpe:** 0.92
- **Validation Alpha vs BTC:** 0.19
- **Validation Newey-West t-stat:** 1.36

This variant was selected because it showed the strongest balance of Sharpe, alpha, and statistical robustness, while maintaining better drawdown behavior than the residual-momentum alternatives.

## Research Notes

Additional ideas explored in the project included:
- different universe sizes
- transaction costs from 5 bps to 20 bps
- momentum lookbacks from 4 to 12 weeks

A 4-week momentum lookback was chosen as the preferred setting because it captured recent activity more responsively and delivered the strongest overall performance.

Weekly rebalancing was chosen to reduce trading costs, while 4-hour sampling was used to reduce market microstructure noise while still capturing meaningful intraday behavior.

## File Structure

- `Cross_sectional_crypto_momentum.ipynb` — full research notebook
- `README.md` — project overview and findings

## Current Limitations

- small universe size
- sensitivity to implementation choices
- limited statistical significance in current validation results
- further robustness testing required before production use

## Future Improvements

- convert notebook workflow into a modular Python project
- achieve higher statistically significant alpha
- add transaction-cost sensitivity tables and cleaner result exports
- extend robustness testing to larger universes and alternative benchmark controls
- productionize signal generation and backtesting in a local IDE-based environment

## Tools Used

- Python
- Pandas
- NumPy
- Matplotlib
- Statsmodels

## How to Run

1. Open the notebook in Google Colab or Jupyter
2. Install required dependencies
3. Load the input price and volume data
4. Run the notebook cells in order to reproduce the strategy construction, evaluation tables, and plots
