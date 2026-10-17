# Data

None of the data is published. The training corpus was built from third-party datasets and machine translation, the test set comes from a television show, and the licences do not allow redistribution.

## Training corpus: 608,540 sentences

Built by the team in three stages:

1. **Foundational data and translation:** existing emotion datasets were identified and aggregated, machine-translated into Bulgarian, and used to train a baseline model.
2. **Large-scale automated labelling:** the corpus was expanded by labelling more text automatically, keeping only high-confidence predictions, and then balancing it.
3. **AI-driven verification and cleaning:** a review for consistency and refinement of the labels.

| Emotion | Sentences |
|---|---|
| Neutral | 349,245 |
| Sadness | 90,404 |
| Fear | 54,348 |
| Happiness | 46,643 |
| Anger | 34,916 |
| Disgust | 17,363 |
| Surprise | 15,621 |

The corpus is heavily imbalanced, with more than half of it neutral. The LSTM experiments split it 80/20 into training and validation data, and tried several ways of balancing it.

## Test set: 653 sentences of real speech

Transcripts of spoken Bulgarian, inspected, corrected and cleaned by hand, and annotated by the team with emotions. It is the only data that resembles what the final pipeline sees, which is why it is the number that matters.

Every sentence has two labels: one from **reading** the text and one from **listening** to the audio. The two disagree on 32% of the sentences (211 of 651 with both labels), which shows how ambiguous the task is. The LSTM notebooks score against the read labels.

## Prompt-engineering set: 1,005 sentences

A separate labelled set used to evaluate the Llama prompts. Its results are not comparable with the test set above.

## Files the notebooks expect

| File | Content |
|---|---|
| `FINAL_but_cooler.pkl` | The training corpus |
| `NLP_features_engineered_but_even_cooler.csv` | The test sentences with their annotations and NLP features |
| `Prompt_data.csv`, `Test_set.csv` | The Llama evaluation sets |
| `cc.bg.300.bin` | Pretrained FastText vectors for Bulgarian |

## Why the data is a limit

The gap between translated written text and spoken Bulgarian is the main reason the LSTMs scored 0.6 on validation and 0.3 on the test set. Emotion labels are also ambiguous: annotators often disagree, so there is a ceiling on how well any model can score.
