# Quantitative Finance Research Projects

This repository contains a collection of quantitative finance projects built in
Python. The focus is on research process, data validation, backtesting discipline,
risk measurement, and clear communication of results.

The projects are works in progress at different stages of maturity. The strongest
current project is the pairs trading research pipeline, which is being developed
into a full walk-forward and out-of-sample research framework.

## Project Index

| Project | Status | Focus | Main Signal |
|---|---|---|---|
| `pairs-trading-ai-tech` | Active WIP | Equity pairs trading research pipeline | Validation, pair selection, walk-forward design, portfolio-level testing |
| `Crypto_Cross-sectional_momentum` | Completed notebook research | Crypto momentum strategy research | Train/validation/OOS comparison and Newey-West diagnostics |
| `cvar_var_risk_pipeline` | Completed small project | VaR and CVaR risk analytics | Historical, parametric, and Monte Carlo tail-risk estimation |
| `options-research-platform` | Early WIP scaffold | Options analytics and risk tooling | Config and validation groundwork; pricing/Greeks modules planned |

## Featured Project: Pairs Trading Research Pipeline

The main project in this repository is a modular pairs trading research pipeline
for large-cap U.S. equities.

The project is designed to answer a practical research question:

> Can statistically selected equity pairs produce robust test and out-of-sample
> returns after realistic validation, portfolio construction, and cost modeling?

Current components include:

- config-driven data loading and universe management,
- price and volume matrix validation,
- liquidity filtering using average dollar volume,
- correlation and Engle-Granger cointegration screening,
- hedge-ratio estimation and spread construction,
- half-life and z-score diagnostics,
- signal generation with lagged positions to reduce lookahead bias,
- pair-level backtesting,
- walk-forward train/test/OOS fold design,
- portfolio weighting methods,
- portfolio-level performance metrics,
- Newey-West adjusted t-statistics,
- transaction-cost modeling utilities,
- pytest coverage for validators, config loading, costs, and portfolio weights.

Pairs V2 is not complete yet. The current results are treated as research
diagnostics, not as evidence of a deployable trading strategy. Early portfolio
tests show regime instability and mixed out-of-sample behavior, which is an
important part of the research conclusion rather than something to hide.

## Research Principles

These projects prioritize:

- avoiding lookahead bias where possible,
- separating training, testing, and out-of-sample evaluation,
- validating inputs before modeling,
- documenting assumptions and limitations,
- reporting weak or unstable results honestly,
- using statistical diagnostics instead of relying only on headline returns,
- keeping notebooks readable as research reports rather than scratchpads.

## Repository Structure

```text
QuantProjects-main/
├── pairs-trading-ai-tech/
│   ├── config/
│   ├── notebooks/
│   ├── outputs/
│   ├── src/
│   └── tests/
├── Crypto_Cross-sectional_momentum/
├── cvar_var_risk_pipeline/
└── options-research-platform/
```

## How To Read This Repository

For the best signal, start here:

1. `pairs-trading-ai-tech/README.md`
2. `pairs-trading-ai-tech/design_notes.md`
3. `pairs-trading-ai-tech/notebooks/02_pairs_selection.ipynb`
4. `pairs-trading-ai-tech/notebooks/03_portfolio_backtest_v2.ipynb`
5. `pairs-trading-ai-tech/src/`
6. `pairs-trading-ai-tech/tests/`

The crypto momentum and VaR/CVaR projects are smaller supporting projects. The
options research platform is intentionally early-stage and should be read as a
scaffold for future derivatives analytics work, not as a finished project.

## Current Cleanup Roadmap

The next repository improvements are:

- rewrite the pairs trading README as a complete employer-facing case study,
- clean dependency files into minimal UTF-8 `requirements.txt` files,
- move notebook-only V2 portfolio aggregation logic into tested source modules,
- apply the configured transaction-cost assumptions consistently in V2,
- add passive benchmark comparisons,
- expand tests for lookahead prevention and portfolio aggregation,
- clearly label or archive incomplete options modules until implemented.

## Disclaimer

This repository is for research, learning, and portfolio demonstration only. It
does not provide investment advice or production trading recommendations.
