# Design Methodology for Pairs Trading 

## V1 Design Scope and Limitations:

 - selected 10 stock universe
 - 5 year: 2020 to 2024 date range
 - strictly IS only modelling; no OOS split
 - no rebalancing or walk-forward splits
 - Survivorship and look ahead bias evident as stocks were chosen in 2026.
 - no design rule for stock selection other than large cap tech stocks, which were familiar
 - transaction costs briefly accounted for on the spread level
 - static hedge model
 - Newey west tstats are implemented due to autocorrelation and heteroskedasticity.
 - Lags = 5.

 ## V2 Design Scope:

 ### Data Window

 - Start_Date: 2019-01-01
 - End_Date: 20205-12-31

 ### Universe Construction

 - Static Universe: US Top 50 Stocks 2019 v1
 - Snapshot Date: The data reflects market closing values as of December 31, 2018.
 - Source: The ranking is derived from historical market capitalization data aggregated by RelBanks and cross-referenced with Financial Times records, which track daily market valuations of public corporations.
 - Method: Universe derived from historical large-cap rankings around year-end 2018 and manually verified
 - Known limitations: Static Dataset with survivorship bias
 
 ### Train / Test / OOS Split

 - Train: 3 years
 - Test: 1 year
 - OOS: 1 year

 ### Walk-Forward Design

 - Fold 1: 2019-2021 / 2022 / 2023
 - Fold 2: 2020-2022 / 2023 / 2024
 - Fold 3: 2021-2023 / 2024 / 2025

 ### Pair Selection Frequency

 - Quarterly reselection

 ### Trading Logic

 - Signal-driven entry and exit
 - No arbitrary rebalancing

 ### Fold Comparison Metrics

 - Sharpe Ratio
 - Return
 - Max Drawdown
 - Hit Rate
 - Turnover
 - Annualized alpha

 ## Future Improvements

  - Dynamic universe construction
  - Surviviorship-bias handling
  - Transaction costs and slippage
  - Larger universe