# Pairs Trading in AI and Technology Stocks

This project tests whether temporary deviations between related AI and technology equities can be traded profitably through a mean-reversion strategy.

## Data source
- Tiingo API for historical adjusted price data

## Initial candidate pairs
- NVDA / AMD
- AMD / INTC
- NVDA / AVGO
- MSFT / GOOGL
- GOOGL / META
- CRM / NOW

## Core workflow
-1. Load and clean daily adjusted close data
-2. Construct pair spreads
-3. Compute rolling z-scores
-4. Generate entry and exit signals
-5. Backtest performance with transaction costs
-6. Compare robustness across pairs and parameter choices