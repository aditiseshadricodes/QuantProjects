# VaR / CVaR Risk Pipeline

A small Python project that estimates downside risk using historical, parametric, and Monte Carlo approaches.

## Project Overview
This project builds a simple risk analytics pipeline to compare Value at Risk (VaR) and Conditional Value at Risk (CVaR) under different methodologies.

The pipeline:
- generates a stylized portfolio return series,
- computes historical VaR and CVaR,
- computes parametric VaR and CVaR,
- computes Monte Carlo VaR and CVaR,
- calculates additional portfolio risk metrics,
- and saves summary outputs and visualizations.

## Methods Included

### 1. Historical VaR / CVaR
Uses the empirical return distribution directly.

### 2. Parametric VaR / CVaR
Assumes returns are normally distributed and estimates risk using the sample mean and standard deviation.

### 3. Monte Carlo VaR / CVaR
Simulates returns from a fitted normal distribution and estimates tail losses from the simulated sample.

## Additional Metrics
- Mean daily return
- Daily volatility
- Maximum drawdown

## Outputs
The project saves:
- `risk_summary.csv`
- `portfolio_metrics.csv`
- `portfolio_returns_histogram.png`
- `cumulative_wealth.png`
- `drawdown.png`

## Tools
- Python
- NumPy
- Pandas
- SciPy
- Matplotlib

## Why this project
This project demonstrates practical Python-based risk analysis and a clean workflow for comparing empirical, parametric, and simulation-based tail-risk estimation.

## Notes
This is a simplified educational project and not a production-grade institutional risk engine.
