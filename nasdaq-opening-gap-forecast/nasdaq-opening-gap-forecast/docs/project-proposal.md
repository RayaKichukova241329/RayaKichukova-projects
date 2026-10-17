# Project proposal and what changed

A summary of the group's proposal (27 May 2025) and how the delivered project compares with it.

## The proposal

**Problem.** The client, Move Tickers, had no system that uses overnight moves in international markets to predict how the NASDAQ-100 will open. Traders relied on late reactions or judgement, which led to inefficient hedging and slippage. General pre-market tools such as TrendSpider and LuxAlgo exist, but none specialises in overnight international data.

**Objectives**
- A daily prediction of an up, down or flat opening gap.
- Performance targets of **ROC-AUC of at least 0.70** and **F1 of at least 0.60**.
- Integration into the client's dashboards through a REST API.
- Showing which international indices contribute to each prediction, for transparency.
- Future direction: segment the NASDAQ-100 by sector, volatility or market cap and predict gaps per group.

**Planned data.** Daily closing prices of seven indices (Nikkei 225, Hang Seng, Shanghai Composite, NIFTY 50, DAX 40, CAC 40, FTSE 100), the previous U.S. close and the NASDAQ-100 open: about 3,000 rows from 2012 to 2024. Labels from gaps of 0.5% or more. Optional VIX and 5-day volatility. Quality plan: forward-fill, interpolation, z-score outlier checks, time-zone alignment and standardisation.

**Planned method.** A classification model (logistic regression first) with a chronological train and validation split, evaluated with ROC-AUC, F1, accuracy, precision and recall. Deployment as a Docker microservice in the client's Kubernetes infrastructure behind a REST API, or alternatively as a standalone Streamlit or Flask site on a cloud platform.

**Planned phases.** Four phases over weeks 4 to 7: data collection and pre-processing, model development and training, evaluation and optimisation, and deployment and integration, with a milestone at the end of each.

## Planned against delivered

| | Proposal | Delivered |
|---|---|---|
| **Period** | 2012 to 2024, about 3,000 rows | February 2015 to February 2025, 2,480 labelled trading days |
| **Gap threshold** | 0.5% | 0.4% |
| **Classes** | Up, down, flat | Up, down, flat |
| **Model** | Logistic regression | Four model types against a baseline, tuned XGBoost chosen |
| **Validation** | Chronological split | Chronological split and time-series cross-validation for tuning |
| **Targets** | ROC-AUC 0.70 or more, F1 0.60 or more | **Not reached:** macro ROC-AUC 0.634, macro F1 0.45 |
| **Extra features** | Optional VIX and 5-day volatility | Index moves, shock flags, weighted global move, 5-day global volatility, Europe against Asia |
| **Deployment** | Docker microservice behind a REST API | Streamlit dashboard, plus a packaged and tested Python project |

The performance targets were ambitious for a signal this weak. The honest result is a model that beats the baseline at catching moves but is not strong enough to trade on.

Back to the [project README](../README.md).
