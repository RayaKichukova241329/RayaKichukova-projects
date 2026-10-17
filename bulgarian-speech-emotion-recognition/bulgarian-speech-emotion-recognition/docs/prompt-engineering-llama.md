# Prompt engineering with Llama

A separate track: can a large language model classify the emotion of a Bulgarian sentence without any training? Twenty documented iterations, from a zero-shot baseline on a small Llama model to self-consistency voting on a 70B model. The code is in [`notebooks/04_prompt_engineering_llama.ipynb`](../notebooks/04_prompt_engineering_llama.ipynb).

## Setup

- **Models:** Llama 3.2 3B first, then Llama 3.3 70B from iteration 7, served through an Open WebUI server. The server address and key are read from the environment variables `OPENWEBUI_URL` and `OPENWEBUI_API_KEY`.
- **Data:** a separate set of 1,005 Bulgarian sentences with seven emotion labels. Neutral is 452 of them, so the classes are imbalanced. The early iterations ran on small samples, the later ones on the full set.
- **Metric:** macro F1, because accuracy rewards guessing the majority class.

## Results

| Iteration | Model | Technique | Macro F1 |
|---|---|---|---|
| 1 | 3B | Zero-shot baseline | 0.162 |
| 2 | 3B | Few-shot prompt | 0.491 |
| 3 | 3B | Structured instructions | 0.406 |
| 4 | 3B | Several techniques combined | 0.362 |
| 5 | 3B | Focused prompting on difficult emotions | 0.300 |
| 6 | 3B | Few-shot, full dataset | 0.368 |
| 8 | 70B | Few-shot, full dataset | 0.565 |
| 14 | 70B | Anti-neutral-bias prompt | 0.518 |
| 16 | 70B | Majority vote of 3 answers | 0.530 |
| **20** | **70B** | **Refined self-consistency with better label extraction** | **0.589** |

The other iterations tried prompt and temperature changes, balanced few-shot examples, five votes instead of three and best-of-N sampling.

## Final result

Llama 3.3 70B with a refined prompt and three-vote self-consistency: **macro F1 0.59**, accuracy 0.70, weighted F1 0.69 on the 1,005 sentences.

| Emotion | Precision | Recall | F1 | Sentences |
|---|---|---|---|---|
| Anger | 0.49 | 0.39 | 0.43 | 51 |
| Disgust | 0.48 | 0.59 | 0.53 | 22 |
| Fear | 0.73 | 0.53 | 0.61 | 66 |
| Happiness | 0.81 | 0.62 | 0.70 | 187 |
| Neutral | 0.72 | 0.85 | 0.78 | 452 |
| Sadness | 0.66 | 0.65 | 0.66 | 188 |
| Surprise | 0.52 | 0.33 | 0.41 | 39 |

## What it showed

- **Model size mattered more than prompt design.** Moving from 3B to 70B lifted macro F1 on the full set from 0.37 to 0.57. Every prompt trick after that added only a few points.
- **Neutral bias is hard to prompt away.** Anti-neutral prompts and voting helped a little but never closed the gap on the rare emotions.
- **It missed the target.** The notebook aimed for a weighted F1 above 0.85 and reached 0.69.
- **The 0.59 is not comparable to the 0.42 of the fine-tuned transformer.** They were measured on different sentence sets.

Back to the [project README](../README.md).
