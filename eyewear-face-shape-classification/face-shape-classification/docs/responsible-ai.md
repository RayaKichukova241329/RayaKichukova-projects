# Responsible AI

Bias in the dataset, a fairness approach, and an explanation of what the model looks at.

## Bias in the dataset

The images were collected from the web. A search for "round face shape" returned:

| Group | Images |
|---|---|
| Caucasian | 80 |
| Asian | 40 |
| African-American | 26 |
| Latino-American | 0 |

The dataset does not reflect the diversity of the population. Models trained on skewed faces tend to misread under-represented groups, which can reinforce stereotypes and exclude people. In applications such as face recognition, beauty filters, hiring or healthcare, those errors can become real discrimination. Ethnicity is a sensitive attribute, so an imbalance like this is a fairness risk, not only an accuracy problem.

## Fairness approach

I proposed **fairness through awareness**: acknowledge differences between groups so that similar individuals receive equitable treatment. Simply ignoring ethnicity ("fairness through unawareness") would let the model reproduce the bias in the data. In practice this means balancing the dataset through additional collection and augmentation, and applying fairness-aware techniques so that no group is systematically favoured.

I also made an infographic on **group fairness metrics** (demographic parity, equalised odds and calibration) and had it reviewed by a peer. It is not included here.

## Explainability with Grad-CAM

Grad-CAM shows which image regions drive a prediction. I chose it over LIME because it produces consistent, class-specific heatmaps that localise features such as the jawline and cheekbones, and it needs no change to the model or retraining.

```python
from xplique.attributions import GradCAM
from xplique.plots import plot_attributions

explainer = GradCAM(model=model, output_layer=-1, batch_size=16, conv_layer=None)
explanations = explainer.explain(images, predicted_classes_one_hot)
plot_attributions(explanations, images, img_size=5, cmap="cividis", cols=3, alpha=0.6)
```

**What it showed:** applied to the first CNN (about 37% accuracy), the heatmaps concentrated on the jawline, cheeks and forehead, the regions that matter for face shape. The activations were weak and diffuse, which reflects the model's uncertainty. The model attends to the right areas but is not yet confident.

**Next steps it points to:** a larger, balanced set of front-facing images, face alignment to reduce the effect of head tilt and expression, and facial landmarks to isolate the chin and cheekbones.

The heatmaps themselves are not published, because they are overlaid on photographs of real people.

Back to the [project README](../README.md).
