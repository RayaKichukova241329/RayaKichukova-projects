# Research summary

## Question

To what extent do morphological evolution and digital data degradation contribute to the performance decay of modern object detection models in historical urban environments?

Prior work (Pégeot et al., 2025) studied how classification accuracy changes as the years pass. This study asks the same of object detection over 35 years, and separates two causes: poorer image quality and the changing look of cars, buildings and people.

## Design

A quantitative comparison in which no model trains on historical images. Four datasets span the period (1980s New York, 1990s Los Angeles and London, KITTI 2012, Mapillary 2017+), unified into five classes. Contemporary-only YOLOv11 models (small and nano) are fine-tuned on KITTI and Mapillary and evaluated on every period, so they measure how a modern detector copes with data from the past. The primary metric is AP@0.5 per class, with confidence 0.25 and IoU 0.5 throughout.

The proposal's null hypothesis is that temporal distance has no effect on detection performance, tested through five alternative hypotheses (H1 to H5). The multi-era models are kept as a secondary finding.

## Hypotheses

| | Prediction | Test | Result |
|---|---|---|---|
| H1 | F1 is lower on historical than modern data | Mann-Whitney U, per-class F1 (10 against 10) | **Supported:** p = 0.0008 (small), 0.0041 (nano) |
| H2 | Car, Truck and Pedestrian degrade more than Cyclist and Building | Observed ranking (5 classes is too few for a test) | **Not clearly supported:** by AP@0.5 the predicted group loses 69% (small) and 71% (nano) against 73% and 68% for Cyclist and Building; Car is among the least degraded |
| H3 | Resolution normalisation narrows the gap | Wilcoxon, per class, 320 against 640 px | **Refuted:** the gap widens for four of the five classes (p = 0.97) |
| H4 | Historical errors concentrate at the edges | Fisher's exact on pooled error counts | **Partly supported:** errors reach the outer 15% of the frame 63.2% of the time against 32.3% (small), p < 0.0001, but by box centre they sit toward the middle |
| H5 | Failure is recognition rather than localisation | Binomial on classified class-period pairs | **Refuted:** recognition failures are 4 of 18 (small) and 1 of 19 (nano) |

## Main results

- Relative mAP drop of **61.2%** (small) and **62.9%** (nano).
- Quality explains **11.2%** (small) and **22.4%** (nano) of the drop. Ageing a modern photo to look like the 1980s costs 6% and 13% of the mAP. Real 1980s photos cost 54% and 58%.
- Resolution normalisation widens the gap by **128%** (small) and **109%** (nano) from 320 to 1280 pixels.
- Error boxes reach the outer 15% of the frame about **62%** of the time on historical images against **33%** on modern ones. By box centre, errors sit toward the middle of every dataset.
- Truck and Cyclist AP@0.5 is zero on both historical periods (7 historical trucks; 121 historical cyclists, all missed). Pedestrian loses about 75%, Building 35 to 46% and Car 33 to 39%. At the default confidence threshold of 0.25 the ranking differs (Pedestrian 89%, Car 73 to 79%, Building 46 to 61%) because the model ranks historical cars sensibly but reports them with low confidence.
- Training on all four periods raised held-out 1980s mAP from about 0.15 to 0.44-0.46, with no visible loss on modern images in this small test.

## Why the finding matters

Temporal degradation is a semantic problem, not an image-restoration one. Pipelines that enhance or upscale historical images address the minority contributor and can make things worse.

## Limitations

See the README. The most important is the size of the modern held-out sets (30 images each).

Back to the [project README](../README.md).
