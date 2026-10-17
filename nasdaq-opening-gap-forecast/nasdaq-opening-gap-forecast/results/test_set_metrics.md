# Test-set metrics

Final model: XGBoost (`gbtree`, `max_depth=3`, `learning_rate=0.005`, `n_estimators=100`, `min_child_weight=9`, `gamma=0.3`, `reg_alpha=0.5`, `reg_lambda=1`), tuned with a grid search on macro ROC-AUC using 3-fold time-series cross-validation.

**Test set:** 496 trading days, 17 February 2023 to 10 February 2025, the last 20% of the data in chronological order.

| Class | Share of test days |
|---|---|
| Down (gap of -0.4% or lower) | 18.5% |
| Flat | 53.4% |
| Up (gap of +0.4% or higher) | 28.0% |

## Final model

| | Precision | Recall | F1 | Days |
|---|---|---|---|---|
| Down | 0.34 | 0.59 | 0.43 | 92 |
| Flat | 0.61 | 0.50 | 0.55 | 265 |
| Up | 0.41 | 0.36 | 0.38 | 139 |
| **Accuracy** | | | **0.476** | 496 |
| **Macro average** | 0.45 | 0.48 | 0.45 | 496 |

Macro ROC-AUC (one-vs-rest): **0.634**.

Confusion matrix (rows are actual, columns are predicted):

| | Predicted down | Predicted flat | Predicted up |
|---|---|---|---|
| **Actual down** | 54 | 27 | 11 |
| **Actual flat** | 72 | 132 | 61 |
| **Actual up** | 33 | 56 | 50 |

## Comparison

| Model | Accuracy | Macro ROC-AUC |
|---|---|---|
| Always predict "flat" | 0.534 | not applicable |
| Linear regression (rounded) | 0.530 | 0.510 |
| Random forest | 0.514 | 0.628 |
| Neural network (MLP) | 0.502 | 0.567 |
| XGBoost, default | 0.435 | 0.629 |
| XGBoost, tuned | 0.476 | 0.634 |

## Reading the numbers

- The baseline has the highest accuracy because it always predicts the majority class. It catches none of the 231 days with a gap, which is why accuracy alone is misleading here.
- The tuned model finds 59% of down-gap days, but only about a third of the days it calls "down" actually are (precision 0.34), so it raises many false alarms.
- A macro ROC-AUC of 0.634 is a modest improvement over chance (0.5). The signal is real but weak, and it is not strong enough to trade on.

The row-level results file is not published, because it consists of values derived from market data. The figures above were recomputed from it and match the notebook output.
