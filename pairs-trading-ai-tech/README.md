# Pairs Trading Research Pipeline

## 1. Overview

This project is a modular pairs trading research pipeline for large-cap U.S. equities.

The project began as a single-pair statistical arbitrage backtest and has evolved into a V2 research framework with:

* expanded universe construction
* walk-forward validation
* fold-wise pair selection
* hedge-ratio estimation
* spread and z-score construction
* pair-level backtesting
* portfolio construction
* test and out-of-sample evaluation
* saved research outputs
* final research-summary reporting

The goal is not simply to produce a high Sharpe ratio, but to test whether statistically selected equity pairs survive disciplined validation across test and held-out OOS periods.

The current V2 results are reported as **gross / zero-cost baseline results**. Expanded transaction-cost, slippage, and stress-testing scenarios are planned for a future research iteration.

---

## 2. Research Objective

The central research question is:

> Can a cointegration-based equity pairs strategy generate robust portfolio-level returns across multiple train/test/OOS folds under a disciplined walk-forward validation framework?

The project evaluates:

* whether selected pairs remain useful through time
* whether signals survive held-out OOS validation
* whether portfolio construction materially changes results
* whether weighting methods improve robustness
* whether the framework can identify instability before overclaiming strategy performance

---

## 3. Current Status

V1 implemented a basic single-pair backtest.

V2 expands the project into a multi-pair portfolio research process with completed test and OOS evaluation.

Current V2 components include:

* 50-stock large-cap equity universe
* 1,225 candidate pairs
* 3 walk-forward folds
* fold-wise pair selection
* hedge-ratio, spread, and z-score artifacts
* pair-level test and OOS backtests
* portfolio weighting across multiple methods
* portfolio-level test and OOS metrics
* saved output tables
* saved pickle artifacts
* final research-summary notebook

The completed V2 research conclusion is that the framework is strong, but the current gross-baseline strategy results are mixed and regime-sensitive. The current configuration is **not capital-ready**.

---

## 4. Methodology

### 4.1 Data

The project uses adjusted close prices and adjusted volume data.

Dollar volume is computed to support liquidity filtering and data-quality checks.

### 4.2 Validation

Input data is validated before modeling.

Validation checks include:

* DataFrame type checks
* non-empty data checks
* datetime index validation
* duplicate timestamp checks
* minimum observation count
* missing value thresholds
* positive price validation
* required asset coverage

### 4.3 Universe Construction

V2 uses a static 50-stock large-cap U.S. equity universe selected using late-2018 market-cap information.

This is documented as a limitation. Future versions should move universe selection inside the walk-forward process so that each fold constructs its tradable universe using only training-period liquidity, price history, missing-data coverage, and tradability filters.

### 4.4 Pair Selection

Candidate pairs are filtered and ranked using:

* correlation
* Engle-Granger cointegration
* half-life
* liquidity
* minimum observation count

Pairs are selected separately for each training fold.

### 4.5 Walk-Forward Design

The V2 framework uses 3 rolling folds:

| Fold | Train | Test | OOS |
| ---- | ----- | ---- | --- |
| 1 | 2019-2021 | 2022 | 2023 |
| 2 | 2020-2022 | 2023 | 2024 |
| 3 | 2021-2023 | 2024 | 2025 |

Pairs and model artifacts are estimated using training data only. Test and OOS windows are evaluated separately.

### 4.6 Cost Assumptions

The current Notebook 04 research summary reports **gross / zero-cost baseline results**.

The project contains cost-modeling infrastructure, but expanded cost and slippage scenario analysis is planned for V3. Future scenarios should include:

* gross baseline
* base-cost scenario
* conservative-cost scenario
* slippage stress
* turnover-based cost drag

### 4.7 Portfolio Construction

The portfolio module evaluates multiple weighting methods:

* equal weight
* rank-based weighting
* inverse half-life weighting

These methods test whether portfolio aggregation improves robustness compared with pair-level signals alone.

### 4.8 Metrics

Performance evaluation includes:

* final cumulative return
* annualized return
* annualized volatility
* Sharpe ratio
* max drawdown
* hit rate
* Newey-West adjusted t-statistics
* Newey-West p-values

