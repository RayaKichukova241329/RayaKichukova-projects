# Results

All values are mAP@0.5 on images the models never saw (see [`../docs/evaluation-protocol.md`](../docs/evaluation-protocol.md)). The 1980s and 1990s sets contain every image (302 and 304). KITTI and Mapillary use 30 held-out images each (contemporary-only models) or 31, 31, 30 and 30 images per period (multi-era models).

## Experiment 2: four fine-tuned models

| Model | 1980s | 1990s | KITTI | Mapillary | Historical avg | Modern avg |
|---|---|---|---|---|---|---|
| YOLOv11n contemporary | 0.133 | 0.213 | 0.614 | 0.317 | 0.173 | 0.466 |
| YOLOv11n multi-era | 0.436 | 0.659 | 0.716 | 0.331 | 0.548 | 0.524 |
| YOLOv11s contemporary | 0.153 | 0.206 | 0.590 | 0.333 | 0.179 | 0.461 |
| YOLOv11s multi-era | 0.462 | 0.660 | 0.656 | 0.385 | 0.561 | 0.520 |

Relative drop of the contemporary-only models, historical average against modern average: **61.2%** (small) and **62.9%** (nano). The multi-era models trained on all four periods and are scored on their own held-out images, so they are not directly comparable with the contemporary-only rows.

## Experiment 3: resolution normalisation

| Model | Period | 320 px | 640 px | 1280 px |
|---|---|---|---|---|
| YOLOv11s | 1980s | 0.204 | 0.153 | 0.013 |
| YOLOv11s | 1990s | 0.238 | 0.206 | 0.158 |
| YOLOv11s | KITTI | 0.440 | 0.590 | 0.475 |
| YOLOv11s | Mapillary | 0.285 | 0.333 | 0.342 |
| YOLOv11n | 1980s | 0.144 | 0.133 | 0.088 |
| YOLOv11n | 1990s | 0.208 | 0.213 | 0.153 |
| YOLOv11n | KITTI | 0.411 | 0.614 | 0.506 |
| YOLOv11n | Mapillary | 0.237 | 0.317 | 0.354 |

| Model | Gap at 320 | Gap at 640 | Gap at 1280 | Change, 320 to 1280 |
|---|---|---|---|---|
| YOLOv11s | 0.142 | 0.282 | 0.323 | +127.9% |
| YOLOv11n | 0.148 | 0.293 | 0.310 | +108.6% |

The gap is the modern average minus the historical average.

## Experiment 4: quality or morphology?

Held-out Mapillary images, aged to match the contrast and brightness of the 1980s photos.

| Model | Original | Aged | Real 1980s | Quality share | Morphology share |
|---|---|---|---|---|---|
| YOLOv11s | 0.333 | 0.313 | 0.153 | 11.2% | 88.8% |
| YOLOv11n | 0.317 | 0.276 | 0.133 | 22.4% | 77.6% |

The ageing pipeline cannot reproduce historical sharpness, so the quality share is a lower bound and the morphology share an upper bound.

## SQ3: edge error rate

Share of false positives and false negatives whose box reaches into the outer 15% of the frame on any side (the edge-reach rate).

| Model | 1980s | 1990s | KITTI | Mapillary | Historical avg | Modern avg | Gap |
|---|---|---|---|---|---|---|---|
| YOLOv11s | 61.1% | 64.5% | 33.5% | 31.8% | 62.8% | 32.7% | 30.2 points |
| YOLOv11n | 61.0% | 60.7% | 34.1% | 31.3% | 60.8% | 32.7% | 28.1 points |

Because large boxes reach the border almost by construction, there is no simple uniform baseline for this measure, and the comparison between periods is the evidence.

Measured by box centre instead, from the notebook's error heatmaps, the share of errors in the outer 15% border is 29.8% (1980s), 37.7% (1990s), 20.1% (KITTI) and 24.6% (Mapillary). A uniform spread of centres would give about 51%, so errors sit toward the middle in every dataset, with historical shares higher than modern ones.

## Per-class AP@0.5 (Ultralytics, full precision-recall curve)

Computed from the per-class values in the Experiment 2 heatmap (rounded to two decimals), averaged over the two historical and the two modern sets.

| Class | v11s historical | v11s modern | v11s drop | v11n historical | v11n modern | v11n drop |
|---|---|---|---|---|---|---|
| Truck | 0.000 | 0.285 | 100% | 0.000 | 0.340 | 100% |
| Cyclist | 0.000 | 0.200 | 100% | 0.000 | 0.285 | 100% |
| Pedestrian | 0.155 | 0.630 | 76% | 0.135 | 0.540 | 75% |
| Building | 0.240 | 0.445 | 46% | 0.285 | 0.440 | 35% |
| Car | 0.500 | 0.745 | 33% | 0.445 | 0.725 | 39% |

Truck rests on 7 historical instances and Cyclist on 121 (all missed). The modern Truck and Cyclist values rest on few instances in the 30-image held-out sets.

## SQ4: per-class vulnerability

Approximate AP@0.5 (11-point interpolation of detections at confidence 0.25, comparable across periods but not with the Ultralytics mAP above), averaged over the two historical and the two modern sets.

| Class | v11s historical | v11s modern | v11s drop | v11n historical | v11n modern | v11n drop |
|---|---|---|---|---|---|---|
| Truck | 0.000 | 0.205 | 100.0% | 0.000 | 0.250 | 100.0% |
| Cyclist | 0.000 | 0.115 | 100.0% | 0.000 | 0.091 | 100.0% |
| Pedestrian | 0.045 | 0.419 | 89.2% | 0.045 | 0.384 | 88.2% |
| Car | 0.133 | 0.645 | 79.4% | 0.170 | 0.623 | 72.7% |
| Building | 0.115 | 0.296 | 61.3% | 0.150 | 0.277 | 45.7% |

The SQ4 table below counts only detections above the default confidence threshold of 0.25, which is why historical Car looks far worse here than in the AP@0.5 table above.

Dominant error type (at threshold 0.25): localisation failure for every class and period on historical data. Recognition failures appear only on the modern held-out sets (4 of 18 classified class-period pairs for YOLOv11s, 1 of 19 for YOLOv11n).

## Hypothesis tests

| | Test | YOLOv11s | YOLOv11n | Verdict |
|---|---|---|---|---|
| H1 | Mann-Whitney U on per-class F1 | p = 0.0008 | p = 0.0041 | Supported |
| H2 | Observed degradation ranking (AP@0.5) | 69.3% against 72.9% | 71.1% against 67.7% | Not clearly supported |
| H3 | Wilcoxon, per-class gap, 320 against 640 | gap grew for 4 of 5 classes (p = 0.97) | gap grew for 4 of 5 classes (p = 0.97) | Refuted |
| H4 | Fisher's exact, pooled errors | 63.2% against 32.3% | 60.8% against 32.0% | Supported (p < 0.0001) |
| H5 | Binomial, localisation against recognition | 4 of 18 recognition | 1 of 19 recognition | Refuted |

H2 compares the mean AP@0.5 drop of Car, Truck and Pedestrian against Cyclist and Building (computed in Section 3.2 of the notebook).

The raw result files (`*.json`) are written to `results/` by the notebook and are not committed.

Back to the [project README](../README.md).
