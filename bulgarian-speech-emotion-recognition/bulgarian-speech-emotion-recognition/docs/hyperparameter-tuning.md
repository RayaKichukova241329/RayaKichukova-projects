# Hyperparameter tuning of the final LSTM

A random search over 12 configurations of the stacked bidirectional LSTM with multi-head attention, BPE tokenisation and focal loss (gamma 2.0, alpha 0.75), ranked by validation macro F1.

| Config | Embedding | LSTM units | Layers | Dropout (LSTM, dense) | Learning rate | Batch | Epochs | Validation F1 | Test F1 | Test accuracy |
|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 256 | 512 | 2 | 0.3, 0.5 | 0.0001 | 128 | 9 | 0.601 | 0.314 | 0.556 |
| 7 | 128 | 512 | 2 | 0.3, 0.5 | 0.0001 | 128 | 9 | 0.598 | 0.299 | 0.564 |
| 1 | 128 | 384 | 2 | 0.3, 0.4 | 0.0001 | 128 | 9 | 0.597 | 0.299 | 0.547 |
| 5 | 256 | 384 | 2 | 0.3, 0.5 | 0.0002 | 128 | 8 | 0.596 | 0.305 | 0.562 |
| 3 | 256 | 512 | 1 | 0.3, 0.5 | 0.0002 | 256 | 8 | 0.594 | 0.285 | 0.570 |
| 2 | 128 | 384 | 1 | 0.3, 0.4 | 0.0001 | 128 | 9 | 0.594 | 0.278 | 0.545 |
| 9 | 256 | 512 | 1 | 0.3, 0.5 | 0.0001 | 256 | 9 | 0.592 | 0.295 | 0.553 |
| 10 | 128 | 512 | 1 | 0.3, 0.5 | 0.0002 | 256 | 8 | 0.592 | 0.287 | 0.553 |
| 12 | 256 | 512 | 2 | 0.4, 0.4 | 0.0001 | 256 | 8 | 0.588 | 0.291 | 0.554 |
| 4 | 256 | 384 | 1 | 0.4, 0.4 | 0.0002 | 256 | 8 | 0.585 | 0.284 | 0.542 |
| 11 | 128 | 512 | 1 | 0.3, 0.4 | 0.0001 | 128 | 8 | 0.583 | 0.283 | 0.551 |
| 6 | 128 | 512 | 1 | 0.3, 0.4 | 0.0002 | 256 | 8 | 0.573 | 0.286 | 0.554 |

Test macro F1 across all 12 configurations ranged from 0.278 to 0.314.

## Best configuration and final model

Configuration 8: embedding 256, 2 LSTM layers of 512 units, dropout 0.3 and 0.5, learning rate 0.0001, batch size 128.

| | Epochs | Validation F1 | Test F1 | Validation accuracy | Test accuracy |
|---|---|---|---|---|---|
| Best configuration (tuning) | 9 | 0.601 | 0.314 | 0.742 | 0.556 |
| Final model (full training) | 9 | 0.591 | 0.318 | 0.745 | 0.556 |

The final model trained for 9 epochs, with the training loss falling to 0.13 while the best validation loss was 0.29. The gap between a validation F1 of about 0.6 and a test F1 of about 0.3 is the domain gap, not a tuning problem.

Back to the [LSTM experiments](lstm-experiments.md).