Notebook 04 also includes:

* test/OOS comparison tables
* equity curve visuals
* drawdown visuals
* weighting-method comparison
* key findings
* limitations
* V3 roadmap

---

## 5. Notebooks

| Notebook | Purpose |
| -------- | ------- |
| `01_data_loading_validation.ipynb` | Load and validate price and volume data |
| `02_pairs_selection.ipynb` | Generate folds and select pairs per training window |
| `03_portfolio_backtest_v2.ipynb` | Run pair-level and portfolio-level test/OOS backtests, compute metrics, and save outputs |
| `04_research_summary_v2.ipynb` | Load saved outputs and present the final V2 research summary, visuals, limitations, and V3 roadmap |

Notebook 03 is the research engine. Notebook 04 is the interpretation and reporting layer.

---

## 6. Source Modules

| Module | Purpose |
| ------ | ------- |
| `data_validator.py` | Price and volume validation |
| `pairs_selection.py` | Pair filtering and ranking |
| `spread_model.py` | Hedge ratio, spread, and z-score logic |
| `backtest.py` | Pair-level backtest logic |
| `walk_forward.py` | Fold generation and fold slicing |
| `cost_model.py` | Transaction-cost assumptions and future cost-scenario support |
| `portfolio.py` | Portfolio weighting and aggregation |
| `metrics.py` | Performance metrics and statistical diagnostics |

---

## 7. Key Research Observations

Initial V2 pair selection showed:

* Fold 1: 50 selected pairs
* Fold 2: 50 selected pairs
* Fold 3: 24 selected pairs
* Common pairs across all folds: 6

This suggests that pair selection is regime-dependent. Pair identities change through time, even when some mean-reversion characteristics remain present.

The final V2 test and OOS analysis shows mixed results. Test-period behavior does not persist consistently into OOS periods, and no weighting method demonstrates sufficiently robust performance across all folds for capital deployment.

The weighting-method comparison suggests that rank weighting is the least weak method on average in the current outputs, but the evidence is not strong enough to conclude that it solves the strategy instability.

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
04_research_summary_v2.ipynb
```

Notebook 04 should be run after Notebook 03 because it loads saved Notebook 03 outputs.

## 9. Outputs

Outputs include:

* selected pairs per fold,
* pair-level model artifacts,
* pair-level backtest summaries,
* portfolio construction summaries,
* test portfolio metrics,
* OOS portfolio metrics,
* test/OOS comparison tables,
* return, Sharpe, drawdown, and t-stat pivot tables,
* and saved pickle artifacts for return-series visualization.

Generated outputs are stored in the `outputs/` directory.

## 10. Limitations

Current limitations include:

* static universe construction based on late-2018 market-cap information,
* possible stale-universe or survivorship-related bias,
* current reported results are gross / zero-cost baseline results,
* pair selection is not yet portfolio-aware,
* no graph-based pair matching yet,
* no explicit regime filter,
* limited benchmark or factor exposure analysis,
* no stress-testing layer yet,
* no full cost/slippage scenario comparison,
* and no live trading/execution integration.

These limitations do not invalidate the framework. They define the next research iteration.

## 11. V3 Roadmap

Planned V3 improvements include:

* `universe_selector.py` for fold-level dynamic universe selection using training-period liquidity and data-quality filters,
* `pair_graph_selector.py` for graph-based pair selection and maximum weighted matching to reduce repeated ticker exposure,
* expanded gross, base-cost, and conservative-cost scenarios,
* slippage and stress-testing extensions,
* alpha decay analysis across train, test, and OOS periods,
* expanded pytest coverage across backtesting, metrics, spread modeling, pair selection, and walk-forward logic,
* CI, logging, and configuration traceability,
* benchmark and factor exposure diagnostics,
* and a capital deployment dashboard to classify strategies as deploy, paper-trade, monitor, or reject.

## 12. Disclaimer

This project is for research and educational purposes only. It is not investment advice and does not represent a production trading system.

The current V2 results do not support capital deployment. The primary value of the project is the research infrastructure: walk-forward validation, OOS evaluation, portfolio diagnostics, saved outputs, and honest strategy interpretation.

