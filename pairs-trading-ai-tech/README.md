# Pairs Trading Research Pipeline

## 1. Overview

This project is a modular pairs trading research pipeline for large-cap U.S. equities.

The project began as a single-pair statistical arbitrage backtest and has evolved into a V2 research framework with:

* expanded universe construction,
* walk-forward validation,
* fold-wise pair selection,
* transaction-cost modeling,
* portfolio construction,
* test and out-of-sample evaluation,
* and reproducible research outputs.

The goal is not simply to produce a high Sharpe ratio, but to test whether statistically selected equity pairs survive realistic validation and implementation assumptions.

## 2. Research Objective

The central research question is:

> Can a cointegration-based equity pairs strategy generate robust portfolio-level returns across multiple train/test/OOS folds after realistic transaction costs and portfolio construction assumptions?

The project evaluates:

* whether selected pairs are stable through time,
* whether signals survive out-of-sample testing,
* whether performance is sensitive to transaction costs,
* whether portfolio construction materially changes results,
* and whether the strategy behaves as a market-neutral strategy.

## 3. Current Status

V1 implemented a basic single-pair backtest.

V2 expands the framework into a multi-pair portfolio research process.

Current V2 components include:

* 50-stock universe,
* 1,225 candidate pairs,
* 3 walk-forward folds,
* fold-wise pair selection,
* cost model,
* portfolio weighting module,
* test and OOS portfolio backtests,
* and structured outputs for further analysis.

Notebook 4 / final research analysis is planned as the final synthesis layer.

## 4. Methodology

### 4.1 Data

The project uses adjusted close prices and adjusted volume data.

Dollar volume is computed to support liquidity filtering.

### 4.2 Validation

Input data is validated before modeling.

Validation checks include:

* DataFrame type,
* non-empty data,
* datetime index,
* duplicate timestamp checks,
* minimum observation count,
* missing value thresholds,
* positive price validation,
* and required asset coverage.

### 4.3 Universe Construction

V2 uses an expanded 50-stock large-cap U.S. equity universe.

This is a static research universe and is documented as a limitation. Future versions may move toward dynamic or survivorship-aware universe construction.

### 4.4 Pair Selection

Candidate pairs are filtered using:

* correlation,
* Engle-Granger cointegration,
* half-life,
* liquidity,
* and minimum observation count.

Pairs are ranked using statistical and practical selection criteria.

### 4.5 Walk-Forward Design

The V2 framework uses 3 rolling folds:

| Fold | Train     | Test | OOS  |
| ---- | --------- | ---- | ---- |
| 1    | 2019-2021 | 2022 | 2023 |
| 2    | 2020-2022 | 2023 | 2024 |
| 3    | 2021-2023 | 2024 | 2025 |

Pairs are selected using training data only.

### 4.6 Transaction Costs

The project includes a configurable cost model with:

* commission,
* bid-ask spread,
* slippage,
* market impact,
* borrow cost,
* financing cost,
* and tax/friction proxy.

The goal is to evaluate both gross and cost-adjusted performance.

### 4.7 Portfolio Construction

The portfolio module supports multiple weighting methods, including:

* equal weight,
* rank-based weighting,
* inverse half-life weighting,
* and inverse volatility weighting.

This allows the project to test whether results depend heavily on a single portfolio construction assumption.

### 4.8 Metrics

Performance evaluation includes:

* cumulative return,
* annualized return,
* volatility,
* Sharpe ratio,
* max drawdown,
* hit rate,
* turnover,
* t-statistics,
* and planned benchmark-relative metrics such as alpha, beta, and correlation versus SPY.

## 5. Notebooks

| Notebook                           | Purpose                                                   |
| ---------------------------------- | --------------------------------------------------------- |
| `01_data_loading_validation.ipynb` | Load and validate price and volume data                   |
| `02_pairs_selection.ipynb`         | Generate folds and select pairs per training window       |
| `03_portfolio_backtest_v2.ipynb`   | Run pair-level and portfolio-level test/OOS backtests     |
| `04_research_analysis.ipynb`       | Planned final research comparison and robustness analysis |

## 6. Source Modules

| Module              | Purpose                                |
| ------------------- | -------------------------------------- |
| `data_validator.py` | Price and volume validation            |
| `pair_selection.py` | Pair filtering and ranking             |
| `spread_model.py`   | Hedge ratio, spread, and z-score logic |
| `backtest.py`       | Pair-level backtest logic              |
| `walk_forward.py`   | Fold generation and fold slicing       |
| `cost_model.py`     | Transaction-cost assumptions           |
| `portfolio.py`      | Portfolio weighting and aggregation    |
| `metrics.py`        | Performance metrics                    |

## 7. Key Research Observations So Far

Initial V2 pair selection showed:

* Fold 1: 50 selected pairs
* Fold 2: 50 selected pairs
* Fold 3: 24 selected pairs
* Common pairs across all folds: 6

This suggests that pair selection is regime-dependent. Pair identities change through time, even when the mean-reversion characteristics of surviving pairs remain broadly similar.

## 8. How to Run

Create and activate a virtual environment.

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

Recommended notebook order:

```text
01_data_loading_validation.ipynb
02_pairs_selection.ipynb
03_portfolio_backtest_v2.ipynb
```

## 9. Outputs

Outputs include:

* selected pairs per fold,
* pair-level model artifacts,
* portfolio backtest tables,
* summary metrics,
* and figures.

Generated outputs are stored in the `outputs/` directory.

## 10. Limitations

Current limitations include:

* static universe construction,
* possible survivorship bias,
* simplified transaction-cost assumptions,
* limited benchmark-relative analysis,
* no stress-testing layer yet,
* and no live trading/execution integration.

## 11. Roadmap

Near-term:

* finish Notebook 3 cleanup,
* add Notebook 4 research analysis,
* tidy outputs folder,
* add benchmark-relative metrics,
* polish README and documentation.

Future:

* stress testing,
* dynamic universe construction,
* stronger survivorship-bias controls,
* regime detection,
* and expanded statistical diagnostics.

## 12. Disclaimer

This project is for research and educational purposes only. It is not investment advice and does not represent a production trading system.
