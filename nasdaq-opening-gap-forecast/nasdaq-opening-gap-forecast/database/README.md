# Database

The team stored all price data in a PostgreSQL database that I designed and built, so that every model read from one source of truth and wrote its results back to it.

## Source data

Two raw tables were loaded from CSV exports:

| Table | Content | Size |
|---|---|---|
| `stock_indices` | Daily open, close and adjusted close for the seven international indices | about 10,000 rows |
| `nasdaq_100_daily` | Daily open and close for each NASDAQ-100 company | about 224,000 rows |

The NASDAQ-100 index prices were loaded from a third source table. The price data itself is not published: see [`../data/README.md`](../data/README.md).

## Design draft: `01_dimensional_model_design.sql`

A dimensional (star) model with one fact table and three dimensions.

| Table | Role |
|---|---|
| `date_dim`, `company`, `stock_index` | Dimensions for date, company and index |
| `daily_company_index_data` | Fact table with open, close and adjusted close, keyed by date, company and index, with foreign keys to the dimensions |
| `daily_company_index_data_partitioned` | The same fact table, range-partitioned by date |
| `model_ready_data` | A join of company prices with the adjusted close of the international indices, with types, constraints and indexes |

## Schema used by the models: `02_project_schema.sql`

A schema called `project_schema` with three tables:

| Table | Content |
|---|---|
| `nasdaq_table` | NASDAQ-100 open and close prices, labelled `NASDAQ` |
| `indices_table` | The other global indices (CAC, DAX, FTSE, Hang Seng, NIFTY, Nikkei, Shanghai Composite) |
| `daily_index_stats` | The two combined: the table the machine learning notebook reads |

Transformations: kept only date, open and close, labelled the NASDAQ rows explicitly, dropped volume, dividends and splits, and combined everything into one unified table. The notebook read `daily_index_stats`, and the final predictions were written back to a results table.

## Design choices

| Concern | Decision |
|---|---|
| **Reliability** | A primary key on `(date_value, stock_index)` prevents duplicates. `CHECK` constraints prevent negative prices. Types are fixed to `DATE` and `NUMERIC(12,4)`. |
| **Speed** | Indexes on `date_value` and `stock_index`. Partitioning by date is possible later. |
| **Privacy** | No personal data is stored. |
| **Security** | Schema-level access control, ready for per-role permissions in PostgreSQL. |
| **Clarity** | A central fact table keeps analytical queries simple and makes it easy to add dimensions. |

## Possible extensions

| Table | Purpose |
|---|---|
| `users` | Track usage of predictions per user |
| `predictions` | Store model outputs and confidence scores |
| `volatility_metrics` | Add rolling volatility features (5-day, 20-day) |
| `sector_clusters` | Enable sector-level predictions, the future direction from the proposal |

Back to the [project README](../README.md).
