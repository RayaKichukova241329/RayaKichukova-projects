# LSTM experiments

Eleven documented experiments, from a simple recurrent baseline to a stacked bidirectional LSTM with multi-head attention, BPE tokenisation and focal loss. All were trained on the translated Bulgarian corpus and tested on 653 sentences of real spoken Bulgarian.

![Validation against test macro F1 for the eleven experiments](../figures/lstm_validation_vs_test.png)

| # | Model | Test accuracy | Test macro F1 | Validation macro F1 | What it showed |
|---|---|---|---|---|---|
| 1 | Bidirectional RNN, learned embeddings | 0.481 | 0.302 | n/r | Severe overfitting (training 77.9%, validation 58.3%) and an extreme bias between classes. |
| 2 | Bidirectional RNN, heavily regularised | 0.460 | 0.316 | 0.578 | Regularisation removed the overfitting but exposed the real problem: a gap between book text and spoken test data. |
| 3 | Bidirectional RNN, custom pre-computed embeddings | 0.480 | 0.188 | 0.295 | Collapsed to a near-trivial classifier: anger, disgust and surprise were never predicted. |
| 4 | Bidirectional RNN, tuned | 0.429 | 0.289 | 0.582 | Tuning could not fix the data and embedding problem; longer training only overfitted. |
| 5 | Bidirectional LSTM, custom embeddings | 0.500 | 0.185 | 0.324 | LSTM instead of RNN made no difference, so the embeddings were the bottleneck. |
| 6 | Bidirectional LSTM, FastText embeddings | 0.564 | 0.304 | 0.501 | First good embeddings and the best accuracy so far, but surprise still failed. |
| 7 | Bidirectional LSTM, FastText, aggressive class balancing | 0.331 | 0.257 | 0.661 | Highest validation score (0.661) and the lowest test accuracy (33%). Duplicating minority samples fitted the artificially balanced validation set, not reality. |
| 8 | Bidirectional LSTM, FastText, class weights | 0.403 | 0.326 | 0.467 | **Best test macro F1.** Class weights beat resampling. |
| 9 | BiLSTM with self-attention, trainable embeddings, undersampling | 0.380 | 0.300 | 0.597 | Undersampling to the smallest class threw away 87% of the data and the model overfitted. |
| 10 | Stacked BiLSTM, multi-head attention, BPE tokens, focal loss | 0.430 | 0.319 | 0.530 | The most balanced model: the only one with no emotion at zero F1. Close to the ceiling for LSTMs. |
| 11 | Experiment 10, tuned over 12 random configurations | 0.556 | 0.318 | 0.591 | Tuning gave no improvement: all 12 configurations landed in a narrow band. |

n/r: not reported in the log (validation accuracy was 58.3%).

## What the experiments taught me

- **Embeddings were the first bottleneck.** Learned and custom embeddings (experiments 1 to 5) could not carry emotion. Pretrained FastText vectors (experiment 6) were the first step up.
- **A good validation score can mislead.** Experiments 7 and 9 scored 0.66 and 0.60 on validation and 0.26 and 0.30 on test. The validation sets came from the same translated written text as the training data, so they said little about spoken Bulgarian.
- **Resampling hurt.** Oversampling by duplication (7) and undersampling to the smallest class (9) were both worse than simply weighting the classes (8).
- **Architecture hit a ceiling.** Attention, BPE tokenisation and focal loss (10) and a 12-configuration search (11) all landed at a test macro F1 of about 0.32. That is why the team moved to a pretrained transformer, which reached 0.42.

Details of the search in [`hyperparameter-tuning.md`](hyperparameter-tuning.md). Back to the [project README](../README.md).
