# Pairs Trading Research Pipeline

## Overview
One paragraph: config-driven Python research pipeline for pair selection, spread modeling, backtesting, and performance diagnostics.

## Project Objective
Explain relative-value / mean-reversion research.

## Pipeline
Data loading → validation → pair selection → hedge model → z-score → backtest → metrics.

## Methodology
- Adjusted close and adjusted volume
- Dollar-volume liquidity filter
- Correlation
- Engle-Granger cointegration
- Half-life
- OLS hedge ratio
- Spread and rolling z-score
- Lagged positions
- Transaction-cost-adjusted returns
- Newey-West adjusted t-stat

## V1 Results
Include key META_CRM numbers.

## Visuals
Embed cumulative return and drawdown images.

## Limitations
In-sample, small static universe, no walk-forward, simplified costs, no slippage, no portfolio aggregation yet.

## V2 Roadmap
Expanded universe, OOS validation, walk-forward pair selection, full cost model, portfolio construction, pytest, config validation.

## Repository Structure
Show folders and files.

## How to Run
Mention config, notebooks, and output artifacts.

## Disclaimer
Research project only; not investment advice.

# V1 Result
The V1 META_CRM backtest generated a 269.8% final cumulative return, 30.0% annualized return, 0.81 Sharpe ratio, and a Newey-West adjusted t-statistic of 2.34. However, the strategy also experienced a -35.4% maximum drawdown, so the result is treated as an in-sample research finding requiring further robustness testing.