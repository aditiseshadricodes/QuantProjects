# Quantitative Finance Research Projects

A collection of Python-based quantitative finance research projects focused on systematic trading, portfolio construction, options pricing, risk analytics, validation, and reproducible research workflows.

The repository emphasizes:

- clean research pipelines
- input validation
- out-of-sample and walk-forward testing
- realistic implementation assumptions
- modular Python code
- readable notebooks
- automated pytest coverage
- honest reporting of limitations

## Projects

| Project | Status | Focus |
|---|---|---|
| pairs-trading-ai-tech | Complete V2, V2.1 scheduled | Equity statistical arbitrage, walk-forward/OOS validation, portfolio-level backtesting, transaction-cost modelling |
| options-research-platform | WIP | Black-Scholes pricing, option chain pricing, Greeks, scalar validation, volatility and risk tooling |
| cvar_var_risk_pipeline | Complete small project | VaR/CVaR risk analytics |
| Crypto_Cross-sectional_momentum | Complete notebook research | Crypto momentum, train/test/OOS evaluation |

Across the active projects, the repository includes 244 automated tests covering pricing logic, validation, backtesting assumptions, edge cases, and research pipeline behavior.

## Featured Project: Pairs Trading Research Pipeline

The main project is a modular equity pairs trading research framework.

It currently includes:

* data loading and validation,
* 50-stock universe expansion,
* correlation and cointegration-based pair selection,
* walk-forward train/test/OOS folds,
* transaction-cost modeling,
* portfolio construction,
* train/test/OOS backtesting,
* performance diagnostics,
* and pytest coverage for key modules.

The project is currently in V2.1 development. Results are treated as research diagnostics, not production trading claims.

## Repository Structure

```text
QuantProjects-main/
├── pairs-trading-ai-tech/
├── Crypto_Cross-sectional_momentum/
├── cvar_var_risk_pipeline/
└── options-research-platform/
```

## How to Read This Repository

Start with:

1. `pairs-trading-ai-tech/README.md`
2. `pairs-trading-ai-tech/notebooks/01_data_loading_validation.ipynb`
3. `pairs-trading-ai-tech/notebooks/02_pairs_selection.ipynb`
4. `pairs-trading-ai-tech/notebooks/03_portfolio_backtest_v2.ipynb`
5. `pairs-trading-ai-tech/src/`
6. `pairs-trading-ai-tech/tests/`

## Disclaimer

This repository is for research, learning, and portfolio demonstration only. It does not provide investment advice or production trading recommendations.
